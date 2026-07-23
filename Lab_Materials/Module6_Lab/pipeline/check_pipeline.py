"""Local deployment-policy checker for Lab 6 (no cloud, no network, stdlib only).

This is a deliberately small checker for the lab workflow, not a general GitHub Actions
parser. It ignores comments, inspects the expected ``test`` and ``deploy`` jobs, and
applies the rules in ``platform-space/deploy-standards.md``.

    python check_pipeline.py                # checks the workflow beside/in this repo
    python check_pipeline.py path/to/f.yml

Exit code 0 = all checks pass. It never runs a pipeline or contacts GitHub.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_WORKFLOW = HERE / ".github" / "workflows" / "ci.yml"
DEFAULT = REPO_WORKFLOW if REPO_WORKFLOW.exists() else HERE / "ci.yml"

SECRET_LITERALS = [
    re.compile(r"ghp_[A-Za-z0-9]{10,}"),
    re.compile(r"AKIA[0-9A-Z]{12,}"),
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
]
USES = re.compile(
    r"^\s*-\s*uses:\s*([A-Za-z0-9_.-]+/[A-Za-z0-9_.\-/]+)@([A-Za-z0-9_.-]+)\s*$",
    re.M,
)
SHA40 = re.compile(r"^[0-9a-f]{40}$", re.I)


def without_comments(text: str) -> str:
    """Remove whole-line and trailing comments from this controlled lab YAML."""
    return "\n".join(line.split("#", 1)[0].rstrip() for line in text.splitlines())


def job_block(text: str, name: str) -> str:
    """Return one two-space-indented job from the controlled lab workflow."""
    match = re.search(
        rf"(?ms)^  {re.escape(name)}:\s*$\n(?P<body>(?:^(?:    .+|\s*)$\n?)*)",
        text,
    )
    return match.group("body") if match else ""


def has_guarded_rollback(deploy: str) -> bool:
    lines = deploy.splitlines()
    for index, line in enumerate(lines):
        if "scripts/rollback.sh" not in line:
            continue
        preceding_step = "\n".join(lines[max(0, index - 6):index])
        return bool(re.search(r"if:\s*.*failure\(\)", preceding_step, re.I))
    return False


def check(text: str) -> list[tuple[str, bool, str]]:
    clean = without_comments(text)
    test = job_block(clean, "test")
    deploy = job_block(clean, "deploy")
    results: list[tuple[str, bool, str]] = []

    def add(name: str, ok: bool, hint: str) -> None:
        results.append((name, bool(ok), hint))

    # 1. Dependencies are installed in the test job before pytest runs.
    install = re.search(r"python\s+-m\s+pip\s+install[^\n]*-r\s+\S*requirements\.txt", test, re.I)
    pytest = re.search(r"(?:python\s+-m\s+)?pytest\b", test, re.I)
    deps = bool(install and pytest and install.start() < pytest.start())
    add("deps-installed", deps,
        "In the `test` job, run `python -m pip install -r requirements.txt` before pytest.")

    # 2. The test job blocks deploy and is not allowed to continue after failure.
    gates = bool(
        pytest
        and not re.search(r"continue-on-error:\s*true", test, re.I)
        and re.search(r"^\s*needs:\s*(?:\[?\s*)?test\b", deploy, re.I | re.M)
    )
    add("test-gate", gates,
        "Run `python -m pytest -q` without `continue-on-error`, and make `deploy` need `test`.")

    # 3. A full commit SHA is GitHub's immutable pin; tags are mutable.
    action_refs = USES.findall(clean)
    unpinned = [f"{action}@{ref}" for action, ref in action_refs if not SHA40.fullmatch(ref)]
    pin_detail = ", ".join(unpinned) if unpinned else ("none" if action_refs else "no action references found")
    add("actions-pinned", bool(action_refs) and not unpinned,
        f"Pin every action to a full 40-character commit SHA. Unpinned: {pin_detail}")

    # 4. Least-privilege permissions declared.
    perms = bool(
        re.search(r"^permissions:\s*$", clean, re.M)
        and re.search(r"^\s{2}contents:\s*read\s*$", clean, re.M)
        and not re.search(r"^\s{2}\S+:\s*write\s*$|^permissions:\s*write-all\s*$", clean, re.I | re.M)
    )
    add("least-privilege", perms,
        "Declare top-level `permissions:` with only `contents: read` for this workflow.")

    # 5. No hardcoded credentials; the deploy token comes from the secret store.
    literal_pattern = re.search(
        r"^\s*DEPLOY_TOKEN:\s*(?!\$\{\{\s*secrets\.DEPLOY_TOKEN\s*\}\}\s*$)\S+",
        clean,
        re.I | re.M,
    )
    known_literal = any(pattern.search(clean) for pattern in SECRET_LITERALS)
    secret_ref = re.search(
        r"^\s*DEPLOY_TOKEN:\s*\$\{\{\s*secrets\.DEPLOY_TOKEN\s*\}\}\s*$",
        clean,
        re.I | re.M,
    )
    add("no-hardcoded-secrets", bool(secret_ref) and not literal_pattern and not known_literal,
        "Reference `${{ secrets.DEPLOY_TOKEN }}`; never put a literal token in workflow YAML.")

    # 6. Production is protected and cannot deploy from a PR or ordinary push.
    manual_trigger = bool(re.search(r"^\s{2}workflow_dispatch:\s*$", clean, re.M))
    protected = bool(re.search(r"^\s*environment:\s*production\s*$", deploy, re.I | re.M))
    manual_only = bool(
        re.search(
            r"^\s*if:\s*.*github\.event_name\s*==\s*['\"]workflow_dispatch['\"]",
            deploy,
            re.I | re.M,
        )
    )
    add("prod-approval", manual_trigger and protected and manual_only,
        "Use `workflow_dispatch`, `environment: production`, and a deploy-job `if` guard so PRs never deploy.")

    # 7. Gradual rollout — no 100% blast radius on first push.
    full_blast = re.search(r"--traffic(?:=|\s+)100\b", deploy, re.I)
    canary = re.search(r"--traffic(?:=|\s+)10\b", deploy, re.I)
    add("gradual-rollout", bool(canary) and not full_blast,
        "Start the simulated production deployment at the approved 10% canary, not 100%.")

    # 8. A failed canary invokes the supplied rollback script; a comment alone cannot pass.
    add("rollback-defined", has_guarded_rollback(deploy),
        "Add a step that runs `scripts/rollback.sh` under an `if: failure()` guard.")

    return results


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    if not path.exists():
        print(f"FAIL  no workflow found at: {path}")
        print("      Pass a workflow path, or copy `ci-broken.yml` to `ci.yml` beside this checker.")
        return 2

    results = check(path.read_text(encoding="utf-8"))
    width = max(len(n) for n, _, _ in results)
    failed = 0
    print(f"Deployment policy check - {path.name}\n")
    for name, ok, hint in results:
        print(f"  [{'PASS' if ok else 'FAIL'}] {name.ljust(width)}")
        if not ok:
            print(f"         -> {hint}")
            failed += 1
    print(f"\n{len(results) - failed}/{len(results)} checks passed.")
    if failed:
        print("Fix the workflow (not this checker) until every check passes.")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

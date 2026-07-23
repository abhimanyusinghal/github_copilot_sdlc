# Lab 6 · Facilitator key

> **Facilitator notes.** Expected states, the seeded defects, and the judgement to coach.

## Pre-flight
- **Publish the template repo first.** Follow `template-repo/SETUP-FACILITATOR.md`: push `template-repo/`
  to a **public** GitHub repo and mark it a template. Confirm a CI run is **red**.
- Send participants the **pre-work**: create a free github.com account, sign in to GitHub **from VS Code**,
  install the **GitHub Pull Requests and Issues** extension. This saves 15+ minutes.
- Python **3.11** on every machine (or use CI) for the app and contract tests. The checker supports 3.10+,
  but the deliberately old dependency snapshot is not runtime-compatible with every newer Python version.
- **The repo must be public** on the free tier — Actions minutes and environment required-reviewers are free
  on public repos, not private. It holds only fictional Acme data. Verify current GitHub tiers before the session.
- **Offline substitutes cover the learning work:** if github.com is blocked, participants use
  `pipeline/failing-run.log` + `check_pipeline.py` and draft the PR/environment evidence. They must label
  hosted controls as simulated; branch protection, a merge, and a real approval click cannot be proven offline.

## Expected states
- The workflow's first run is **red** (test job fails: `pytest` not installed). If creating a participant
  repo from the template does not emit a run, use the workflow's manual **Run workflow** trigger.
- The app's own tests **pass** (`python -m pytest -q` in the repo) — so red = pipeline, not code.
- `python check_pipeline.py ci-broken.yml` (or the repo's `ci.yml`) → **1/8 passed** (only `test-gate`).
- A correctly fixed `ci.yml` → **8/8 passed**, and the PR's Actions run should go **green**. Validate both
  the reference fix and a template-repo Actions run before each delivery.
- After Ex 4, the production environment and required reviewer are configured. After the Ex 6 go/no-go,
  a manual run makes the **deploy job pause for approval**; Ship approves and Hold rejects.

## Seeded defects in `ci-broken.yml`
| Check | Defect | Fix |
| --- | --- | --- |
| `deps-installed` | `pytest` run with no install step → the failing run log | Add `python -m pip install -r requirements.txt` |
| `actions-pinned` | `actions/checkout@main`, `setup-python@main` | Use the full SHAs in `deploy-standards.md` |
| `least-privilege` | No `permissions:` block | Add `permissions: contents: read` |
| `no-hardcoded-secrets` | Fictional token committed as a literal | Use `${{ secrets.DEPLOY_TOKEN }}`; document that a real exposed token must be rotated |
| `prod-approval` | Prod runs on PR/push and has no environment | Manual-dispatch-only job + `environment: production` |
| `gradual-rollout` | `--traffic 100` on first push | Canary at 10%, then ramp |
| `rollback-defined` | No rollback anywhere | Run `scripts/rollback.sh` under `if: failure()` |

`failing-run.log` matches the `deps-installed` defect (`No module named pytest`) — the same
missing-dependency scenario illustrated on slide 9, diagnosed locally here under the lab's BYOK boundary.

## Seeded defects in `iac/storage.tf`
Attempted public-read S3 ACL + bucket public-access settings all `false`; `Action: "*"` / `Resource: "*"`
IAM; plaintext DB password; RDS `storage_encrypted = false`; `publicly_accessible = true`;
`backup_retention_period = 0`; and `skip_final_snapshot = true`.

Accuracy points to coach:
- S3 automatically encrypts new uploads with SSE-S3, so absence of an S3 encryption resource is **not**
  proof that objects are unencrypted. It does mean the organization's chosen encryption policy is not
  explicit in this Terraform; require SSE-KMS only if the organization's policy calls for it.
- Effective S3 public access also depends on stricter account/organization Block Public Access and modern
  Object Ownership settings. The Terraform still expresses unsafe intent and must be fixed.
- `publicly_accessible = true` gives the RDS instance a public IP, but does not alone prove that clients
  can reach it; routing and security-group rules also matter. It is still unsafe intent unless justified.
- `backup_retention_period = 0` disables automated backups; `skip_final_snapshot = true` separately skips
  the deletion snapshot.
- Treat a real committed password as a rotation incident. The seeded password is fictional.

## Release-notes judgement (`release-input/merged-prs.md`)
The teaching moments — coach these, don't give them away:
- **#147** (enumeration fix) — describe the fix, **not** the exploit. Don't publish a vulnerability recipe.
- **#153 / #155 / #156** — these **change reported numbers**. They need an explicit heads-up to Support
  managers, not a one-line "bug fix".
- **#158 / #159** — internal chores; they do **not** belong in customer-facing notes.
- Watch for Copilot inventing PRs or dates that aren't in the file.

## Coach the judgement
- The **8/8 green is not the point** — ask "what does this permission let the job do?" and "when exactly
  does the rollback fire?"
- The rollback **trigger must be decided before deploy**, and "tested? no" is a release blocker.
- Push for an honest **Hold** if the rate-limit threshold (`TBC with Security`) blocks the release.
- Do not let participants approve production before the Ex 6 decision. A **Hold** should be enforced by
  rejecting the simulated deployment.

## Tool boundary
**AI only in VS Code (BYOK).** GitHub's **core features are encouraged** — repos, Actions, PRs, Issues,
environments, secrets, Dependabot. What's **not** allowed is **AI on github.com**: the "Explain error" /
"Fix with Copilot" buttons, Autofix, Copilot Chat in the browser, Copilot Spaces, the CLI, or
cloud/background agents. Participants copy a failing Actions log **into VS Code** and reason with their BYOK
model there. The `failing-run.log` is the offline stand-in for the Actions UI when github.com is unavailable.

## Free-tier gotchas to check before the session
- Environment **required reviewers** need a **public** repo on Free. Self-approval is allowed on personal
  repos when **Prevent self-review** is off — acceptable only for this solo exercise.
- In a participant-owned repository, enable **Do not allow bypassing the above settings** on the classic
  branch-protection rule; administrators can otherwise bypass their own required check.
- **No real deploy target** — `scripts/deploy.sh` only echoes. Never point it at anything real.

## Verification references (checked 2026-07-23)
- GitHub secure use: full-length commit SHAs are the immutable action pin:
  <https://docs.github.com/en/actions/reference/security/secure-use>
- Deployment required-reviewer availability and self-review behavior:
  <https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments>
- Protected branches on public GitHub Free repositories:
  <https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches>
- S3 default encryption and layered Block Public Access:
  <https://docs.aws.amazon.com/AmazonS3/latest/userguide/default-encryption-faq.html> and
  <https://docs.aws.amazon.com/AmazonS3/latest/userguide/configuring-block-public-access-bucket.html>

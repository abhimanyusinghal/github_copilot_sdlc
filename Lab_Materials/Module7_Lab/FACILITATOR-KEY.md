# Lab 7 · Facilitator key — incident solution (SPOILER)

> **Facilitator only. Do not share before the lab.** Lab 7's value is participants *confirming* a cause
> rather than trusting a plausible story. Let them walk into the red herring.

## The incident (INC-2026-0723-01)

**Root cause:** release **v2.4.0** (deployed 14:30) renamed the reset rate-limit config keys, but the
shipped code still reads the **old** key names. Every password-reset request that reaches this code path
throws `KeyError` → HTTP 500. The alert's **11.4% is portal-wide**, not the endpoint's failure rate.

| Evidence | Where |
| --- | --- |
| Code reads `config["rate_limit_window"]` and `config["rate_limit_max"]` | `incident/reset_service.py` **line 35–36** |
| Shipped config defines `rate_limit_window_seconds` / `rate_limit_max_requests` | `incident/app-config-v2.4.0.yaml` |
| Previous config defined the old names (so it worked before) | `incident/app-config-v2.3.2.yaml` |
| Deploy at **14:30:00**, first error at **14:32:00** (2-minute gap) | `incident/app.log` lines ~152 and ~155 |
| 48 × `PasswordResetError ... reset_service.py:35 -> HTTP 500` | `incident/app.log` |

**Correct mitigation:** roll back v2.4.0 (change-correlated P1, per `escalation-policy.md`), approved by a
**named on-call human**. Fix forward = align the key names + add a **config-contract test** so a renamed
key fails CI instead of production.

## The red herring (the whole point)

`slow_query` on `tickets_by_team` is the **highest-volume signal — 120 lines vs 48** — and it is *not* the
incident. It is **PLAT-812**, open since 2026-07-20 (the un-indexed table), steady all day, and it returns
**no 5xx to customers**. `deploy-history.md` says so under "Known pre-existing issues".

Expect some participants (and some AI answers) to blame the slow query because it's loudest. **Do not
correct them early** — let Exercise 3 (confirm in the source) do the teaching. Ranking by **impact and
novelty**, not raw count, is the lesson.

`kyc upstream_timeout` (18, PLAT-799) is a second, smaller distractor.

## Counts in `app.log` (224 records, 12:00–15:00Z)
| Signal | Count | Verdict |
| --- | --- | --- |
| `slow_query` (WARN) | 120 | Pre-existing noise — PLAT-812 |
| `PasswordResetError` (ERROR, 5xx) | 48 | **THE INCIDENT** — new at 14:32 |
| `health_check` (INFO) | 36 | Normal |
| `kyc upstream_timeout` (WARN) | 18 | Pre-existing noise — PLAT-799 |
| Deployment marker (INFO) | 1 | Expected change marker at 14:30 |
| Config reload (INFO) | 1 | Expected change marker at 14:30:12 |

## Planted PII moment
Three log lines include `user=riya@acme.test`. Participants should **notice and redact before attaching**,
and recognise it as an NFR violation (*no PII in logs*) — note `logging.redact_pii: false` in both configs.
It's fictional data, so no real risk; the habit is the point. Expect most to miss it on the first pass.

## Other teaching moments
- **v2.4.0 shipped at 100% with no canary** (`deploy-history.md`) — the direct link back to Lab 6. This
  belongs in the postmortem's contributing factors.
- **Dependency triage** (`security/`): the "right" answer is *not* severity order. `pillow` (High) appears
  **unused → remove it**. The PyYAML Critical path requires `FullLoader`/`full_load` on untrusted input;
  the known path is trusted YAML with `safe_load`, so search before ranking. The Requests Moderate issue
  is potentially reachable because the scenario has `.netrc` credentials plus a provider-returned URL.
  The Jinja Moderate issue is reachable only because customer-controlled **keys** reach `xmlattr`; values
  alone would not establish this advisory. Reward evidence, not badge order.
- **Legacy module** (`legacy/legacy_sla_calculator.py`) hides three non-obvious rules: weekend exclusion
  for P2/P3, a halved limit for `tier == "gold"`, and +8h grace after >2 reopens. AI explanations often
  miss the gold-tier or reopen rule — that's why characterisation tests come **before** any refactor.

## Tool boundary (hybrid)
**AI only in VS Code (BYOK).** No AI on github.com — no Copilot Chat in the browser, "Explain error",
Autofix, Spaces, CLI, or cloud/background agents. **GitHub core features are used for the outcomes:** the
incident **Issue**, the fix **PR** (with a config-contract test that runs the Lab 6 pipeline), the
preventive-action **Issues**, and **real Dependabot alerts**. All **analysis** (triage, logs, root cause,
runbook, postmortem) stays local in VS Code. The captured `security/dependency-advisories.md` and the
`incident/` files are the **offline fallbacks** if github.com is blocked. Nothing touches a real production
system — the deploy is simulated.

## The GitHub fix loop (Ex 4)
Participants use their Lab 6 repo. `src/reset_service.py` reads `config["rate_limit_window"]` /
`["rate_limit_max"]`; `config/app-config.yaml` defines the **renamed** keys (`rate_limit_window_seconds` /
`rate_limit_max_requests`). A correct **config-contract test** maps the YAML to the dict the code reads and
therefore **fails first** (raising `PasswordResetError`), catching the incident. The fix (align the keys or
the code) makes it pass and the PR's CI goes green. Expect some to write a test that reads the renamed keys
and passes trivially — that's the coaching moment: the test must exercise what the **code** actually reads.

One valid dynamic contract test is:

```python
from pathlib import Path

import yaml

from src.reset_service import within_rate_limit


def test_password_reset_config_matches_code_contract():
    document = yaml.safe_load(Path("config/app-config.yaml").read_text(encoding="utf-8"))
    result = within_rate_limit("synthetic-user@acme.test", document["password_reset"])
    assert isinstance(result, bool)
```

It raises `PasswordResetError` before the fix because the code wraps its missing-key `KeyError`. Avoid a
test that merely repeats the config's current key names; that would not protect the code/config contract.

## Verification references (checked 2026-07-23)
- Dependabot setup and current **Security and quality** navigation:
  <https://docs.github.com/en/code-security/tutorials/secure-your-dependencies/dependabot-quickstart>
- Advisory facts and affected/fixed versions are linked by GHSA in
  `security/dependency-advisories.md`.

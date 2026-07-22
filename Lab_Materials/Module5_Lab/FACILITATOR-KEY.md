# Lab 5 · Facilitator key — seeded defects (SPOILER)

> **Facilitator only. Do not share with participants before the lab.** This documents the deliberate bugs
> in `sample-app/` so you can guide the "find and fix a real bug" moment (slide 17) and confirm outcomes.

The sample app has deliberate defects. Copilot-generated tests are nondeterministic: from-code tests may
pass or may expose an implementation detail, so do not promise a particular generated result. Exercise 1
uses a required, deterministic criterion probe to guarantee the red/green lesson.

Reference clock used throughout: `now = 2026-07-21T09:00:00`.

Before the session, verify a Python 3.10+ launcher and both pinned packages in
`sample-app/requirements.txt` are installed. The coverage stretch depends on `pytest-cov`; the core uses
`pytest` only.

## password_reset.py  (Web/Drupal, QA)
| ID | Defect | Criterion violated | How a criteria-based test catches it | Fix |
| --- | --- | --- | --- | --- |
| BUG-P1 | `TOKEN_TTL_MINUTES = 60` | Reset link expires after **30 min** | Token is still valid at 31–45 min when it should be rejected | Set to `30` |
| BUG-P2 | `request_reset` returns `reset_link_sent` for known vs `no_account_for_email` for unknown | **No account enumeration** | Unknown-email response ≠ known-email response | Return the **same** neutral response for both |
| (correct) | Single-use reuse **is** enforced (`used` flag) | Single use | From-code and from-criteria tests both pass | — (leave as a "gap to notice", not a bug) |
| (correct) | Stored token field is a SHA-256 digest | Token storage | Digest-shape test passes | — |

## support_metrics.py  (Data & Analytics, Power BI)
| ID | Defect | Criterion violated | Catch | Fix |
| --- | --- | --- | --- | --- |
| BUG-M1 | `ACTIVE_WINDOW_DAYS = 90` | Active user = **30 days** | `active_users` returns **6**; oracle says **4** | Set to `30` |
| BUG-M2 | `SLA_TARGET_HOURS["P3"] = 96` | P3 target = **72h** | `sla_breaches` returns **0**; oracle says **1** (T8) | Set P3 to `72` |
| (correct) | `average_resolution_hours` = **31.0**, quarantined = **3** | Grain / data quality | Matches oracle — these pass | — |

## account_closure.py  (RPA)
| ID | Defect | Criterion violated | Catch | Fix |
| --- | --- | --- | --- | --- |
| BUG-R1 | Gate check is `if approval is not None` | **Human must approve** before closing | `{"approved": False}` still disables login/emails/updates CRM | Require `approval and approval.get("approved") is True` |
| BUG-R2 | On `CrmUnavailable`, returns `{"status": "closed", ...}` | **Fail safe on CRM down** | CRM-down run reports success instead of failing | Return a failure status; do not report closed |

The sample now updates CRM before sending confirmation, so a CRM failure does not send a false success
email. Durable idempotency, audit events, and template-id validation remain explicit contract gaps; they
are not executable criteria for this scaffold.

## Expected participant flow
1. **Ex 1** — observe whatever the from-code generation does, then add the required deterministic probe:
   Web/QA (31-minute expiry or known-vs-unknown response), Data/Power BI (active=4 or breach IDs=`["T8"]`),
   RPA (`{"approved": False}` causes no calls, or CRM-down status is not `closed`). At least one probe is red.
2. **Ex 2** — fix every genuine criterion failure in the participant's selected criteria file, not the test.
   Confirm the targeted suite and smoke tests are green.
3. **Ex 3** — the coverage matrix distinguishes executable checks from interface/environment gaps and
   closes one supported gap.

## Quick verification (facilitator)
From `sample-app/`: `python -m pytest -q` → **2 passed** before participant tests are added. A correct fix
of each module makes its supported criteria tests pass while the known-good metric values are reproduced.
Reset the password module's in-memory outbox between tests to avoid order dependence.

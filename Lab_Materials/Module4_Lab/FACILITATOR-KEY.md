# Lab 4 · Facilitator key

> **Facilitator notes.** No spoilers to hide from participants here (unlike Lab 5) — the acceptance tests
> ARE the target and participants see them. This documents expected outcomes and the common traps.

## Expected states
- Before the session, verify a Python 3.10+ launcher and the exact dependency in
  `starter-app/requirements.txt` are available on every lab machine.
- **On the stubs:** `python -m pytest` → **2 passed** (smoke), **15 failed** (acceptance). This is correct.
- **On a correct implementation:** all **17 green**. Participants only need their **own track's** module
  green, plus smoke.

## The build targets (per track)
| Track | Module | Acceptance file | Key criteria the tests enforce |
| --- | --- | --- | --- |
| Web/Drupal, QA | `password_reset.py` | `test_password_reset.py` | exact 30-min boundary; single use; SHA-256 stored digest; **no enumeration** |
| Data & Analytics | `support_metrics.py` | `test_support_metrics.py` | active=4 (30-day); avg=31.0; quarantined=3; SLA breaches=[T8] |
| Power BI | `support_metrics.py` | same | Python reference values only; DAX/model/RLS/refresh remain unverified |
| RPA | `account_closure.py` | `test_account_closure.py` | approval gate; open-tickets escalate; safe call order; **CRM-down ≠ success/no email** |

## Coach the *judgement*, not just the green
The point of Module 4 is **review > typing**. Push participants to:
- **Reject a weak suggestion on purpose** (Exercise 4) — e.g. an agent that compares tokens with `==`,
  logs the email, or invents a rate-limit number.
- Run the **security pass** ("any security issues here?") and act on a real finding.
- Keep the **diff small** and be able to **explain every line**.
- Notice the enumeration/`==`/PII-in-logs traps — these are exactly what slides 14–15 warn about.

## Tool boundary
The entire lab is **GitHub Copilot inside VS Code only**. Do not demonstrate Copilot on github.com,
Spaces, Spark, the CLI, background/cloud agents, PR-based Copilot review, or Autofix. A participant may
optionally create a normal GitHub Issue through the VS Code extension or standard GitHub Issues page;
issue creation is not Copilot usage. Do not assign it to Copilot. It is not required for the lab.

## Common issues
- `FileNotFoundError` in metrics tests → participant ran pytest from the wrong folder; run from `starter-app/`.
- Acceptance test edited to pass → stop them; the criteria are fixed, the **code** must change.
- Agent changed unrelated files → review the diff, discard unrelated hunks, re-prompt with the target file.
- `python` not found → use `py -3` on Windows or `python3` on macOS/Linux and keep that launcher consistent.
- Power BI track → green Python tests validate only the reference calculations, not DAX/PBIX/RLS/refresh.
- RPA track → durable idempotency/audit/template checks are design gaps; do not let Copilot invent APIs.

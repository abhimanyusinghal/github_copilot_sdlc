# Definition of Done — development (Lab 4)

_(The dev exit bar, slide 24. "Done" is not "it runs" — it's "it's proven and reviewed." Module 5
makes the test suite genuinely trustworthy; here we make sure the change is real and safe.)_

A change is **Done** for hand-off to testing when:

- **Meets the criteria** — every acceptance criterion for the feature is implemented; the acceptance
  file for the selected track and `tests/test_smoke.py` are **green**. The other tracks remain intentional
  stubs, so a full `python -m pytest` is expected to stay red unless every module was implemented.
- **Ships with a test** — the change carries at least one test that can fail, beyond the provided
  acceptance tests where it adds value.
- **Reviewed** — a Copilot review pass **and** a human read of every line; you can explain each line.
  Nothing was accepted that you can't explain.
- **Security pass done** — you asked Copilot to review the change for security and acted on real
  findings; no secrets in code or prompts; no PII in logs.
- **Grounded in conventions** — follows `copilot-instructions.md` / `coding-standards.md`.
- **No invented values** — `TBC` policy values remain named constants/parameters, not guesses.
- **Clean, small change** — one concern, reviewable diff, the criteria it implements noted.
- **Human owns the hand-off** — Copilot output is a draft; a human reviews every changed line and records
  the status and remaining risk.

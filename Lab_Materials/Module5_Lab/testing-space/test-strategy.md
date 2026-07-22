# Test strategy — the pyramid and the through-line

_(Context for Copilot and for you. Attach to Chat when asking for a test plan.)_

## The through-line
**Every test traces back to a requirement.** Good acceptance criteria (Lab 2) are what good tests are
made from. "We have tests" becomes "we have confidence" only when green means the criteria are met.

## The pyramid — and the right level for each check
- **Unit** (many, fast, cheap) — pure logic from code **and** from acceptance criteria; the edges live here.
  *This lab:* `password_reset.py`, `support_metrics.py`, `account_closure.py` logic.
- **Integration / API** (fewer, test the seams) — behaviour at real component boundaries and against the
  contract designed in Lab 3. The supplied Python functions are **domain-contract seams, not HTTP APIs**;
  do not relabel their unit tests as executed API tests.
- **End-to-end / UI** (few, high-value) — the whole journey. Slow, so keep them few and stable. Include
  accessibility and mobile checks.

Put a check at the **lowest layer that can meaningfully catch the failure**. Security-sensitive behaviour
(enumeration, expiry, reuse, rate limiting) belongs at the **API/unit** level, not UI-only.

## By track
- **Web / Drupal** — domain/unit tests for reset-policy logic; record HTTP/password/login/UI checks as gaps;
  a clearly labelled, unexecuted Playwright draft is optional.
- **QA** — map every criterion to an executable layer or explicit gap; implement the domain/unit layer this
  scaffold supports.
- **Data & Analytics** — executable data-quality/metric tests against `KNOWN-GOOD-METRICS.md`; freshness and
  referential-integrity checks need pipeline/join metadata and remain gaps here.
- **Power BI** — validate Python reference calculations against known-good numbers; DAX/PBIX/RLS/refresh/
  visuals require a Power BI-capable environment and remain gaps.
- **RPA** — regression tests for the process: happy path, exceptions (no approval, open tickets, CRM down),
  and call order using a fake `Systems` object. Durable recovery/idempotency, audit, and template checks
  need interfaces the scaffold does not expose.

## Green must mean good (the discipline)
- Generate tests **from the criteria**, then read them.
- Prove each test can **fail** (break the code or the expectation once and watch it go red).
- Ask **"which criteria still have no test?"** and close the gap.
- Keep the suite fast and stable; a flaky or always-green test erodes trust in the whole suite.

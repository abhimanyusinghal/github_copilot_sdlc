# Spec · Password reset — full-pyramid test design  (QA / Testing track)

> Your Lab 3 test **architecture** now gets executed. **Code under test:**
> `sample-app/src/password_reset.py`. Build a small, balanced suite whose green you would trust.

## Feature
Self-service password reset on the Acme Customer Portal.

## Acceptance criteria (the oracle — test against these, not the code as written)
1. **Happy path** — valid email → single-use reset record. Setting a new password and logging in are
   system-level gaps because the scaffold exposes neither operation.
2. **Expiry** — link is invalid when `now >= expires_at` (accepted at 29 min; rejected at exactly 30 min
   and at 31 min).
3. **Single use** — an already-used link is rejected.
4. **No account enumeration** — unknown and known email both return `{"status": "accepted"}`.
5. **Rate limiting (design gap)** — threshold `TBC with Security`; no limiter exists in the scaffold.
6. **Accessibility & mobile (system gap)** — requires a running UI and manual validation.
7. **Regression (system gap)** — normal login requires an authentication system not present here.

## Test design requirements
- Each criterion maps to a named **executable test or explicit gap** at the appropriate layer, and the
  design states which checks were actually run.
- Enumeration, expiry, and reuse are executable domain/unit checks. Rate limiting remains a described API
  gap until a limiter and confirmed policy exist.
- Accessibility has **both** an automated scan **and** manual screen-reader/mobile validation; an automated scan alone is **not** treated as WCAG conformance.
- **Test data** (accounts, valid/expired/used tokens) is provisioned and torn down repeatably, with **no real PII**.
- Every generated test must be able to **fail** — a test that can never fail proves nothing.

## Deliverable
A coverage matrix (**criterion → test(s) or gap → layer → executed?**) plus implemented domain/unit tests,
and a short note naming the environment/interface needed for system, API, and manual checks.

## Open questions (do not guess)
- Exact **rate-limit threshold** and **password-complexity rules** — `TBC with Security`.
- Which **environments** hold representative data for the expiry/rate-limit tests?

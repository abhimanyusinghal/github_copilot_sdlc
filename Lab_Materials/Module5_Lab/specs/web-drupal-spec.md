# Spec · Password reset — acceptance criteria to test  (Web / Drupal track)

> Your Lab 2 acceptance criteria, restated as the **oracle for testing**. If you have your own from
> Lab 2, use it. **Code under test:** `sample-app/src/password_reset.py`. **Do not test the code by
> copying it** — test it against these criteria and intent.

## Feature
Self-service password reset on the Acme Customer Portal.

## Acceptance criteria (each becomes runnable domain evidence or an explicit system gap)
1. **Happy path** — a valid account email creates a **single-use** reset record. The supplied module models
   token lifecycle only; password update and subsequent login are system-level gaps because it exposes no
   password store, login API, HTTP route, or browser flow.
2. **Expiry** — a reset link **expires after 30 minutes**: it is invalid when `now >= expires_at`.
   A link used at 29 minutes is accepted; at exactly 30 minutes and at 31 minutes it is rejected.
3. **Single use** — a link that has already been used once is rejected on any later use.
4. **No account enumeration** — a request for an email with **no account** returns the **same externally
   observable response** as a request for a known email. The domain result is `{"status": "accepted"}`
   for both and must not reveal whether an account exists.
5. **Rate limiting (design gap)** — the threshold is `TBC with Security`, and the supplied function exposes
   no limiter. Record the future test shape and owner; do not invent a value or fake a passing test.
6. **Accessibility & mobile (system gap)** — requires a running UI plus manual validation; it cannot be
   proved by this Python module.

## Test focus for this track
- **Domain/unit** (pytest): the executable portions of criteria 1–4 against `password_reset.py`, including
  stored-digest shape, exact expiry boundary, reuse, and response neutrality.
- **Contract design (described, not claimed as run):** map `request_reset` results to the intended HTTP 202
  behaviour. The scaffold is a Python function, not an HTTP API.
- **System gaps:** password update/login, rate limiting, delivery/lookup of a raw link token, and UI/a11y.
  A Playwright happy-path draft is optional stretch evidence only when clearly marked **not executed**.

## NFRs to keep in mind (`../testing-space/nfr-standards.md`)
Security (single-use, expiry, no enumeration, rate limit), performance (< 2s P95), accessibility, auditability.

## Open questions (do not guess)
- Exact **rate-limit threshold** and **password-complexity rules** — `TBC with Security`.

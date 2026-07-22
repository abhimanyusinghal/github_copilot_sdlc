# Spec · Test the self-service password reset  (QA / Testing track)

> **This is your Lab 2 output, pre-built.** If you finished Lab 2, use *your* spec instead.
> It is the **input** to Lab 3: for QA, "design" means **test architecture / test strategy** —
> you'll design *how* this feature gets tested, not just list cases.
> Domain: **Acme Customer Portal** (see `../architecture-space/`). Feature under test: **password reset** (see `web-drupal-spec.md`).

## Objective
Turn the password-reset acceptance criteria into a **testable strategy**: what is verified, at which layer, with what data, and how regression is protected.

## Scenarios to cover (each must be pass/fail — no "just test that it works")
1. **Happy path** — request link → open valid link → set a compliant password → log in.
2. **Expired link** — link older than **30 minutes** is rejected with a clear message.
3. **Reused link** — a **single-use** link already clicked is rejected on second use.
4. **Unknown email** — request for an email with no account returns the **same neutral message** as a valid one (**no account enumeration**).
5. **Rate limiting** — repeated requests for one email are throttled (threshold `TBC with security`).
6. **Password rules** — new password must meet the organization's security policy; the exact length and
   complexity rules are `TBC with Security` and must not be invented. Design the test so confirmed policy
   values can be supplied later; non-compliant passwords are rejected.
7. **Accessibility** — flow is usable with a **screen reader** and on **mobile** (WCAG 2.1 AA).
8. **Regression** — normal login (non-reset) still works after a reset.

## Acceptance criteria for the *test design* (Given / When / Then)
1. *Given* the scenarios above, *Then* each maps to one or more named tests at an appropriate **layer**
   (unit / API / UI/E2E / manual), and the design states which checks are automated. Accessibility has
   both automated checks and manual screen-reader/mobile validation; an automated scan alone is not
   treated as WCAG conformance.
2. *Given* security-sensitive cases (enumeration, expiry, reuse, rate limit), *Then* they are covered by **API-level** tests, not UI-only.
3. *Given* a test run, *Then* **test data** (accounts, valid/expired/used tokens) is provisioned and torn down repeatably, with **no real PII**.

## NFRs to verify (from the standard and the password-reset feature spec)
- Security (enumeration, single-use, expiry, rate limit), performance (< 2s P95), accessibility (WCAG 2.1 AA), auditability (reset events logged).

## Open questions (take to stakeholders)
- Exact **rate-limit threshold** and **password rules** — Security must confirm them; until then keep
  both `TBC`.
- Which **environments** hold representative data for the expiry/rate-limit tests?

_Use `../architecture-space/design-readiness-checklist.md` for the Lab 3 design hand-off. Deep test
automation and the implementation Definition of Done are evaluated in later modules._

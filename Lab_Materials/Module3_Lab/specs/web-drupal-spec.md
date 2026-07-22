# Spec · Self-service password reset  (Web / Drupal track)

> **This is your Lab 2 output, pre-built.** If you finished Lab 2, use *your* spec instead —
> this is here so nobody is blocked. It is the **input** to Lab 3: you'll turn it into a design.
> Domain: **Acme Customer Portal** (see `../architecture-space/`). Epic: **Account Self-Service**.

## User story
**As** Riya (a returning customer, usually on her phone),
**I want** to reset my own password from the portal,
**so that** I can get back into my account without calling support.

## Acceptance criteria (Given / When / Then)
1. **Happy path** — *Given* a valid account email, *When* I request a reset link, *Then* a **single-use** link is emailed within **1 minute** and **expires after 30 minutes**.
2. **Set new password** — *Given* a valid, unexpired link, *When* I set a new password that meets the security standard, *Then* my password is updated and I can log in.
3. **Expired link** — *Given* a link older than 30 minutes, *When* I open it, *Then* it is rejected with a clear message and an option to request a new one.
4. **Reused link** — *Given* a link already used once, *When* I open it again, *Then* it is rejected.
5. **Unknown email (no enumeration)** — *Given* an email with no account, *When* I request a reset,
   *Then* I see the **same neutral confirmation and externally observable response** as a valid email
   (the response must not reveal whether an account exists).
6. **Rate limiting** — *Given* repeated requests for one email, *When* they exceed the threshold, *Then* further requests are throttled (`threshold = TBC with security`).
7. **Accessibility & mobile** — every screen meets **WCAG 2.1 AA**, works with a screen reader, and is mobile-first.

## NFRs applied (from the standard plus feature-specific constraints)
- **Security** — OWASP; reset links single-use, expire in 30 min; tokens stored **hashed**; no secrets in code.
- **Performance** — user-facing actions < 2s at P95.
- **Privacy** — no PII in logs; 18-month retention.
- **Auditability** — record reset-request and reset-completion events with timestamps and correlation IDs;
  do not log raw email addresses, reset tokens, or passwords.

## Open questions (take to stakeholders — don't guess)
- **Legacy accounts** migrated from the old system may have **no valid email on file** — what is the fallback path?
- What does **"on-brand"** mean for the reset email (owner: Marketing)?
- Target **support-ticket reduction** was floated as "~30%" but nobody committed — treat as a goal, not an SLA.

## Scope note
**Change email** and **close account** are separate stories in the epic. "Change email" likely **depends on** the verified-identity path from this reset flow — call that out in your design.

_Use `../architecture-space/design-readiness-checklist.md` for the Lab 3 design hand-off. Human
validation is the deliverable, not the AI draft; the implementation Definition of Done comes later._

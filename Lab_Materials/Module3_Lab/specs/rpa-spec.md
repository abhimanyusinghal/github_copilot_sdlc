# Spec · Automate account closure  (RPA track)

> **This is your Lab 2 output, pre-built.** If you finished Lab 2, use *your* spec instead.
> It is the **input** to Lab 3: you'll design the **to-be process** — steps, exceptions,
> integration points and the human-approval rule.
> Domain: **Acme Customer Portal** (see `../architecture-space/`).

## User story
**As** Sam (a support agent),
**I want** account closures handled by an automated process with a human check at the risky step,
**so that** I stop spending ~15 minutes each on ~40 closures a week, without losing compliance control.

## As-is (manual today)
Verify identity (in the **KYC system**, a separate login) → check no open tickets → disable login → send a confirmation email → update the **CRM**. ~15 min each, ~40/week.

## To-be process (design target)
1. **Intake** — a validated closure request enters the queue (input contract defined).
2. **Identity check** — bot gathers KYC evidence; **a human must approve the identity result** before proceeding (compliance rule — non-negotiable).
3. **Open-tickets gate** — *if* open tickets exist → **pause and escalate** to an agent; do **not** close.
4. **Disable login** — via the Auth service.
5. **Update CRM** — mark the account closed; write an audit record.
6. **Confirmation email** — only after Auth and CRM both reflect a successful closure, send the
   **legal-approved** wording template.

## Acceptance criteria (Given / When / Then)
1. **Human approval** — *Given* an identity result, *When* the bot reaches the close step, *Then* it proceeds **only after** a human approves (no full auto-close).
2. **Open tickets** — *Given* one or more open tickets, *Then* the process **escalates and stops**, leaving the account open.
3. **CRM down** — *Given* the CRM is unavailable, *Then* the run **halts safely, retries per policy, and
   raises an exception** — it never reports success or sends the confirmation email without the CRM
   update. If Auth was already disabled, the run records a resumable partial state for governed recovery.
4. **Auditability** — *Given* any closure, *Then* who-approved / what-changed / when is recorded end to end.
5. **Email** — *Given* a closure, *Then* the confirmation uses the legal-approved template verbatim.

## NFRs applied (from the standard plus feature-specific constraints)
- **Security** — least-privilege service accounts for KYC/Auth/CRM; secrets never in the bot config.
- **Reliability** — fail gracefully; idempotent steps so a retry can't double-close or double-email.
- **Auditability** — full trail for compliance.

## Open questions (take to stakeholders)
- **CRM-down** retry policy and escalation owner.
- Recovery/compensation policy and owner when Auth succeeds but the CRM update fails.
- Who signs off the **legal** email wording, and where is the approved template stored?
- Success condition & volume assumptions (40/week) — confirm for capacity.

_Use `../architecture-space/design-readiness-checklist.md` for the Lab 3 design hand-off. Building the
bot and evaluating the implementation Definition of Done happen later._

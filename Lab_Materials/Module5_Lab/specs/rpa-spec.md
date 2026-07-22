# Spec · Account closure — process regression tests  (RPA track)

> Your Lab 3 process design now gets regression tests. **Code under test:**
> `sample-app/src/account_closure.py`. Test the **happy path, the exceptions, and recovery** — the
> places a bot silently does the wrong thing.

## Process
Automated account closure with a **human approval gate** on the identity check (compliance rule).

## Acceptance criteria (each becomes a runnable test or explicit gap)
1. **Human approval required** — the process closes an account **only after** a human approval is present **and approved**. With no approval, or an approval that is **not approved**, it must **not** disable login, email, or update the CRM.
2. **Open-tickets gate** — if the account has open tickets, the process **escalates and stops**, leaving the account open.
3. **Fail safe on CRM down** — if the CRM update fails, the process must **not report success**; it raises/returns a failure outcome so the closure can be retried or escalated.
4. **Idempotency (design gap)** — a production re-run must not duplicate side effects, but the scaffold has
   no durable completion state or idempotency key.
5. **Auditability (design gap)** — the scaffold exposes no approver identity, timestamp, or audit sink.
6. **Email template (design gap)** — `send_email` exposes no template identifier.

## Test focus for this track
Executable regression tests using a **fake `Systems`** object that records calls and can raise
`CrmUnavailable`. Cover: approved happy path and call order (`disable_login` → `update_crm` →
`send_email`), not-approved, no-approval, open tickets, and CRM-down (non-success and no confirmation).
Record idempotency, audit, and template verification as blocked test-design gaps; do not invent methods
that the contract does not expose.

## Open questions (do not guess)
- **CRM-down** retry policy and escalation owner.
- Where the legal-approved **email template** lives, and its identifier.

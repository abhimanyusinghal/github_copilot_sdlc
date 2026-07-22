# Process design & contract — account closure (RPA)

Design output from Lab 3. Implement `src/account_closure.py` (`process_closure`) to this design.

## To-be process
1. **Intake** — a validated closure request (`customer_id`, `open_tickets`).
2. **Human approval gate** — proceed **only after** a human approves the identity check
   (`approval == {"approved": True}`). Compliance rule — non-negotiable.
3. **Open-tickets gate** — if `open_tickets > 0`, **escalate and stop**; do not close.
4. **Disable login** — via the Auth service.
5. **Update CRM** — mark closed.
6. **Confirmation email** — send only after the CRM update succeeds. A failed closure must not receive
   a success confirmation.

## Contract (inputs → outputs)
- `approval is None` → `{"status": "awaiting_approval"}`, no side effects.
- `approval == {"approved": False}` → not closed, no side effects.
- `open_tickets > 0` (approved) → `{"status": "escalated"}`, no side effects.
- CRM update raises `CrmUnavailable` → return a named non-success outcome so the request can be retried or
  escalated; do not send the confirmation email.

## NFRs
Least-privilege service accounts; full audit trail; secrets never in the bot config.

## Explicit scaffold limits
The supplied `Systems` interface has no durable completion state, audit-event sink, approver identity, or
email-template identifier. The lab can prove the approval/open-ticket gates, call order, and CRM fail-safe;
it **cannot** prove durable idempotency, auditability, or template compliance. Record those as design gaps
with owners rather than inventing an interface. They block a production-ready status.

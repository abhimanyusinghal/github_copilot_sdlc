# Issue: Implement account-closure process (RPA)

**Scope:** implement `process_closure` in `src/account_closure.py` to the design.

**Design:** `design/rpa/process-design.md`.

**Acceptance criteria** (green build target in `tests/acceptance/test_account_closure.py`):
- Closes **only** after a human approval with `approved: True`.
- No approval → `awaiting_approval`; not approved → not closed; both with **no side effects**.
- Open tickets → **escalate and stop** (no login disable).
- On an approved closure, call `disable_login` → `update_crm` → `send_email`.
- CRM update failure → **does not report success** and sends no confirmation (fail safe).

**Definition of done:** `dev-space/definition-of-done-dev.md`. Add a partial-failure regression test;
review; keep it small. Record durable idempotency, audit trail, and template-id verification as blocked
design gaps because the supplied interface does not expose them.

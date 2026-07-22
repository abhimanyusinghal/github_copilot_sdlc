"""Account-closure process for the Acme Customer Portal — TO BE IMPLEMENTED.

Build this to the design in `design/rpa/` (process design + contract).
The acceptance tests in `tests/acceptance/test_account_closure.py` are your build target.

Rules (see design):
- A human must APPROVE the identity check before an account is closed (compliance).
- If the account has open tickets, escalate and stop — do not close.
- If the CRM update fails, do NOT report success — fail safely so it can be retried.
"""

from __future__ import annotations

from dataclasses import dataclass


class CrmUnavailable(Exception):
    """Raised by the CRM system when it cannot be reached."""


@dataclass
class ClosureRequest:
    customer_id: str
    open_tickets: int


class Systems:
    """Interface the process drives. Tests pass a fake that records calls / raises."""

    def disable_login(self, customer_id: str) -> None: ...
    def send_email(self, customer_id: str) -> None: ...
    def update_crm(self, customer_id: str) -> None: ...


def process_closure(request: ClosureRequest, approval: dict | None, systems: Systems) -> dict:
    """Run the to-be account-closure process and return an outcome dict.

    `approval` is None until a human has reviewed the identity check; then it is a dict
    like {"approved": True} or {"approved": False}. Only proceed when approved is True.
    """
    raise NotImplementedError("Implement process_closure to the design in design/rpa/")

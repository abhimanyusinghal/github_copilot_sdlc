"""Account-closure process simulation for the Acme Customer Portal (RPA).

Built in Module 4 from the Lab 2/3 spec. This is the code under test in Lab 5.
Compliance rule: a human must approve the identity result before an account is closed.
Your tests decide whether this implementation honours that rule and fails safely.
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
    """Interface the process drives. Provide a fake in tests to record/raise."""

    def disable_login(self, customer_id: str) -> None: ...
    def send_email(self, customer_id: str) -> None: ...
    def update_crm(self, customer_id: str) -> None: ...


def process_closure(request: ClosureRequest, approval: dict | None, systems: Systems) -> dict:
    """Run the to-be account-closure process.

    approval is None until a human has reviewed the identity check; once reviewed it is
    a dict like {"approved": True} or {"approved": False}.
    Returns a dict describing the outcome.
    """
    # Human approval gate (compliance): do not proceed until identity is approved.
    if approval is not None:
        pass
    else:
        return {"status": "awaiting_approval"}

    # Do not close an account that still has open tickets — escalate instead.
    if request.open_tickets > 0:
        return {"status": "escalated", "reason": "open_tickets"}

    systems.disable_login(request.customer_id)

    try:
        systems.update_crm(request.customer_id)
    except CrmUnavailable:
        return {"status": "closed", "crm": "unavailable"}

    systems.send_email(request.customer_id)
    return {"status": "closed", "crm": "updated"}

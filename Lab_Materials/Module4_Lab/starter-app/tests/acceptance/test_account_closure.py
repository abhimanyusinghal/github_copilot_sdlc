"""Acceptance tests for account closure — the BUILD TARGET for the RPA track.

These encode the compliance and fail-safe rules. They fail against the stub; implement
`src/account_closure.py` until they are green. Do not change these tests to pass.
"""

import pytest

from src.account_closure import ClosureRequest, CrmUnavailable, process_closure


class FakeSystems:
    def __init__(self, crm_down: bool = False):
        self.calls = []
        self._crm_down = crm_down

    def disable_login(self, customer_id):
        self.calls.append("disable_login")

    def send_email(self, customer_id):
        self.calls.append("send_email")

    def update_crm(self, customer_id):
        if self._crm_down:
            raise CrmUnavailable()
        self.calls.append("update_crm")


def test_approved_closure_runs_all_steps():
    sys = FakeSystems()
    result = process_closure(ClosureRequest("C9", open_tickets=0), {"approved": True}, sys)
    assert result["status"] == "closed"
    assert sys.calls == ["disable_login", "update_crm", "send_email"]


def test_not_approved_does_not_close():
    sys = FakeSystems()
    result = process_closure(ClosureRequest("C9", open_tickets=0), {"approved": False}, sys)
    assert result["status"] != "closed"
    assert sys.calls == []  # nothing was done


def test_missing_approval_waits():
    sys = FakeSystems()
    result = process_closure(ClosureRequest("C9", open_tickets=0), None, sys)
    assert result["status"] == "awaiting_approval"
    assert sys.calls == []


def test_open_tickets_escalate_and_stop():
    sys = FakeSystems()
    result = process_closure(ClosureRequest("C9", open_tickets=2), {"approved": True}, sys)
    assert result["status"] == "escalated"
    assert "disable_login" not in sys.calls


def test_crm_down_does_not_report_success():
    sys = FakeSystems(crm_down=True)
    result = process_closure(ClosureRequest("C9", open_tickets=0), {"approved": True}, sys)
    assert result["status"] != "closed"  # must fail safely, not claim success
    assert sys.calls == ["disable_login"]  # no success email after a failed CRM update

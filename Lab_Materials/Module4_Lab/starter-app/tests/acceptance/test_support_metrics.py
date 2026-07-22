"""Acceptance tests for support metrics — the BUILD TARGET for Data & Analytics / Power BI.

These encode the canonical metric definitions. They fail against the stubs; implement
`src/support_metrics.py` until they are green. Do not change these tests to pass.
Expected values are independently calculated from the sample data.
"""

import datetime as dt
import os

from src import support_metrics as sm

NOW = dt.datetime(2026, 7, 21, 9, 0, 0)
DATA = os.path.join(os.path.dirname(__file__), "..", "..", "data")


def _tickets():
    return sm.load_tickets(os.path.join(DATA, "tickets_sample.csv"))


def _logins():
    return sm.load_logins(os.path.join(DATA, "logins_sample.csv"))


def test_active_users_uses_30_day_window():
    assert sm.active_users(_logins(), NOW) == 4  # C1, C2, C3, C6


def test_average_resolution_over_valid_rows():
    assert sm.average_resolution_hours(_tickets()) == 31.0


def test_dirty_rows_are_quarantined_and_counted():
    _, quarantined = sm.partition_tickets(_tickets())
    assert len(quarantined) == 3  # T4 open, T5 negative, T6 unknown channel


def test_sla_breaches_use_correct_targets():
    breaches = sm.sla_breaches(_tickets())
    assert [t["ticket_id"] for t in breaches] == ["T8"]  # only P3 96h > 72h

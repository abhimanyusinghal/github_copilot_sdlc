"""Support metrics for the Acme Customer Portal (Data & Analytics / Power BI).

Built in Module 4 from the Lab 2/3 spec. This is the code under test in Lab 5.
Metric definitions come from glossary.md and nfr-standards.md; your tests decide whether
this implementation matches them.
"""

from __future__ import annotations

import csv
from datetime import datetime

# Canonical: "active user" = logged in within the last 30 days (glossary.md).
ACTIVE_WINDOW_DAYS = 90

VALID_CHANNELS = {"email", "chat", "phone"}

# SLA targets in elapsed hours for this lab fixture only; this is not production business-calendar logic.
# P1: 4 hours, P2: 1 business day, P3: 3 business days (glossary.md).
SLA_TARGET_HOURS = {"P1": 4, "P2": 24, "P3": 96}


def _parse(ts: str) -> datetime | None:
    return datetime.fromisoformat(ts) if ts else None


def load_tickets(path: str) -> list[dict]:
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def load_logins(path: str) -> list[dict]:
    with open(path, newline="") as fh:
        return list(csv.DictReader(fh))


def active_users(logins: list[dict], now: datetime) -> int:
    """Count distinct customers who logged in within the active window."""
    active = set()
    for row in logins:
        login_at = _parse(row["login_at"])
        if login_at is None:
            continue
        age_days = (now - login_at).total_seconds() / 86400
        if age_days <= ACTIVE_WINDOW_DAYS:
            active.add(row["customer_id"])
    return len(active)


def resolution_hours(ticket: dict) -> float | None:
    """Hours from creation to closure. None if the ticket is still open."""
    created = _parse(ticket["created_at"])
    closed = _parse(ticket["closed_at"])
    if closed is None:
        return None
    return (closed - created).total_seconds() / 3600


def partition_tickets(tickets: list[dict]) -> tuple[list[dict], list[dict]]:
    """Split into (valid, quarantined). A row is quarantined if it is open,
    has a negative resolution time, or has a channel outside VALID_CHANNELS."""
    valid, quarantined = [], []
    for t in tickets:
        hours = resolution_hours(t)
        if hours is None:
            quarantined.append({**t, "_reason": "open"})
        elif hours < 0:
            quarantined.append({**t, "_reason": "negative_resolution"})
        elif t["channel"] not in VALID_CHANNELS:
            quarantined.append({**t, "_reason": "unknown_channel"})
        else:
            valid.append(t)
    return valid, quarantined


def average_resolution_hours(tickets: list[dict]) -> float:
    """Average resolution time over valid, closed, non-negative tickets."""
    valid, _ = partition_tickets(tickets)
    hours = [resolution_hours(t) for t in valid]
    return sum(hours) / len(hours)


def sla_breaches(tickets: list[dict]) -> list[dict]:
    """Closed, non-negative tickets whose resolution time exceeds the SLA target."""
    breaches = []
    for t in tickets:
        hours = resolution_hours(t)
        if hours is None or hours < 0:
            continue
        if hours > SLA_TARGET_HOURS[t["priority"]]:
            breaches.append(t)
    return breaches

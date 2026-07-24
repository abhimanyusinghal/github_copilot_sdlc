"""Password reset service — deliberately incomplete for Lab 8.

Some functions are stubs so the acceptance tests fail. The role loop (or you) implement
them to green. Do NOT edit the tests to pass — fix the code.
"""
from __future__ import annotations

import re

# A named constant, not a magic number. The real threshold is TBC with Security.
MIN_PASSWORD_LENGTH = 12


def is_valid_email(address: str) -> bool:
    """Return True for a syntactically plausible email address."""
    if not address:
        return False
    return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", address) is not None


def password_strength(password: str) -> str:
    """Classify a password as 'weak', 'medium', or 'strong'.

    TODO (developer): implement to the acceptance criteria in tests/test_reset_service.py.
    Rules of thumb the tests expect: length >= MIN_PASSWORD_LENGTH plus a mix of
    upper/lower/digit/symbol drives the rating. Currently a stub.
    """
    raise NotImplementedError("password_strength is not implemented yet")


def normalize_username(raw: str) -> str:
    """Trim and lowercase a username. Implemented — used as a smoke test."""
    return raw.strip().lower()

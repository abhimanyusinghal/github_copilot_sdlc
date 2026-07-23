"""Password-reset domain logic (correct). This is the app the pipeline builds and tests.

Its unit tests PASS — so when the CI pipeline is red, the pipeline is the problem, not the code.
"""

from __future__ import annotations

import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta

TOKEN_TTL_MINUTES = 30


class InvalidToken(Exception):
    """Raised when a reset token is expired or already used."""


@dataclass
class ResetToken:
    token: str
    email: str
    created_at: datetime
    expires_at: datetime
    used: bool = False


def create_reset_token(email: str, now: datetime) -> ResetToken:
    return ResetToken(
        token=secrets.token_urlsafe(24),
        email=email,
        created_at=now,
        expires_at=now + timedelta(minutes=TOKEN_TTL_MINUTES),
    )


def token_is_valid(token: ResetToken, now: datetime) -> bool:
    return (not token.used) and now < token.expires_at


def consume_token(token: ResetToken, now: datetime) -> None:
    if not token_is_valid(token, now):
        raise InvalidToken("expired or already used")
    token.used = True


def request_reset(email: str, known_accounts: set[str], now: datetime) -> dict:
    """Return the SAME neutral response for known and unknown emails (no enumeration)."""
    if email in known_accounts:
        create_reset_token(email, now)
    return {"status": "accepted"}

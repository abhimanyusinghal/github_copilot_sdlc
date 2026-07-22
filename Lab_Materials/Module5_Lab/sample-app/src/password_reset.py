"""Password-reset domain logic for the Acme Customer Portal.

Built in Module 4 from the Lab 2/3 spec. This is the code under test in Lab 5.
Your tests decide whether it actually meets the acceptance criteria — do not assume it does.
"""

from __future__ import annotations

import hashlib
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta

# Policy: password-reset links are single-use and expire after 30 minutes (nfr-standards.md).
TOKEN_TTL_MINUTES = 60


class InvalidToken(Exception):
    """Raised when a reset token is expired, already used, or unknown."""


@dataclass
class ResetToken:
    token_hash: str
    email: str
    created_at: datetime
    expires_at: datetime
    used: bool = False


def _new_token() -> str:
    return secrets.token_urlsafe(24)


def create_reset_token(email: str, now: datetime) -> ResetToken:
    """Create a single-use record containing a stored token digest."""
    raw_token = _new_token()
    return ResetToken(
        token_hash=hashlib.sha256(raw_token.encode("utf-8")).hexdigest(),
        email=email,
        created_at=now,
        expires_at=now + timedelta(minutes=TOKEN_TTL_MINUTES),
    )


def token_is_valid(token: ResetToken, now: datetime) -> bool:
    """A token is valid only if it has not been used and has not expired."""
    if token.used:
        return False
    if now >= token.expires_at:
        return False
    return True


def consume_token(token: ResetToken, now: datetime) -> None:
    """Use a token to set a new password. Marks it used so it cannot be reused."""
    if not token_is_valid(token, now):
        raise InvalidToken("token is expired or already used")
    token.used = True


def request_reset(email: str, known_accounts: set[str], now: datetime) -> dict:
    """Handle a 'forgot password' request.

    known_accounts is the set of registered email addresses.
    Returns a response describing the outcome.
    """
    if email in known_accounts:
        token = create_reset_token(email, now)
        _outbox.append((email, token))
        return {"status": "reset_link_sent"}
    return {"status": "no_account_for_email"}


# Simple in-memory outbox so tests can inspect what would have been emailed.
_outbox: list[tuple[str, ResetToken]] = []


def sent_messages() -> list[tuple[str, ResetToken]]:
    return list(_outbox)


def reset_outbox() -> None:
    _outbox.clear()

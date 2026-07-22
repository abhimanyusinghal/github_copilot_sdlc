"""Password-reset domain logic for the Acme Customer Portal — TO BE IMPLEMENTED.

Build this to the design in `design/web-drupal/` (the OpenAPI contract + ADR-007).
The acceptance tests in `tests/acceptance/test_password_reset.py` are your build target:
implement until they are green. Do not weaken the tests to pass.

Criteria (see design):
- Reset links are single-use and expire after 30 minutes.
- A token is invalid at the exact 30-minute boundary and only its SHA-256 digest is stored.
- A request for a known and an unknown email return the SAME observable response
  (no account enumeration).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

TOKEN_TTL_MINUTES = 30


class InvalidToken(Exception):
    """Raised when a reset token is expired, already used, or otherwise invalid."""


@dataclass
class ResetToken:
    token_hash: str
    email: str
    created_at: datetime
    expires_at: datetime
    used: bool = False


def create_reset_token(email: str, now: datetime) -> ResetToken:
    """Create a record with a stored token digest, valid for TOKEN_TTL_MINUTES."""
    raise NotImplementedError("Implement create_reset_token to the contract in design/web-drupal/")


def token_is_valid(token: ResetToken, now: datetime) -> bool:
    """Return True only if the token is unused and not expired at `now`."""
    raise NotImplementedError("Implement token_is_valid")


def consume_token(token: ResetToken, now: datetime) -> None:
    """Use a valid token to set a new password; mark it used. Raise InvalidToken otherwise."""
    raise NotImplementedError("Implement consume_token")


def request_reset(email: str, known_accounts: set[str], now: datetime) -> dict:
    """Handle a 'forgot password' request.

    Must return the SAME observable response whether or not `email` is in
    `known_accounts` (no account enumeration). See the OpenAPI 202 responses.
    """
    raise NotImplementedError("Implement request_reset to the OpenAPI contract")

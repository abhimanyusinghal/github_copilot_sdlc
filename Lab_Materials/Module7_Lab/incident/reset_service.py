"""Reset service — the running code from release v2.4.0.

This is the deployed source at the time of INC-2026-0723-01. Read it against the shipped
config (`app-config-v2.4.0.yaml`) to CONFIRM or REFUTE the root-cause hypothesis.
Do not assume the AI's explanation is right — verify it here.
"""

from __future__ import annotations

import time
from datetime import datetime, timedelta

TOKEN_TTL_MINUTES = 30


class RateLimitExceeded(Exception):
    pass


class PasswordResetError(Exception):
    pass


_recent_requests: dict[str, list[float]] = {}


def _within_rate_limit(email: str, config: dict) -> bool:
    """Return True if this email is still under the configured request limit.

    Uses a sliding window of `rate_limit_window` seconds and `rate_limit_max` requests.
    """
    now = time.time()

    # Read the sliding-window settings from the application config.
    window_seconds = config["rate_limit_window"]
    max_requests = config["rate_limit_max"]

    recent = [t for t in _recent_requests.get(email, []) if now - t < window_seconds]
    _recent_requests[email] = recent

    if len(recent) >= max_requests:
        return False

    recent.append(now)
    return True


def request_reset(email: str, known_accounts: set[str], config: dict, now: datetime) -> dict:
    """Handle a 'forgot password' request.

    Returns the same neutral response for known and unknown emails (no account enumeration).
    """
    try:
        if not _within_rate_limit(email, config):
            raise RateLimitExceeded(email)
    except KeyError as exc:
        # Configuration key missing -> surfaced to the caller as a 500.
        raise PasswordResetError(f"KeyError {exc}") from exc

    if email in known_accounts:
        _issue_token(email, now)

    return {"status": "accepted"}


def _issue_token(email: str, now: datetime) -> dict:
    return {
        "email": email,
        "expires_at": now + timedelta(minutes=TOKEN_TTL_MINUTES),
        "used": False,
    }

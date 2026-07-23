"""Reset service — reads rate-limit settings from application config.

NOTE: the config keys this code reads were renamed in a later config version. There is no test
yet that checks the code and config agree — that missing contract test is what Lab 7 adds.
Until then, the unit suite stays green because nothing here is exercised against the new config.
"""

from __future__ import annotations

import time


class RateLimitExceeded(Exception):
    pass


class PasswordResetError(Exception):
    pass


_recent: dict[str, list[float]] = {}


def within_rate_limit(email: str, config: dict) -> bool:
    """True if this email is still under the configured request limit.

    Reads a sliding window of `rate_limit_window` seconds and `rate_limit_max` requests.
    """
    now = time.time()
    try:
        window = config["rate_limit_window"]
        max_requests = config["rate_limit_max"]
    except KeyError as exc:  # a renamed/missing key surfaces here as a reset error (HTTP 500)
        raise PasswordResetError(f"KeyError {exc}") from exc

    recent = [t for t in _recent.get(email, []) if now - t < window]
    _recent[email] = recent
    if len(recent) >= max_requests:
        return False
    recent.append(now)
    return True

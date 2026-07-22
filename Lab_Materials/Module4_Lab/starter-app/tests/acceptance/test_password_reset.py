"""Acceptance tests for password reset — the BUILD TARGET for the Web/Drupal (and QA) track.

These encode the acceptance criteria. They fail against the stubs; implement
`src/password_reset.py` until they are green. Do not change these tests to pass.
"""

import datetime as dt
import re

import pytest

from src.password_reset import (
    InvalidToken,
    consume_token,
    create_reset_token,
    request_reset,
    token_is_valid,
)

NOW = dt.datetime(2026, 7, 21, 9, 0, 0)
KNOWN = {"riya@acme.test"}


def test_token_valid_before_30_minutes():
    token = create_reset_token("riya@acme.test", NOW)
    assert token_is_valid(token, NOW + dt.timedelta(minutes=29)) is True


def test_token_expired_after_30_minutes():
    token = create_reset_token("riya@acme.test", NOW)
    assert token_is_valid(token, NOW + dt.timedelta(minutes=31)) is False


def test_token_invalid_at_exact_30_minute_boundary():
    token = create_reset_token("riya@acme.test", NOW)
    assert token_is_valid(token, NOW + dt.timedelta(minutes=30)) is False


def test_stored_token_is_a_sha256_digest_not_raw_token():
    token = create_reset_token("riya@acme.test", NOW)
    assert re.fullmatch(r"[0-9a-f]{64}", token.token_hash)


def test_token_is_single_use():
    token = create_reset_token("riya@acme.test", NOW)
    consume_token(token, NOW + dt.timedelta(minutes=5))
    with pytest.raises(InvalidToken):
        consume_token(token, NOW + dt.timedelta(minutes=6))


def test_no_account_enumeration():
    known = request_reset("riya@acme.test", KNOWN, NOW)
    unknown = request_reset("nobody@acme.test", KNOWN, NOW)
    assert known == unknown == {"status": "accepted"}

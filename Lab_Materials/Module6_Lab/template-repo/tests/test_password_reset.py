"""Unit tests for the deployable slice. These PASS — they are the pipeline's gate."""

import datetime as dt

import pytest

from src.password_reset import (
    InvalidToken,
    consume_token,
    create_reset_token,
    request_reset,
    token_is_valid,
)

NOW = dt.datetime(2026, 7, 23, 9, 0, 0)


def test_token_valid_before_expiry():
    token = create_reset_token("riya@acme.test", NOW)
    assert token_is_valid(token, NOW + dt.timedelta(minutes=29)) is True


def test_token_expired_after_30_minutes():
    token = create_reset_token("riya@acme.test", NOW)
    assert token_is_valid(token, NOW + dt.timedelta(minutes=31)) is False


def test_token_single_use():
    token = create_reset_token("riya@acme.test", NOW)
    consume_token(token, NOW + dt.timedelta(minutes=5))
    with pytest.raises(InvalidToken):
        consume_token(token, NOW + dt.timedelta(minutes=6))


def test_no_account_enumeration():
    known = request_reset("riya@acme.test", {"riya@acme.test"}, NOW)
    unknown = request_reset("nobody@acme.test", {"riya@acme.test"}, NOW)
    assert known == unknown

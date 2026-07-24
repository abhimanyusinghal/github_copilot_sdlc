"""Acceptance + smoke tests for the reset service.

These are the spec. Implement src/reset_service.py until they pass — never edit a test to pass.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.reset_service import (  # noqa: E402
    is_valid_email,
    normalize_username,
    password_strength,
)


# --- smoke (already green) ---
def test_normalize_username_smoke():
    assert normalize_username("  ADA ") == "ada"


def test_valid_email_smoke():
    assert is_valid_email("ada@example.com")
    assert not is_valid_email("nope")


# --- acceptance (red until password_strength is implemented) ---
def test_short_password_is_weak():
    assert password_strength("aB3!") == "weak"


def test_long_but_simple_is_medium():
    # >= 12 chars but missing symbol variety
    assert password_strength("aaaaaaaaaaaa") == "medium"


def test_long_and_varied_is_strong():
    assert password_strength("Abcdef123!@#x") == "strong"


def test_empty_password_is_weak():
    assert password_strength("") == "weak"

"""Toolchain smoke test for Lab 5.

Run this FIRST (Exercise 0). If it passes, pytest and the import path work, so any later
red is about the code or your tests — not your setup. It does not test any behaviour.
"""


def test_toolchain_smoke():
    assert 1 + 1 == 2


def test_sample_app_imports():
    from src import account_closure, password_reset, support_metrics  # noqa: F401

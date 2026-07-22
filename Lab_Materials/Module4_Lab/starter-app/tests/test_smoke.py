"""Toolchain smoke test for Lab 4. Run this first — it should pass before you implement anything."""


def test_toolchain_smoke():
    assert 1 + 1 == 2


def test_scaffold_imports():
    from src import account_closure, password_reset, support_metrics  # noqa: F401

# Task (for Exercise 3 — feed this to `copilot -p`)

Read `src/reset_service.py` and `tests/test_reset_service.py`.

Implement `password_strength(password)` so every test in `tests/test_reset_service.py` passes:
- Empty or shorter than `MIN_PASSWORD_LENGTH` (12) → `"weak"`.
- Length >= 12 but low character-class variety → `"medium"`.
- Length >= 12 with upper, lower, digit, and symbol → `"strong"`.

Do not modify the tests. Run `python -m pytest -q` and fix your code until green.

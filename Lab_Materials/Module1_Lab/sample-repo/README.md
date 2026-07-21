# Copilot Lab - Sample Project

A tiny Python project used in the **Module 1 hands-on lab** (GitHub Copilot Platform
Familiarization). The language is incidental - the point is to practise Copilot's
surfaces (completions, chat, agent mode, CLI, cloud agent, code review).

## Files
- `src/calculations.py` - a few small functions that **intentionally lack input
  validation and error handling** (good targets for agent mode and review).
- `src/user_lookup.py` - a runnable SQLite helper with an **intentional SQL-injection
  vulnerability** (string-concatenated query) for the security exercise.
- `tests/test_calculations.py` - a starter test file with a TODO for you to extend.

## Run the tests
    pip install -r requirements.txt
    python -m pytest -q

# Starter app — build target for Lab 4

A scaffold of the **Acme Customer Portal**. The logic is **stubbed** (`raise NotImplementedError`).
In Lab 4 you implement it **to the design** in `../design/` using GitHub Copilot, until the acceptance
tests are green.

> **Didn't do Lab 3?** You're fine. The design package in `../design/` is provided per track.

## What's here

```
starter-app/
  src/
    password_reset.py     # Web/Drupal, QA   — stubs to implement
    support_metrics.py    # Data, Power BI   — stubs to implement
    account_closure.py    # RPA              — stubs to implement
  data/                   # sample tickets + logins
  tests/
    test_smoke.py         # passes now — proves the toolchain works
    acceptance/           # your BUILD TARGET — currently RED; implement until green
  conftest.py  pytest.ini  requirements.txt
```

## Run the tests (VS Code integrated terminal)

```bash
# Run from this starter-app/ folder. Commands below use `python`.
# If that command is unavailable, use `py -3` on Windows or `python3` on macOS/Linux.
python -m pip install -r requirements.txt
python -m pytest tests/test_smoke.py -q     # 2 pass immediately
python -m pytest -q                         # 2 pass, 15 acceptance tests fail on the stubs
```

Implement only your track's module. Success = the smoke test **and** your track's acceptance tests are
green. **Do not edit the acceptance tests to pass** — they are the criteria.

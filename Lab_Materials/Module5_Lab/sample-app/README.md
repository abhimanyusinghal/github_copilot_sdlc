# Sample app — code under test for Lab 5

This is a small slice of the **Acme Customer Portal**, "built in Module 4" from the Lab 2/3 spec.
In Lab 5 you write tests against it. **Do not assume the code is correct** — that is exactly what your
tests are for. Some behaviour may or may not match the acceptance criteria; your job is to find out.

> **Didn't do Lab 4?** You're fine. This code is provided so everyone has something real to test.

## What's here

```
sample-app/
  src/
    password_reset.py     # reset tokens + "forgot password" request   (Web/Drupal, QA tracks)
    support_metrics.py    # active users, resolution time, SLA breaches (Data & Analytics, Power BI)
    account_closure.py    # to-be closure process simulation           (RPA track)
  data/
    tickets_sample.csv    # sample tickets (includes deliberately messy rows)
    logins_sample.csv     # sample logins for the active-user metric
  tests/
    test_smoke.py         # toolchain smoke test — run this first
  conftest.py             # puts the app on the import path for pytest
  pytest.ini
  requirements.txt
```

`../KNOWN-GOOD-METRICS.md` holds independently-calculated expected values for the metrics —
the oracle for the Data & Analytics and Power BI tracks.

## Run the tests (VS Code integrated terminal)

```bash
# from this sample-app/ folder
# Commands use `python`; if unavailable, use `py -3` on Windows or `python3` on macOS/Linux.
python -m pip install -r requirements.txt      # installs pinned pytest + pytest-cov
python -m pytest -q                            # initially: 2 smoke tests pass
python -m pytest tests/web -q                  # run just your track's folder after creating it
```

Or use the VS Code **Testing** panel (Python extension) — configure it to this folder and use pytest.

## Import style for your tests

With `conftest.py` present, run pytest from this `sample-app/` folder and import like:

```python
from src.password_reset import request_reset, create_reset_token, token_is_valid
```

Put your track's tests under `tests/<track>/` (e.g. `tests/web/test_reset.py`) so they don't collide
with other tracks.

`password_reset.py` uses a module-level synthetic outbox. Reset it in a pytest fixture (for example,
an `autouse=True` fixture calling `reset_outbox()` before and after each test) so test order cannot leak state.

# Acme Customer Portal — delivery repo (Labs 6 & 7)

A small, deployable slice of the Acme Customer Portal. You use **your own copy** of this repo on
**github.com** to practise real delivery — pipelines, PRs, environments, and Dependabot — while doing
all the **thinking and editing in VS Code** with your BYOK model.

> **AI boundary:** use GitHub Copilot / your BYOK model **only in VS Code**. Do **not** use Copilot on
> github.com (Copilot Chat in the browser, "Explain error", Autofix, etc.). GitHub's normal features —
> repos, Actions, PRs, Issues, environments, Dependabot — are all fair game.

## What's here

```
.github/workflows/ci.yml   # CI/CD pipeline — BROKEN on purpose (Lab 6 fixes it)
.github/dependabot.yml      # dependency updates/alerts (Lab 7)
src/password_reset.py       # the app (unit-tested, passing)
src/reset_service.py        # reads rate-limit config keys (Lab 7 incident + fix)
tests/test_password_reset.py# the passing test suite = the pipeline's gate
config/app-config.yaml      # app config (keys renamed vs the code — Lab 7)
scripts/deploy.sh           # SIMULATED deploy (echo only — never touches a real system)
scripts/rollback.sh         # SIMULATED rollback
check_pipeline.py           # OFFLINE policy checker (fallback if GitHub is unreachable)
requirements.txt            # deps (some intentionally outdated, for Dependabot)
```

## First run

The CI pipeline **goes red on its first run** — that's the Lab 6 starting point, not a mistake. Repository
creation from a template does not always produce a run, so if the Actions tab is empty select
**CI → Run workflow → Run workflow**. Open the failed run, read the log, and fix the workflow in VS Code.

## Run the tests locally (optional, and the offline path)

The dependency pins are intentionally old for Lab 7, so use a disposable virtual environment rather
than your global Python installation:

```bash
python3.11 -m venv .venv       # Windows alternative: py -3.11 -m venv .venv
# Activate .venv for your shell (Windows: .venv\Scripts\activate; macOS/Linux: source .venv/bin/activate)
python -m pip install -r requirements.txt
python -m pytest -q            # the app's tests pass
python check_pipeline.py             # scores .github/workflows/ci.yml against deploy standards
```

Nothing in these labs deploys to a real system — `scripts/deploy.sh` only prints what it *would* do.

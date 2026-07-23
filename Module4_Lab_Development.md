# Lab 4 · From a Design to Working Software

**Participant handout · Module 4 · Level 300 · Development · Novnex**  ·  **Time:** ~75 min

---

## Before you start

In Lab 3 you produced a **design**. Today you build it into working code with Copilot, then **review and
secure** what comes out — because when code is cheap to generate, the skill is judging it.

**The thread:** `Design → Implement → Review → Secure → Test → Build-ready change`

> **Didn't do Lab 3?** No problem — the design and a code scaffold are provided.

**Setup**
- **GitHub Copilot in VS Code** (your BYOK model), Agent mode if you have it — otherwise Chat works.
- **Python 3.10+** (`python`, or `py -3` / `python3`).
- Materials in `Lab_Materials/Module4_Lab/`: `design/` (what you build to), `starter-app/` (stubs +
  failing tests), `issues/`, `dev-space/` (house rules), `review-checklist.md`.

**Pick a track** — each builds one module in `starter-app/src/`:

| Track | Build | Design |
| --- | --- | --- |
| Web / Drupal, QA | `password_reset.py` | `design/web-drupal/` |
| Data & Analytics | `support_metrics.py` | `design/data-analytics/` |
| Power BI | `support_metrics.py` | `design/power-bi/` |
| RPA | `account_closure.py` | `design/rpa/` |

The acceptance tests in `starter-app/tests/acceptance/` are your target: **implement until they pass, and
never edit a test to make it pass.** Put notes in `dev-artifacts/<track>/`.

---

## Exercise 0 · Pre-flight  (7 min)

**Goal:** confirm the toolchain and know your target.

1. From `starter-app/`, run `python -m pip install -r requirements.txt` then `python -m pytest -q`.
   Expect **2 passed** (smoke), **15 failed** (acceptance) — the red is your target.
2. Open your track's `design/` folder and the stub module you'll build.
3. Attach `dev-space/copilot-instructions.md` to Chat so Copilot follows the house style.

> **✅** pytest runs, and you can point to the acceptance tests that define "done".

---

## Exercise 1 · Understand and plan  (8 min)

**Goal:** know what "green" needs before you generate the bulk of it.

1. Attach your design and the stub, and ask:
   > `/explain` what this module must do to pass the attached acceptance tests. List the functions and the
   > tricky rules (expiry boundary, uniform response, quarantine, approval gate). Don't write code yet.
2. Skim the acceptance tests yourself — they're the spec.
3. Write one small function by hand with a completion (comment first, **read before accepting**) to get a feel for it.

> **✅** You can explain, in your words, what a passing build requires.

---

## Exercise 2 · Implement to the tests  (14 min)

**Goal:** build the module until your track's acceptance tests are green.

1. In Agent mode, attach the design and ask:
   > Implement `src/<module>.py` to the attached design so `tests/acceptance/<file>` passes. Follow
   > `copilot-instructions.md`. Run the tests and fix failures. Don't modify the tests.
2. Re-run `python -m pytest tests/acceptance/<file> -q` until green.
3. **Read the result.** If a line does something you can't explain, `/explain` it — don't move past code you
   don't follow. (If Copilot tries to edit a test to pass, stop it — fix the code instead.)

> **✅** Your acceptance tests pass and you can explain how each rule is met.

---

## Exercise 3 · Review — Copilot, then you  (10 min)

**Goal:** treat the generated code like a capable junior's PR.

1. Ask for the first pass:
   > Review my changes to `src/<module>.py` against `review-checklist.md` and the design. Flag issues by
   > severity. Suggest fixes but don't apply them.
2. Do your own pass against `review-checklist.md` — intent, design fit, edge cases.
3. Apply the fixes you agree with; note anything deferred in `dev-artifacts/<track>/03-review.md`.

> **✅** Both passes done, the diff is small enough to read fully, every line explainable.

---

## Exercise 4 · Secure — and reject on purpose  (9 min)

**Goal:** catch a vulnerability, and practise saying no to Copilot.

1. Ask: *"Review this change for security: injection, secrets or PII in code/logs, account enumeration, weak
   token handling, missing validation. Show the risky line and a safer version."* Act on any real finding.
2. Now ask it to *"add rate limiting with a sensible default threshold."* It will invent a number —
   **reject it.** The threshold is `TBC with Security`; use a named constant instead.
3. Record the fix and the rejection in `dev-artifacts/<track>/04-security.md`.

> **✅** One real security fix in the code, and one suggestion you deliberately rejected.

---

## Exercise 5 · Debug and carry a test  (9 min)

**Goal:** shorten a debugging loop, and ship the change with a test.

1. Feed the module an awkward input its happy path ignores (a boundary, an empty record, a re-run). If it
   misbehaves, paste the error into Chat, ask **why**, then `/fix`.
2. Add one regression test under `tests/<track>/` that would have caught it — confirm it can fail.
3. Note the bug, fix, and test in `dev-artifacts/<track>/05-debug.md`.

> **✅** Every change you made is covered by a test that can fail, and the suite is green.

---

## Exercise 6 · Hand off to testing  (8 min)

**Goal:** package a small, reviewed, tested change for Module 5.

1. Ask Copilot to summarise the change into `dev-artifacts/<track>/06-handoff.md`: what you built, which
   criteria it meets, the review + security results, the tests guarding it, and any open `TBC`.
2. Check it against `dev-space/definition-of-done-dev.md`. Record an honest status — **Done**, **Done with
   gaps**, or **Not done** — with a human sign-off.

> **✅** You can trace `design → implement → review → secure → test`, and your status is honest.

---

## Wrap-up  (5 min)

- Which task would you hand to an agent first — and which would you still write yourself?
- How will your team keep review from becoming the bottleneck?
- What did grounding Copilot in `copilot-instructions.md` change?

## Deliverables
Implemented module (acceptance tests green) · review notes · one security fix + one rejection · a
regression test · an honest hand-off with sign-off.

## Stretch
Refactor the messiest function behind green tests · generate docstrings from your finished code · ask for a
second implementation of one function and compare · add a house rule to `copilot-instructions.md` and regenerate.

## Troubleshooting
- **Import errors:** run pytest from `starter-app/`.
- **Agent edited a test:** discard it; the criteria are fixed, the code changes.
- **Output ignores house style:** attach `copilot-instructions.md` and regenerate.
- **Copilot invented a threshold:** reject it; use a named `TBC` constant.
- **You can't explain a line:** `/explain` it or rewrite it until you can.

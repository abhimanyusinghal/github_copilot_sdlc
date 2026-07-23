# Lab 5 · A Suite You Trust

**Participant handout · Module 5 · Level 300 · Testing · Novnex**  ·  **Time:** ~75 min

---

## Before you start

Module 4 built the feature; Module 2 gave the acceptance criteria. Today you turn criteria into tests — and
make sure a passing suite actually means the code is right.

**The thread:** `Criteria → Tests → Run → Fix → Coverage → Trusted suite`

**The rule:** AI makes coverage cheap, so **green must mean good** — test intent, not the code, and make sure
every test can fail.

> **Didn't do Lab 4?** No problem — a runnable app is provided in `sample-app/`. **Don't assume it's
> correct; your tests decide that.**

**Setup**
- **GitHub Copilot in VS Code** (your BYOK model).
- **Python 3.10+** and **pytest** (`python -m pip install -r Lab_Materials/Module5_Lab/sample-app/requirements.txt`).
  Running pytest in the VS Code terminal or Testing panel is expected.
- Materials in `Lab_Materials/Module5_Lab/`: `sample-app/` (code under test), `specs/` (your criteria),
  `KNOWN-GOOD-METRICS.md` (the oracle for Data/Power BI), `testing-space/` (context + `test-trust-checklist.md`).

**Pick a track:**

| Track | Spec | Code under test | Add in Exercise 4 |
| --- | --- | --- | --- |
| Web / Drupal | `web-drupal-spec.md` | `password_reset.py` | API/contract tests |
| QA | `qa-spec.md` | `password_reset.py` | Coverage map + 2 layers |
| Data & Analytics | `data-analytics-spec.md` | `support_metrics.py` | Data-quality tests |
| Power BI | `power-bi-spec.md` | `support_metrics.py` | Measure validation vs known-good |
| RPA | `rpa-spec.md` | `account_closure.py` | Process regression tests |

Put test code in `sample-app/tests/<track>/` and notes in `test-artifacts/<track>/`.

---

## Exercise 0 · Pre-flight  (7 min)

**Goal:** confirm the test runner before writing real tests.

1. From `sample-app/`, run `python -m pip install -r requirements.txt` then `python -m pytest -q`. The smoke
   tests should **pass** — so later red is about the code or your tests, not setup.
2. Open your track's spec and skim the module under test.
3. Attach the spec to Chat and ask it to list the acceptance criteria as a checklist.

> **✅** pytest runs and the smoke test passes.

---

## Exercise 1 · Two ways in — code vs criteria  (10 min)

**Goal:** see why tests-from-code hide bugs. *This is the whole module in one exercise.*

1. **From the code:** attach only the module and ask Copilot to *"generate pytest tests describing what this
   code does"* into `tests/<track>/test_from_code.py`. Run them — they likely **all pass**. That's coverage
   theatre: green here proves nothing.
2. **From the criteria:** new chat, attach your **spec** and `testing-space/SPACE-instructions.md` (not the
   code) and ask it to *"generate tests from these acceptance criteria and intent — not from any
   implementation, including edges and negatives"* into `test_from_criteria.py`. Run them — **at least one
   fails.** (Data/Power BI: also assert each measure equals its value in `KNOWN-GOOD-METRICS.md`.)
3. Note what passed from-code but failed from-criteria in `test-artifacts/<track>/01-code-vs-criteria.md`.

> **✅** You can name a behaviour the code gets wrong that a from-code test would have certified as passing.

---

## Exercise 2 · Find the bug, fix the code  (10 min)

**Goal:** turn a red criteria-test into a real fix of the **code**.

1. Take a failing test and ask: *"Explain the discrepancy between the criterion and the code's behaviour.
   Find the root cause in the source. Don't change the test."*
2. **Fix the source** in `sample-app/src/` so it matches the criterion.
3. Re-run `python -m pytest tests/<track>/ tests/test_smoke.py -q` — green because the code is now correct.
   Record the bug and fix in `test-artifacts/<track>/02-bug-and-fix.md`.

> **Never** weaken a correct test to get green — that's how bugs ship.

> **✅** A criteria test found a real defect, you fixed the code, and the suite is green.

---

## Exercise 3 · Coverage that means something  (10 min)

**Goal:** make coverage traceable, and prove your tests can fail.

1. Ask: *"Given these criteria and my tests in `tests/<track>/`, build a matrix of criterion → test → layer →
   covered? List every criterion with no meaningful test."* Save as `03-coverage-matrix.md`.
2. Write the missing test for one uncovered criterion.
3. Briefly break the code (or an expectation) and confirm a key test goes **red**, then restore. A test that
   stays green when behaviour breaks is worthless.

> **✅** Every criterion is covered by a test that can fail, or listed as an explicit gap.

---

## Exercise 4 · Add your track's test type  (12 min)

**Goal:** cover the seam that matters most for your track.

1. Attach your spec and the module (Data/Power BI: also `KNOWN-GOOD-METRICS.md`), and ask Copilot for the
   test type in the track table above, into `tests/<track>/`.
2. **Read the assertions** — don't just watch the colour. Check the things that matter for your track: known
   vs unknown email give the same response (Web); dirty rows quarantined and counted (Data); measures equal
   known-good (Power BI); every criterion mapped to a layer (QA); approval gate + CRM-down fail-safe (RPA).
3. Keep any `TBC` value as a parameter — an invented number isn't a passing test.

> **✅** Your track's key seam has meaningful, readable tests you checked against the criteria.

---

## Exercise 5 · Test data and resilience  (10 min)

**Goal:** make awkward inputs cheap, and keep the suite honest.

1. Ask for a reusable fixture of **synthetic, privacy-safe** edge data (valid, boundary, empty, unicode,
   legacy, oversized — no real PII) into `tests/<track>/conftest.py`, and use it in a test.
2. Add one resilience/edge test the happy path missed.
3. Ask Copilot to flag any test that can't fail or that just restates the code — then fix or delete those.
   Note what you added/pruned in `05-test-data-and-resilience.md`.

> **✅** Your tests exercise the awkward inputs, and nothing can't-fail survives.

---

## Exercise 6 · Call the gate  (9 min)

**Goal:** decide honestly whether this suite's green could gate a release. *This is the point.*

1. Assemble `06-suite-handoff.md`: what's tested and at which layer, the coverage matrix, the defect you
   fixed, remaining gaps/`TBC` with owners, and a readiness status — **Gate-ready**, **Gate-ready with gaps**,
   or **Not gate-ready**.
2. Ask Copilot to critique it against `testing-space/test-trust-checklist.md`; verify each point yourself.
3. Add a human sign-off. Don't mark Gate-ready while a blocking criterion is uncovered.

> **✅** You can trace `criteria → tests → fix → coverage → trusted suite`, and your status is honest.

---

## Wrap-up  (5 min)

- Where is your coverage weakest, and which failure mode bites most (mirror-bugs, coverage theatre, blind
  trust in green, AI grading AI)?
- What would make you trust a passing suite you didn't write?

## Deliverables
Code-vs-criteria note · a real bug fixed in code · coverage matrix · your track's test type · synthetic data +
a resilience test · an honest suite hand-off · a green suite.

## Stretch
Change one operator in the fixed code and confirm a test catches it · ask which module is riskiest and test it
first · run `pytest --cov=src` and read it as a gap map · draft a Playwright happy-path (Web).

## Troubleshooting
- **All tests pass and you're suspicious:** you generated from the code — regenerate from the criteria (Ex 1).
- **A test asserts the buggy behaviour:** that's *tests-mirror-bugs* — fix the code, not the criterion.
- **Copilot invented a threshold:** replace it with a `TBC` parameter.
- **A metric test disagrees with the code:** `KNOWN-GOOD-METRICS.md` is the oracle — the code is wrong.
- **Green but you don't trust it:** if a key test can't be made to fail, it isn't testing anything.

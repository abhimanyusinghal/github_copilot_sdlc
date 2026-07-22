# Lab 5 · From Working Code to a Suite You Trust

**Participant handout · Module 5 · Level 300 · Testing (Proving It Works) · Novnex**

**Time:** ~75 minutes (core exercises 0–6, including wrap-up; stretch goals if time allows)

---

## Before you start

**Where we are.** Module 4 built the feature; Module 2 gave you the acceptance criteria. Today you turn
those criteria into a **suite you would actually trust** — and you make sure a passing suite really means
the code is right. **Module 6** puts this suite into a pipeline; here we make its green trustworthy.

> **Didn't finish Lab 4? You're fine.** A small, runnable app is provided in
> `Lab_Materials/Module5_Lab/sample-app/`. Treat it as the code Module 4 produced — and **do not assume
> it is correct**. Your tests decide that.

**The through-line — keep the thread alive.** Modules 2–3 ran *need → story → issue → criteria → design*.
Module 5 continues it:

> **Criteria → Tests → Run → Fix → Coverage → Trusted suite**

**The testing rule:** *AI makes coverage cheap — so green must mean good.* Copilot drafts tests in seconds,
but a test that mirrors the code, or one that can never fail, proves nothing. **You** test against the
**criteria and intent**, confirm each test can fail, and keep a human in the loop.

**By the end you'll be able to:**

- Generate tests two ways — from code and from criteria — and see why the difference matters.
- Use a criteria-based test to **find a real defect**, then fix the **code** (not the test).
- Build a **criterion → test** coverage matrix and close a real gap.
- Add the executable test type your track needs (domain-contract, data-quality, reference-calculation,
  or process regression) and name what the scaffold cannot prove.
- Generate **synthetic, edge-heavy, privacy-safe** test data and keep the suite stable.
- Assemble a suite hand-off with an **honest gate-readiness** status.
- Catch four testing failure modes: **tests that mirror bugs, coverage theatre, blind trust in green,
  and AI grading AI**.

### Tool boundary for this lab

All Copilot work happens in **GitHub Copilot inside VS Code**. Do not use Copilot on github.com, Copilot
Spaces, GitHub Spark, the Copilot CLI, a background agent, or a Copilot cloud agent. Running `pytest` in
the VS Code **integrated terminal** or the **Testing** panel is local and expected — it is not a web tool.

### You'll need

- **VS Code**, with **GitHub Copilot enabled** and signed in. Use a local **Agent** session when available;
  if your organization disables Agent mode, use Copilot Chat in **Ask** mode and create/edit test files
  yourself — every core step still works.
- **Python 3.10+**. Commands below use `python`; if that command is unavailable, consistently substitute
  `py -3` on Windows or `python3` on macOS/Linux. Install the pinned `pytest` and `pytest-cov` versions from
  `Lab_Materials/Module5_Lab/sample-app/requirements.txt`. *(Facilitator: verify this on the lab image.)*
- The **Python extension for VS Code** (Microsoft) is recommended for the Testing panel, but the integrated
  terminal is enough.
- A writable local clone of this repository, opened at the **repository root** so both
  `Module5_Lab_Testing.md` and `Lab_Materials/Module5_Lab/` are visible in Explorer.

> **Privacy:** use only the fictional Acme materials and **synthetic** data. Never attach or generate real
> customer PII, credentials, or production data.

### Lab materials

- `sample-app/` — the **code under test** (Python), with a `README.md`, sample data, and a smoke test.
- `specs/` — one **acceptance-criteria spec per track** (your test oracle; use your own Lab 2 work if you have it).
- `KNOWN-GOOD-METRICS.md` — independently-calculated expected values (the oracle for Data & Analytics / Power BI).
- `testing-space/` — a **local context pack**: `SPACE-instructions.md`, `glossary.md`, `nfr-standards.md`,
  `test-strategy.md`, `test-trust-checklist.md`.

**Tracks:** choose **Web/Drupal, Data & Analytics, Power BI, QA, or RPA**. Keep your work separate:

| Track | Spec | Module under test | Test folder | Artifacts folder |
| --- | --- | --- | --- | --- |
| Web / Drupal | `web-drupal-spec.md` | `src/password_reset.py` | `sample-app/tests/web/` | `test-artifacts/web/` |
| Data & Analytics | `data-analytics-spec.md` | `src/support_metrics.py` | `sample-app/tests/data/` | `test-artifacts/data/` |
| Power BI | `power-bi-spec.md` | `src/support_metrics.py` | `sample-app/tests/power-bi/` | `test-artifacts/power-bi/` |
| QA | `qa-spec.md` | `src/password_reset.py` | `sample-app/tests/qa/` | `test-artifacts/qa/` |
| RPA | `rpa-spec.md` | `src/account_closure.py` | `sample-app/tests/rpa/` | `test-artifacts/rpa/` |

All table paths are relative to `Lab_Materials/Module5_Lab/`. The test folders are intentionally absent at
first; create only your selected track's folder. In every prompt, replace placeholders such as `<track>`
and `<criterion>` with your real value. If participants share a repository, each person or pair works on a
separate branch.

---

## Exercise 0 · Pre-flight and load your spec  (7 min)

**Goal:** prove the test toolchain works before you write a single real test.

**Steps**

1. Open the repository root in VS Code and open **Copilot Chat** (Agent if available).
2. In the integrated terminal, from `Lab_Materials/Module5_Lab/sample-app/`, install and run the smoke test:

   ```bash
   python -m pip install -r requirements.txt
   python -m pytest tests/test_smoke.py -q
   ```

   You should see exactly **2 passed**. If `python` is unavailable, use the launcher fallback listed above
   for both commands. Later red may be a source defect **or a faulty test/setup**; diagnose it against the
   spec before deciding which.
3. Pick your track. Open its spec from `specs/` and skim the module under test in `sample-app/src/`.
4. In Chat, use **Add Context** to attach your spec (type `#`, or drag it in) and ask:

   > State the title of the attached spec and list its acceptance criteria as a numbered checklist. Do not
   > write tests yet and do not edit files.

5. Create your exact track folders under `Lab_Materials/Module5_Lab/` (for example,
   `sample-app/tests/web/` and `test-artifacts/web/`).

**What you should see:** green smoke tests, the correct criteria list, and empty output folders for your track.

> **✅ Checkpoint:** pytest runs and the smoke test passes before you continue.

---

## Exercise 1 · Two ways in — from code, then from criteria  (10 min)

**Goal:** see the difference between tests that mirror the code and tests that verify intent. *(This is the
whole module in one exercise.)*

**Steps**

1. **From the code first.** Attach **only the module under test**. In local Agent mode, ask Copilot to create
   exactly one test file from the implementation:

   > Generate pytest unit tests that describe what the attached implementation currently does. Create only
   > `Lab_Materials/Module5_Lab/sample-app/tests/<track>/test_from_code.py`; do not edit source or any other
   > file. Keep expected behaviour implementation-derived so we can critique it.

   If Agent mode is unavailable, ask for one code block in Ask mode, review it, and paste it into that exact
   file yourself. From `sample-app/`, run
   `python -m pytest tests/<track>/test_from_code.py -q`. Record what actually happens; generated tests are
   nondeterministic, so passing is not promised. Even a green result proves only agreement with the code.
2. **Now from the criteria.** Start a fresh Chat. Attach your **spec** and
   `testing-space/SPACE-instructions.md`. Attach the module only so Copilot can bind the criteria to its
   public names; expected outcomes must come from the spec. Ask:

   > Generate pytest tests **from these acceptance criteria and intent — not from the implementation's
   > current behaviour**. Cover happy paths, boundaries, and negative cases. Name the criterion each test
   > covers. Preserve every `TBC` or missing interface as an explicit gap; do not invent it or create an
   > always-green placeholder. Use the attached module only for imports/signatures. Create only
   > `Lab_Materials/Module5_Lab/sample-app/tests/<track>/test_from_criteria.py`; do not edit source.

3. Before running, make the lesson deterministic: verify the criteria file contains at least one correct
   probe from your row below. Add it yourself if Copilot omitted it.

   | Track | Required red probe against the supplied sample app |
   | --- | --- |
   | Web / Drupal or QA | Token invalid at 31 minutes **or** known response equals unknown response. |
   | Data & Analytics or Power BI | Active users equals **4** **or** breach IDs equal `["T8"]`, using the supplied oracle clock/data. |
   | RPA | `{"approved": False}` causes no calls **or** CRM-down status is not `closed`. |

   From `sample-app/`, run the criteria file. At least one required probe is red on the untouched seeded
   app. Review all other failures: keep only assertions supported by the spec and scaffold.
4. In `Lab_Materials/Module5_Lab/test-artifacts/<track>/01-code-vs-criteria.md`, record the observed
   from-code result, the deterministic criteria failure, and why the difference matters.

**What you should see:** an observed code-derived result and a deterministic criteria-derived red on a real
disagreement, without fabricated tests for missing interfaces.

> **✅ Checkpoint:** You can name a behaviour the supplied code gets wrong and show the criteria-derived
> test that catches it.

---

## Exercise 2 · Find the bug, fix the code  (10 min)

**Goal:** turn a red criteria-test into a real fix — of the **code**, not the test.

**Steps**

1. Review the failing criteria tests from Exercise 1. Separate genuine executable-criterion failures from
   bad setup, invented policy, and requirements the scaffold cannot expose. Ask Copilot to explain each
   genuine failure:

   > This test fails. Explain the discrepancy between the acceptance criterion and the code's behaviour.
   > Identify the root cause in the source. Do not change the test to make it pass.

2. **Fix the source** in `sample-app/src/` for every genuine executable-criterion failure in your criteria
   file. Do not invent APIs for recorded gaps. Confirm each edit is a real rule correction, not a value
   copied merely to satisfy the sample.
3. Re-run your track's tests **and** the smoke test: `python -m pytest tests/<track>/ tests/test_smoke.py -q`.
   The criteria test goes green **because the code is now correct**.
4. Record at least one defect in
   `Lab_Materials/Module5_Lab/test-artifacts/<track>/02-bug-and-fix.md`: the criterion, root cause, fix,
   and test that now guards it. List any other fixed criteria failures too.

> **Guardrail:** if a test is genuinely wrong (asserts something the criteria don't require), fix the test —
> but never weaken a correct test just to get green. That is how bugs ship.

> **✅ Checkpoint:** Criteria-based tests found real defects, you fixed the **code**, and all supported tests
> (including smoke) are green; unsupported criteria are documented gaps, not failing placeholders.

---

## Exercise 3 · Coverage that means something  (10 min)

**Goal:** make coverage traceable, then prove your tests can actually fail.

**Steps**

1. Ask Copilot for the gaps:

   > Given these acceptance criteria and my current tests in `tests/<track>/`, build a matrix of
   > **criterion → test(s) → layer → covered? (yes/partial/no)**. List every criterion with **no** meaningful
   > test. Do not edit files.

   Save it as `Lab_Materials/Module5_Lab/test-artifacts/<track>/03-coverage-matrix.md`. For every `no`, state
   whether a supported test can be added or an interface/environment is missing.
2. **Close one supported gap** — for example stored-digest shape/consumed-token validity (Web/QA), exact
   30-day boundary (Data/Power BI), or customer-ID forwarding and call order (RPA). Do not fabricate an
   idempotency, API, freshness, RLS, audit, or accessibility seam.
3. **Prove your tests can fail.** Pick one passing test and temporarily break either the code or the
   expectation; confirm it goes **red**; then restore. A test that stays green when the behaviour breaks is
   worthless — replace it.

**What you should see:** a matrix that names uncovered criteria, one new test closing a gap, and evidence
that your key tests can fail.

> **✅ Checkpoint:** Every criterion is either covered by a test that can fail, or listed as an explicit gap
> with an owner.

---

## Exercise 4 · Add your track's test type  (12 min)

**Goal:** cover the seam that matters most for your track, at the right level.

| Track | Runnable evidence to add | Described gap evidence (do not claim executed) |
| --- | --- | --- |
| **Web/Drupal** | Domain-contract tests for neutrality, exact expiry boundary, reuse, and stored-digest shape; save `04-domain-contract.md` | HTTP 202 mapping, raw-token delivery/lookup, password update/login, rate limiting, UI/a11y |
| **Data & Analytics** | Data-quality tests for defined open/negative/unknown-channel cases plus oracle metrics; save `04-data-quality.md` | Other schema/range rules, freshness, and referential integrity until ingestion/pipeline/join contracts exist |
| **Power BI** | Python reference-calculation tests; active=4, average=31.0, quarantine=3, breach IDs=`["T8"]`; save `04-reference-validation.md` | DAX, PBIX, RLS, refresh, visuals/traffic light in a Power BI-capable environment |
| **QA** | Coverage architecture plus the domain/unit layer supported by this scaffold; save `04-test-architecture.md` | Real API/E2E/login/rate-limit/a11y layers and their required environment |
| **RPA** | Process regressions for gates, call order, customer ID, CRM non-success, and no confirmation after failure; save `04-regression.md` | Durable idempotency, audit trail, approver identity, and template ID until interfaces exist |

**Steps**

1. Attach your spec, the module under test, and (Data/Power BI) `KNOWN-GOOD-METRICS.md`. Ask Copilot for the
   runnable test type above, into the exact
   `Lab_Materials/Module5_Lab/sample-app/tests/<track>/` folder. For a **fake `Systems`** (RPA), ask it to
   record operation + customer ID and be able to raise `CrmUnavailable`.
2. Run the new tests. Review each against the table — **read the assertions**, don't just watch the colour.
3. Keep `TBC` values and absent interfaces in the described-gap note. A guessed value or always-green
   placeholder is not a passing test.

**Example prompt (RPA):**

> From the attached spec and `account_closure.py`, write pytest regression tests using a fake `Systems`
> object that records calls and can raise `CrmUnavailable`. Cover: approved happy path and exact call order;
> approval present but not approved; no approval; open tickets; and CRM unavailable with a non-success
> result and no confirmation email. Assert on **calls and customer IDs**, not just status. Create only
> `Lab_Materials/Module5_Lab/sample-app/tests/rpa/test_closure.py`. List durable idempotency/audit/template
> checks as gaps because the interface does not expose them.

> **✅ Checkpoint:** Your track's highest-value seam has meaningful, readable tests — and you verified them
> against the checklist, not the colour.

---

## Exercise 5 · Test data and resilience  (10 min)

**Goal:** make the awkward inputs cheap, and keep the suite honest and stable.

**Steps**

1. **Generate synthetic edge data.** Ask Copilot:

   > Generate a reusable pytest fixture/factory of **synthetic, privacy-safe** records for `<track>`.
   > Include representative valid, boundary, empty, unicode, legacy, and a **bounded** oversized example,
   > but use only a case whose expected behaviour is defined by the attached spec in an executable test.
   > Mark undefined behaviours as questions; do not invent assertions. No real PII or unbounded allocation.
   > Put it in `Lab_Materials/Module5_Lab/sample-app/tests/<track>/conftest.py` and use one supported case.

2. **Add one resilience/edge test** whose expected result is defined (e.g. an RPA dependency failure, the
   exact 30-minute reset boundary, or a ticket exactly at—not over—its SLA threshold).
3. **Keep green honest.** Ask Copilot to review your suite for tests that can't fail or that duplicate each
   other, then act on it:

   > Review my tests in `tests/<track>/`: flag any test that cannot fail, any that only restates the code,
   > and any redundant duplicates. List them; do not edit.

4. Record what you added/pruned in
   `Lab_Materials/Module5_Lab/test-artifacts/<track>/05-test-data-and-resilience.md`.

**What you should see:** edge-heavy synthetic data behind your tests, one new resilience case, and a suite
with no dead-weight or always-green tests.

> **✅ Checkpoint:** Your tests exercise the awkward inputs, and you removed or fixed anything that couldn't
> fail.

---

## Exercise 6 · Assemble the suite and call the gate  (9 min)

**Goal:** decide honestly whether this suite's green could gate a release. *This is the point of the lab.*

**Steps**

1. Ask Copilot to assemble
   `Lab_Materials/Module5_Lab/test-artifacts/<track>/06-suite-handoff.md` with:
   - what's tested and at which layer;
   - the criterion-coverage matrix (from Ex 3), updated;
   - the defect you found and fixed (Ex 2);
   - remaining gaps and each `TBC`, with an owner;
   - suite stats (counts by layer) and known flakiness (if any);
   - readiness: **Gate-ready**, **Gate-ready with stated gaps**, or **Not gate-ready**, with a reason;
   - an explicit distinction between **executed evidence** and described future tests.
2. Ask Copilot to critique it against the trust checklist, then **you** verify:

   > Critique this suite against `testing-space/test-trust-checklist.md` and the spec. Check traceability,
   > tests-intent-not-code, can-fail, edges, right-level, synthetic data, and honest status. List gaps by
   > severity and cite the file. Do not edit anything.

3. Verify every claim yourself. Add a human sign-off line: name/initials, date, readiness status, remaining
   risk. **Do not** choose *Gate-ready* while a blocking criterion is uncovered or a blocking `TBC` is open.

**What you should see:** a short, navigable suite hand-off and a defensible gate decision — not an automatic
"all green, ship it".

> **✅ Checkpoint:** You can trace **criteria → tests → run → fix → coverage → trusted suite**, and your
> readiness status is honest about what is still uncovered.

---

## Wrap-up  (5 min)

Talk it over with the person next to you:

- Where does your team have the weakest coverage today — and which failure mode (mirror-bugs, coverage
  theatre, blind trust in green, AI grading AI) bites you most?
- What would make you trust a passing suite you didn't write?
- Which `TBC` blocked a real test, and who owns confirming it?

---

## Your deliverables checklist

1. ☐ `01-code-vs-criteria.md` — the observed code-derived result versus the deterministic criteria failure.
2. ☐ `02-bug-and-fix.md` — a real defect, fixed in the **code**, now guarded by a test.
3. ☐ `03-coverage-matrix.md` — criterion → test → layer → covered?, with gaps named.
4. ☐ Track-specific `04-*` tests + note (domain-contract / data-quality / reference-validation /
   test-architecture / regression), with unsupported layers named as gaps.
5. ☐ `05-test-data-and-resilience.md` — synthetic fixtures + one resilience test; dead-weight pruned.
6. ☐ `06-suite-handoff.md` — coverage, gaps/owners, and an honest gate-readiness sign-off.
7. ☐ A green **supported** suite (your track's runnable tests + smoke), with the fixed code; no fake passing
   placeholders for unavailable interfaces.

---

## Stretch goals — VS Code Copilot only

- **Prove it with a mutation:** change one operator in the fixed code (e.g. `>=` → `>`) and confirm a test
  catches it. If nothing goes red, your suite has a hole.
- **Defect hotspots:** ask Copilot which module is riskiest (most branching / most criteria) and add tests
  there first.
- **Coverage report:** run `python -m pytest --cov=src` (`pytest-cov` is pinned in `requirements.txt`) and
  read it as a *map of gaps*, not a score to chase.
- **E2E draft (Web/Drupal):** have Copilot draft a Playwright happy-path script from the spec; label it
  **not executed** unless a browser and running application are actually set up.
- **Visual/described a11y:** ask for the accessibility checks the flow needs, and mark which require manual
  validation.

---

## Troubleshooting

- **Smoke test fails to collect / import errors:** run pytest **from the `sample-app/` folder** so
  `conftest.py` is picked up; confirm `python -m pytest -q` (not a globally different Python).
- **Agent mode is missing:** stay in Copilot Chat Ask mode and create/edit the test files yourself. Do not
  switch to a cloud or third-party agent.
- **All the generated tests pass and you're suspicious:** re-run from the **criteria** with the spec
  attached and verify your row's required red probe (Exercise 1).
- **A from-code test fails:** inspect its setup and assumptions first; generation is nondeterministic, and
  a failure does not by itself prove a product defect. Judge it against the spec.
- **A test asserts the buggy behaviour:** that's the *tests-mirror-bugs* failure mode — regenerate from the
  criteria, and fix the **code**, not the criterion.
- **Copilot invented a threshold/policy value:** replace it with a parameter marked `TBC with Security`; a
  guessed number is not a valid assertion.
- **A metric test disagrees with the code:** `KNOWN-GOOD-METRICS.md` is the oracle — the **code** is wrong,
  not the oracle. Fix the measure.
- **Password tests affect one another:** reset the module-level synthetic outbox before and after every test.
- **Power BI:** Python green validates reference calculations only, not DAX/PBIX/RLS/refresh/visuals.
- **RPA idempotency/audit/template test cannot be written:** expected — the scaffold lacks those seams.
  Record the gap and owner; do not invent production interfaces.
- **Flaky test:** ask Copilot *"why is this test intermittent?"*, stabilise it, and never let self-healing
  hide a real regression — review a healing change like any other diff.
- **Green but you don't trust it:** run the trust checklist (Ex 6). If a key test can't be made to fail,
  it isn't testing anything.

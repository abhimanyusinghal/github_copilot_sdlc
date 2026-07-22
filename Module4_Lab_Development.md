# Lab 4 · From a Buildable Design to Working Software

**Participant handout · Module 4 · Level 300 · Development (Building with AI) · Novnex**

**Time:** ~75 minutes (core exercises 0–6, including wrap-up; stretch if time allows)

---

## Before you start

**Where we are.** Lab 3 produced a **buildable design** — a contract, a data model, ADRs. Today you turn
that design into **working software** with GitHub Copilot, and — the part that matters most now — you
**review and secure** what comes out. **Module 5** makes the tests trustworthy; today you make the change
real, reviewed, and safe.

> **Didn't finish Lab 3? You're fine.** A complete design package per track is in
> `Lab_Materials/Module4_Lab/design/`, and a scaffold to build into is in `starter-app/`. Nothing today
> depends on having finished Lab 3.

**The through-line — keep the thread alive.** Modules 2–3 ran *need → story → design*. Module 4 continues it:

> **Design → Implement → Review → Secure → Test → Build-ready change**

**The development rule:** *generation is cheap; judgement is the job.* Copilot drafts code fast — so the
skill shifts from **writing** to **judging**. You build to the contract, **review every line**, reject the
weak suggestions on purpose, and a human owns the hand-off and any later merge decision.

**By the end you'll be able to:**

- Implement a feature **to a contract and ADR** with Copilot agent mode, until the acceptance tests are green.
- Match the **mode to the task** — completions for flow, chat to understand, agent for a whole feature.
- Run a **two-pass review** (Copilot first, human second) and a **security pass** before committing.
- **Reject** a weak or insecure suggestion deliberately, and ground Copilot in your conventions.
- Hand off a **small, reviewed, tested** change that's ready for Module 5.
- Catch four development failure modes: **unreviewed output, secrets in prompts, invented policy, and no tests**.

### Tool boundary for this lab

All Copilot work happens in **GitHub Copilot inside VS Code**. Do not use Copilot on github.com, Copilot
Spaces, GitHub Spark, the Copilot CLI, a background agent, or a Copilot cloud agent. Use local Chat,
local Agent mode when available, VS Code's Source Control view, and `pytest` in the integrated terminal.
A normal GitHub Issue may be created from the VS Code GitHub Pull Requests and Issues extension **or the
repository's standard GitHub Issues page**; issue creation is not Copilot usage. Do not assign it to
Copilot or invoke any Copilot web/cloud workflow.

### You'll need

- **VS Code** with **GitHub Copilot** enabled. Use local **Agent mode** when available. If your organization
  disables Agent mode, use Chat in **Ask mode** and apply the edits yourself — every core step still works.
- **Python 3.10+**. Commands below use `python`; if that command is unavailable, consistently substitute
  `py -3` on Windows or `python3` on macOS/Linux. Install the pinned lab dependency from
  `Lab_Materials/Module4_Lab/starter-app/requirements.txt`.
- The repository open at its **root** so `Module4_Lab_Development.md` and `Lab_Materials/Module4_Lab/` are visible.
- Optional issue creation only: either the **GitHub Pull Requests and Issues** VS Code extension or access
  to the repository's standard GitHub Issues page, with permission to create issues.

> **Privacy & IP:** never paste secrets, keys, real customer data, or code you are not authorized to share
> into prompts. Use only the fictional Acme materials and follow your organization's Copilot policy.

### Lab materials

- `design/` — the **Lab 3 design package** per track (contracts, ADRs, models) — what you build to.
- `starter-app/` — a Python **scaffold** with stubbed logic and **failing acceptance tests** as the build target.
- `issues/` — a **well-scoped issue brief** per track to attach to local Agent/Chat.
- `dev-space/` — conventions to ground Copilot: `copilot-instructions.md`, `coding-standards.md`,
  `glossary.md`, `nfr-standards.md`, `definition-of-done-dev.md`.
- `review-checklist.md` — the two-pass review + security checklist.

**Tracks:** choose **Web/Drupal, Data & Analytics, Power BI, QA, or RPA**. Each builds one module:

| Track | Design | Issue brief | Build target (under `starter-app/`) | Acceptance file | Artifact folder |
| --- | --- | --- | --- | --- | --- |
| Web / Drupal | `design/web-drupal/` | `issues/web-reset-issue.md` | `src/password_reset.py` | `tests/acceptance/test_password_reset.py` | `dev-artifacts/web/` |
| QA | `design/web-drupal/` | `issues/web-reset-issue.md` | `src/password_reset.py` | `tests/acceptance/test_password_reset.py` | `dev-artifacts/qa/` |
| Data & Analytics | `design/data-analytics/` | `issues/data-metrics-issue.md` | `src/support_metrics.py` | `tests/acceptance/test_support_metrics.py` | `dev-artifacts/data/` |
| Power BI | `design/power-bi/` | `issues/data-metrics-issue.md` | `src/support_metrics.py` (Python reference only) | `tests/acceptance/test_support_metrics.py` | `dev-artifacts/power-bi/` |
| RPA | `design/rpa/` | `issues/rpa-closure-issue.md` | `src/account_closure.py` | `tests/acceptance/test_account_closure.py` | `dev-artifacts/rpa/` |

All table paths except artifact folders are relative to `Lab_Materials/Module4_Lab/`; artifact folders live
directly under that directory. If you share a repository, work on a separate branch.

---

## Exercise 0 · Pre-flight and load the design  (7 min)

**Goal:** prove the toolchain works and know what you're building.

**Steps**

1. Open the repo root in VS Code and open **Copilot Chat** (Agent mode if available).
2. From `Lab_Materials/Module4_Lab/starter-app/`, run:

   ```bash
   python -m pip install -r requirements.txt
   python -m pytest -q
   ```

   Expect **2 passed** (smoke) and **15 failed** (acceptance). The red is your build target. If `python`
   is unavailable, use the launcher fallback listed above for both commands.
3. Open your track's **design** folder and its **issue**. Open the stub module you'll implement.
4. **Ground Copilot:** attach `dev-space/copilot-instructions.md` to Chat using **Add Context** (type `#`
   or drag the file in). Do not overwrite an existing repository-level Copilot instructions file.
5. Create only your selected `Lab_Materials/Module4_Lab/dev-artifacts/<track>/` folder.

**What you should see:** smoke green, acceptance red, and the design + stub open.

> **✅ Checkpoint:** pytest runs, and you can point to the acceptance tests that define "done" for your track.

---

## Exercise 1 · Understand the design, match the mode  (8 min)

**Goal:** plan the build and use the right Copilot mode for each part.

**Steps**

1. **Understand first.** Attach your issue brief, design files, acceptance file, and stub, and ask Chat:

   > `/explain` what this module must do to satisfy the attached contract and acceptance tests. List the
   > functions, their responsibilities, and the tricky rules (expiry boundary, uniform response, quarantine,
   > approval gate). Do not write code yet.

2. Attach the acceptance file directly (or use `#codebase`) and ask: *"What exactly does each acceptance
   test assert, and which design rule does it trace to?"* Verify the answer against the file yourself.
3. **Try a completion.** In the stub, write a precise intent comment above one small function and let Copilot
   suggest a line or two. **Read the suggestion before accepting it.** Notice how a clear comment/signature
   steers it.
4. Note your plan in `Lab_Materials/Module4_Lab/dev-artifacts/<track>/01-plan.md`: which parts you'll give
   to local **Agent mode**, which
   you'll write with **completions**, and the rules you must not get wrong.

> **✅ Checkpoint:** You can explain, in your words, what "green" requires — before generating the bulk of it.

---

## Exercise 2 · Implement to the contract with agent mode  (14 min)

**Goal:** build the module to the design until the acceptance tests pass — the payoff of a clear design.

**Steps**

1. In local **Agent mode**, attach your issue, design files, acceptance file, house rules, and point it at
   the exact root-relative targets (adapt to your track):

   > Implement `Lab_Materials/Module4_Lab/starter-app/src/<module>.py` to the attached design so that
   > `Lab_Materials/Module4_Lab/starter-app/tests/acceptance/<file>` passes. Modify only the source module.
   > Do **not** modify acceptance tests or invent interfaces/policy. Run the targeted tests from
   > `starter-app/`, follow the attached house rules, and show me the diff.

2. Let it edit, run tests, and self-heal. Watch the diff as it goes — you are reviewing, not just waiting.
3. From `starter-app/`, re-run yourself:
   `python -m pytest tests/acceptance/<file> tests/test_smoke.py -q`. Iterate until green.
4. **Read the result now, before reviewing formally.** If any line does something you don't understand,
   ask `/explain` — don't move on past code you can't follow.

> **Guardrail:** if the agent tries to "fix" a failing test by editing the test, stop it. The criteria are
> fixed; the **code** changes to meet them.

> **✅ Checkpoint:** Your track's acceptance tests (and the smoke test) are green, and you can explain how
> each rule is met.

---

## Exercise 3 · Review — Copilot first, human second  (10 min)

**Goal:** treat the generated code exactly like a capable junior's draft.

**Steps**

1. **Copilot's pass.** In Chat, attach the changed source, design, acceptance file, and
   `review-checklist.md`, then ask:

   > Review my changes to `src/<module>.py` against `review-checklist.md` and the design. Flag issues by
   > severity (correctness, security, clarity). Suggest fixes but do not apply them.

   If your VS Code Source Control view also shows a **Code Review** button, you may run it as an additional
   local pass; availability depends on the Copilot plan and organization policy, so it is not required.
2. **Your pass.** Walk `review-checklist.md` yourself — intent, design fit, edge cases (expiry boundary,
   uniform response, quarantine, CRM-down, no-approval). These are what a tool won't feel.
3. Apply the fixes you agree with; note anything you deferred, with a reason, in
   `Lab_Materials/Module4_Lab/dev-artifacts/<track>/03-review-notes.md`.

> **✅ Checkpoint:** Both passes are done, the diff is small enough to read fully, and you can explain every line.

---

## Exercise 4 · Secure as you write — and reject on purpose  (9 min)

**Goal:** catch a vulnerability at write-time, and practise saying no to Copilot.

**Steps**

1. **Security pass** — before you'd commit, ask:

   > Review this change for security: injection, secrets/PII in code or logs, account enumeration,
   > weak token handling, missing input validation. Show the risky line and a safer version.

   Act on any **real, in-scope** finding. If it finds none, record the evidence-based no-change result; do
   not manufacture a vulnerability merely to satisfy the exercise.
2. **Reject on purpose.** In **Ask mode**, ask Copilot to evaluate one unsupported proposal below without
   editing files. Reject it and explain which missing decision or interface blocks it:

   | Track | Weak proposal to evaluate and reject |
   | --- | --- |
   | Web / Drupal or QA | Hard-code a "sensible" rate-limit threshold even though it is `TBC with Security`. |
   | Data & Analytics | Silently drop invalid rows so the published average looks cleaner. |
   | Power BI | Claim green Python tests prove DAX, PBIX, RLS, visuals, and refresh are correct. |
   | RPA | Invent retry/idempotency/audit/template APIs that are absent from the supplied contract. |

   Keep `TBC` values and interface gaps explicit rather than guessing.
3. Record the security-pass result, any real finding/fix, and the suggestion you rejected in
   `Lab_Materials/Module4_Lab/dev-artifacts/<track>/04-security-and-rejections.md`.

> **✅ Checkpoint:** The security pass is documented, every real finding was addressed or owned, and you
> deliberately rejected one unsupported suggestion.

---

## Exercise 5 · Debug, then carry a test  (9 min)

**Goal:** use Copilot to shorten a debugging loop, and make sure the change ships with a test.

**Steps**

1. **Choose a supported edge beyond the provided acceptance assertions:** consumed token reports invalid
   (Web/QA), a login exactly 30 days old (Data/Power BI), or correct customer ID and call sequence through
   the RPA fake. Do not invent a requirement.
2. Add one regression test under
   `Lab_Materials/Module4_Lab/starter-app/tests/<track>/`. Prove it can fail by making a **temporary,
   one-line mutation**, running the targeted test to see red, and immediately restoring the line. If the
   unmutated implementation genuinely fails, diagnose it with Chat and fix the source instead.
3. If the code got gnarly, ask for a small, safe **refactor behind the green tests** ("extract a helper; keep
   behaviour"), and re-run.
4. Note the probe, red evidence, any real fix, and the restored green run in
   `Lab_Materials/Module4_Lab/dev-artifacts/<track>/05-debug-and-test.md`.

> **✅ Checkpoint:** Every change you made is covered by a test that can fail, and your track's tests plus
> smoke are green. Other tracks' stubs may remain red.

---

## Exercise 6 · Hand off to testing  (8 min)

**Goal:** package a small, reviewed, tested change that Module 5 can build on. *This is the point of the lab.*

**Steps**

1. Ask Copilot to summarise the change into
   `Lab_Materials/Module4_Lab/dev-artifacts/<track>/06-change-summary.md`:
   - what was implemented and which **acceptance criteria** it meets;
   - the review findings and the suggestion you rejected;
   - the security pass result;
   - the tests that now guard it, and any remaining `TBC`/gap with an owner.
2. Check it against `dev-space/definition-of-done-dev.md`. Be honest: **Done**, **Done with stated gaps**, or
   **Not done** — don't mark Done while a criterion is unmet or a blocking `TBC` is open.
3. Add a human sign-off line: name/initials, date, status, remaining risk. A human owns the hand-off.
4. **Optional GitHub record:** if your team wants a normal issue, create one from the supplied brief using
   the VS Code GitHub Pull Requests and Issues extension's **Issues** view or the repository's standard
   GitHub Issues page. Do not use Copilot on github.com and do not assign the issue to Copilot.

> **✅ Checkpoint:** You can trace **design → implement → review → secure → test → build-ready change**, and
> your "done" status is honest.

---

## Wrap-up  (5 min)

Talk it over with the person next to you:

- Which coding task would you hand to an agent first — and which would you still write yourself?
- How will your team keep **review** from becoming the bottleneck as generation speeds up?
- What did grounding Copilot in `copilot-instructions.md` change about the output?

---

## Your deliverables checklist

1. ☐ `01-plan.md` — your build plan and the mode you chose for each part.
2. ☐ An implemented module with your track's **acceptance tests green** (+ smoke).
3. ☐ `03-review-notes.md` — Copilot pass + your human pass against the checklist.
4. ☐ `04-security-and-rejections.md` — the security-pass result, any real fix, and one deliberate rejection.
5. ☐ `05-debug-and-test.md` — a supported edge probe, red evidence, any real fix, and restored green.
6. ☐ `06-change-summary.md` — a clean hand-off with an honest DoD status and human sign-off.
7. ☐ Optional: a normal GitHub Issue created from VS Code (not delegated to Copilot).

---

## Stretch goals — VS Code Copilot only

- **Refactor for clarity:** ask Copilot to simplify the messiest function behind the green tests; confirm behaviour is unchanged.
- **Explain to a newcomer:** have Copilot generate docstrings and a short module overview from your finished code.
- **Second implementation:** ask for an alternative approach to one function and compare — which is simpler and easier to review?
- **Tighten the grounding:** add one house rule to `copilot-instructions.md`, regenerate a piece, and see if the style improves.

---

## Troubleshooting

- **Smoke fails / import errors:** run pytest **from `starter-app/`** so `conftest.py` is used; check `python --version` is 3.10+.
- **Metrics tests can't find data:** run from `starter-app/`; the tests resolve `../../data` relative to themselves.
- **Agent edited the acceptance tests:** discard those hunks — the criteria are fixed; re-prompt "implement the source only; do not modify tests".
- **Agent changed unrelated files:** review the diff and keep only the intended hunks; re-prompt with the exact target file.
- **Output ignores the house style:** attach `dev-space/copilot-instructions.md` and regenerate; do not
  overwrite repository-level instructions during the lab.
- **Agent mode unavailable:** use Chat Ask mode and apply edits yourself — the build target is the same.
- **Copilot invented a threshold/policy value:** reject it; use a named `TBC` constant. A guessed number is not a design decision.
- **You can't explain a line the agent wrote:** don't keep it. `/explain` it, or rewrite it until you can.
- **Power BI:** green Python tests prove only the reference calculations. Record DAX/PBIX/RLS/refresh as
  unverified until tested in a Power BI-capable environment.
- **RPA:** the scaffold cannot prove durable idempotency, audit events, or template use. Record those gaps;
  do not invent interfaces to make the checklist green.

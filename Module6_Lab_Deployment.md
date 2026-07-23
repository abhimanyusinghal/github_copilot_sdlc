# Lab 6 · Shipping Safely

**Participant handout · Module 6 · Level 300 · Deployment · Novnex**  ·  **Time:** ~75 min

---

## Before you start

Lab 5 gave you a suite you trust. Today you put it to work on a **real GitHub repo**: a pipeline that gates on
your tests, an approval a human actually clicks, and a rollout that fails small.

**The thread:** `Trusted suite → Pipeline → Green → Safe rollout → Release notes → Go/No-Go`

**The rule:** automate the steps, but a **human approves what ships** — deployment is where a mistake reaches
every user at once.

> **Didn't do Lab 5?** No problem — you start from a template repo with a passing app and a broken pipeline.

**Setup**
- **AI stays in VS Code** (your BYOK model). Use GitHub's normal features — repos, Actions, PRs, Issues,
  environments, secrets — but **no AI on github.com** (no "Explain error", no Autofix). Copy a failing log
  *into VS Code* to reason about it.
- A **free GitHub account** signed into VS Code (GitHub Pull Requests and Issues extension).
- **Python 3.11** (matching CI) for local app tests. The standard-library checker itself supports 3.10+.
  Use your installed launcher (`python`, `py -3.11`, or `python3.11`).
- Keep `Lab_Materials/Module6_Lab/` available alongside your cloned repo in the same VS Code workspace;
  material paths below are relative to that folder.
- **No GitHub access?** The analysis, workflow, plans, and drafts have offline substitutes — see
  Troubleshooting. Hosted controls such as branch protection and approval cannot be proven offline, so
  record them as simulations. Nothing here deploys to a real system.

**Pick a track** — the pipeline work is shared; your rollout gate differs: Web (5xx/latency) · Data (data
tests + freshness) · Power BI (refresh + measure validation) · QA (suite as a hard blocker) · RPA (pause
new runs; protect in-flight work). Put files in `release-artifacts/<track>/`.

---

## Exercise 0 · Make your repo and see it go red  (8 min)

**Goal:** get your own repo and watch the pipeline fail for real.

1. Open the template repo — **https://github.com/abhimanyusinghal/acme-portal-lab** — and choose
   **Use this template → Create a new repository** (**Public**). Clone it
   and open it in VS Code.
2. Open the repo's **Actions** tab. If template creation did not start **CI** automatically, select
   **CI → Run workflow → Run workflow**. The run is **red**. Open the failed **test** job and read the
   log. Don't fix anything yet.

*Offline (from the course repo):* open
`Lab_Materials/Module6_Lab/pipeline/failing-run.log`, then run
`python Lab_Materials/Module6_Lab/pipeline/check_pipeline.py Lab_Materials/Module6_Lab/pipeline/ci-broken.yml`
→ **1/8**. Use `py -3` or `python3` instead of `python` if that is your installed launcher.

> **✅** You have a repo, the pipeline is red, and you can see the failing step.

---

## Exercise 1 · Diagnose the red build  (9 min)

**Goal:** find the real cause, in VS Code.

1. Copy the failing log from Actions (or open `failing-run.log`) and attach it with
   `.github/workflows/ci.yml` (online repo) or `pipeline/ci-broken.yml` (offline):
   > This CI run failed. Explain what failed and why, citing the log lines. Then find the **root cause in the
   > workflow** — not just the symptom. Don't edit files.
2. Verify it against the log — the symptom (missing module) and cause (missing step) differ.
3. Ask for the minimal fix and record the diagnosis in `01-diagnosis.md`.

> **✅** You can state the root cause and point to the evidence.

---

## Exercise 2 · Fix, harden, and prove the gate  (14 min)

**Goal:** a green pipeline whose test suite actually blocks a merge.

1. On a branch, attach `ci.yml` and `platform-space/deploy-standards.md`, and fix it one concern at a time:
   > Fix `ci.yml` per the attached standards: install deps before tests; pin actions to the approved
   > **full commit SHAs**; least-privilege `permissions:`; replace the hardcoded token with a secret
   > reference; run production only on `workflow_dispatch`, never on a PR or ordinary push; deploy as a
   > **10% canary**; and run the rollback script under `if: failure()`. Explain each change. Use thresholds
   > from `environments.md`; don't invent them.
2. Validate locally: `python check_pipeline.py .github/workflows/ci.yml` → work up to **8/8**. Then commit,
   push, and open a **PR** — watch its **test** check go **green** and its production job be **skipped**.
3. **Make the suite a real gate:** Settings → Branches → add a classic protection rule for `main` →
   **Require status checks** → the **test** check. Also enable **Do not allow bypassing the above
   settings**; otherwise you, as the repository administrator, could bypass your own lab gate.
4. Replace the committed lab token with `${{ secrets.DEPLOY_TOKEN }}`. Record that a real exposed
   credential would need rotation; this seeded value is fictional, so the lab simulates the incident
   response without creating or reusing a real credential.

For each change, be able to say what the permission allows, where the token comes from, and what the canary
slice is. *(Offline: make `pipeline/ci.yml` as a working copy of `ci-broken.yml`, then run the checker
against that copy until it reaches 8/8.)*

> **✅** The PR is green, the suite is a required check, and you can explain every line.

---

## Exercise 3 · Review the infrastructure  (9 min)

**Goal:** catch expensive, public mistakes before they ship.

1. Attach `iac/storage.tf` with `deploy-standards.md`:
   > Review this Terraform for security: intended and effective public access, encryption at rest, IAM
   > scope, credentials, automated backups, and deletion recovery. List findings by severity with the
   > line, any cloud/account-level assumption, and a safer version. Don't edit it.
2. Verify each finding yourself; fix the ones you agree with. Watch for the plaintext password (a real
   credential would require rotation), explicitly unencrypted RDS storage, disabled backups, and
   over-broad IAM. For S3, remember that AWS now applies SSE-S3 to new uploads by default; the finding is
   missing explicit enforcement of whichever encryption policy the organization requires (for example,
   SSE-KMS if required), not “objects are definitely unencrypted.”
   Record in `03-iac-review.md`.

> **✅** Every high-severity finding is fixed or owned, and credentials in code are flagged for rotation.

---

## Exercise 4 · Rollout, rollback, and a real approval gate  (13 min)

**Goal:** make failure small and put a human on the button before any release run starts.

1. Copy `rollout-plan-template.md` to `04-rollout-plan.md`, attach `environments.md`, and ask for a canary
   plan for release 2.4.0 with stages, health signals, and an explicit **rollback trigger and method**. Use
   the attached thresholds; mark unknowns `TBC`.
2. **Create the gate on GitHub:** Settings → Environments → new `production` → add yourself as a **Required
   reviewer**, then add an environment secret named `DEPLOY_TOKEN` with a random, disposable lab-only value.
   The deploy job already references `environment: production`. In this solo exercise, leave
   **Prevent self-review** off; in a real production repo, use a second reviewer and enable it. Do not start
   the release run yet — the go/no-go decision comes first.
3. Answer the three that make rollback real: the exact trigger (a number), whether it's been **tested** (if
   not, that blocks release), and whether it's **safe for the data**.

> **✅** A numeric rollback trigger, a named approver, and a protected environment ready to stop the release.

*Offline:* document the environment name, reviewer, secret **name** (never a value), and the expected
approve/reject path. The checker can validate the workflow configuration, but do not claim a hosted gate ran.

---

## Exercise 5 · Release notes from the PRs  (7 min)

**Goal:** kill the chore, then apply judgement.

1. Attach `release-input/merged-prs.md` and ask for two versions — a technical changelog and a customer-facing
   note — using only what's in the file.
2. Edit like a human: internal chores stay out of the customer note; a security fix is described as a fix, not
   an exploit; number-moving changes (metric/SLA fixes) need a heads-up to affected users. Save to
   `05-release-notes.md`.

> **✅** Nothing invented, nothing internal leaked, number-moving changes called out.

---

## Exercise 6 · Go / No-Go and merge  (9 min)

**Goal:** make an honest release call, then merge through review.

1. Assemble `06-go-no-go.md`: pipeline status, IaC findings, rollout + rollback trigger, release notes, open items.
2. Ask Copilot to critique it against `release-readiness-checklist.md`; verify yourself.
3. Record an honest status — **Ship / Ship with constraints / Hold** — with a named sign-off. Don't Ship with
   an untested rollback or an open high-severity finding. Then inspect and **merge your pipeline PR** (the
   green required check is what allows it).
4. In **Actions → CI → Run workflow**, dispatch the workflow from `main`. The test runs first and the
   production job waits for review. Enforce your decision: approve the simulated deploy only for **Ship**
   (or constraints that explicitly permit it); for **Hold**, reject it and capture that evidence.

> **✅** You can trace `suite → pipeline → green → rollout → notes → go/no-go → enforced gate`, and the
> merge went through a green check.

*Offline:* record the expected merge and approve/reject outcome in `06-go-no-go.md`; do not claim an actual
PR merge or environment review.

---

## Wrap-up  (5 min)

- Where would AI help most in your release process — and where must a human stay in control?
- What's your rollback story, and how would you make failure small?

## Deliverables
Your repo (red→green pipeline) · diagnosis · a PR with the suite as a required check · IaC review · a rollout
plan + an approval gate that enforces the decision · release notes · an honest go/no-go with sign-off.
For the offline track, submit the locally validated workflow and clearly labelled simulated PR, branch-rule,
environment-review, and approval evidence instead.

## Stretch
Add a new check to `check_pipeline.py` for your platform · risk-score the release from the PR list · push a
failing test and confirm the required check blocks the merge · design a feature flag for the risky change.

## Troubleshooting
- **No GitHub / Actions:** use `failing-run.log` + `check_pipeline.py` for the workflow and draft the hosted
  artifacts locally. Mark branch-protection, PR, and environment evidence as **simulated**.
- **No first run appeared:** Actions → CI → **Run workflow**. If that control is unavailable, confirm Actions
  is enabled and the workflow is present on the default branch.
- **First run wasn't red:** confirm you used the broken template and didn't already edit `ci.yml`.
- **A check still fails after the AI "fixed" it:** the right words may be in the wrong place. Fix the workflow, not the checker.
- **The AI suggests a tag such as `@v6` or invents a threshold:** reject it — use the approved full SHA;
  take numbers from `environments.md`.
- **Deploy didn't pause:** confirm the run was manually dispatched from `main`, `production` has a required
  reviewer, and the job sets `environment: production`.
- **Tempted to Ship with an untested rollback:** don't — record Hold or Ship with constraints.

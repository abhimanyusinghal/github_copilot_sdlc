# Lab 7 · Operating What You Shipped

**Participant handout · Module 7 · Level 300 · Maintenance & Support · Novnex**  ·  **Time:** ~75 min

---

## Before you start

A **P1 fired at 14:41 and is still firing**. You'll diagnose the incident **in VS Code**, then turn the
outcome into a real **Issue and fix PR** on your GitHub repo. This is the final lab, so we also close the
whole week.

**The thread:** `Detect → Diagnose → Confirm → Resolve → Learn → Sustain`

**The rule:** AI assists the operator; a human owns production. And: **a diagnosis is a hypothesis until you
confirm it in the source**. A reversible rollback can restore a change-correlated P1 before full root-cause
analysis, but a fix-forward must not be based on an unverified AI explanation.

> **Didn't do the earlier labs?** No problem — the incident is fully provided; for the GitHub parts, generate
> a fresh repo from the template.

**Setup**
- **AI stays in VS Code** (your BYOK model). Use GitHub's normal features — Issues, PRs, Actions, Dependabot —
  for the *outcomes*, but **no AI on github.com**. All the analysis is local files.
- A **free GitHub account** in VS Code, and your **Lab 6 repo** (or a fresh one from the template).
- **Python 3.11** (matching the lab workflow) for the contract test and legacy stretch. The deliberately
  old dependency snapshot is not supported on every newer Python runtime.
- For local tests, install the template repo's deliberately old exercise dependencies only in a disposable
  virtual environment. If you use CI for the test run, no local installation is required.
- **No GitHub access?** Use `Lab_Materials/Module6_Lab/template-repo/` as a local working copy. Draft the
  Issue and PR text, test the change locally, and label hosted outcomes as simulated.
- **⚠ Privacy:** read `ops-space/pii-and-prompts.md` first. The log is fictional, but treat it like
  production — **scan for PII and redact before pasting.** Never paste real customer data.

**Materials** in `Lab_Materials/Module7_Lab/`: `incident/` (alert, `app.log`, deploy history, the running code
and both config versions), `ops-space/` (standards + PII rules), `security/` (advisories fallback),
`legacy/`, and the runbook/postmortem templates + `operate-quality-checklist.md`.

**Pick a track** (prevention lens): Web (portal errors) · Data (freshness/quality alerts) · Power BI (refresh)
· QA (turn it into a regression/contract test) · RPA (bot exceptions). Notes go in `ops-artifacts/<track>/`.

---

## Exercise 0 · Take the page  (6 min)

**Goal:** get oriented and set the privacy habit first.

1. Read `ops-space/pii-and-prompts.md`.
2. Open `incident/alert.md`, `app.log`, and `deploy-history.md`.
3. **Scan the log for PII before attaching it** — find at least one customer email and decide how you'll
   handle it (redact, or attach an excerpt without it).

> **✅** You found PII in the log and decided how to handle it. (No PII in logs is also an NFR — it's a finding to fix.)

---

## Exercise 1 · Triage the alert  (8 min)

**Goal:** what's broken, for whom, and what changed?

1. Attach `alert.md`, `deploy-history.md`, `ops-space/alerting-standards.md`:
   > Triage this P1 in under 150 words: what's failing, the **blast radius**, **what changed recently**, and
   > the two most likely causes with the evidence to confirm each. Mark anything you're inferring. No action yet.
2. Check the timing yourself — when the symptom started vs when the last change landed.
3. Note severity, impact, and **two hypotheses** in `01-triage.md`.

> **✅** Two candidate causes, and you know what evidence would settle between them.

---

## Exercise 2 · Signal in the noise  (11 min)

**Goal:** turn 224 log records into a correctly-ranked short list.

1. Attach `app.log` (redacted) and `deploy-history.md`:
   > Cluster the log by signature. For each: count, first/last timestamp, **new or pre-existing**, and whether
   > it returns an error to a customer. Rank by **impact and novelty, not raw count**, and name the incident
   > cluster. Cross-check the "known pre-existing issues" in the deploy history.
2. Interrogate it: which cluster is **new**, which are **already ticketed**, which return **5xx**? Record in
   `02-log-analysis.md`, including the loud signal you **ruled out** and why.

> **Watch out:** the highest-count signal is *not* the incident. If your answer is the loudest one, re-read the known issues.

> **✅** You can name the incident cluster, its start time, and why the noisy ones aren't it.

---

## Exercise 3 · Confirm the cause in the source  (11 min)

**Goal:** prove it. *This is the point of the lab.*

1. The log names a file and line — open `incident/reset_service.py` and go there yourself first.
2. Attach `reset_service.py`, `app-config-v2.4.0.yaml`, and `app-config-v2.3.2.yaml`:
   > Explain the exact mechanism behind the error. Compare the config keys the code reads with what each
   > config version defines. State what confirms and what would refute it. Cite file and line. No fix yet.
3. Verify every claim against the files. Write it up in `03-root-cause.md` — mechanism, evidence
   (file:line, config key, timestamps), and the trigger vs the latent weakness.

> **✅** A mechanism with file/line/config evidence — not a story. If you can't point at the line, you haven't confirmed it.

---

## Exercise 4 · Resolve — Issue, contract test, PR  (13 min)

**Goal:** restore service with a human in control, and close the loop to the Lab 6 pipeline.

1. **File the incident** as a GitHub **Issue** (`INC-2026-0723-01`) with your confirmed cause and evidence —
   your audit trail. Put the incident ID in the issue title. Draft it in VS Code, then create it from the
   GitHub extension.
2. Attach `ops-space/escalation-policy.md`, ask for mitigation options (roll back / flag / fix forward) with
   trade-offs and **who approves each**, and name the human approver.
3. **Prevent the class:** on a branch in your repo, add a **config-contract test** that loads
   `config/app-config.yaml` and checks every rate-limit key `src/reset_service.py` reads exists. Run it —
   it **fails** (catches the incident). Then align the keys so it **passes**.
4. Open a **PR**, watch your **Lab 6 CI gate it** (red → green), and **review and merge**. Record options,
   approver, and the PR link in `04-resolution.md`.

*Offline:* write the contract test locally, confirm it fails then passes, and capture the Issue/PR text.

> **✅** An incident Issue, a contract test that **failed then passed**, and a PR merged through your green pipeline.

---

## Exercise 5 · Learn — runbook, postmortem, follow-ups  (10 min)

**Goal:** make the next person faster, and be honest about what went wrong.

1. Fill `runbook-template.md` → `05-runbook.md`. Test it: could the next on-call actually *execute* your
   confirm-steps? Name the signature, file, timestamp.
2. Ask for a **blameless** postmortem into `05-postmortem.md`, building the timeline from **actual timestamps**
   (verify each). Separate the trigger from the latent weakness.
3. File the **preventive actions as GitHub Issues** with owners — including the uncomfortable ones: the release
   went out at **100% with no canary**, and there was **PII in the logs**.

> **✅** A runbook with checkable steps, a verified timeline, and preventive-action Issues with owners.

---

## Exercise 6 · Sustain — dependencies, docs, honest status  (10 min)

**Goal:** keep the system healthy, and prioritise by real risk.

1. **Dependabot:** in repository **Settings**, choose **Advanced Security** in the Security section and
   enable **Dependabot alerts**. View them under
   **Security and quality → Dependabot → Vulnerabilities**.
   *(No alerts yet or offline? Use `security/dependency-advisories.md`.)*
2. Live alerts change as the advisory database changes. For a consistent group exercise, attach the
   captured scenario (or equivalent live alerts) with `security/requirements.txt`:
   > Triage these for **our** system: is each actually **reachable**, what's the **real exposure**, and the
   > right action (bump / remove / mitigate)? Rank by real risk, not severity label.
3. Argue with it — an unused **High** is a **removal**, a **Critical** whose vulnerable path is not
   reachable ranks lower, and a reachable **Moderate** on customer-controlled input is real. Run
   `operate-quality-checklist.md`, then record an honest status
   (**Resolved / Mitigated with follow-ups / Ongoing**) with owners and a sign-off in `06-sustain.md`.

> **✅** Dependency order justified by reachability, and an honest status with every follow-up owned.

---

## Wrap-up & course close  (5 min)

- Which loud-but-harmless signal is your team's red herring?
- What would have caught this before production — and why don't you have it yet?
- Across the week, which one change will you take back first?

**The whole lifecycle, one platform:** Requirements → Design → Development → Testing → Deployment →
Maintenance — each phase fed the next. **The thread through all of it:** AI proposes and accelerates; humans
decide and stay accountable. **On Monday:** pick one workflow, ground it in your context, measure the
before/after, set the guardrails, share what you learn.

## Deliverables
Triage · ranked log analysis · a confirmed root cause · a GitHub Issue + a merged PR with a contract test that
failed then passed · a runbook + postmortem + preventive-action Issues · an honest sustain status with sign-off.
For the offline track, submit the fail→pass test evidence and clearly labelled Issue/PR drafts instead of
claiming hosted creation or merge.

## Stretch
Tame `legacy/legacy_sla_calculator.py` with characterisation tests before refactoring · file proactive Issues
for what's trending toward failure · propose faster monitors and one noisy alert to drop · sketch a custom ops agent.

## Troubleshooting
- **No GitHub / Actions:** work in the local Lab 6 template repo, run the contract test locally, draft the
  Issue/PR artifacts, and use the fixed dependency-advisory scenario. Mark all hosted evidence simulated.
- **The AI blames the highest-count warning:** ask it to re-rank by novelty and customer impact; attach `deploy-history.md`.
- **The explanation cites nothing:** reject it — require file, line, config key, timestamps, then check each.
- **The contract test passes when it should fail:** it must read the keys the **code** reads, with no fallback — it must fail before your fix.
- **No Dependabot alerts yet:** they may take a few minutes and the live set may differ; use the fixed
  scenario in `security/dependency-advisories.md`.
- **You pasted a customer email:** stop, redact going forward, and raise `redact_pii` as a real finding.
- **Tempted to mark Resolved:** if follow-ups are open with no owner, it's **Mitigated with follow-ups**.

# Lab 2 · From Notes to Build-Ready Requirements

**Participant handout · Module 2 · Level 300 · Requirements (Planning & Analysis) · Novnex**

**Time:** ~75 minutes (core exercises 0–6; stretch goals if time allows)

---

## Before you start

**What you'll do:** take a pile of **messy, contradictory notes** for your own role track and turn them, with GitHub Copilot, into **build-ready work** — structured requirements, a testable user story, a real GitHub Issue, an epic broken into sub-issues, and one validated criterion you can trace all the way to a test.

**The through-line — keep the thread alive.** Requirements rot when they drift from the work. Everything today builds one unbroken thread:

> **Need → Story → Issue → Criteria → Test**

**The one rule from Module 1 still applies:** *ground the context, review everything, humans own the decision.* Copilot drafts; **you and your stakeholders decide.** The validation is the deliverable — not the volume of text generated.

**By the end you'll be able to:**

- Turn notes, transcripts and screenshots into clear, de-duplicated requirements — and spot what Copilot **invented** or **dropped**.
- Write **testable** Given/When/Then acceptance criteria (no "fast", no "user-friendly").
- Create GitHub Issues and break an epic into sub-issues that an agent or a developer could pick up.
- Ground drafts in a Copilot **Space** so they use *your* terms, personas and standards.
- Catch the four requirements failure modes: **invented scope, false precision, lost intent, rubber-stamping.**

**How to read this handout:** each exercise has a **Goal**, numbered **Steps**, **What you should see**, and a **Checkpoint**. Do the steps — don't just read them. Prompts you can paste are shown in boxes; treat every result as a draft to verify.

**You'll need:**

- **GitHub Copilot in VS Code** — Copilot Chat with **Agent mode** enabled. *This entire lab runs inside VS Code — you never need the browser.*
- The **GitHub Pull Requests and Issues** extension (`GitHub.vscode-pull-request-github`) — so you can view and create Issues without leaving the editor.
- For Copilot to create Issues **for** you, enable **GitHub tools in Agent mode** (the GitHub MCP server). If you can't, a draft-and-paste fallback (below) keeps everything in VS Code anyway.
- A **sample GitHub repo** with **Issues** enabled (the Module 1 sample repo is fine).
- The provided **lab materials** (your facilitator will point you to them):
  - `Lab_Materials/Module2_Lab/notes/` — the **messy notes** for each track.
  - `Lab_Materials/Module2_Lab/epic-account-self-service.md` — the **epic** to break down.
  - `Lab_Materials/Module2_Lab/mockup-reset-password.png` — a **wireframe** to draft an issue from.
  - `Lab_Materials/Module2_Lab/requirements-space/` — the docs behind the **"Product Requirements" Space** (`glossary.md`, `personas.md`, `nfr-standards.md`, `definition-of-done.md`, `SPACE-instructions.md`).

**Pairing & tracks:** pick your track — **Web/Drupal, Data & Analytics, Power BI, QA, or RPA** (see *Role-track variations* at the end). If you don't write code day-to-day, pair with a developer. Everyone completes each core exercise.

---

## Exercise 0 · Open your materials  (5 min)

**Goal:** get set up and choose your track.

**Steps**

1. Open **Copilot Chat** in VS Code and switch it to **Agent mode**.
2. Open the **messy notes** for your track from `Lab_Materials/Module2_Lab/notes/` (e.g. `web-drupal-notes.md`).
3. Open the **Issues view** in VS Code (the GitHub icon in the Activity Bar, from the GitHub Pull Requests and Issues extension), pointed at your sample repo.
4. Open the grounding docs so you can attach them later: `glossary.md`, `personas.md` and `nfr-standards.md` from `requirements-space/`. *(These are the docs behind the github.com "Product Requirements" Space; in VS Code you ground by attaching them to Chat.)*

**What you should see:** Copilot Chat in Agent mode, your notes, the repo's Issues view, and the grounding docs all open in VS Code.

> **✅ Checkpoint:** You have your track's notes and can reach the Space (or its grounding docs).

---

## Exercise 1 · Notes → structured requirements  (12 min)

**Goal:** turn messy, contradictory input into a structured, de-duplicated list — and catch what the AI gets wrong.

**Steps**

1. Paste your track's notes into Copilot Chat with the prompt below.
2. **Read the output critically.** Mark anything **invented** (not in the notes) or **dropped** (in the notes but missing). This is the *invented scope* failure mode — catch it here.
3. Turn 2–3 flagged ambiguities into **clarifying questions** for stakeholders (you'll validate these, not guess them).

**Paste this prompt:**

> Extract the discrete requirements from these notes. For each one give:
> a clear statement, the stakeholder need behind it, and any ambiguity or open question.
> Flag duplicates and conflicts, and group by theme.
> Only use what is in the notes — list any assumptions separately.
> `<paste your notes>`

**What you should see:** a themed requirement list with the "why" kept, explicit open questions, and flagged conflicts (e.g. *"reset link should never expire"* vs the security rule; *"active user"* defined two different ways).

> **✅ Checkpoint:** You verified nothing was invented or silently dropped, and you captured real open questions to take back to stakeholders.

---

## Exercise 2 · A user story with testable criteria  (15 min)

**Goal:** write one story that QA — or a Copilot agent — could build and verify.

**Steps**

1. Pick **one** requirement. Ask Copilot for a **user story** (*As a … I want … so that …*) plus **Given/When/Then** acceptance criteria.
2. Ask specifically for **edge cases, negative paths, and one non-functional criterion** (pull it from `nfr-standards.md`).
3. **Kill the vagueness.** Replace every fuzzy term or guessed number with a real value from the glossary/NFR docs, or mark it **`TBC with stakeholder`**. (Unconfirmed numbers are the *false precision* failure mode — don't ship a guess as fact.)
4. Append your team's **definition of done** from `requirements-space/definition-of-done.md`.

**Paste this prompt:**

> Write a user story for `<requirement>`, then its acceptance criteria as Given/When/Then.
> Add edge cases, negative paths, and one non-functional criterion.
> Keep every criterion objectively testable — a tester must be able to pass or fail it.

**What you should see:** one story with complete, testable criteria — for a password reset, e.g. *"Given a valid account email, When I request a reset link, Then a single-use link is emailed within 1 minute and expires after 30 minutes."*

> **✅ Checkpoint:** Every criterion is objectively testable — no "fast", no "user-friendly" — and each guessed number is either sourced or marked `TBC`.

---

## Exercise 3 · Create a GitHub Issue  (10 min)

**Goal:** move the requirement to where the work actually happens.

**Steps**

1. In Copilot Chat **Agent mode**, ask Copilot to create the issue directly in your repo (this uses the GitHub tools / MCP server):
   > In `owner/repo`, create an issue for `<your story>`. Use the acceptance criteria we just wrote as the body, and add labels `auth` and `ux`. **Show me the draft first and create it only after I confirm.**

   **No GitHub tools in Agent mode?** Do it draft-and-paste, still entirely in VS Code: ask Copilot in Chat to *"draft the full issue — title, body with the acceptance criteria, and labels"*, then run **Command Palette → GitHub Issues: Create Issue**, paste Copilot's body, and submit.
2. Copilot drafts a **title, body, labels and metadata** (mapping to your repo's issue templates if it has them). **Review and edit every field** — you own the final wording — then create (confirm the agent's action, or submit the extension form).
3. **Draft an issue from an image.** Start a new Chat prompt and **drag `mockup-reset-password.png` into the chat** (VS Code Copilot Chat accepts image attachments), then add: *"Create an issue from this wireframe for the password-reset screen."* Review and create as in step 1.

**What you should see:** one or two well-formed, self-contained issues in your repo, each carrying its acceptance criteria.

> **✅ Checkpoint:** The issue is **build-ready** — a developer, or the Copilot cloud agent (Module 1), could pick it up with no extra context.

---

## Exercise 4 · Break the epic into sub-issues  (12 min)

**Goal:** decompose a larger requirement into independently shippable pieces.

**Steps**

1. Open `epic-account-self-service.md`. Ask Copilot to break it down:
   > Break this epic into sub-issues, each independently shippable, each with its own acceptance criteria. Note dependencies and a sensible sequence.
   > `<paste the epic>`
2. Require: **each sub-issue has its own acceptance criteria**, and **dependencies are explicit** (e.g. *"change email" needs verified identity from the reset flow*).
3. **Review the cut** — does the sequence deliver value in the right order? Reshape it if not; the AI proposes, you confirm it matches reality.
4. Create them as **native sub-issues without leaving VS Code**:
   - **Agent mode:** ask Copilot to create each one under the parent, e.g. *"Create these as sub-issues of #`<n>` in `owner/repo`, each with its own body and acceptance criteria."* (the GitHub tools support parent/sub-issue links), **or**
   - **Integrated terminal** (part of VS Code): `gh issue create --parent <n> ...` for each.

   A parent can hold up to 100 sub-issues. If native sub-issues aren't enabled, track the breakdown as a task list in the epic body.

**What you should see:** a parent issue with right-sized sub-issues, dependencies noted, and progress tracked on the parent.

> **✅ Checkpoint:** Each sub-issue is independently testable, and the order of work makes sense.

---

## Exercise 5 · Ground it in a Space & compare  (8 min)

**Goal:** see, concretely, the difference real context makes.

**Steps**

1. Re-run your Exercise 1 (structure) or Exercise 2 (story) prompt — this time **attach `glossary.md`, `personas.md` and `nfr-standards.md` to the chat** as grounding (drag them in, or reference them with `#file`). *(On github.com the equivalent is the "Product Requirements" Space; in VS Code, the attached files are your Space.)*
2. **Compare the two drafts.** Does the grounded one use your **domain terms** (e.g. *"active user" = logged in within 30 days*), your **personas** (Riya, Sam, Dana), and the **NFR checklist** — and does it **cite the source doc**?
3. Note **one concrete improvement** grounding made that the ungrounded draft missed.

**What you should see:** a grounded draft that speaks your language and applies your standards, with citations — clearly better than the generic first attempt.

> **✅ Checkpoint:** You can point to at least one specific improvement grounding produced over the ungrounded draft.

---

## Exercise 6 · Validate, fix & trace  (8 min)

**Goal:** practise the human checkpoint and close the loop to testing. *This is the point of the whole lab.*

**Steps**

1. **Hunt a failure mode.** Find one place in your work that shows **invented scope** (a requirement nobody asked for), **false precision** (an unagreed number/SLA/date), **lost intent** (a requirement with no "why"), or **rubber-stamping** (something you'd have accepted unread). Fix it, and note **who would confirm it**.
2. Ask Copilot to close the loop to testing:
   > For this story, list the tests each acceptance criterion implies. Then tell me which criteria are **not yet** covered by a test.
3. Add a short note linking the requirement to those test ideas, so the thread is complete.

**What you should see:** a validated, corrected requirement with test ideas attached, and a named failure mode you personally caught.

> **✅ Checkpoint:** You can trace the whole thread out loud: **need → story → issue → criteria → test** — and you fixed at least one real problem.

---

## Wrap-up  (5 min)

Talk it over with the person next to you:

- Which technique from today will you adopt **first** on real work?
- Which failure mode (**invented scope, false precision, lost intent, rubber-stamping**) is the biggest risk on your team — and how would you enforce a guard against it?
- Where in *need → story → issue → criteria → test* does your team most often break the thread?

---

## Role-track variations

Everyone follows the same six exercises; only your **input** and **focus** change.

| Track | Your input | Focus |
|---|---|---|
| **Web / Drupal** | `web-drupal-notes.md` | Feature request → issue with criteria; scope a module; note migration & compatibility needs. |
| **Data & Analytics** | `data-analytics-notes.md` | Define the metric precisely: source, grain, refresh, and data-quality acceptance criteria. |
| **Power BI** | `power-bi-notes.md` | Spec a report/dashboard: measures, filters, row-level security roles, and what "correct" means. |
| **QA** | `qa-notes.md` | Turn the feature into a testable checklist: happy path, edge cases, negative paths, regression. |
| **RPA** | `rpa-notes.md` | Spec the process: steps, exceptions, inputs/outputs, the human-approval rule, and the success condition. |

---

## Your deliverables checklist

1. ☐ Structured requirement list + clarifying questions *(Ex 1)*.
2. ☐ One user story with testable Given/When/Then criteria + definition of done *(Ex 2)*.
3. ☐ A build-ready GitHub Issue (bonus: a second issue drafted from the wireframe) *(Ex 3)*.
4. ☐ An epic broken into native sub-issues with dependencies *(Ex 4)*.
5. ☐ A grounded draft + a one-line note on what grounding improved *(Ex 5)*.
6. ☐ One validated/fixed criterion with linked test ideas, and a named failure mode you caught *(Ex 6)*.

---

## Stretch goals

- **Prioritise:** ask Copilot for a first-pass **MoSCoW** or **RICE** ranking of your requirement list — then correct it with your own judgement (Copilot has no access to your strategy, budget or politics).
- **Estimate — carefully:** ask for t-shirt sizes to *react to*, then note why you wouldn't commit a date on an AI number alone.
- **Spec-driven flow:** turn your requirement into a short spec with a toolkit like **Spec Kit** (`/specify` → `/plan` → `/tasks`) and review the spec *before* any code is written.
- **Delegate:** assign one well-scoped sub-issue to the **Copilot cloud agent** (Module 1) and review its draft PR — the payoff of writing a clear, testable issue.
- **Stakeholder summary:** ask Copilot to turn your technical backlog into a plain-language summary for sign-off.

---

## Troubleshooting

- **Output feels generic:** you're probably not grounded — use the Space, or attach `glossary.md` / `personas.md` / `nfr-standards.md`.
- **Copilot invented requirements:** add *"only use what is in the notes; list any assumptions separately"* and re-run.
- **Criteria are vague:** ask *"make each criterion objectively testable, with a specific threshold or value."*
- **Copilot can't create the issue from Agent mode:** the GitHub tools/MCP server probably aren't enabled — use the draft-and-paste fallback (Ex 3): let Copilot draft the body, then **GitHub Issues: Create Issue** from the Command Palette and paste it. Still 100% in VS Code.
- **`@github` / GitHub tools missing in Agent mode:** confirm you're signed in to GitHub in VS Code and the GitHub Pull Requests and Issues extension is installed; for direct issue creation, add the GitHub MCP server to Agent mode.
- **No "Create sub-issue" button:** confirm sub-issues are enabled for your repo, or track the breakdown as a task list in the epic body for now.

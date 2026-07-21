# Lab 1 · GitHub Copilot Platform Familiarization

**Participant handout · Module 1 · Level 300 · Applied AI Across the SDLC · Novnex**

**Time:** ~75 minutes (core exercises 0–6 ≈ 60 min; Exercise 7 and the stretch goals are optional)

---

## Before you start

**What you'll do:** get hands-on with Copilot across its surfaces — VS Code (completions, chat, agent mode), the Copilot CLI, and github.com (cloud agent, code review, security) — and practise the two habits that make it safe to use: **grounding the context** so answers are accurate, and **reviewing critically** so you catch what the AI gets wrong.

**The through-line — one change, end to end.** These aren't seven random tasks. Together they walk the same journey from the lecture, with a human in the loop at every decision:

> **Plan → Delegate → Review → Secure → Ship**

**By the end you'll be able to:**

- Tell generative from agentic AI by *using* both, and explain why output is a draft to verify.
- Move between Copilot's surfaces (editor, terminal, cloud) and pick the right model.
- Ground Copilot in the right context so it answers like it knows your code.
- Spot a hallucination, an insecure suggestion, and code you can't explain — and reject them.

**How to read this handout:** each exercise has a **Goal**, numbered **Steps**, **What you should see**, and a **Checkpoint** to confirm before moving on. Anything you should **type or paste is shown in a grey box** — copy it exactly, then edit to taste. Do the steps yourself — don't just read them.

**You'll need:**

- A GitHub account with a Copilot licence, signed in to VS Code (Accounts menu, bottom-left).
- VS Code with the **GitHub Copilot** and **GitHub Copilot Chat** extensions.
- The provided **sample repository** cloned locally *and* open on github.com (with Issues enabled).
- Optional: the **Copilot CLI** (`copilot`) for Exercise 4.

**Pairing & access:** if you don't write code day-to-day, pair with a developer — everyone should get hands on keyboard. Some surfaces (the cloud agent, Advanced Security) depend on your org's settings. If one isn't available to you, **ask your facilitator** to show it and follow along.

---

## Set up your workspace (do this once, before Exercise 0)

**1. Open the correct folder.** In VS Code choose **File → Open Folder…** and open the **`sample-repo`** folder:

```
Lab_Materials/Module1_Lab/sample-repo
```

> ⚠️ **Open `sample-repo`, not its parent.** Every file path in this handout (for example `src/calculations.py`) is written **relative to `sample-repo`**. If you open the wrong folder those paths won't match and file-attaching in chat will point at the wrong file.

**2. Confirm the layout.** In the VS Code **Explorer** (left sidebar) you should see:

```
sample-repo/
├─ src/
│  ├─ calculations.py      ← used in Ex 2, 3
│  └─ user_lookup.py       ← used in Ex 7 (security)
├─ tests/
│  └─ test_calculations.py ← the starter test file
├─ requirements.txt
└─ README.md
```

**3. Install dependencies and confirm the tests run.** Open a terminal in VS Code (**Terminal → New Terminal**) and run:

```
pip install -r requirements.txt
python -m pytest -q
```

You should see the tests pass. If they do, your workspace is ready.

**Reference — how to attach context / a file in Copilot Chat** (you'll do this constantly):

- Type **`#`** in the chat box, then start typing a filename (e.g. `#calculations.py`) and pick it from the dropdown, **or**
- Click the **paperclip / "Add Context…"** button above the chat box and choose the file, **or**
- **Drag a file** from the Explorer straight into the chat box.
- Special tokens: **`#codebase`** = the whole workspace · **`#selection`** = the code you've highlighted · **`#file`** = pick a file.

---

## Exercise 0 · Verify your setup — and find the model picker  (5 min)

**Goal:** confirm Copilot is live, and notice *which model* is answering you.

**Steps**

1. Make sure the `sample-repo` folder is open (see setup above).
2. Look at the **Copilot icon in the Status Bar** (bottom of the window). It should show active with no error/warning. If prompted, sign in to GitHub.
3. Create a new file called **`scratch.py`** (**File → New File**, or right-click in the Explorer → *New File*). Type the comment below, press **Enter** to move to a new line, and wait for grey *ghost-text* to appear:

   ```
   # add two numbers and return the result
   ```

4. Open **Copilot Chat** (the chat icon in the title bar, or `Ctrl+Alt+I` / `⌃⌘I`). Type this and press Enter:

   ```
   what can you do?
   ```

   Confirm it replies.
5. At the bottom of the chat box, open the **model picker** dropdown and note which model is selected (you'll see options such as *Auto* plus specific GPT / Claude / Gemini models). You'll use this again later.
6. *Optional:* in the terminal, run `copilot --version` to confirm the CLI. Skip if it isn't installed.

**What you should see:** inline ghost-text under your comment, a Chat reply, and the model dropdown.

> **✅ Checkpoint:** You see ghost-text and a Chat reply, and you can point to the model picker. If not, tell your facilitator before continuing.

---

## Exercise 1 · Completions & Chat — generative AI up close  (10 min)

**Goal:** get fluent with the two everyday modes (*you drive* / *you direct*), and see for yourself that the output is a draft, not a fact.

**Steps**

1. Create a new file called **`utils.py`** in the repo root. Type the comment below, press **Enter**, and wait for the grey ghost-text completion. Press **Tab** to accept it. This is **generative AI** — it predicts the next tokens from your context.

   ```
   # Return the factorial of a non-negative integer n. Raise ValueError if n is negative.
   ```

2. Trigger alternative suggestions and cycle them with **Alt+]** / **Alt+[** (**⌥]** / **⌥[** on Mac); pick the best.
3. **See non-determinism:** delete the function body (keep the comment) and regenerate it two or three times — retype the comment, or in Chat ask `write the factorial function again`. Notice the result can differ run to run — that's why you treat output as a draft to verify, never a looked-up fact.
4. Select the whole function with your mouse, open Copilot Chat, and type:

   ```
   /explain
   ```

   Read the explanation.
5. With the function still selected, generate tests:

   ```
   /tests
   ```

   Skim them for correctness. (Save them as `test_utils.py` if you want to run them.)
6. Ask Chat, with the function still selected:

   ```
   what edge cases am I missing for this function?
   ```

   Note one edge case you'd add (e.g. very large `n`, non-integer input).

**What you should see:** a `factorial` function, generated tests, and an explanation — all reviewed by you — plus visible run-to-run variation.

> **✅ Checkpoint:** You accepted, explained and tested a function, saw the output change between runs, and can name one thing you'd change.

---

## Exercise 2 · Ground the context — "context is the product"  (12 min)

**Goal:** prove to yourself that the same question gets a better answer when Copilot can see the right context. This is the single most useful habit in the whole course.

**Steps**

1. **Ask with nothing attached.** Open a **new chat** (the `+` icon), attach *no* file, and type exactly:

   ```
   What does the apply_discount function do, and what inputs would break it?
   ```

   Notice how vague or hedged the answer is — Copilot is guessing, because it can't see the code.

2. **Now give it the context.** In the same chat box, type **`#`**, then `calculations.py`, and select **`src/calculations.py`** from the dropdown (or drag that file into the chat). Then ask the **same question again**:

   ```
   #src/calculations.py What does the apply_discount function do, and what inputs would break it?
   ```

   Compare the answers — the grounded one should quote the real code (it will mention `percent_off` must be 0–100). For a whole-workspace question you'd use **`#codebase`** instead of a single file.

3. **Set a standing instruction.** Create a new file at exactly this path (create the `.github` folder if it doesn't exist):

   ```
   .github/copilot-instructions.md
   ```

   Paste these house rules into it and save:

   ```markdown
   - Always validate input and raise a clear `ValueError` on bad input.
   - Write a matching pytest test for every function you add.
   ```

   VS Code auto-applies this file to **every** chat request in this workspace — you don't attach it manually.

   *Shortcut: you can type `/init` in Chat to have Copilot generate this file for you, then edit it down to the two rules above.*

4. **See it take effect.** Open a **fresh chat** and type:

   ```
   Add a function to src/calculations.py that returns the median of a list of numbers.
   ```

   Notice it now **validates input and offers a matching test without being asked** — your instruction is part of the context on every request.

5. **Team-scale grounding (discuss, or do if available):** on github.com, a **Copilot Space** bundles repos + docs + instructions so your whole team gets grounded answers. Name one Space your team would create (e.g. *"our coding standards + the service README"*). If you have access, create one and ask it a question.

**What you should see:** a noticeably better, code-quoting answer once context is attached, and a `copilot-instructions.md` that shapes every future suggestion.

> **✅ Checkpoint:** You can show the difference between an ungrounded and a grounded answer, and you have a `.github/copilot-instructions.md` in the repo.

---

## Exercise 3 · Agent mode — delegate a change and watch the loop  (12 min)

**Goal:** delegate a small, scoped change and see agentic AI run the **Plan → Act → Observe** loop.

**Steps**

1. In Copilot Chat, open the **mode dropdown** at the bottom of the chat box (it usually says *Ask*) and switch it to **Agent**.
2. Paste the goal below into the chat box and send it. Watch Copilot **plan**, then **act** (edit across files), then **observe** (run the tests and read the result).

   ```
   Add an input-validation helper to src/calculations.py and use it in the existing functions so they raise a clear ValueError on bad input. Add tests for the helper in tests/test_calculations.py. Run the tests and fix any failures.
   ```

3. When it asks to **run a command** (e.g. `python -m pytest`), read the command and click **Continue / Allow** deliberately — this approval is a guardrail, not a formality.
4. If a test fails, watch it **read the error and try again** (the self-heal step).
5. Read the proposed **diff before accepting** (**Keep** / **Undo** per file). Reject or refine anything you can't explain.
6. As it runs, name the loop out loud: **Goal → Plan → Act → Observe → Repeat.**

**What you should see:** a reviewed multi-file change with passing tests, and you can point to where each step of the loop happened.

> **✅ Checkpoint:** You can describe what changed and why, you approved the test run consciously, and you reviewed before accepting.

---

## Exercise 4 · Copilot CLI — an agent in the terminal  (8 min)

**Goal:** use the same agent from the shell. *(No CLI installed? Do the stretch goal in Chat instead — see the note at the end of the steps.)*

**Steps**

1. In the VS Code terminal, make sure you're in the repo folder, then start the agent:

   ```
   copilot
   ```

2. Press **Shift+Tab** to enter **Plan mode** (or type **`/plan`**). Give it this task and review the plan **before** it acts:

   ```
   add a short README section documenting the functions in utils.py
   ```

3. Let it execute; review the changes it makes. *(Press Shift+Tab again to reach **Autopilot** mode if you want it to proceed without step-by-step approval — use with care.)*
4. Type **`/model`** to see and switch models, and **`/`** on its own to list every command (**`/help`** for help).
5. Notice it uses the **same tools and models** as the IDE — one agent, another surface.

**Example session:**

```
$ copilot
> add a short README section documenting the functions in utils.py
> /model
```

> **No CLI? Stretch alternative:** back in Copilot Chat (Agent mode), send the same request —
> `add a short README section documenting the functions in utils.py` — and review the diff. Same task, different surface.

**What you should see:** a change made and reviewed entirely from the terminal (or Chat, if you did the alternative).

> **✅ Checkpoint:** You ran an agent task from the CLI, reviewed the plan, and reviewed the result.

---

## Exercise 5 · Delegate to the cloud agent — async + guardrails  (12 min)

**Goal:** experience asynchronous delegation and the built-in guardrails. *(No cloud agent in your org? Ask your facilitator to run it and read the session log together.)*

**Steps**

1. On **github.com**, open the sample repo's **Issues** tab and create a new issue. Use the prepared text from **`Lab_Materials/Module1_Lab/ISSUE-assign-to-copilot.md`** — copy its **Title** and **Body** into the new issue. *This is the "Plan" step.*
2. On the issue, open **Assignees** (right sidebar) and assign **Copilot**. *This is "Delegate."* Copilot adds a 👀 reaction and starts a session (powered by GitHub Actions).
   - *Alternatives you can note:* the repo's **Agents** tab, or mentioning **`@copilot`** in a pull-request comment.
3. Wait a moment and watch it open a **draft pull request**. Open the PR.
4. Read the **session log**: plan → edits → test runs. It's the same loop as Exercise 3, running in the cloud.
5. Note the guardrails and *why* each exists:
   - it only pushes to a **`copilot/*`** branch;
   - your branch protections and rulesets still apply;
   - **CI on its PR needs a human to approve the run**;
   - it **cannot approve or merge its own PR**;
   - **the person who assigned it can't approve it either** — an *independent* human always reviews.
6. Leave a review comment on the PR requesting one change, for example:

   ```
   @copilot please also add a test for a list containing negative numbers.
   ```

   Watch it revise the PR.

**What you should see:** a draft PR authored by the agent, with your review comment, and a visible session log.

> **✅ Checkpoint:** You delegated a task and can explain at least two guardrails — including why the assigner can't self-approve.

---

## Exercise 6 · Review critically — catch what the AI gets wrong  (10 min)

**Goal:** use automated review, then practise the skill that matters most — catching a failure mode *before* it ships.

**Steps**

1. On an open PR (the agent's from Ex 5, or one you push), go to **Reviewers** in the right sidebar and, next to **Copilot**, click **Request**. *(From the terminal: `gh pr edit --add-reviewer @copilot`.)* The review usually takes under a minute. *This is the "Review" step.*
2. Read its comments and **severity labels** (High / Medium / Low). Apply one good suggestion with the one-click **Commit suggestion** button.
3. **Now hunt for a failure mode.** Pick **one** of the three below, run the exact prompt, inspect the result, then reply on the PR (or tell your partner) which failure mode you found:

   - **Hallucination** — in Copilot Chat, ask it to use a library that doesn't exist in this repo:

     ```
     Rewrite average() in src/calculations.py to use the fastmath.mean() helper from our fastmath library.
     ```

     There is no `fastmath` library here — confirm Copilot invents a plausible-but-wrong `import`/API. Verify against the real code (there's no such dependency in `requirements.txt`).

   - **Insecure code** — ask it to "quickly" add a feature and check whether it reproduces an unsafe pattern:

     ```
     Quickly add a function to src/user_lookup.py that finds a user by email address. Keep it short.
     ```

     Check whether it builds the SQL query by string concatenation (the unsafe pattern) instead of a parameterized query.

   - **Over-trust** — find one suggested line anywhere in the lab that you **cannot fully explain**, and reject it on those grounds alone.

4. Confirm a human still has to approve the merge: a Copilot review is always left as a **"Comment"**, so it **does not** count as an approval and won't satisfy a required-reviewer rule.

**What you should see:** a PR with a Copilot review — one suggestion accepted, one rejected — and a documented failure mode you personally caught.

> **✅ Checkpoint:** You can point to exactly where **you** — not Copilot — made the decision, and you named a real failure mode you found.

---

## Exercise 7 · Security pass — find and fix an insecure pattern  (8 min · optional)

**Goal:** do the "Secure" step of the journey — turn a real vulnerability into a safe, tested fix.

**Steps**

1. Open **`src/user_lookup.py`**. In Copilot Chat, attach that file (`#user_lookup.py`) and ask:

   ```
   #src/user_lookup.py Is there a security problem in find_user_by_name? Show me an input that exploits it.
   ```

   It should identify the **SQL-injection** risk (the query is built by string concatenation) and give an exploit such as `' OR '1'='1`.
2. Switch Chat to **Agent** mode and ask it to fix it:

   ```
   Fix find_user_by_name in src/user_lookup.py to use a parameterized query. Add a test proving that the input ' OR '1'='1 no longer returns every row.
   ```

3. Review the diff: the fix should pass the value as a **bound parameter** (e.g. `WHERE name = ?` with `[name]`), **not** concatenate it into the string.
4. **If your repo has Advanced Security / code scanning enabled:** push the original file, open the **code-scanning alert**, and use **Copilot Autofix** to generate the suggested fix on the PR. Compare it with your hand fix. *(If it isn't enabled, the manual fix teaches the same lesson.)*
5. Discuss: **secret scanning** is the sibling capability — it flags credentials that shouldn't be committed. Where would that have saved your team time?

**What you should see:** a parameterized, tested version of `find_user_by_name` — fixed by you, the agent, or Autofix.

> **✅ Checkpoint:** The concatenated query is gone, the exploit input no longer dumps the table, and a test proves it.

---

## Wrap-up  (5 min)

You just walked one change end to end — the same arc from the lecture:

> **Plan** (Ex 5) → **Delegate** (Ex 3–5) → **Review** (Ex 6) → **Secure** (Ex 7) → **Ship** (a human approves & merges).

Talk it over with the person next to you:

- Which surface (completions, chat, agent mode, CLI, cloud agent) would change your week the most, and why?
- Where in that arc is the human **most** essential — and what would need to be true (guardrails, data boundaries, model choice) for you to trust delegating the rest?
- Write down **one task from your real work** you'll try with Copilot tomorrow.

---

## Your deliverables checklist

1. ☐ A reviewed `factorial` function with generated tests, seen to vary between runs *(Ex 1)*.
2. ☐ A grounded (code-quoting) answer plus a `.github/copilot-instructions.md` *(Ex 2)*.
3. ☐ A reviewed multi-file change from agent mode, with the loop named *(Ex 3)*.
4. ☐ A change made from the CLI, or the stretch alternative *(Ex 4)*.
5. ☐ A draft PR from the cloud agent with your review comment *(Ex 5)*.
6. ☐ A PR with a Copilot review — one accepted, one rejected — and a failure mode you caught *(Ex 6)*.
7. ☐ *Optional:* a parameterized, tested fix for `find_user_by_name` *(Ex 7)*.

---

## Stretch goals

- **Model choice, A/B:** run the *same* prompt on two different models (model picker) and note the difference in quality or style.
- **Context, deeper:** attach a doc, or use `@workspace` / `#codebase`, and compare answer quality with and without it.
- **Spaces:** create a Copilot Space on github.com bundling the repo + a standards doc, and ask it a question only the docs could answer.
- **Docs:** ask Copilot to add documentation (`/doc`) and a short CONTRIBUTING note.
- **Design preview:** GitHub Spark turns a prompt into a running app — the design-and-prototyping deep dive comes in Module 3.

---

## Troubleshooting

- **No suggestions:** check the Copilot Status Bar icon and your sign-in; confirm the file type is supported.
- **Wrong file gets attached / paths don't match:** you probably opened the parent folder — reopen **`sample-repo`** itself (see *Set up your workspace*).
- **Agent mode missing:** update VS Code and the Copilot Chat extension, then pick **Agent** in the Chat mode dropdown.
- **Instructions ignored:** confirm the file is at `.github/copilot-instructions.md` in the `sample-repo` folder you have open, then start a fresh chat.
- **Cloud agent unavailable:** it must be enabled by your org admin — ask your facilitator to demo it.
- **Autofix unavailable (Ex 7):** this needs GitHub Advanced Security; if it's off, do the fix by hand — the learning is the same.
- **Network blocked:** confirm the Copilot / GitHub allow-list from the Lab Setup document.

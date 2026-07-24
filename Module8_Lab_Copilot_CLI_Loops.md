# Lab 8 · The SDLC in Your Terminal — GitHub Copilot CLI, BYOK & Unattended Loops

**Participant handout · Module 8 · Level 300 · Automation & Agentic Workflows · Novnex**  ·  **Time:** ~90 min

---

## Before you start

Every lab so far put Copilot inside the editor. Today you take it **out of the IDE and into the terminal**,
give it **your own model (BYOK)**, wire up **one agent per SDLC role**, and then let those agents run
**unattended** — including full-autonomy **YOLO mode** — with the guardrails that make that safe.

**The thread:** `Install → BYOK → Drive interactively → Script it → One agent per role → Loop the lifecycle → Run unattended`

**The rule:** the terminal removes the friction that was quietly keeping you honest. An agent that never
pauses can do a lot of good work — or a lot of damage — before you look. **Autonomy is earned with scope,
sandboxing, and a stopping condition, never granted by default.**

> **New to the week?** You don't need the earlier labs. This one stands alone: the sample app and all agent
> profiles are provided in `Lab_Materials/Module8_Lab/`.

**Setup**
- **Windows 11**, **PowerShell 6+** (`$PSVersionTable.PSVersion` ≥ 6). The new `copilot` CLI needs pwsh 6+.
- An **active GitHub Copilot subscription** for auth — *or* a **BYOK provider** (we use Azure OpenAI, which
  replaces GitHub model routing entirely).
- **Git**, and **Python 3.10+** for the sample app.
- **We install without Node.js** — via **WinGet** or the **standalone binary**. (npm needs Node 22+; we skip it.)
- Materials in `Lab_Materials/Module8_Lab/`: `agents/` (six SDLC-role `.agent.md` profiles), `scripts/`
  (`setup-byok.ps1`, `role-loop.ps1`, `unattended-run.ps1`), `sample-app/`, and `AGENTS.md`.

**Pick your seat at the table** — you'll drive the whole lifecycle, but lead from one role:

| Role | Agent profile | Owns the step |
| --- | --- | --- |
| Business Analyst | `requirements-analyst.agent.md` | Requirements → acceptance criteria |
| Architect | `solution-architect.agent.md` | Design → ADR + interface |
| Developer | `developer.agent.md` | Implement to the criteria |
| QA / Tester | `qa-tester.agent.md` | Tests + coverage gate |
| DevOps | `release-engineer.agent.md` | CI/CD + release notes |
| SRE / Support | `sre-maintainer.agent.md` | Triage + fix-forward |

> **⚠ Secrets:** the BYOK key is a **live credential**. Never commit it, never paste it into a prompt, never
> print it to a shared screen. The scripts read it from an env var you set locally; the repo only ever holds a
> placeholder. Treat a leaked key as a rotate-now incident.

---

## Exercise 0 · Install Copilot CLI on Windows — no Node  (10 min)

**Goal:** a working `copilot` binary installed without touching npm/Node.

1. Check your shell — you need PowerShell 6+:
   ```powershell
   $PSVersionTable.PSVersion    # Major must be >= 6  (winget install Microsoft.PowerShell if not)
   ```
2. **Install — pick one (both are Node-free):**

   **A · WinGet (recommended):**
   ```powershell
   winget install GitHub.Copilot
   # prerelease channel:  winget install GitHub.Copilot.Prerelease
   ```

   **B · Standalone binary (locked-down / no WinGet):** download the Windows `x64` archive from the
   [copilot-cli releases](https://github.com/github/copilot-cli/releases), unzip to a folder such as
   `C:\Tools\copilot\`, then add it to `PATH` for this session:
   ```powershell
   $env:Path = "C:\Tools\copilot;$env:Path"
   ```
3. Verify — open a **new** terminal so `PATH` refreshes:
   ```powershell
   copilot --version
   copilot --help        # skim the flags; you'll use -p, --allow-tool, --yolo later
   ```

> **✅** `copilot --version` prints a version, and you installed it **without Node.js**.

---

## Exercise 1 · Bring Your Own Key — Azure OpenAI  (12 min)

**Goal:** point Copilot CLI at **your** model instead of GitHub-hosted routing.

**How BYOK works:** set four `COPILOT_PROVIDER_*` / `COPILOT_MODEL` environment variables *before* launching.
When they're present, Copilot CLI sends **all model requests to your provider** regardless of GitHub auth.
Your model **must support tool calling and streaming** (128k+ context recommended) or the CLI errors out.

1. Set the variables for this session. Use the provided script so the key never lands in the repo — it reads
   the key from a local env var you set once:
   ```powershell
   $env:COPILOT_PROVIDER_API_KEY = "<PASTE-YOUR-AZURE-KEY-HERE>"   # local only, never committed
   .\Lab_Materials\Module8_Lab\scripts\setup-byok.ps1
   ```
   The script sets the non-secret trio for you:
   ```powershell
   $env:COPILOT_PROVIDER_BASE_URL = "https://bujo-resource.openai.azure.com/openai/deployments/gpt-5.4"
   $env:COPILOT_PROVIDER_TYPE     = "azure"
   $env:COPILOT_MODEL             = "gpt-5.4"
   # COPILOT_PROVIDER_API_KEY must already be set in your session (see above)
   ```
   > For Azure, `COPILOT_BASE_URL` ends at `/deployments/<deployment-name>` and `COPILOT_MODEL` **is** the
   > deployment name. For plain OpenAI you'd use `https://api.openai.com/v1`; for Ollama, `http://localhost:11434`.
2. Authenticate the CLI itself (separate from model routing) — launch and run `/login` once:
   ```powershell
   copilot
   ```
   ```text
   /login          # device-code GitHub auth (skips if a BYOK key is already handling models)
   /model          # confirm the active model is your Azure deployment, not a GitHub default
   ```
3. Sanity-check the model actually answers:
   ```text
   In one line, tell me which model and provider you are running on.
   ```

> **✅** `/model` shows **your** Azure deployment, and a prompt gets a real answer. If it errors on tool
> calling or streaming, your deployment doesn't support them — pick a model that does.

---

## Exercise 2 · Drive it interactively  (8 min)

**Goal:** get fluent with the session before you automate it.

1. From the repo root, start a session scoped to the sample app:
   ```powershell
   copilot --add-dir ".\Lab_Materials\Module8_Lab\sample-app"
   ```
2. Ask it to get oriented, then make one small, reviewable change:
   ```text
   Read sample-app/. Summarise what it does and list the failing tests. Don't change anything yet.
   ```
   Then: `Implement the smallest fix to make one failing test pass. Show me the diff before writing.`
3. Learn the controls you'll rely on when it's unattended: watch how it **asks permission** before each
   shell/write, and note the slash commands (`/model`, `/agent`, `/help`, `/clear`).

> **✅** You made one change through the CLI and saw exactly where it pauses for approval — that pause is the
> thing you'll be removing later, so understand it now.

---

## Exercise 3 · Script it — non-interactive mode  (10 min)

**Goal:** turn a session into a one-shot command you can put in a loop.

The `-p` flag runs a single prompt and exits — this is the atom of every automation:

1. Run one headless task:
   ```powershell
   copilot -p "List the functions in sample-app/src and the acceptance tests each still fails." -s
   ```
   `-s` suppresses stats/decoration so you get just the answer — ideal for piping.
2. Feed it from a variable or file (great for CI):
   ```powershell
   $task = Get-Content ".\Lab_Materials\Module8_Lab\sample-app\TASK.md" -Raw
   copilot -p $task -s --add-dir ".\Lab_Materials\Module8_Lab\sample-app"
   ```
3. Notice: in `-p` mode it still **stops at the first tool it needs permission for**. That's why the next two
   exercises exist — scoped permissions, then full autonomy.

> **✅** You ran Copilot with zero interaction and got a usable result on stdout.

---

## Exercise 4 · One agent per SDLC role  (15 min)

**Goal:** stop re-typing role context — bake each role into a reusable **custom agent**.

A custom agent is a Markdown file with YAML frontmatter (`.agent.md`) that fixes a role's **instructions,
tools, and model**. Copilot CLI reads them from `~/.copilot/agents/` (personal) or `.github/agents/` (repo);
home-dir wins on name clashes.

1. Install the six provided role agents to your user profile:
   ```powershell
   New-Item -ItemType Directory -Force "$HOME\.copilot\agents" | Out-Null
   Copy-Item ".\Lab_Materials\Module8_Lab\agents\*.agent.md" "$HOME\.copilot\agents\"
   ```
2. Open **your role's** profile and read the frontmatter — `name`, `description`, `tools` (note how
   `qa-tester` can run tests but the `requirements-analyst` can't touch the shell). Tighten one instruction to
   match how your team actually works.
3. Invoke your agent, interactively and headless:
   ```text
   /agent solution-architect          # interactive: pick it, then give it the task
   ```
   ```powershell
   copilot --agent qa-tester -p "Add the missing edge-case tests for sample-app/src and report coverage." `
     --add-dir ".\Lab_Materials\Module8_Lab\sample-app"
   ```

> **✅** Your role agent runs from a single flag, and its scope (tools + instructions) is fixed in a file you
> can review and version — not retyped each time.

---

## Exercise 5 · Loop the lifecycle  (12 min)

**Goal:** chain the role agents so one feature flows Requirements → Design → Dev → Test → Release, each step's
output feeding the next.

1. Read `scripts/role-loop.ps1` — it runs each role agent in `-p` mode in order, writing every step's output
   to `artifacts/<step>.md` so the next agent reads the last one's work. This is the SDLC as a pipeline.
2. Run it against the sample feature (still **approval-gated** — you'll confirm tools; that's deliberate for a
   first run):
   ```powershell
   .\Lab_Materials\Module8_Lab\scripts\role-loop.ps1 -Feature "Add password-strength validation"
   ```
3. Inspect `artifacts/`. Where did a handoff lose information? Which role's prompt needs tightening? Fix one
   agent profile and re-run just that step.

> **✅** A single feature idea produced criteria → design → code → tests → release notes, each traceable to the
> agent that made it.

---

## Exercise 6 · Run unattended — autonomy with a leash  (15 min)

**Goal:** remove the approval pauses **safely**, and understand exactly what you're trading away.

**The permission model (deny beats allow, always):**

| Flag | Effect |
| --- | --- |
| `--allow-tool 'shell(git:*)'` | allow just git subcommands |
| `--allow-tool 'write'` `--allow-tool 'shell(pytest)'` | let it write files & run tests, nothing else |
| `--deny-tool 'shell(rm)'` | hard block — wins even under `--yolo` |
| `--allow-all-tools` | every tool, no prompts (paths/URLs still gated) |
| `--yolo` / `--allow-all` | **everything**: all tools, paths, URLs. Full trust. |
| `--no-ask-user` | never pause to ask *you* a question mid-run |
| `--max-autopilot-continues N` | cap the autonomous steps — your **stopping condition** |

1. **Scoped autonomy first** — let the tester loop run itself, but only with the tools it needs:
   ```powershell
   copilot --agent qa-tester -p "Get sample-app tests to green. Don't edit tests to cheat." `
     --allow-tool 'write' --allow-tool 'shell(pytest)' --allow-tool 'shell(python)' `
     --deny-tool 'shell(git push)' --no-ask-user `
     --add-dir ".\Lab_Materials\Module8_Lab\sample-app"
   ```
2. **Full YOLO — in a sandbox, with a cap.** Only ever do this on a disposable copy. Use the provided wrapper,
   which runs on a throwaway git branch and bounds the steps:
   ```powershell
   .\Lab_Materials\Module8_Lab\scripts\unattended-run.ps1 `
     -Feature "Add rate limiting to the reset endpoint" -MaxContinues 10
   # internally: copilot --yolo --no-ask-user --max-autopilot-continues 10 -p "<feature>" ...
   ```
3. Watch it work end-to-end with no prompts, then **review the branch diff as a human** before it goes
   anywhere. Answer for yourself: what could this have deleted, and what stopped it? (The deny rules and the
   step cap — not luck.)

> **✅** You ran one **scoped** unattended loop and one **full-YOLO** loop in a sandbox with a hard step cap,
> and you reviewed the result before trusting it.

> **Watch out:** `--yolo` grants delete/overwrite/network with no second look, and every autonomous step
> spends credits. Never point it at a repo you can't throw away, a shell with prod credentials, or the open
> internet. Deny-list the irreversible things; cap the continues; run in a container or fresh clone.

---

## Wrap-up  (5 min)

- Which SDLC step will you hand to an unattended loop first — and which will you *never* fully automate?
- Where does BYOK help your org (data residency, model choice, cost) versus GitHub-hosted models?
- What's your team's minimum safe-autonomy recipe: which deny rules and what step cap, as a default?

**The whole lifecycle, one terminal:** the same agent loop that files requirements can ship code and triage
incidents. **The thread:** the CLI makes autonomy cheap; scope, sandboxing, and a stopping condition make it
safe. **On Monday:** wrap your real repo's most repetitive role loop in a scoped, capped `copilot -p` script —
approval-gated first, unattended only once you trust the diff.

## Deliverables
A Node-free install · BYOK pointed at your Azure deployment (verified via `/model`) · six role agents
installed · one full lifecycle loop with artifacts · one scoped and one YOLO unattended run in a sandbox, each
reviewed before trust.

## Stretch
Add a `code-reviewer` agent and insert it between Dev and Test in the loop · schedule `unattended-run.ps1` as a
nightly Task Scheduler / cron job that opens a PR · put the loop in GitHub Actions with `--allow-all` and a
deny-list · swap `COPILOT_MODEL` to a local Ollama model and compare quality/latency · add an `AGENTS.md` house
rule and confirm every agent picks it up.

## Troubleshooting
- **`copilot` not found:** open a new terminal (PATH refresh); confirm the install dir is on `PATH`.
- **PowerShell too old:** the CLI needs pwsh 6+ — `winget install Microsoft.PowerShell`.
- **`/model` shows a GitHub model, not Azure:** the `COPILOT_PROVIDER_*` vars aren't set in *this* shell —
  re-run `setup-byok.ps1` and check `$env:COPILOT_PROVIDER_API_KEY` is non-empty.
- **Error about tool calling / streaming:** your deployment lacks them — use a model that supports both.
- **Auth confusion:** BYOK handles *models*; `/login` handles *GitHub features*. You can need both.
- **It still pauses under `--yolo`:** a `--deny-tool` rule is firing (deny always wins) — that's correct, not a bug.
- **Runaway loop / burning credits:** you forgot `--max-autopilot-continues` — always set a cap for unattended runs.
- **Key leaked to a screen or commit:** rotate it in Azure immediately; treat as an incident.

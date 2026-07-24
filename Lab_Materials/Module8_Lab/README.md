# Module 8 Lab · GitHub Copilot CLI — BYOK & Unattended Loops

Supporting materials for **`Module8_Lab_Copilot_CLI.md`**. Everything here is runnable on Windows + PowerShell 6+.

## Contents

```
Module8_Lab/
├─ AGENTS.md                    # house rules every agent reads
├─ agents/                      # one custom agent per SDLC role (.agent.md)
│   ├─ requirements-analyst.agent.md
│   ├─ solution-architect.agent.md
│   ├─ developer.agent.md
│   ├─ qa-tester.agent.md
│   ├─ release-engineer.agent.md
│   └─ sre-maintainer.agent.md
├─ scripts/
│   ├─ setup-byok.ps1           # point Copilot CLI at your Azure OpenAI deployment (BYOK)
│   ├─ role-loop.ps1            # run the lifecycle as a pipeline of role agents
│   └─ unattended-run.ps1       # full-autonomy (YOLO) run, safely: throwaway branch + cap + deny-list
├─ sample-app/                  # small Python app; 2 tests pass, 4 fail — the loop's target
│   ├─ src/reset_service.py
│   ├─ tests/test_reset_service.py
│   └─ TASK.md
└─ artifacts/                   # created at runtime; one file per pipeline step (gitignored)
```

## Quick start

```powershell
# 1. Install (no Node): winget install GitHub.Copilot
# 2. BYOK — set your key locally, then configure the rest:
$env:COPILOT_PROVIDER_API_KEY = "<your-azure-key>"
.\scripts\setup-byok.ps1

# 3. Install the role agents to your user profile:
New-Item -ItemType Directory -Force "$HOME\.copilot\agents" | Out-Null
Copy-Item .\agents\*.agent.md "$HOME\.copilot\agents\"

# 4. Run the lifecycle (approval-gated first run):
.\scripts\role-loop.ps1 -Feature "Add password-strength validation"

# 5. Full autonomy in a sandbox, when you trust it:
.\scripts\unattended-run.ps1 -Feature "Add rate limiting to the reset endpoint" -MaxContinues 10
```

**Security:** the BYOK API key is a live credential. It is never stored in this repo — the scripts read it
from `$env:COPILOT_PROVIDER_API_KEY`, which you set locally. Never commit it, print it, or paste it into a
prompt. Rotate immediately if exposed.

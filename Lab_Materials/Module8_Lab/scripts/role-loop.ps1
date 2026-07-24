<#
.SYNOPSIS
  Run the SDLC as a pipeline: one Copilot CLI role-agent per phase, each reading the previous phase's output.

.DESCRIPTION
  Runs requirements -> design -> development -> testing -> release, each in non-interactive (-p) mode.
  Every step writes to artifacts/<step>.md so the next agent has the prior work as context.
  This run is APPROVAL-GATED by default (the CLI still asks before tools) — that is intentional for a first run.
  Add -Unattended to allow the agents their declared tools without prompting (still deny-listed & bounded).

.EXAMPLE
  .\role-loop.ps1 -Feature "Add password-strength validation"

.EXAMPLE
  .\role-loop.ps1 -Feature "Add rate limiting" -Unattended
#>

param(
  [Parameter(Mandatory = $true)][string]$Feature,
  [switch]$Unattended
)

$ErrorActionPreference = "Stop"

# Resolve paths relative to this script so it runs from anywhere.
$LabRoot  = Split-Path -Parent $PSScriptRoot           # ...\Module8_Lab
$AppDir   = Join-Path $LabRoot "sample-app"
$Artifacts = Join-Path $LabRoot "artifacts"
New-Item -ItemType Directory -Force $Artifacts | Out-Null

if ([string]::IsNullOrWhiteSpace($env:COPILOT_MODEL)) {
  Write-Warning "BYOK not configured — run scripts\setup-byok.ps1 first (and set COPILOT_PROVIDER_API_KEY)."
}

# Ordered pipeline: agent -> the file it produces.
$Steps = @(
  @{ Agent = "requirements-analyst"; Out = "01-requirements.md";  Task = "Feature idea: '$Feature'. Produce requirements and acceptance criteria." }
  @{ Agent = "solution-architect";   Out = "02-design.md";        Task = "Design the feature to the approved requirements. Read artifacts/01-requirements.md and the code first." }
  @{ Agent = "developer";            Out = "03-implementation.md"; Task = "Implement the design in sample-app so the acceptance criteria pass. Read artifacts/01-requirements.md and artifacts/02-design.md. Run tests." }
  @{ Agent = "qa-tester";            Out = "04-testing.md";        Task = "Verify sample-app against the acceptance criteria and add missing edge-case tests. Report a pass/fail matrix." }
  @{ Agent = "release-engineer";     Out = "05-release.md";        Task = "Confirm tests are green, then prepare release notes and a PR body on a feature branch. Do not deploy." }
)

# Unattended: let each agent use the tools it declares, but hard-block irreversible things and never ask the human.
$AutonomyFlags = @()
if ($Unattended) {
  $AutonomyFlags = @(
    "--allow-all-tools",
    "--deny-tool", "shell(git push)",
    "--deny-tool", "shell(rm)",
    "--deny-tool", "shell(Remove-Item)",
    "--no-ask-user",
    "--max-autopilot-continues", "15"
  )
  Write-Host "Running UNATTENDED (tools auto-allowed; push/delete denied; capped at 15 steps)." -ForegroundColor Yellow
} else {
  Write-Host "Running APPROVAL-GATED (you'll confirm each tool). Add -Unattended to automate." -ForegroundColor Cyan
}

foreach ($step in $Steps) {
  $outPath = Join-Path $Artifacts $step.Out
  Write-Host "`n=== [$($step.Agent)] -> artifacts/$($step.Out) ===" -ForegroundColor Green

  $prompt = @"
$($step.Task)

Write your full output to '$outPath' (overwrite it). Read any prior artifacts/*.md in that folder for context.
Feature under development: $Feature
"@

  & copilot --agent $step.Agent -p $prompt -s --add-dir $AppDir --add-dir $Artifacts @AutonomyFlags

  if (-not (Test-Path $outPath)) {
    Write-Warning "Step '$($step.Agent)' did not produce $($step.Out). Inspect and re-run this step."
  }
}

Write-Host "`nPipeline complete. Review artifacts in: $Artifacts" -ForegroundColor Cyan
Get-ChildItem $Artifacts -Filter *.md | Select-Object Name, Length, LastWriteTime | Format-Table

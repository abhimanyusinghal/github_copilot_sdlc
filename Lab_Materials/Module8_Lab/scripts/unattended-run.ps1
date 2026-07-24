<#
.SYNOPSIS
  Run Copilot CLI in full-autonomy (YOLO) mode SAFELY: on a throwaway git branch, with a hard step cap.

.DESCRIPTION
  Demonstrates --yolo (== --allow-all: all tools, paths, URLs, no prompts) the responsible way:
    * a disposable feature branch you can delete, so mistakes are contained
    * --deny-tool guards on the truly irreversible actions (deny ALWAYS beats allow, even under --yolo)
    * --max-autopilot-continues as the stopping condition, so it can't loop forever
    * --no-ask-user so it never blocks waiting for you
  YOLO trades away your per-action review. Only ever run this on a repo/branch you can throw away.

.EXAMPLE
  .\unattended-run.ps1 -Feature "Add rate limiting to the reset endpoint" -MaxContinues 10
#>

param(
  [Parameter(Mandatory = $true)][string]$Feature,
  [int]$MaxContinues = 10
)

$ErrorActionPreference = "Stop"

$LabRoot = Split-Path -Parent $PSScriptRoot
$AppDir  = Join-Path $LabRoot "sample-app"

if ([string]::IsNullOrWhiteSpace($env:COPILOT_MODEL)) {
  Write-Warning "BYOK not configured — run scripts\setup-byok.ps1 first (and set COPILOT_PROVIDER_API_KEY)."
}

# --- containment: work on a disposable branch ---
$branch = "yolo/lab8-$((Get-Date).ToString('yyyyMMdd-HHmmss'))"
Write-Host "Creating throwaway branch '$branch' — delete it when done." -ForegroundColor Yellow
git checkout -b $branch | Out-Null

Write-Host @"

============================================================
 FULL AUTONOMY (YOLO). No per-action approval.
 Contained by: throwaway branch, deny-list, step cap ($MaxContinues).
 Review the diff before trusting anything this produces.
============================================================
"@ -ForegroundColor Red

$prompt = @"
Implement this feature end to end in sample-app and get the tests green: $Feature
Follow the acceptance criteria. Do not edit tests to cheat. Commit your work on the current branch.
"@

# --yolo grants everything; deny rules below still win and cannot be overridden.
& copilot `
    --yolo `
    --no-ask-user `
    --max-autopilot-continues $MaxContinues `
    --deny-tool "shell(git push)" `
    --deny-tool "shell(rm)" `
    --deny-tool "shell(Remove-Item)" `
    --deny-tool "shell(git reset --hard)" `
    --add-dir $AppDir `
    -p $prompt

Write-Host "`nDone. Review before trusting:" -ForegroundColor Cyan
Write-Host "  git --no-pager diff master...$branch" -ForegroundColor Cyan
Write-Host "  git log --oneline master..$branch" -ForegroundColor Cyan
Write-Host "Discard everything with:  git checkout master; git branch -D $branch" -ForegroundColor Cyan

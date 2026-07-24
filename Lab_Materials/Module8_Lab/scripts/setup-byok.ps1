<#
.SYNOPSIS
  Configure GitHub Copilot CLI to use a BYOK (Bring Your Own Key) model — Azure OpenAI.

.DESCRIPTION
  Sets the non-secret COPILOT_PROVIDER_* / COPILOT_MODEL variables for the CURRENT session.
  The API key is NEVER stored in this file or the repo. Set it yourself first:

      $env:COPILOT_PROVIDER_API_KEY = "<your-azure-key>"

  ...then run this script. When these variables are present, Copilot CLI routes ALL model
  requests to your provider regardless of GitHub auth status.

.NOTES
  Model must support tool calling AND streaming (128k+ context recommended).
  For Azure: BASE_URL ends at /deployments/<deployment>, and COPILOT_MODEL == deployment name.
#>

param(
  [string]$BaseUrl = "https://bujo-resource.openai.azure.com/openai/deployments/gpt-5.4",
  [string]$ProviderType = "azure",
  [string]$Model = "gpt-5.4"
)

# --- non-secret configuration (safe to commit) ---
$env:COPILOT_PROVIDER_BASE_URL = $BaseUrl
$env:COPILOT_PROVIDER_TYPE     = $ProviderType
$env:COPILOT_MODEL             = $Model

Write-Host "BYOK provider configured for this session:" -ForegroundColor Cyan
Write-Host "  COPILOT_PROVIDER_TYPE     = $env:COPILOT_PROVIDER_TYPE"
Write-Host "  COPILOT_PROVIDER_BASE_URL = $env:COPILOT_PROVIDER_BASE_URL"
Write-Host "  COPILOT_MODEL             = $env:COPILOT_MODEL"

# --- secret check (the key must already be in your session) ---
if ([string]::IsNullOrWhiteSpace($env:COPILOT_PROVIDER_API_KEY)) {
    Write-Host ""
    Write-Warning "COPILOT_PROVIDER_API_KEY is NOT set. Set it before launching Copilot:"
    Write-Host '    $env:COPILOT_PROVIDER_API_KEY = "<your-azure-key>"' -ForegroundColor Yellow
    Write-Host "  (Never commit the key. Never paste it into a prompt or a shared screen.)"
} else {
    $len = $env:COPILOT_PROVIDER_API_KEY.Length
    Write-Host "  COPILOT_PROVIDER_API_KEY  = set ($len chars, hidden)" -ForegroundColor Green
    Write-Host ""
    Write-Host "Ready. Launch 'copilot' and run /model to confirm your Azure deployment is active." -ForegroundColor Cyan
}

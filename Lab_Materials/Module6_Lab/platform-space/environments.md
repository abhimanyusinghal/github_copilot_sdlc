# Environments & approvals — Acme Customer Portal
_(Local context for Copilot Chat in VS Code.)_

| Environment | Purpose | Deploy trigger | Approval | Rollback |
| --- | --- | --- | --- | --- |
| **dev** | Continuous integration of merged work | Every push to `main` | None | Redeploy previous build |
| **staging** | Release candidate verification; mirrors prod data shape (synthetic) | Tagged RC | Team lead | Redeploy previous tag |
| **production** | Live customers | Tagged release; **manual dispatch in this lab** | **Named human reviewer** (protected environment) | Tested rollback script + feature flag off |

## Rules
- **Production is protected.** A named human approves; approval is never delegated to an agent or bot.
- **Canary slice for production:** start at **10%** of traffic, hold for the soak window, then ramp
  25% → 50% → 100% while health metrics stay green.
- **Soak window:** minimum **15 minutes** at the canary slice before any ramp.
- **Feature flags** decouple deploy from release — prefer flagging a risky change off over a redeploy.
- **Secrets** live in the environment's secret store, scoped per environment. Prod secrets are never
  readable from dev/staging jobs.

## Health signals that gate a ramp (and trigger rollback)
Use these pre-agreed thresholds; do not invent replacements:
- **Web:** roll back if portal HTTP **5xx exceeds 1% for 5 consecutive minutes**, or user-facing
  **p95 latency is 2 seconds or more for 5 consecutive minutes**.
- **Changed component:** roll back if the new error signature appears **5 times in 5 minutes**.
- **Data / Power BI:** stop the ramp on **any mandatory data or measure-test failure**, any refresh
  failure, or freshness lag over **30 minutes**.
- **QA:** any required-suite failure blocks the ramp.
- **RPA:** pause new runs and stop the ramp after **2 matching unhandled exceptions in 5 minutes**;
  do not terminate in-flight work until its transaction-safety point is known.

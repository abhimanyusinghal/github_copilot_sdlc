# ALERT · INC-2026-0723-01 · P1

```
SEVERITY : P1
FIRED    : 2026-07-23T14:41:00Z
MONITOR  : portal-5xx-rate
CONDITION: HTTP 5xx rate across the portal > 5% for 5 minutes
OBSERVED : 11.4% (baseline 0.2%)
SERVICE  : Acme Customer Portal (errors traced to reset-service)
STATUS   : FIRING
```

**Customer impact reported by Support:** several customers say the "Forgot password" page shows an error
after they submit their email. Support has 6 open tickets in the last 20 minutes.

**On-call first actions (per policy):** acknowledge, assess blast radius, identify what changed, and
confirm enough evidence and rollback safety to choose a mitigation. A fix-forward requires a confirmed
root cause; a safe rollback of a change-correlated P1 need not wait for full root-cause analysis.

> Attach this file, `app.log`, and `deploy-history.md` to Copilot Chat in VS Code to triage.
> Do **not** paste customer data into a prompt — see `ops-space/pii-and-prompts.md`.

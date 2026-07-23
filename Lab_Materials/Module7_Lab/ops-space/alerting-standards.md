# Alerting & triage standards — Acme Customer Portal

## Severity
| Sev | Meaning | Response | Comms |
| --- | --- | --- | --- |
| **P1** | Customers cannot complete a core task, or data/security is at risk | Immediate, page on-call | Incident channel + Support within 15 min |
| **P2** | Degraded experience, workaround exists | Same business day | Incident channel |
| **P3** | Minor / cosmetic / internal | Next planned work | Ticket only |

## What is allowed to page a human
Alert on **user pain**, not on every wiggle:
- 5xx rate on a user-facing endpoint above baseline for a sustained window.
- p95 latency breaching the NFR (2s) for a sustained window.
- A **new** error signature appearing after a change.
- Data/report freshness or refresh failure before a business deadline.

**Not** page-worthy on their own: a warning that has been firing at a steady rate for days, a single
transient timeout with successful retry, or a threshold breach shorter than the sustained window.

## Triage order (the operate loop)
1. **Detect** — what fired, when, and what is the **blast radius** (who/how many affected)?
2. **Diagnose** — cluster the logs, rank by **impact and novelty**, and correlate with recent change.
3. **Confirm** — verify the hypothesis in code/config before a fix-forward. For a reversible rollback,
   first confirm the change correlation and rollback safety; full root-cause analysis may follow recovery.
4. **Resolve** — the smallest safe action (roll back, flag off, or fix forward), **approved by a human**.
5. **Learn** — capture a runbook and a postmortem; fix the class of problem, not just the instance.

## Noise discipline
- Known, ticketed issues are recorded in `deploy-history.md` under "Known pre-existing issues" — check
  there before declaring anything new.
- Too many alerts is the same as none. If an alert fires and no one acts, fix the alert.

# Merged pull requests since release 2.3.2 — input for release notes

_(A captured list. In Lab 6 you generate release notes from this file locally in VS Code.
Not everything here belongs in a customer-facing note — that judgement is yours.)_

| PR | Title | Type | Notes |
| --- | --- | --- | --- |
| #128 | Add self-service password reset (single-use, 30-min link) | feature | User-facing. The headline change. |
| #142 | Add rate limiting to password-reset requests | security | Threshold still `TBC with Security`; shipped with a conservative default. |
| #147 | Return a uniform response for unknown emails on reset | security | Closes an account-enumeration side channel. **Do not describe the vulnerability in detail publicly.** |
| #151 | Fix: legacy accounts with no email on file get a clear message | fix | User-facing. |
| #153 | Correct active-user metric to a 30-day window (was 90) | fix | Changes reported numbers — dashboards will shift. Needs a heads-up to Support managers. |
| #155 | Correct P3 SLA target to 72h in breach calculation | fix | Changes reported numbers. |
| #156 | Quarantine and count dirty ticket rows instead of dropping them | fix | Data quality; affects reported totals. |
| #158 | Bump pytest and CI dependencies | chore | Internal only — not customer-facing. |
| #159 | Refactor reset service into smaller helpers | chore | Internal only; no behaviour change. |
| #161 | Account-closure process: require human approval before closing | compliance | Internal process change; Support/Compliance need to know. |

**Release:** 2.4.0 · **Target:** production · **Previous:** 2.3.2

# Escalation & production-action policy

## Who approves what
| Action | Approver | Notes |
| --- | --- | --- |
| Roll back a release | **On-call engineer** (named) | Preferred first action for a change-correlated P1 |
| Toggle a feature flag off | On-call engineer | Fastest mitigation when the change is flagged |
| Fix forward to production | On-call **+ a second reviewer** | Only when rollback is unsafe (e.g. data migration) |
| Config change in production | On-call engineer | Must be recorded in the incident timeline |
| Anything by an automated agent | **Not permitted unattended** | Agents propose; a named human approves and executes |

## Rules
- **A human owns production.** No agent, bot, or AI suggestion applies a production change on its own.
- **Confirm before you fix forward.** Acting on an unverified AI root cause is how you cause a second
  incident. For a reversible rollback, confirm the change correlation and rollback safety first; do not
  delay restoration solely to complete root-cause analysis.
- **Audit trail.** Every production action is recorded: who, what, when, why, and the approval.
- **Communicate.** P1 → Support informed within 15 minutes with customer-safe wording.
- **Rollback first, complete the root-cause analysis second** for a change-correlated P1 when rollback is
  safe. Continue incident-priority investigation after recovery; “at your own pace” does not mean
  abandoning the follow-up.

## Escalate when
- The cause is not confirmed within **30 minutes**, or
- Rollback is unsafe or fails, or
- The incident involves **data loss, a security issue, or exposed PII** → escalate to Security immediately.

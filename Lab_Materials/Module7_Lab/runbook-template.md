# Runbook — `<failure name>`

**Applies to:** <service / component>  ·  **Severity:** <P1/P2/P3>  ·  **Owner:** <team>
**Last verified:** <date, by whom>

## 1. How you'll know (detect)
- **Alert:** <monitor name and condition>
- **Symptom users see:** <plain language>
- **Error signature:** <type + file:line, or log pattern>

## 2. Confirm it's this (not something else)
> Confirm the evidence needed for the action. A fix-forward requires a confirmed cause; a safe rollback
> can precede full root-cause analysis when the failure clearly correlates with a change.

- [ ] <check 1 — e.g. error signature present in logs, and started at time T>
- [ ] <check 2 — e.g. correlates with a change at time T-n; state the gap>
- [ ] <check 3 — e.g. verified in code/config: file, line, and the mismatch>
- **Rule out:** <the known noisy signals that look similar but aren't this>

## 3. Blast radius
<Who is affected, how many, which journey is broken, and what still works.>

## 4. Mitigate (fastest safe action first)
| Step | Action | Approver | Expected effect |
| --- | --- | --- | --- |
| 1 | <e.g. roll back to the previous release> | <named human> | <service restored in ~N min> |
| 2 | <e.g. toggle feature flag off> | <named human> | <…> |
| 3 | <fix forward — only if rollback is unsafe> | <on-call + 2nd reviewer> | <…> |

## 5. Verify recovery
- [ ] <signal returns to baseline — name the metric and the value>
- [ ] <a real user journey succeeds end to end>
- [ ] <no new error signature introduced by the mitigation>

## 6. Communicate
- **Support/customers:** <customer-safe wording — no exploit detail, no PII>
- **Incident channel:** <what to post, and when>

## 7. Prevent (follow-ups)
| Action | Why | Owner | Ticket |
| --- | --- | --- | --- |
| <e.g. add a test for the config contract> | <stops the class of failure> | <name> | <id> |

---
_Copilot can draft this from a resolved incident; **you** verify each confirm-step is actually checkable
and that a human approver is named for every production action._

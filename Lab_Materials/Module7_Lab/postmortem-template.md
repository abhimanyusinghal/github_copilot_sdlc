# Postmortem — `<incident id>` (blameless)

**Severity:** <P1/P2/P3>  ·  **Duration:** <detect → resolved>  ·  **Author:** <name>  ·  **Date:** <date>

## Summary
<Two or three sentences a non-engineer could follow: what broke, for whom, for how long, and how it was fixed.>

## Impact
- **Users affected:** <how many / which journey>
- **Duration of impact:** <start → end, in UTC>
- **Support load:** <tickets, calls>
- **Data impact:** <any loss, corruption, or none — say explicitly>

## Timeline (UTC)
| Time | Event |
| --- | --- |
| <t> | <change deployed / alert fired / triage started / cause confirmed / mitigation applied / verified> |

## Root cause
<The actual mechanism, with evidence: file, line, config key, and why it produced the symptom.
Distinguish the **trigger** (what changed) from the **latent weakness** (why the system was fragile).>

## What went well
- <e.g. correlation to the deploy was fast>

## What went badly
- <e.g. shipped at 100% with no canary; the cause was masked by a noisy known warning>

## Contributing factors
- <e.g. config keys renamed without a contract test; no staging soak; PII in logs slowed sharing>

## Preventive actions
| Action | Type | Owner | Due | Ticket |
| --- | --- | --- | --- | --- |
| <fix the class, not just the instance> | detect / prevent / respond | <name> | <date> | <id> |

## Detection & response quality
- **Time to detect:** <n min>  · **Time to confirm cause:** <n min> · **Time to mitigate:** <n min>
- Did an alert catch it, or did a human/customer? <…>
- Was there a runbook? <yes/no — if no, it is now: link it>

---
_Blameless: describe systems and decisions, not people. Copilot can draft the timeline from the logs and
deploy history — **verify every timestamp** against the source before publishing._

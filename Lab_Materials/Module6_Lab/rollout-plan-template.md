# Rollout plan — `<release>` (template)

**Change:** <what is shipping, in one line>
**Risk assessment:** <low / medium / high> — <why: diff size, hot files, coverage, blast radius>

## Stages
| Stage | Traffic | Soak | Proceed if | Owner |
| --- | --- | --- | --- | --- |
| Canary | 10% | 15 min | all health signals green | <name> |
| Ramp 1 | 25% | <time> | <condition> | <name> |
| Ramp 2 | 50% | <time> | <condition> | <name> |
| Full | 100% | — | <condition> | <name> |

## Health signals watched
| Signal | Normal | Rollback threshold | Source |
| --- | --- | --- | --- |
| HTTP 5xx rate | <baseline> | <trigger> | <dashboard/log> |
| p95 latency | < 2s (NFR) | <trigger> | <dashboard> |
| Error-log rate (changed component) | <baseline> | <trigger> | <log query> |

## Rollback
- **Trigger:** <the pre-agreed condition — decided BEFORE deploy>
- **Method:** <script / redeploy previous tag / feature flag off>
- **Tested?** <yes/no — when and by whom. "No" is a release blocker.>
- **Time to recover:** <estimate>
- **Data considerations:** <migrations, backfills — is the rollback safe for data?>

## Approval
- **Production approver (named human):** <name>
- **Approved at:** <timestamp>
- **Feature flag:** <name, default state>

## Open items
| Item | Owner | Blocks release? |
| --- | --- | --- |
| <TBC value or unknown> | <name> | <yes/no> |

---
_Copilot can draft this; **you** set the thresholds and the trigger, and a named human approves.
Do not invent thresholds — take them from `platform-space/environments.md` or mark them `TBC`._

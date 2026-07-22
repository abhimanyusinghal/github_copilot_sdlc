# Data model & metric definitions — support metrics (Data & Analytics)

Design output from Lab 3. Implement `src/support_metrics.py` to these definitions.

## Sources
- `data/tickets_sample.csv` — `ticket_id, customer_id, channel, priority, created_at, closed_at`.
- `data/logins_sample.csv` — `customer_id, login_at`.

## Canonical definitions (glossary)
- **Active user** — a **distinct** customer who logged in within the **last 30 days**.
- **Resolution time** — `closed_at − created_at` (hours), per ticket; averaged over **valid** rows.
- **Valid row** — closed, non-negative resolution time, channel in {email, chat, phone}.
- **Quarantined row** — open, negative, or unknown channel. **Counted, never silently dropped.**
- **SLA breach (lab fixture)** — resolution time exceeds **P1 = 4h, P2 = 24 elapsed hours,
  P3 = 72 elapsed hours**. The source requirement says business days; a production calendar and timezone
  remain **TBC with Support Operations**. Do not present this lab approximation as business-calendar logic.

## Functions to build
`active_users`, `resolution_hours`, `partition_tickets` (→ valid, quarantined),
`average_resolution_hours`, `sla_breaches`. The acceptance tests encode the expected results.

## Rules
- Nightly publish (not real-time) and row-level access by team are downstream pipeline/model requirements.
  This Python scaffold exposes neither refresh metadata nor team/role context, so record them as unverified
  gaps rather than claiming them from green function tests.
- No PII beyond what a report needs.

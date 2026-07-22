# Spec · Support metrics — data-quality & metric tests  (Data & Analytics track)

> Your Lab 2 metric definitions, restated as the **oracle for testing**. **Code under test:**
> `sample-app/src/support_metrics.py`. **Oracle values:** `../KNOWN-GOOD-METRICS.md`.

## Metrics
Active users, average ticket resolution time, and SLA breaches — by the canonical definitions below.

## Canonical definitions (from `../testing-space/glossary.md`)
- **Active user** — logged in within the last **30 days** (not 90). Count **distinct** customers.
- **Resolution time** — `closed_at − created_at`, per ticket; averaged over **valid** rows.
- **Valid row** — closed, non-negative, channel in {email, chat, phone}.
- **Quarantined row** — open, negative, or unknown channel — **counted, never silently dropped**.

## Acceptance criteria (each becomes a runnable test or explicit gap)
1. **Active-user window** — `active_users` counts logins within **30 days**; the expected count for the sample is in the oracle.
2. **Grain** — resolution time is computed at the **grain of one ticket**.
3. **Data quality** — open / negative / unknown-channel rows are **quarantined and counted**, not dropped and not averaged in.
4. **Average correctness** — the average matches the oracle when computed over valid rows only.
5. **SLA classification** — breaches use targets **P1 = 4h, P2 = 24h, P3 = 72h**; the breach set matches the oracle.
6. **Freshness (design gap)** — the published metric is "as of last night" (nightly), **not** real-time.
   The scaffold has no publish timestamp or pipeline metadata, so document the missing test seam and owner;
   do not write an always-green placeholder or claim real-time behaviour.

## Test focus for this track
Executable tests for the defined data-quality cases (open `closed_at`, negative resolution, and unknown
channel) plus metric correctness against `../KNOWN-GOOD-METRICS.md`. Requirements for other malformed
schemas/ranges need a confirmed ingestion contract. Freshness and referential integrity need pipeline/join
metadata that this scaffold does not expose; keep them as named test-design gaps.

> **SLA fixture assumption:** P2=24 and P3=72 are elapsed-hour values for this lab data. They are not a
> production business-hours calendar. Calendar and timezone rules remain TBC.

## Open questions (do not guess)
- Is **CSAT** captured, and where? (Out of scope for these tests until confirmed.)
- Confirm the authoritative **join key** between tickets and logins.

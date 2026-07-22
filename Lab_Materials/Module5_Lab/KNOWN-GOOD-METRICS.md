# Known-good metrics — the test oracle (Data & Analytics / Power BI)

These values were calculated **independently of the application code**, directly from the sample data,
using the **canonical definitions** in `testing-space/glossary.md` and `testing-space/nfr-standards.md`.
Use them as the source of truth: a measure that disagrees with a number here is **wrong**, even if it
runs without error. (This is slide 20's "validate measures against known-good numbers.")

**Reference clock for the active-user window:** `now = 2026-07-21T09:00:00`.
**Data files:** `sample-app/data/tickets_sample.csv`, `sample-app/data/logins_sample.csv`.

## Definitions used (canonical)

- **Active user** — a customer who logged in within the last **30 days** (i.e. `login_at ≥ 2026-06-21T09:00:00`). Count **distinct** customers.
- **Resolution time (hours)** — `closed_at − created_at`, per ticket. Average over **valid** rows only.
- **Valid ticket** — closed, non-negative resolution time, **and** a channel in {`email`, `chat`, `phone`}.
- **Quarantined ticket** — open, or negative resolution time, or an unknown channel. Counted, never silently dropped.
- **SLA target (lab-fixture hours)** — P1 = 4, P2 = 24 elapsed hours, P3 = 72 elapsed hours. **Breach**
  when resolution time **exceeds** the target. The production requirement uses business days; calendar,
  working hours, holidays, and timezone remain TBC and are not modeled by this fixture.

## Expected values

| Metric | Expected value | Notes |
| --- | --- | --- |
| Active users (30-day) | **4** | C1, C2, C3, C6. C4 (41 days) and C5 are **not** active. |
| Average resolution time | **31.0 hours** | Over 5 valid tickets: T1=6, T2=2, T3=48, T7=3, T8=96. |
| Quarantined tickets | **3** | T4 (open), T5 (negative), T6 (unknown channel `sms`). |
| SLA breaches | **1** | T8 only (P3, 96h > 72h). |

## Per-ticket resolution time (for reference)

| Ticket | Channel | Priority | Hours | Classification |
| --- | --- | --- | --- | --- |
| T1 | email | P2 | 6 | valid, within SLA |
| T2 | chat | P1 | 2 | valid, within SLA |
| T3 | phone | P3 | 48 | valid, within SLA |
| T4 | email | P2 | — | quarantined (open) |
| T5 | chat | P1 | −24 | quarantined (negative) |
| T6 | sms | P2 | 3 | quarantined (unknown channel) |
| T7 | email | P1 | 3 | valid, within SLA |
| T8 | phone | P3 | 96 | valid, **SLA breach** |

> If a measure you are validating returns something other than the "Expected value" column, you have
> found a real defect. Write the failing check first, then trace it to the rule it violates.

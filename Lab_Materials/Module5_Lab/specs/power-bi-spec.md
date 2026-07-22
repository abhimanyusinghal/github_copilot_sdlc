# Spec · Support dashboard — measure validation  (Power BI track)

> Power BI itself is not exercised in this VS Code-only lab. You validate **Python reference
> calculations** in `sample-app/src/support_metrics.py` against known-good numbers.
> **Oracle:** `../KNOWN-GOOD-METRICS.md`. Green tests here do not validate DAX, a PBIX model, visuals,
> row-level security, or refresh.

## Dashboard measures
Ticket volume, average resolution time, and an **SLA traffic light** — filtered by team, channel, date;
row-level security by team.

## Canonical definitions (from `../testing-space/glossary.md`)
- **SLA breach** — a ticket open longer than its target: **P1 = 4h, P2 = 1 business day (24h), P3 = 3 business days (72h)**.
- **Active user** — logged in within **30 days**.
- **Resolution time** — `closed_at − created_at`.

## Acceptance criteria (each becomes runnable reference evidence or an explicit gap)
1. **SLA reference calculation** — the breach classification matches the oracle (**1 breach: T8**).
2. **Average resolution** — matches the oracle (**31.0h**) over valid rows.
3. **Active users** — matches the oracle (**4**), using the **30-day** window.
4. **Quarantine** — dirty rows (open / negative / unknown channel) do **not** silently distort the totals; the quarantined count matches the oracle (**3**).
5. **RLS (design gap)** — row-level security belongs in the Power BI model. Describe the required role/user
   validation and owner; do not claim it from Python tests.
6. **Refresh (design gap)** — freshness requires dataset refresh metadata. Describe the check and owner;
   do not create an always-green placeholder.
7. **Visual/traffic-light design gap** — DAX/conditional formatting must be validated in a Power BI-capable
   environment; the scaffold exposes no traffic-light calculation.

## Test focus for this track
Reference-calculation tests: compute criteria 1–4 from the sample data and compare them with the oracle.
Treat a mismatch as a defect in the Python reference implementation. Keep DAX/PBIX/RLS/refresh/visual
validation as explicit gaps; a green Python suite is not evidence that those layers work.

## Open questions (do not guess)
- Confirm the **business-hours calendar** used for P2/P3 "business day" math.
- The fixture uses P2=24 and P3=72 **elapsed hours** only; it is not a production calendar.
- Next-week **forecast** page is out of scope for validation this iteration.

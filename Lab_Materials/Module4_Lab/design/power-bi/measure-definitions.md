# Measure definitions — support dashboard (Power BI)

Design output from Lab 3. Power BI itself is not exercised in this VS Code-only lab. In Lab 4 you
implement **Python reference calculations** in `src/support_metrics.py` (the same functions the Data track
builds) and prove them against acceptance tests. Later DAX should match this oracle, but these tests do
**not** validate DAX, a PBIX model, row-level security, visuals, or refresh.

## Measures (must agree with these results on the sample data)
- **Active users (30-day)** — distinct customers with a login in the last 30 days → **4**.
- **Average resolution time** — over valid rows → **31.0 hours**.
- **Quarantined tickets** — open / negative / unknown channel → **3**.
- **SLA breaches** — resolution time over target (P1 4h, P2 24h, P3 72h) → **1** (T8).

## Design notes to carry into the model
- **Row-level security by team** — enforced in the model, not just the visual.
- **Refresh** before 9:00am; a data-as-of timestamp is visible. Both refresh and RLS remain unverified design
  gaps in this lab and need Power BI-capable validation before release.
- Traffic light: red only for a genuine breach; amber ≥ 80% of target; green otherwise.
- P2=24h and P3=72h are elapsed-hour assumptions for the supplied fixture. The production business-hours
  calendar and timezone are **TBC with Support Operations**.

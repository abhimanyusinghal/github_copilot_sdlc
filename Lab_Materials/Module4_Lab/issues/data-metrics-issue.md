# Issue: Implement support metrics (Data & Analytics / Power BI)

**Scope:** implement `src/support_metrics.py` to the definitions.

**Design:** `design/data-analytics/metric-and-data-model.md` (Power BI: `design/power-bi/measure-definitions.md`).

**Acceptance criteria** (green build target in `tests/acceptance/test_support_metrics.py`):
- `active_users` uses the **30-day** window → 4 on the sample data.
- `average_resolution_hours` over valid rows → 31.0.
- Dirty rows (open / negative / unknown channel) are **quarantined and counted** → 3.
- `sla_breaches` uses targets P1 4h / P2 24h / P3 72h → only T8.

**Definition of done:** `dev-space/definition-of-done-dev.md`. Add a data-quality test; review; keep it small.

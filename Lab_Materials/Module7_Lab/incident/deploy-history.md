# Deploy & change history — Acme Customer Portal

| When (UTC) | Release | Change | Rollout | By |
| --- | --- | --- | --- | --- |
| 2026-07-23 14:30 | **v2.4.0** | Password reset (#128), reset rate limiting (#142), uniform response for unknown emails (#147), metric corrections (#153/#155/#156), closure approval (#161). **Renamed reset rate-limit config keys.** | **100% immediately** | ci-bot |
| 2026-07-21 09:15 | v2.3.2 | Ticket export fix; dependency bumps | 100% | ci-bot |
| 2026-07-20 16:40 | infra | Increased `tickets` table size; **no index added on `team_id`** | n/a | platform |
| 2026-07-17 11:05 | v2.3.1 | Dashboard filter fix | 100% | ci-bot |

## Known pre-existing issues (already ticketed — not new today)

- **PLAT-812 — slow `tickets_by_team` query.** Open since **2026-07-20**, after the table grew without an
  index. Produces a steady stream of `slow_query` WARNs (~40/hour, all day, every day). Being worked by the
  platform team. **This is noisy, but it is not new and it does not return 5xx to customers.**
- **PLAT-799 — occasional KYC upstream timeouts.** Long-standing, low volume, retried automatically.

> Note: v2.4.0 went out at **100% traffic with no canary** — exactly what Lab 6's rollout plan was meant to
> prevent. Worth capturing in the postmortem.

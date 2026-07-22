# Spec · Support metrics — resolution time & active users  (Data & Analytics track)

> **This is your Lab 2 output, pre-built.** If you finished Lab 2, use *your* spec instead.
> It is the **input** to Lab 3: you'll design the **data model and pipeline** for it.
> Domain: **Acme Customer Portal** (see `../architecture-space/`).

## User story
**As** Dana (a support manager),
**I want** a trustworthy view of **average ticket resolution time** and **active users**, broken down by channel,
**so that** I can spot SLA risk and staffing needs for my own team.

## Metric definitions (canonical — from `../architecture-space/glossary.md`)
- **Active user** — a customer who logged in within the last **30 days** (*not* 90; not "ticket activity").
- **Resolution time** — time from ticket creation to ticket closed.
- **Channel** — one of `email`, `chat`, `phone`.

## Acceptance criteria (Given / When / Then)
1. **Grain** — *Given* the ticket source, *When* resolution time is computed, *Then* it is at the **grain of one ticket**, and the report aggregates to **team × channel × day**.
2. **Sources** — *Given* two systems, *Then* tickets come from the **support database** and logins from the **auth logs**; the join key and its owner are documented.
3. **Refresh** — *Given* the warehouse refreshes **nightly**, *Then* the report states "as of last night" — **not** real-time (the raw ask for "real time" is out of scope this iteration).
4. **History** — *Given* an 18-month retention window, *Then* queries beyond 18 months return "no data", not silent zeros.
5. **Data quality** — *Given* a nightly load, *Then* rows with a null/negative resolution time or an unknown channel are **quarantined and counted**, not dropped silently.
6. **CSAT (conditional)** — *Given* CSAT is captured at ticket closure, *Then* include it **only if** the field is confirmed populated (`TBC: do we actually capture it?`).

## NFRs applied (from the standard plus feature-specific constraints)
- **Privacy** — no PII in the reporting layer beyond what's needed; 18-month retention; row-level access by team.
- **Reliability** — a failed source load fails the run with a clear message; no partial silent publish.
- **Auditability** — each published dataset records source loads and row counts.

## Open questions (take to stakeholders)
- "Active" was requested as logins **or** ticket activity — confirmed here as **logins in 30 days**; get sign-off.
- A login event has no support **channel**. Confirm how an active user is attributed to a channel, which
  join key is authoritative, and whether one user may count in more than one channel before building the
  team × channel × day aggregate.
- The **same metric was requested last quarter under a different name** — reconcile before publishing.
- Is **CSAT** actually captured, and where?

_Use `../architecture-space/design-readiness-checklist.md` for the Lab 3 design hand-off. The
implementation Definition of Done is evaluated in later modules._

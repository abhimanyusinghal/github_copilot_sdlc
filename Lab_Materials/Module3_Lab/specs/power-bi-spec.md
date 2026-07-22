# Spec · Support performance dashboard  (Power BI track)

> **This is your Lab 2 output, pre-built.** If you finished Lab 2, use *your* spec instead.
> It is the **input** to Lab 3: you'll design the **semantic model (star schema), measures and RLS**.
> Domain: **Acme Customer Portal** (see `../architecture-space/`).

## User story
**As** Dana (a support manager),
**I want** a dashboard of ticket volume and resolution time with an SLA traffic light,
**so that** I can manage my own team's performance before stand-up each morning.

## Acceptance criteria (Given / When / Then)
1. **Filters** — *Given* the dashboard, *When* I open it, *Then* I can filter by **team**, **channel** (`email`/`chat`/`phone`) and **date range**.
2. **Row-level security** — *Given* I am a manager, *When* I view any page, *Then* I see **only my own team's** rows (RLS by team); a VP role sees all teams.
3. **SLA traffic light** — *Given* the **SLA-breach** definition below, *When* a ticket is over target, *Then* it shows **red**; within target **green**; approaching (≥80% of target) **amber**.
4. **Refresh** — *Given* a scheduled refresh, *Then* data is current **before 9:00am** local, before stand-up.
5. **Mobile** — *Given* a phone layout, *When* a VP opens it on mobile, *Then* the key visuals are usable (a phone-optimised layout exists).
6. **Brand** — visuals use the corporate palette.

## SLA breach definition (canonical — from `../architecture-space/glossary.md`)
A ticket **open longer than its target resolution time**: **P1 = 4 hours, P2 = 1 business day, P3 = 3 business days**. (This was undefined in the raw notes — now pinned.)

## NFRs applied (from the standard plus feature-specific constraints)
- **Security/Privacy** — RLS enforced in the model, not just visuals; no PII beyond what a manager needs.
- **Performance** — pages render < 2s at P95 on the published dataset.
- **Auditability** — refresh history retained; a data-as-of timestamp is visible.

## Open questions (take to stakeholders)
- **Next-week volume forecast** — requested by one VP; treat as a **stretch** page, not core, this iteration.
- Confirm the **business-hours calendar** used for P2/P3 "business day" math.
- Confirm whether the SLA traffic light covers only currently open tickets or also tickets that closed
  after their target; the current definition explicitly describes a ticket that is open too long.

_Use `../architecture-space/design-readiness-checklist.md` for the Lab 3 design hand-off. The
implementation Definition of Done is evaluated in later modules._

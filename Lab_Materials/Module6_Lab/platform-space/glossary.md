# Glossary — delivery terms (Lab 6)
_(Portal domain terms are unchanged from Modules 2–5.)_

- **Canary** — releasing to a small slice of traffic first, watching health, then ramping.
- **Progressive rollout** — increasing traffic in stages while health metrics stay good.
- **Feature flag** — a toggle that decouples *deploy* (code is out) from *release* (users see it).
- **Blast radius** — how many users a bad change reaches. Smaller is safer.
- **Rollback trigger** — the pre-agreed condition that causes an automatic or immediate revert.
- **Soak window** — the minimum time to observe a canary before ramping.
- **Protected environment** — an environment whose deploys require a named human approval.
- **Least privilege** — granting only the access a job needs, and no more.
- **Active user** — a customer who logged in within the last **30 days** (canonical, from Module 2).
- **SLA breach** — a ticket open longer than its target (P1 4h, P2 1 business day, P3 3 business days).

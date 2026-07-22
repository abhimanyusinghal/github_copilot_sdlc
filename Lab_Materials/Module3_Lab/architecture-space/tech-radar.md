# Tech Radar — Acme Customer Portal
_(Use this as local context by attaching it to GitHub Copilot Chat in VS Code.)_

Copilot: **prefer "Adopt", justify "Trial", avoid "Hold".** Don't propose trend-driven tech that
isn't on this radar without saying why.

## Adopt (our approved, default stack)
- **Drupal 10 / PHP 8.x** — the customer portal.
- **PostgreSQL** — relational data store.
- **Existing Auth service (OAuth2 / OIDC)** — for all identity, MFA and reset tokens.
- **REST + OpenAPI (contract-first)** — service interfaces.
- **Mermaid** — diagrams-as-code (C4, sequence, ER) in the repo.
- **Power BI** — dashboards and semantic models.
- **GitHub** — source, PRs, Issues, code scanning.

## Trial (allowed with a justification + an ADR)
- **Serverless functions** — for isolated, spiky, stateless jobs only.
- **Message queue** — where async decoupling is genuinely needed.
- **Redis cache** — for read-heavy hot paths with measured need.

## Hold (avoid unless there's a strong, recorded case)
- **New microservices** for a single portal feature — start with the modular monolith.
- **A second datastore technology** (NoSQL/graph) for this domain.
- **Rolling your own crypto, auth, or token store** — use the Auth service.
- **Real-time streaming** for reporting — the warehouse refresh is **nightly** by design.

> Rule of thumb: **the simplest, most reversible option that reuses what we have** wins. If you
> reach for a "Trial" or override a "Hold", that's exactly what an **ADR** is for.

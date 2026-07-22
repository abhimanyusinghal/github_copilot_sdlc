# Acme Customer Portal — Architecture Overview
_(Use this as local context by attaching it to GitHub Copilot Chat in VS Code.)_

**Purpose:** ground Copilot's design suggestions in what **already exists**, so options reuse our
systems instead of inventing new ones.

## Systems that already exist (reuse these)
- **Customer Portal** — the customer-facing web app, built on **Drupal 10 / PHP 8.x**. All self-service
  screens live here.
- **Auth service** — central identity service (OAuth2 / OIDC). Owns login, MFA, sessions, and
  **password-reset tokens**. New account flows integrate with it — they do **not** roll their own auth.
- **Support / Ticketing system** — source of truth for tickets (creation, status, resolution, channel).
- **CRM** — customer records; updated on account changes (e.g. closure).
- **Email service** — transactional email (reset links, confirmations); templates are brand/legal managed.
- **KYC system** — separate identity-verification system (its own login), used for high-assurance checks.
- **Analytics warehouse** — nightly-refreshed store behind reporting; feeds the **Power BI** semantic layer.

## Integration & conventions
- Services talk over **REST**, described **contract-first with OpenAPI**.
- **PostgreSQL** is the default relational store; the warehouse is separate from operational databases.
- Hosting is our standard cloud platform; environments are **dev → staging → prod**.
- Everything that ships is **versioned in Git** and reviewed in pull requests — including diagrams,
  contracts and ADRs (**design-as-code**).

## Design defaults
- Prefer a **modular monolith** for portal features unless a case is made otherwise (see the tech radar).
- **Reuse** the Auth, Email, Ticketing and CRM services; don't duplicate their responsibilities.
- Apply the **NFR checklist** (`nfr-standards.md`) to every design.
- Record significant choices as **ADRs** (`past-ADRs/`); honour the ones already made.

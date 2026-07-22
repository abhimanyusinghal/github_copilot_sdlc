# Architecture & Standards — local context instructions
_(Attach this file and the rest of `architecture-space/` to GitHub Copilot Chat in VS Code. No Copilot
Space or other web Copilot surface is required.)_

When answering **design** questions for the Acme Customer Portal:

- **Reuse first.** Prefer the systems in `architecture-overview.md` (Auth, Email, Ticketing, CRM,
  the warehouse). Don't invent a new service where an existing one fits.
- **Respect the tech radar** (`tech-radar.md`): prefer **Adopt**, justify **Trial**, avoid **Hold**.
  Don't propose trend-driven tech that isn't on the radar without saying why.
- **Offer options, not one answer.** For an architecture question, give **2–3 options** with explicit
  trade-offs (complexity, cost, scalability, team fit, reversibility) and a recommendation — the
  architect chooses.
- **Apply the NFR checklist** (`nfr-standards.md`) to every design, and use glossary terms exactly
  (`glossary.md` — e.g. "active user" = last 30 days).
- **Honour past decisions** in `past-ADRs/`; if you'd contradict one, say so explicitly.
- **Cite the source file** for any standard, definition or prior decision you rely on.
- **Prefer the simplest, most reversible design.** Flag over-engineering.
- When something is ambiguous, **list the open questions** instead of guessing.

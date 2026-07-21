# Definition of Done — Acme Customer Portal
_(Add this to the "Product Requirements" Copilot Space. Append it to every story in Lab 2.)_

A requirement is **Done** only when all of the following are true:

- **Acceptance criteria met** — every Given/When/Then criterion is demonstrated, not just claimed.
- **Independently reviewed** — code reviewed and approved by a human other than the author (see Module 1: the assigner can't self-approve an agent PR).
- **Tested** — automated tests cover each acceptance criterion (unit + relevant integration); all pass.
- **NFR checklist applied** — meets `nfr-standards.md`: performance (< 2s P95), security (OWASP; reset links single-use, expire in 30 min), privacy (no PII in logs; 18-month retention), accessibility (WCAG 2.1 AA), reliability, auditability.
- **No new High/Critical security alerts** — code scanning is clean (or alerts triaged and justified).
- **Traceable** — the item links need → issue → PR → test; the stakeholder "why" is recorded.
- **Docs updated** — user-facing changes noted; release/change summary drafted.
- **Stakeholder sign-off** — the product owner (or the requesting stakeholder) has validated it. Human validation is the deliverable, not the AI draft.

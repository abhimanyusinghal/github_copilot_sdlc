# Non-Functional Requirements (NFR) checklist
_(Same standard as Module 2. Attach this file to GitHub Copilot Chat in VS Code and apply it to every design.)_

- **Performance** — user-facing actions complete in under 2 seconds at P95.
- **Security** — follow OWASP; secrets never in code; MFA where available;
  password-reset links are **single-use and expire after 30 minutes**.
- **Privacy** — no PII in logs; comply with the 18-month data-retention policy.
- **Accessibility** — WCAG 2.1 AA; works with screen readers; mobile-friendly.
- **Reliability** — fail gracefully with a clear message when a dependency is down.
- **Auditability** — record who changed what and when for all account actions.

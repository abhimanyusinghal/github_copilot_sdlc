# Non-Functional Requirements (NFR) checklist
_(Same standard as Modules 2–3. Attach to Copilot Chat in VS Code. Tests should verify these where they apply.)_

- **Performance** — user-facing actions complete in under 2 seconds at P95.
- **Security** — follow OWASP; secrets never in code; MFA where available;
  password-reset links are **single-use and expire after 30 minutes**.
- **Privacy** — no PII in logs; comply with the 18-month data-retention policy. **Test data is synthetic.**
- **Accessibility** — WCAG 2.1 AA; works with screen readers; mobile-friendly.
  (An automated scan alone is **not** WCAG conformance — pair it with manual validation.)
- **Reliability** — fail gracefully with a clear message when a dependency is down.
- **Auditability** — record who changed what and when for all account actions.

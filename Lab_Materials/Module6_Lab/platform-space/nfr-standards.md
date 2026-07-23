# Non-Functional Requirements (NFR) checklist
_(Same standard as Modules 2–5. Attach to Copilot Chat in VS Code. Releases must not regress these.)_

- **Performance** — user-facing actions complete in under 2 seconds at P95.
- **Security** — follow OWASP; secrets never in code, logs, or prompts; MFA where available;
  password-reset links are **single-use and expire after 30 minutes**.
- **Privacy** — no PII in logs; comply with the 18-month data-retention policy.
- **Accessibility** — WCAG 2.1 AA; works with screen readers; mobile-friendly.
- **Reliability** — fail gracefully with a clear message when a dependency is down.
- **Auditability** — record who changed what and when, including **who approved a production deploy**.

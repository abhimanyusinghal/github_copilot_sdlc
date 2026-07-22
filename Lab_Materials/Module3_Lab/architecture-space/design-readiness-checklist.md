# Design readiness checklist — Acme Customer Portal

Use this checklist to decide whether a Lab 3 package is ready for Module 4. It is a **design exit
checklist**, not the implementation Definition of Done.

- **Spec coverage** — every acceptance criterion maps to explicit design evidence or a named gap.
- **Grounded decision** — the selected option cites the architecture overview, tech radar, NFR standard,
  glossary, and relevant accepted ADRs; rejected options and trade-offs are recorded.
- **Consistent artifacts** — the diagram and contract/model describe the same systems, boundaries,
  sequence, data, and error/exception behavior.
- **Reviewable design-as-code** — Mermaid renders in VS Code; text artifacts are saved under the track's
  `design/` folder; validation performed (and not performed) is stated truthfully.
- **Security and privacy** — trust boundaries are visible, STRIDE has been reviewed, at least one credible
  threat has a design-time mitigation, and no secrets or real PII appear in the package.
- **NFRs** — performance, security, privacy, accessibility, reliability, and auditability are addressed
  where applicable, with sourced targets rather than invented values.
- **Decision record** — one significant decision is captured in a substantively human-edited ADR whose
  status remains **Proposed** until the real approval process occurs.
- **Open decisions** — each assumption or `TBC` has an owner, the decision needed, and a stated effect on
  readiness. A blocking unknown prevents a **Ready** status.
- **Traceability** — the hand-off links spec → options → grounded decision → diagram/contract → risk → ADR,
  and all relative links resolve.
- **Human sign-off** — a named reviewer records **Ready**, **Ready with stated constraints**, or **Blocked**,
  with the date and remaining risk.

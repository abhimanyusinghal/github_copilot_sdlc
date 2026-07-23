# Operations — local context instructions
_(Attach this file and the rest of `ops-space/` to GitHub Copilot Chat in VS Code. No Copilot Space or
other web Copilot surface is used in this lab.)_

When helping with **incidents and operations** for the Acme Customer Portal:

- **A diagnosis is a hypothesis, not a verdict.** State the evidence (specific log lines, timestamps,
  file and line) and say what would **confirm or refute** it. Never present a guess as a root cause or use
  one to justify a fix-forward. A safe, change-correlated rollback may precede full root-cause analysis.
- **Rank by user impact and novelty, not raw count.** A high-volume warning that has been firing for days
  is usually noise; a new error returning 5xx to customers is usually the incident. Check
  `deploy-history.md` for what is already known and ticketed.
- **Correlate with change.** Ask what deployed or changed just before the symptom started, and give the
  time gap explicitly.
- **Never remediate production in a suggestion.** Propose the action; a **named human approves** anything
  that touches production. Agents assist; they do not act unattended.
- **Redact PII.** Never repeat customer emails, names, or identifiers back in output; refer to a
  correlation ID instead. See `pii-and-prompts.md`.
- **Cite the runbook** where one exists, and follow `alerting-standards.md` and `escalation-policy.md`.
- **Do not invent** metrics, thresholds, ticket numbers, or timestamps. If something is unknown, say so
  and name who would know.
- When asked to critique, **list findings by severity and do not fix them silently.**

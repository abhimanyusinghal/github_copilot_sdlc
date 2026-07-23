# Glossary — operations terms (Lab 7)
_(Portal domain terms are unchanged from Modules 2–6.)_

- **MTTR** — an ambiguous industry acronym (often “mean time to restore/recover,” sometimes “resolve”).
  In this lab it means time from detection until service is restored; record full resolution separately.
- **Blast radius** — how many users an incident or change affects.
- **Correlation ID** — a per-request identifier used to trace a request without naming a person.
- **Error signature** — the distinct shape of an error (type + location), used to group occurrences.
- **Novelty** — whether an error is *new* (first seen after a change) or pre-existing background noise.
- **Red herring** — a loud but unrelated signal; usually a known, ticketed, steady-rate warning.
- **Runbook** — the documented steps to detect, confirm, mitigate and verify a known failure.
- **Postmortem** — a blameless write-up: timeline, root cause, impact, and preventive actions.
- **Characterisation test** — a test that captures the *current* behaviour of legacy code so you can
  refactor safely, before you change anything.
- **Tech debt** — the maintenance cost of past shortcuts; prioritise the debt that slows delivery or raises risk.
- **Active user** — a customer who logged in within the last **30 days** (canonical, from Module 2).

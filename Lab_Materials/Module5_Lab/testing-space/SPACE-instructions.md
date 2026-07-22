# Testing — local context instructions
_(Attach this file and the rest of `testing-space/` to GitHub Copilot Chat in VS Code. Do not use a
Copilot Space or any other web/cloud Copilot surface.)_

When generating or reviewing **tests** for the Acme Customer Portal:

- **Test the criteria, not the code.** Derive tests from the acceptance criteria in the spec and from
  intent — **never** by asserting whatever the current implementation happens to do. Code may contain
  defects; a test that mirrors the code hides them.
- **Every test must be able to fail.** If a test can never go red, it proves nothing. Prefer meaningful
  assertions over lines covered.
- **Push to the edges.** Include boundary and negative cases (expiry at 29 vs 31 minutes, unknown email,
  reused link, negative/empty/oversized data), not just the happy path.
- **Trace every test to a criterion.** Name the criterion each test covers so coverage is meaningful.
- **Use the canonical definitions** in `glossary.md` (e.g. "active user" = last 30 days) and the targets
  in `nfr-standards.md`. Where a value is `TBC`, **do not invent it**. If a real seam exists, design a
  parameterized future test; otherwise record the missing interface/environment as a gap rather than
  creating an always-green placeholder.
- **Name the evidence boundary.** A Python domain function is not an HTTP API; Python reference calculations
  do not validate DAX/PBIX/RLS/refresh; a fake process interface cannot prove durable idempotency or audit.
  Distinguish tests actually run from future test designs.
- **Synthetic data only.** Generate realistic, edge-heavy, **privacy-safe** data. Never use real PII.
- **Keep the human in the loop.** You draft tests and data; the participant reviews them, confirms each
  can fail, and decides what is trustworthy. A passing suite is a claim to verify, not a guarantee.
- When asked to critique a suite, **list gaps by severity and do not fix them silently.**

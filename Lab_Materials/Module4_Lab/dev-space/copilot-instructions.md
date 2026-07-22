# copilot-instructions.md (house rules for Copilot)
_(Attach this file to Copilot Chat in VS Code. Do **not** overwrite an existing repository-level
`.github/copilot-instructions.md`; repository instructions can affect every participant and unrelated
work. A repository owner may merge these rules later through the normal review process.)_

When writing or changing code for the Acme Customer Portal:

- **Build to the design.** Implement to the contract, data model, and ADRs in `design/`. If the design
  is silent or ambiguous, ask — do not invent behaviour.
- **Small, single-purpose functions.** Prefer composition and early returns over deep nesting.
- **Type hints and docstrings** on public functions. Docstrings state the behaviour, not the mechanics.
- **A test with every change.** New or changed behaviour ships with a test that can fail.
- **Errors are explicit.** `consume_token` raises `InvalidToken`. A `Systems` dependency may raise
  `CrmUnavailable`; `process_closure` catches it and returns a named non-success outcome. Do not return
  silent `None` or falsely report success.
- **Security by default.** No secrets in code or prompts; no PII in logs; validate inputs; use the Auth
  service for tokens (ADR-001). If asked, review your own change for security before committing.
- **Do not invent policy values.** Anything marked `TBC` (rate-limit threshold, password rules) stays a
  named constant/parameter — never a guessed number.
- **Keep diffs reviewable.** One concern per change; explain non-obvious choices in the PR/commit.

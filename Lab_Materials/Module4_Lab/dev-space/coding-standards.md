# Coding standards — Acme Customer Portal (lab reference)

_(Attach to Chat, or fold into `copilot-instructions.md`. Keep it short so it's actually followed.)_

- **Language/runtime for this scaffold:** Python 3.10+, standard library only unless the design says otherwise.
- **Structure:** logic in `src/`, tests in `tests/`. Pure functions where possible; inject dependencies
  (e.g. the `Systems` object) rather than reaching for globals.
- **Naming:** `snake_case` for functions/variables, `PascalCase` for classes, verbs for actions
  (`create_reset_token`, `process_closure`).
- **Time:** pass `now` in explicitly (don't call the clock inside logic) so behaviour is testable.
- **Data:** treat CSV/input rows as untrusted — validate and quarantine bad rows; never crash on one bad record.
- **Tests:** `pytest`, one behaviour per test, assert on observable outcomes (return values, recorded calls).
- **Reviewability:** functions short enough to read at a glance; comments explain *why*, not *what*.

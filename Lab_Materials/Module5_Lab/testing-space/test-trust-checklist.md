# Test-trust checklist — would you gate a release on this suite?

Use this to decide whether a Lab 5 suite is trustworthy enough to hand to Module 6 (deployment).
It is the "**green must mean good**" gate, not a coverage-percentage target.

- **Traceable** — every acceptance criterion maps to at least one test, and every test names the
  criterion it covers. Uncovered criteria are listed as gaps with an owner.
- **Tests intent, not code** — tests were derived from the criteria, not by asserting the current
  implementation. No test encodes a known defect as "expected".
- **Each test can fail** — every meaningful test has been shown to go red when the behaviour or
  expectation is broken. No always-green tests.
- **Edges and negatives** — boundary, negative, and error paths are covered, not just the happy path.
- **Right level and honest boundary** — checks sit at the lowest available layer that can catch the failure.
  Domain-function tests are not relabelled as HTTP API tests; unavailable layers are explicit gaps.
- **Real defects found and fixed in the code** — where a test exposed a bug, the **code** was fixed (or
  the defect logged with an owner); the test was **not** weakened to make it pass.
- **Data is synthetic and repeatable** — fixtures/factories generate privacy-safe data; setup and
  teardown are repeatable; no real PII.
- **Stable and fast** — no known flakiness; any self-healing/retolerance is reviewed like code and does
  not hide a regression; the suite is quick enough to run on every change.
- **Balanced for the available system** — no thousand shallow duplicates, and missing integration/API/E2E
  layers are named rather than simulated or claimed as executed.
- **Honest status** — the hand-off states **Gate-ready**, **Gate-ready with stated gaps**, or **Not
  gate-ready**, with a reason, and no `TBC` policy value was invented to force green.
- **Human sign-off** — a named reviewer read the generated tests and recorded the status, date, and
  remaining risk.

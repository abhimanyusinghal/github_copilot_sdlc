# House rules for Copilot CLI agents (Lab 8)

Every agent in this lab reads this file. These are the non-negotiables.

- **Never edit a test to make it pass.** Tests are the spec; fix the code.
- **Never invent a policy value** (thresholds, limits, retention). Use a named constant marked `TBC` and
  flag it for a human.
- **Small, reviewable diffs.** Match the existing code style, naming, and error handling.
- **No irreversible actions unattended.** No force-push, no history rewrite, no deleting files you didn't
  create, no deploys. Propose; let a human approve destructive steps.
- **Secrets never appear in output** — not in code, logs, prompts, or artifacts. Redact PII before quoting.
- **Cite evidence** for any root-cause or "this works" claim: file, line, and the test that proves it.
- **Stay in your lane.** Requirements don't design; design doesn't implement; QA doesn't patch prod code to
  go green.

# Review & security checklist — Lab 4

Two passes on every change: **Copilot first** (fast, catches the obvious), **human second** (intent,
design fit, edge cases). Small diffs make both possible. Treat generated code exactly like a capable
junior's draft — read every line.

## Correctness & design fit
- [ ] Implements the **contract/design** (`design/<track>/`) — not a vague paraphrase of it.
- [ ] Every acceptance test is **green**, and each one can actually fail.
- [ ] You can **explain every line**. Nothing accepted that you don't understand.
- [ ] Edge/negative paths handled (expiry boundary, unknown email, bad data row, CRM down, no approval).
- [ ] Errors are explicit (domain exceptions), not silent `None`/success.

## Security (ask Copilot "any security issues here?" before committing)
- [ ] No secrets in code, config, or prompts; no PII in logs.
- [ ] Inputs validated; no injection (parameterised queries, no string-built SQL).
- [ ] No account enumeration (uniform reset response); tokens single-use, 30-min, hashed.
- [ ] Least privilege for any external system access.
- [ ] Acted on any real finding; nothing security-related merged unread.

## Craft & accountability
- [ ] Follows `copilot-instructions.md` / `coding-standards.md`.
- [ ] `TBC` values stay named constants/parameters — no invented numbers.
- [ ] Diff is small and single-purpose; the criteria it implements are noted.
- [ ] You rejected at least one weak suggestion **on purpose** — accept the good, reject the weak.
- [ ] A human owns the hand-off and has not treated Copilot's review as approval.

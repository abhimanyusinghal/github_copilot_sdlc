# PII, logs and prompts — what must never leave the system

## The rule
**Never paste real customer data into a prompt** — not to debug, not "just this once". This applies to
Copilot Chat exactly as it applies to a support ticket or a screenshot.

## What counts as PII here
Email addresses, names, phone numbers, postal addresses, account identifiers tied to a person, IP
addresses, and any free-text a customer wrote.

## Safe substitutes
- Refer to a **correlation ID** (`rst-9001`) instead of a person.
- Replace an address with a placeholder: `user=<redacted-email>`.
- Share the **error signature and line**, not the payload.
- Use synthetic examples (`riya@acme.test` in fictional lab data is fine; real customer data never is).

## Before attaching a log to Chat
1. **Scan it for PII first.** Logs are a common leak path — an application that logs a user's email puts
   PII into every downstream tool that reads that log.
2. **Redact** what you find, or attach an excerpt that excludes it.
3. If you discover PII in production logs, that is a **finding to fix**, not just something to work around:
   the NFR standard says *no PII in logs*. Raise it, and check the logging config
   (e.g. `redact_pii`) as part of the follow-up.

## Also never paste
Secrets, tokens, connection strings, or private keys. If one is exposed, treat it as an **incident** and
**rotate it** — deleting the line is not remediation.

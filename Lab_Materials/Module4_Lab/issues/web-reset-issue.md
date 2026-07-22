# Issue: Implement password-reset service (Web/Drupal, QA)

**Scope:** implement `src/password_reset.py` to the design.

**Design:** `design/web-drupal/openapi-password-reset.yaml`, `adr-007-reset-tokens.md`, `component-structure.md`.

**Acceptance criteria** (green build target in `tests/acceptance/test_password_reset.py`):
- Reset tokens are single-use and expire after **30 minutes**.
- A token is invalid at the exact 30-minute boundary, and its stored value is a SHA-256 digest.
- A used token cannot be reused.
- `POST /password-reset` returns the **same response** for known and unknown emails (no enumeration).

**Definition of done:** `dev-space/definition-of-done-dev.md`. Add a test with the change; run a local
Copilot Chat review and a security pass in VS Code; keep the diff small.

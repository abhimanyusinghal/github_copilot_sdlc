# ADR 007: Single-use, 30-minute reset tokens

**Status:** Accepted

**Context:** Self-service password reset needs a token that is safe if intercepted or leaked.
Security requires expiry and single use; the flow must not let an attacker enumerate accounts.

**Decision:**
- Reset tokens are **single-use** and **expire 30 minutes** after creation.
- A token is invalid at the exact boundary (`now >= expires_at`).
- Tokens are stored as a **SHA-256 digest**, never in plaintext or in logs. The random raw token used in
  the link exists only at the Auth-service boundary.
- `POST /password-reset` returns the **same 202 response** for known and unknown emails
  (no account enumeration).
- Reuse the central **Auth service** (ADR-001); the portal does not roll its own token store.

**Consequences:**
- (+) Short-lived, single-use tokens limit the blast radius of a leaked link.
- (+) The uniform response closes the account-enumeration side channel.
- (−) Users who wait too long must request a new link — accepted trade-off.
- (−) Requires a rate limit on requests; the exact threshold is **TBC with Security**.

**Teaching-scaffold boundary:** `password_reset.py` models the stored digest and lifecycle policy. It does
not simulate link delivery or Auth-service lookup of a presented raw token. Passing its tests is therefore
evidence for this policy model, not proof that the full HTTP/Auth integration is complete.

# ADR 001: Reuse the central Auth service for all account flows

**Status:** Accepted

**Context:** Multiple portal features (login, MFA, password reset, account closure) need identity and
token handling. We already run a central **Auth service** (OAuth2 / OIDC) that owns sessions, MFA and
token lifecycle. Duplicating any of this in the portal would fragment security responsibility.

**Decision:** All account flows **integrate with the existing Auth service** for identity, MFA and
token issuance/validation. The portal (Drupal) does **not** implement its own credential store, token
store, or crypto.

**Consequences:**
- (+) One place owns identity security; consistent MFA and audit.
- (+) Reset/closure flows inherit existing token and rate-limit machinery.
- (−) The portal depends on the Auth service's API and availability — design for graceful failure.

# Component structure — password reset (Web/Drupal)

Design output from Lab 3. Implement `src/password_reset.py` to this shape.

- **Route / controller** — accepts `POST /password-reset` and `/password-reset/confirm`
  (see `openapi-password-reset.yaml`).
- **Service** (`password_reset.py`) — the domain logic you build in Lab 4:
  - `create_reset_token(email, now)` — single-use, 30-minute record containing a stored token digest
    (ADR-007).
  - `token_is_valid(token, now)` / `consume_token(token, now)` — expiry + single use.
  - `request_reset(email, known_accounts, now)` — **uniform 202 response** (no enumeration).
- **Auth integration** — raw-token issue, delivery, and digest lookup belong to the central Auth service
  (ADR-001); the module here models the stored record and lifecycle policy the service enforces.
- **Boundaries** — no PII in logs; only a SHA-256 digest is stored; rate limit at the edge (threshold TBC).
  The scaffold is not an HTTP, email, password-update, or login integration.

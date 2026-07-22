# ADR 002: Start portal features as a modular monolith

**Status:** Accepted

**Context:** New self-service features (reset password, change email, close account) are small and
share data and auth. There's pressure to build each as a separate microservice "because we can", but
our team is small and the operational cost of many services is high.

**Decision:** Build portal features as **modules within the existing Drupal monolith**, with clear
internal boundaries. Reach for serverless or a separate service **only** with a recorded justification
(see the tech radar's "Trial").

**Consequences:**
- (+) Lower operational overhead; simpler local dev, deploy and debugging.
- (+) Easy reuse of shared account data and the Auth integration.
- (−) Must keep module boundaries disciplined so the monolith doesn't become a big ball of mud.
- (−) A genuinely independent-scaling need would require revisiting this (a new ADR).

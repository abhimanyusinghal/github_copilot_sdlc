# Raw notes - QA for password reset  (QA / Testing track)
_Unstructured on purpose. Turn these into testable acceptance criteria._

- Need to test the new self-service password reset.
- Happy path: request link, click it, set a new password, log in.
- What about an expired link? and a reused (already-clicked) link?
- Invalid or unknown email address?
- Rate limiting - can someone spam reset requests?
- Must work on mobile and with a screen reader.
- Password rules - minimum length? we follow the security standard (see the NFR standards doc).
- Someone said "just test that it works" - but we need real, specific criteria.
- Regression: make sure normal login still works afterwards.

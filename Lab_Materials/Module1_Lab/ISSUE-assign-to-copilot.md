# Prepared issue for Exercise 4 (assign this to Copilot / the cloud agent)

**Title:** Add input validation and error handling to the calculations module

**Body:**

The functions in `src/calculations.py` do not handle invalid input and can crash
(for example an empty list, or a `whole`/`percent_off` of zero).

**Acceptance criteria**
- Given an empty list, When `average()` is called, Then it raises a clear `ValueError`
  (not `ZeroDivisionError`).
- Given `whole == 0`, When `percentage()` is called, Then it raises a clear `ValueError`.
- Given `percent_off` outside 0-100, When `apply_discount()` is called, Then it raises a `ValueError`.
- Add unit tests covering each case; the existing tests still pass.

**Labels:** enhancement, good-first-issue

> Facilitator: create this as a real GitHub Issue in the sample repo, then assign it to
> Copilot (Assignees -> Copilot) during the lab. Keep a pre-made draft PR as a fallback.

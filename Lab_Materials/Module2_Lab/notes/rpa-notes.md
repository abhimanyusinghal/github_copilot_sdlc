# Raw notes - Automate account closure  (RPA track)
_Unstructured on purpose. Capture the process, exceptions and the human-approval rule._

- Support agents close accounts manually - about 15 minutes each, lots of steps.
- Steps: verify identity, check there are no open tickets, disable login, send a confirmation
  email, and update the CRM.
- Sometimes there are open tickets - then they pause and escalate instead of closing.
- Identity check is done in the KYC system (a separate login).
- Volume is around 40 closures a week.
- They want it "fully automated", but compliance says a human must approve the identity check.
- What happens if the CRM is down?
- The confirmation email wording must be approved by legal.

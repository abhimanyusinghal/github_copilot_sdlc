# Release readiness checklist — would you ship this?

Use this to make the go/no-go call at the end of Lab 6. It is a **release exit checklist** — the
question is not "does the pipeline run?" but "is it safe for this to reach every user?"

## Pipeline
- [ ] **Dependencies installed** and the **test suite gates** the release (Module 5's suite is the gate).
- [ ] **Actions pinned to full-length commit SHAs** — tags and branch references are mutable.
- [ ] **Least-privilege `permissions:`** declared, and you can say what each one is for.
- [ ] **No secrets** in YAML, logs, or prompts; all references go through the secret store.
- [ ] `check_pipeline.py` passes **8/8**, and you understand each check rather than pattern-matching it.

## Release safety
- [ ] **Production is protected** — a **named human** approves the deploy; no unattended agent ship.
- [ ] The production job runs only for the approved release trigger — **never for a pull request or
      ordinary push**.
- [ ] **Gradual rollout** defined (canary slice, soak window, ramp stages) with health signals.
- [ ] **Rollback path and trigger** are defined **before** deploy, and the path has been tested.
- [ ] **Risky-change signals** considered (large diff, hot files, weak coverage) and extra gates added if warranted.

## Infrastructure
- [ ] IaC reviewed like code: required **encryption controls** are explicit, **public access is blocked**,
      IAM is least-privilege, credentials are not plaintext, and backup/retention settings are adequate.
- [ ] Any credential found in code is treated as an **incident** (rotate), not a tidy-up.

## Communication
- [ ] **Release notes** generated from the merged PRs and **edited by a human**; nothing invented.
- [ ] Changes that **move reported numbers** (metric/SLA corrections) are called out to affected users.
- [ ] Security fixes are described **without** publishing an exploit recipe.

## Accountability
- [ ] Every unresolved item has an **owner** and a stated effect on the release.
- [ ] Honest status recorded: **Ship**, **Ship with stated constraints**, or **Hold** — with a reason.
- [ ] **Named human sign-off** with date and remaining risk. A blocking unknown prevents **Ship**.

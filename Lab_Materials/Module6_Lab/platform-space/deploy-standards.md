# Deploy standards — Acme Platform & Delivery
_(Attach this file to GitHub Copilot Chat in VS Code as local context. These are the rules
`check_pipeline.py` enforces.)_

## Pipeline
- **Dependencies installed** before tests run — never assume the runner has them.
- **The suite gates the release.** A red suite from Module 5 blocks the deploy. No `continue-on-error`
  on the test job.
- **Pin every action to a full-length commit SHA.** Tags such as `@v6` are convenient but mutable; a
  full SHA is GitHub's immutable pin. For this lab, the verified pins are:
  - `actions/checkout@d23441a48e516b6c34aea4fa41551a30e30af803` (`v6.1.0`)
  - `actions/setup-python@ece7cb06caefa5fff74198d8649806c4678c61a1` (`v6.3.0`)
  Keep the version in a comment so Dependabot can propose reviewed SHA updates.
- **Least privilege.** Declare an explicit `permissions:` block; start at `contents: read` and add only
  what a job needs.
- **Secrets stay vaulted.** Reference `${{ secrets.NAME }}`. Never a literal token in YAML, a log, or a
  prompt. If a secret is ever committed, rotate it — deleting the line is not enough.

## Release
- **Production is a protected environment.** The prod job declares `environment:` so a **named human**
  approves the deploy. No agent or automation ships to production unattended.
- **A PR never deploys production.** In this lab the production job runs only for a manual
  `workflow_dispatch` after merge; ordinary `pull_request` and `push` runs test only.
- **Ship gradually.** Canary first (a small traffic slice), then ramp while health metrics stay good.
  A blast radius of 1% beats a blast radius of 100%.
- **Rollback is part of the release.** Define the rollback path *and the trigger* **before** you deploy,
  make sure it has been tested, and guard an automated rollback step with `if: failure()` so it does
  not undo a healthy deployment.
- **Every release has notes** generated from the merged PRs and reviewed by a human.

## Review
- Pipeline and IaC changes are **reviewed like application code** — including the permissions they grant.
- An AI-proposed pipeline fix is read before it is accepted. A fix you didn't read is a risk you didn't measure.

_Pins and GitHub feature availability verified 2026-07-23. Re-verify action releases before a future
delivery of this course._

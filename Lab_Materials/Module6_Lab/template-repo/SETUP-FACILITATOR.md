# Facilitator setup — the template repo for Labs 6 & 7

Goal: participants each get their **own public repo** from a single **template repo** you publish once.
This keeps setup to ~2 minutes per participant and makes Actions, environments, and Dependabot work on
the free tier.

## Why public
On GitHub's **free tier**, two features these labs rely on work as follows:
- **Actions minutes** are unlimited on public repos (private repos have a monthly cap).
- **Environment protection rules** (required reviewers = the "named human approves prod" lesson) are
  available on public repos on Free; on private repos they need a paid plan.

So the practice repo **must be public**, which is fine because it contains only **fictional Acme data**.
Verify current GitHub tier details before the session — GitHub changes these periodically.

## One-time: publish the template repo
1. Create a new **public** repo on github.com, e.g. `acme-portal-lab` (an org repo is ideal).
2. Push the contents of **this `template-repo/` folder to the repo root** (so `.github/`, `src/`, etc.
   sit at the top level).
3. Repo **Settings → General → Template repository → ✅**.
4. Confirm a CI run is **red** (the publish push should trigger it; otherwise use
   **Actions → CI → Run workflow**). The workflow is broken on purpose.
5. Optional: protect `main` (Settings → Branches) so participants practise via PRs; they can also set this
   up themselves in Lab 6.

## Participant pre-work (send before the session — saves 15+ minutes)
- Create a **free github.com account** (personal is fine).
- Sign in to GitHub **from VS Code** (Accounts menu), and install the **GitHub Pull Requests and Issues**
  extension.
- Install **Python 3.11**, or plan to use the GitHub Actions runs for tests. The exercise dependency
  snapshot deliberately contains versions that do not support every newer Python runtime.
- **Do not** enable or use Copilot on github.com. BYOK models are used **only in VS Code**.

## Making a participant repo (in the lab)
Participant clicks **Use this template → Create a new repository**, sets it **Public**, then clones it and
opens it in VS Code. One repo serves **both** Lab 6 and Lab 7. If repository creation does not trigger CI,
the participant starts it with **Actions → CI → Run workflow**.

## Free-tier notes
- **Dependabot alerts** (Lab 7): under **Settings**, choose **Advanced Security** in the Security section,
  then enable **Dependabot alerts** (and optionally security updates). View results under
  **Security and quality → Dependabot → Vulnerabilities**. Alerts may take a few minutes to populate;
  the fixed scenario in `Module7_Lab/security/dependency-advisories.md` is the fallback.
- **Environment required reviewers** (Lab 6): Settings → Environments → New environment `production` →
  add the participant as a required reviewer. For the solo exercise, leave **Prevent self-review** off.
  Real production should use a second person and prevent self-review.
- **No real deploy target exists** — `scripts/deploy.sh` only echoes. Never point it at anything real.

## If github.com is blocked on lab machines
The core analysis and authoring work has an offline substitute: diagnose from the provided `failing-run.log`
(`Module6_Lab/pipeline/`), validate the workflow with `check_pipeline.py`, and use the captured
`dependency-advisories.md` for Lab 7. Participants can draft Issues, PR text, and environment settings, but
must label them simulated: hosted branch protection, PR merges, approvals, and live Dependabot results
require GitHub.

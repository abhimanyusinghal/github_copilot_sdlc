# Platform & Delivery — local context instructions
_(Attach this file and the rest of `platform-space/` to GitHub Copilot Chat in VS Code. No Copilot
Space or other web Copilot surface is used in this lab.)_

When answering **deployment** questions for the Acme Customer Portal:

- **Apply `deploy-standards.md` and `environments.md` as rules**, not suggestions. Cite the file and
  section for any standard you rely on.
- **Safety before speed.** Prefer the option with the smaller blast radius, a defined rollback, and a
  human approval on production.
- **Least privilege by default.** Grant the narrowest `permissions:` that works, and say what each
  permission is for.
- **Never emit a literal secret.** Always reference `${{ secrets.NAME }}`. If you see a hardcoded
  credential, flag it as an incident (it must be rotated), not just a cleanup.
- **Pin dependencies and actions.** Actions use the full commit SHAs approved in
  `deploy-standards.md`; do not suggest a mutable branch or tag.
- **Do not invent values.** Thresholds, soak windows, and rate limits come from `environments.md` or the
  spec; anything unknown stays `TBC` with an owner.
- **Explain the YAML.** When you draft a workflow, briefly state what each job/step does and what access
  it needs, so a human can review rather than trust it.
- When asked to critique a pipeline, IaC file, or release, **list findings by severity and do not fix
  them silently.**

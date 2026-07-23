# Operate-quality checklist — did you handle this incident well?

Use this at the end of Lab 7. The question is not "did you find an answer?" but **"would you stake a
production change on it, and will the next person be faster because of you?"**

## Diagnosis
- [ ] The root cause is stated as a **mechanism with evidence** — file, line, config key, timestamps —
      not a plausible-sounding narrative.
- [ ] You **confirmed it in the source** (code/config), not just from the AI's explanation.
- [ ] You explicitly **ruled out the noisy signals** (known, ticketed, steady-rate warnings) and can say
      why they are not the cause.
- [ ] Ranking used **impact and novelty**, not raw log count.
- [ ] The correlation to a change names the **time gap** between deploy and first error.

## Response
- [ ] The mitigation is the **smallest safe action** that restores service.
- [ ] A **named human** approves any production action; no agent acts unattended.
- [ ] Rollback safety considered (data, migrations, in-flight work).
- [ ] Recovery is **verified** against a named signal, not assumed.

## Privacy & security
- [ ] **No PII or secrets** were pasted into any prompt; log excerpts were redacted first.
- [ ] PII found in logs is raised as a **finding to fix** (NFR: no PII in logs), not worked around.
- [ ] Any exposed credential is treated as an **incident → rotate**.

## Learning
- [ ] A **runbook** exists whose confirm-steps are actually checkable by the next on-call.
- [ ] A **blameless postmortem** separates the trigger from the latent weakness.
- [ ] Preventive actions fix the **class** of problem (e.g. a contract test for config keys), each with an
      owner and a due date.
- [ ] Every timestamp and ticket reference was **verified against the source** — nothing invented.

## Sustain
- [ ] Dependency advisories triaged by **real reachability and exposure**, not badge colour.
- [ ] Unused dependencies proposed for **removal**, not just a version bump.
- [ ] Docs/runbooks updated so they stay worth reading.
- [ ] Honest status recorded: **Resolved**, **Mitigated with follow-ups**, or **Ongoing** — with owners.

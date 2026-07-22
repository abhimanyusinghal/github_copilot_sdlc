# Lab 3 · From an Agreed Spec to a Build-Ready Design

**Participant handout · Module 3 · Level 300 · Design (Architecture & UX) · Novnex**

**Time:** ~75 minutes (core exercises 0–6, including wrap-up; stretch goals if time allows)

---

## Before you start

**Where we are.** In **Lab 2** you turned messy notes into an **agreed, testable spec**. Today you
take that spec and turn it into a design that is honest about its constraints and ready for a build
decision. **Module 4 builds it**; this lab stops at a design a developer could pick up.

> **Didn't finish Lab 2? You're fine.** A pre-built spec for every track is in
> `Lab_Materials/Module3_Lab/specs/`. Use it as your Lab 2 output.

**The through-line — keep the thread alive.** Module 2's thread was
*need → story → issue → criteria → test*. Module 3 continues it:

> **Spec → Options → Grounded decision → Design-as-code → Risk → Hand-off**

**The design rule:** *ground the context, review everything — and AI proposes; the architect decides
and records why.* Copilot widens your options and pressure-tests them. **You** make the call against
the real constraints and record the reasoning.

**By the end you'll be able to:**

- Generate and compare 2–3 design options with real trade-offs.
- Ground a decision in local architecture, standards, glossary, and past ADR files.
- Produce a Mermaid diagram plus the contract or model appropriate to your track.
- Run a STRIDE risk pass and make a mitigation visible in the design.
- Draft a **Proposed** ADR without overwriting accepted architecture records.
- Assemble a traceable hand-off and give it an honest readiness status.
- Catch four design failure modes: **plausible-but-wrong, over-engineering, undocumented decisions,
  and security-as-an-afterthought**.

### Tool boundary for this lab

All Copilot work happens in **GitHub Copilot inside VS Code**. Do not use Copilot on github.com,
Copilot Spaces, GitHub Spark, the Copilot CLI, a background agent, or a Copilot cloud agent. Keep the
chat/agent session local to the open VS Code workspace.

Creating a normal GitHub Issue is allowed. The optional issue step uses the **GitHub Pull Requests and
Issues** extension in VS Code; Copilot drafts the text in VS Code, and you submit it. A first-time
GitHub sign-in may open an authentication page, but no web Copilot feature is used.

### You'll need

- **VS Code 1.121 or later**, which renders Mermaid in its built-in Markdown preview. Check with
  **Help → About** (Windows/Linux) or **Code → About Visual Studio Code** (macOS). If your organization
  pins an older VS Code release, the facilitator must preinstall and test the legacy
  **Markdown Preview Mermaid Support** extension (`bierner.markdown-mermaid`) before the lab.
- A GitHub account with **GitHub Copilot enabled**, signed in from VS Code.
- **Copilot Chat** in VS Code. Use a local **Agent** session when it is available. If your organization
  disables Agent mode, use Copilot Chat in Ask mode and create/save the requested files manually; every
  core learning step still works.
- A writable local clone of this repository, opened at the repository root so that both
  `Module3_Lab_Design.md` and `Lab_Materials/Module3_Lab/` are visible in Explorer.
- Optional, only for creating the hand-off Issue: **GitHub Pull Requests and Issues**
  (`GitHub.vscode-pull-request-github`), signed in to a repository with Issues enabled.
- For the Web/Drupal track, a YAML extension approved by your organization is useful for validating
  the OpenAPI draft. It is not required for the other tracks.

> **Privacy:** use only the fictional Acme materials. Do not attach production data, credentials,
> customer PII, or confidential documents to Chat.

### Lab materials

- `specs/` — one pre-built input spec per track.
- `architecture-space/` — a **local context pack**. The folder keeps its course name, but it does not
  require or use the Copilot Spaces web feature.
  - `SPACE-instructions.md`
  - `architecture-overview.md`
  - `tech-radar.md`
  - `nfr-standards.md`
  - `glossary.md`
  - `design-readiness-checklist.md`
  - `past-ADRs/`
- `adr-template.md` — the shape for a Proposed ADR.
- `mermaid-smoke-test.md` — a known-good diagram for the setup check.

**Tracks:** choose **Web/Drupal, Data & Analytics, Power BI, QA, or RPA**. Use one output folder so
files from different participants or tracks do not collide:

| Track | Spec | Output folder |
| --- | --- | --- |
| Web / Drupal | `web-drupal-spec.md` | `design/web/` |
| Data & Analytics | `data-analytics-spec.md` | `design/data/` |
| Power BI | `power-bi-spec.md` | `design/power-bi/` |
| QA | `qa-spec.md` | `design/qa/` |
| RPA | `rpa-spec.md` | `design/rpa/` |

In every prompt, replace angle-bracket placeholders such as `<track>`, `<artifact>`, and `<decision>`
with your real value before sending. Do not create folders whose names literally contain angle brackets.

If participants share a repository, each person or pair should work on a separate branch.

---

## Exercise 0 · Pre-flight and load the spec  (7 min)

**Goal:** prove the local toolchain works before doing design work.

**Steps**

1. Open the repository root in VS Code and open **Copilot Chat**. Start a new local Chat session and
   select **Agent** if your organization enables it.
2. Pick your track. Open its spec from `Lab_Materials/Module3_Lab/specs/`.
3. Open `Lab_Materials/Module3_Lab/mermaid-smoke-test.md`, then run
   **Markdown: Open Preview to the Side** (`Ctrl+K V` on Windows/Linux or `Cmd+K V` on macOS).
   Confirm that you see a rendered three-box diagram, not a literal code block.
4. In Chat, use **Add Context** to attach your spec. You can also type `#` and select the file, or drag
   the file from Explorer into Chat. Ask:

   > State the title of the attached spec and list its explicit open questions. Do not edit any files.

5. Confirm the answer against the spec. Create your track's output folder from the table above. In
   Agent mode you may ask Copilot to create **only** that empty folder; otherwise create it in Explorer.
6. Open the files in `architecture-space/` and skim the two accepted records in `past-ADRs/`. Do not
   edit these source materials during the lab.

**What you should see:** the correct spec title/open questions, a rendered Mermaid smoke test, and an
empty output folder for your track.

> **✅ Checkpoint:** Context attachment and local Mermaid preview both work before you continue.

---

## Exercise 1 · Spec → ungrounded options  (9 min)

**Goal:** expose what a plausible answer looks like before Copilot sees your architecture constraints.

**Steps**

1. Start a fresh Chat session and attach **only your spec**. Do not attach the architecture context pack
   yet; this deliberate first pass gives you something to compare in Exercise 2.
2. Paste the prompt below. Do not let Agent edit files on this first request.
3. Challenge at least one option. Ask: *What breaks at 10× load? Where is the single point of failure?
   What assumption most threatens this option?*
4. Save the result as `design/<track>/01-options-ungrounded.md`. Label it **Ungrounded draft — not a
   decision**.

**Paste this prompt:**

> Using only the attached spec, propose exactly **3 distinct design options** for the design deliverable
> named by the spec. For each option, give a one-line sketch and trade-offs in **complexity, cost,
> scalability, team fit, security, and reversibility**. Recommend one provisionally. Separate facts from
> assumptions and open questions. Do not invent values for anything marked `TBC`. Do not edit files.

**What you should see:** three meaningfully different options, an explicitly provisional recommendation,
and visible assumptions rather than hidden guesses.

> **✅ Checkpoint:** You found at least one unsupported assumption or weak trade-off. You have **not**
> made the architecture decision yet.

---

## Exercise 2 · Ground, compare, and decide  (10 min)

**Goal:** make the decision only after applying the actual systems, standards, and past decisions.

**Steps**

1. Start another fresh Chat session. Attach:
   - your spec;
   - `01-options-ungrounded.md`;
   - all six top-level files in `architecture-space/`; and
   - the `past-ADRs/` folder (or attach both ADR files individually).
2. Paste the prompt below. Check every cited claim in the named source file.
3. Compare the grounded result with the ungrounded draft. Identify at least one concrete change, such
   as reusing Auth/Email, respecting nightly refresh, or rejecting a new microservice under ADR-002.
4. **You decide.** Save `design/<track>/02-grounded-decision.md` with:
   - the selected option and 1–2 sentence rationale;
   - why the other options were rejected;
   - the source constraints that drove the choice;
   - assumptions and unresolved questions; and
   - one sentence written or materially edited by you.

**Paste this prompt:**

> Re-evaluate the three options using the attached local architecture context. Treat
> `SPACE-instructions.md` as instructions. Honour the accepted ADRs, apply the NFR checklist and tech
> radar, and use glossary terms exactly. Cite the **filename and section** for every constraint or past
> decision you rely on. Call out any conflict with the spec. Recommend an option, but do not make the
> decision for me and do not edit files.

**What you should see:** a recommendation that fits the existing environment and explains exactly what
the local context changed.

> **✅ Checkpoint:** The recorded decision follows the grounded pass, cites real files, and preserves
> unresolved `TBC` items instead of guessing them.

---

## Exercise 3 · Diagram as code  (10 min)

**Goal:** turn the grounded decision into a reviewable diagram stored as text.

Use the diagram type for your track:

| Track | Required Mermaid view | Critical content |
| --- | --- | --- |
| Web / Drupal | `sequenceDiagram` | Portal, Auth, Email, token expiry/reuse, neutral response, failure path |
| Data & Analytics | `flowchart` | sources → validation/quarantine → transform → warehouse → semantic layer; nightly publish gate |
| Power BI | `flowchart` | warehouse → semantic model/RLS → report; refresh and access boundary |
| QA | `flowchart` | unit/API/E2E/manual layers plus repeatable test-data setup/teardown |
| RPA | `flowchart` | KYC + human approval + open-ticket gate + Auth/Email/CRM and exception paths |

**Steps**

1. Attach the spec, `02-grounded-decision.md`, and the local context files relevant to the flow.
2. Ask Copilot to create **only** `design/<track>/03-design-diagram.md` using the prompt below. If using
   Ask mode, paste the result into that file yourself.
3. Open Markdown preview to the side. Fix any Mermaid syntax error in the source file.
4. Trace the main path and at least one failure path against the spec. A diagram that renders but omits
   a constraint is still wrong.

**Paste this prompt:**

> Create the required Mermaid view for my track from the attached grounded decision and spec. Put one
> diagram in a fenced `mermaid` block. Use only broadly supported Mermaid syntax: `sequenceDiagram`,
> `flowchart`, or `erDiagram`; simple node IDs; and quoted labels where punctuation is needed. Do not use
> experimental C4 syntax, icons, themes, or external assets. Show trust boundaries, relevant failure
> paths, and explicit constraints. Preserve `TBC` values. Create or update only
> `design/<track>/03-design-diagram.md`; do not implement code.

**What you should see:** a diagram that renders in VS Code and names the real systems and constraints for
your track.

> **✅ Checkpoint:** The diagram renders locally and a human can trace its main and failure paths back to
> the spec.

---

## Exercise 4 · Create the track contract or model  (12 min)

**Goal:** produce the core design artifact that constrains the later implementation.

| Track | Output | You must check |
| --- | --- | --- |
| **Web/Drupal** | `04-openapi.yaml` + `04-component-structure.md` | Same externally observable response for known/unknown emails; `429` behavior without inventing the threshold; Auth reuse; expiry/reuse; dependency failure responses |
| **Data & Analytics** | `04-data-model.md` + `04-source-to-semantic.md` | Ticket grain and keys; 30-day login definition; team × channel × day output; quarantine; PII; nightly, all-or-nothing publish |
| **Power BI** | `04-semantic-model.md` | Fact grain; conformed dimensions; business-calendar dependency; SLA measure; team RLS in the model; data-as-of timestamp |
| **QA** | `04-test-architecture.md` | Every scenario mapped to an automated or manual layer; security cases at API level; accessibility includes manual validation; repeatable synthetic data; no invented password/rate-limit policy |
| **RPA** | `04-process-contract.md` | Inputs/outputs; human approval; open-ticket stop; least privilege; idempotency; partial failure after Auth/Email/CRM steps |

**Steps**

1. Attach the spec, grounded decision, rendered diagram, NFR standard, tech radar, and relevant accepted ADRs.
2. Adapt the prompt below to the output in the table. Allow Agent to create **only** the named file(s).
3. Review against every item in the last column. Ask Copilot for a separate critique, then verify it
   yourself against the sources.
4. Keep unresolved policy values as `TBC` with an owner. A plausible number invented by Copilot is not a
   design decision.
5. For Web/Drupal, inspect the VS Code **Problems** panel if a YAML/OpenAPI-aware extension is available.
   If no validator is available, label the artifact **Draft — syntax/schema not machine-validated** in
   `04-component-structure.md`; do not claim validation happened.

**Prompt pattern:**

> From the attached spec and grounded decision, draft `<artifact>` for the `<track>` design. Apply the
> attached NFRs and accepted ADRs. Include source references, explicit error/exception behavior, and a
> section called **Open decisions** with the owner of each `TBC`. Do not invent policy values and do not
> implement the feature. Create or update only `<exact output path(s)>`.

**Web/Drupal example:**

> Draft an OpenAPI 3.1 contract for the password-reset endpoints plus a Drupal component/module structure.
> Reuse the central Auth service under ADR-001. For reset requests, known and unknown emails must have
> the same externally observable response; include rate-limit behavior but leave its threshold
> `TBC with Security`.
> Cover expired/used tokens and Auth/Email dependency failures. Create only
> `design/web/04-openapi.yaml` and `design/web/04-component-structure.md`.

> **✅ Checkpoint:** The artifact is saved, source-grounded, and checked for the track-specific failure
> modes. Any validation you could not perform is stated explicitly.

---

## Exercise 5 · Risk pass and Proposed ADR  (12 min)

**Goal:** change the design in response to a real threat, then record the decision without pretending it
has already been approved.

**Steps**

1. Attach the spec, diagram, contract/model, grounded decision, and NFR standard. Ask:

   > Run a STRIDE pass over the attached design and its trust boundaries: spoofing, tampering,
   > repudiation, information disclosure, denial of service, and elevation of privilege. For each
   > applicable threat, identify the affected asset/flow, evidence in the design, likelihood, impact,
   > and a design-time mitigation. Mark non-applicable categories with a reason. Rank the highest risk.
   > Do not edit files and do not treat guesses as facts.

2. Verify the threats against the actual flow. Save the reviewed result as
   `design/<track>/05-threat-model.md`.
3. Pick one credible threat. Update the diagram or contract/model so its mitigation is visible. Examples
   include hashed single-use reset tokens, model-enforced RLS, synthetic test data, least-privilege bot
   identities, or idempotency/compensation for a partial failure.
4. Copy `Lab_Materials/Module3_Lab/adr-template.md` to
   `design/<track>/06-adr-proposed.md`. Ask Copilot to draft one **single** decision from your discussion.
   Keep its status **Proposed**.
5. Edit at least one substantive line yourself. Do **not** add the lab ADR to `past-ADRs/`, reuse an
   existing ADR number, or mark it Accepted; that requires the team's real review process.

**ADR prompt:**

> Draft one concise Proposed ADR for the decision to `<decision>`. Include context, considered options,
> decision, positive and negative consequences, the highest relevant risk, and source-file references.
> Preserve unresolved questions. Update only `design/<track>/06-adr-proposed.md`.

**What you should see:** one mitigation reflected in the actual design and a Proposed ADR whose trade-off
you personally reviewed and edited.

> **✅ Checkpoint:** The risk pass caused a visible design change, and the ADR records one decision with
> an honest approval status.

---

## Exercise 6 · Assemble, critique, and hand off  (10 min)

**Goal:** make readiness traceable instead of simply declaring the design “build-ready.”

**Steps**

1. Attach your spec and every reviewed file in `design/<track>/`. Ask Copilot to create only
   `design/<track>/07-handoff.md` with:
   - scope and chosen design;
   - links to the diagram, contract/model, threat model, and Proposed ADR;
   - an acceptance-criterion coverage matrix (**criterion → design evidence → gap/open decision**);
   - NFR targets and risk mitigations;
   - assumptions, `TBC` items, owner, and the decision needed;
   - a suggested build sequence; and
   - readiness: **Ready**, **Ready with stated constraints**, or **Blocked**, with a reason.
2. Ask Copilot to critique the package against
   `architecture-space/design-readiness-checklist.md`. Tell it to list gaps and **not fix them silently**.
3. Verify every link and every coverage row yourself. Fix genuine gaps in the source artifact, then update
   the hand-off so the package remains consistent.
4. Add a human sign-off line with your name/initials, date, readiness status, and remaining risk. Do not
   choose **Ready** while a blocking policy or interface decision is still `TBC`.
5. **Optional GitHub Issue, still from VS Code:** ask Copilot Chat to draft an issue title and body from
   `07-handoff.md`. Review the draft, then use the **+** button in the extension's Issues view to submit it
   to your GitHub repository. Link the versioned hand-off rather than pasting contradictory copies of all
   artifacts. If the extension, remote, or Issues permission is unavailable, skip this optional step.

**Critique prompt:**

> Critique this package against the attached design-readiness checklist and spec. Check every acceptance
> criterion, standard, accepted ADR, diagram/contract consistency, threat mitigation, relative link, and
> unresolved decision. List gaps by severity and cite the affected file. Do not edit anything.

**What you should see:** a short, navigable design package and a defensible readiness decision—not an
automatic claim that unfinished work is ready.

> **✅ Checkpoint:** You can trace **spec → options → grounded decision → design-as-code → risk → hand-off**,
> and every unresolved item has an owner and an honest effect on readiness.

---

## Wrap-up  (5 min)

Talk it over with the person next to you:

- Which design task would you trust Copilot to accelerate, and which decision stays firmly human?
- What changed only after you added local architecture context?
- Which `TBC` item blocks implementation, and who owns the decision?
- How will your team move a Proposed ADR through review without losing the reasoning in Chat?

---

## Your deliverables checklist

1. ☐ `01-options-ungrounded.md`, clearly marked as a draft.
2. ☐ `02-grounded-decision.md`, with source citations and your rationale.
3. ☐ `03-design-diagram.md`, rendered and manually traced.
4. ☐ Track-specific `04-*` contract/model file(s), with validation status stated.
5. ☐ `05-threat-model.md` plus one mitigation visible in the design.
6. ☐ `06-adr-proposed.md`, kept Proposed and substantively edited by you.
7. ☐ `07-handoff.md`, with criterion coverage, open-decision owners, and human readiness sign-off.
8. ☐ Optional: a GitHub Issue created from VS Code that links the hand-off.

---

## Stretch goals — VS Code Copilot only

- **Local UX sketch:** for Web/Drupal, attach the spec or Lab 2 wireframe and ask the local Agent to create
  a static `design/web/prototype.html` with no external assets or production code. Preview it with VS Code's
  built-in HTML preview. Treat it as a review sketch, not the product.
- **Alternative diagram:** generate a second standard Mermaid view and check whether it exposes a risk the
  first diagram hid.
- **One-way doors:** ask which decisions are hard to reverse, then add the answer to the Proposed ADR.
- **Simplicity pass:** ask Copilot to critique coupling and over-engineering and identify the smallest
  design that still meets every criterion.
- **Issue quality:** have Copilot critique the optional GitHub Issue against `07-handoff.md`, then correct
  any loss of intent before submission in VS Code.

---

## Troubleshooting

- **Agent mode is missing or disabled:** stay in Copilot Chat Ask mode and create/edit the files manually.
  Do not switch to a cloud or third-party agent.
- **Copilot used the wrong file:** remove the attachment and use **Add Context** to select the exact file.
  Open the repository root, not only `Lab_Materials/Module3_Lab/`.
- **The answer is generic:** start a fresh chat and attach the spec plus the complete local context pack
  listed in Exercise 2.
- **A source citation is wrong:** the file—not Copilot—is authoritative. Correct the output and record the
  mismatch as a plausible-but-wrong failure mode.
- **Mermaid shows as code:** confirm VS Code 1.121+, use a `.md` file with a fenced `mermaid` block, and run
  **Markdown: Open Preview to the Side**. If your organization pins an older release, use the facilitator's
  pretested `bierner.markdown-mermaid` fallback. Reopen `mermaid-smoke-test.md` to separate setup failure
  from generated-syntax failure.
- **Mermaid reports a syntax error:** ask Copilot to simplify to `sequenceDiagram`, `flowchart`, or
  `erDiagram`; remove experimental C4 syntax, icons, themes, HTML labels, and external assets.
- **Copilot changed unrelated files:** review the proposed edits and discard only the unrelated hunks.
  Re-prompt with the exact allowed output path before continuing.
- **A policy value is unknown:** leave it `TBC`, name the owner, and mark the hand-off Conditional or Blocked
  if implementation cannot safely proceed without it.
- **OpenAPI was not validated:** do not say it passed. Record **not machine-validated** and have the owning
  team validate it before implementation.
- **GitHub Issue creation is unavailable:** confirm the optional extension is signed in, the repository has
  a GitHub remote and Issues enabled, and your account has permission. Otherwise keep the local hand-off;
  issue creation is not a core checkpoint.
- **The ADR looks final:** reset its status to Proposed and keep it in `design/<track>/`; accepted ADRs belong
  in `past-ADRs/` only after real review.

---
name: design-system
description: Project start-off skill, run once per UI project after /agents-md and setup; re-run `extend` as the design grows or to fold a shipped page's UI back into the library. Turns a provided design system — a Figma file, written spec/brand guide, reference screens, or a guided-definition session — into named tokens, a real UI library, a verifiable preview page, docs under docs/design-system/, and a short binding AGENTS.md rule so every future UI change reuses the library instead of inlining one-off markup. Stack-adaptive via the Project Matrix. A design-system source is required — never fabricated. Never auto-chains.
---

# Design System

## Purpose

A Workflow-A (project start-off) skill. It turns a project's design system into things that make every later UI task correct by default:

1. a real **UI library** (tokens + reusable components) in the target's stack idiom,
2. a **preview page** the user can eyeball to verify it,
3. **documentation under `docs/design-system/`** (the durable record — source, tokens, component inventory, rules), and
4. a short **binding reference in AGENTS.md** so that on **any UI change**, every future agent checks the library first — reusing what exists, building what's missing from the reference, or asking for a reference — instead of inlining one-off markup.

Run it once per project, after `/agents-md` → `/setup-matt-pocock-skills` → placeholder fill. Re-run it (`extend` mode) whenever the design system grows, a UI change needs a component the library lacks, or a page/feature ships and its emergent UI should flow back into the library.

## Prerequisites

- The workspace already has a binding `AGENTS.md` with a Project Matrix (from `/agents-md`) and setup decisions incl. the docs location (from `/setup-matt-pocock-skills`). If the Project Matrix is missing, stop and route to `/agents-md` first.
- The target's stack is read from the Project Matrix / `AGENTS.md`. Do not guess it.

## Inputs

Infer first from the request and cheap repo evidence; interview the user — the way `/feature-prompt` does — only for what's genuinely missing:

- **TARGET PROJECT-CODE** — full Project Matrix code. Determines the output idiom. Never abbreviate or invent it.
- **DESIGN-SYSTEM SOURCE (required)** — one of:
  - a **Figma** file/URL — read it via the Figma MCP companion (frames, components, tokens);
  - a **written design spec / brand guide**;
  - existing **reference screens or a reference app**;
  - if none exists, a **guided-definition session**: walk the user through brand/primary colours, neutrals, typography families, type scale, spacing scale, radius, shadow, and the base component set, and end in **explicit user approval** before building.
  - **Never fabricate a whole design system silently.** No source and no approved guided session → stop and ask.

If the Figma MCP is not installed, say so and fall back: ask the user to export the relevant frames/tokens or provide a written spec. Do not assume a companion is present.

## Stack-adaptive output

Read the target's stack from the matrix / `AGENTS.md`, then emit in that idiom. Do **not** hardcode Laravel or any one framework:

- **Framework web** (Laravel/Livewire, Rails, Django templates, etc.): components in the framework's component idiom + a **server-rendered preview route** (e.g. `/ui/preview/all`).
- **React Native**: a component library + a **preview screen**.
- **Plain / static PHP or HTML**: plain HTML/CSS components + a **static preview HTML file**.

For anything not listed, map to the closest of these three by how the target renders UI.

## Rules (non-negotiables)

- **Suggest, never auto-chain.** After `bootstrap`, suggest verifying the preview and then beginning Workflow B. Then stop. Never start feature work here.
- **Design-system source is required.** The guided-definition path must end in explicit user approval before any component is built. A new component always traces to a reference — if none exists, **ask the user for one**; never invent it.
- **Decisions are artifacts.** Tokens, library, preview, the `docs/design-system/` doc, the AGENTS.md reference, and the seeded project skill all live on disk — not in chat.
- **AGENTS.md holds a reference only.** The full design-system documentation lives under the configured docs location (`docs/design-system/`); AGENTS.md points to it and states the binding rule. Keep the AGENTS.md entry terse, the way `/agents-md` structures that file.
- **On any UI change, the library is checked first.** The binding reference routes every UI fix/change through the library: reuse an existing component; if it's missing, build it via `/design-system` (extend) from the design-system source; if no reference exists for that component, ask the user for one. Never inline a one-off, never fabricate a component without a reference.
- **Name the full PROJECT-CODE** from the Project Matrix everywhere. Never carry one project's conventions, tokens, or components into another; adapt to the target stack.
- **Verification is the preview page, eyeballed by the user.** Building the library is not "done" until the preview renders and the user has looked at it. Per-page pixel conformance *during feature work* is `/pixel-audit`'s job — reference it, do not duplicate it here.
- **Never hardcode locations.** Resolve artifact and docs paths from the target's stack conventions and the setup decisions; record the real paths in the doc, the AGENTS.md reference, and the project skill.
- **Emit `Stage / Found / Next / Needs user`** at each phase transition.
- **Local-only.** Read-only sub-agents for extraction/survey are fine; the main agent owns synthesis. No cloud agents.

## Modes

### bootstrap (default)

Full first run. Produce the artifacts in order:

1. **Extract the design system** from the source (Figma via MCP, spec, reference screens, or the approved guided session). Capture the token set and the base component list with their states.
2. **Theme / tokens** — write colours, typography, spacing, radii, and shadows as **named tokens** in the stack's native mechanism (CSS variables, Tailwind config `theme`, an RN theme object, etc.). Named, not hardcoded per use.
3. **UI library** — build the base reusable components (buttons, inputs, selects, checkboxes/toggles, cards, alerts, badges, form sections, headings, …) faithfully to the source, built **from the tokens**, in the target's component idiom.
4. **Preview page** — one page/route/screen that renders **every** component in its states: default, hover, focus, disabled, active; empty/loading/error where relevant; responsive. This is the verification gate. Show the user how to open it and wait for them to eyeball it.
5. **Document** the design system under `docs/design-system/` (see template), **add the short reference to AGENTS.md** (see template), and **seed the project skill** (see below).

### extend (re-run)

Three triggers:

- the design system grew (e.g. a new component from Figma);
- a UI change needs a component the library lacks;
- **post-development feedback loop** — a page or feature just shipped and its UI should flow back into the library.

**On a UI change that needs a component (before/during development):**

1. **Check the library first** for the needed component.
2. If it **exists**, there's nothing to build — the feature reuses it; stop and say so.
3. If it's **missing**, build it from the design-system source. If no reference covers it, **ask the user for a reference before building** — do not invent it.

**Post-development feedback loop (after a page/feature ships):**

1. Review the finished page's **diff** for UI that emerged or changed — new reusable components, altered tokens, new patterns or states.
2. **Promote** each reusable piece into the library (build it from the shipped UI plus the design-system source).
3. Leave **page-local one-off UI in place only when it's documented with a reason**, per the project skill's reuse-vs-new rule.

This subsumes the old "update the UI library after landing" step.

**Always keep in sync.** Whichever trigger fired, update the **library, preview, `docs/design-system/` doc, AGENTS.md reference, and project `*-ui-coding` skill together** — a promoted or changed component must render in the preview and appear in the doc and project skill in the same pass.

**Boundary — design system only.** `extend` updates the design system and nothing else. It does **not** commit, push, write ADRs, or produce handovers; those stay `/grill-with-docs` and `/commit-push-*`, invoked separately per suggest-never-auto-chain. It is the same skill the binding rule calls into on a UI change.

## Documentation & registration

### The `docs/design-system/` doc (the durable record)

Write the full documentation to the configured docs location — resolve it from setup / `<artifacts-root>`, do **not** hardcode:

```text
<docs-root>/design-system/<TARGET-PROJECT-CODE>-design-system.md
```

```markdown
# Design System — <TARGET-PROJECT-CODE>

- **Source:** <Figma URL | spec doc | reference app | guided-definition (approved <date>)>
- **Stack:** <from the Project Matrix>
- **Tokens:** <path + mechanism — e.g. resources/css/tokens.css (CSS vars) / tailwind.config.js theme / src/theme.ts>
- **Library:** <path where the components live>
- **Preview:** <preview route or file — the verification gate>
- **Project skill:** <project-slug>-ui-coding

## Tokens
<colour / typography / spacing / radius / shadow token groups and names>

## Components
| Component | States | Notes |
| --------- | ------ | ----- |
| Button | default/hover/focus/disabled/active | primary, secondary, ghost |
| ... | ... | ... |

## Consumption rule
On any UI change: check this library first → reuse an existing component; if missing, add it via `/design-system` (extend) from the source, or ask the user for a reference when none exists → never inline a one-off. Per-page pixel conformance is `/pixel-audit`.

## Deviations
<any place the build departs from the source, and why>
```

### The AGENTS.md reference (short, binding, PROJECT-CODE-keyed)

Add only a terse reference into the binding `AGENTS.md`, integrated the way `/agents-md` structures that file. Update the subsection in place on `extend`; never duplicate it. **Do not put the full design system in AGENTS.md** — it points to the doc:

```markdown
## Design System / UI Library

Per project. When building or changing UI for a listed project, consume its UI library and tokens — never inline markup the library covers. Full docs under `docs/design-system/`.

### <TARGET-PROJECT-CODE>

Design system: `<docs-root>/design-system/<TARGET-PROJECT-CODE>-design-system.md` · Preview: `<preview location>` · Project skill: `<project-slug>-ui-coding`.

**On any UI change:** check the `<TARGET-PROJECT-CODE>` library first. Reuse the component if it exists. If it's missing, add it via `/design-system` (extend) from the design-system source; if no reference exists for it, ask the user for one. Never inline a one-off. Per-page pixel conformance is `/pixel-audit`.
```

### Seed the project `<project>-ui-coding` skill

This project skill is the **deep, project-specific reference** an implementer opens when doing real UI work. It can grow large and hand-grown over time (component inventory, project rules, high-frequency gotchas, ADR trail). Keep the division of labour clear: the always-on "check the library first" trigger lives in the AGENTS.md reference above; **all project-specific rules — naming, allowed/forbidden patterns, per-project conventions, token names, component lists — live in this skill and the `docs/design-system/` doc, never hardcoded into `/design-system` itself.** `/design-system` is generic machinery; this seeded skill is where a project's own UI law is written.

Create a **project-local** operational skill named `<project-slug>-ui-coding` (kebab-case, matching the target's existing project naming — e.g. `admin-web-ui-coding` for `ADMIN-WEB`) in the project's local skills directory. It captures the operational rules an implementer needs:

- where the tokens, library, preview, and design-system doc live (the real paths);
- the base component inventory and their states;
- **reuse-before-new** discipline: on any UI change, check the library first; extend an existing component before adding a parallel one; no one-off UI unless documented and justified;
- how a missing component is added (via `/design-system` extend, from the reference — ask the user for a reference if none exists) and that the preview must render it;
- the binding "consume the library, never inline covered markup" rule, pointing back to the AGENTS.md reference and the `docs/design-system/` doc.

**If the project already has a `<project>-ui-coding` skill (e.g. a mature project), detect it and UPDATE it — merge the new rules/paths in. Never overwrite hand-grown conventions.** Show the diff of what you'd change and keep the project's existing voice.

Minimal seed frontmatter + shape (match the kit's skill format):

```markdown
---
name: <project-slug>-ui-coding
description: UI-coding rules for <TARGET-PROJECT-CODE> — on any UI change, consume the design-system library and tokens; reuse existing components, extend from the reference for missing ones, never inline covered markup. Docs: docs/design-system/<TARGET-PROJECT-CODE>-design-system.md.
---

# <TARGET-PROJECT-CODE> UI Coding

- Tokens: <path/mechanism> · Library: <path> · Preview: <route/file> · Docs: <doc path>
- On any UI change: check the library first; reuse before new; promote repeated markup to the library; no undocumented one-offs.
- Add/change a component only via /design-system (extend), from the reference (ask the user if none), then verify it in the preview.
```

## Output

After `bootstrap` (or `extend`):

- **Suggest the next step and stop.** Recommend the user open the preview and eyeball it; once verified, begin Workflow B (`/feature-prompt` → `/grill-with-docs` → …) for the first feature, which will now consume the library.
- **Emit the phase update:**

```markdown
Stage: design-system (<bootstrap|extend>) — built tokens + library + preview for <TARGET-PROJECT-CODE>; wrote docs/design-system/<TARGET-PROJECT-CODE>-design-system.md; added AGENTS.md reference; seeded/updated <project-slug>-ui-coding.
Found: <N> tokens, <M> components (<states covered>); source = <Figma|spec|reference|guided(approved)>; stack = <from matrix>.
Next: open <preview location> and eyeball every component/state; then start Workflow B for the first feature.
Needs user: verify the preview, and confirm any guided-definition choices or DS/stack deviations.

Suggested next skills (optional):
- Open the preview and verify it (the human gate).
- /feature-prompt: begin the first feature — it will consume this library.
- /pixel-audit: for per-page pixel conformance during that feature work (not here).
```

Do not proceed past the suggestion.

## Checklist

Before finishing:
- [ ] TARGET PROJECT-CODE known; stack read from the Project Matrix / `AGENTS.md` (not guessed)
- [ ] A real design-system source was used (Figma / spec / reference / guided-definition **approved by the user**) — nothing fabricated silently
- [ ] Tokens written as named values in the stack's native mechanism (not hardcoded per use)
- [ ] UI library built from the tokens, in the target's idiom, faithful to the source
- [ ] Preview renders every component in its states (default/hover/focus/disabled/active; empty/loading/error; responsive) — the stack-appropriate kind (route vs screen vs static file)
- [ ] User was shown how to open the preview and asked to eyeball it (verification gate)
- [ ] Full documentation written to `<docs-root>/design-system/<TARGET-PROJECT-CODE>-design-system.md`
- [ ] AGENTS.md holds only a short PROJECT-CODE-keyed **reference** to that doc + the binding "on any UI change, check the library first" rule — not the full design system; updated in place on `extend`
- [ ] `<project-slug>-ui-coding` project skill seeded, or an existing one updated (never overwritten)
- [ ] `extend` kept library + preview + doc + AGENTS.md reference + project skill in sync; a missing component was built from a reference (asked the user when none existed), never invented
- [ ] Post-development feedback loop (when that trigger fired): reviewed the shipped page's diff; promoted emergent reusable UI into the library; left page-local one-offs only when documented with a reason
- [ ] `extend` updated the design system only — no commit, push, ADR, or handover (those stay `/grill-with-docs` and `/commit-push-*`)
- [ ] No conventions carried in from another project; `/pixel-audit` referenced, not duplicated
- [ ] Suggested the next step and stopped — no auto-chain, no feature work started
- [ ] `Stage / Found / Next / Needs user` emitted

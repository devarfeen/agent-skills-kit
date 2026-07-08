---
name: design-system
description: Project start-off skill, run once per UI project after /agents-md and setup; re-run `extend` as the design grows or to fold a shipped page's UI back into the library. Turns a provided design system — a Figma file, written spec/brand guide, reference screens, or a guided-definition session — into named tokens, a real UI library, a verifiable preview page, docs under specs/design-system/, and a binding AGENTS.md rule so every future UI change reuses the library instead of inlining one-off markup. Stack-adaptive via the Project Matrix. A design-system source is required — never fabricated. Never auto-chains.
---

# Design System

## Purpose

A Workflow-A (project start-off) skill. It turns a project's design system into things that make every later UI task correct by default:

1. a real **UI library** (tokens + reusable components) in the target's stack idiom,
2. a **preview page** the user can eyeball to verify it,
3. **documentation under `specs/design-system/`** (the durable record — source, tokens, component inventory, rules),
4. a short **binding reference in AGENTS.md** so every future UI change routes through the library, and
5. a seeded — or, when the project already has a UI skill, **adopted and extended** — **project UI skill** so later UI work loads the library-first rules automatically.

Run it once per project, after `/agents-md` → `/setup-matt-pocock-skills` → placeholder fill. Re-run it in `extend` mode when one of its three triggers fires (see extend below).

**Not this skill.** Building the library is this skill; consuming it to make one page match its design pixel-for-pixel is `/pixel-audit`; a scattered cosmetic QA tail is `/polish-batch`; bringing a feature (and its UI) over from a reference stack is `/port-feature`; tracing how existing UI works is `/feature-discovery`.

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

## Conventions

These bind in every mode; the mode sections below own their remaining rules where they apply:

- **Name the full PROJECT-CODE** from the Project Matrix everywhere. Never carry one project's conventions, tokens, or components into another; adapt to the target stack.
- **Decisions are artifacts.** Tokens, library, preview, the `specs/design-system/` doc, the AGENTS.md reference, and the seeded project skill all live on disk — not in chat.
- **Never hardcode locations.** Resolve artifact and docs paths from the target's stack conventions and the setup decisions; record the real paths in the doc, the AGENTS.md reference, and the project skill.
- **Local-only.** Read-only sub-agents for extraction/survey are fine when the user has allowed them; the main agent owns synthesis. No cloud agents.
- **Emit `Stage / Found / Next / Needs user`** at each phase transition.
- **Suggest, never auto-chain.** Recommend the next step and stop. Never start feature work here.

## Modes

### bootstrap (default)

Full first run. If the target already has a design-system doc or library, this is not a first run — switch to `extend` and update in place instead of rebuilding over it. Produce the artifacts in order:

1. **Extract the design system** from the source (Figma via MCP, spec, reference screens, or the approved guided session). Capture the token set and the base component list with their states. The guided-definition path must end in explicit user approval before any component is built.
2. **Theme / tokens** — write colours, typography, spacing, radii, and shadows as **named tokens** in the stack's native mechanism (CSS variables, Tailwind config `theme`, an RN theme object, etc.). Named, not hardcoded per use.
3. **UI library** — build the base reusable components (buttons, inputs, selects, checkboxes/toggles, cards, alerts, badges, form sections, headings, …) faithfully to the source, built **from the tokens**, in the target's component idiom.
4. **Preview page** — one page/route/screen that renders **every** component in its states: default, hover, focus, disabled, active; empty/loading/error where relevant; responsive. This is the verification gate, in two halves:
   - **Agent half — evidence first.** Build/serve the target, load the preview (agent-browser screenshot, or at minimum fetching the served HTML / rendered file — a status code alone can't show components), and compare what rendered against the extracted component inventory: every component appears, no error output. Quote the evidence (URL or file, status, screenshot path, components counted).
   - **Human half — the gate.** Show the user how to open it and ask them to eyeball it. If the user is away, state the preview location and the agent-half evidence, record the eyeball as pending in the phase update, and continue to the suggestions — never claim the design system verified until they have looked.
   Per-page pixel conformance *during feature work* is `/pixel-audit`'s job — reference it, do not duplicate it here.
5. **Document** the design system under `specs/design-system/` (see template), **add the short reference to AGENTS.md** (see template), and **seed or extend the project UI skill** (see below).

### extend (re-run)

Three triggers: the design system grew (e.g. a new component from Figma); a UI change needs a component the library lacks; **post-development feedback loop** — a page or feature just shipped and its UI should flow back into the library.

**On a UI change that needs a component:** check the library first. If the component **exists**, there's nothing to build — the feature reuses it; stop and say so. If it's **missing**, build it from the design-system source; if no reference covers it, **ask the user for a reference before building** — do not invent it.

**Post-development feedback loop:** review the finished page's **diff** for UI that emerged or changed, **promote** each reusable piece into the library (built from the shipped UI plus the design-system source), and leave page-local one-off UI in place only when it's documented with a reason, per the project skill's reuse-vs-new rule.

**Always keep in sync.** Whichever trigger fired, update the **library, preview, `specs/design-system/` doc, AGENTS.md reference, and project UI skill together** — a promoted or changed component must render in the preview and appear in the doc and project skill in the same pass.

**Boundary — design system only.** `extend` updates the design system and nothing else. It does **not** commit, push, write ADRs, or produce handovers; those stay `/grill-with-docs` and `/commit-push-*`, invoked separately per suggest-never-auto-chain. It is the same skill the binding rule calls into on a UI change.

## Documentation & registration

### The `specs/design-system/` doc (the durable record)

Write the full documentation to the docs location chosen at setup. When no setup decision exists, fall back to `<artifacts-root>/specs/`, resolving `<artifacts-root>` the same way the other kit skills do: (1) the directory containing a `*.code-workspace` file if one exists, (2) the per-context root in a multi-context repo (`CONTEXT-MAP.md` at root), (3) the single repo root. Do **not** hardcode a path:

```text
<docs-root>/design-system/<TARGET-PROJECT-CODE>-design-system.md
```

Fill the doc skeleton in [`references/registration-templates.md`](references/registration-templates.md) §1 — Source, Stack, token/library/preview paths, `Project skill:` (the UI skill's real name), a component/states table, the consumption rule, and any deviations.

### The AGENTS.md reference (short, binding, PROJECT-CODE-keyed)

Add only a terse reference into the binding `AGENTS.md`, integrated the way `/agents-md` structures that file. Update the subsection in place on `extend`; never duplicate it. **Do not put the full design system in AGENTS.md** — it points to the doc. Fill [`references/registration-templates.md`](references/registration-templates.md) §2: the PROJECT-CODE-keyed pointer (doc path · preview · project skill) plus the binding library-first rule.

### Seed or extend the project UI skill

This project skill is the **deep, project-specific reference** an implementer opens when doing real UI work. It can grow large and hand-grown over time (component inventory, project rules, high-frequency gotchas, ADR trail). Keep the division of labour clear: the always-on "check the library first" trigger lives in the AGENTS.md reference above; **all project-specific rules — naming, allowed/forbidden patterns, per-project conventions, token names, component lists — live in this skill and the `specs/design-system/` doc, never hardcoded into `/design-system` itself.** `/design-system` is generic machinery; the project UI skill is where a project's own UI law is written.

**Detect an existing UI skill first.** Before seeding anything, survey the project's and workspace's skill locations — `<project>/.agents/skills/` plus the runtime dirs in use (`.claude/skills/`, `.cursor/skills/`, …) — for a skill whose name or description already owns UI work for this project (UI coding, frontend, components, design, styling). Found one → **adopt and extend it in place; never seed a parallel `<project-slug>-ui-coding` beside it** — two UI skills would compete for routing. Expand and improve the existing skill from the design system: fold in the real token/library/preview/doc paths, the component inventory and states, the reuse-before-new discipline, the missing-component procedure, and the binding consume-the-library rule; sharpen its description so UI work still routes to it. Preserve its hand-grown conventions and voice — show the diff of what you'd change, and where an existing rule contradicts the design system, surface the conflict to the user rather than silently rewriting either side. Record the adopted skill's **real name** (not `<project-slug>-ui-coding`) in the doc's `Project skill:` line and the AGENTS.md reference — that reference is the pointer other skills and sessions follow.

Only when no UI skill exists anywhere in the project: create a **project-local** operational skill named `<project-slug>-ui-coding` (kebab-case, matching the target's existing project naming — e.g. `admin-web-ui-coding` for `ADMIN-WEB`) at the kit's project-local skills location: `<project>/.agents/skills/<project-slug>-ui-coding/SKILL.md`, which the generated AGENTS.md tells every runtime to read. When the current runtime also discovers project skills natively from its own directory (e.g. `.claude/skills/`, `.cursor/skills/`), add a copy or symlink there by that runtime's mechanism — the `.agents/skills/` copy stays canonical. Seeded or adopted, the skill captures the operational rules an implementer needs:

- where the tokens, library, preview, and design-system doc live (the real paths);
- the base component inventory and their states;
- **reuse-before-new** discipline: on any UI change, check the library first; extend an existing component before adding a parallel one; no one-off UI unless documented and justified;
- how a missing component is added (via `/design-system` extend, from the reference — ask the user for a reference if none exists) and that the preview must render it;
- the binding "consume the library, never inline covered markup" rule, pointing back to the AGENTS.md reference and the `specs/design-system/` doc.

Fresh-seed frontmatter + shape (fresh-seed path only): [`references/registration-templates.md`](references/registration-templates.md) §3.

## Output

After `bootstrap` (or `extend`):

- **Suggest the next step and stop.** Recommend the user open the preview and eyeball it; once verified, begin Workflow B (`/feature-prompt` → `/grill-with-docs` → …) for the first feature, which will now consume the library.
- **Emit the phase update:**

```markdown
Stage: design-system (<bootstrap|extend>) — built tokens + library + preview for <TARGET-PROJECT-CODE>; wrote <docs-root>/design-system/<TARGET-PROJECT-CODE>-design-system.md; added AGENTS.md reference; seeded/extended <ui-skill name>.
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

- [ ] TARGET PROJECT-CODE known; stack read from the Project Matrix / `AGENTS.md`, not guessed (missing matrix → routed to `/agents-md`)
- [ ] A real design-system source was used (Figma / spec / reference / guided-definition **approved by the user**) — nothing fabricated silently
- [ ] Tokens written as named values in the stack's native mechanism; library built from the tokens, in the target's idiom, faithful to the source
- [ ] Preview demonstrably renders — build/serve ran, the preview loaded (served HTML/file or screenshot quoted), and every extracted component appears in its states (default/hover/focus/disabled/active; empty/loading/error; responsive)
- [ ] User was shown how to open the preview and asked to eyeball it; if the user was away, the pending eyeball is recorded and nothing was claimed verified
- [ ] Full documentation written to `<docs-root>/design-system/<TARGET-PROJECT-CODE>-design-system.md`; AGENTS.md holds only the short PROJECT-CODE-keyed reference + binding library-first rule (updated in place on `extend`)
- [ ] Project UI skill handled: an existing UI skill (any name) was detected, adopted, and extended in place — hand-grown conventions preserved, conflicts surfaced, real name recorded in the doc + AGENTS.md reference — or, only when none existed, `<project-slug>-ui-coding` was seeded; never a parallel duplicate
- [ ] `extend`: library + preview + doc + AGENTS.md reference + project skill updated together; a missing component was built from a reference (asked the user when none existed), never invented; nothing outside the design system touched — no commit, push, ADR, or handover
- [ ] Post-development feedback loop (when that trigger fired): shipped page's diff reviewed; emergent reusable UI promoted; page-local one-offs left only when documented with a reason
- [ ] No conventions carried in from another project; `/pixel-audit` referenced, not duplicated; suggested the next step and stopped — no auto-chain; `Stage / Found / Next / Needs user` emitted

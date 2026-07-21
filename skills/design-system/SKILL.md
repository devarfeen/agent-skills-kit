---
name: design-system
disable-model-invocation: true
description: Project start-off skill, run once per UI project after /agents-md and setup; re-run `extend` as the design grows or to fold a shipped page's UI back into the library. Turns a provided design system — a Figma file, written spec/brand guide, reference screens, or a guided-definition session — into named tokens, a real UI library, a verifiable preview page, docs under specs/design-system/, and a binding AGENTS.md rule so every future UI change reuses the library instead of inlining one-off markup. Stack-adaptive — reads each project's stack from the workspace matrix that /agents-md generates. A design-system source is required — never fabricated. Never auto-chains.
---

# design-system

Builds a provided design system into named tokens, a UI library in the target stack's idiom, a verifiable preview page, a doc under `specs/design-system/`, a binding AGENTS.md reference, and a project UI skill — so every later UI change reuses the library instead of inlining one-off markup. Run once per UI project after `/agents-md` → `/setup-matt-pocock-skills` → placeholder fill; re-run `extend` when a trigger fires.

**Not this skill.** One page matching its design pixel-for-pixel is `/pixel-audit`; cosmetic QA tails are `/polish-batch`; porting UI from a reference stack is `/port-feature`; tracing existing UI is `/feature-discovery`.

## Inputs

Infer from the request and cheap repo evidence; interview only for gaps:

- **TARGET PROJECT-CODE** — the full Project Matrix code; it determines the output idiom. Project Matrix missing → stop and route to `/agents-md` first. Read the target's stack from the matrix / `AGENTS.md`, never guess it.
- **DESIGN-SYSTEM SOURCE (required)** — a **Figma** file/URL (via the Figma MCP companion — not installed → say so and ask for exported frames/tokens or a written spec); a **written design spec / brand guide**; **reference screens or a reference app**; or, when none exists, a **guided-definition session** — walk the user through colours, neutrals, typography, type scale, spacing, radius, shadow, and base components, and end in **explicit user approval** before building. **Never fabricate a whole design system silently.** No source and no approved guided session → stop and ask.

## Rules

- Name the full PROJECT-CODE from the Project Matrix everywhere; never mix one project's conventions, tokens, or components into another.
- Decisions are **artifacts** — every output lives on disk, not in chat.
- Never hardcode locations — resolve paths from the target's stack conventions and setup decisions; record real paths in doc, reference, and skill.
- Sub-agents: dispatch local lanes automatically for independent work — never cloud agents; announce the lane count at dispatch and report each lane as it completes. Lanes extract and survey only; the main agent owns synthesis.
- Emit `Stage / Found / Next / Needs user` at each phase transition — one line per field.
- **Suggest, never auto-chain.** Recommend the next step and stop; never start feature work here.

## Stack-adaptive output

Never hardcode one framework — emit in the target's idiom: framework web (Laravel/Livewire, Rails, Django, …) → framework components + a server-rendered preview route (e.g. `/ui/preview/all`); React Native → library + preview screen; static HTML/PHP → HTML/CSS components + a static preview file. Anything else → the closest by how it renders UI.

## Modes

### bootstrap (default)

Full first run; an existing design-system doc or library → switch to `extend` and update in place. In order:

1. **Extract** tokens and the base component list with states from the source; the guided-definition path must end in explicit user approval before any component is built.
2. **Tokens** — colours, typography, spacing, radii, shadows as named tokens in the stack's native mechanism (CSS variables, Tailwind `theme`, RN theme object, …), never hardcoded per use.
3. **UI library** — build the base components (buttons, inputs, selects, toggles, cards, alerts, badges, …) from the tokens, faithful to the source.
4. **Preview page** — one page/route/screen rendering every component in its states (default/hover/focus/disabled/active; empty/loading/error where relevant; responsive) — the verification gate, in two halves:
   - **Agent half — evidence first.** Build/serve the target, load the preview, and check every extracted component appears with no error output. An agent-browser screenshot is the evidence floor for any stack; a served-HTML fetch substitutes only for server-rendered output. **Exception — client-rendered stacks (React Native, React SPA):** the served HTML is an empty root, so a screenshot or rendered DOM/tree snapshot is required — a plain HTML fetch is not evidence there. Quote the evidence: URL/file, status, screenshot path, and the rendered component list (DOM query, tree snapshot, or served-HTML match) checked off against the extracted inventory — a bare aggregate count is not evidence.
   - **Human half — the gate.** Show the user how to open the preview and ask them to eyeball it. If the user is away, state the preview location and the agent-half evidence, record the eyeball as pending in the phase update, and continue to the suggestions — never claim the design system verified until they have looked.
   Where a snapshot harness exists, add a minimal render/snapshot test per base component. Per-page pixel conformance during feature work stays `/pixel-audit`'s — reference, don't duplicate.
5. **Register** — write the doc, the AGENTS.md reference, and the project UI skill (below).

### extend (re-run)

Triggers: the design system grew (a new Figma component); a UI change needs a missing component; the post-development feedback loop — a shipped page's UI flows back into the library.

- **Missing component:** check the library first. Exists → nothing to build; stop and say so. Missing → build from the design-system source; no covering reference → ask the user for one before building — do not invent it.
- **Feedback loop:** review the shipped page's diff and promote each reusable piece into the library, built from the shipped UI plus the design-system source; leave page-local one-offs only when documented with a reason.
- **Sync:** update library, preview, doc, AGENTS.md reference, and project UI skill together in one pass.
- **Boundary — design system only.** `extend` updates the design system and nothing else. It does not commit, push, write ADRs, or produce handovers; those stay `/grill-with-docs` and `/commit-push-*`, invoked separately per suggest-never-auto-chain.

## Registration

### The `specs/design-system/` doc

Write the full doc to `<docs-root>/design-system/<TARGET-PROJECT-CODE>-design-system.md`, with `<docs-root>` the setup docs location; no setup decision → fall back to `<artifacts-root>/specs/`. Resolve `<artifacts-root>`: the `*.code-workspace` directory if one exists, else the per-context root (`CONTEXT-MAP.md` at repo root), else the repo root. Fill the doc skeleton in [`references/registration-templates.md`](references/registration-templates.md) §1.

### The AGENTS.md reference

Add only a terse PROJECT-CODE-keyed reference where `/agents-md` structures it; update in place on `extend`, never duplicate. The full design system never goes in AGENTS.md — it points to the doc. Fill [`references/registration-templates.md`](references/registration-templates.md) §2.

### The project UI skill

The deep reference for real UI work; every project-specific UI rule lives in it and the doc, never in `/design-system`.

- **Detect an existing UI skill first:** survey `<project>/.agents/skills/` and the runtime dirs (`.claude/skills/`, `.cursor/skills/`, …) for a skill already owning this project's UI work.
- Found one → adopt and extend it in place; **never seed a parallel skill beside it** — two UI skills compete for routing. Fold in the real paths, component inventory and states, reuse-before-new discipline, missing-component procedure, and the consume-the-library rule; sharpen its description so UI work still routes to it.
- Preserve its hand-grown conventions and voice: show the diff, and where an existing rule contradicts the design system, surface the conflict to the user rather than silently rewriting either side.
- Record the adopted skill's **real name** in the doc's `Project skill:` line and the AGENTS.md reference.
- Only when no UI skill exists anywhere: seed a project-local `<project-slug>-ui-coding` (kebab-case, per target naming); location, per-runtime copies, and operational content: [`references/registration-templates.md`](references/registration-templates.md) §3.

## Output

Emit the phase update and stop:

```markdown
Stage: design-system (<bootstrap|extend>) — tokens+library+preview for <TARGET-PROJECT-CODE>; doc <docs-root>/design-system/<TARGET-PROJECT-CODE>-design-system.md; AGENTS.md reference added; <ui-skill name> seeded/extended.
Found: <N> tokens, <M> components (<states covered>); source = <Figma|spec|reference|guided(approved)>; stack = <from matrix>.
Next: open <preview location>, eyeball every component/state; then `/feature-prompt` for the first feature.
Needs user: verify the preview; confirm guided-definition choices or DS/stack deviations.

Suggested next skills (optional):
- /feature-prompt: begin the first feature — it consumes this library.
- /pixel-audit: per-page conformance during that feature work (not here).
```

Do not proceed past the suggestion.

## Completion criteria

- [ ] Tokens, library, and preview exist at the doc-recorded paths
- [ ] Preview evidence quoted per the agent half; render/snapshot tests pass where a harness exists
- [ ] `<docs-root>/design-system/<TARGET-PROJECT-CODE>-design-system.md` exists with a `Project skill:` line naming a skill present on disk
- [ ] `AGENTS.md` holds exactly one design-system reference for the TARGET PROJECT-CODE
- [ ] The phase update records the eyeball as done or pending; nothing ran after it
- [ ] `extend` runs: `git log` shows no new commits from this run

# Registration templates

Fill-in skeletons for the three durable outputs `/design-system` registers. The
SKILL.md body owns *when* and *why* each is written and the adopt-vs-seed logic;
this file is only the shapes to fill. Resolve `<docs-root>` from the setup docs
location (fallback `<artifacts-root>/specs/`); record real paths, never the
placeholders.

## 1. The design-system doc — `<docs-root>/design-system/<TARGET-PROJECT-CODE>-design-system.md`

```markdown
# Design System — <TARGET-PROJECT-CODE>

- **Source:** <Figma URL | spec doc | reference app | guided-definition (approved <date>)>
- **Stack:** <from the Project Matrix>
- **Tokens:** <path + mechanism — e.g. resources/css/tokens.css (CSS vars) / tailwind.config.js theme / src/theme.ts>
- **Library:** <path where the components live>
- **Preview:** <preview route or file — the verification gate>
- **Project skill:** <the project UI skill's real name — `<project-slug>-ui-coding` when seeded fresh>

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

## 2. The AGENTS.md reference — short, binding, PROJECT-CODE-keyed

Add only this terse reference into the binding `AGENTS.md`, integrated the way
`/agents-md` structures that file. Update the subsection in place on `extend`;
never duplicate it. Do **not** put the full design system in `AGENTS.md` — it
points to the doc.

```markdown
## Design System / UI Library

Per project. When building or changing UI for a listed project, consume its UI library and tokens — never inline markup the library covers. Full docs under `<docs-root>/design-system/`.

### <TARGET-PROJECT-CODE>

Design system: `<docs-root>/design-system/<TARGET-PROJECT-CODE>-design-system.md` · Preview: `<preview location>` · Project skill: `<ui-skill name>`.

**On any UI change:** check the `<TARGET-PROJECT-CODE>` library first. Reuse the component if it exists. If it's missing, add it via `/design-system` (extend) from the design-system source; if no reference exists for it, ask the user for one. Never inline a one-off. Per-page pixel conformance is `/pixel-audit`.
```

## 3. Fresh-seed project UI skill — frontmatter + shape

Only for the fresh-seed path (no existing UI skill anywhere in the project); when
one exists, adopt and extend it in place instead. Match the kit's skill format.

**Location.** Create it at `<project>/.agents/skills/<project-slug>-ui-coding/SKILL.md`
— the generated AGENTS.md tells every runtime to read that canonical copy. When the
current runtime also discovers project skills natively from its own directory (e.g.
`.claude/skills/`, `.cursor/skills/`), add a copy or symlink there by that runtime's
mechanism; the `.agents/skills/` copy stays canonical.

```markdown
---
name: <project-slug>-ui-coding
description: UI-coding rules for <TARGET-PROJECT-CODE> — on any UI change, consume the design-system library and tokens; reuse existing components, extend from the reference for missing ones, never inline covered markup. Docs: <docs-root>/design-system/<TARGET-PROJECT-CODE>-design-system.md.
---

# <TARGET-PROJECT-CODE> UI Coding

- Tokens: <path/mechanism> · Library: <path> · Preview: <route/file> · Docs: <doc path>
- On any UI change: check the library first; reuse before new; promote repeated markup to the library; no undocumented one-offs.
- Add/change a component only via /design-system (extend), from the reference (ask the user if none), then verify it in the preview.
```

# Registration templates

Fill-in skeletons for the three durable outputs `/design-system` registers. The
SKILL.md body owns *when* and *why* each is written and the adopt-vs-seed logic;
this file is only the shapes to fill. Record real paths, never the placeholders.

Zero attribution: never add or leave co-author, AI, or tool attribution in commits, PRs, issue comments, release notes, generated docs, settings, or code comments. Retain the rule in every filled template.

## 1. The design-system doc — `<docs-root>/design-system/<TARGET-PROJECT-CODE>-design-system.md`

```markdown
# Design System — <TARGET-PROJECT-CODE>

Zero attribution: never add or leave co-author, AI, or tool attribution in commits, PRs, issue comments, release notes, generated docs, settings, or code comments.

- **Source:** <Figma URL | spec doc | reference app | guided-definition (approved <date>)>
- **Stack:** <from the Project Matrix>
- **Tokens:** <actual path and token mechanism from the installed project>
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
On any UI change, reuse components this library covers. For a missing reusable component, suggest `/design-system` extend and pause that dependency until authorized; do not auto-chain. Ask for a source reference when none exists. Document page-local one-offs and their reason. Per-page pixel conformance is `/pixel-audit`.

## Deviations
<any place the build departs from the source, and why>
```

## 2. The AGENTS.md reference — short, binding, PROJECT-CODE-keyed

The shape to insert; SKILL.md owns placement and the update-in-place rule.

```markdown
## Design System / UI Library

Zero attribution: never add or leave co-author, AI, or tool attribution in commits, PRs, issue comments, release notes, generated docs, settings, or code comments.

Per project. When building or changing UI for a listed project, consume its UI library and tokens — never inline markup the library covers. Full docs under `<docs-root>/design-system/`.

### <TARGET-PROJECT-CODE>

Design system: `<docs-root>/design-system/<TARGET-PROJECT-CODE>-design-system.md` · Preview: `<preview location>` · Project skill: `<ui-skill name>`.

**On any UI change:** check the `<TARGET-PROJECT-CODE>` library first. Reuse covered components. For a missing reusable component, suggest `/design-system` extend and pause that dependency until authorized; do not auto-chain. Ask for a source reference when none exists. Document page-local one-offs and their reason. Per-page pixel conformance is `/pixel-audit`.
```

## 3. Fresh-seed project UI skill — frontmatter + shape

Fresh-seed path only (SKILL.md owns adopt-vs-seed); match the kit's skill format.

**Location.** Create it at `<project>/.agents/skills/<project-slug>-ui-coding/SKILL.md`
— the generated AGENTS.md tells every runtime to read that canonical copy. When the
current runtime also discovers project skills natively from its own directory (e.g.
`.claude/skills/`, `.cursor/skills/`), add a copy or symlink there by that runtime's
mechanism; the `.agents/skills/` copy stays canonical.

```markdown
---
name: <project-slug>-ui-coding
description: "UI-coding rules for <TARGET-PROJECT-CODE>: reuse the design-system library and tokens on UI changes; suggest an authorized extension for missing reusable components. Docs: <docs-root>/design-system/<TARGET-PROJECT-CODE>-design-system.md."
---

# <TARGET-PROJECT-CODE> UI Coding

Zero attribution: never add or leave co-author, AI, or tool attribution in commits, PRs, issue comments, release notes, generated docs, settings, or code comments.

- Tokens: <path/mechanism> · Library: <path> · Preview: <route/file> · Docs: <doc path>
- On any UI change: check the library first; reuse before new; promote repeated markup to the library; no undocumented one-offs.
- Suggest /design-system extend for a missing reusable component and pause that dependency until authorized; never auto-chain. Build from the reference, asking when none exists, then verify it in the preview.
```

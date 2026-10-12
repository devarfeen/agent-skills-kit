# Fresh-seed project UI skill

Zero attribution: never add or leave co-author, AI, or tool attribution in commits, PRs, issue comments, release notes, generated docs, settings, or code comments.

Load only after the existing-skill survey found no project UI skill.

**Location.** Create it at `<project>/.agents/skills/<project-slug>-ui-coding/SKILL.md`
— the generated AGENTS.md tells every runtime to read that canonical copy. When the
current runtime also discovers project skills natively from its own directory (e.g.
`.claude/skills/`, `.cursor/skills/`), add a copy or symlink there by that runtime's
mechanism; the `.agents/skills/` copy stays canonical.

```markdown
---
name: <project-slug>-ui-coding
description: "UI-coding rules for <TARGET-PROJECT-CODE>: reuse the design-system library and tokens on UI changes; suggest an authorized extension for missing reusable components."
metadata:
  version: "0.0.1"
---

# <TARGET-PROJECT-CODE> UI Coding

Zero attribution: never add or leave co-author, AI, or tool attribution in commits, PRs, issue comments, release notes, generated docs, settings, or code comments.

- Tokens: <path/mechanism> · Library: <path> · Preview: <route/file> · Docs: <doc path>
- On any UI change: check the library first; reuse before new; promote repeated markup to the library; no undocumented one-offs.
- Suggest /design-system extend for a missing reusable component and pause that dependency until authorized; never auto-chain. Build from the reference, asking when none exists, then verify it in the preview.
```

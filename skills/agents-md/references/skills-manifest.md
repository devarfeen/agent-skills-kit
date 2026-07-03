# Skills Manifest

Single source for the `## Working With Skills` tables generated into `AGENTS.md`.
Do not hardcode skill rows in `SKILL.md` — edit this file to add or move a skill.

Columns:

- `skill` — invocation (e.g. `/tdd`) or companion name.
- `kind` — `kit` (part of this kit) or `companion` (optional separate install).
- `phase` — for `kit`: a gradient phase (`discover`, `sharpen`, `plan`, `slice`, `implement`, `verify`, `ship`) or `startup`. Blank for companions.
- `note` — optional short suffix shown after the skill in the gradient cell (e.g. `→ ADR`).
- `use-when` — for `companion`: the trigger text. Blank for kit skills.

## Kit Skills

| skill | kind | phase | note | use-when |
| ----- | ---- | ----- | ---- | -------- |
| `/feature-discovery` | kit | discover | | |
| `/port-feature` | kit | discover | reference → target gap map | |
| `/feature-prompt` | kit | sharpen | | |
| `/grill-with-docs` | kit | plan | → ADR | |
| `/to-prd` | kit | plan | → PRD | |
| `/to-issues` | kit | slice | | |
| `/integration-contract` | kit | slice | multi-project seams | |
| `/tdd` | kit | implement | | |
| `/review` | kit | verify | | |
| `/diagnosing-bugs` | kit | verify | | |
| `/polish-batch` | kit | verify | cosmetic punch-list | |
| `/pixel-audit` | kit | verify | per-page visual conformance | |
| `/commit-push-close` | kit | ship | | |
| `/commit-push-pr` | kit | ship | | |
| `/release-notes` | kit | ship | | |
| `/design-system` | kit | startup | | |

## Companion Skills And MCPs

| skill | kind | phase | note | use-when |
| ----- | ---- | ----- | ---- | -------- |
| ask-matt | companion | | | You want Matt's upstream router for choosing a user-invoked skill flow. |
| domain-modeling | companion | | | Project terminology, aliases, or ADR-backed domain language need sharpening. |
| codebase-design | companion | | | Module boundaries, seams, or interface design decisions matter. |
| Graphify | companion | | | Querying a generated code/docs/media graph would save broad file reads. |
| Codex plugin for Claude Code | companion | | | Claude Code needs Codex for review or delegated work. |
| Impeccable | companion | | | Frontend design quality, visual polish, or browser-backed UI checks matter. |
| notebooklm-py | companion | | | The user asks to work with NotebookLM sources or artifacts. |
| agent-browser | companion | | | Browser automation, app QA, screenshots, scraping, or Electron app control is needed. |
| herdr | companion | | | Running inside herdr and managing panes, tabs, or worker agents is needed. |
| docker-expert | companion | | | Dockerfiles, Compose, images, containers, or registry workflows are central. |
| Laravel Boost | companion | | | A Laravel project has Boost installed and Laravel-specific MCP context helps. |
| Figma MCP | companion | | | A task references Figma designs, components, frames, tokens, or design-to-code. |
| MySQL/Postgres MCP | companion | | | Approved local or staging database inspection is needed. Default read-only. |

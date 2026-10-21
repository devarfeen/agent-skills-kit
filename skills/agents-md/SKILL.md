---
name: agents-md
disable-model-invocation: true
description: "Generate workspace-root AGENTS.md and rules from .code-workspace, or sync project runtime blocks. Never writes CLAUDE.md/GEMINI.md; a request to make a shim, even with AGENTS.md: writing-for-agents."
metadata:
  version: "0.8.0"
---

# AGENTS.md generator

Produces workspace-root instructions and on-demand rules, optionally synchronizing existing project runtime blocks from local Compose evidence.

## Inputs

- The target root must contain a `*.code-workspace` file (multi- or single-folder). If none exists, stop and do not generate files — the Project Matrix is built from its `folders` list; tell the user to rerun from a folder holding one. If several exist, ask which one to use before scanning.
- Never read or copy the agent's own global or user instruction files (`~/.claude/CLAUDE.md`, `~/.codex/`, global `AGENTS.md`, personal memory/rules). Generate rules from the shipped templates and workspace evidence. Zero attribution: omit co-author, AI, and tool attribution from generated files and all output.

## Rules

- Workspace-root `AGENTS.md` is the single source of truth for Codex CLI, Claude CLI, Antigravity CLI, Cursor CLI, Opencode CLI, and GitHub Copilot CLI; shared operating instructions — context, memory policy, issue routing, skill use — live there.
- Never create or edit `CLAUDE.md` or `GEMINI.md`, or take rules from them; report an existing one as a [competing instruction file](references/competing-instructions.md).
- Create exactly one root `AGENTS.md` and the `rules/` files in the [file map](references/on-demand-files.md). Project synchronization edits existing `AGENTS.md` files only; never create project instruction files.

## Modes

Default: generate or refresh the root file and its on-demand files. When `.devcontainer/compose.yml` exists, read [Project runtime synchronization](references/project-runtime.md) and synchronize existing project runtime blocks; otherwise report synchronization skipped without loading that reference.

A request naming only project-runtime synchronization selects **runtime-only**: follow that reference and existing stack detection; skip root generation, migrations, and setup suggestions. Never create or edit the workspace-root `AGENTS.md` or `rules/` in this mode. Root-generation rules and completion checks below apply only in the default mode.

## Workspace scan

Scan every workspace folder first: note any `VISION.md`/`vision.md` at the workspace or a project root (feeds North star) and detect each stack. Multiple stacks → the intro slot says so and warns against mixing conventions or code across projects.

### Stack detection

The `Stack` cell is fact read from the app-root manifest and lockfiles — never guessed from a folder's name, a root-level manifest, or a file's mere existence. Find the real app root first — often nested (`application/`, `app/`, `src/`) — and read the manifest there. Per-ecosystem manifest reads: [`references/stack-detection.md`](references/stack-detection.md).

## Project Matrix format

One row per `.code-workspace` folder, in `folders` order — never invent or drop projects. Columns exactly `| Project | Path | Stack |`:

- `Project`: the PROJECT-CODE from the folder `name` — strip emojis, uppercase, collapse punctuation/space runs to single hyphens, trim leading/trailing hyphens (`Payments API` → `PAYMENTS-API`); path basename when `name` is missing; type prefix for non-app folders (`PACKAGE-QUEUE`, `DB`). Name the full PROJECT-CODE from the Project Matrix everywhere; never mix one project's conventions, tokens, or components into another.
- `Path`: the folder `path` relative to the workspace root; `.` marks the meta/workspace row.
- `Stack`: one terse line — language, every primary framework, build tooling, package manager; versions only when a manifest pins them; non-app folders state the role. No prose in cells.

If normalization yields an empty or duplicate PROJECT-CODE, stop and ask for a unique code before emitting the matrix. Inspect a `.` folder's manifest too; it can be an application root.

Sample:

```markdown
| Project      | Path             | Stack |
| :---         | :---             | :---  |
| PAYMENTS-API | ../payments-api  | PHP 8.3 / Laravel 13 / Vite / Composer + npm (application/) |
| DB           | ../db-migrations | MySQL / raw SQL migrations |
```

Vite alone never implies a package manager.

## Emitted skeleton

Emit [`assets/agents-md-template.md`](assets/agents-md-template.md) as `AGENTS.md` and each `assets/rules/` file as `rules/<name>`, byte-for-byte, filling only the bracketed slots that the [file map](references/on-demand-files.md) assigns, except customizations retained under Versioning and regeneration. Three rules bind the default skeleton:

- Emit `## Matt skill routing` in `skills.md` only when Matt Pocock's skills are installed: a `SKILL.md` for `ask-matt`, `grill-with-docs`, or `to-spec` exists under `.agents/skills/` or `.claude/skills/` at the workspace root or in the user's home. Otherwise delete the section. If this check and the runtime's skill list disagree, ask. The gradient table lists external skills either way.
- Emit `#### North star` only when the scan found a vision file, listing each with its scope; never fabricate one or restate its content — the subsection points at the file. None found → delete it.
- Keep `issues.md` exactly as concise as its asset has it — routing/label procedure lives in the issue skills, never here — and leave the two Context & native memory placeholders unfilled.

## Working with skills

Generate the gradient table and companions from `references/skills-manifest.md` — the single source; never hardcode rows here. Kit entries with `phase: companion` render only among the companions.

Apply that file's note exclusions, cell and startup-line formats, and install check before emitting a catalog or note.

Fill the `[RUNTIME TOOL-CALLING …]` slot from `references/tool-calling.md`, following its **Emitting into AGENTS.md** format exactly; open a per-runtime table ([claude](references/claude-tools.md), [codex](references/codex-tools.md), [copilot](references/copilot-tools.md), [cursor](references/cursor-tools.md), [opencode](references/opencode-tools.md), [antigravity](references/antigravity-tools.md)) only when a cell is missing or unclear. Native memory setup, on request only: [memory defaults](references/memory-global-defaults.md). Never link the reference files (they do not ship) or restate the Local orchestration rule.

## Versioning and regeneration

The skill version is `v54`. Every generated file carries the marker `<!-- agents-md marker · v54 · re-run /agents-md to regenerate -->` as its first line. Bump it here and in every asset together whenever these rules change. Legacy pre-`v6` markers: [regeneration](references/regeneration.md#legacy-markers).

On run, check each target — the root `AGENTS.md` and every [on-demand file](references/on-demand-files.md#existing-files):

- **None** — generate fresh.
- **Marker present** — before overwriting, show the complete diff section by section — never truncated or summarized — with customizations flagged separately, and confirm. If the user does not respond, stop without writing and say so.
- **No marker (hand-authored)** — do not rewrite it; show what generation would add or change, merge only user-approved sections, and let the existing file win everywhere else.
- **Keep PROJECT-CODEs stable** — keep each existing row's code, matched by `Path`. A code that would now derive differently (a renamed folder) is a separate diff item needing explicit approval; never change it silently. New folders get derived codes.
- **Preserve user edits** — carry over user-filled placeholder values (especially the `GLOSSARY.md` and `specs/adr` paths), customized rule bodies, and foreign sections, per [regeneration](references/regeneration.md).
- **Single-file layout** (marker below `v50`): [layout migration](references/on-demand-files.md#from-the-single-file-layout).
- **Write safely** — re-read each target just before writing; if it changed since approval, show the recomputed diff again. On any write or move failure, stop and report what was and was not written.

### Migrations (ask first)

List every move and every file whose links would be rewritten, and ask first. Move and rewrite only in the artifacts root; report project repositories read-only. Declined or no response → keep the existing paths; never rename unattended.

- An artifact subfolder still under `docs/` (pre-v7): [docs to specs](references/regeneration.md#migrate-docs-to-specs).
- `CONTEXT.md` or `CONTEXT-MAP.md` still in use (pre-v47): [glossary rename](references/regeneration.md#migrate-context-to-glossary).

## Output

Chat carries the pre-write diff, the migration move list and report, the manifest file read for each Project Matrix row, the rule-link check result, [competing instruction files](references/competing-instructions.md), and the emitted byte size — above 32768, add the [Codex size note](references/codex-tools.md#size-cap).

Close by suggesting `/setup-matt-pocock-skills`, `/design-system` for each UI project, and [env-guard hooks](references/env-guard-hooks.md) when hosts are named — suggest only, never run them.

## Completion criteria

- [ ] Requested project synchronization satisfies the matching, approval, and preservation checks in its reference
- [ ] Every file's sections appear in asset order; Matt skill routing present only when Matt's skills resolve, `#### North star` only when a vision file was found
- [ ] Every `rules/` path that `AGENTS.md` names exists after the run — the check is reported in chat; omitting optional sections preserves all numbered rules and Runtime tool-calling
- [ ] Regeneration: foreign sections, user-filled values, and rule-body customizations survive; any customized-rule replacement has explicit approval — or the run stopped without writing
- [ ] Generated catalogs and startup notes contain no manifest-excluded entries; kit companions appear only among the companions, each passing the install check
- [ ] Worktree routing survives Matt routing omission; when emitted, Matt routing passes the verified checkout to the task skill
- [ ] Project Matrix row count equals the `folders` count; chat names the manifest read for every Stack cell; existing PROJECT-CODEs unchanged unless a change was approved
- [ ] Every generated file opens with the current version marker; Context & native memory placeholders intact or carried over filled
- [ ] No `CLAUDE.md` or `GEMINI.md` was created or edited; chat states the emitted byte size, with the Codex note above 32768
- [ ] After an approved migration, moved artifacts have no stale `docs/<sub>/` links or old glossary names, only listed files were rewritten, and unrelated `docs/` content and declined moves remain intact
- [ ] A search of the generated files finds no session data: dates, conversation references, machine-local absolute paths

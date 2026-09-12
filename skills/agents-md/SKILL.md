---
name: agents-md
disable-model-invocation: true
description: "Generate or refresh the workspace-root AGENTS.md and its CLAUDE.md redirect shim for a VS Code .code-workspace root. Any request to write, create, or generate an AGENTS.md file routes here — /writing-for-agents is style guidance for authoring agent-facing documents, not the generator. It creates the Project Matrix of PROJECT-CODEs and the workspace's non-negotiable rules. Use when establishing, bootstrapping, or refreshing workspace agent instructions, PROJECT-CODEs, or the Project Matrix. Use only when a .code-workspace file exists; stop otherwise. It does not build the UI design system or its binding AGENTS.md rule — that is /design-system."
---

# AGENTS.md generator

Generates the workspace-root `AGENTS.md` and `CLAUDE.md` redirect shim from a `.code-workspace` scan, with optional Compose-backed runtime blocks in existing project instructions.

## Inputs

- The target root must contain a `*.code-workspace` file (multi- or single-folder). If none exists, stop and do not generate files — the Project Matrix is built from its `folders` list; tell the user to rerun from a folder holding one.
- Never read or copy the agent's own global or user instruction files (`~/.claude/CLAUDE.md`, `~/.codex/`, global `AGENTS.md`, personal memory/rules). Generate rules from the shipped templates and workspace evidence. Zero attribution: omit co-author, AI, and tool attribution from generated files and all output.

## Rules

- Workspace-root `AGENTS.md` is the single source of truth for Codex CLI, Claude CLI, Antigravity CLI, Cursor CLI, Opencode CLI, and GitHub Copilot CLI; shared operating instructions — context, memory policy, issue routing, skill use — live there.
- `CLAUDE.md` is only a redirect shim for Claude CLI: emit [`assets/claude-md-template.md`](assets/claude-md-template.md) byte-for-byte, nothing more, and never read other context from it.
- Create exactly one root pair. Project synchronization edits existing `AGENTS.md` files only; never create project instruction files. The generated root `AGENTS.md` is spartan and direct.

## Modes

Default: generate or refresh the root pair, and synchronize existing project runtime blocks when `.devcontainer/compose.yml` exists. Read [Project runtime synchronization](references/project-runtime.md) for matching, migration, and approved edits.

A request naming only project-runtime synchronization selects **runtime-only**: follow that reference and existing stack detection; skip root generation, docs migration, and setup suggestions. Never create or edit workspace-root `AGENTS.md` or `CLAUDE.md` in this mode. Root-generation rules and completion checks below apply only in the default mode.

## Workspace scan

Small-scan every workspace folder before generating: note any `VISION.md`/`vision.md` at the workspace or a project root (feeds North star) and detect each stack. Multiple stacks → the intro slot says so and warns against mixing conventions or code across projects.

### Stack detection

The `Stack` cell is fact read from the app-root manifest and lockfiles — never guessed from a folder's name, a root-level manifest, or a file's mere existence. Find the real app root first — often nested (`application/`, `app/`, `src/`) — and read the manifest there. Per-ecosystem manifest reads (PHP, frontend build, JS/TS, Python, test runners, non-app folders): [`references/stack-detection.md`](references/stack-detection.md).

## Project Matrix format

One row per `.code-workspace` folder, in `folders` order — never invent or drop projects. Columns exactly `| Project | Path | Stack |`:

- `Project`: the PROJECT-CODE from the folder `name` — strip emojis, uppercase, collapse punctuation/space runs to single hyphens, trim leading/trailing hyphens (`Payments API` → `PAYMENTS-API`); path basename when `name` is missing; type prefix for non-app folders (`PACKAGE-QUEUE`, `DB`). Name the full PROJECT-CODE from the Project Matrix everywhere; never mix one project's conventions, tokens, or components into another.
- `Path`: the folder `path` relative to the workspace root; `.` marks the meta/workspace row.
- `Stack`: one terse line — language, every primary framework, build tooling, package manager; versions only when a manifest pins them; non-app folders state the role. No prose in cells.

If normalization yields an empty or duplicate PROJECT-CODE, stop and ask for a unique code before emitting the matrix. A folder named `.` still needs its manifest inspected; it can be an application root.

Sample:

```markdown
| PAYMENTS-API | ../payments-api  | PHP 8.3 / Laravel 13 / Vite / Composer + npm (application/) |
| DB           | ../db-migrations | MySQL / raw SQL migrations |
```

## Emitted skeleton

Emit [`assets/agents-md-template.md`](assets/agents-md-template.md) byte-for-byte, filling only the bracketed slots (intro line, Project Matrix, skills tables + startup note, `### Runtime tool-calling` tables, and the `#### North star` list when emitted), except customizations retained under Versioning and regeneration. Three rules bind the default skeleton:

- Emit `### Matt skill routing` only when Matt Pocock's skills are installed (`/ask-matt`, `/grill-with-docs`, or `/to-spec` resolves); otherwise delete the subsection — dead routing rules cost every session tokens.
- Emit `#### North star` only when the scan found a vision file, listing each with its scope; never fabricate one or restate its content — the subsection points at the file. None found → delete it.
- Keep `Issue titles` exactly as concise as the skeleton has it — routing/label procedure lives in the issue skills, never here — and leave the two Context & native memory placeholders unfilled.

## Working with skills

Generate the gradient and companion tables from `references/skills-manifest.md` — the single source; adding or moving a skill edits the manifest, never this file. Kit entries with `phase: companion` render only in the companion table.

Apply the manifest's note exclusions before emitting any catalog or startup note.

Fill the `[RUNTIME TOOL-CALLING …]` slot from `references/tool-calling.md`, opening a per-runtime `*-tools.md` only when a cell is missing or unclear. Emit three compact tables — skill invocation, parallel/background mechanism (drop the `Custom agent files` column), and highest elevated launch preset per runtime — inlined; never link the reference files (they do not ship) or restate the Local orchestration rule. Precede the elevated table with an in-document link to `#skill-tool-use`; the template's Skill & tool use rule owns the permission boundary, so do not repeat it beside the table.

## Versioning and regeneration

The skill version is `v27`. Both generated root files carry the marker `<!-- agents-md marker · v27 · re-run /agents-md to regenerate -->` as their first line (the first line of each template asset in `assets/`). Bump it here and in both template assets together whenever these rules change. Recognize pre-`v6` attribution-bearing comments as legacy markers for migration only; replace them with the current marker in approved regeneration.

On run, check for an existing workspace-root `AGENTS.md`:

- **None** — generate fresh.
- **Marker present** — before overwriting, show a short diff (changed lines only) and confirm. If the user does not respond, stop without writing and say so.
- **No marker (hand-authored)** — do not rewrite it; show what generation would add or change, merge only user-approved sections, and let the existing file win everywhere else.
- **Preserve user edits** — carry over every user-filled placeholder value (especially the `CONTEXT.md` and `specs/adr` paths) and per-project on-demand reads.
- **Reconcile customized rules** — when an exact template for the existing marker is available locally, compare against it to distinguish user edits inside generated rule bodies from template updates. Without that baseline, treat differences as potential customizations, not obsolete defaults. Show customizations and proposed resolutions explicitly in the pre-write diff; retain them unless the user approves changing them. An unresolved conflict or no response means stop without writing.
- **Preserve foreign sections** — carry over verbatim any section another skill added (e.g. `## Design System / UI Library` from /design-system); regeneration replaces only sections this skill generates.
- Regenerate the `CLAUDE.md` shim only if it is missing or its marker is stale.

### Migrate docs/ → specs/ (ask first)

Pre-v7 workspaces kept the artifacts tree under `docs/` instead of `specs/`. When any artifact subfolder (`agents/`, `adr/`, `prompts/`, `qa/`, `port/`, `pixel-audit/`, `integration/`, `design-system/`, `release-notes/`) still sits under `docs/` — strays included — show what would move and ask first; declined or no response → keep the `docs/` paths, never rename unattended. On approval, `git mv` per subfolder (plain `mv` when untracked), merging file by file into any existing `specs/<sub>/` — never `git mv docs specs` wholesale. Rewrite `docs/<sub>/` links to `specs/<sub>/` in the moved files and any file linking them, update filled placeholder paths, and report every move. Non-artifact `docs/` content (the GitHub Pages site) stays.

## Output

Chat carries the pre-write diff, the migration move list and report, and the close: suggest `/setup-matt-pocock-skills`, and `/design-system` for each UI project, then stop — suggest only, never run them.

## Completion criteria

- [ ] Requested project synchronization satisfies the matching, approval, and preservation checks in its reference
- [ ] `AGENTS.md` sections appear in template order; `### Matt skill routing` present only when Matt's skills resolve, `#### North star` only when a vision file was found
- [ ] Named rule links resolve; omitting optional sections preserves all numbered rules and Runtime tool-calling
- [ ] Regeneration: foreign sections, user-filled values, and rule-body customizations survive; any customized-rule replacement has explicit approval — or the run stopped without writing
- [ ] Generated catalogs and startup notes contain no manifest-excluded entries; kit companions appear only in the companion table
- [ ] Worktree routing survives Matt routing omission; when emitted, Matt routing passes the verified checkout to the task skill

- [ ] Project Matrix row count equals the `folders` count; every Stack cell traces to a manifest actually read
- [ ] Both generated files open with the current version marker; Context & native memory placeholders intact or carried over filled
- [ ] `diff` of `CLAUDE.md` against the shim template is empty
- [ ] After an approved migration, moved artifacts have no stale `docs/<sub>/` links; unrelated `docs/` content and declined moves remain intact
- [ ] Neither file leaks session data: dates, conversation references, machine-local absolute paths

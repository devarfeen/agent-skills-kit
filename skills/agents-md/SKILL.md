---
name: agents-md
disable-model-invocation: true
description: "Generate or refresh the workspace-root AGENTS.md and its CLAUDE.md redirect shim for a VS Code .code-workspace root. It creates the Project Matrix of PROJECT-CODEs and the workspace's non-negotiable rules. Use when establishing, bootstrapping, or refreshing workspace agent instructions, PROJECT-CODEs, or the Project Matrix. Use only when a .code-workspace file exists; stop otherwise. It does not build the UI design system or its binding AGENTS.md rule — that is /design-system."
---

# AGENTS.md Generator

Generate agent instructions for VS Code workspaces only.

## Scope

- Target root must contain a `*.code-workspace` file.
- If no `*.code-workspace` file exists, stop and do not generate files. Explain why: this skill builds the Project Matrix from the `.code-workspace` `folders` list, so without that file there is no defined workspace root or project set to generate from. Tell the user to open the task from a folder that holds a `*.code-workspace` file.
- Do not generate per-project or per-repo `AGENTS.md` — workspace-root only.
- Generate one workspace-root `AGENTS.md`.
- Generate one workspace-root `CLAUDE.md`.
- Support both multi-folder and single-folder `.code-workspace` files.

## Source Of Truth

- `AGENTS.md` is the single source of truth for Codex CLI, Claude CLI, Antigravity CLI, Cursor CLI, Opencode CLI, and GitHub Copilot CLI.
- `CLAUDE.md` is only a redirect shim for Claude CLI.
- `CLAUDE.md` must contain only the `@AGENTS.md` forward plus the short redirect note shown below. Do not add or read any other context from `CLAUDE.md`.
- Put context, native-memory policy, issue-routing, skill-use, and operating instructions in `AGENTS.md`.

Use the exact shim in [`assets/claude-md-template.md`](assets/claude-md-template.md) — emit it byte-for-byte, nothing more.

## AGENTS.md Tone And Intro

- Generated `AGENTS.md` must be spartan, direct, concise, and clear — no fluff, no verbose explanation.
- Start generated `AGENTS.md` exactly as the skeleton opens: the version marker, `# Agent Instructions`, then the one-line workspace intro slot.

## Workspace Scan

- Use only two input sources: the `.code-workspace` file and the small-scan of its workspace folders.
- Do not read or copy from the agent's own global or user instruction files. This includes global `AGENTS.md`, user or global `CLAUDE.md`, `~/.claude/CLAUDE.md`, `~/.codex/`, and any personal memory or rules file.
- Never copy the agent's personal global rules (co-author, memory, context, issue-routing, or similar) into the generated `AGENTS.md` or `CLAUDE.md`.
- Parse the `.code-workspace` `folders` list.
- Build the Project Matrix only from that `folders` list.
- Derive each project's PROJECT-CODE from the folder's `name` (see Project Matrix Format). Use path/package metadata only when `name` is missing.
- Small-scan every workspace folder before generating `AGENTS.md`.
- During the small-scan, note whether a `VISION.md` / `vision.md` exists at the workspace root or any project root — each found file feeds the North star subsection.
- Infer stack details per the Stack Detection rules below.
- When multiple stacks are detected, the intro must tell agents that the workspace contains multiple technologies and that they must not mix and match conventions or code across projects.

### Stack Detection

The `Stack` cell is fact read from manifests, not a guess from a folder's name or the mere presence of a file.

- **Find the real app root.** Code often lives in a nested dir (`application/`, `app/`, `src/`), not the folder top. Read the manifest there and note the dir, e.g. `(application/)`.
- **Read manifest contents; never infer from a file's existence.** A `phpunit.xml` is not proof of PHPUnit; an `application/` dir is not proof of Vite.
- **PHP** — `composer.json`: `require.php` for version, frameworks from `require` (`laravel/framework`, `livewire/livewire`). CodeIgniter version from `system/core/CodeIgniter.php` `CI_VERSION`. List every primary framework — a Livewire app must say Livewire.
- **Frontend build** — read the app's own `package.json` (usually `application/package.json`, not the repo root). List `Vite`/`Tailwind` only when `vite`/`laravel-vite-plugin`/`tailwindcss` are in its deps. Never assume Laravel implies a frontend build.
- **JS / TS** — `package.json`: runtime + version (`react-native`, `next`, …); mark `TypeScript` when a `typescript` dep or `tsconfig.json` is present; package manager from the lockfile (`package-lock.json` → npm, `yarn.lock` → yarn, `pnpm-lock.yaml` → pnpm).
- **Python** — framework from `requirements.txt` / `pyproject.toml` (`fastapi`, `django`, `flask`, …); version from `Dockerfile` `FROM python:X.Y`, `.python-version`, or `requires-python`.
- **A test runner is not the stack.** Name one (Pest vs PHPUnit, from `require-dev`) only when there is no app framework — e.g. a plain-PHP site.
- **Distrust the `name` field and root-level manifests.** A root `package.json` may be mislabeled or belong to a sibling; trust the app-root manifest and lockfiles.
- **Composer packages / libraries** — a `composer.json` with `"type": "library"` (or no app framework) is a package, not an app. Note the install source when it comes from a branch: `VCS, branch <name>`.
- **Database / migrations** — a folder of raw SQL or migration files with no app manifest: name the engine (MySQL, Postgres, …) and call it "raw SQL migrations".
- **Meta / workspace root** — the `.`-path folder holding the `.code-workspace`, shared docs, and MCP config: describe it as a meta workspace, not a code stack.

## Project Matrix Format

The Project Matrix is a table in the generated `AGENTS.md`. One row per `.code-workspace` folder, in `folders` order. No extra rows. Never invent projects.

Generate it with these exact columns:

```markdown
| Project | Path | Stack |
| ------- | ---- | ----- |
```

- `Project`: the PROJECT-CODE derived from the folder `name` — strip emojis, uppercase every letter, replace each run of spaces, separators, or punctuation with a single hyphen, then trim leading/trailing hyphens. Example: `Payments API` → `PAYMENTS-API`, `Web` → `WEB`. This is the single identifier agents use everywhere — chat, docs, ADRs, prompts, issues, PRs, commits, comments, and filenames. When `name` is missing, derive it from the folder path basename. For non-app folders, prefix a type when it clarifies, e.g. `PACKAGE-QUEUE`, `SERVICE-SEARCH`, `DB`.
- `Path`: the folder `path` from the `.code-workspace`, relative to the workspace root (`../repo` for a sibling checkout). Use `.` for the folder that points at the workspace root itself — that row is the meta/workspace row.
- `Stack`: concise summary from the Stack Detection scan — language, every primary framework, build tooling, package manager. One line, terse, but omit nothing defining. No version padding unless a manifest pins it. For non-app folders, state the role instead: a shared-config meta root, a composer package (note `VCS, branch <name>` when installed from a branch), a raw-SQL migrations set, and so on.

Keep cells terse. No prose in cells.

Example:

```markdown
| Project        | Path              | Stack                                                       |
| -------------- | ----------------- | ----------------------------------------------------------- |
| WORKSPACE      | .                 | Meta workspace / shared docs + MCP config                   |
| PAYMENTS-API   | ../payments-api   | PHP 8.3 / Laravel 13 / Vite / Composer + npm (application/) |
| APP-MOBILE     | ../app-mobile     | TypeScript / React Native 0.84 / npm                        |
| SERVICE-SEARCH | ../service-search | Python 3.11 / FastAPI / pip / Docker (app/)                 |
| DB             | ../db-migrations  | MySQL / raw SQL migrations                                  |
| PACKAGE-QUEUE  | ../queue-lib      | PHP composer package (VCS, branch `local`)                  |
```

## Emitted Skeleton

The full `AGENTS.md` body lives in [`assets/agents-md-template.md`](assets/agents-md-template.md). Emit it byte-for-byte, filling only the bracketed slots:

- the one-line workspace intro (per Workspace Scan; it carries the multi-stack warning when detected),
- the Project Matrix (per Project Matrix Format above),
- the gradient table, startup note, and companion table (per Working With Skills below),
- the `### Runtime Tool-Calling` tables (per Skills Manifest below).

Three rules bind on the verbatim parts:

- Emit the `### Matt Skill Routing` subsection only when Matt Pocock's skills are installed (any of `/ask-matt`, `/grill-with-docs`, `/to-spec` resolves in the runtime's skill list); otherwise delete that whole subsection — dead routing rules cost every session tokens.
- Emit the `### North star` subsection only when the scan found a `VISION.md` / `vision.md`; list each found file with its scope (workspace, or the PROJECT-CODE). Never fabricate a vision file or restate its content into `AGENTS.md` — the subsection points at the file; the file stays the source. No vision file → delete the subsection.
- Keep `GitHub Issue Titles` exactly as concise as the skeleton has it — the routing/label procedure lives in the issue skills, never here. Leave the two Context & Native Memory placeholders for the user to fill after setup.

## Working With Skills

Build the gradient and companion tables from `references/skills-manifest.md` (see Skills Manifest below) and fill them into the skeleton's Working With Skills section. That section's prose and rules are verbatim skeleton content; only the two tables and the startup note are generated.

### Skills Manifest

The gradient and companion tables are generated from `references/skills-manifest.md`, the single source for both. Do not hardcode skill rows in this file. Adding or moving a skill means editing the manifest, not this `SKILL.md`.

Column semantics (`skill`, `kind`, `phase`, `note`, `use-when`) are documented in the manifest's own header — read them there, not here. One rendering rule binds here: `kit` and `external` skills render in the gradient table alike — the "Do not assume a skill exists; use what is installed" rule already covers separate installs.

Then fill the skeleton's `[RUNTIME TOOL-CALLING …]` slot with a `### Runtime Tool-Calling` subsection, following each of these:

- Read `references/tool-calling.md` only — its "All runtimes (index)", "Parallel & background mechanism by runtime", and "Highest elevated permission by runtime" tables carry everything the emitted tables need.
- Consult a per-runtime `*-tools.md` only when a cell in those tables is missing or unclear.
- Emit three compact tables for the supported runtimes: (1) how each runtime invokes a skill, (2) its local parallel/background mechanism, and (3) the highest elevated launch / permission preset.
- Inline the results in `AGENTS.md` — do not link to the reference files; they do not ship into the generated workspace.
- Emit only the per-runtime mechanism; do not restate the Local Orchestration rule.
- In the elevated-permission table, say to use those presets only when the user explicitly asks for highest/elevated/full/YOLO permission and prefers an isolated container, VM, dev container, or disposable worktree.

## Versioning & Regeneration

The skill version is `v10`. Both generated files carry the marker `<!-- agents-md marker · v10 · re-run /agents-md to regenerate -->` as their first line (the first line of each template asset in `assets/`). Bump the version here and in both template assets whenever these rules change. Files generated before `v6` open with the older `<!-- Generated by the agents-md skill · v<N> · … -->` line — treat either form as a valid version marker when deciding regeneration, never as hand-authored.

On run, check for an existing workspace-root `AGENTS.md`:

- **None** — generate fresh.
- **Exists with a version marker** — read it. Before overwriting, show the user a short diff of what will change (added, removed, or reworded rules, removed non-template sections, new Project Matrix rows, version bump) and confirm. If the user does not respond, stop without writing and say so — regeneration is never worth an unconfirmed overwrite.
- **Exists without a marker (hand-authored)** — do not rewrite it. Show what a generated file would add or change, and merge only the sections the user approves; the existing file's structure and wording win everywhere else.
- **Preserve user edits** — carry over any values the user filled into placeholders, especially the `CONTEXT.md` and `specs/adr` paths in Context & Native Memory, and any per-project on-demand reads they added. Never blow those away on regenerate.
- **Migrate `docs/` → `specs/` (ask first).** The kit's artifacts tree is `specs/`; workspaces generated before v7 used `docs/`. The artifact subfolders are `agents/` (domain model, chat-style rules, issue-tracker conventions, and other agent-instruction docs), `adr/`, `prompts/`, `qa/`, `port/`, `pixel-audit/`, `integration/`, `design-system/`, and `release-notes/`. Trigger when the filled placeholder paths or the workspace root still show any of these under `docs/` — including the **incomplete-migration** case where `specs/` already exists but stray artifact files or a straggler subfolder were later created back under `docs/` (e.g. a new ADR + its prompt written to `docs/adr/` and `docs/prompts/` after the tree already moved). Show what would move and ask the user to confirm. On approval, reconcile **per artifact subfolder**, never by a blanket tree move:
  - Target subfolder absent under `specs/` → move the whole subfolder (`git mv docs/<sub> specs/<sub>` when tracked, plain `mv` otherwise).
  - Target subfolder already exists under `specs/` → move only the stray files into it, file by file (`git mv docs/<sub>/<file> specs/<sub>/<file>` per file when tracked). Never `git mv docs specs` wholesale — it fails or clobbers when `specs/` is present.
  - After moving, rewrite intra-artifact references from `docs/<sub>/…` to `specs/<sub>/…` in the moved files and in any file that links them (e.g. a prompt that links its ADR), so no moved artifact still points at a stale `docs/` path.

  Then update the filled placeholder paths to match (a no-op when they already read `specs/…`) and report every moved path and rewritten link. Declined or no response → keep the `docs/` paths as filled; never rename unattended. Move every artifact subfolder listed above — in this kit `docs/` is reserved for the GitHub Pages public site, so the only content that stays behind is that site (its `_config.yml`, HTML/Jekyll pages, assets); everything agent-facing belongs under `specs/`.
- **Preserve foreign sections** — carry over verbatim any section another skill added (e.g. `## Design System / UI Library` from `/design-system`) and any other section not produced by this skill's templates. Regeneration replaces only the sections this skill generates.

Regenerate the `CLAUDE.md` shim only if it is missing or its marker is stale.

## Completion checklist

Verify against the generated files — each item is observable, not a recollection:

- [ ] `AGENTS.md` contains, in order: intro (+ multi-stack warning when detected), Project Matrix, Non-Negotiable Rules 1–13, Working With Skills (gradient table, startup note, companion table, Matt routing only when installed, Runtime Tool-Calling), Context & Native Memory (North star only when a vision file was found), GitHub Issue Titles, Output Style
- [ ] Project Matrix row count equals the `.code-workspace` `folders` count — no invented or dropped rows; every Stack cell traces to a manifest that was actually read
- [ ] Both generated files open with the current version marker; the two Context & Native Memory placeholders are intact (fresh run) or carried over filled (regeneration)
- [ ] Regeneration: foreign sections preserved verbatim, user-filled values carried, and the shown diff confirmed — or the run stopped without writing
- [ ] Migration (when performed): every artifact subfolder (`agents/` included) left `docs/`, merged into the existing `specs/<sub>/` rather than tree-moved over it, no moved artifact still links a `docs/` path, and only the GitHub Pages public site remains under `docs/`
- [ ] `CLAUDE.md` is exactly the shim template, nothing more
- [ ] No session-specific content leaked into either file — no dates, conversation references, or machine-local absolute paths outside the workspace root

Then suggest the next startup step — `/setup-matt-pocock-skills`, and `/design-system` for each UI project — and stop; suggest only, never run them.

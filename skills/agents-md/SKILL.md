---
name: agents-md
description: "Generate or update AGENTS.md for a repository or VS Code workspace, create CLAUDE.md and GEMINI.md shims, build a project matrix with stable project codes, and reference CONTEXT.md / ADRs as required domain context."
---

# AGENTS.md Generator

Create or update agent instruction files for a codebase:

- `AGENTS.md` as the canonical instruction file
- `CLAUDE.md` shim pointing to `AGENTS.md`
- `GEMINI.md` shim pointing to `AGENTS.md`

Include the four non-negotiable behavioral principles in the `AGENTS.md` template below.
Make clear that these principles must be followed and fully enforced.

## Non-Negotiable Principles

Every generated `AGENTS.md` must include the following five principles as non-negotiables. The five principles are:

1. Think Before Coding
2. Simplicity First
3. Surgical Changes
4. Goal-Driven Execution
5. Caveman Communication (chat output only, intensity: `full`)

## Discovery Workflow

1. Identify the workspace root.
2. Detect whether this is a VS Code workspace:
   - Look for `*.code-workspace` in the current directory.
   - Look for `.vscode/` settings when no `.code-workspace` file exists.
3. If a `.code-workspace` file exists, parse its `folders` entries and build the project matrix from those folders.
4. For VS Code workspace folders, use each folder's `name` field as the source of truth for the project display name and project code. Do not replace it with the filesystem folder name unless `name` is missing.
5. Treat any workspace folder whose `path` is `.` as the meta workspace, not a code project. Also mention the `.code-workspace` file itself, if present, as workspace metadata. Add the meta workspace to `AGENTS.md` with no tech stack.
6. If no VS Code workspace is detected, infer projects from repo roots, package files, app folders, and README files.
7. Detect each project's tech stack from files such as:
   - `package.json`, `pnpm-workspace.yaml`, `yarn.lock`, `vite.config.*`, `next.config.*`
   - `pyproject.toml`, `requirements.txt`, `uv.lock`, `poetry.lock`
   - `go.mod`, `Cargo.toml`, `Gemfile`, `composer.json`
   - `Dockerfile`, `docker-compose.yml`, Terraform files, mobile app configs
8. Check whether `CONTEXT.md` or any artifacts under `docs/adr/` exist. The `docs/adr/` folder is shared across three artifact types — distinguish by filename suffix:
   - `NNNN-<slug>.md` — ADR (no suffix), written by `grill-with-docs`.
   - `NNNN-<slug>-prompt.md` — feature prompt, written by `feature-prompt`.
   - `NNNN-<slug>-release-notes.md` — release notes, written by `release-notes`.
   All three share one numbering sequence so the folder reads chronologically. Reference them as required domain context when present. If none exists and terminology matters, note that domain language is sharpened inline by the `grill-with-docs` skill, which writes to `CONTEXT.md` and ADRs as decisions crystallise. If a legacy `UBIQUITOUS_LANGUAGE.md` is present, also reference it, but prefer `CONTEXT.md` going forward.

Use structured parsing when available. For `.code-workspace`, prefer JSON parsing that tolerates comments if the local toolchain supports it. If not, read carefully and avoid corrupting paths.

## Project Matrix

Every `AGENTS.md` must include a project matrix with this exact heading and columns:

````markdown
## Project Matrix

| Project Name (Code) | Path | Tech Stack |
| --- | --- | --- |
| Full Platform Workspace (FULL-PLATFORM-WORKSPACE) | . | Meta workspace, no code |
| PARTNERS-API (PARTNERS-API) | ../partners-apis.example.com | PHP, Laravel |
````

Project code rules:

- Codes are stable identifiers used by feature prompts, discovery, PRDs, issues, and release notes.
- Use uppercase letters, digits, and hyphens only.
- For VS Code workspaces, derive the code from the workspace folder `name`, not from `path`.
- Preserve the workspace folder `name` as the project name, but remove leading emoji/icons and trim whitespace for the display text in `Project Name (Code)`.
- Normalize the code from the cleaned workspace folder name by uppercasing and replacing non-alphanumeric runs with hyphens.
- Example: `🔌 PARTNERS-API` becomes `PARTNERS-API (PARTNERS-API)`.
- Example: `🧩 Full Platform Workspace` with path `.` becomes `Full Platform Workspace (FULL-PLATFORM-WORKSPACE)` and is marked as meta workspace.
- If two projects collide, add a qualifier: `ADMIN-WEB`, `ADMIN-API`.
- Do not rename existing project codes in an existing `AGENTS.md` unless the user asks.
- Mark the VS Code workspace folder with `path: "."` as `Meta workspace, no code`.

## AGENTS.md Structure

Generate `AGENTS.md` with this structure:

````markdown
# Agent Instructions

## Read First

- `AGENTS.md` is the canonical instruction file for agents in this workspace.
- `CLAUDE.md` and `GEMINI.md` are shims that point here.
- Read `CONTEXT.md` and the relevant files under `docs/adr/` before making domain decisions. The folder holds three artifact types, all sharing one numbering sequence:
  - `NNNN-<slug>.md` — ADRs (no suffix). Architectural decisions; treat as binding.
  - `NNNN-<slug>-prompt.md` — feature prompts produced by `feature-prompt`. Read the latest matching prompt before implementing a feature.
  - `NNNN-<slug>-release-notes.md` — release notes produced by `release-notes`. Read for prior context on a recently shipped feature.
- If a legacy `UBIQUITOUS_LANGUAGE.md` is present, read it too.
- Use the project codes in the Project Matrix when referring to projects in prompts, PRDs, issues, release notes, and discovery reports.

## Non-Negotiable Principles

Follow the following 5 principles. They are non-negotiable and must be fully enforced.

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

## 5. Caveman Communication

**Activate caveman mode (intensity: `full`) for every chat reply. Never apply it to written artifacts.**

- Invoke the `caveman` skill (Julius Brussee, https://github.com/JuliusBrussee/caveman) at intensity `full` for all conversational output to the user in this project.
- Activation is automatic: do not wait for the user to type "caveman mode" or `/caveman`. Treat reading this `AGENTS.md` as the trigger.
- **Chat only.** Do **not** apply caveman compression to:
  - Code, configs, migrations, or any file written to disk.
  - Generated docs (`AGENTS.md`, `CONTEXT.md`, ADRs, READMEs, PRDs, release notes, changelog entries).
  - Commit messages, PR titles, PR bodies, issue bodies, Agent Briefs, or any artifact `/ship-pr`, `/to-issues`, `/to-prd`, `/triage`, or `/release-notes` produces.
  - Tool arguments, search queries, or anything sent to external services.
- If a chat reply contains an inline code block or quoted artifact, the surrounding prose is caveman; the block itself stays in its native form.
- If the user asks for a different intensity (`lite`, `ultra`, `wenyan-*`) or asks to disable caveman, honour that for the rest of the session.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

## Project Matrix

| Project Name (Code) | Path | Tech Stack |
| --- | --- | --- |
| ... | ... | ... |

## Domain Context

- Read `CONTEXT.md` before domain-heavy work.
- `docs/adr/` is the shared folder for architectural decisions, feature prompts, and release notes — distinguish by filename suffix:
  - `NNNN-<slug>.md` (no suffix) — ADR. Binding architectural decision.
  - `NNNN-<slug>-prompt.md` — feature prompt. Implementation-ready spec from `feature-prompt`.
  - `NNNN-<slug>-release-notes.md` — release notes. PM-facing summary from `release-notes`.
  All three share one sequential `NNNN` so the folder reads chronologically.
- If a legacy `UBIQUITOUS_LANGUAGE.md` exists, read it as supplementary context.
- If terminology is unclear, sharpen it inline via the `grill-with-docs` skill, which updates `CONTEXT.md` and ADRs as decisions crystallise.

## Workspace Notes

- [VS Code workspace detection result.]
- [Meta workspace entry explanation, including the workspace folder with path `.` and the `.code-workspace` file if present.]

## Operating Rules

- Preserve unrelated user changes.
- Prefer existing project patterns over new abstractions.
- Keep generated plans tied to project codes.
- Run targeted validation for changed behavior.
````

Preserve any useful existing local instructions when updating `AGENTS.md`, but reorganize duplicated content into this structure.

## Shim Files

Create or update `CLAUDE.md` and `GEMINI.md` as shims.

Use this content unless the project already has important tool-specific instructions:

```markdown
# Agent Instructions

Read `AGENTS.md` first. It is the canonical instruction file for this workspace.

This file is a shim for tool compatibility.
```

If an existing shim contains valuable tool-specific rules, keep them under:

```markdown
## Tool-Specific Notes
```

Do not duplicate the full `AGENTS.md` content into shims.

## Final Response

After writing files, respond with:

```markdown
Generated agent instructions.

Files:
- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`

Project codes:
- `CODE` - Project Name

Notes:
- [VS Code workspace detected / not detected.]
- [CONTEXT.md / `docs/adr/` artifacts (ADRs, `*-prompt.md`, `*-release-notes.md`) referenced, or noted as to-be-produced inline by `grill-with-docs` / `feature-prompt` / `release-notes`. Legacy `UBIQUITOUS_LANGUAGE.md` referenced if present.]
```

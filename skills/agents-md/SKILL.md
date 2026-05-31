---
name: agents-md
description: "Generate workspace-root AGENTS.md and a CLAUDE.md redirect shim for a VS Code .code-workspace root. Use only when a .code-workspace file exists; stop otherwise."
---

# AGENTS.md Generator

Generate agent instructions for VS Code workspaces only.

## Scope

- Target root must contain a `*.code-workspace` file.
- If no `*.code-workspace` file exists, stop. Do not generate files.
- Do not support individual project or repo generation.
- Do not generate per-project or per-repo `AGENTS.md`.
- Generate one workspace-root `AGENTS.md`.
- Generate one workspace-root `CLAUDE.md`.
- Support both multi-folder and single-folder `.code-workspace` files.

## Source Of Truth

- `AGENTS.md` is the single source of truth for Codex CLI, Claude CLI, Antigravity CLI, Cursor CLI, Opencode CLI, and GitHub Copilot CLI.
- `CLAUDE.md` is only a redirect shim to `AGENTS.md`.
- Do not import `CONTEXT.md`, `MEMORY.md`, or any other file from `CLAUDE.md`.
- Do not duplicate operating rules in `CLAUDE.md`.
- Put context, memory, issue-routing, skill-use, and operating instructions in `AGENTS.md`.

Use this exact `CLAUDE.md`:

```markdown
# Agent Instructions

@AGENTS.md

This file redirects Claude CLI to AGENTS.md. AGENTS.md is the source of truth.
```

## AGENTS.md Tone And Intro

- Generated `AGENTS.md` must be spartan, direct, concise, and clear.
- No fluff.
- No verbose explanation.
- Start generated `AGENTS.md` with:

## Workspace Scan

- Use only two input sources: the `.code-workspace` file and the small-scan of its workspace folders.
- Do not read or copy from the agent's own global or user instruction files. This includes global `AGENTS.md`, user or global `CLAUDE.md`, `~/.claude/CLAUDE.md`, `~/.codex/`, and any personal memory or rules file.
- Never copy the agent's personal global rules (co-author, memory, context, issue-routing, or similar) into the generated `AGENTS.md` or `CLAUDE.md`.
- Parse the `.code-workspace` `folders` list.
- Build the Project Matrix only from that `folders` list.
- Use each folder's `name` as the project display name and project-code source. Use path/package metadata only when `name` is missing.
- Support multi-folder and single-folder `.code-workspace` files.
- Small-scan every workspace folder before generating `AGENTS.md`.
- Infer stack details from real files such as `composer.json`, `package.json`, `requirements.txt`, `pyproject.toml` and other common stack indicators.

```markdown
# Agent Instructions

[one concise workspace intro inferred from the .code-workspace name and folder scan]
```

- Generate the multi-technology warning from scan results.
- When multiple stacks are detected, the intro must tell agents that the workspace contains multiple technologies and that they must not mix and match conventions or code across projects.

## Project Matrix Format

The Project Matrix is a table in the generated `AGENTS.md`. One row per `.code-workspace` folder, in `folders` order. No extra rows. Never invent projects.

Generate it with these exact columns:

```markdown
| Project | Path | Stack |
|---------|------|-------|
```

- `Project`: the folder `name` with emojis removed. Preserve case, spacing, and punctuation exactly — no case change, no slugifying, no separator changes. Trim surrounding whitespace only. This is both the display name and the token agents use to refer to the project. When `name` is missing, use the folder path basename.
- `Path`: the folder `path` from the `.code-workspace`, relative to the workspace root. Use `.` when a single-folder workspace points at the root.
- `Stack`: concise stack summary inferred from the folder small-scan — language, framework, package manager. One line. No version padding unless a manifest pins it.

Keep cells terse. No prose in cells.

Example:

```markdown
| Project | Path | Stack |
|---------|------|-------|
| Partners API | ./partners-api | PHP 8.3 / Laravel / Composer |
| Web | ./apps/web | TypeScript / Next.js / pnpm |
```

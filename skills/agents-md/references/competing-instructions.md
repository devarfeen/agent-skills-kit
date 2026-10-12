# Competing instruction files

The generated `AGENTS.md` is the single source of rules, but some runtimes also load their own instruction files beside it, or instead of it. Those files can contradict or hide it without anyone noticing. Report them; never resolve them.

Zero attribution: omit co-author, AI, and tool attribution from all output.

## What to look for

At the workspace root and at each Project Matrix project root, list any that exist:

- `.github/copilot-instructions.md` and `.github/instructions/*.instructions.md` (GitHub Copilot)
- `.cursor/rules/` and a legacy `.cursorrules` (Cursor)
- `GEMINI.md` (Antigravity CLI, GitHub Copilot CLI)
- `AGENTS.override.md` (Codex reads it hierarchically, and it wins over `AGENTS.md`; see `codex-tools.md`)
- `CLAUDE.md`, `.claude/CLAUDE.md`, or `CLAUDE.local.md` (Claude CLI) — open each one to classify it; take no rules from it. Claude CLI reads `AGENTS.md` directly only when none of these sits in the working directory or above it. One that does not import `@AGENTS.md` hides the generated rules from Claude CLI: say so in its report line. One carrying an `agents-md marker` is a redirect an older version of this skill wrote; it still works, and the user may delete it.

## How to report

In chat, under the pre-write diff (or under the matrix evidence on a fresh generation): the heading `Competing instruction files:`, then `<path> (<runtime>)` one per line, or `none found`. Add one line per file naming any rule it states that contradicts a generated rule, quoted shortest-first.

Never edit, merge, move, or delete these files. Consolidating them is the user's call, made outside this skill.

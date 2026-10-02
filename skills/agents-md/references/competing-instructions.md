# Competing instruction files

The generated `AGENTS.md` is the single source of rules, but some runtimes also load their own instruction files beside it. Those files can contradict it without anyone noticing. Report them; never resolve them.

Zero attribution: omit co-author, AI, and tool attribution from all output.

## What to look for

At the workspace root and at each Project Matrix project root, list any that exist:

- `.github/copilot-instructions.md` and `.github/instructions/*.instructions.md` (GitHub Copilot)
- `.cursor/rules/` and a legacy `.cursorrules` (Cursor)
- `GEMINI.md` that is not the generated redirect shim
- `AGENTS.override.md` (Codex reads it hierarchically, and it wins over `AGENTS.md`; see `codex-tools.md`)
- a `CLAUDE.md` that is not the generated shim

## How to report

In chat, under the pre-write diff: `Competing instruction files: <path> (<runtime>)`, one per line, or `none found`. Add one line per file naming any rule it states that contradicts a generated rule, quoted shortest-first.

Never edit, merge, move, or delete these files. Consolidating them is the user's call, made outside this skill.

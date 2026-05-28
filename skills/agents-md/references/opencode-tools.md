Tool-calling index: [`tool-calling.md`](tool-calling.md).

| Skill Reference | Opencode Equivalent |
| :--- | :--- |
| `Read` (file reading) | `read` |
| `Write` (file creation) | `write` |
| `Edit` (file editing) | `edit` (also `apply_patch`) |
| `Bash` (run commands) | `bash` |
| `Grep` (search content) | `grep` |
| `Glob` (search by name) | `glob` |
| `Task` tool (dispatch subagent) | `task` (`subagent_type`, optional `background`) + `task_status` |
| Ask the user mid-run | `question` |
| LSP integration (experimental) | `lsp` (gated by `OPENCODE_EXPERIMENTAL_LSP_TOOL=true`) |
| `WebFetch` / `WebSearch` | `webfetch` / `websearch` |
| `TodoWrite` (task tracking) | `todowrite` |
| `Skill` tool (invoke a skill) | `skill` |

**Key Notes:**

- opencode exposes plain tool names (`read`, `write`, `edit`, `bash`, `grep`, `glob`, `task`, …) — no POSIX (`cat` / `tee` / `sed` / `sh`) aliasing. Discovery walks up for `AGENTS.md` (preferred) then `CLAUDE.md` (Claude-Code compat); globals at `~/.config/opencode/AGENTS.md` and `~/.claude/CLAUDE.md`. Other files (e.g. `CONTEXT.md`, `MEMORY.md`) must be wired via `opencode.json` `instructions` (supports globs and remote URLs).
- `websearch` requires the opencode provider or `OPENCODE_ENABLE_EXA`.
- Skills resolve from `.opencode/skills/`, `~/.config/opencode/skills/`, plus compat dirs `.claude/skills/`, `.agents/skills/`, `~/.claude/skills/`, `~/.agents/skills/`.
- Multi-repo workspace policy: use workspace-root MCP config.
- For exact config-file placement by tool, use [`tool-calling.md`](tool-calling.md).

## Agents: parallel, background & roles

Parallel: the primary agent issues multiple `task` calls in one turn (each runs a child session and returns one `<task_result>`). `task` takes `subagent_type`, `prompt`, optional `task_id` (resume a child session), and optional `background`. Local background: `task(background=true)` runs async and returns a `task_id`; poll with `task_status` (gated by `OPENCODE_EXPERIMENTAL_BACKGROUND_SUBAGENTS=true`; otherwise `task` is synchronous). opencode is fully local — no cloud agent.

Built-in agents: `build` (primary, full access), `plan` (primary, analysis-only), `general` (subagent, multi-step executor), `explore` (subagent, read-only), `scout` (subagent, read-only — external docs and dependency research). Hidden system agents (`compaction`, `title`, `summary`) run automatically. Users can also dispatch a subagent manually by mentioning `@<agent-name>` in a message; `task` permissions (`allow` / `deny` / `ask` per subagent) gate which children a primary may dispatch. Custom agents: `.opencode/agents/<name>.md` (project), `~/.config/opencode/agents/<name>.md` (global), or inline under `"agent"` in `opencode.json`; frontmatter accepts `description`, `mode` (`primary` | `subagent` | `all`), `model`, `permission`, `temperature`, `top_p`, `steps`, `color`, `disable`, `hidden`, and `tools` (per-tool toggles, e.g. `tools: { skill: false }`).

| Role | opencode mechanism |
| :--- | :--- |
| Orchestrator | primary `build` agent |
| Explorer | `task` → `explore` (read-only) |
| Researcher | `task` → `general` + `webfetch` / `websearch` |
| Planner | `plan` primary agent |
| Implementer | `task` → `general` or a write-enabled custom agent |
| Reviewer | custom read-only agent |
| Tester | `task` → `general` (bash) |
| Tool-runner | `task` → `general` (bash); `task(background=true)` for long runs |

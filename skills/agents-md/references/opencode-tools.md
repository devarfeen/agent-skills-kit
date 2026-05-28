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
| `WebFetch` / `WebSearch` | `webfetch` / `websearch` |
| `TodoWrite` (task tracking) | `todowrite` |
| `Skill` tool (invoke a skill) | `skill` (loads `.opencode/skills/`) |

**Key Notes:**

- opencode exposes plain tool names (`read`, `write`, `edit`, `bash`, `grep`, `glob`, `task`, …) verified from source — there is no POSIX (`cat` / `tee` / `sed` / `sh`) aliasing. It reads local `AGENTS.md`, with `CLAUDE.md` as a Claude Code compatibility fallback when no local `AGENTS.md` exists; additional files such as `CONTEXT.md` must be loaded explicitly through `opencode.json` `instructions` or by a direct instruction in `AGENTS.md`.
- Multi-repo workspace policy: use workspace-root MCP config.
- For exact config-file placement by tool, use [`tool-calling.md`](tool-calling.md).

## Agents: parallel, background & roles

Parallel: the primary agent issues multiple `task` calls in one turn (each runs a child session and returns one `<task_result>`). `task` takes `subagent_type`, `prompt`, optional `task_id` (resume a child session), and optional `background`. Local background: `task(background=true)` runs async and returns a `task_id`; poll or block with `task_status` (gated behind the `experimentalBackgroundSubagents` flag; otherwise `task` is synchronous). opencode is fully local — no cloud agent.

Built-in agents: `build` (primary, full access), `plan` (primary, analysis-only), `general` (subagent, multi-step executor), `explore` (subagent, read-only), `scout` (subagent, repo overview; experimental). Custom agents: `.opencode/agents/<name>.md` (project) or `~/.config/opencode/agents/<name>.md` (global) with frontmatter (`description`, `mode`, `model`, `permission`, …), or inline under `"agent"` in `opencode.json`.

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

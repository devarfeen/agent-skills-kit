Tool-calling index: [`tool-calling.md`](tool-calling.md).

| Skill Reference | Copilot CLI Equivalent |
| :--- | :--- |
| `Read` (file reading) | `view` |
| `Write` (file creation) | `create` |
| `Edit` (file editing) | `edit` |
| `Bash` (run commands) | `bash` |
| `Grep` (search content) | `grep` |
| `Glob` (search by name) | `glob` |
| `Task` tool (dispatch subagent) | `task` (with `agent_type`) |
| `WebFetch` | `web_fetch` |
| `TodoWrite` | `sql` with built-in `todos` table |

**Key Notes:**

- Supports async shell sessions (`bash` with `async: true`).
- Auto-discovers skills from installed plugins.
- Multi-repo workspace policy: use workspace-root MCP config and one workspace memtrace server (`memtrace serve --dir <workspace-root>`), not repo-level memtrace MCP entries.
- Understand-Anything policy: keep each project graph in `<project-root>/.understand-anything/knowledge-graph.json`, not workspace root.
- For exact config-file placement by tool, use [`tool-calling.md`](tool-calling.md).

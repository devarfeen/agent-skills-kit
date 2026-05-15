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

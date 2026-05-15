| Skill Reference | Claude Code Equivalent |
| :--- | :--- |
| `Read` (file reading) | `read_file` |
| `Write` (file creation) | `write_file` |
| `Edit` (file editing) | `replace` |
| `Bash` (run commands) | `run_shell_command` |
| `Grep` (search content) | `grep_search` |
| `Glob` (search by name) | `glob` |
| `Skill` tool (invoke a skill) | `Skill` (natively available as tool) |
| `Task` tool (dispatch subagent) | Native sub-agent support |

**Key Notes:**
- Claude Code loads skill content directly into context via the `Skill` tool.
- Supports `defer_loading: true` for metadata-only initial context.

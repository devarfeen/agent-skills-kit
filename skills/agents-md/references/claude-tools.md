Tool-calling index: [`tool-calling.md`](tool-calling.md).

| Skill Reference | Claude Code Equivalent |
| :--- | :--- |
| `Read` (file reading) | `read_file` |
| `Write` (file creation) | `write_file` |
| `Edit` (file editing) | `replace` |
| `Bash` (run commands) | `run_shell_command` |
| `Grep` (search content) | `grep_search` |
| `Glob` (search by name) | `glob` |
| Skill invocation | Direct `/skill-name` command, or automatic loading when the request matches the skill description |
| `Task` tool (dispatch subagent) | Native sub-agent support |

**Key Notes:**

- Claude Code skills are filesystem-backed and can be invoked directly with `/skill-name`.
- Claude Code can also load a skill automatically when the request matches the skill's `description`.
- Supports `defer_loading: true` for metadata-only initial context.

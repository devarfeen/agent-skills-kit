Tool-calling index: [`tool-calling.md`](tool-calling.md).

| Skill Reference | Antigravity CLI Equivalent |
| :--- | :--- |
| `Read` (file reading) | `read_file` |
| `Write` (file creation) | `write_file` |
| `Edit` (file editing) | `replace` |
| `Bash` (run commands) | `run_shell_command` |
| `Grep` (search content) | `grep_search` |
| `Glob` (search by name) | `glob` |
| `TodoWrite` (task tracking) | `write_todos` |
| `Skill` tool (invoke a skill) | `activate_skill` |
| `WebSearch` | `google_web_search` |
| `WebFetch` | `web_fetch` |
| `Task` tool (dispatch subagent) | `@agent-name` (e.g., `@generalist`) |

**Key Notes:**

- Subagents are invoked using the `@` syntax (e.g., `@generalist`, `@code-reviewer`).
- Supports parallel subagent dispatch by requesting multiple `@agent` tasks in one prompt.
- Includes unique tools like `list_directory`, `save_memory`, `ask_user`, and `enter_plan_mode`.

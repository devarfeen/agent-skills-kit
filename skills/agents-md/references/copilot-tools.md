Tool-calling index: [`tool-calling.md`](tool-calling.md).

| Skill Reference | Copilot CLI Equivalent |
| :--- | :--- |
| `Read` (file reading) | `view` |
| `Write` (file creation) | `create` |
| `Edit` (file editing) | `edit` |
| `Edit` (apply patch) | `apply_patch` |
| `Bash` (run commands) | `bash` |
| `Grep` (search content) | `grep` |
| `Glob` (search by name) | `glob` |
| `Task` tool (dispatch subagent) | `task` tool + `/fleet` (orchestrated parallel subagents); built-in agents `explore` / `task` / `general-purpose` / `code-review` / `research` / `rubber-duck` |
| Long-running shell management | `list_bash` / `read_bash` / `stop_bash` / `write_bash` |
| Ask user / memory | `ask_user`, `memory` |
| `WebFetch` | `web_fetch` |
| Skill invocation | `skill` |

**Key Notes:**

- Background: promote a running task or shell with `Ctrl+X → b`; inspect backgrounded shells with `read_bash` / `list_bash` / `stop_bash` / `write_bash`.
- Modes: `Shift+Tab` cycles **standard → plan → autopilot**. Plan is a *mode*, not a subagent.
- Skills are invoked explicitly (e.g. `/skill-name`); plugins bundle agents, skills, hooks, and MCP server configs for distribution.
- Cloud handoff: `/delegate` ships a task to the remote Copilot coding agent (opens PRs). Kit policy: do not use.
- The GitHub MCP server ships built in; custom MCP servers add to it.
- Multi-repo workspace policy: use workspace-root MCP config.
- For exact config-file placement by tool, use [`tool-calling.md`](tool-calling.md).

## Agents: parallel, background & roles

Parallel: `/fleet` makes the main agent decompose a prompt into independent subtasks and run them as context-isolated subagents; the underlying primitive is the `task` tool (with `list_agents` / `read_agent` for inspection). Built-in agents the orchestrator delegates to: `explore`, `task`, `general-purpose`, `code-review`, `research`. Local background: `Ctrl+X → b` promotes a running task / shell to the background. **Cloud coding agent** (runs in GitHub Actions, opens PRs; reachable via `/delegate`) is remote — do not use it.

Custom agents: `.github/agents/<name>.md` or `.agent.md` (repo) or `~/.copilot/agents/<name>.md` (user). Frontmatter fields: `name` (optional), `description` (required), `tools`, `model`, `target` (`vscode` | `github-copilot`), `mcp-servers`, `disable-model-invocation`, `user-invocable`, `metadata`. The agent's prompt is the markdown body (max 30,000 chars), not a frontmatter field.

| Role | Copilot CLI mechanism |
| :--- | :--- |
| Orchestrator | main session / `/fleet` lead |
| Explorer | `explore` built-in agent |
| Researcher | `research` built-in agent (or `explore` + `web_fetch`) |
| Planner | Plan mode (`Shift+Tab`) — no `plan` subagent; orchestrator plans |
| Implementer | write-enabled custom `.github/agents/<name>.md` |
| Reviewer | `code-review` built-in agent |
| Tester | `task` built-in agent |
| Tool-runner | `task` built-in agent; `Ctrl+X → b` background shell |

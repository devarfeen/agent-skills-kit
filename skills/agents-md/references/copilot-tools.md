Tool-calling index: [`tool-calling.md`](tool-calling.md).

| Skill Reference | Copilot CLI Equivalent |
| :--- | :--- |
| `Read` (file reading) | `view` |
| `Write` (file creation) | `create` |
| `Edit` (file editing) | `edit` |
| `Bash` (run commands) | `bash` |
| `Grep` (search content) | `grep` |
| `Glob` (search by name) | `glob` |
| `Edit` (apply patch) | `apply_patch` |
| `Task` tool (dispatch subagent) | `/fleet` (orchestrated parallel subagents); built-in agents `explore` / `task` / `plan` / `code-review` |
| `WebFetch` | `web_fetch` |
| Skill invocation | `skill` |

**Key Notes:**

- Background: promote a running shell to the background with `Ctrl+X → b` (no `async: true` flag exists).
- Skills are invoked explicitly (e.g. `/skill-name`); plugins bundle agents, skills, and MCP servers for distribution.
- Multi-repo workspace policy: use workspace-root MCP config.
- For exact config-file placement by tool, use [`tool-calling.md`](tool-calling.md).

## Agents: parallel, background & roles

Parallel: `/fleet` makes the main agent decompose a prompt into independent subtasks and run them as context-isolated subagents. Built-in agents are role names the orchestrator delegates to: `explore`, `task`, `plan`, `code-review`. Local background: `Ctrl+X → b` promotes a running shell command to the background. **Cloud coding agent** (runs in GitHub Actions, opens PRs) is remote — do not use it. Custom agents: `.github/agents/<name>.agent.md` (repo) or `~/.copilot/agents/<name>.agent.md` (frontmatter `name`, `description`, `tools`, `model`).

| Role | Copilot CLI mechanism |
| :--- | :--- |
| Orchestrator | main session / `/fleet` lead |
| Explorer | `explore` built-in agent |
| Researcher | `explore` + `web_fetch` |
| Planner | `plan` built-in agent |
| Implementer | write-enabled custom `.github/agents/<name>.agent.md` |
| Reviewer | `code-review` built-in agent |
| Tester | `task` built-in agent |
| Tool-runner | `task` built-in agent; `Ctrl+X → b` background shell |

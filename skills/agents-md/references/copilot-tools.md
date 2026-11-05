Tool-calling index: [`tool-calling.md`](tool-calling.md).

> Last verified: 2026-09-28 against installed GitHub Copilot CLI 1.0.88 — flag/command surface via installed `--help`; internal tool names via official docs or the shipped binary; re-verify on touch (see CONTRIBUTING sync map).

| Skill Reference | Copilot CLI Equivalent |
| :--- | :--- |
| `Read` (file reading) | `view` |
| `Write` (file creation) | `create` |
| `Edit` (file editing) | `edit` |
| `Edit` (apply patch) | `apply_patch` |
| `Bash` (run commands) | `bash` (`powershell` on Windows); permission kind `shell(command)`, e.g. `--allow-tool='shell(git:*)'` |
| `Grep` (search content) | `grep` |
| `Glob` (search by name) | `glob` |
| `Task` tool (dispatch subagent) | `task` tool + `/fleet` (orchestrated parallel subagents); built-in agents `explore` / `task` / `general-purpose` / `code-review` / `security-review` / `research` / `rubber-duck` |
| Long-running shell management | `list_bash` / `read_bash` / `stop_bash` / `write_bash` |
| Ask user / memory | `ask_user`, `memory` (Copilot Memory tool) |
| `WebFetch` | `web_fetch` |
| Skill invocation | `skill` |

**Key Notes:**

- Modes: `Shift+Tab` cycles **interactive → plan → autopilot** (`--mode` choices: `interactive`, `plan`, `autopilot`). Plan is a *mode*, not a subagent.
- Skills are invoked explicitly (e.g. `/skill-name`); plugins bundle agents, skills, hooks, and MCP server configs.
- The GitHub MCP server ships built in; custom MCP servers add to it.
- Multi-repo workspace policy: use workspace-root MCP config.
- **Memory:** enable in GitHub Copilot settings (account); CLI: `/memory on`, `/memory off`, `/memory show` (persists). `store_memory` stores recall in GitHub. Do not create or sync repo memory files. See [`memory-global-defaults.md`](memory-global-defaults.md).
- Highest elevated permission launch: `copilot --allow-all` (alias `--yolo`). This is equivalent to `--allow-all-tools --allow-all-paths --allow-all-urls`; combine with `--autopilot` only when the user wants autonomous multi-step continuation.
- `includeCoAuthoredBy` defaults to `true` and adds a `Co-authored-by` trailer to commits; set it to `false` — generated rules forbid attribution.
- For exact config-file placement by tool, use [`tool-calling.md`](tool-calling.md).

## Agents: parallel, background & roles

Parallel: `/fleet` decomposes a prompt into independent subtasks run as context-isolated subagents; the underlying primitive is the `task` tool (with `list_agents` / `read_agent` / `write_agent`). Local background: `Ctrl+X → b` promotes a running task / shell to the background; inspect backgrounded shells with `read_bash` / `list_bash` / `stop_bash` / `write_bash`. **Cloud coding agent** (runs in GitHub Actions, opens PRs; reachable via `/delegate`) is remote — do not use it.

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

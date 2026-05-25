Tool-calling index: [`tool-calling.md`](tool-calling.md).

VS Code's agent surface is **Copilot agent mode**. It shares the custom-agent format and tool set with GitHub Copilot CLI (see [`copilot-tools.md`](copilot-tools.md)) but adds editor-native parallel and background sessions.

| Skill Reference | VS Code (Copilot agent mode) Equivalent |
| :--- | :--- |
| `Read` / `Write` / `Edit` | editor file tools (agent mode) |
| `Bash` (run commands) | integrated terminal tool |
| `Grep` / `Glob` | workspace search tools |
| Skill / custom agent | custom agents in `.github/agents/<name>.agent.md` (formerly `.chatmode.md`) |
| `Task` tool (dispatch subagent) | parallel sessions + sub-sessions in the Agents window |
| MCP tools | configured via `.vscode/mcp.json` or the `mcp` settings key |

**Key Notes:**

- Reads `AGENTS.md`, `.github/copilot-instructions.md`, `.github/instructions/*.instructions.md`, and also `CLAUDE.md` / `GEMINI.md`.
- Custom agents load from `.github/agents/*.agent.md`, `.claude/agents/*.agent.md`, or `~/.copilot/agents/*.agent.md`; add extra paths via the `chat.agentFilesLocations` setting. Frontmatter: `name`, `description`, `tools`, `model`, `handoffs`.
- Multi-repo workspace policy: keep MCP config at workspace root (`.vscode/mcp.json`) and run one workspace memtrace server (`memtrace serve --dir <workspace-root>`), not repo-level memtrace MCP entries.
- Understand-Anything policy: keep each project graph in `<project-root>/.understand-anything/knowledge-graph.json`, not workspace root.
- For exact config-file placement by tool, use [`tool-calling.md`](tool-calling.md).

## Agents: parallel, background & roles

Parallel: the **Agents window** runs multiple agent sessions at once (across workspaces) and can spawn sub-sessions for isolated parallel tasks. Local background: background sessions (surfaced from Copilot CLI) run unattended on your machine and appear in the Chat view. **Cloud coding agent** (assign a GitHub issue to Copilot, or `@copilot` in a PR — runs in GitHub Actions) is remote — do not use it.

| Role | VS Code mechanism |
| :--- | :--- |
| Orchestrator | the main chat session (owns merge + final judgment) |
| Explorer | a read-only `.agent.md` agent or an `explore`-style sub-session |
| Researcher | an agent with web/fetch tools |
| Planner | a plan-focused `.agent.md` agent |
| Implementer | a write-enabled `.agent.md` agent / sub-session |
| Reviewer | a `code-review`-style `.agent.md` agent |
| Tester | a terminal-tool session running tests/build |
| Tool-runner | a background session for long shell work |

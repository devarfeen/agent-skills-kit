# Cursor CLI / IDE Tool Mapping

Mechanics and permissions: [`tool-calling.md`](tool-calling.md).

| Skill Reference | Cursor CLI / IDE Equivalent |
| :--- | :--- |
| `Read` (file reading) | `Read` |
| `Write` (file creation) | `Write` |
| `Edit` (file editing) | `StrReplace` |
| `Bash` (run commands) | `Shell` |
| `Grep` (search content) | `Grep` |
| `Glob` (search by name) | `Glob` |
| `Delete` (remove file) | `Delete` |
| Semantic / codebase search | `SemanticSearch` (indexed workspace; agent may chain with `Grep`) |
| `TodoWrite` (task tracking) | `TodoWrite` |
| Skill invocation | `/skill-name` in chat, or `@skill-name` to attach as context |
| `Task` tool (dispatch subagent) | `Task` with `subagent_type` (`explore`, `shell`, `generalPurpose`, …) or custom `.cursor/agents/<name>.md` |
| Custom subagents | `.cursor/agents/<name>.md` or `~/.cursor/agents/<name>.md`; also `/name` in chat |
| `WebSearch` | `WebSearch` |
| `WebFetch` | `WebFetch` |
| `GenerateImage` | `GenerateImage` |
| MCP tools | Configured MCP servers; hook matcher form `MCP:<server>:<tool>` |
| Background shell polling | `Await` (after `Shell` with background execution) |
| Mode switch (plan vs agent) | `SwitchMode` or CLI `--mode=plan` / `--mode=ask` |

**Key Notes:**

- Cursor CLI command is `agent` (interactive: `agent`, non-interactive: `agent -p "..."`).
- `AGENTS.md` is the canonical workspace instruction file; no extra shim is required for Cursor.
- Cursor MCP config files: `<workspace-root>/.cursor/mcp.json` (recommended for multi-repo workspaces), `~/.cursor/mcp.json` (global fallback).
- Memtrace policy for multi-repo workspaces: keep one workspace-root memtrace MCP server and avoid repo-level memtrace MCP entries.
- Understand-Anything knowledge base policy: keep project graphs at `<project-root>/.understand-anything/knowledge-graph.json` and avoid workspace-root project graph storage.
- Skills load from `.cursor/skills/`, `.agents/skills/`, and user-level `~/.cursor/skills/` / `~/.agents/skills/`.
- Project overrides: `.cursor/cli.json` layered from git root to cwd; home config: `~/.cursor/cli-config.json`.
- Built-in subagents **Explore**, **Bash**, and **Browser** are delegated automatically when appropriate; see [Subagents](https://cursor.com/docs/subagents).

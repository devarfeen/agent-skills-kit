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
| `Task` tool (dispatch subagent) | `Task` with `subagent_type` (`explore`, `bash`, `browser`, `generalPurpose`, …) or custom `.cursor/agents/<name>.md` |
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

## Agents: parallel, background & roles

Parallel: issue multiple `Task` calls in one turn (practical cap ~4). Local background: set `is_background: true` in `.cursor/agents/<name>.md` and rejoin with `Await`; for heavier isolation, run up to 8 local agents in separate git worktrees. **Cloud Agents** (formerly "Background Agents") are remote — do not use them; keep everything local. Custom-agent frontmatter: `name`, `description`, `model` (`inherit` or an ID), `readonly`, `is_background`.

| Role | Cursor mechanism |
| :--- | :--- |
| Orchestrator | main `agent` session (owns merge + final judgment) |
| Explorer | `Task` → `explore` subagent |
| Researcher | `Task` → `generalPurpose` + `WebSearch` / `WebFetch` |
| Planner | Plan mode (`--mode=plan` / `SwitchMode`) or a `readonly: true` custom agent |
| Implementer | `Task` → `generalPurpose` or a write-enabled `.cursor/agents/<name>.md` |
| Reviewer | `readonly: true` custom agent (e.g. `.cursor/agents/reviewer.md`) |
| Tester | `Task` → `bash` subagent |
| Tool-runner | `Task` → `bash` subagent; `Shell` + `Await` for background output |

Corrections vs older notes: the shell subagent type is `bash` (not `shell`); `~/.cursor/permissions.json` holds the MCP auto-run allowlist (the `cli-config.json` path is unconfirmed in current docs).

# Cursor CLI Tool Mapping

Mechanics and permissions: [`tool-calling.md`](tool-calling.md).

| Skill Reference | Cursor CLI Equivalent |
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
| Skill invocation | `/skill-name` in chat (auto-discovery via skill `description`; set `disable-model-invocation: true` for slash-only) |
| `Task` tool (dispatch subagent) | `Task` invoking built-in (`explore`, `bash`, `browser`) or custom `.cursor/agents/<name>.md` |
| Custom subagents | `.cursor/agents/<name>.md` or `~/.cursor/agents/<name>.md`; also `/name` in chat |
| `WebSearch` | `WebSearch` |
| `WebFetch` | `WebFetch` |
| `GenerateImage` | `GenerateImage` |
| MCP tools | Configured MCP servers; hook matcher `MCP:<tool>`; CLI permission pattern `Mcp(server:tool)` |
| Background shell polling | `Await` (after `Shell` with background execution) |
| Mode switch (plan vs agent) | `SwitchMode` or CLI `--mode=plan` / `--mode=ask` |

**Key Notes:**

- Cursor CLI command is `agent` (interactive: `agent`, non-interactive: `agent -p "..."`).
- `AGENTS.md` is the canonical workspace instruction file; no extra shim is required for Cursor.
- **Memory:** No memory flag in `~/.cursor/cli-config.json`. IDE “Generate Memories” (Settings → Rules) is separate from repo `<repo-root>/MEMORY.md`. Read repo `MEMORY.md` at session start per `AGENTS.md`; `/memory-steward` light pass at start, full on user request. Optional MCP memory in `.cursor/mcp.json` is supplementary. See [`memory-global-defaults.md`](memory-global-defaults.md).
- Cursor MCP config files: `<workspace-root>/.cursor/mcp.json` (recommended for multi-repo workspaces), `~/.cursor/mcp.json` (global fallback).
- Skills load from `.cursor/skills/`, `.agents/skills/`, `~/.cursor/skills/`, `~/.agents/skills/`, plus compat dirs `.claude/skills/`, `.codex/skills/`, `~/.claude/skills/`, `~/.codex/skills/`.
- Subagent dirs: `.cursor/agents/`, `.claude/agents/`, `.codex/agents/` (project) and `~/.cursor/agents/`, `~/.claude/agents/`, `~/.codex/agents/` (user).
- CLI permissions: per-project `<root>/.cursor/cli.json` (layered git-root → cwd), global `~/.cursor/cli-config.json`. IDE-only auto-run allowlist (separate): `~/.cursor/permissions.json`.
- Built-in subagents **Explore**, **Bash**, and **Browser** are delegated automatically when appropriate; see [Subagents](https://cursor.com/docs/subagents).

## Agents: parallel, background & roles

Parallel: issue multiple `Task` calls in one turn (practical cap ~4). Local background: set `is_background: true` in `.cursor/agents/<name>.md` and rejoin with `Await`; for heavier isolation, run up to 8 local agents in separate git worktrees. **Cloud Agents** (formerly "Background Agents") are remote — do not use them; keep everything local. Custom-agent frontmatter: `name`, `description`, `model` (`inherit` or an ID), `readonly`, `is_background`.

| Role | Cursor mechanism |
| :--- | :--- |
| Orchestrator | main `agent` session (owns merge + final judgment) |
| Explorer | `Task` → `explore` subagent |
| Researcher | `Task` → custom agent + `WebSearch` / `WebFetch` |
| Planner | Plan mode (`--mode=plan` / `SwitchMode`) or a `readonly: true` custom agent |
| Implementer | `Task` → write-enabled `.cursor/agents/<name>.md` |
| Reviewer | `readonly: true` custom agent (e.g. `.cursor/agents/reviewer.md`) |
| Tester | `Task` → `bash` subagent |
| Tool-runner | `Task` → `bash` subagent; `Shell` + `Await` for background output |

The shell subagent type is `bash` (not `shell`). `~/.cursor/permissions.json` is the **IDE** auto-run allowlist; **CLI** permissions live in `~/.cursor/cli-config.json` (global) and `<root>/.cursor/cli.json` (project).

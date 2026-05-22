# Tool Calling Reference

How agent runtimes invoke tools, and how this kit maps generic skill instructions to each runtime.

## Cursor CLI / IDE

Cursor Agent (editor and `agent` CLI) uses the same tool-calling loop: the model emits a structured tool request, the runtime executes it, and results are appended to context before the next turn. There is no practical limit on tool calls per task.

Docs: [Tool calling fundamentals](https://cursor.com/learn/tool-calling), [Agent tools overview](https://cursor.com/docs/agent/overview), [CLI usage](https://cursor.com/docs/cli/using), [Subagents](https://cursor.com/docs/subagents).

### Tool names (runtime / hooks)

These are the identifiers used in hook matchers (`preToolUse`, `postToolUse`) and in agent traces:

| Tool | Purpose |
| :--- | :--- |
| `Read` | Read file contents (images supported for vision models) |
| `Write` | Create or overwrite files |
| `StrReplace` | Exact string replace edits (primary edit path) |
| `Shell` | Run terminal commands; use `Await` to poll background shells |
| `Grep` | Content search (Instant Grep / ripgrep-backed) |
| `Glob` | Find files by path pattern |
| `Delete` | Remove a file |
| `SemanticSearch` | Codebase search by meaning (indexed workspace) |
| `Task` | Spawn a subagent (`subagent_type` or custom `.cursor/agents/` name) |
| `TodoWrite` | Session task list updates |
| `WebSearch` | Web search queries |
| `WebFetch` | Fetch URL content as markdown |
| `GenerateImage` | Image generation from description |
| `SwitchMode` | Switch to `plan` or `agent` interaction mode |
| `ListMcpResources` / `FetchMcpResource` | MCP resource read |
| MCP tools | `MCP:<server>:<tool>` in hook matchers (e.g. `MCP:github:search`) |
| `EditNotebook` | Edit Jupyter notebook cells |
| `Await` | Poll a background `Shell` session |
| `TabRead` / `TabWrite` | Editor tab read/write (hook matchers only) |

Agent also uses built-in **Explore**, **Bash**, and **Browser** subagents automatically for heavy search, shell series, and browser work. Custom subagents live in `.cursor/agents/*.md` and are invoked via `Task` or `/subagent-name` in chat.

### Skill invocation (not a hook tool type)

Skills are separate from the table above:

- Explicit: `/skill-name` in chat (e.g. `/caveman`, `/release-notes`)
- Context attach: `@skill-name`
- Auto: agent loads skills whose `description` matches the request (unless `disable-model-invocation: true`)

Skill directories: `.cursor/skills/`, `.agents/skills/`, `~/.cursor/skills/`, plus `.claude/skills/` and `.codex/skills/` for compatibility.

### Subagents (`Task` tool)

| `subagent_type` | Role |
| :--- | :--- |
| `explore` | Parallel codebase search; keeps noise out of main context |
| `shell` | Isolated shell command batches (hook/docs: bash subagent) |
| `generalPurpose` | General delegated work |
| Custom | Any `name` from `.cursor/agents/<name>.md` |

Parallel work: multiple `Task` calls in one assistant turn. Resume with agent ID from a prior subagent run.

CLI and editor share subagent support per [Subagents](https://cursor.com/docs/subagents).

### Modes and write access

| Mode | CLI flag / command | Tool writes |
| :--- | :--- | :--- |
| Agent | default | Full tools |
| Plan | `--mode=plan`, `/plan` | Read-only / planning |
| Ask | `--mode=ask`, `/ask` | Read-only Q&A |

Non-interactive CLI: `agent -p "prompt"` (`--print`) runs with full tools unless mode restricts edits. Use `--force` / `--yolo` only when the user wants auto-approved shell.

### Permissions (`~/.cursor/cli-config.json`)

Tool allow/deny uses pattern strings, for example:

- `Shell(**)` — all shell commands
- `Mcp(server-name, tool-name)` — specific MCP tool

Project overrides: `.cursor/cli.json` merged from git root to cwd (deeper wins).

### Kit mapping (generic → Cursor)

See [`cursor-tools.md`](cursor-tools.md) for the full skill-kit → Cursor equivalence table.

## All runtimes (index)

| Runtime | Tool mapping | Skill / caveman invocation |
| :--- | :--- | :--- |
| **Cursor CLI / IDE** | [`cursor-tools.md`](cursor-tools.md) (details in [Cursor section](#cursor-cli--ide) above) | `/caveman`, `/skill-name` — [`caveman-invocation.md`](caveman-invocation.md) |
| Claude Code | [`claude-tools.md`](claude-tools.md) | `/caveman`, `/skill-name` — [`caveman-invocation.md`](caveman-invocation.md) |
| Codex CLI | [`codex-tools.md`](codex-tools.md) | `activate("caveman")` |
| Copilot CLI | [`copilot-tools.md`](copilot-tools.md) | `skill("caveman")` |
| Antigravity CLI | [`antigravity-tools.md`](antigravity-tools.md) | `activate_skill(name="caveman")` |
| Opencode CLI | [`opencode-tools.md`](opencode-tools.md) | `load_skill("caveman")` |

### MCP placement (multi-repo workspaces)

Keep MCP configuration at workspace root for supported coding tools:

- Cursor CLI / IDE: `<workspace-root>/.cursor/mcp.json` (plus optional `~/.cursor/mcp.json` fallback)
- Claude Code: `<workspace-root>/.claude/settings.local.json`
- Legacy MCP readers: `<workspace-root>/.mcp.json`
- Antigravity CLI: `<workspace-root>/.agents/mcp_config.json`
- Codex CLI: `<workspace-root>/.codex/config.toml`

For memtrace, define one workspace-root server (`memtrace serve --dir <workspace-root>`) and avoid repo-level memtrace MCP entries.

### Understand-Anything knowledge base placement

- Keep code knowledge graphs at project-repo root: `<project-root>/.understand-anything/knowledge-graph.json`.
- In multi-repo workspaces, do not place project code knowledge graphs at workspace root.
- First use in a task: check the target project graph exists; if missing, run `/understand` for that project repo.
- Follow-up use: run `/understand-diff` after major edits and `/understand-explain <path>` for targeted deep dives in the same repo.

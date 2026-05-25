# Tool Calling Reference

How agent runtimes invoke tools, and how this kit maps generic skill instructions to each runtime.

## Agent Orchestration Model

The main session is the **orchestrator**. It decomposes work into role-typed lanes, dispatches each lane to a local subagent (or a focused in-process tool pass when the runtime has no subagents), runs independent lanes in parallel, pushes long or noisy lanes to local background/async, and keeps the only seat for merge, conflict resolution, and final judgment. Subagents return summaries, not raw transcripts. This model is enforced by `AGENTS.md` Rules 3, 15, 16, and 17.

### Local-only policy (no cloud agents)

Use only **local** subagents and **local** background/async execution. Local worktree-isolated parallel agents are allowed. Never delegate to cloud or remote background-agent products, even when the runtime makes them one keystroke away:

| Runtime | Cloud/remote product to AVOID | Local equivalent to use instead |
| :--- | :--- | :--- |
| Cursor | Cloud Agents (formerly "Background Agents"), `&`-prefixed cloud hand-off, cursor.com/agents | `Task` subagents; `is_background` subagents + `Await`; local worktree agents |
| Claude Code | (no first-party cloud agent) | `Agent` subagents; `run_in_background` Bash; `background: true` subagents; `isolation: worktree` |
| Codex CLI | Codex Cloud / Codex web delegated tasks | `[features] multi_agent` subagents; local worktrees; local Automations |
| GitHub Copilot CLI | Cloud coding agent (GitHub Actions) | `/fleet` parallel subagents; `Ctrl+X → b` background shell |
| VS Code | Cloud coding agent (assign issue / `@copilot`) | Agents window local + background sessions |
| Antigravity | Managed Agents API / remote managed execution | Agent Manager local parallel instances; `/schedule` local background |
| Opencode | (verify against opencode docs) | local subagents / sessions |
| Legacy MCP readers | n/a (no agent system) | sequential in-process tool passes |

### Canonical role lanes

Standard lane roles used across this kit. Each runtime's `*-tools.md` maps these to that runtime's concrete mechanism. Where a runtime has no dedicated built-in for a role, use its general-purpose subagent with the listed tool profile.

| Role | Tool profile | Purpose |
| :--- | :--- | :--- |
| **Orchestrator** | full (main session) | Decompose, dispatch, await, merge, final judgment. Never spawned. |
| **Explorer** | read-only | Search and map the codebase; trace callers and usage sites. |
| **Researcher** | read-only + web | External docs, web search, dependency source. |
| **Planner** | read-only | Produce a dependency-aware plan or design. |
| **Implementer** | write | Make the edits for one independent slice. |
| **Reviewer** | read-only | Critique a diff for correctness, risk, and convention fit. |
| **Tester** | shell | Run tests / build / lint / typecheck; report evidence. |
| **Tool-runner** | shell + MCP | Isolated shell / MCP / tool-call batches; keep noisy output out of main context. |

### Parallel & background mechanism by runtime

| Runtime | Parallel dispatch | Local background / async | Custom agent files |
| :--- | :--- | :--- | :--- |
| Cursor CLI / IDE | Multiple `Task` calls in one turn (practical cap ~4); local worktree agents (up to 8) | `is_background: true` subagent + `Await`; `bash` subagent isolates output | `.cursor/agents/<name>.md` |
| Claude Code | Multiple `Agent` calls in one turn | `run_in_background` Bash; `background: true` subagents; `isolation: worktree` | `.claude/agents/<name>.md` |
| Codex CLI | `[features] multi_agent` + `spawn_agent` / `spawn_agents_on_csv` (`agents.max_threads`, default 6; `max_depth` 1) | local git worktrees; Automations | `[agents.<name>]` in `config.toml`, or `.codex/agents/<name>.toml` |
| GitHub Copilot CLI | `/fleet` (orchestrated parallel subagents) | `Ctrl+X → b` promotes a shell to background | `.github/agents/<name>.agent.md` |
| VS Code | Multiple parallel sessions in the Agents window | Background sessions surfaced in the Chat view | `.github/agents/<name>.agent.md` |
| Antigravity | `/goal` orchestrator-spawned dynamic subagents (Agent Manager, ~5 parallel) | `/schedule` local background; Artifacts for review | `.agents/agents.md` personas |
| Opencode | (verify in [`opencode-tools.md`](opencode-tools.md)) | (verify) | (verify) |
| Legacy MCP readers | none — sequential in-process tool passes | none | n/a |

Per-runtime role-to-mechanism maps and corrections live in each `*-tools.md`.

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

- Explicit: `/skill-name` in chat (e.g. `/release-notes`)
- Context attach: `@skill-name`
- Auto: agent loads skills whose `description` matches the request (unless `disable-model-invocation: true`)

Skill directories: `.cursor/skills/`, `.agents/skills/`, `~/.cursor/skills/`, plus `.claude/skills/` and `.codex/skills/` for compatibility.

### Subagents (`Task` tool)

| `subagent_type` | Role |
| :--- | :--- |
| `explore` | Parallel codebase search; keeps noise out of main context |
| `bash` | Isolated shell command batches (canonical type name; some community docs say `shell`) |
| `browser` | Browser control via MCP; filters DOM/screenshot noise |
| `generalPurpose` | General delegated work |
| Custom | Any `name` from `.cursor/agents/<name>.md` |

Parallel work: multiple `Task` calls in one assistant turn (practical cap ~4 parallel subagents). Local async: set `is_background: true` in a subagent's `.cursor/agents/<name>.md` frontmatter and rejoin with the `Await` tool. For heavier isolation, Cursor can run up to 8 local agents in separate git worktrees. Resume with the agent ID from a prior subagent run.

Cursor **Cloud Agents** (formerly "Background Agents") run remotely and are out of policy here — use local subagents/worktrees instead (see [Agent Orchestration Model](#agent-orchestration-model)).

CLI and editor share subagent support per [Subagents](https://cursor.com/docs/subagents).

### Modes and write access

| Mode | CLI flag / command | Tool writes |
| :--- | :--- | :--- |
| Agent | default | Full tools |
| Plan | `--mode=plan`, `/plan` | Read-only / planning |
| Ask | `--mode=ask`, `/ask` | Read-only Q&A |

Non-interactive CLI: `agent -p "prompt"` (`--print`) runs with full tools unless mode restricts edits. Use `--force` / `--yolo` only when the user wants auto-approved shell.

### Permissions

Tool allow/deny uses pattern strings, for example:

- `Shell(**)` — all shell commands
- `Mcp(server-name, tool-name)` — specific MCP tool

The MCP auto-run allowlist lives in `~/.cursor/permissions.json`. Verify exact CLI permission-file names against the current [Cursor docs](https://cursor.com/docs); older `cli-config.json` / `.cursor/cli.json` paths are not confirmed in current docs.

### Kit mapping (generic → Cursor)

See [`cursor-tools.md`](cursor-tools.md) for the full skill-kit → Cursor equivalence table.

## All runtimes (index)

| Runtime | Tool mapping | Skill invocation |
| :--- | :--- | :--- |
| **Cursor CLI / IDE** | [`cursor-tools.md`](cursor-tools.md) (details in [Cursor section](#cursor-cli--ide) above) | `/skill-name` |
| Claude Code | [`claude-tools.md`](claude-tools.md) | `/skill-name` |
| Codex CLI | [`codex-tools.md`](codex-tools.md) | runtime skill activation command |
| Copilot CLI | [`copilot-tools.md`](copilot-tools.md) | runtime skill activation command |
| Antigravity CLI | [`antigravity-tools.md`](antigravity-tools.md) | runtime skill activation command |
| Opencode CLI | [`opencode-tools.md`](opencode-tools.md) | runtime skill activation command |
| VS Code (Copilot agent mode) | [`vscode-tools.md`](vscode-tools.md) | custom `.agent.md` + agent mode |

### MCP placement (multi-repo workspaces)

Keep MCP configuration at workspace root for supported coding tools:

- Cursor CLI / IDE: `<workspace-root>/.cursor/mcp.json` (plus optional `~/.cursor/mcp.json` fallback)
- Claude Code: `<workspace-root>/.claude/settings.local.json`
- Legacy MCP readers: `<workspace-root>/.mcp.json`
- Antigravity CLI: `<workspace-root>/.agents/mcp_config.json`
- Codex CLI: `<workspace-root>/.codex/config.toml`
- VS Code (Copilot agent mode): `<workspace-root>/.vscode/mcp.json`

For memtrace, define one workspace-root server (`memtrace serve --dir <workspace-root>`) and avoid repo-level memtrace MCP entries.

### Understand-Anything knowledge base placement

- Keep code knowledge graphs at project-repo root: `<project-root>/.understand-anything/knowledge-graph.json`.
- In multi-repo workspaces, do not place project code knowledge graphs at workspace root.
- First use in a task: check the target project graph exists; if missing, run `/understand` for that project repo.
- Follow-up use: run `/understand-diff` after major edits and `/understand-explain <path>` for targeted deep dives in the same repo.

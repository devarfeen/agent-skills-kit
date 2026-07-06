# Tool Calling Reference

How the six supported CLI runtimes invoke tools, and how this kit maps generic skill instructions to each runtime.

Supported runtimes are Codex CLI, Claude CLI, Antigravity CLI, Cursor CLI,
Opencode CLI, and GitHub Copilot CLI only. Compatibility filenames used by
those tools do not imply support for any other runtime.

> Last verified: 2026-07-06 against all six installed CLIs (codex-cli 0.142.5, claude 2.1.201, agy 1.0.16, cursor-agent 2026.07.01, opencode 1.17.13, copilot 1.0.68) — flag/command surface via `--help`; internals are docs-level and re-verified on touch.

## Agent Orchestration Model

The main session is the **orchestrator**. It decomposes work into role-typed lanes, dispatches each lane to a local subagent (or a focused in-process tool pass when the runtime has no subagents), runs independent lanes in parallel, pushes long or noisy lanes to local background/async, and keeps the only seat for merge, conflict resolution, and final judgment. Subagents return summaries, not raw transcripts. This model is enforced by the `AGENTS.md` Non-Negotiable Rule **Local Orchestration**.

### Local-only policy (no cloud agents)

Use only **local** subagents and **local** background/async execution. Local worktree-isolated parallel agents are allowed. Never delegate to cloud or remote background-agent products, even when the runtime makes them one keystroke away:

| Runtime | Cloud/remote product to AVOID | Local equivalent to use instead |
| :--- | :--- | :--- |
| Codex CLI | Codex Web delegated tasks | `spawn_agent` subagents (on by default); local git worktrees |
| Claude CLI | Routines (`/schedule`), agent teams (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`), background agents on claude.ai | `Agent` subagents; `run_in_background` Bash; `background: true` subagents; `isolation: worktree` |
| Antigravity CLI | Managed Agents API / remote managed execution | Agent Manager local parallel instances via `start_subagent`; `/schedule` local background |
| Cursor CLI | Cloud Agents (formerly "Background Agents"), `&`-prefixed cloud hand-off, cursor.com/agents | `Task` subagents; `is_background` subagents + `Await`; local worktree agents |
| Opencode CLI | (no cloud agent in scope) | `task` subagents / child sessions; `task(background=true)` + `task_status` |
| GitHub Copilot CLI | Cloud coding agent via `/delegate` (runs in GitHub Actions, opens PRs) | `task` tool + `/fleet` parallel subagents; `Ctrl+X → b` background task/shell |

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
| Codex CLI | `spawn_agent` / `spawn_agents_on_csv` (`agents.max_threads`, default 6; `max_depth` 1) — on by default | local git worktrees (Worktrees / Automations are Codex app features, not CLI) | `.codex/agents/<name>.toml` (or `~/.codex/agents/<name>.toml`) |
| Claude CLI | Multiple `Agent` calls in one turn | `run_in_background` Bash; `background: true` subagents; `isolation: worktree` | `.claude/agents/<name>.md` |
| Antigravity CLI | `start_subagent` orchestrator-spawned dynamic subagents (Agent Manager); `browser_subagent` for browser tasks | `/schedule` local background; Artifacts for review | `.agents/agents.md` |
| Cursor CLI | Multiple `Task` calls in one turn (practical cap ~4); local worktree agents (up to 8) | `is_background: true` subagent + `Await`; `bash` subagent isolates output | `.cursor/agents/<name>.md` |
| Opencode CLI | Multiple `task` calls with `subagent_type` | `task(background=true)` + `task_status` | `.opencode/agents/<name>.md`, `~/.config/opencode/agents/<name>.md`, or inline `opencode.json` agents |
| GitHub Copilot CLI | `task` tool + `/fleet` (orchestrated parallel subagents; built-ins `explore` / `task` / `general-purpose` / `code-review` / `research` / `rubber-duck`) | `Ctrl+X → b` promotes a task or shell to background | `.github/agents/<name>.md` or `.agent.md` (user-scope `~/.copilot/agents/`) |

Per-runtime role-to-mechanism maps and corrections live in each `*-tools.md`.

### Highest elevated permission by runtime

Use these only when the user explicitly asks for highest/elevated/full/YOLO permission, and prefer isolated containers, VMs, dev containers, or disposable worktrees.

| Runtime | Highest elevated launch / preset | Effect |
| :--- | :--- | :--- |
| Codex CLI | `codex --dangerously-bypass-approvals-and-sandbox` (or explicit `codex --sandbox danger-full-access --ask-for-approval never`) | No sandbox and no approval prompts. |
| Claude CLI | `claude --dangerously-skip-permissions` (equivalent to `--permission-mode bypassPermissions`) | Skips the permission layer; protected paths are allowed except hard circuit breakers. |
| Antigravity CLI | `agy --dangerously-skip-permissions`; do not pair with `--sandbox` for full elevation | Auto-approves tool permission requests without terminal sandbox restrictions. |
| Cursor CLI | `agent --yolo --sandbox=disabled --approve-mcps` (`--yolo` is `--force`) | Force-allows commands unless explicitly denied, disables sandboxing, and approves MCP servers. |
| Opencode CLI | `opencode run --auto` (v1.17 renamed the old `--dangerously-skip-permissions`); for agent config set needed permission keys to `allow` / wildcard `{"*":"allow"}` | Auto-approves non-denied permissions; per-agent `allow` grants tools without prompts. |
| GitHub Copilot CLI | `copilot --allow-all` (alias `--yolo`) | Allows all available tools, all paths, and all URLs without approval. |

## Cursor CLI

Cursor CLI uses the `agent` command and the same tool-calling loop: the model emits a structured tool request, the runtime executes it, and results are appended to context before the next turn. There is no practical limit on tool calls per task.

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
| MCP tools | Hook matcher: `MCP:<tool>` (e.g. `MCP:search`). CLI permission pattern: `Mcp(server:tool)` (e.g. `Mcp(github:*)`) |
| `EditNotebook` | Edit Jupyter notebook cells |
| `Await` | Poll a background `Shell` session |
| `TabRead` / `TabWrite` | Editor tab read/write (hook matchers only) |

Agent also uses built-in **Explore**, **Bash**, and **Browser** subagents automatically for heavy search, shell series, and browser work. Custom subagents live in `.cursor/agents/*.md` and are invoked via `Task` or `/subagent-name` in chat.

### Skill invocation (not a hook tool type)

Skills are separate from the table above:

- Explicit: `/skill-name` in chat (e.g. `/release-notes`)
- Auto: agent loads skills whose `description` matches the request (unless `disable-model-invocation: true`)

Skill directories: project `.cursor/skills/`, `.agents/skills/`, `.claude/skills/`, `.codex/skills/`; user `~/.cursor/skills/`, `~/.agents/skills/`, `~/.claude/skills/`, `~/.codex/skills/` (compat).

### Subagents (`Task` tool)

| `subagent_type` | Role |
| :--- | :--- |
| `explore` | Parallel codebase search; keeps noise out of main context |
| `bash` | Isolated shell command batches (canonical type name; some community docs say `shell`) |
| `browser` | Browser control via MCP; filters DOM/screenshot noise |
| Custom | Any `name` from `.cursor/agents/<name>.md` |

Parallel work: multiple `Task` calls in one assistant turn (practical cap ~4 parallel subagents). Local async: set `is_background: true` in a subagent's `.cursor/agents/<name>.md` frontmatter and rejoin with the `Await` tool. For heavier isolation, Cursor can run up to 8 local agents in separate git worktrees. Resume with the agent ID from a prior subagent run.

Cursor **Cloud Agents** (formerly "Background Agents") run remotely and are out of policy here — use local subagents/worktrees instead (see [Agent Orchestration Model](#agent-orchestration-model)).

Cursor CLI subagent support is documented in [Subagents](https://cursor.com/docs/subagents).

### Modes and write access

| Mode | CLI flag / command | Tool writes |
| :--- | :--- | :--- |
| Agent | default | Full tools |
| Plan | `--mode=plan`, `/plan` | Read-only / planning |
| Ask | `--mode=ask`, `/ask` | Read-only Q&A |

Non-interactive CLI: `agent -p "prompt"` (`--print`) runs with full tools unless mode restricts edits. Use `--sandbox=disabled` only when the user wants auto-approved shell.

Highest elevated launch: `agent --yolo --sandbox=disabled --approve-mcps` for interactive sessions; in headless automation use `cursor-agent -p --force --sandbox=disabled --trust --approve-mcps "prompt"`. `--yolo` is an alias for `--force`.

Headless output: `--output-format text|json|stream-json` (with `--stream-partial-output` for incremental deltas). Auth via `CURSOR_API_KEY`. Useful CLI flags: `--worktree`, `--workspace <path>`, `--resume [thread-id]`; sessions managed with `agent ls` / `agent resume`.

### Permissions

Tool allow/deny uses pattern strings. Examples:

- `Shell(git)` — prefix match: any `git` subcommand. `Shell(**)` — all shell commands.
- `Mcp(server:tool)` — colon-separated (e.g. `Mcp(datadog:*)`, `Mcp(*:read_*)`).
- `Read(src/**/*.ts)`, `Write(<glob>)`, `WebFetch(*.example.com)` — file / web allowlists.
- Deny rules take precedence over allow rules.

Permission files:

- **CLI**: `~/.cursor/cli-config.json` (global) and `<root>/.cursor/cli.json` (per-project, layered git-root → cwd).
- **IDE only** (separate auto-run allowlist for editor): `~/.cursor/permissions.json` — uses `server:tool` for MCP and prefix matching for shell.

### Kit mapping (generic → Cursor)

See [`cursor-tools.md`](cursor-tools.md) for the full skill-kit → Cursor equivalence table.

## All runtimes (index)

| Runtime | Tool mapping | Skill invocation |
| :--- | :--- | :--- |
| Codex CLI | [`codex-tools.md`](codex-tools.md) | runtime skill activation command |
| Claude CLI | [`claude-tools.md`](claude-tools.md) | `/skill-name` |
| Antigravity CLI | [`antigravity-tools.md`](antigravity-tools.md) | runtime skill activation command |
| Cursor CLI | [`cursor-tools.md`](cursor-tools.md) (details in [Cursor section](#cursor-cli) above) | `/skill-name` |
| Opencode CLI | [`opencode-tools.md`](opencode-tools.md) | runtime skill activation command |
| GitHub Copilot CLI | [`copilot-tools.md`](copilot-tools.md) | runtime skill activation command |

### Context files (multi-repo workspaces)

| Artifact | Location | Steward |
| :--- | :--- | :--- |
| `CONTEXT.md` | `<artifacts-root>` | `grill-with-docs` |
| `docs/adr/` | `<artifacts-root>/docs/adr/` | `grill-with-docs` |

Native CLI memory defaults: [`memory-global-defaults.md`](memory-global-defaults.md).

### MCP placement (multi-repo workspaces)

Keep MCP configuration at workspace root for supported coding tools:

- Codex CLI: `<workspace-root>/.codex/config.toml`
- Claude CLI: `<workspace-root>/.claude/settings.local.json`
- Antigravity CLI: `<workspace-root>/.agents/mcp_config.json`
- Cursor CLI: `<workspace-root>/.cursor/mcp.json` (plus optional `~/.cursor/mcp.json` fallback)
- Opencode CLI: workspace-root `opencode.json` / MCP config where used
- GitHub Copilot CLI: `<workspace-root>/.mcp.json` or `<workspace-root>/.github/mcp.json` (user fallback: `~/.copilot/mcp-config.json`)

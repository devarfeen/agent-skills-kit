# Tool Calling Reference

How the six supported runtimes — Codex CLI, Claude CLI, Antigravity CLI, Cursor CLI, Opencode CLI, and GitHub Copilot CLI, no others — invoke tools, and how this kit maps generic skill instructions to each. Compatibility filenames do not imply support for any other runtime.

Zero attribution: omit co-author, AI, and tool attribution from all output. Use the current runtime's exposed tool schema when a mapping differs; these tables describe capabilities, not a guarantee that a tool is enabled in every session. Read-only role prompts are behavioral instructions; enforce access limits with runtime permissions when a hard boundary is needed.

> Last verified: 2026-09-28 against all six installed CLIs (codex-cli 0.158.0, claude 2.1.283, agy 1.2.12, cursor-agent 2026.09.26-dd393fe, opencode 1.18.33, copilot 1.0.88) — flag/command surface via installed `--help`; internal tool names via official docs or the shipped binary; re-verify on touch (see CONTRIBUTING sync map).

## Emitting into AGENTS.md

The `agents-md` generator fills its `### Runtime tool-calling` slot with exactly three untitled tables, one row per runtime in this file's order, cells copied verbatim, alignment row `| :--- |`:

1. `| Runtime | Skill invocation |` — from the **All runtimes (index)** table; drop its `Tool mapping` column.
2. `| Runtime | Parallel dispatch | Local background / async |` — from **Parallel & background mechanism by runtime**; drop `Custom agent files`.
3. `| Runtime | Highest elevated launch / preset | Effect |` — from **Highest elevated permission by runtime**.

## Agent Orchestration Model

The model itself is the `AGENTS.md` Non-negotiable rule **Local orchestration** (main session orchestrates role-typed local lanes and keeps the only seat for merge and final judgment); this file maps it to each runtime's concrete mechanisms. A runtime with no subagents uses a focused in-process tool pass per lane.

### Local-only policy (no cloud agents)

Use only **local** subagents and **local** background/async execution; local worktree-isolated parallel agents are allowed. Never delegate to cloud or remote background-agent products:

| Runtime | Cloud/remote product to AVOID | Local equivalent to use instead |
| :--- | :--- | :--- |
| Codex CLI | Codex Web delegated tasks | Available spawn tools (`spawn_agent`); `codex --worktree` managed worktrees |
| Claude CLI | Routines (`/schedule`), background agents on claude.ai; local agent teams are separately excluded by kit policy | `Agent` subagents; `run_in_background` Bash; `isolation: worktree` |
| Antigravity CLI | Managed Agents API / remote managed execution | `invoke_subagent` local subagents; `/schedule` timer or cron prompts |
| Cursor CLI | Cloud Agents (formerly "Background Agents"), `&`-prefixed cloud hand-off, cursor.com/agents | `Task` subagents; local worktree agents |
| Opencode CLI | (no cloud agent in scope) | `task` subagents; `task(background=true)` |
| GitHub Copilot CLI | Cloud coding agent via `/delegate` (runs in GitHub Actions, opens PRs) | `task` + `/fleet` subagents; `Ctrl+X → b` background |

### Canonical role lanes

Standard lane roles across this kit; each runtime's `*-tools.md` maps them to that runtime's concrete mechanism. No dedicated built-in for a role → use the general-purpose subagent with the listed tool profile.

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
| Codex CLI | Available spawn tools; `agents.max_concurrent_threads_per_session` controls capacity (`agents.max_threads` is a legacy alias) | Available wait / follow-up tools for local threads | `.codex/agents/<name>.toml` (or `~/.codex/agents/<name>.toml`) |
| Claude CLI | Multiple `Agent` calls in one turn | `run_in_background` Bash; `background: true` subagents | `.claude/agents/<name>.md` |
| Antigravity CLI | `invoke_subagent` (built-ins `research` / `browser` / `self`; `define_subagent` for ad-hoc types) | `/schedule` one-time timer or cron prompt; Artifacts for review | `.agents/agents/<name>.md` (global `~/.gemini/config/agents/<name>.md`) |
| Cursor CLI | Multiple `Task` calls in one turn (no documented cap) | `is_background: true` subagent (output under `~/.cursor/subagents/`); `Await` for background shells; `bash` subagent isolates output | `.cursor/agents/<name>.md` |
| Opencode CLI | Multiple `task` calls with `subagent_type` | `task(background=true)` (needs `OPENCODE_EXPERIMENTAL_BACKGROUND_SUBAGENTS=true`; completion is pushed back, no polling tool) | `.opencode/agents/<name>.md`, `~/.config/opencode/agents/<name>.md`, or inline `opencode.json` agents |
| GitHub Copilot CLI | `task` tool + `/fleet` (orchestrated parallel subagents; built-ins `explore` / `task` / `general-purpose` / `code-review` / `security-review` / `research` / `rubber-duck`) | `Ctrl+X → b` promotes a task or shell to background | `.github/agents/<name>.md` or `.agent.md` (user-scope `~/.copilot/agents/`) |

### Git worktree isolation by runtime

Verified against the installed CLI surface (`--help`, feature flags, shipped bundle) for Codex, Cursor, Copilot, and Opencode; against official docs for Antigravity. Plain `git worktree add` is the portable fallback everywhere — reach for a native surface only when it buys session-switching or setup scripts. Generated workspace rules require `<project-repo>/.worktrees/<task-name>`; of the surfaces below, only Copilot with `worktreePathTemplate` set to `{repoPath}/.worktrees/{branchSlug}`, or Claude `EnterWorktree` on a worktree first created there with Git, complies — otherwise use `git worktree add`.

| Runtime | Native surface | Location | Base ref |
| :--- | :--- | :--- | :--- |
| Claude CLI | `-w, --worktree [name]`; `EnterWorktree` / `ExitWorktree` (switches session cwd; fires only when the user or `CLAUDE.md` says "worktree"); `isolation: worktree` on subagents | `.claude/worktrees/<name>`; no CLI location setting (`worktree.location` is Desktop-SSH only); a `WorktreeCreate` hook replaces creation and may place it elsewhere | `worktree.baseRef` — `fresh` (default) = `origin/<default-branch>`, `head` = local HEAD |
| Cursor CLI | `-w, --worktree [name]`, `--worktree-base <branch>`, `--skip-worktree-setup`; setup scripts from `.cursor/worktrees.json` | `~/.cursor/worktrees/<reponame>/<name>` | current HEAD |
| GitHub Copilot CLI | `-w, --worktree[=NAME]` (documented; not in the 1.0.88 `--help` option list), `/worktree`, `/new worktree`, `/fork worktree`; `/move` carries uncommitted changes in. `--worktree` conflicts with `--resume` / `--continue` / `--connect` | `<repo>.worktrees/` (sibling); `worktreePathTemplate` overrides (`{repoPath}`, `{repo}`, `{branch}`, `{branchSlug}`) | `HEAD`; `worktreeBaseRef: "defaultBranch"` uses the remote default branch |
| Antigravity CLI | `invoke_subagent` with workspace mode `branch` (vs `inherit`, `share`); worktrees auto-cleaned when the subagent is killed | not documented | not documented |
| Opencode CLI | TUI-only: "Create new worktree" in the new-session picker, plus a per-project worktree startup script. No CLI flag. The new tab layout does not support worktrees yet | not documented | not documented |
| Codex CLI | `codex --worktree` (managed worktree; `worktrees` feature, stable and on) | `$CODEX_HOME/worktrees`; `desktop.git-worktree-root` (absolute path) overrides | not documented for the CLI |

### Highest elevated permission by runtime

| Runtime | Highest elevated launch / preset | Effect |
| :--- | :--- | :--- |
| Codex CLI | `codex --dangerously-bypass-approvals-and-sandbox` (or explicit `codex --sandbox danger-full-access --ask-for-approval never`) | No sandbox and no approval prompts. |
| Claude CLI | `claude --dangerously-skip-permissions` (equivalent to `--permission-mode bypassPermissions`) | Skips the permission layer; protected paths are allowed except hard circuit breakers. |
| Antigravity CLI | `agy --dangerously-skip-permissions`; do not pair with `--sandbox` for full elevation | Auto-approves tool permission requests without terminal sandbox restrictions. |
| Cursor CLI | `agent --yolo --sandbox=disabled --approve-mcps` (`--yolo` is `--force`) | Force-allows commands unless explicitly denied, disables sandboxing, and approves MCP servers. |
| Opencode CLI | `opencode --auto` for interactive sessions; `opencode run --auto` for non-interactive runs; verify installed help | Auto-approves permissions that are not explicitly denied. |
| GitHub Copilot CLI | `copilot --allow-all` (alias `--yolo`) | Allows all available tools, all paths, and all URLs without approval. |

## All runtimes (index)

| Runtime | Tool mapping | Skill invocation |
| :--- | :--- | :--- |
| Codex CLI | [`codex-tools.md`](codex-tools.md) | `$skill-name` inline mention, or the `/skills` command |
| Claude CLI | [`claude-tools.md`](claude-tools.md) | `/skill-name`, or auto on `description` match |
| Antigravity CLI | [`antigravity-tools.md`](antigravity-tools.md) | auto from `description`; name the skill to force activation |
| Cursor CLI | [`cursor-tools.md`](cursor-tools.md) | `/skill-name`, or auto on `description` match |
| Opencode CLI | [`opencode-tools.md`](opencode-tools.md) | auto via the `skill` tool on `description` match |
| GitHub Copilot CLI | [`copilot-tools.md`](copilot-tools.md) | `/skill-name` |

### Context files (multi-repo workspaces)

| Artifact | Location | Steward |
| :--- | :--- | :--- |
| `CONTEXT.md` | `<artifacts-root>` | `grill-with-docs` |
| `specs/adr/` | `<artifacts-root>/specs/adr/` | `grill-with-docs` |

Native CLI memory defaults: [`memory-global-defaults.md`](memory-global-defaults.md).

### MCP placement (multi-repo workspaces)

Keep MCP configuration at workspace root for supported coding tools:

- Codex CLI: `<workspace-root>/.codex/config.toml`
- Claude CLI: `<workspace-root>/.mcp.json` for project-scoped servers; `.claude/settings.local.json` holds local settings, not server definitions
- Antigravity CLI: `<workspace-root>/.agents/mcp_config.json`
- Cursor CLI: `<workspace-root>/.cursor/mcp.json` (plus optional `~/.cursor/mcp.json` fallback)
- Opencode CLI: workspace-root `opencode.json` / MCP config where used
- GitHub Copilot CLI: `<workspace-root>/.mcp.json` or `<workspace-root>/.github/mcp.json` (user fallback: `~/.copilot/mcp-config.json`)

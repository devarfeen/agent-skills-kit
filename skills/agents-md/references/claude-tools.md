Tool-calling index: [`tool-calling.md`](tool-calling.md).

> Last verified: 2026-09-28 against installed claude 2.1.283 — flag/command surface via installed `--help`; internal tool names via official docs or the shipped binary; re-verify on touch (see CONTRIBUTING sync map).

Authoritative tool reference: https://code.claude.com/docs/en/tools-reference

Zero attribution: omit co-author, AI, and tool attribution from all output.

| Skill Reference | Claude CLI Equivalent |
| :--- | :--- |
| `Read` (file reading) | `Read` |
| `Write` (file creation) | `Write` |
| `Edit` (file editing) | `Edit` |
| `Bash` (run commands) | `Bash` |
| `Grep` (search content) | `Grep` |
| `Glob` (search by name) | `Glob` |
| `TodoWrite` (task tracking) | `TaskCreate` / `TaskGet` / `TaskList` / `TaskUpdate` (`TodoWrite` is disabled by default; task tools ship by default only on Claude 3.x, Opus 4–4.7, Sonnet 4–4.6, and Haiku 4.5 — other models get none unless opted in) |
| `Task` tool (dispatch subagent) | `Agent` (spawns a subagent in its own context window and returns the final result) |
| `WebSearch` | `WebSearch` |
| `WebFetch` | `WebFetch` |
| Skill invocation | `/skill-name`, the built-in `Skill` tool, or automatic loading when the request matches the skill `description` |

**Key Notes:**

- Tool names are the exact strings used in permission rules (`permissions.allow`/`deny`), subagent `tools` lists, and hook matchers. Permission patterns also accept file globs and domain filters: `Read(~/secrets/**)`, `Edit(/src/**)`, `Agent(Explore)`, `WebFetch(domain:example.com)`.
- Task tracking uses `TaskCreate` / `TaskGet` / `TaskList` / `TaskUpdate` / `TaskStop`. `TodoWrite` is disabled by default; set `CLAUDE_CODE_ENABLE_TASKS=0` to re-enable it.
- `allowed-tools` pre-approves listed tools during the invoking turn; it does not restrict which tools are callable. Use permission deny rules or supported `disallowed-tools` to restrict access. Verified 2026-09-09 against [skill permissions](https://code.claude.com/docs/en/skills#pre-approve-tools-for-a-skill).
- Claude CLI reads `CLAUDE.md`, not `AGENTS.md`, as its canonical workspace file; keep `AGENTS.md` canonical and write a `CLAUDE.md` shim importing only it (`@AGENTS.md`) — the pattern the `agents-md` skill emits.
- **Memory:** auto memory is on by default (`autoMemoryEnabled` in settings; `/memory` to toggle); native project memory is user-local. Do not create, import, symlink, or sync repo memory files. See [`memory-global-defaults.md`](memory-global-defaults.md).
- Other built-in tools available for permission / hook matchers: `AskUserQuestion`, `EnterPlanMode` / `ExitPlanMode`, `EnterWorktree` / `ExitWorktree`, `LSP`, `Monitor`, `NotebookEdit`, `PowerShell` (Windows default; opt-in elsewhere via `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`), `ToolSearch`, `WaitForMcpServers`, `ScheduleWakeup`, `PushNotification`, `RemoteTrigger`, `SendMessage`, `ShareOnboardingGuide`, `Artifact`, `EndConversation`, `ListAgents`, `ReportFindings`, `SendFeedback`, `SendUserFile`, `Skill`, `SubagentHandback`, `TaskOutput` (deprecated), `Workflow`, `CronCreate` / `CronList` / `CronDelete`, `ListMcpResourcesTool` / `ReadMcpResourceTool`.
- `EnterWorktree` switches the session's cwd into a worktree it creates under `.claude/worktrees/`, and only fires when the user or `CLAUDE.md` says "worktree". Its base ref follows the `worktree.baseRef` setting — `fresh` (default) branches from `origin/<default-branch>`, so local unpushed commits are absent; `head` branches from local HEAD. To land a worktree under the project-local `.worktrees/` path the generated rules mandate, `git worktree add .worktrees/<name>` first, then `EnterWorktree` with that `path` — a path outside `.claude/worktrees/` prompts for approval. `ExitWorktree` takes `keep` or `remove`. No CLI setting moves `.claude/worktrees/` (`worktree.location` is read only by Desktop for SSH sessions); a `WorktreeCreate` hook replaces creation entirely.
- Multi-repo workspace policy: use workspace-root MCP config.
- Highest elevated permission launch: `claude --dangerously-skip-permissions`, equivalent to `claude --permission-mode bypassPermissions`. This bypasses the permission layer.
- For exact config-file placement by tool, use [`tool-calling.md`](tool-calling.md).

## Agents: parallel, background & roles

Parallel: issue multiple available `Agent` calls for independent work, using the selector in the live tool schema. Local background: `run_in_background: true` on `Bash`; a supported `background: true` subagent or Ctrl+B; `isolation: worktree` separates files. Inspect task controls in the installed runtime before managing them. Cloud Routines and background agents on claude.ai are out of scope. [Agent teams](https://code.claude.com/docs/en/agent-teams) run locally, but the kit separately excludes them. Do not infer a hard tool boundary from a role's name.

| Role | Claude CLI mechanism |
| :--- | :--- |
| Orchestrator | main session (owns merge + final judgment) |
| Explorer | `Agent` → `Explore` (read-only, fast model) |
| Researcher | `Agent` → `general-purpose` + `WebSearch` / `WebFetch` |
| Planner | `Agent` → `Plan` (read-only) |
| Implementer | `Agent` → `general-purpose`, or a write-enabled custom `.claude/agents/<name>.md` |
| Reviewer | custom read-only agent (`tools: Read, Grep, Glob`) |
| Tester | `Agent` → `general-purpose`, or `run_in_background` Bash for long suites |
| Tool-runner | `run_in_background` Bash, or a custom agent scoped to `Bash` |

Custom-agent frontmatter: `name`, `description`, `tools` / `disallowedTools`, `model`, `permissionMode`, `maxTurns`, `background`, `isolation: worktree`, `skills`, `mcpServers`, `hooks`, `memory`, `effort`, `color`, `initialPrompt`, `omitClaudeMd`, `experimental`. To restrict which subagents a main-thread agent can spawn, use `Agent(type1, type2)` in `tools`.

Tool-calling index: [`tool-calling.md`](tool-calling.md).

Authoritative tool reference: https://code.claude.com/docs/en/tools-reference

| Skill Reference | Claude CLI Equivalent |
| :--- | :--- |
| `Read` (file reading) | `Read` |
| `Write` (file creation) | `Write` |
| `Edit` (file editing) | `Edit` |
| `Bash` (run commands) | `Bash` |
| `Grep` (search content) | `Grep` |
| `Glob` (search by name) | `Glob` |
| `TodoWrite` (task tracking) | `TaskCreate` / `TaskGet` / `TaskList` / `TaskUpdate` (`TodoWrite` is disabled by default as of v2.1.142) |
| `Task` tool (dispatch subagent) | `Agent` (spawns a subagent in its own context window and returns the final result) |
| `WebSearch` | `WebSearch` |
| `WebFetch` | `WebFetch` |
| Skill invocation | `/skill-name`, the built-in `Skill` tool, or automatic loading when the request matches the skill `description` |

**Key Notes:**

- Tool names are the exact strings used in permission rules (`permissions.allow`/`deny`), subagent `tools` lists, and hook matchers. Permission patterns also accept file globs and domain filters: `Read(~/secrets/**)`, `Edit(/src/**)`, `Agent(Explore)`, `WebFetch(domain:example.com)`.
- The subagent tool is `Agent`. It runs autonomously in a separate context window and returns a single text result; parallel work means multiple `Agent` calls in one turn.
- Skills run through the built-in `Skill` tool — there is no separate per-skill tool entry. Invoke directly with `/skill-name`, or let Claude CLI auto-load a skill when the request matches its `description`.
- Task tracking uses `TaskCreate` / `TaskGet` / `TaskList` / `TaskUpdate` / `TaskStop`. `TodoWrite` is disabled by default; set `CLAUDE_CODE_ENABLE_TASKS=0` to re-enable it.
- Skills support `allowed-tools` frontmatter to restrict which tools a skill may use.
- Claude CLI reads `CLAUDE.md` as its canonical workspace file, not `AGENTS.md`. To share rules across runtimes, keep `AGENTS.md` canonical and write a `CLAUDE.md` shim that imports only it (e.g. `@AGENTS.md`) — this is the pattern the `agents-md` skill emits.
- **Memory:** Auto memory is on by default (`autoMemoryEnabled` in settings; `/memory` to toggle). Native project memory is user-local. Do not create, import, symlink, or sync repo memory files. See [`memory-global-defaults.md`](memory-global-defaults.md).
- Other built-in tools available for permission / hook matchers: `AskUserQuestion`, `EnterPlanMode` / `ExitPlanMode`, `EnterWorktree` / `ExitWorktree`, `LSP`, `Monitor`, `NotebookEdit`, `PowerShell` (Windows default; opt-in elsewhere via `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`), `ToolSearch`, `WaitForMcpServers`, `ScheduleWakeup`, `PushNotification`, `RemoteTrigger`, `SendMessage`, `ShareOnboardingGuide`, `TeamCreate` / `TeamDelete` (gated by `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`), `CronCreate` / `CronList` / `CronDelete`, `ListMcpResourcesTool` / `ReadMcpResourceTool`.
- Multi-repo workspace policy: use workspace-root MCP config.
- Highest elevated permission launch: `claude --dangerously-skip-permissions`, equivalent to `claude --permission-mode bypassPermissions`. This bypasses the permission layer; use only in isolated containers, VMs, or disposable worktrees.
- For exact config-file placement by tool, use [`tool-calling.md`](tool-calling.md).

## Agents: parallel, background & roles

Parallel: issue multiple `Agent` calls in one turn (each runs in its own context window and returns one summary). The subagent selector parameter is `agent_type`. Local background: `run_in_background: true` on `Bash`; mark a subagent `background: true` in `.claude/agents/<name>.md` (background subagents auto-deny permission prompts) or press Ctrl+B; add `isolation: worktree` for file isolation. List/stop background **Bash** tasks with `/tasks` (also via `TaskList` / `TaskStop`); manage background **subagents** via `/agents` (Running tab). Subagents cannot spawn subagents. Fork the current conversation via the `Agent` tool's fork mode (a forked Agent inherits the parent conversation and always runs in background). Cloud features (Routines via `/schedule` / `RemoteTrigger`, agent teams behind `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, background agents on claude.ai) are out of scope here — kit policy is local-only.

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

Custom-agent frontmatter: `name`, `description`, `tools` / `disallowedTools`, `model`, `permissionMode`, `maxTurns`, `background`, `isolation: worktree`, `skills`, `mcpServers`, `hooks`, `memory`, `effort`, `color`, `initialPrompt`. To restrict which subagents a main-thread agent can spawn, use `Agent(type1, type2)` in `tools`. Task tracking uses `TaskCreate` / `TaskGet` / `TaskList` / `TaskUpdate` / `TaskStop`.

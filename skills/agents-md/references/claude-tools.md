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
| `Task` tool (dispatch subagent) | `Agent` (spawns a subagent in its own context window; returns only the final result) |
| `WebSearch` | `WebSearch` |
| `WebFetch` | `WebFetch` |
| Skill invocation | `/skill-name`, the built-in `Skill` tool, or automatic loading when the request matches the skill `description` |

**Key Notes:**

- Tool names are the exact strings used in permission rules (`permissions.allow`/`deny`), subagent `tools` lists, and hook matchers.
- The subagent tool is `Agent`, not `Task`. It runs the subagent autonomously in a separate context window and returns a single text result; parallel work means multiple `Agent` calls in one turn.
- Skills run through the built-in `Skill` tool — there is no separate per-skill tool entry. Invoke directly with `/skill-name`, or let Claude CLI auto-load a skill when the request matches its `description`.
- `TodoWrite` is disabled by default as of v2.1.142 in favor of the `TaskCreate` / `TaskGet` / `TaskList` / `TaskUpdate` task tools. Set `CLAUDE_CODE_ENABLE_TASKS=0` to re-enable `TodoWrite`.
- Skills support `allowed-tools` frontmatter to restrict which tools a skill may use.
- Multi-repo workspace policy: use workspace-root MCP config.
- For exact config-file placement by tool, use [`tool-calling.md`](tool-calling.md).

## Agents: parallel, background & roles

Parallel: issue multiple `Agent` calls in one turn (each runs in its own context window and returns one summary). The subagent selector parameter is `agent_type` (older `subagent_type` still works). Local background: `run_in_background: true` on `Bash`; mark a subagent `background: true` in `.claude/agents/<name>.md` (background subagents auto-deny permission prompts) or press Ctrl+B; add `isolation: worktree` for file isolation. List/stop background work with `/tasks`. Subagents cannot spawn subagents. There is no first-party cloud agent — keep all work local.

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

Custom-agent frontmatter: `name`, `description`, `tools` / `disallowedTools`, `model`, `permissionMode`, `background`, `isolation: worktree`, `skills`, `mcpServers`. Task tracking uses `TaskCreate` / `TaskGet` / `TaskList` / `TaskUpdate` / `TaskStop`.

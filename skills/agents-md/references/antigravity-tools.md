Tool-calling index: [`tool-calling.md`](tool-calling.md).

| Skill Reference | Antigravity CLI Equivalent |
| :--- | :--- |
| `Read` (file reading) | `read_file` |
| `Write` (file creation) | `write_file` |
| `Edit` (file editing) | `replace` |
| `Bash` (run commands) | `run_shell_command` |
| `Grep` (search content) | `grep_search` |
| `Glob` (search by name) | `glob` |
| `TodoWrite` (task tracking) | `write_todos` |
| `Skill` tool (invoke a skill) | `activate_skill` |
| `WebSearch` | `google_web_search` |
| `WebFetch` | `web_fetch` |
| `Task` tool (dispatch subagent) | `/goal` → orchestrator auto-spawns dynamic subagents (no built-in `@agent` personas; `@` includes files/context) |

**Key Notes:**

- `@` references files/context (e.g. `@src/main.go`), not agents. There are no built-in `@generalist` / `@code-reviewer` personas.
- Parallelism comes from the Agent Manager and `/goal`: the orchestrator decomposes a goal and spawns dynamic, auto-named subagents (dependency-aware). Reusable personas (`@pm`, `@engineer`, `@qa`) are user-defined in `.agents/agents.md`.
- The tool names above are not confirmed against current Antigravity docs (some may be inherited from earlier Gemini CLI); verify before relying on exact names. Reads both `AGENTS.md` and `GEMINI.md` (GEMINI.md wins on conflict).
- Multi-repo workspace policy: use workspace-root MCP config.
- For exact config-file placement by tool, use [`tool-calling.md`](tool-calling.md).

## Agents: parallel, background & roles

Parallelism is built into the **Agent Manager**: `/goal` makes the orchestrator decompose work and spawn dynamic, auto-named subagents (dependency-aware; ~5 parallel instances typical). Local background: `/schedule` runs cron-style tasks that survive app close, and Artifacts (plans, diffs, walkthroughs) are written to a folder you review on return. **Managed Agents API / remote managed execution** is cloud — do not use it. Define reusable personas in `.agents/agents.md` (e.g. `@pm`, `@engineer`, `@qa`, `@devops`) and wire order via `.agents/workflows/`.

| Role | Antigravity mechanism |
| :--- | :--- |
| Orchestrator | lead agent / `/goal` (owns merge + final judgment) |
| Explorer | dynamic read-only subagent |
| Researcher | dynamic subagent + web tools |
| Planner | planning mode (`/goal` task groups, Artifacts) |
| Implementer | dynamic worker subagent or `@engineer` persona |
| Reviewer | `@qa` / reviewer persona in `.agents/agents.md` |
| Tester | dynamic subagent running tests/build |
| Tool-runner | dynamic subagent (shell) |

MCP: project `.agents/mcp_config.json`; remote HTTP entries use `serverUrl`. Skills: `.agents/skills/<name>/SKILL.md`.

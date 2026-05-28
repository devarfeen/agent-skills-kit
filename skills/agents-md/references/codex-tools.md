Tool-calling index: [`tool-calling.md`](tool-calling.md).

| Skill Reference | Codex Equivalent |
| :--- | :--- |
| `Task` tool (dispatch subagent) | `spawn_agent` |
| Send more input to a running subagent | `send_input` |
| Resume a paused subagent thread | `resume_agent` |
| Task returns result | `wait_agent` |
| Task completes automatically | `close_agent` to free slot |
| Batch fan-out from CSV | `spawn_agents_on_csv` (each worker calls `report_agent_job_result` once) |
| `TodoWrite` (task tracking) | `update_plan` |
| `Skill` tool (invoke a skill) | `/skills` slash command or `$skill-name` inline mention; auto-loaded from `.agents/skills/`, `~/.agents/skills/`, `/etc/codex/skills/` |

**Key Notes:**
- Subagent workflows are on by default. Config lives in `~/.codex/config.toml` (global) or `<workspace-root>/.codex/config.toml` (project).
- Codex CLI reads `AGENTS.md` (and `AGENTS.override.md`, which wins) hierarchically from `~/.codex` and from repo root down to CWD, capped at `project_doc_max_bytes` (32 KiB default). The `child_agents_md` feature flag layers additional per-directory guidance.
- **Memory:** Off by default. Enable globally: `[features] memories = true` and `[memories] use_memories` / `generate_memories` in `~/.codex/config.toml`. Private store: `~/.codex/memories/`. Team SSOT: `<repo-root>/MEMORY.md` + `AGENTS.md`. `/memory-steward` for repo file hygiene. See [`memory-global-defaults.md`](memory-global-defaults.md).
- Multi-repo workspace policy: use workspace-root MCP config.
- For exact config-file placement by tool, use [`tool-calling.md`](tool-calling.md).

## Agents: parallel, background & roles

The orchestrator dispatches workers via `spawn_agent` / `send_input` / `resume_agent` / `wait_agent` / `close_agent`, plus `spawn_agents_on_csv` for batch fan-out (each worker calls `report_agent_job_result` once). Limits live under `[agents]`: `max_threads` (default 6), `max_depth` (default 1 — workers cannot spawn workers), `job_max_runtime_seconds` (fallback 1800). Switch between live threads with `/agent`. **Worktrees** and **Automations** are Codex *app* features, not CLI features. **Codex Web** runs tasks remotely — kit policy is local-only, so do not use it.

Built-in roles: `default`, `worker`, `explorer`. Custom roles live in standalone `.codex/agents/<name>.toml` or `~/.codex/agents/<name>.toml` files. Required fields: `name`, `description`, `developer_instructions`. Optional: `model`, `model_reasoning_effort`, `sandbox_mode`, `mcp_servers`, `skills.config`, `nickname_candidates`.

| Role | Codex mechanism |
| :--- | :--- |
| Orchestrator | root Codex session |
| Explorer | `explorer` built-in role (read-only sandbox) |
| Researcher | `worker` or custom role + MCP / web |
| Planner | Plan mode (`update_plan`) |
| Implementer | `worker` role |
| Reviewer | custom `.codex/agents/<name>.toml` role, read-only sandbox |
| Tester | `worker` role running tests/build |
| Tool-runner | `worker` role |

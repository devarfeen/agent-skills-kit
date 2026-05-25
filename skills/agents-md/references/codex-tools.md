Tool-calling index: [`tool-calling.md`](tool-calling.md).

| Skill Reference | Codex Equivalent |
| :--- | :--- |
| `Task` tool (dispatch subagent) | `spawn_agent` |
| Task returns result | `wait_agent` |
| Task completes automatically | `close_agent` to free slot |
| `TodoWrite` (task tracking) | `update_plan` |
| `Skill` tool (invoke a skill) | runtime skill activation (verify exact syntax in Codex docs) |

**Key Notes:**
- Requires `multi_agent = true` under the `[features]` table in `config.toml` (`~/.codex/config.toml` global or `.codex/config.toml` project); toggle at runtime with `/experimental`.
- Multi-repo workspace policy: use workspace-root MCP config and one workspace memtrace server (`memtrace serve --dir <workspace-root>`), not repo-level memtrace MCP entries.
- Understand-Anything policy: keep each project graph in `<project-root>/.understand-anything/knowledge-graph.json`, not workspace root.
- For exact config-file placement by tool, use [`tool-calling.md`](tool-calling.md).

## Agents: parallel, background & roles

With `[features] multi_agent = true`, the model dispatches workers via `spawn_agent` / `wait_agent` / `close_agent` (and `spawn_agents_on_csv` for batch fan-out, where each worker calls `report_agent_job_result` once). Limits live under `[agents]`: `max_threads` (default 6), `max_depth` (default 1 — workers cannot spawn workers), `job_max_runtime_seconds` (default 1800). Switch between live threads with `/agent`. Local background: git worktrees and local Automations. **Codex Cloud / Codex web** delegated tasks are remote — do not use them.

Built-in roles: `default`, `worker`, `explorer`, `monitor`. Custom roles: a `[agents.<name>]` block in `config.toml` pointing at a `config_file` (per-role TOML with `model`, `sandbox_mode`, `developer_instructions`, MCP servers), or a standalone `.codex/agents/<name>.toml` / `~/.codex/agents/<name>.toml`.

| Role | Codex mechanism |
| :--- | :--- |
| Orchestrator | root Codex session |
| Explorer | `explorer` built-in role (read-only sandbox) |
| Researcher | `worker` or custom role + MCP / web |
| Planner | Plan mode (`update_plan`) |
| Implementer | `worker` role |
| Reviewer | custom `[agents.<name>]` role, read-only sandbox |
| Tester | `worker` role running tests/build |
| Tool-runner | `worker` / `monitor` role |

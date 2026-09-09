Tool-calling index: [`tool-calling.md`](tool-calling.md).

Zero attribution: omit co-author, AI, and tool attribution from all output. The live tool schema wins over cached names below; tool names and availability vary by host.

> Last verified: 2026-07-06 against installed codex-cli 0.142.5 — flag/command surface via `--help`; internal tool names, config schemas, and chat slash commands are docs-level and re-verified on touch (see CONTRIBUTING sync map).

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
- **Memory:** off by default; enable with `[features] memories = true` and `[memories] use_memories` / `generate_memories` in `~/.codex/config.toml`. Native store: `~/.codex/memories/`. Do not create or sync repo memory files. See [`memory-global-defaults.md`](memory-global-defaults.md).
- Multi-repo workspace policy: use workspace-root MCP config.
- Highest elevated permission launch: `codex --dangerously-bypass-approvals-and-sandbox` (or explicit `codex --sandbox danger-full-access --ask-for-approval never`). This removes sandboxing and approval prompts; use only in an external sandbox or disposable worktree.
- For exact config-file placement by tool, use [`tool-calling.md`](tool-calling.md).

## Agents: parallel, background & roles

The orchestrator uses the available spawn and coordination tools. Under `[agents]`, use `max_concurrent_threads_per_session`; `max_threads` remains a legacy alias. When unset, the runtime chooses capacity. Check actual nesting limits and permissions instead of assuming six workers or depth one. Switch between live threads with `/agent`. Codex Web tasks are remote and excluded by kit policy. Verified 2026-09-09 against [official subagent configuration](https://learn.chatgpt.com/docs/agent-configuration/subagents) and installed codex-cli 0.153.4.

Built-in roles: `default`, `worker`, `explorer`. Custom roles live in standalone `.codex/agents/<name>.toml` or `~/.codex/agents/<name>.toml` files. Required fields: `name`, `description`, `developer_instructions`. Optional: `model`, `model_reasoning_effort`, `sandbox_mode`, `mcp_servers`, `skills.config`, `nickname_candidates`.

| Role | Codex mechanism |
| :--- | :--- |
| Orchestrator | root Codex session |
| Explorer | `explorer` built-in role for read-heavy work; explicitly configure a read-only sandbox when required |
| Researcher | `worker` or custom role + MCP / web |
| Planner | Plan mode (`update_plan`) |
| Implementer | `worker` role |
| Reviewer | custom `.codex/agents/<name>.toml` role, read-only sandbox |
| Tester | `worker` role running tests/build |
| Tool-runner | `worker` role |

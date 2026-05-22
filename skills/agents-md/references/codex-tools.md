Tool-calling index: [`tool-calling.md`](tool-calling.md).

| Skill Reference | Codex Equivalent |
| :--- | :--- |
| `Task` tool (dispatch subagent) | `spawn_agent` |
| Task returns result | `wait_agent` |
| Task completes automatically | `close_agent` to free slot |
| `TodoWrite` (task tracking) | `update_plan` |
| `Skill` tool (invoke a skill) | Skills load natively |

**Key Notes:**
- Requires `multi_agent = true` in `~/.codex/config.toml`.
- Multi-repo workspace policy: use workspace-root MCP config and one workspace memtrace server (`memtrace serve --dir <workspace-root>`), not repo-level memtrace MCP entries.
- Understand-Anything policy: keep each project graph in `<project-root>/.understand-anything/knowledge-graph.json`, not workspace root.
- For exact config-file placement by tool, use [`tool-calling.md`](tool-calling.md).

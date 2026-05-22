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

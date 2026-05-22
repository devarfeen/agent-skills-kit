Tool-calling index: [`tool-calling.md`](tool-calling.md).

| Skill Reference | Opencode Equivalent |
| :--- | :--- |
| `Read` (file reading) | `cat` |
| `Write` (file creation) | `tee` |
| `Edit` (file editing) | `sed` / `patch` |
| `Bash` (run commands) | `sh` |
| `Skill` tool (invoke a skill) | Loads via `.opencode/skills/` |

**Key Notes:**

- Opencode CLI uses POSIX-style tool naming for its internal mapping.
- Multi-repo workspace policy: use workspace-root MCP config and one workspace memtrace server (`memtrace serve --dir <workspace-root>`), not repo-level memtrace MCP entries.
- Understand-Anything policy: keep each project graph in `<project-root>/.understand-anything/knowledge-graph.json`, not workspace root.
- For exact config-file placement by tool, use [`tool-calling.md`](tool-calling.md).

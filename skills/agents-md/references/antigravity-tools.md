Tool-calling index: [`tool-calling.md`](tool-calling.md).

> Last verified: 2026-09-28 against installed agy (Antigravity) 1.2.12 — flag/command surface via installed `--help`; internal tool names via official docs or the shipped binary; re-verify on touch (see CONTRIBUTING sync map).

| Skill Reference | Antigravity CLI Equivalent |
| :--- | :--- |
| `Read` (file reading) | `view_file` |
| `Write` (file creation) | `write_to_file` |
| `Edit` (file editing) | `replace_file_content` / `multi_replace_file_content` |
| `Bash` (run commands) | `run_command` |
| `Grep` (search content) | `code_search` (`grep_search` left the default toolset in 1.2.7) |
| `Glob` (search by name) | `glob` |
| `Skill` tool (invoke a skill) | auto-activated from `SKILL.md` metadata (no explicit tool; mention skill name to force activation) |
| `WebSearch` | `search_web` |
| `WebFetch` | `read_url_content` |
| `Task` tool (dispatch subagent) | `invoke_subagent` (built-ins `research`, `browser`, `self`); `define_subagent`, `send_message` |

**Key Notes:**

- `@` references files/context (e.g. `@src/main.go`), not agents.
- Antigravity CLI reads `AGENTS.md` directly from the active workspace; it is the canonical instruction file, and this kit emits no Antigravity-specific shim.
- **Memory:** no native memory file store; use generated `AGENTS.md` and binding context files. No repo memory files or memory MCP servers for this kit. See [`memory-global-defaults.md`](memory-global-defaults.md).
- Multi-repo workspace policy: use workspace-root MCP config.
- For exact config-file placement by tool, use [`tool-calling.md`](tool-calling.md).

## Agents: parallel, background & roles

Parallelism is built into the **Agent Manager**: `invoke_subagent` spawns dynamic, dependency-aware subagents whose workspace mode is `inherit` (parent's workspace), `branch` (isolated Git worktree, auto-cleaned on kill), or `share` (shared directory storage) (clean context window, same model; concurrency limit not publicly documented). Local background: `/schedule` sets a one-time timer or recurring cron prompt; Artifacts (plans, diffs, walkthroughs) are written to a folder for review on return. **Managed Agents API / remote managed execution** is cloud — do not use it.

| Role | Antigravity mechanism |
| :--- | :--- |
| Orchestrator | lead agent / Agent Manager (owns merge + final judgment) |
| Explorer | `invoke_subagent` with a read-only subagent definition |
| Researcher | `invoke_subagent` + `search_web` / `read_url_content` |
| Planner | planning mode (task groups, Artifacts) |
| Implementer | `invoke_subagent` with a write-enabled subagent definition |
| Reviewer | `invoke_subagent` with a read-only reviewer subagent definition |
| Tester | `invoke_subagent` running tests / build |
| Tool-runner | `invoke_subagent` scoped to shell; built-in `browser` subagent for browser sequences |

MCP: project `.agents/mcp_config.json`; remote HTTP entries use `serverUrl`. Skills: project `.agents/skills/<name>/SKILL.md`; user-global `~/.gemini/antigravity/skills/<name>/` (also `.agent/skills/` accepted as a back-compat path).

## Permissions, hooks, slash commands

- **Permission resources** (config + `/permissions`): `view_file`, `write_to_file`, plus MCP-tool filtering. Rules use `action(target)` form with Allow / Deny / Ask lists.
- **Permission modes**: `request-review` (default), `proceed-in-sandbox`, `always-proceed`, `strict`.
- **Highest elevated permission launch**: `agy --dangerously-skip-permissions`. Do not combine it with `--sandbox` when the goal is full elevation; `--sandbox` enables terminal restrictions.
- **Hooks**: `PreToolUse` / `PostToolUse` with regex `matcher` on tool name; JSON schema includes `toolCall.name`, `toolCall.args`, `stepIdx`, plus common fields (`conversationId`, `workspacePaths`, `transcriptPath`, `artifactDirectoryPath`). Hook decision values: `allow`, `deny`, `ask`.
- **Useful slash commands**: `/goal`, `/grill-me`, `/schedule`, `/browser`, `/permissions`, `/btw`, `/model`.
- **Non-interactive**: `agy -p "<prompt>"` for pipelines.

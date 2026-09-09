# Intake

Four decisions, asked as one batched question set after Discover. Reuse choices the user already supplied. Respect the question tool's option and question limits, splitting the batch when required; free-text replies remain available. Zero attribution: omit co-author, AI, and tool attribution from all output.

## 1. Which coding agent

Ask by **product name**. Never label an option with a bare binary — Cursor's binary is `agent`, and an option reading `agent` names no product the user recognizes. The command belongs in the option's description, the product name in its title.

| Runtime | herdr `--kind` | Launch token |
| :--- | :--- | :--- |
| Codex CLI | `codex` | `codex` |
| Claude CLI | `claude` | `claude` |
| Antigravity CLI | `agy` | `agy` |
| Cursor CLI | `cursor` | `agent` (installs also expose `cursor-agent`) |
| Opencode CLI | `opencode` | `opencode` |
| GitHub Copilot CLI | `copilot` | `copilot` |

These six are the kit's supported runtimes. Name every one whose launch token resolves on PATH and which are missing. If the question tool cannot show the full roster, split the choices into supported batches or use a plain-text question; never exceed its schema limits.

**`AGENT_KIND` comes from this table, never from `CODING_CLI`'s first token.** For Cursor the two differ, so deriving the kind from the command yields `agent`, which `herdr agent start --kind` rejects. Worker-tab labels use the runtime's launch token so they stay readable.

## 2. Which permission mode

A fresh session pauses at its own approval prompts (shell, tracker, test commands) unless launched with an auto-accept preset or the folder pre-approves them. Offer, for the chosen runtime:

- its elevated interactive preset from the workspace's Runtime tool-calling table, verified against the installed CLI's `--help`; if the table is absent, derive the offered flags from that help and explain their effect
- the **bare launch token**, with the consequence stated: every worker pauses at its own approvals

Never pick an elevated mode yourself. Elevation requires the user's explicit choice. A worktree separates files, but does not sandbox commands, credentials, or network access; an external container or VM supplies that boundary. Do not pass non-interactive subcommands such as `opencode run` through `agent start`; verify flags on the interactive launch command.

The answer becomes `CODING_CLI`: the launch token plus flags. Under `herdr agent start`, flags go after `--`, never inside `--kind`.

## 3. How the work is isolated

Name the affected issues and their repos in the question, then offer:

| Mode | Each worker gets | Concurrency | Cost |
| :--- | :--- | :--- | :--- |
| `worktree` | its own git worktree and branch | parallel, no collisions | one checkout per issue on disk |
| `branch` | its own branch in the shared checkout | **serial only** — one checkout cannot hold two branches at once | none |
| `shared` | the orchestrator's folder and branch | parallel, collisions possible | none |

`worktree` is the recommended default whenever more than one open sub-issue touches the same repo — it is the only mode that makes same-repo parallelism safe, and the kit's guide already sanctions locally worktree-isolated agents.

`branch` cannot run parallel workers against one repo: two workers checking out two branches in one working folder overwrite each other. Choosing `branch` for a same-repo set means serial dispatch — say that in the question rather than discovering it at fan-out.

Ask for a branch name pattern, defaulting to the tracker's own: Linear supplies `gitBranchName` per issue; GitHub has no native name, so use `<issue-number>-<slug>`.

**User away:** retain an already chosen mode. If the user has not chosen one, stop before creating workers. Never fan out unattended into `shared` with a same-repo collision.

## 4. Leftover tabs and agents

Tabs labelled `[<launch token>] - <TRACKER_TAG> #<n>`, or live agents holding those slugs, survive from a previous run of this spec. List both per **Context** in [`herdr-commands.md`](herdr-commands.md) and ask whether to monitor them instead of re-creating; re-running blindly creates a second tab per issue, and a surviving agent name blocks `agent start` outright.

**User away →** monitor the existing tabs and create tabs only for open sub-issues that have none.

## Creating worktrees

In `worktree` mode, herdr backs the checkout itself:

```bash
herdr worktree create --workspace "$HERDR_WORKSPACE_ID" --cwd "$PWD" \
  --branch <branch-name> --base <default-branch> --label "<tab label>" --no-focus
```

Read the resulting workspace, tab, pane, and checkout path from the JSON response. Worktree creation can create a linked workspace; save that worker's context separately from the caller's. Never predict IDs or hand-roll `git worktree add`. In `branch` and `shared` mode use **Create tab** instead, and never create a worktree the user did not choose.

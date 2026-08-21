# Intake

Three decisions, asked as **one batched question set** after Discover — never one prompt at a time, and never before the issue list exists, because two of the three need it. Follow the workspace `AGENTS.md` decision-options rule: label exactly one option `Recommended`, add a final `Write your own`, and never pad.

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

These six are the supported runtimes; no others. Offer every one whose launch token resolves on PATH, and say which of the six are missing rather than silently shortening the list. This question enumerates a fixed roster, so it may run past three options — that cap governs recommendations, not rosters.

**`AGENT_KIND` comes from this table, never from `CODING_CLI`'s first token.** For Cursor the two differ, so deriving the kind from the command yields `agent`, which `herdr agent start --kind` rejects. Worker-tab labels use the runtime's launch token so they stay readable.

## 2. Which permission mode

A fresh session pauses at its own approval prompts (shell, tracker, test commands) unless launched with an auto-accept preset or the folder pre-approves them. Offer, for the chosen runtime:

- its **highest elevated preset**, quoted from the Runtime table in [`../../agents-md/references/tool-calling.md`](../../agents-md/references/tool-calling.md) — that file is the single source; never retype a preset from memory
- the **bare launch token**, with the consequence stated: every worker pauses at its own approvals

Never pick an elevated mode yourself — that is always the user's explicit call. Elevation is safest inside worktree isolation; if the user takes an elevated preset with `shared` isolation, say so once before fan-out.

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

**User away →** `worktree` when more than one open sub-issue touches the same repo, otherwise `shared`. Never fan out unattended into `shared` with a same-repo collision; that is the one case that still stops and reports.

## 4. Leftover tabs and agents

Tabs labelled `[<launch token>] - <TRACKER_TAG> #<n>`, or live agents holding those slugs, survive from a previous run of this spec. List both per **Context** in [`herdr-commands.md`](herdr-commands.md) and ask whether to monitor them instead of re-creating; re-running blindly creates a second tab per issue, and a surviving agent name blocks `agent start` outright.

**User away →** monitor the existing tabs and create tabs only for open sub-issues that have none.

## Creating worktrees

In `worktree` mode, herdr backs the checkout itself:

```bash
herdr worktree create --workspace "$HERDR_WORKSPACE_ID" --cwd "$PWD" \
  --branch <branch-name> --base <default-branch> --label "<tab label>"
```

Read the resulting IDs from the JSON response — never predict them, and never hand-roll `git worktree add`. In `branch` and `shared` mode use **Create tab** instead, and never create a worktree the user did not choose.

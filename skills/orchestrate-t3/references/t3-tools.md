# T3 Code tools

Zero attribution: omit co-author, AI, and tool attribution from all output.

T3 Code is controlled through its MCP server, never a shell command. The connected server's live tool schema is the authority for parameter names and enum values: inspect it before the first call and use what it shows. T3 Code is pre-1.0, so a tool named here that the live list lacks is a stop, not a cue to improvise. Tools carry the prefix of the name the server was added under (`t3` in the setup below), so match each tool by the suffix given here.

## Connect

The server is connected when the session's tool list holds `orchestrator_capabilities` and `t3_thread_launch`. Neither present → stop and print the setup for the user to run; a skill cannot complete the sign-in:

```sh
claude mcp add --transport http t3 <MCP URL>
claude mcp login t3
```

The MCP URL comes from T3 Code's **Settings → Connections → Copy MCP URL**; other runtimes add it as a remote HTTP MCP server with OAuth. On the sign-in page the user picks the access mode. **Read only** cannot launch threads, and a thread never runs with more permission than that mode.

Call `orchestrator_capabilities` once. A permission error on it, or on the first launch, means the sign-in mode is too low: report it under Needs user and stop.

## Capabilities

`orchestrator_capabilities` lists the provider instances and their models from the same catalog as T3 Code's composer. Every agent and model offered in Intake comes from this result, never from a remembered list.

## Project

A thread launched from outside T3 Code needs a `projectId`. Call `t3_project_list`, following its pages, and match the project whose workspace root is the repository's primary checkout. No match → report the unregistered repository under Needs user; registering a project changes the user's T3 Code setup, so ask first. Loaded by `/factory run`, register it with the project-create tool the live schema shows, titled with its PROJECT-CODE, and name it in the report instead of asking.

## Launch

`t3_thread_launch`, one call per group:

- `projectId` — from **Project**.
- `title` — the thread label from the workflow.
- `modelSelection` — the Intake choice; omit it to take the project's default model.
- `runtimeMode` — the Intake choice, set explicitly on every launch.
- `workspaceStrategy` — `{type: "existing_worktree", worktreePath: <absolute checkout path>, branch: <branch>}`. An omitted strategy means the project root, not a worktree.
- `message` — the filled worker prompt.

Save the returned `threadId` and `runId` with the group before the next call. A launch has no retry key: after an error or a lost response, call `t3_thread_list` and look for the title before launching again, or the group gets two threads.

## Wait

`t3_thread_wait` with the saved `threadId` and `runId` blocks until the run reaches a terminal state or the timeout passes. Issue the waits for all threads together. `timedOut: true` leaves the work running; wait again.

| Status | Meaning for the orchestrator |
| :--- | :--- |
| `preparing`, `queued`, `starting`, `running` | Working — leave it |
| `waiting` | Stopped on a question or an approval — see **Questions** |
| `completed`, `idle` | The turn ended — **Read** the report; not proof the task finished |
| `failed`, `interrupted`, `cancelled`, `rolled_back` | Errored — **Read** the cause |

## Read

`t3_thread_read` with the saved `threadId` returns the thread's messages. Take the worker's report from its last assistant message. When the result marks an item as truncated, fetch the rest with that item's ID and the next text offset it returns; a partly read report is not evidence.

## Questions

`t3_pending_request_list`, then `t3_pending_request_read`, show a waiting thread's question. `t3_pending_request_respond` answers a question; it cannot approve a permission prompt. A `waiting` thread with no pending question is held on a permission prompt only the user can clear in T3 Code.

## Send

`t3_thread_send` with the saved `threadId` delivers a follow-up message. Pass a `clientRequestId` so a retry cannot deliver it twice.

## Recover

After compaction or a restart, rebuild the thread map from `t3_thread_list` by title, and from tracker state per **Verify** in [`tracker-map.md`](tracker-map.md), before any wait, read, or send. Never launch from recollection: a second thread redoes finished work in the same checkout.

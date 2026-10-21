# T3 Code tools

Zero attribution: omit co-author, AI, and tool attribution from all output.

T3 Code is controlled through its MCP server, never a shell command. The connected server's live tool schema is the authority for parameter names and enum values: inspect it before the first call and use what it shows. T3 Code is pre-1.0, so a tool named here that the live list lacks is a stop, not a cue to improvise. Tools carry the prefix of the name the server was added under (`t3` in the setup below), so match each tool by the suffix given here.

## Connect

Discover `orchestrator_capabilities` and a supported launcher for the workspace's binding policy: `t3_thread_launch` or local child delegation. Missing connectivity or a compatible launcher → stop and print the setup for the user to run; a skill cannot complete the sign-in:

```sh
claude mcp add --transport http t3 <MCP URL>
claude mcp login t3
```

The MCP URL comes from T3 Code's **Settings → Connections → Copy MCP URL**; other runtimes add it as a remote HTTP MCP server with OAuth. On the sign-in page the user picks the access mode. **Read only** cannot launch threads, and a thread never runs with more permission than that mode.

Call `orchestrator_capabilities` once; retain its result reference and bounded usable-provider summary for this run. Refresh only after reconnect or changed availability/model evidence. A permission error on it, or on the first launch, means the sign-in mode is too low: report it under Needs user and stop.

## Capabilities

`orchestrator_capabilities` lists the provider instances and their models from the same catalog as T3 Code's composer. Every agent and model offered in Intake comes from this result, never from a remembered list.

- **Usable provider** — an entry of `providers` with `canRunChildTask: true`. One with `false` is disabled or not installed, says why in `constraints`, and is never offered. This is the only availability signal: the result carries no sign-in state.
- **Default model** — for Cursor, `composer-2.5` when the result lists it. Otherwise the provider's model with id `default` when it lists one, else its first listed model. The result marks no other default.
- **This session** — `inheritedProviderInstanceId` and `inheritedModel`; both null when the caller is not a T3 Code thread.

## Project

Read workspace thread policy before selecting a project. When threads must stay bound to the workspace, resolve its registered project/root through live session metadata or paginated `t3_project_list`. Under that policy this applies to every supervisor, builder, reviewer, QA and standalone task. A product worktree is an execution assignment, not a T3 project selection. Reuse that workspace project; no product registration or separate product thread is needed.

Without a workspace-bound policy, match the repository's primary checkout to its registered project. No match → report the unregistered repository under Needs user; registration changes the user's T3 setup and needs authorization. `/factory run` may register it through the live project-create schema, titled with its PROJECT-CODE, and report the registration.

## Launch

Select the supported launch mode from live schemas and workspace policy. Preserve saved provider/model and permission-mode choices in either mode.

- **Workspace-bound:** use supported local child delegation inheriting the workspace (`isolation: "shared"` when exposed), or an authorized `t3_thread_launch` selecting the workspace project/root. For an authorized top-level launch use `workspaceStrategy: {type: "root"}` when the live schema exposes it. Keep the workspace root strategy; assigning a product `existing_worktree` would change the thread binding. A product checkout assignment does not itself require a top-level thread. Apply host authorization requirements only when a top-level launch is actually needed. If no permitted launcher preserves the binding and required review isolation, report that specific blocker.
- **Checkout-bound:** use `t3_thread_launch` with the repository's `projectId` and `workspaceStrategy: {type: "existing_worktree", worktreePath: <absolute checkout path>, branch: <branch>}`, or another supported exact-checkout launcher. Omitting strategy means the project root, not a task worktree.

Set the workflow title, saved provider/model (`modelSelection` for thread launch), permission mode (`runtimeMode`), and filled worker prompt through the selected launcher's live schema. Prepend: "Verify thread binding and assigned execution checkout separately. Report ready without edits, commits or tests; wait for the parent's release."

Save returned worker/thread and run IDs. Read live thread project/root/branch/worktree identity and the readiness report. In workspace-bound mode, compare thread identity to the workspace and independently verify the assigned product checkout's canonical path, common Git directory, branch and head. A prompt naming a checkout alone is insufficient evidence. In checkout-bound mode compare live binding to the task checkout. Mismatches block writes. Release only a matching ready worker through the launcher's supported send control; record its implementation run ID from the receipt/live read. The readiness turn is not implementation completion.

Keep actual thread binding separate from product execution identity in group maps, checkpoints and replacement-parent handoffs. Resolve null `worktreePath` against the registered project root, never against the product assignment. Resolve absolute paths from local workspace/project records on macOS, Linux and WSL2; do not embed another platform's home path.

A launch has no assumed retry key: after an error or lost response, reconcile live workers/threads before relaunching. Confirm any previous writer terminal before replacement. Use the selected launcher's matching wait/read/send/recovery controls; the T3 thread controls below apply when it returns T3 thread/run IDs. Shared workspace binding grants no shared write ownership, conversation inheritance for reviewers, or permission to bypass supervisor telemetry gates.

## Wait

`t3_thread_wait` with the saved `threadId` and `runId` blocks until the run reaches a terminal state or the timeout passes. Issue waits of at most 60 seconds for all threads together. `timedOut: true` leaves the work running; wait again. Compare cheap progress deltas; after five minutes without progress inspect pending requests/authentication, live commands and supported provider/host health. A verified running long command differs from no events or dead transport; elapsed time alone never authorizes a competing writer.

| Status | Meaning for the orchestrator |
| :--- | :--- |
| `preparing`, `queued`, `starting`, `running` | Working — leave it |
| `waiting` | Stopped on a question or an approval — see **Questions** |
| `completed`, `idle` | The turn ended — **Read** the report; not proof the task finished |
| `failed`, `interrupted`, `cancelled`, `rolled_back` | Errored — **Read** the cause |

## Read

`t3_thread_read` with the saved `threadId` returns the thread's messages. For routine monitoring prefer supported state/summary views and small cursor/delta reads discovered in the live schema. Fetch report items only when a turn changes or a gate needs their evidence; retain cursors and result references. Never assume a `summaryOnly` or limit flag exists. Take the worker's report from its last assistant message. When the result marks an item as truncated, fetch the rest with that item's ID and the next text offset it returns; a partly read report is not evidence. Save large output to a durable report/log and inspect bounded sections rather than putting every worker transcript in the parent context.

## Context

Check context at phase boundaries and before large reads, fan-out, completion imports or provider handoff. At 60% observed root occupancy, checkpoint and compact through supported controls before the next long phase; act earlier if projected payloads threaten the reserve. A reserve guard is not the model's hard ceiling. Reserve at least 25% of the parent's receiving context budget; account for pending tool payloads and inherited messages, not only current text. Child capacity cannot absorb an oversized parent envelope. Scoped workers start without full parent conversation inheritance when supported and receive only their objective, instructions, verified checkout, ownership and needed facts. Reviewer isolation remains mandatory. Subagents reduce root growth through bounded returns; they do not compact the parent. Workers return concise evidence and complete report paths; complete acceptance maps and findings remain readable on demand.

Use supported harness compaction before the handoff when needed. The live MCP schema may expose no compact operation; never invent one or claim it ran. Without supported compaction, reduce payloads through supported controls or save checkout/head, thread/run IDs, status, budgets and outstanding gates for an authorized fresh parent thread with a neutral handoff. Confirm active writers and follow **Recover** before resuming. Context reduction never clears an unread gate or authorizes duplicate dispatch.

## Queued native compaction

When the installed provider adapter supports native compaction and the live send schema accepts queued messages, submit the exact attachment-free `/compact` through `t3_thread_send` with `mode:"queue"` and a stable boundary `clientRequestId`. Save its thread/message/run receipt, then queue a separate idempotent continuation naming that compact run and the durable checkpoint. Persist both receipts before ending the current turn. Use `WAITING_COMPACTION` with the next automatic action and `Needs user: None`; never wait in this turn for its own queued maintenance run.

The continuation verifies that exact compact run completed, reconciles workers/checkout and checks fresh same-native-thread occupancy before retrying a budget-blocked handoff. Unsupported or failed compaction clears no gate. Preserve the original provider/harness/model and budgets. Lost receipts use the same supported idempotency key, not a new request. Prefer this boundary before fan-out with no pending child completions. Automatic child completions can outrank ordinary queued turns, so this procedure does not implement a pre-delivery context guard. Early harness-native compaction remains useful; a binary install alone needs no archive patching.

## Questions

`t3_pending_request_list`, then `t3_pending_request_read`, show a waiting thread's question. `t3_pending_request_respond` answers a question; it cannot approve a permission prompt. A `waiting` thread with no pending question is held on a permission prompt only the user can clear in T3 Code.

## Send

`t3_thread_send` with the saved `threadId` delivers a follow-up message. Pass a `clientRequestId` so a retry cannot deliver it twice.

## Recover

After compaction or a restart, rebuild the thread map from `t3_thread_list` by title, and from tracker state per **Verify** in [`tracker-map.md`](tracker-map.md), before any wait, read, or send. Never launch from recollection: a second thread redoes finished work in the same checkout.

# T3 backend

Zero attribution: never add co-author, AI, or tool attribution in any output.

Read when **Select once** in [execution-and-continuity.md](execution-and-continuity.md) selects T3. Every gate, cap and stop there and in [run.md](run.md) still binds; this file maps them to T3 Code controls. Standalone `orchestrate-t3` retains its T3-only contract.

## Select

Exposed tool names alone do not prove connectivity. Cache the successful bounded capability/catalog result for this run; refresh only after reconnect or changed availability/model evidence. A failed capability query is one failure, not a reason to repeat slow calls; native local execution is allowed only when workspace policy permits delegation and the saved required execution/model route remains available. Review availability recovery follows [Factory model selection](review-models.md); this backend failure grants no unapproved route. Report the fallback and cause. This is another executor, not a T3 authentication workaround. Never reuse OAuth secrets, change sign-in mode, or control T3 through shell commands.

T3 reviewer options require live cross-provider launch support when different from the builder. Read **Capabilities** in `orchestrate-t3/references/t3-tools.md` for T3 catalog interpretation.

## Dispatch

T3 dispatch loads `orchestrate-t3` with the unit and **Start** as intake.

Resolve thread binding from workspace instructions separately from the assigned execution checkout. Under a workspace-bound thread policy, every T3 thread stays bound to that workspace project/root: supervisor, builder, reviewer, QA and standalone tasks. Execute product commands and edits in the verified assigned product worktree through explicit working directories and edit paths. Use supported shared child delegation that inherits the workspace binding; an explicitly authorized top-level launch selects the workspace project and root strategy through its live schema. A product assignment alone never requires a product-bound or top-level thread.

A root-bound thread may report `worktreePath: null`; reconcile it against its registered workspace root.

For worker monitoring, follow **Delegated tasks/Wait** in `orchestrate-t3/references/t3-tools.md`: save task handles for delegates and thread/run handles for separate threads. A completion-notice response checkpoints and yields; never poll its running task or wait on its child thread. Supported PR watches belong to the owning parent under **PR watches**, never a delegated stage worker.

Stage skills: send `/<skill> <args>` as the first token of a `t3_thread_send` message to the unit's idle builder thread or a stage thread. Read the thread's first new items back; no skill load means no skill ran: resubmit once, then park the stage as `stage_skill_not_invoked`. If the send returns a new delegated task, save its task ID and follow its completion notice. No T3 run has recorded a positive readback for this path yet.

## Compaction

For a binary-installed T3 host, first check **Queued native compaction** in `orchestrate-t3/references/t3-tools.md` and workspace overrides. A supported queued maintenance command plus queued continuation can compact at a turn boundary without a dedicated compact MCP tool. This is not a guarantee that automatic child delivery waits for compaction.

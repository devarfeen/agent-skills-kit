# Herdr backend

Zero attribution: never add co-author, AI, or tool attribution in any output.

Read when **Select once** in [execution-and-continuity.md](execution-and-continuity.md) selects herdr. Every gate, cap, stop and record there and in [run.md](run.md) still binds; this file maps them to the herdr CLI. Syntax lives in `orchestrate-herdr/references/herdr-commands.md`; load its sections when a step needs them. The worker checkout record follows `orchestrate-herdr/references/checkout-binding.md`.

## Contents

- Preconditions
- Dispatch
- Wait and read
- Review and QA workers
- Recovery
- Parent continuity
- Cleanup

## Preconditions

- `HERDR_ENV=1` in the parent's shell and `herdr status` shows a running server. Otherwise park every unit with the missing herdr context.
- Save `HERDR_WORKSPACE_ID`, `HERDR_TAB_ID` and `HERDR_PANE_ID` in the checkpoint. Every worker tab goes in that workspace.
- Read the workspace's herdr policy before the first dispatch. It owns launch flags, the working directory agents start in, worktree placement and supervisor inputs. No policy → agents start in the parent's folder, with their native default permissions.
- The parent never answers a `blocked` agent, never runs `herdr server stop`, and closes only tabs it created.

## Dispatch

Per builder, reviewer round or QA worker, in this order. Read each result's IDs from its JSON; never predict them.

1. **Checkout.** For a new unit checkout, run `herdr worktree create --cwd <owning-repo> --branch <task> --base origin/<base> --path <owning-repo>/.worktrees/<task> --no-focus`. Verify placement and identity per checkout binding. Save the linked workspace ID it returns; its panes run the unit's long commands, never agents.
2. **Tab.** `herdr tab create --workspace "$HERDR_WORKSPACE_ID" --cwd <policy-start-folder> --label "<role> - <unit>" --no-focus`.
3. **Agent.** `herdr agent start <name> --kind <kind> --pane <root-pane> --timeout 120000 -- <policy flags> <model flag>`. `<name>` is `<role>-<unit-slug>`, unique among live agents and within herdr's name rule. `agent_not_ready` means a startup dialog: read it, park that unit with the dialog's purpose, and send it no keys. Codex always gets `--no-daemon`; its shared daemon runs commands outside the pane without `HERDR_ENV`.
4. **Prompt.** Builders get the filled `orchestrate-t3/references/worker-prompt.md` contract, with `THREAD_BINDING` naming the herdr workspace and start folder. Submit with `herdr agent prompt <name> "<prompt>" --wait --timeout 60000`. A `timeout` error means the turn is working, not undelivered.
5. **Stage skill.** Submit `/<skill> <args>` to the unit's idle builder agent, or to a `<stage>-<unit>` agent started the same way, with `herdr agent prompt`: one line, no leading whitespace, under 700 characters, naming a private brief file. For a longer inline brief, type the slash line with `herdr pane send-text <pane> "/<skill> <args> "` and paste the body with `herdr agent prompt`. herdr pastes with bracketed paste, and Claude wraps a paste above about 800 characters as pasted text that loads no skill. Verify with `herdr agent read` that the turn began from the skill.
6. **Record.** Worker ID is the agent name. Run ID is `<terminal_id>.<dispatch-number>`, and the number increases with each prompt to the same agent. Save the run ID, checkout, branch, head and budgets in the checkpoint and **Round log** before waiting.

## Wait and read

- Wait with `herdr agent wait <name> --timeout 60000`, one bounded wait per active worker, and report progress after each wait. `working` keeps waiting. `idle` or `done` → read. `unknown` → inspect output, never completion.
- `blocked` is a human boundary for that unit only. Read the dialog with `herdr agent read <name> --source recent-unwrapped --lines 120`, park the unit with its purpose, and keep other units running.
- Ask each worker to write its complete report to the unit's log directory and reply with at most 400 words and the path. Read the reply with `herdr agent read <name> --source recent-unwrapped --lines 200`; query the file in bounded sections.
- Run long task-stack and full-check commands in the unit's linked worktree pane: `herdr pane run <pane> "<command>"`, then `herdr pane wait-output <pane> --regex '<end marker>' --timeout 60000` in a loop. The parent's own shell never blocks for longer than one wait.
- Before a completion import, use the workspace supervisor's herdr read operation when it provides one. Fixes for a worker go to the same agent as a new prompt once it is `idle`; never paste into a `working` or `blocked` agent.

## Review and QA workers

- Each review round starts a new tab and a new agent with the saved reviewer kind and model and the read-only reviewer prompt. A new process has no conversation fork, so it satisfies **Independent review**. Never reuse the builder agent.
- The QA worker is its own agent in its own tab, admitted only after **Browser admission** and holding the unit's browser lease.
- After a round's report is read back, exit that agent with `herdr agent send-keys <name> ctrl+c ctrl+c`. Close its tab only after `herdr agent get <name>` reports it gone.
- Reviewer options are the installed runtimes in herdr's `--kind` list whose launch token is on PATH.

## Recovery

Each relaunch counts against the worker-recovery cap in **Supervise and recover**.

- **Exited agent.** `herdr agent get` reports it gone, and `herdr pane process-info --pane <pane>` shows only the shell. The writer is confirmed stopped. Relaunch in that pane with the same name, the harness's exact resume arguments and the session ID from the last `agent_session`, then the saved flags.
- **No exact session ID.** Park the unit. Never resume "latest".
- **Closed pane or unknown foreground.** The writer state is unknown. Park that checkout.
- **Server restart.** herdr restores agents without their launch flags, and a restart gives each pane a new `terminal_id`. Wait until the harness executable appears in the `process-info` argv, then check it for the saved flags and model (Codex: including `--no-daemon`). Missing → exit it: an idle agent gets Ctrl-C twice in separate calls; a `blocked` one gets `herdr pane close <pane>`, because any key on a dialog is an answer the CLI may save. Confirm the agent is gone, then relaunch as above, in a new tab when the pane was closed. **Resume** in `herdr-commands.md` covers the restore timing.

## Parent continuity

- **Controller run.** A controller turn contract names the herdr host and a report path. Follow it:
  - Write the report file before the turn ends.
  - Keep supervising inside the turn with bounded waits.
  - End the turn only at completion, a park, a compaction need, or a needed fresh turn.
  - The controller prompts the same session again. It compacts at the idle boundary when its threshold is reached.
  - herdr children never deliver results into the parent on their own, so compaction has no delivery-ordering gap.
- **Inline run.** Without a controller, an inline `/factory run` in a herdr pane ends like any other run, through **End and resume**.

## Cleanup

At **Cleanup** in `review-and-delivery.md`, after its merged-only checks pass:

1. Exit the unit's agents.
2. Close the tabs the run created for the unit.
3. Run `herdr worktree remove --workspace <linked-id>` without `--force`.

A refused removal preserves the checkout and is reported.

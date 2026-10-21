# Session handoff

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Use status updates at phase changes; use the handoff when a run ends unfinished, pauses, stops, or resumes after interruption. Save this handoff after each gate or worker state change. Prefer the workspace supervisor's supported handoff operation when available; discover its schema rather than inventing a command. When the adapter exposes `handoff` and `handoff-show`, persist with `handoff` and let the authorized host render `handoff-show` after interruption. A saved handoff does not prove the host has installed that rendering hook. Discover optional renderer formats from its live help/schema: Markdown for T3, terminal color only for a supported TTY renderer, default machine output for adapters. Save optional recovery options using its supported schema. Checkpoints store references and bounded summaries, never credentials or raw transcripts.

## Active status

Use Markdown list items so T3 and CLI render separate fields. Semantic emoji provide portable color cues on macOS, Linux and WSL2; retain text labels for accessibility. Chat uses no ANSI escapes or HTML. These are display states, separate from issue/PR gate states.

- 🟦 **Stage:** [current] QA — `WAITING_RUNTIME`
- 🟩 **Found:** [verified] Worktree/head matched; BASE ready; HEAD assets building.
- 🟨 **Next:** [todo] Runtime owner verifies HEAD, then supervisor starts browser QA automatically.
- 👤 **Needs user:** None. Supervisor remains active.
- **Workers:** 1 running / 1 done / 0 blocked — runtime: build HEAD assets.

`RUNNING` advances work. `WAITING_WORKERS` means a child or known queued check is active; wait with supported controls and continue on its result. `WAITING_RUNTIME` means authorized preparation/repair is active; its owner finishes readiness before dependent work starts. Neither is human-blocked, and neither emits a paste/run prompt or ends the active supervisor turn. `WAITING_COMPACTION` may yield only after durable compact and continuation receipts under the runtime's supported maintenance boundary; it also needs no user action. Name the owner, observed progress and next automatic action. A timeout alone changes neither ownership nor state. Count only evidenced human/capability failures as blocked. `BLOCKED` names the missing human decision, authority, fact or exhausted gate; `PAUSED`/`STOPPED` preserve explicit user intent. `COMPLETE` requires every requested gate or the authorized ceiling; child completion alone cannot earn it.

## Human boundary

When a unit truly needs a person, state why, owner, attempted recovery, preserved head and budgets, next automatic action after resolution, and the exact user action. Keep independent work running. Offer up to three feasible, authorized options: each states action, benefit, cost and preserved gate. Recommend one when possible; otherwise explain why. State missing capabilities separately, without unavailable filler options. Retaining the parked unit for its owner is a valid option. Options never reset caps, weaken acceptance, grant access or bypass review. Do not ask for a choice while workers or authorized runtime work merely run. A pause/stop needs no unsolicited recovery menu.

## Durable handoff

Persist these fields for each unfinished unit/group; render them at its real human boundary or interruption. Limit prose to 400 words; link longer evidence without dropping blockers or required steps.

- **Current state:** requested stop/pause or blocker, actual thread project/root and separate execution checkout/branch/head, checkpoint reference, original builder and chosen reviewer, worker IDs/status/ownership, last verified gate, next missing gate, remaining recovery/stage budgets, and evidence paths. Mark stale or unavailable live status unknown.
- **Required setup:** exact supported repair, connection or runtime restart steps and their authorization requirements. Use `None` when no setup is needed. Separate authorized local work from user-only access or decisions. Include the diagnosed failed condition and recovery already attempted.
- **Next prompt:** save one copyable recovery prompt in the checkpoint; show it only when the supervisor has ended at a human boundary or after interruption, never as an action during active waiting. Include the workflow/reference, checkpoint, required workspace thread binding, preserved execution checkout/head, saved choices, and first missing gate. Require live writer/checkout/gate reconciliation before execution. State that completed implementation and attempt counters remain preserved. Missing reviewer intake names that pending choice without asking for a builder again.

Before a planned pause/stop, save the reason and intent so recovery does not restart against the user's direction. After an abrupt interruption, an authorized host renders these fields from the last checkpoint even if the agent sent no final reply. Its output identifies checkpoint age and unverified live state; it performs no work. If no host integration exists, persist the handoff and report that automatic interruption output is unavailable. Instructions and checkpoint storage alone cannot restart a terminated session.

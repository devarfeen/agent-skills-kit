# Session handoff

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Load when a run ends unfinished, pauses, stops, or resumes after interruption. Save this handoff after each gate or worker state change. Prefer the workspace supervisor's supported handoff operation when available; discover its schema rather than inventing a command. When the adapter exposes `handoff` and `handoff-show`, persist with `handoff` and let the authorized host render `handoff-show` after interruption. A saved handoff does not prove the host has installed that rendering hook. Checkpoints store references and bounded summaries, never credentials or raw transcripts.

## Output

Emit these fields for each unfinished unit/group. Limit prose to 400 words; link longer evidence without dropping blockers or required steps.

- **Current state:** requested stop/pause or blocker, actual thread project/root and separate execution checkout/branch/head, checkpoint reference, original builder and chosen reviewer, worker IDs/status/ownership, last verified gate, next missing gate, remaining recovery/stage budgets, and evidence paths. Mark stale or unavailable live status unknown.
- **Required setup:** exact supported repair, connection or runtime restart steps and their authorization requirements. Use `None` when no setup is needed. Separate authorized local work from user-only access or decisions. Include the diagnosed failed condition and recovery already attempted.
- **Next prompt:** one copyable prompt with the workflow/reference, checkpoint, required workspace thread binding, preserved execution checkout/head, saved choices, and first missing gate. Require live writer/checkout/gate reconciliation before execution. State that completed implementation and attempt counters remain preserved. Missing reviewer intake names that pending choice without asking for a builder again.

Before a planned pause/stop, save the reason and intent so recovery does not restart against the user's direction. After an abrupt interruption, an authorized host renders these fields from the last checkpoint even if the agent sent no final reply. Its output identifies checkpoint age and unverified live state; it performs no work. If no host integration exists, persist the handoff and report that automatic interruption output is unavailable. Instructions and checkpoint storage alone cannot restart a terminated session.

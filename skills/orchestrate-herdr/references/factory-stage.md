# Factory stage

Zero attribution: omit co-author, AI, and tool attribution from all output.

Read when a user-started `/factory run` selects the herdr backend. The factory parent is the orchestrator and follows the factory skill's `references/backend-herdr.md`. That file's gates, caps and stops replace this skill's **Workflow** and **Completion criteria**; this skill supplies only [`herdr-commands.md`](herdr-commands.md) and [`checkout-binding.md`](checkout-binding.md).

The factory's **Start** answers every Intake question, and no question is asked:

| Intake | Factory answer |
| :--- | :--- |
| Which coding agent | Builder runtime from the saved builder choice; reviewer runtime from the saved reviewer choice. `AGENT_KIND` still comes from the Intake roster table |
| Which permission mode | The flags named by workspace herdr policy; with no policy, the bare launch token, so a startup dialog parks the unit |
| How work is isolated | `worktree`, one per unit, placed under `<owning-repo>/.worktrees/<task>` |
| Leftover tabs and agents | Monitor existing tabs that match the unit; never create a second agent for a live writer |

The **Rules** above still bind: saved IDs only, prompts submitted into a ready agent and never into a dead shell, completion by quoted test evidence, and never answering a `blocked` agent. Tracker writes follow the factory's records, not **Block** in `tracker-map.md`. The factory's bounded return contract asks for the full report file in the first prompt; that replaces the first-prompt limit in the **Read** alternate-screen caveat.

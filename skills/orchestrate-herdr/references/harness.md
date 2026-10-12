# Harness mode — no spec

Zero attribution: omit co-author, AI, and tool attribution from all output.

Use when there is no `SPEC_REF`: eval harnesses, parallel coding agents, or any multi-tab run that does not fan out from a tracker parent issue.

## Define workers

Build `WORKERS` — one entry per tab, each with a short `label` (for the tab name) and a full `prompt` (what that agent should do). Sources, in order:

1. Skill args or the user's message — a numbered list, one prompt block per worker, or `WORKERS=` metadata if supplied.
2. Otherwise ask: how many workers, and the prompt (or distinct prompt) for each.

You may use [`worker-prompt.md`](worker-prompt.md) when filling tracker fields for an assigned issue.

Minimum prompt footer (append if the user's text omits it):

```md
Report back when completed, errored, or blocked.

Completion requires test evidence when the task involves code: the test command and its passing output, with the verified checkout identity and baseline result from the supplied checkout block. Zero attribution: never add co-author, AI, or tool attribution to output.
End the report with three fields, one line each:
Status: <completed | blocked — decision needed | errored — cause>
Decisions: <choices made that the task didn't dictate, or "none">
Open items: <what a next session must resolve, or "none">
```

Include the sub-agent and **Never cloud** paragraphs from `worker-prompt.md` when the task benefits from local lanes.

Append the verified checkout and instruction block from `checkout-binding.md` for every worker. A harness prompt never relaxes its placement, first-write identity, baseline, or instruction-preservation gates.

## Tabs and labels

Tab label: `[CLI_NAME] - <label>` — e.g. `codex - harness 1`, `codex - eval-judge-2`.

Isolation, creation, launch, monitor, and read-back follow the main skill, including tracker **Block** / **Verify** when a worker maps to an issue.

## Intake

Same agent, permission, and isolation questions as spec mode. Skip leftover-tab matching on spec issue numbers; still list live agents and ask whether to monitor existing harness tabs.

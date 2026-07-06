---
name: orchestrate-herdr
description: "Orchestrate herdr worker tabs for a PRD. Reads a PRD/issue URL, finds open sub-issues, and launches one herdr-managed worker tab per issue running a chosen coding CLI, then monitors them for test-backed completion. Re-runnable prompt parameterized by PRD URL and coding CLI. Use when running inside herdr (HERDR_ENV=1) and the user wants to fan a PRD out to per-issue workers."
---

# Orchestrate herdr

This is a tested, working orchestrator prompt. The **only** things that change between runs are the **PRD URL** and the **coding CLI** to launch.

## Intake

Everything below the `---` divider is the frozen prompt body — per this repo's
AGENTS.md rule 8, do not edit, summarize, reword, or "improve" it; run it
exactly as written. This Intake section is the only editable part of the skill.

Resolve two values before running the prompt:

- `PRD_URL` — the PRD or parent issue URL whose open sub-issues become workers.
- `CODING_CLI` — the coding CLI command to run in each worker tab (e.g. `codex`, `claude`).

Source order:

1. Use values passed as skill args (a URL plus a CLI name, or `PRD_URL=... CODING_CLI=...`).
2. For anything still missing, ask the user. Do not guess. Do not proceed until both are set.

Pre-flight — check before executing, and fail fast naming exactly what is
missing instead of stalling mid-run:

1. `HERDR_ENV=1` is set — you are inside herdr.
2. The herdr companion skill is installed — the prompt's "Load required
   skills" step means it (tab create / submit / read / monitor mechanics).
3. `CODING_CLI` resolves on PATH, and `gh` is authenticated (`gh auth status`).
4. No leftover worker tabs: if tabs named `[CODING_CLI] - GH #<n>` from a
   previous run of this PRD already exist, ask whether to monitor those
   instead — re-running blindly creates a second tab per issue. If the user
   is away, monitor the existing tabs and create tabs only for open
   sub-issues that have none.
5. Same-repo collision: workers run simultaneously in one shared working
   folder and the prompt bans worktrees. If more than one open sub-issue
   touches the same repo, say so and get explicit confirmation before
   proceeding — or agree with the user to run those issues serially. If the
   user is away, do not fan out: report the collision and stop — shared-tree
   concurrency is never a safe unattended default.

Run policy — supplements the frozen prompt without changing it:

- **Sub-issue discovery** (the prompt's step 3): prefer
  `gh api repos/<owner>/<repo>/issues/<n>/sub_issues`; fall back to task-list
  checkboxes and "Tracked by" references in the PRD body. State the count
  found and cross-check it against the PRD before creating any tab —
  under-fanning silently drops slices.
- **Test evidence** (the prompt's completion gate) means the worker's test
  command plus its quoted passing output. An unquoted "tests pass" stays
  incomplete — read the tab and get the output.
- **After the frozen prompt's final report:** suggest `/review` on the
  workers' diffs or `/release-notes` for what shipped — suggest only, then
  stop.

Then set the two header lines below to the resolved values and execute the prompt **verbatim**.

---

PRD_URL: [PRD_URL]
CODING_CLI: [CODING_CLI]

You are the **orchestrator**. Do not implement. Do not close this tab.

## Non-Negotiables

* Use the existing `herdr` workspace/session only.
* Use Herdr-managed tabs only.
* No panes.
* No internal sub-agents.
* No nested agents.
* No nested coding sessions.
* Stay in the same folder as this orchestrator tab.
* Never `cd` into task folders, issue folders, worktrees, or any other folder when creating worker tabs.
* Create workers only as new Herdr tabs inside the current workspace.
* Do not launch `CODING_CLI` from inside another `CODING_CLI`.
* In each worker tab, run only `CODING_CLI` from the original current folder.
* Do not pass prompts as launch arguments/flags.
* Do not leave prompts staged or unsent.

## Orchestrator Workflow

1. Load required skills.
2. Read `PRD_URL`.
3. Find open sub-issues / linked child issues.
4. Save current Herdr workspace/session ID.
5. Save current working folder.
6. For each open issue, create one Herdr-managed worker tab in the saved workspace and same folder.
7. Name each tab: `[CODING_CLI] - GH #[ISSUE_NUMBER]`.
8. Save each tab ID immediately after creation.
9. Use only saved tab IDs for prompt submit, read, monitor, and follow-up.
10. Never rely on active tab, latest tab, visual order, or guessed tab.

## Worker Launch

For each saved worker tab:

1. Confirm tab ID, workspace/session ID, and folder match the saved orchestrator context.
2. Run only `CODING_CLI`.
3. Wait 30 seconds for CLI readiness.
4. Paste the issue prompt into that same saved tab.
5. Submit the prompt.
6. Confirm the first response is visible.

A worker is not launched until its tab ID is saved, prompt is submitted, and first response is visible.

## Worker Prompt

Do not send the full PRD to workers. Do not send identical prompts to workers. Each worker receives only its assigned issue.

```md
GH_ISSUE: #[ISSUE_NUMBER]
GH_ISSUE_URL: [ISSUE_URL]

Work only on this GitHub issue.

Infer project/repo context from the assigned issue.

Use `/tdd` / `$tdd`.

Do not work on the full PRD. Do not redo PRD orchestration. Do only issue-level discovery required for this issue.

Avoid unrelated changes.

Report back to the main orchestrator/Herdr when completed, errored, or blocked.

Completion requires test evidence.
```

## Monitoring

Monitor all saved Herdr tab IDs every 1 minute.

Do not accept completion without test evidence.

Do not add `BLOCKER:`, `AFK:`, or `HITL:` to issue titles.

Use issue order, dependency notes, comments, `ready-for-agent`, and `ready-for-human` labels.

Report only: workspace/session ID, folder, tab ID map, assigned issues, workers/status, test evidence, blocked/error issues, completion report per issue.

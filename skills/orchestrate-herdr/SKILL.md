---
name: orchestrate-herdr
disable-model-invocation: true
description: "Orchestrate herdr worker tabs for a spec (PRD). Reads a spec/issue URL, finds its open sub-issues, launches one herdr-managed worker tab per issue running a chosen coding CLI, then monitors the tabs until every issue is completed with test evidence, blocked, or errored. Use when running inside herdr (HERDR_ENV=1) and the user wants to fan a spec out to per-issue workers."
---

# Orchestrate herdr

Fan a spec's open sub-issues out to one herdr-managed worker tab each and drive each to a test-backed end state. You are the **orchestrator**: never implement, never close your own tab.

## Inputs

Resolve both before anything else: skill args first (`SPEC_URL=... CODING_CLI=...` or a bare URL plus CLI name; the legacy `PRD_URL=` key is accepted), then ask the user. Never guess; do not proceed until both are set.

- **SPEC_URL** — the spec (PRD) or parent issue whose open sub-issues become workers.
- **CODING_CLI** — the full command that launches the coding CLI in each worker tab, launch flags included — typically the user's auto-accept or permission-preset variant. The prompt is never a launch argument (see Rules).
- **CLI_NAME** — the first token of `CODING_CLI`, the bare binary with no flags. PATH checks and worker-tab names use `CLI_NAME`, never the full command, so they stay stable when only launch flags change.

## Rules

- **Never implement.** The orchestrator reads, creates tabs, submits prompts, monitors, and reports — nothing else.
- **Herdr-managed tabs only,** created in the existing herdr workspace/session. No panes, no internal sub-agents, no nested coding sessions, and never launch `CODING_CLI` from inside another `CODING_CLI`.
- **Stay in the orchestrator's folder.** Never `cd` into task, issue, or any other folder, and never create worktrees; every worker tab starts in this tab's folder and runs only `CODING_CLI` from it.
- **Saved tab IDs only.** Every submit, read, monitor, and follow-up call uses a tab ID saved at creation — never the active tab, latest tab, visual order, or a guess.
- **Prompts are pasted and submitted into a ready CLI** — never passed as launch arguments/flags, never left staged or unsent, and **never pasted into a dead tab's shell**, where the prompt text would execute as commands.
- **Completion requires test evidence:** the worker's test command plus its quoted passing output, read from the tab. An unquoted "tests pass" stays incomplete.
- **Suggest, never auto-chain.** After the final report, suggest `/code-review` on the workers' diffs or `/release-notes` for what shipped — suggest only, then stop.

## Workflow

Emit `Stage / Found / Next / Needs user` at each phase transition — one line per field. Transitions: tabs created, prompts submitted, any worker status change, final report.

### 1. Pre-flight

Fail fast before creating anything, naming what is missing:

1. `HERDR_ENV=1` is set — you are inside herdr. Not set → stop.
2. The herdr companion skill is installed (tab create/submit/read/monitor mechanics). Load it now.
3. `CLI_NAME` resolves on PATH — check the bare binary, not the flagged command, which never resolves — and `gh` is authenticated (`gh auth status`).
4. **Leftover tabs:** tabs named `[CLI_NAME] - GH #<n>` from a previous run of this spec already exist → ask whether to monitor those instead; re-running blindly creates a second tab per issue. User away → monitor the existing tabs and create tabs only for open sub-issues that have none.
5. **Same-repo collision:** workers run simultaneously in one shared working folder. More than one open sub-issue touches the same repo → say so and get explicit confirmation, or agree with the user to run those issues serially. User away → do not fan out: report the collision and stop — shared-tree concurrency is never a safe unattended default.
6. **Worker permission mode:** a fresh `CODING_CLI` session pauses at its own approval prompts (shell, `gh`, test commands) unless launched with an auto-accept/permission preset or the folder pre-approves them. Confirm the mode with the user before fan-out: use the flags they give in `CODING_CLI`, or warn that every worker will need manual approvals. Never pick an elevated or dangerous mode yourself — that is always the user's explicit call.

### 2. Discover sub-issues

Read `SPEC_URL`. Prefer `gh api repos/<owner>/<repo>/issues/<n>/sub_issues`; fall back to task-list checkboxes and "Tracked by" references in the spec body. State the count found and cross-check it against the spec before creating any tab — under-fanning silently drops slices.

### 3. Create worker tabs

Save the current herdr workspace/session ID and working folder; every later step must confirm it acts in that workspace and folder. For each open sub-issue, create one worker tab there named `[CLI_NAME] - GH #<n>` — the bare binary, so a re-run whose launch flags differ still matches the leftover-tab check. Save its tab ID immediately.

### 4. Launch workers

Parallelize the slow parts across tabs:

- Start `CODING_CLI` in every saved tab first, so the CLIs boot concurrently.
- Poll each tab for CLI readiness (its input prompt visible) — every ~5 seconds, up to 60 seconds per tab; never a fixed sleep. Not ready by then → a dead-CLI case under Monitor.
- Paste that issue's worker prompt into its saved tab as soon as it is ready, and submit it.

A worker is not launched until its tab ID is saved, its prompt is submitted, and its first response is visible.

Each worker receives only its assigned issue — never the full spec, never an identical bulk prompt:

```md
GH_ISSUE: #[ISSUE_NUMBER]
GH_ISSUE_URL: [ISSUE_URL]

Work only on this GitHub issue.

Infer project/repo context from the assigned issue.

Use the installed test-first skill: `/tdd` when present, otherwise `/tdd-loop`.

Do not work on the full spec. Do not redo spec orchestration. Do only the
issue-level discovery this issue needs.

Avoid unrelated changes.

Zero attribution anywhere you write — commits, PR titles/bodies, issue
comments, code comments: no `Co-authored-by:` trailers, "Generated with" /
"Made with" footers, "AI-assisted" notes, or tool signature lines; strip any
your tooling injects.

Report back when completed, errored, or blocked.

Completion requires test evidence: the test command and its passing output.
```

Workers with neither skill installed still owe test evidence; say so in the prompts-submitted phase update.

### 5. Monitor

Prefer the herdr companion's wait/state-change primitives to react the moment a saved tab changes; where waiting isn't available, sweep every saved tab ID at least every 30–60 seconds.

- **Stalls:** a worker with no new output for ~3 minutes is stalled — read its tab.
  - The CLI is waiting on a permission prompt → it is not dead; surface it under Needs user for approval, never relaunch it.
  - The CLI died → redo Launch workers for that tab once (relaunch the CLI, wait for readiness, resubmit). Never paste the prompt into a dead shell.
  - A long command (test run, build) still running → allow up to ~3 more minutes.
  - Past that, or any other case → mark the issue blocked and surface it under Needs user.
- **Labels:** `ready-for-agent` marks an issue a worker may take; a worker blocked on a human decision gets its issue flipped to `ready-for-human` with a comment naming the decision. Issue order and dependency notes only sequence dispatch. Never edit issue titles (no `BLOCKER:`, `AFK:`, or `HITL:` markers).
- **Completion:** apply the test-evidence rule per issue — read the tab and quote the passing output.
- **Status board:** on every sweep or state-change wake, emit a one-line count — `N running · M completed · K blocked/needs-user` — naming any tab whose state changed.

### 6. Report

Report workspace/session ID, working folder, tab ID map, assigned issues, and blocked/errored issues, plus per worker its end state and the shortest decisive test tail — the pass/fail line and counts; never dump full logs.

## Completion criteria

- [ ] The final report's tab ID map, read back from herdr, shows one tab per open sub-issue in the stated count
- [ ] Each tab, read back, shows its submitted prompt and a worker response — nothing staged or unsent
- [ ] Every sub-issue's end state is reported: completed with quoted test command and passing output, blocked, or errored
- [ ] Each blocked issue shows `ready-for-human` and a decision-naming comment in `gh issue view`, title unchanged
- [ ] The transcript ends with the final report and the `/code-review` / `/release-notes` suggestion — nothing after it

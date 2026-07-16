---
name: orchestrate-herdr
disable-model-invocation: true
description: "Orchestrate herdr worker tabs for a spec (PRD). Reads a spec/issue URL, finds its open sub-issues, launches one herdr-managed worker tab per issue running a chosen coding CLI, then monitors the tabs until every issue is completed with test evidence, blocked, or errored. Use when running inside herdr (HERDR_ENV=1) and the user wants to fan a spec out to per-issue workers."
---

# Orchestrate herdr

## Purpose

Fan a spec's open sub-issues out to one herdr-managed worker tab each, running a
chosen coding CLI, and monitor them to test-backed completion. You are the
**orchestrator**: you never implement, and you never close your own tab.

## Inputs

Resolve both before anything else. Source order: skill args (a URL plus a CLI
name, or `SPEC_URL=... CODING_CLI=...`; the legacy `PRD_URL=` key is accepted),
then ask the user. Never guess; do not proceed until both are set.

- **SPEC_URL** — the spec (PRD) or parent issue whose open sub-issues become workers.
- **CODING_CLI** — the full command that launches the coding CLI in each
  worker tab, including any launch flags the user wants — typically their
  auto-accept or permission-preset variant (e.g. `claude`, `codex`, or a
  flagged form from the user's own launcher alias). The prompt is never one
  of those arguments (see Rules).
- **CLI_NAME** — the first token of `CODING_CLI`, the bare binary with no
  flags. PATH checks and worker-tab names use `CLI_NAME`, never the full
  command, so they stay stable when only the launch flags change between runs.

## Pre-flight

Check all of these before creating anything; fail fast naming exactly what is
missing instead of stalling mid-run:

1. `HERDR_ENV=1` is set — you are inside herdr. Not set → stop.
2. The herdr companion skill is installed (tab create / submit / read / monitor
   mechanics). Load it now.
3. `CLI_NAME` resolves on PATH — check the bare binary, not the flagged
   command, which never resolves — and `gh` is authenticated (`gh auth status`).
4. **Leftover tabs:** if tabs named `[CLI_NAME] - GH #<n>` from a previous
   run of this spec already exist, ask whether to monitor those instead —
   re-running blindly creates a second tab per issue. If the user is away,
   monitor the existing tabs and create tabs only for open sub-issues that
   have none.
5. **Same-repo collision:** workers run simultaneously in one shared working
   folder (worktrees are banned — see Rules). If more than one open sub-issue
   touches the same repo, say so and get explicit confirmation before
   proceeding — or agree with the user to run those issues serially. If the
   user is away, do not fan out: report the collision and stop — shared-tree
   concurrency is never a safe unattended default.
6. **Worker permission mode:** a fresh `CODING_CLI` session pauses at its own
   approval prompts (shell commands, `gh`, the test command) unless launched
   with an auto-accept/permission preset or the folder pre-approves those
   commands. Confirm the mode with the user before fan-out: use the flags
   they give in `CODING_CLI` (their usual auto-accept launcher), or warn that
   every worker will need manual approvals during the run. Never pick an
   elevated or dangerous mode yourself — that is always the user's explicit
   call.

## Rules (non-negotiables)

- **Never implement.** The orchestrator reads, creates tabs, submits prompts,
  monitors, and reports. Nothing else.
- **Herdr-managed tabs only,** created in the existing herdr workspace/session.
  No panes, no internal sub-agents, no nested coding sessions, and never
  launch `CODING_CLI` from inside another `CODING_CLI`.
- **Stay in the orchestrator's folder.** Never `cd` into task, issue, or any
  other folder, and never create worktrees; every worker tab starts in the
  same folder as this tab, and workers run only `CODING_CLI` from it.
- **Saved tab IDs only.** Save each tab ID immediately at creation; every
  submit, read, monitor, and follow-up call uses a saved ID. Never rely on the
  active tab, latest tab, visual order, or a guessed tab.
- **Prompts are pasted and submitted into a ready CLI** — never passed as
  launch arguments/flags, never left staged or unsent, and **never pasted into
  a dead tab's shell**, where the prompt text would execute as commands.
- **Completion requires test evidence:** the worker's test command plus its
  quoted passing output, read from the tab. An unquoted "tests pass" stays
  incomplete.
- **Suggest, never auto-chain.** After the final report, suggest `/code-review` on
  the workers' diffs or `/release-notes` for what shipped — suggest only,
  then stop.

## Workflow

1. Read `SPEC_URL`.
2. **Discover open sub-issues:** prefer
   `gh api repos/<owner>/<repo>/issues/<n>/sub_issues`; fall back to task-list
   checkboxes and "Tracked by" references in the spec body. State the count
   found and cross-check it against the spec before creating any tab —
   under-fanning silently drops slices.
3. Save the current herdr workspace/session ID and working folder; every later
   step must confirm it is acting in that workspace and folder.
4. For each open sub-issue, create one worker tab in the saved workspace and
   folder, named `[CLI_NAME] - GH #<n>` — the bare binary, so a re-run whose
   launch flags differ still matches the Pre-flight leftover-tab check. Save
   its tab ID immediately.
5. **Launch the workers** — parallelize the slow parts across tabs:
   - Start `CODING_CLI` in every saved tab first, so the CLIs boot
     concurrently.
   - Then poll each tab for CLI readiness (its input prompt visible) before
     pasting — check every ~5 seconds, up to 60 seconds per tab; not ready by
     then → treat it as a dead-CLI case under Monitoring.
   - Paste that issue's worker prompt into its saved tab as soon as that tab
     is ready, submit it, and confirm the first response is visible.
   A worker is not launched until its tab ID is saved, its prompt is
   submitted, and its first response is visible.
6. Monitor per Monitoring until every sub-issue is completed-with-evidence,
   blocked, or errored — then emit the final report.

Emit `Stage / Found / Next / Needs user` at each transition: tabs created,
prompts submitted, any worker status change, final report.

## Worker prompt

Each worker receives only its assigned issue — never the full spec, never an
identical bulk prompt:

```md
GH_ISSUE: #[ISSUE_NUMBER]
GH_ISSUE_URL: [ISSUE_URL]

Work only on this GitHub issue.

Infer project/repo context from the assigned issue.

Use the installed test-first skill: `/tdd` when present, otherwise `/tdd-loop`.

Do not work on the full spec. Do not redo spec orchestration. Do only the
issue-level discovery this issue needs.

Avoid unrelated changes.

Report back when completed, errored, or blocked.

Completion requires test evidence: the test command and its passing output.
```

Workers with neither `/tdd` nor `/tdd-loop` installed still owe test evidence;
say so in the prompts-submitted phase update.

## Monitoring

Prefer the herdr companion's wait/state-change primitives so the orchestrator
reacts the moment a saved tab changes; where waiting isn't available, sweep
every saved tab ID at least every 30–60 seconds.

- **Stalls:** a worker with no new output for ~3 minutes is stalled — read
  its tab.
  - The CLI is waiting on a permission prompt → it is not dead; surface it
    under Needs user for approval. Do not relaunch it.
  - The CLI died → redo Worker Launch for that tab once (relaunch the CLI,
    wait for readiness, resubmit). Never paste the prompt into a dead shell.
  - A long command (test run, build) is still running → allow up to ~3 more
    minutes.
  - Past that, or in any other case → mark the issue blocked and surface it
    under Needs user.
- **Labels:** `ready-for-agent` marks an issue a worker may take; a worker
  blocked on a human decision gets its issue flipped to `ready-for-human` with
  a comment naming the decision. Issue order and dependency notes only
  sequence dispatch. Never edit issue titles (no `BLOCKER:`, `AFK:`, or
  `HITL:` markers).
- **Completion:** apply the test-evidence rule per issue — read the tab and
  quote the passing output.
- **Status board:** on every sweep or state-change wake, emit a one-line
  count — `N running · M completed · K blocked/needs-user` — naming any tab
  whose state changed, so the session always shows how many workers are live.

## Final report

Report: workspace/session ID · working folder · tab ID map · assigned issues ·
per-worker status · quoted test evidence · blocked/errored issues. Then
suggest `/code-review` or `/release-notes` and stop.

## Checklist

Before ending the run:

- [ ] Pre-flight passed (HERDR_ENV, companion skill loaded, CLI on PATH, gh
      auth); leftover tabs and same-repo collisions resolved per Pre-flight
- [ ] Sub-issue count stated and cross-checked against the spec before fan-out
- [ ] One tab per open sub-issue, named `[CLI_NAME] - GH #<n>`, every tab ID
      saved at creation; every action used a saved ID
- [ ] Every worker launched: CLI polled ready (≤60s), prompt pasted and
      submitted, first response seen
- [ ] No implementation, no panes, no nesting, no `cd`, no worktrees, no
      prompts as launch arguments
- [ ] Stall protocol applied: ~3 minutes silent → tab read; permission-prompt
      waits surfaced (not relaunched); dead CLI relaunched once; ~3 more
      minutes for a long-running command; then blocked under Needs user
- [ ] Completions accepted only with quoted test evidence; blocked issues
      flipped to `ready-for-human` with a comment naming the decision; no
      issue titles edited
- [ ] `Stage / Found / Next / Needs user` emitted at each transition; a
      status-board count emitted on every monitoring sweep; final report
      includes the full tab map and evidence
- [ ] Suggested `/code-review` / `/release-notes`, then stopped — no auto-chain

---
name: orchestrate-herdr
disable-model-invocation: true
description: "Orchestrate herdr worker tabs for a spec (PRD). Takes a spec reference — a Linear issue ID (PRWL-100, ABC-123) or a GitHub issue URL/number — finds its open sub-issues in the workspace's tracker of record (Linear or GitHub), launches one herdr-managed worker tab per issue running a chosen coding CLI, then monitors the tabs until every issue is completed with test evidence, blocked, or errored. Use when running inside herdr (HERDR_ENV=1) and the user wants to fan a spec out to per-issue workers."
---

# Orchestrate herdr

Fan a spec's open sub-issues out to one herdr-managed worker tab each and drive each to a test-backed end state. You are the **orchestrator**: never implement, never close your own tab.

## Inputs

Resolve both before anything else: skill args first (`SPEC_REF=... CODING_CLI=...` or a bare spec reference plus CLI name; legacy `SPEC_URL=`/`PRD_URL=` keys accepted), then ask the user. Never guess; do not proceed until both are set.

- **SPEC_REF** — the spec (PRD) or parent issue whose open sub-issues become workers, in its tracker's native form: a Linear issue ID (`PRWL-100`, `ABC-123`) or a GitHub issue URL or number.
- **CODING_CLI** — the full command that launches the coding CLI in each worker tab, launch flags included — typically the user's auto-accept or permission-preset variant. The prompt is never a launch argument (see Rules).
- **CLI_NAME** — the first token of `CODING_CLI`, the bare binary with no flags. PATH checks, `--kind`, and worker-tab names use `CLI_NAME`, never the full command, so they stay stable when only launch flags change.
- **TRACKER** / **TRACKER_TAG** — the workspace's tracker of record and its tag — GitHub `G`, Linear `L`. Derived, not asked: resolve per **Resolve** in [`references/tracker-map.md`](references/tracker-map.md), which holds the per-tracker commands cited by bold section name below.

## Rules

- **Never implement.** The orchestrator reads, creates tabs, submits prompts, monitors, and reports — nothing else.
- **One tracker of record per run.** The workspace `AGENTS.md` names it, not `SPEC_REF`'s shape. Never run `gh issue` against a Linear workspace, or the reverse.
- **Herdr-managed tabs only,** created in the existing herdr workspace/session. No pane splits, no internal sub-agents, no nested coding sessions, and never launch `CODING_CLI` from inside another `CODING_CLI`.
- **Stay in the orchestrator's folder.** Never `cd` into task, issue, or any other folder, and never create worktrees; every worker tab starts in this tab's folder and runs only `CODING_CLI` from it.
- **Saved IDs only.** Every submit, read, monitor, and follow-up call uses a tab ID and agent name saved at creation — never the active tab, latest tab, visual order, or a guess.
- **Prompts are pasted and submitted into a ready CLI** — never passed as launch arguments/flags, never left staged or unsent, and **never pasted into a dead tab's shell**, where the prompt text would execute as commands.
- **Completion requires test evidence:** the worker's test command plus its quoted passing output, read from the tab. An unquoted "tests pass" stays incomplete.
- **Suggest, never auto-chain.** After the final report, suggest `/code-review` on the workers' diffs or `/release-notes` for what shipped — suggest only, then stop.

## Workflow

Emit `Stage / Found / Next / Needs user` at each phase transition — one line per field. Transitions: tabs created, prompts submitted, any worker status change, final report.

### 1. Pre-flight

Fail fast before creating anything, naming what is missing:

1. `HERDR_ENV=1` is set — you are inside herdr. Not set → stop.
2. Load the herdr companion per **Companion** in [`references/herdr-commands.md`](references/herdr-commands.md) unless already in context — it ships inside the binary, so this is a load, not a gate. That file holds the herdr commands cited by bold section name below.
3. `CLI_NAME` resolves on PATH and is a supported `--kind` per **Start agent**; neither → stop, naming the supported kinds.
4. **Tracker:** resolve `TRACKER` and `TRACKER_TAG` per **Resolve**, then run that tracker's access check. `SPEC_REF`'s shape conflicts with the workspace's tracker → stop and ask.
5. **Leftover tabs and agents:** tabs labelled `[CLI_NAME] - <TRACKER_TAG> #<n>`, or live agents holding those slugs, survive from a previous run of this spec → list both per **Context** and ask whether to monitor them instead; a surviving agent name also blocks `agent start` for that issue. re-running blindly creates a second tab per issue. User away → monitor the existing tabs and create tabs only for open sub-issues that have none.
6. **Same-repo collision:** workers run simultaneously in one shared working folder. More than one open sub-issue touches the same repo → say so and get explicit confirmation, or agree with the user to run those issues serially. User away → do not fan out: report the collision and stop — shared-tree concurrency is never a safe unattended default.
7. **Worker permission mode:** a fresh `CODING_CLI` session pauses at its own approval prompts (shell, tracker, test commands) unless launched with an auto-accept/permission preset or the folder pre-approves them. Confirm the mode with the user before fan-out: use the flags they give in `CODING_CLI`, or warn that every worker will need manual approvals. Never pick an elevated or dangerous mode yourself — that is always the user's explicit call. User away → the flags already in `CODING_CLI` are the confirmed mode; none set → proceed and note in the phase update that every worker will pause at its own approval prompts.

### 2. Discover sub-issues

Read `SPEC_REF` and list its open sub-issues per **Discover**. State the count found and cross-check it against the spec before creating any tab — under-fanning silently drops slices. Fan-out covers every open sub-issue; the `ready-for-agent` label does not filter the set. Each issue's native identifier is `<n>` below.

### 3. Create worker tabs

Save the caller's workspace, tab, and folder per **Context**; every later step must confirm it acts in that workspace and folder. For each open sub-issue, create one worker tab per **Create tab**, labelled `[CLI_NAME] - <TRACKER_TAG> #<n>` — `codex - G #42`, `codex - L #PRWL-101`. Save its tab ID, root pane ID, and slugified agent name per **Names** immediately — `herdr agent` calls take the agent name, never the label.

### 4. Launch workers

Parallelize the slow parts across tabs:

- Start every worker per **Start agent**, `CLI_NAME` as `--kind` and the rest of `CODING_CLI` after `--`. Each call blocks until its agent is ready, so issue them concurrently — serially, every worker waits out the one before it. Never poll or sleep for readiness. `agent_not_ready` means it booted straight into an approval UI — surface that under Needs user, never relaunch it; any other error is a dead-CLI case under Monitor.
- Submit that issue's worker prompt per **Submit**.

A worker is not launched until its tab ID and agent name are saved, its prompt is accepted, and its first response is visible.

Fill each worker's prompt from the template in [`references/worker-prompt.md`](references/worker-prompt.md) — one issue per worker, never the full spec, never an identical bulk prompt.

Workers with neither test-first skill installed still owe test evidence; say so in the prompts-submitted phase update.

### 5. Monitor

Wait on lifecycle state per **Watch** — it reacts the moment a worker settles, and needs no sweep. Read a settled tab per **Read**.

- **States:** `blocked` → an approval or question UI; surface under Needs user, never relaunch or answer it. `idle` / `done` → read the tab for the report. `working` → leave it.
- **Stalls:** `unknown` never proves completion, and a start or submit that errors is not a settled state. Only there, fall back to output silence: nothing new for ~3 minutes → read the tab. Agent gone → redo Launch workers once. Long test or build still running → allow ~3 more minutes. Past that → mark the issue blocked under Needs user.
- **Labels:** a worker blocked on a human decision gets its issue flipped to `ready-for-human` with a comment naming the decision, per **Block**. Issue order and dependency notes only sequence dispatch. Never edit issue titles (no `BLOCKER:`, `AFK:`, or `HITL:` markers).
- **Completion:** apply the test-evidence rule per issue — read the tab per **Read** and quote the passing output.
- **Status board:** on every state-change wake, emit a one-line count — `N running · M completed · K blocked/needs-user` — naming any tab whose state changed.

### 6. Report

Report the tracker, workspace/session ID, working folder, tab map, assigned issues, and blocked/errored issues, plus per worker its end state, the shortest decisive test tail — the pass/fail line and counts; never dump full logs — and its reported `Decisions` / `Open items` lines.

## Completion criteria

- [ ] The final report's tab map, read back per **Context**, shows one tab and one live agent per open sub-issue in the stated count
- [ ] Each tab, read back, shows its submitted prompt and a worker response — nothing staged or unsent
- [ ] Every sub-issue's end state is reported: completed with quoted test command and passing output, blocked, or errored
- [ ] Each blocked issue shows `ready-for-human` and a decision-naming comment in the **Verify** read-back, title unchanged
- [ ] The transcript ends with the final report and the `/code-review` / `/release-notes` suggestion — nothing after it

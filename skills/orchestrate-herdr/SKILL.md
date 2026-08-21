---
name: orchestrate-herdr
disable-model-invocation: true
description: "Orchestrate herdr worker tabs for a spec (PRD). Takes a spec reference — a Linear issue ID (PRWL-100, ABC-123) or a GitHub issue URL/number — finds its open sub-issues in the workspace's tracker of record (Linear or GitHub), launches one herdr-managed worker tab per issue running a chosen coding CLI, then monitors the tabs until every issue is completed with test evidence, blocked, or errored. Use when running inside herdr (HERDR_ENV=1) and the user wants to fan a spec out to per-issue workers."
---

# Orchestrate herdr

Fan a spec's open sub-issues out to one herdr-managed worker tab each and drive each to a test-backed end state. You are the **orchestrator**: never implement, never close your own tab.

## Inputs

`SPEC_REF` is resolved first, from skill args (`SPEC_REF=...`, or a bare spec reference; legacy `SPEC_URL=`/`PRD_URL=` keys accepted) and otherwise by asking. The rest are settled at Intake. Never guess an input.

- **SPEC_REF** — the spec (PRD) or parent issue whose open sub-issues become workers, in its tracker's native form: a Linear issue ID (`PRWL-100`, `ABC-123`) or a GitHub issue URL or number.
- **AGENT** — which coding agent runs the workers, named from the six supported runtimes. It yields two values that are not interchangeable: `CLI_NAME`, its launch token, used for PATH checks and tab labels; and `AGENT_KIND`, its herdr `--kind`. Both come from the roster in [`references/intake.md`](references/intake.md) — never from a command's first token, which is wrong for Cursor.
- **CODING_CLI** — `CLI_NAME` plus the permission-mode flags the user picks. The prompt is never a launch argument (see Rules).
- **ISOLATION** — `worktree`, `branch`, or `shared`; it decides whether workers can run in parallel.
- **TRACKER** / **TRACKER_TAG** — the workspace's tracker of record and its tag — GitHub `G`, Linear `L`. Derived, not asked: resolve per **Resolve** in [`references/tracker-map.md`](references/tracker-map.md), which holds the per-tracker commands cited by bold section name below.

## Rules

- **Never implement.** The orchestrator reads, creates tabs, submits prompts, monitors, and reports — nothing else.
- **One tracker of record per run.** The workspace `AGENTS.md` names it, not `SPEC_REF`'s shape. Never run `gh issue` against a Linear workspace, or the reverse.
- **Herdr-managed tabs only,** created in the existing herdr workspace/session. No pane splits, no internal sub-agents, no nested coding sessions, and never launch `CODING_CLI` from inside another `CODING_CLI`.
- **Isolation is the user's choice, and herdr's job.** Never `cd` into task, issue, or any other folder. Create a worktree only when the user picked `worktree`, and only through `herdr worktree create` — never hand-rolled `git worktree add`. In `branch` and `shared` mode every worker tab starts in the orchestrator's folder.
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
3. **Tracker:** resolve `TRACKER` and `TRACKER_TAG` per **Resolve**, then run that tracker's access check. `SPEC_REF`'s shape conflicts with the workspace's tracker → stop and ask.

### 2. Discover sub-issues

Read `SPEC_REF` and list its open sub-issues per **Discover**. State the count found and cross-check it against the spec before creating any tab — under-fanning silently drops slices. Fan-out covers every open sub-issue; the `ready-for-agent` label does not filter the set. Each issue's native identifier is `<n>` below.

### 3. Intake

Ask **one batched question set**, after Discover and never before — two of the four need the issue list. Name the affected issues and repos in the questions. Away-fallbacks and the full matrices: [`references/intake.md`](references/intake.md).

1. **Which coding agent.** Offer all six supported runtimes **by product name** — Codex CLI (`codex`), Claude CLI (`claude`), Antigravity CLI (`agy`), Cursor CLI (`cursor`), Opencode CLI (`opencode`), GitHub Copilot CLI (`copilot`); the parenthesised value is `AGENT_KIND`. Never label an option with a bare binary: Cursor launches as `agent`, which names no product the user would recognise and is not a valid `--kind`. Offer every runtime whose launch token is on PATH and say which are missing.
2. **Which permission mode.** That runtime's elevated preset, quoted from `tool-calling.md` — never retyped from memory — or its bare launch token with the consequence stated. Never pick elevation yourself. The answer becomes `CODING_CLI`.
3. **How work is isolated.** `worktree`, `branch`, or `shared`; `worktree` whenever two open sub-issues share a repo.
4. **Leftover tabs and agents** from a previous run of this spec — monitor them, or create alongside.

### 4. Create worker tabs

Save the caller's workspace, tab, and folder per **Context**; every later step must confirm it acts in that workspace and folder. For each open sub-issue, create one worker tab labelled `[CLI_NAME] - <TRACKER_TAG> #<n>` — `codex - G #42`, `codex - L #PRWL-101`. `ISOLATION` picks the command: `worktree` → **Creating worktrees**; `branch` or `shared` → **Create tab**. Save its tab ID, root pane ID, and slugified agent name per **Names** immediately — `herdr agent` calls take the agent name, never the label.

### 5. Launch workers

Parallelize the slow parts across tabs:

- Start every worker per **Start agent**, `AGENT_KIND` as `--kind` and `CODING_CLI`'s flags after `--`. Each call blocks until its agent is ready, so issue them concurrently — serially, every worker waits out the one before it. `branch` isolation on a shared checkout is the exception: dispatch those workers one at a time. Never poll or sleep for readiness. `agent_not_ready` means it booted straight into an approval UI — surface that under Needs user, never relaunch it; any other error is a dead-CLI case under Monitor.
- Submit that issue's worker prompt per **Submit**.

A worker is not launched until its tab ID and agent name are saved, its prompt is accepted, and its first response is visible.

Fill each worker's prompt from the template in [`references/worker-prompt.md`](references/worker-prompt.md) — one issue per worker, never the full spec, never an identical bulk prompt. It tells each worker to run as many local sub-agent lanes as its CLI supports, and never a cloud agent.

Workers with neither test-first skill installed still owe test evidence; say so in the prompts-submitted phase update.

### 6. Monitor

Wait on lifecycle state per **Watch** — it reacts the moment a worker settles, and needs no sweep. Read a settled tab per **Read**.

- **States:** `blocked` → an approval or question UI; surface under Needs user, never relaunch or answer it. `idle` / `done` → read the tab for the report. `working` → leave it.
- **Stalls:** `unknown` never proves completion, and a start or submit that errors is not a settled state. Only there, fall back to output silence: nothing new for ~3 minutes → read the tab. Agent gone → redo Launch workers once. Long test or build still running → allow ~3 more minutes. Past that → mark the issue blocked under Needs user.
- **Labels:** a worker blocked on a human decision gets its issue flipped to `ready-for-human` with a comment naming the decision, per **Block**. Issue order and dependency notes only sequence dispatch. Never edit issue titles (no `BLOCKER:`, `AFK:`, or `HITL:` markers).
- **Completion:** apply the test-evidence rule per issue — read the tab per **Read** and quote the passing output.
- **Status board:** on every state-change wake, emit a one-line count — `N running · M completed · K blocked/needs-user` — naming any tab whose state changed.

### 7. Report

Report the tracker, agent and isolation mode, workspace/session ID, working folder, tab map, assigned issues, and blocked/errored issues, plus per worker its end state, the shortest decisive test tail — the pass/fail line and counts; never dump full logs — and its reported `Decisions` / `Open items` lines.

## Completion criteria

- [ ] The final report's tab map, read back per **Context**, shows one tab and one live agent per open sub-issue in the stated count
- [ ] Each tab, read back, shows its submitted prompt and a worker response — nothing staged or unsent
- [ ] In `worktree` or `branch` mode, each worker's commits land on that issue's branch and no other
- [ ] Every sub-issue's end state is reported: completed with quoted test command and passing output, blocked, or errored
- [ ] Each blocked issue shows `ready-for-human` and a decision-naming comment in the **Verify** read-back, title unchanged
- [ ] The transcript ends with the final report and the `/code-review` / `/release-notes` suggestion — nothing after it

---
name: factory
disable-model-invocation: true
description: "Conductor for the factory workflow — reads where a spec (PRD), ticket, or PR stands from the tracker, the PR, CI, review, and deploy state, names the one gate it is at, checks that gate's evidence, and suggests the single skill that moves it forward. Use when the user runs /factory, asks \"where is SPEC-142 in the factory\", \"what's next for this PR\", or wants a spec walked from outcome to staging. Started as /factory run — \"/factory run PRWL-127\" for one issue, or \"/factory run automate\" for every issue carrying a label — it carries the chain out itself after one question: builds in T3 Code threads, has a second agent review the code, merges into local or staging, and hands the issue to manual QA. Without run it never implements and never runs the next skill; in both modes it never closes an issue and never goes past staging — production promotion is the owner's. Running one stage directly routes to that stage's skill (/ci-loop, /risk-review, /deploy-watch, /incident-triage)."
metadata:
  version: "1.0.1"
---

# factory

The factory is a state machine over things that already exist — tracker issues, PRs, CI runs, review comments, deploy runs. This skill derives the current state from them, checks the gate out of that state, and names the next skill. It holds no state file: re-running it from any point gives the same answer, so state can never drift.

## Inputs

- **Mode** — `report` (default) or `run`, from the first argument. Enter `run` only when the user's own request says it; a status question never does.
- **Reference** — one of: a spec (PRD) issue (`PRWL-100`, a GitHub issue URL or number), a ticket, a PR number or URL, or the word `start` for an idea with no spec yet. `run` also takes a label name (`/factory run automate`): every open issue carrying it. Missing → ask; never guess from the current branch.
- **Tracker of record** — Linear (via Linear MCP) or GitHub (via `gh`), read from the workspace `AGENTS.md`. Unclear → ask.
- **Staging branch** — default `staging`; confirm with `git ls-remote --heads origin <branch>` before any state that depends on it.

## Rules

- **Report mode is read only.** It reads the tracker, `gh`, and git. It writes nothing remote and edits no file; every state change belongs to the skill it names.
- **Report mode suggests, never auto-chains.** Name the next skill with the exact invocation, then stop. The user runs it. Only `run` mode, started by the user, carries a suggestion out.
- **Gates need evidence, not status words.** A gate passes only on the observable signal in [`references/states.md`](references/states.md) — a green run URL for the head SHA, an agentic-qa and a risk-review marker comment for the head SHA, a deploy-watch pass marker for the merge commit. A label, a chat claim, or "CI is fine" does not pass a gate.
- **Head SHA binds everything.** Review, QA, and risk evidence counts only for the PR's current `headRefOid`; an approval counts only when its review's `commit.oid` is head. A new push sends the PR back to CI.
- **Staging is the ceiling in both modes.** `READY_FOR_OWNER` is terminal. Never suggest a production deploy, a merge or PR into the default or any production branch, or feature-flag rollout; name the owner as the next actor instead.
- **Unreadable signals stop.** A signal the table needs can't be read (tracker access denied, no deploy workflow found) → report `UNKNOWN` with what is missing. Never guess the more advanced state. A failed or erroring `gh` query is unknown — never an empty result, a pass, or green; report the command and its error.
- **Zero attribution.** No co-author, AI, or tool attribution in any output.
- Emit `Stage / Found / Next / Needs user` at each phase transition — one line per field.

## Workflow

### 1. Resolve the unit of work

From the reference, build the list of units to place: a spec expands to all its sub-issues, open and closed (state the count); a ticket or PR is one unit. For each ticket, find its PR: `gh pr list --search "<issue-id>" --state all --json number,headRefName,baseRefName,state` or the tracker's linked-PR field. Closed and merged tickets stay in the list — they may still be in `STAGING`. A `qa-escape` marker other than `not-deployed` places its ticket by the newest later PR.

### 2. Read the signals

Per unit, read only what the state table needs:

```bash
gh pr view <pr> --json state,isDraft,baseRefName,headRefOid,mergeCommit,mergedAt,reviewDecision,reviews,statusCheckRollup,autoMergeRequest,comments,commits
gh pr diff <pr> --name-only
gh run list --workflow <deploy-workflow> --branch <staging-branch> --json headSha,status,conclusion,url
gh issue view <issue> --json state,comments
```

The risk-review marker is a PR comment containing `<!-- risk-review: tier=<low|high> sha=<sha> blocking=<n> -->`. Read it from `comments`; ignore markers for any other SHA. The agentic-qa marker `<!-- agentic-qa: sha=<sha> result=<…> findings=<n> recheck=<n> -->` and the deploy-watch marker `<!-- deploy-watch: merge=<merge-sha> deployed=<run-head-sha> result=<pass|fail> -->` are read the same way; the newest marker wins. The `Acceptance criteria` verdict that clears `BUILDING` is read from the PR body or from a `## QA handoff` comment in `comments` (where `/commit-push-pr` posts it). `qa-escape` markers (`<!-- qa-escape: class=… area=… pr=<n> tested=<sha> reproduced=… -->`) live on the issue, not the PR.

### 3. Place each unit

Match the signals against the table in [`references/states.md`](references/states.md), top row first — the first row whose condition holds is the state. States in order: `OUTCOME`, `TICKETS`, `QA_RETURNED`, `BUILDING`, `CI_STUCK`, `CI`, `QA_STUCK`, `CHANGES`, `QA`, `REVIEW`, `HUMAN_REVIEW`, `MERGE`, `READY_FOR_OWNER`, `DEPLOY_FAILED`, `STAGING`, plus `UNKNOWN`.

### 4. Check the gate and pick one next skill

For each unit, state the gate out of its current state and whether its evidence is present. Pick exactly one next skill per unit from the table's `next` column. When that skill runs or changes code, name the worktree it will use — `<project-repo>/.worktrees/pr-<n>` for a PR, `.worktrees/qa-escape-<issue>` for an escape — so every code-touching step works in isolation per the workspace `AGENTS.md`. For a spec with several units, order the suggestions so a blocked unit (`QA_RETURNED`, `DEPLOY_FAILED`, `CI_STUCK`, `QA_STUCK`, `CHANGES`, `UNKNOWN`) comes before progress on healthy ones; healthy units follow oldest `Since` first, and a unit in one state for more than 3 days is flagged `stalled`. Units that share a gate and skill collapse into one suggestion (for example, `/orchestrate-herdr` for every `BUILDING` ticket of one spec).

### 5. Report and stop

Print the output below. Report mode ends here: do not run the suggested skill, even when the user is away; the next move is theirs.

## Run mode

The user's `/factory run <reference>` approves the whole chain. Read [`references/run.md`](references/run.md) first.

1. **Intake.** Resolve units as in step 1. A label reference lists the open issues carrying it and triages each per **Triage**; one with no checkable outcome becomes `needs-info`, is assigned back to its author, and leaves the run. Missing acceptance criteria are drafted and written. Run the checks in **Start**, then ask its one batch:
   - "Which agent and model builds?"
   - "Which agent and model reviews the code? A different provider than the builder is recommended."

   User away → stop. After this batch the run asks nothing more.
2. **Loop.** One unit at a time, in the order **One unit at a time** gives: place it (steps 2–4), carry out its `Next` per **Stage map**, and place it again; log it and apply **Lessons**. Per unit: status In Progress, its own worktree and **Task stack**, a builder thread, agentic QA, a PR, CI, the **Review loop** between the reviewer and the builder, risk review, **Merge**, **Handover** with status In Review, **Cleanup**. A stage skill is read and followed per **Loading a stage skill**; its stops still stop that unit.
3. **Parks.** A unit whose next actor is a person — a high risk tier, a spent cap, a fact only the reporter holds — is parked with its evidence; the run moves on. No tracked compose file is edited and no issue is closed.
4. **Run report.** The output table, each parked unit's reason, the criteria drafted, and **Lessons** report.

## Output

```
Factory — <reference>  (<n> units)

| Unit | PR | State | Since | Gate evidence | Next |
| ---- | -- | ----- | ----- | ------------- | ---- |
| #418 | #87 | CI | 2026-10-02 14:10 | run 9912 failed on a1b2c3d (unit-tests) | /ci-loop 87 |
| #419 | #88 | HUMAN_REVIEW | 2026-09-28 09:02 (stalled) | risk-review tier=high on 4e5f6a7 (migration) | engineer review — no skill |
| #420 | #85 | READY_FOR_OWNER | 2026-10-01 17:45 | deploy run 9890 success on merge 7c8d9e0, smoke passed | owner promotes — factory ends |

Escapes: 2 qa-escape on this spec — 1 after agentic-qa verified (honesty gap: #418 missed-empty-state)
Next: /ci-loop 87
```

At most one table row per unit; `Gate evidence` names the run, SHA, or comment — never a bare "pass". `Since` is the timestamp of the signal that placed the unit (head push, marker, run), read this run. The closing `Next:` line carries the single most urgent suggestion. When a unit is `UNKNOWN`, its row says which signal is missing. The `Escapes:` line counts the spec's reproduced `qa-escape` markers, excluding class `not-a-regression`, and how many name a PR (`pr=`) whose final head carried a `verified` agentic-qa marker — that count is the honesty gap; name each one.

## Completion criteria

- [ ] Every unit in the spec appears in the table, and the printed unit count matches the total sub-issue count, open and closed, read from the tracker
- [ ] Every `Gate evidence` cell names a run ID, SHA, or comment marker that was actually read this run
- [ ] Report mode: `git status` and the PRs show no change made by this run, and no next skill was invoked
- [ ] Run mode: every unit ends merged with a `factory-delivered` comment read back, or parked with a named reason; no issue was closed and `git status` shows no compose file changed

# Factory run

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Mechanics for `run` mode. `SKILL.md` holds the loop and the **Load map**; this file holds stage loading, run-wide limits, the **Stage map**, scheduling, tracker status and the per-round records every stage uses. Stage files load per the **Load map**: [`intake.md`](intake.md) for **Start** and **Triage**; [`build.md`](build.md) for **Task stack**, **Build**, **After a fix**, **Check cadence** and **Screenshots on the issue**; [`review-loop.md`](review-loop.md) for **Review loop**; [`review-and-delivery.md`](review-and-delivery.md) for **Merge**, **Staging**, **Handover** and **Cleanup**; [`returned-by-qa.md`](returned-by-qa.md) for `QA_RETURNED`. Every gate in those files binds as if it were here.

## Contents

- Loading a stage skill
- Comments only
- Execution questions only
- Stage map
- Dependency-aware scheduling
- Tracker status
- Round log
- Lessons
- Readiness and recovery
- Moved sections: Start, Triage (`intake.md`); Task stack, Build, After a fix, Check cadence, Screenshots on the issue (`build.md`)

## Loading a stage skill

User-invoked stage skills use the worker-turn procedure below. Claude Code refuses a Skill-tool call for one and forbids repeating its steps another way, so the run starts a stage skill only as the user would: its slash command as the first token of a worker turn on the selected backend, with its arguments and a private brief the arguments name. The parent never calls the Skill tool for a stage skill and never performs its steps itself.

1. Confirm the skill is installed in the worker's runtime. Not installed → park the unit and name `npx skills add devarfeen/agent-skills-kit -g --skill <name>`.
2. Submit `/<name> <args>` per the backend file: one line, no leading whitespace, short (herdr: under 700 characters, or a typed prefix plus pasted body). Put the brief, criteria source, checkout record and the facts its **Run authorization** needs in a private file the line names. Read the worker's first items back: a turn that shows no skill load ran no skill; resubmit once correctly, then park with `stage_skill_not_invoked`.
3. The skill's **Run authorization** line says what the run's start already approved; a skill without that line keeps every approval it asks for. The brief answers its intake from **Start**; it asks the user nothing (**Execution questions only**).
4. Classify local setup/testability failures through **Readiness and recovery**, and stopped-worker failures through **Execution**, before parking. These exceptions repeat the original gate; **Execution** defines the factory-only post-commit resume exception. Every other refusal still stops the unit: an unmet criterion, a refused merge, missing authority or input, or an exhausted cap. Park with evidence; never do a refused step by hand.
5. Where the skill stops, suggests a next skill, or ends, read its bounded report and place the unit again.

A model-invoked skill (`tdd-loop`, `code-review`, `risk-review`) is called with the Skill tool as usual in its assigned worker. For `risk-review`, REVIEW explicitly passes `local`; RISK explicitly passes `pr <number-or-url>` and the run authorization. The parent remains the supervisor, not the stage executor. `using-git-worktrees` is user-invoked; an explicitly started `/factory run` may read it for its task-checkout setup only, through the backend's own worktree command and without a Skill-tool invocation. This exception grants no cleanup or unrelated workflow authorization. `local-to-staging`, `staging-fix`, and `staging-to-production` are model-invoked but still start through the worker-turn procedure above, so their **Run authorization** lines apply.

## Start

In [`intake.md`](intake.md#start).

## Comments only

A run never edits an issue's title or body, on any tracker. Everything it writes to an issue — drafted criteria, notes, findings, evidence, handover — is a new comment, so the issue keeps its reporter's text and a dated chain of events. Labels, assignees, and status are still set as the sections here say.

## Execution questions only

After execution setup the run asks the user nothing, except when both authorized review routes are unavailable under [Factory model selection](review-models.md). A fact it lacks is read from the tracker, the repository, or a local reproduction. One it cannot get parks that unit, with the question written out for whoever holds the answer. Never ask the user to guess a fact about someone else's report, and never ask whether to do something a rule here already forbids.

## Triage

In [`intake.md`](intake.md#triage).

## Stage map

Place the unit with `states.md`, then act on its state. `Next` in that table is still the authority for which skill; this table says what the run does with it. Per unit: status In Progress, its own worktree and **Task stack**, a builder worker on the selected backend, agentic QA in a QA worker, a PR, CI, the **Review loop** between the reviewer and the builder, risk review, **Merge**, **Handover** with status In Review, **Cleanup**, **Promotion**, **Staging**.

| State | Run action |
| ----- | ---------- |
| `QA_RETURNED` | **Returned by QA** in [`returned-by-qa.md`](returned-by-qa.md) |
| `BUILDING` | Existing non-draft PR lacking only the current-head acceptance verdict → load `commit-push-pr` in its verified PR checkout to check criteria and refresh the handoff; preserve its branch and create no duplicate PR. Otherwise **Build** in [`build.md`](build.md) |
| `CI` | Apply [`ci-policy.md`](ci-policy.md): pending known checks → use the backend's owned PR watch when supported, else bounded waits, while other ready units may advance; failing → load `ci-loop`. Missing/unreadable required checks → park, never wait for nonexistent CI or waive a required gate |
| `QA` | Load `agentic-qa` in the **QA worker** (**Execution**), then **Screenshots on the issue** ([`build.md`](build.md)). A valid `## QA carried forward` record ([records.md](records.md)) for head settles this state. Findings → **After a fix**. Local-runtime blockers → **Readiness and recovery**, then repeat affected QA within its cap. Remaining `blocked` or `partial` → park, naming the missing input or gap cells |
| `CHANGES` | Risk, QA, or code-review findings → **After a fix**. `CHANGES_REQUESTED` from a person → park; name `/pr-feedback <pr>` |
| `REVIEW` | Read [`review-loop.md`](review-loop.md). After a fix push that answered a review round, test **Fix-only close** before dispatching a reviewer. Otherwise **Review loop** until it settles on head, then the RISK step: dispatch a fresh `<issue-id> risk` worker through **Execution**, using the active review model for it and every child/judge, that loads `risk-review` with `pr <number>` and the run authorization; it may post the marker comment and request reviewers, nothing else. Low tier → `MERGE`; high tier → reviewers requested, unit parks at `HUMAN_REVIEW` for a person to approve and merge |
| `MERGE`, PR open | **Merge** in `review-and-delivery.md`, including workspace migration policy and human-run prerequisites |
| `MERGE`, PR merged into `local` | **Handover**, then **Cleanup**, then **Promotion**, in `review-and-delivery.md` |
| `STAGING` | **Staging** in `review-and-delivery.md` |
| `READY_FOR_OWNER` | **Handover** (`review-and-delivery.md`) when no delivery record matches this PR and merge revision, then **Cleanup**. Done; it joins **Production readiness** there |
| `DEPLOY_FAILED` | **Deploy failure** in `review-and-delivery.md` |
| `OUTCOME`, `TICKETS`, `CI_STUCK`, `QA_STUCK`, `HUMAN_REVIEW`, `UNKNOWN` | Park with the state's evidence and its `Next` — a person decides here |

For staged units, report the event-owned handoff from [records.md](records.md) independently of deployment state, including `DEPLOY_FAILED` or unreadable deploy routing. A handoff does not clear the parked deploy gate.

A parked unit is not retried in the same run. Running `/factory run` again with the same reference places every unit afresh, so it resumes where the signals say the work stands.

## Dependency-aware scheduling

The parent schedules ready stages rather than serializing whole units. Read issue/repository dependencies and planned write ownership first. Prioritize existing PRs, QA returns, prerequisites, then oldest ready work. Unknown independence queues a unit until discovery resolves it; a unit depending on a parked prerequisite parks with that dependency.

Overlap only independent units with separate verified worktrees/branches, disjoint writer ownership, private dependencies/outputs/data and task runtimes. Shared routes, components, contracts, tables or migrations require dependency analysis; shared writable resources serialize. Respect live executor capacity and workspace limits (at most three concurrent writers unless workspace policy explicitly authorizes more); read-only QA/review lanes also consume executor slots. Never dispatch another writer into an occupied or unknown-status checkout. Within one unit, the parent may prepare private PR text and neutral reviewer inputs while its QA worker runs, under [delivery drafts](delivery-drafts.md); independent review still waits for current-head CI and QA.

A CI/deploy wait, read-only review or evidence publication may overlap another unit's build or isolated QA. Grant a browser lease before any browser work: a shared browser/session has one owner until release; parallel browsing requires supported separate contexts with isolated cookies/navigation. Queue browser stages without blocking unrelated non-browser work. Record owners and release/reconcile leases after confirmed worker stop. Unknown ownership preserves the lease and blocks conflicting use.

The parent alone serializes integration and remote merges per repository. Pin each unit's base/head. A dependent unit starts from a base containing its completed prerequisites. If the delivery base moves while an independent unit is active, check its diff/ancestry and compatibility before integration; reconcile on the unit's branch through authorized local operations, then rerun invalidated checks and current-head QA/review/risk gates. Never silently carry old head evidence across a merge or rebase. Designate and verify the integration checkout before shipping/merge (the unit checkout may serve once it contains the current base and intended batch). The final canonical full check covers all integrated changes there after the last edit; sharing a repository alone does not make one unit's proof cover another checkout.

Apply every per-unit stage, cap and cleanup guard. The scheduler changes timing, not gates. **Lessons** is read before each dispatch. Report `N running / M done / K blocked`, each active lane's unit/stage/ownership, and after each terminal unit `<unit> — merged | parked: <reason> — <n> of <m>`. Pending healthy work is running or queued, not parked merely to free capacity.

## Tracker status

The issue's status follows the work, so a person reading the tracker sees where it stands.

- **In Progress** — when **Build** starts for the unit, including the rebuild of a returned issue.
- **In Review** — at **Handover**. It stays there through manual QA. **Moved by promotion** in [`review-and-delivery.md`](review-and-delivery.md#moved-by-promotion) re-checks it after each promotion and staging fix.

Take each status name from the workspace's issue-tracker document when it lists them; otherwise use the tracker's own status of that name for the issue's team (Linear: the live status list). Not found → skip the change and report it under Needs user; never create a status. GitHub issues have no status: skip, unless the workspace names a label or project field for each. Read every change back.

Never set a completed or cancelled status and never close an issue. The person doing manual QA closes it. **Handover** in [`review-and-delivery.md`](review-and-delivery.md) restores an issue the merge closed.

## After a fix

In [`build.md`](build.md#after-a-fix).

## Check cadence

In [`build.md`](build.md#check-cadence).

## Round log

`<artifacts-root>/specs/factory/rounds.md` records every check round, so a later round or run can read what went wrong and how often. It is a log, never state: placing a unit reads only `states.md` signals. Only the run writes it; workers never do.

Resolve `<artifacts-root>`: the `*.code-workspace` directory if one exists, else the per-context root (`GLOSSARY-MAP.md` at repo root; legacy `CONTEXT-MAP.md`), else the repo root.

Missing file → create it with the zero-attribution line from the top of this file and this header, then append:

```md
| Date | Unit | Project | PR | Round | Check | Result | Cause | Tried |
| ---- | ---- | ------- | -- | ----- | ----- | ------ | ----- | ----- |
| 2026-10-10 | #418 | BILLING-WEB | #87 | 1 | agentic-qa | 2 fail | not-wired | first build |
| 2026-10-10 | #418 | BILLING-WEB | #87 | 2 | agentic-qa | pass | - | feat: add order form and route |
```

Append at worker dispatch/recovery and when a check returns for a unit — a readiness repair, an `agentic-qa` result, a `ci-loop` attempt, a `risk-review` marker, a **Review loop** round, a `qa-escape` marker. A passing round is one row; a failing round is one row per distinct cause.

- **Check** — `execution`, `readiness`, `agentic-qa`, `ci`, `risk-review`, `code-review`, or `qa-escape`.
- **Cause** — for `execution`, `readiness` or `ci`, the failing operation/check's name. Otherwise one slug from the class list in the `qa-escape` skill's `references/escape-classes.md`, chosen by that file's rule; no slug fits → `other:<two-word-slug>`. `-` on a pass. Name the missing check, not the symptom: a word broken mid-line is `responsive-layout`, a failed save with no message is `missed-error-state`. A bare slug outside the list is invalid, because **Lessons** counts only matching slugs. When workspace policy names a round-log check, run it before **Lessons** counts and before the run report; fix the rows it rejects.
- **Tried** — execution uses the worker/budget record in **Execution**, plus preferred/active model, effort, role and availability recovery/fallback record; readiness uses the repair record in **Readiness and recovery**. Other checks use the subjects of commits made since the unit's previous round; `first build` on round 1.

Every cell comes from evidence read in that round. `PR` is `-` until one is open.

For `code-review`, append `nit-only=yes|no`, `scope-grew-in-review=yes|no` and `finding-ledger=<report/comment locator>` in Tried, including passing rounds. `nit-only=yes` means all selected axes and the judge completed with suggestions but no confirmed in-scope defects or unresolved material claims; an incomplete review records `nit-only=no`. Scope growth means observed edits or requested work beyond the agreed criteria, not added line count; cite the evidence and park unauthorized behavioral expansion. When it causes a failure, use existing Cause `other:review-scope`; never silently add a new cause vocabulary. Lessons may learn from repeated evidenced scope failures under its existing threshold. Nit-only is an observation, not a failure cause or permission to edit policy. Preserve the table columns and existing Cause rules; no runbook, digest or automatic skill/config edits are added.

## Lessons

`<artifacts-root>/specs/factory/lessons.md` holds how-to-work lines learned from the round log. Count before each worker or fix dispatch, and again before the run report.

1. **Find.** In `rounds.md`, a `Cause` other than `-` that appears for the same `Project` in three distinct units, counting earlier runs, is a habit. Rows whose `Result` is `reproduced no` are never counted.
2. **Write.** A habit with no line yet gets one, appended without asking (missing file → create it with the zero-attribution line first):

   ```md
   - BILLING-WEB — connect each feature to a screen a user can open in the same round its tests pass. (not-wired: #418, #421, #430)
   ```

   The instruction names one action a worker takes, drawn from the `Tried` cells of the rounds that cleared the cause. A habit that already has a line gains the new issue number in that line; never a second line for one cause and project.
3. **Pass on.** At every dispatch, paste the lines for the unit's project into the worker prompt's `LESSONS:` field, or into the fix instruction. Paste the text; a path the worker may skip is not a lesson delivered.
4. **Report.** The run report ends with `Rounds:` — for each unit that needed more than one round, what failed and which commit cleared it — and `Lessons added:` — each line written or extended this run, then the file path, so the user can edit or delete it. Read both files back before printing.

A lesson changes how a worker works, never what is checked. It never edits, removes, or relaxes an acceptance criterion, a test, a QA grid row, a marker, a state-table row, a cap, or a stop, and never tells a worker to skip one. A cause that shows in three more units after its line was written is reported under Needs user as `lesson not holding`, naming `/qa-escape` — a check that cannot be skipped is the stronger guard. The `## QA escape guards` in `AGENTS.md` stay `/qa-escape`'s, with its own approval.

## Task stack

In [`build.md`](build.md#task-stack).

## Readiness and recovery

Before task-stack setup and when a stage reports a local-runtime blocker, load [`readiness-and-recovery.md`](readiness-and-recovery.md). It owns readiness evidence, repair classification, the per-unit repair cap, and resume rules. Passing readiness never substitutes for acceptance, QA, CI, review, or shipping gates.

## Build

In [`build.md`](build.md#build).

## Screenshots on the issue

In [`build.md`](build.md#screenshots-on-the-issue).

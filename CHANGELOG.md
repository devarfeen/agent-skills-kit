# Changelog

Zero attribution: never add or leave co-author, AI, or tool attribution in this file.

Dated entries, newest first. Each names the skills whose behavior changed and
their new versions, so a workspace on an older copy can see what an update
brings. Generated `AGENTS.md` files carry the `agents-md` marker version;
re-run `/agents-md` after a marker bump.

## 2026-10-10

### Changed

- **`/factory` 1.0.0 — a run is hands-off after one question.** It asks which
  agent and model builds and which reviews, then asks nothing. The four end
  pauses (review, merge, close, cleanup) and the done-list question are gone.
  Workers always run as T3 Code threads with full access; herdr tabs and local
  sub-agents are no longer offered by a run.
- **Review loop.** A second agent reviews each PR and posts its findings on the
  issue; the builder fixes or declines each, up to three rounds.
- **Merge and handover.** A low-tier PR that passed every gate is merged into
  `local` or the staging branch through GitHub. The run posts the handover
  comment, sets the issue In Progress and then In Review, and cleans up. It
  never closes an issue. The local trial merge is removed.
- **One app per issue.** Each worktree gets its own copy of the app from a
  temporary compose file under `.worktrees/`. No tracked compose file is edited.
- **Manual QA on staging.** `/local-to-staging` 0.1.0 and `/deploy-watch`
  0.3.0 assign a delivered issue to manual QA once staging holds its merge
  commit and the deploy succeeded.
- **`/orchestrate-t3` 0.3.0** asks nothing and registers a missing project
  when a run loads it, and its worker prompt takes a `STACK:` field.
- **`/agents-md` 0.4.0, marker v49** — the Rule 18 `/factory run` line matches
  the above. Re-run `/agents-md` to pick it up.

### Added

- **`/factory` 0.5.0** — `/factory run <issue>` drafts missing acceptance
  criteria for a single issue too, and shows them before the build. It still
  changes no label for a single issue.
- **`/orchestrate-t3` 0.2.0** — a thread is titled with the issue's own
  identifier (`PRWL-127`, `#42`) instead of the tracker tag and number.

- **`/factory` 0.4.0 — a run learns from its rounds.** Each check round is
  logged in `specs/factory/rounds.md`. The same cause in three issues of one
  project becomes a line in `specs/factory/lessons.md`, written without asking
  and pasted into every later worker and fix prompt. A lesson never changes a
  criterion, test, gate, cap, or stop. Placement still reads no file.
- **`/factory` 0.4.0 — locked checks.** A fix round that deletes a test or
  removes an assertion parks the issue unless the worker named the contract
  change. Acceptance criteria that changed since intake park it before the PR
  opens.
- **`/factory` 0.4.0 — before the build.** The start questions open with a
  preflight (test command, app start command) and show any acceptance criteria
  triage drafted, which are written to the issue only after your answer.
- **`/factory` 0.4.0 — a run works issues QA sent back.** A `QA_RETURNED`
  issue is no longer parked: the run follows `/qa-escape`, then rebuilds from
  the regression test it names. `/qa-escape` 0.3.0 gains a Run authorization
  for its comment and label, and a `not-deployed` class for a report made on an
  environment the fix had not reached. Guards, staging access, and promotion
  stay with the user.
- **`/factory` 0.4.0 — screenshots on the issue.** After every QA round a run
  attaches the before and after screenshots to the Linear issue, or on GitHub
  posts a comment listing their local paths. Images go nowhere else.
- **`/agentic-qa` 0.3.0** records a `not-wired` finding instead of
  `no-ui-reach` when a criterion describes something a user sees or does and
  no screen reaches the change. `/qa-escape` 0.3.0 adds the `not-wired` class.
- **`/orchestrate-t3` 0.1.0, `/orchestrate-herdr` 0.2.0** — the worker prompt
  asks for the entry point of each user-visible criterion and a list of every
  existing reader of a changed rule, format, or field, forbids editing the
  issue body or removing an assertion to reach green, and takes an optional
  `LESSONS:` field that only `/factory run` fills.
- **Companions.** `before-and-after`, `code-structure`, and
  `evidence-driven-testing` from michaelshimeles/skills are listed as optional
  companions (`/agents-md` 0.3.1). They stay separate installs and no kit
  skill calls them. `before-and-after` is listed for local capture only;
  screenshots are never uploaded.

## 2026-10-08

### Added

- **`/orchestrate-t3` 0.0.1** — fans a spec's open sub-issues, or a list of
  issues, out to T3 Code threads through the T3 Code MCP server. Issues that
  block one another or touch the same surface share one worktree and thread;
  the rest get their own. The kit creates each worktree under `.worktrees/`
  and binds the thread to it. Needs a one-time `mcp add` and sign-in above
  read-only. `/ask-kit` 0.0.2 lists it.
- **`/commit-push-pr` 0.3.0** — opt-in **Merge into local** step. When the
  request asks for the merge and the PR base is `local` (and `local` is not the
  default branch), it merges through GitHub's own gates after the usual draft
  approval. Every other base still ends at an open PR.

- **`/factory` 0.3.0 — run mode.** `/factory run <label or reference>`
  (`/factory run automate`) carries the chain out: triages every open issue
  carrying the label, builds through `/orchestrate-t3`, `/orchestrate-herdr`,
  or local sub-agents, runs `/agentic-qa`, opens PRs, and drives CI and
  `/risk-review`. It pauses for code review, merge (GitHub then local, GitHub
  only, or a local trial), issue close, and cleanup. An issue with no checkable
  outcome becomes `needs-info` and is assigned back to its author. Plain
  `/factory` is unchanged and read-only.
- **Run authorization.** `/ci-loop` 0.3.0, `/agentic-qa` 0.2.0,
  `/risk-review` 0.4.0, `/deploy-watch` 0.2.0, and the ship policy
  (`/commit-push-pr` 0.4.0, `/commit-push-close` 0.2.2) treat the start of a
  `/factory run` as their draft or comment approval. Run directly, each keeps
  its gate; under a run every safety stop still stops that issue.
- **`/agentic-qa` 0.2.0** saves a `before` screenshot per route from the base
  run and an `after` from the head run.
- **`/writing-kit-skills` 0.3.0** names `/factory run` as the one skill that
  may follow a user-invoked skill's `SKILL.md`.

### Fixed

Found in a review of `/factory run` against the skills it loads.

- **`/agents-md` 0.3.0, marker `v48`** — Rule 18 names `/factory run`. Without
  it a generated `AGENTS.md` forbade the run's merge, issue close, and cleanup.
  Re-run `/agents-md` in each workspace before using `/factory run`.
- **`/factory` 0.3.1** — triage appends acceptance criteria to the issue body,
  where the ship skills and `/agentic-qa` read them, not to a comment. A PR
  merged into `local` ends the run for that issue instead of returning to the
  merge pause. A fix after the PR is open is pushed through `/commit-push-pr`.
  QA runs on a clean worktree so the tested SHA is the shipped SHA. The start
  questions are named in `SKILL.md`. herdr runs without a spec use its harness
  mode.
- **Ship policy** (`/commit-push-pr` 0.4.1, `/commit-push-close` 0.2.3) — under
  a run, several issues on one branch take the first issue's title as the
  naming anchor, and the run's QA report counts as the agentic-qa marker.
- **`/orchestrate-t3` 0.0.2**, **`/orchestrate-herdr` 0.1.2** — workers drive
  each issue with `/implement` when it is installed; T3 workers never push.

### Changed

- **`/risk-review` 0.3.0** offers auto-merge for a low-risk, zero-blocking PR
  into the staging branch or `local`; it was staging only.
- **`/factory` 0.2.0** places a PR into `local` through `MERGE` and points a
  merged one at `/local-to-staging`.
- **Ship policy** (`/commit-push-close` 0.2.1): names the one merge exception.

## 2026-10-05

Follows Matt Pocock's skills v1.3.0 / v1.3.1.

### Breaking

- **`CONTEXT.md` is now `GLOSSARY.md`** (`CONTEXT-MAP.md` → `GLOSSARY-MAP.md`),
  matching upstream. Kit skills read a legacy `CONTEXT.md` when it is the only
  one present. `/agents-md` (marker `v47`) offers an ask-first rename.
- **`/pr-feedback` 0.2.0** no longer hands off to `/commit-push-pr` itself. It
  stops after the tested local fixes and asks you to run it, then answers the
  threads.

### Added

- **`/ask-kit` 0.0.1** — router over the kit's own skills.
- **Ship policy** (`/commit-push-pr` 0.2.0, `/commit-push-close` 0.2.0):
  `Before:` / `After:` evidence and a Merge danger block (`Door:`,
  `Blast radius:`) in every QA handoff; a `Root cause:` line on bug-fix
  commits; a pre-commit search for leftover debug instrumentation; a path for
  branches that already carry commits, with a scan of their messages; several
  issues on one branch.
- **`/commit-push-pr`**: optional Summary visual, Evidence and Merge danger
  sections in the PR body; its headings win over a PR-body skill such as `pr`.
- **`/risk-review` 0.2.0**: trigger 12, one-way door — declared, or a
  `two-way` claim the diff contradicts.
- **`/agents-md` 0.2.0, marker `v47`**: routing for `/implement-spec`, `/pr`,
  and `/retro`; the phase-boundary order; glossary migration.
- **`/qa-escape` 0.2.0**: guards classify mechanical versus judgement escapes
  first.
- **`/staging-fix` 0.2.0, `/ci-loop` 0.2.0**: tagged debug instrumentation,
  minimised reproduction, root cause in the PR.
- **`writing-kit-skills` 0.2.0**: rules for calling another skill, the cache
  failure mode, and why user-invoked skills keep trigger descriptions.
- Tracked pre-commit hook at `tools/hooks/pre-commit`.
- `.out-of-scope/` records declined ideas.

### Changed

- Manifest: `/implement-spec`, `pr`, `retro`, and `/ask-kit` rows.
- `/orchestrate-herdr` 0.1.1: description boundaries toward the `herdr`
  companion and `/implement-spec`.
- Trigger-eval catalog refreshed to mattpocock/skills v1.3.1; the removed
  `resolving-merge-conflicts` is gone.
- Patch bumps for the renamed canonical artifacts-root line: `agentic-qa`,
  `design-system`, `incident-triage`, `integration-contract`, `pixel-audit`,
  `polish-batch`, `port-feature`, `release-notes` (0.1.1); `feature-discovery`
  and `feature-prompt` (0.2.0).

# Changelog

Zero attribution: never add or leave co-author, AI, or tool attribution in this file.

Dated entries, newest first. Each names the skills whose behavior changed and
their new versions, so a workspace on an older copy can see what an update
brings. Generated `AGENTS.md` files carry the `agents-md` marker version;
re-run `/agents-md` after a marker bump.

## 2026-10-16

### Changed

- `/factory` 5.4.1 and `/orchestrate-t3` 0.11.1 align entrypoint wording,
  README, GUIDE and BEST-PRACTICES with the implemented operating modes.
  Documentation distinguishes stateless reports from durable runs, preserves
  harness choice, explains active waits and queued compaction, and records
  readiness, context and host limitations. Execution behavior is unchanged.
- `/agents-md` 0.6.2 updates the factory companion's manifest wording to retain
  executor choice and ask only for a missing reviewer. Generator templates and
  their version marker are unchanged.
- `/factory` 5.4.0 and `/orchestrate-t3` 0.11.0 support binary-host queued
  native compaction with a separately queued continuation and durable receipts.
  `WAITING_COMPACTION` names that automatic boundary. Child completion priority
  remains explicit; this is not a pre-delivery guard. Optional native runners
  preserve any selected harness/provider/model instead of forcing one CLI.
- `/factory` 5.3.0 and `/orchestrate-t3` 0.10.0 keep active supervisors waiting
  for workers and runtime preparation, then continue automatically. Portable
  Markdown status lists use semantic color badges, owner/action fields and
  worker counts. Recovery prompts stay in checkpoints during active work;
  genuine human blockers show three reasoned recovery options with preserved
  gates and attempt caps.
- Both workflows checkpoint at 60% observed root context occupancy and use
  supported compaction before the next long phase, accounting for pending
  returns and the existing 25% reserve. Stage-scoped instructions, fresh scoped
  workers and bounded reports reduce root growth. Host restart and automatic
  delivery still require actual supported runtime integration.
- `/factory` admits browser QA only after verified task worktree, BASE/HEAD
  services, served revision and applicable readiness checks. An unready app
  waits for its runtime owner; it cannot trigger browser-tool fallback.

## 2026-10-15

### Breaking

- `/factory` 5.0.0 inherits the builder harness, provider and model from the
  user-started session instead of asking for them. Explicit overrides remain
  supported. It asks only for the reviewer and preserves both choices on resume.

### Changed

- `/factory` 5.2.0 and `/orchestrate-t3` 0.9.0 separate T3 thread binding
  from product execution ownership. LUCETT-WORKSPACE keeps every supervisor,
  builder, reviewer, QA and standalone task thread at its workspace root;
  supported child delegation inherits that binding while commands and edits
  use verified product worktrees. No product thread or registration is needed.
  Readiness, checkpoints and handoffs verify both identities on macOS, Linux
  and WSL2. Fresh reviewer sessions, telemetry gates and writer ownership remain.
- `/factory` 5.1.0 checks a workspace adapter's read-only local telemetry source
  when MCP omits usage or window data. It binds occupancy to the current root
  native thread and preserves sample freshness on macOS, Linux and WSL2.
  Return contracts must fit the allowance with metadata, transport overhead
  and all pending returns, without understating costs or raising caps to pass.
- `/factory` 5.0.0 and `/orchestrate-t3` 0.8.0 require explicit prepared-checkout
  launch binding and live identity verification before worker writes. Supervisor
  identity stays separate from product-worker assignments. Factory repeats
  supervisor preflight before every completion import and preserves helper
  failures through wrappers.
- Both skills save an unfinished-session handoff with current state, required
  setup and a copyable next prompt. They route to a workspace handoff adapter
  when available and describe host output from checkpoints after interruption.
  Bounded recovery continues before parking; explicit pause and stop remain
  stopped. Host restart and forced-interruption output require host integration.
- `/orchestrate-t3` 0.8.0 also inherits its workers' builder identity and retains
  its permission-mode and grouping intake.

### Fixed

- **Plan-restricted CI policy** — `/factory` 4.4.1 no longer parks a unit
  when GitHub refuses branch protection and ruleset reads with its
  plan-restriction 403 on a private repo. Once the private visibility, the
  caller's admin permission and a `free` owner plan are confirmed, the run
  records `no GitHub-enforced checks (plan)`. It then gates on PR-triggered
  workflows and mandated local checks. Any other 403 stays `UNKNOWN`.

## 2026-10-14

### Changed

- **Ship skills are user-invoked only** — `/local-to-staging` 2.1.1,
  `/staging-to-production` 0.2.1, `/staging-fix` 0.5.1, `/deploy-watch` 2.0.2,
  `/commit-push-pr` 0.9.1 and `/commit-push-close` 0.6.1 now state in the body
  that they start only when the user invokes them or a user-started
  `/factory run` loads them; any other skill or agent may only suggest them.
  The frontmatter already disabled model invocation. The body rule covers
  runtimes that ignore that flag.
- **Factory run ships to staging** — `/factory` 4.4.0 run mode now loads the
  promotion and staging skills itself. After a merge into `local` it runs
  `/local-to-staging` 2.1.0 once per round for the run's repos, then
  `/deploy-watch`. A failed deploy gets one `/staging-fix` 0.5.0, whose PR
  goes through the run's usual gates rather than auto-merge. A run that
  reached `READY_FOR_OWNER` ends with a read-only `/staging-to-production`
  0.2.0 report. Each skill gains a **Run authorization** line and stays
  user-invocable. Production promotion stays with the owner, and the run
  still never closes an issue, so it never loads `/commit-push-close`.
- **Fix-only review close** — `/factory` 4.3.0 ends the review loop without
  another reviewer round when every finding was fixed, the fix touches only
  cited lines and a mechanical comparison proves no behavior change. The
  parent posts a `## Code review fix check` record bound to head; any doubt
  runs the next round. The three-round cap is unchanged.
- **Factory run feedback** — `/factory` 4.3.0 asks the start question batch
  again: which agent and model builds and which reviews, with options from the
  live T3 or native executor catalog; user away stops the run, and it asks
  nothing more after the batch. QA browser work and evidence publication run
  in a QA worker that returns a bounded summary; the parent checks images by
  metadata and never reads image bytes or oversized saved output. Build and
  fix rounds run focused checks; the full check runs once per head at ship;
  an environment failure resumes from the failed stage; a comment-only change
  reruns only the stages that read comments. `## QA` and `## Delivered` gain a
  `Checks:` block. A new `## QA carried forward` record carries a QA result to
  a head whose diff provably cannot reach a screen; CI and code review still
  run. Reviewer and builder provenance lines appear in code review records
  only when the workspace allows them. QA publication is the four screenshots
  and `results.json`; report and grid stay local and no archive is built.
  Cleanup is automatic: it calls the task adapter's destroy command for BASE
  and HEAD, re-verifies reused attachments from the proof-wide pending list,
  cleans superseded QA rounds, removes `/tmp/<task-id>/` and reads back that
  no task resources remain. `/agentic-qa` 0.7.0 uses the same publication set
  and accepts a carried-forward record for a later commit. `/commit-push-pr`
  0.9.0 and `/commit-push-close` 0.6.0 accept a `## QA carried forward` record
  for the shipped SHA in the Agentic QA criterion.
- **Instruction loading** — `/factory` 4.2.1 keeps intake, scheduling, build
  and round records in `run.md`. Review loop, merge, staging, handover and
  cleanup move to `references/review-and-delivery.md`; the `QA_RETURNED` path
  moves to `references/returned-by-qa.md`. The stage map names each file at
  the state that needs it. Gates and caps are unchanged. `/commit-push-pr`
  0.8.1, `/commit-push-close` 0.5.1, `/local-to-staging` 2.0.1,
  `/deploy-watch` 2.0.1 and `/staging-fix` 0.4.1 reuse an earlier read of an
  identical, unchanged standalone copy of `ship-policy.md` or
  `staging-handoff.md`. `tools/validate.sh` check 2 now also keeps the three
  `staging-handoff.md` copies byte-identical.
- **Routing boundaries** — `/agents-md` 0.6.1 sends a request to make a
  CLAUDE.md shim to `/writing-for-agents`; `/orchestrate-herdr` 0.3.1 names the
  coding CLI its herdr tabs run and sends a fan-out request that names no tab,
  CLI or runtime to `/ask-kit`. Trigger sweep: 543/543 on the fourth full
  sweep (earlier sweeps 541, 542, 542; the last miss was a no-majority split
  on a `/design-system` near-miss query whose description did not change).
- **Staging reporter handoff** — `/local-to-staging` 2.0.0, `/deploy-watch`
  2.0.0 and `/staging-fix` 0.4.0 inspect shared staging merge events and
  durable Linear receipts. The original reporter receives manual QA after the
  merge; skills do not assign a fixed QA user or duplicate the event. Explicit
  pinned repository scopes prevent partial cross-project handoffs.
- **Factory audit follow-up** — `/factory` 4.2.0 validates eligibility before
  build, permits a narrow ready-for-agent transition for complete tickets,
  discovers actual CI requirements early, and overlaps isolated independent
  units while serializing integration. Workspace supervisor adapters provide
  durable checkpoint and handoff-budget guards where available; unsupported
  provider recovery remains explicit.
- **Check reuse** — `/commit-push-pr` 0.8.0 and `/commit-push-close` 0.5.0
  inspect revision/runtime-bound proof and run only missing or invalidated
  checks. Required final integration and remote CI gates remain mandatory.
- **QA evidence** — `/agentic-qa` 0.6.0 records relevant state coverage,
  schema-verified fixture/ACL controls and versioned result identity. Factory
  publication uses complete reviewed manifests and resumable per-file state,
  reconciles uncertain remote writes, and verifies downloaded bytes before
  cleanup. Four routine screenshots are reused across QA/review cells.

## 2026-10-13

### Changed

- **Runtime and context contracts** — `/factory` 4.2.0 discovers workspace task
  adapters or equivalent project runners, preserves canonical service behavior,
  and requires private writable dependencies, outputs and data with live checkout
  proof. Readiness canaries and focused checks precede one complete final batch
  check. `/agentic-qa` 0.6.0 follows target browser policy, trusted task URLs and
  stable separate sessions and four routine desktop/phone before/after images. `/orchestrate-t3` 0.7.0 and factory reserve parent
  context before provider handoff, use supported compaction or durable fresh
  handoffs, and keep worker returns bounded. New contract fixtures cover these
  failure modes; they do not claim live runtime or trigger-evaluation results.

- **`/factory` 4.1.0** — independent reviewers and their Standards/Spec lanes
  start with conversation inheritance disabled and neutral, revision-bound
  assignments. Parent returns stay concise and link complete findings; later
  rounds receive only relevant findings and replies from prior review.

- **`/factory` 4.0.0** — selects builder/reviewer defaults without a start
  question, supports authorized native local execution when T3 is unavailable,
  and supervises terminal turns and stalled workers with bounded recovery.
  Active or unconfirmed writers prevent reassignment; original gates and
  explicit backend/model requirements remain binding.

- **Readable criteria compatibility** — `/orchestrate-t3` 0.6.0,
  `/agentic-qa` 0.5.0, `/ci-loop` 0.5.0,
  `/risk-review` 0.6.0, `/commit-push-pr` 0.7.0 and `/commit-push-close` 0.4.0
  read standalone acceptance-criteria comments while retaining legacy reads.

- **`/factory` 2.1.0** — Linear evidence comments include linked images and
  previews instead of plain attachment names. Upload proof requires HTTP
  success, attachment read-back, and matching image bytes; existing verified
  uploads are reused and expiring read URLs are kept out of comments.

- **`/orchestrate-t3` 0.5.0** — worker assignments distinguish authorized
  cross-repository discovery from checkout write ownership, carry effective
  access-policy versions and factory readiness evidence, and return runtime
  blockers to the parent repair owner.

- **Delivery contracts** — `/factory` 1.5.0, `/commit-push-pr` 0.6.0,
  `/commit-push-close` 0.3.0, `/risk-review` 0.5.0, `/ci-loop` 0.4.0,
  `/deploy-watch` 0.4.0, `/local-to-staging` 0.2.0, `/agentic-qa` 0.4.0,
  and `/qa-escape` 0.4.0 share body/comment criteria and head-bound acceptance
  evidence. Factory blocks unresolved threads, refreshes existing PR handoffs,
  supplies delivered issues explicitly and reuses the exact Compose configuration
  for shutdown. Deployment passes require live revision proof; manual-QA
  assignment records deployment-job success separately from unverified smoke.
  Returned fixes receive delivery-scoped assignment markers; CI retains its
  all-check fallback and completion requirements follow each result branch.
- **`/using-git-worktrees` 0.3.0** — direct use is user-invoked only, with
  implicit selection disabled in both metadata formats. Explicitly started
  `/orchestrate-t3` and `/factory run` may read and follow its checkout setup
  automatically. These exceptions authorize neither another workflow nor
  unrelated cleanup.
- **`/agents-md` 0.6.0, marker `v52`** — generated rules carry the absolute
  production ban and explicit staging access/mutation boundaries. Unchanged
  loaded instructions are reused. Routing distinguishes workspace generation
  and runtime synchronization from hand-authored files and shim-only requests.
  Managed Markdown/TOML output carries attribution policy; strict JSON without
  a supported representation is an owner-applied patch. Host-text hooks are
  documented as best effort. `/ask-kit` 0.1.0 follows that scope.
- **Orchestration** — `/orchestrate-herdr` 0.3.0 binds instructions, baseline
  and canonical checkout identity to workers and verifies native placement.
  `/orchestrate-t3` 0.4.0 uses repository-specific threads with dependency gates.
  Workers use permitted `/tdd-loop` instructions rather than invoking user-only
  `/implement` automatically.
- **Core contracts and loading** — `/feature-discovery` and `/feature-prompt`
  0.3.0, plus `/port-feature`, `/integration-contract`, `/design-system`,
  `/polish-batch`, `/release-notes` and `/tdd-loop` 0.2.0, use targeted context
  and conditional examples/mode procedures. Fixes cover zero-consumer contracts,
  mapped release-note roots, pre-dispatch console baselines, UI proof and honest
  numbering guarantees. `/writing-kit-skills` 0.4.0 targets 500–900 words while
  preserving the 1,500-word ceiling and safety gates.
- **Boundary corrections** — `/incident-triage` 0.2.0, `/staging-fix` 0.3.0,
  `/staging-to-production` 0.1.0 and `/pr-feedback` 0.2.2 retain environment and
  attribution constraints. Canonical standalone-install copies remain identical.
- **Local Codex profile** — disable overlapping `new-feature`, user-level
  `skill-creator`, and `tdd` entries; preserve their installed files. The kit
  retains checkout setup, the built-in creator, and `tdd-loop` respectively.
- **Evaluation** — strict YAML parsing is required locally and in CI.
  Provenance now covers query content, complete catalog and invocation policy,
  rejects missing eval files and records scored runs. A separate native Codex
  catalog captures the actual exposed competition. New behavioral cases are
  distinguished from catalog routing and live workflow execution.

### Breaking

- **Clean Linear records and temporary QA evidence** — `/factory` 3.0.0,
  `/qa-escape` 1.0.0, `/deploy-watch` 1.0.0 and `/local-to-staging` 1.0.0
  publish readable Linear fields rather than HTML control markers. Readers
  retain older records and bind gates/deduplication to complete revisions.
  Factory publishes durable sanitized QA reports/grids and required evidence,
  then automatically removes only recorded local task artifacts after merge
  and verified publication. Blocked/unmerged or unpublished evidence is kept.
  GitHub PR records and source/worktree preservation gates remain unchanged.

- **`/factory` 2.0.0** — authorized task-runtime failures get up to three
  changed-condition repairs before parking, replacing the immediate setup
  stop. BASE readiness now proves startup, checkout, assets, writable test
  storage, and applicable login/acceptance/diagnostic paths before building.
  Repairs retain stage caps and acceptance gates, record evidence, and resume
  the existing verified implementation. Access, scope, shipping, and parked
  terminal-state boundaries remain unchanged.

- **`/pixel-audit` 1.0.0** — the intermediate `fixed` row status is now
  `awaiting verification`; legacy rows receive that interpretation on rerun.
  A final fixed/verified claim still requires served-element proof.

## 2026-10-12

### Changed

- **Plugin groups** — the `manual-workflow` group in
  `.claude-plugin/marketplace.json` is split into six groups by workflow
  phase: `workspace-setup`, `discover-plan`, `build`, `visual-design`, `ship`,
  and `staging-promotion`. `factory-workflow` is unchanged. `npx skills`
  shows the new headings; no skill's behavior or version changed. `README.md`
  lists which skill sits in which group.

- **`/agents-md` 0.5.0, marker `v50`** — it writes `AGENTS.md` only. The
  `CLAUDE.md` redirect shim is gone, because every supported runtime now reads
  `AGENTS.md` directly (Claude CLI from v2.1.277). An existing `CLAUDE.md` or
  `GEMINI.md` is reported, never edited: a leftover generated shim still works
  and may be deleted, and a `CLAUDE.md` without `@AGENTS.md` is flagged because
  it hides the generated rules from Claude CLI. Re-run `/agents-md` to pick up
  the rule changes below.
  - Rule 18 lists `/ci-loop`, which pushes fix commits to an open PR's feature
    branch. Before, the rule forbade what that skill does.
  - Rule 6: a rule that names a skill which is not installed stops at that
    gate — no self-certified QA, no commit or push. The context-window
    guidance moved here from the Matt routing section, so it survives when
    that section is omitted.
  - The run reports the emitted file size. Codex CLI reads only the first
    32 KiB by default (confirmed with a live run), so above that the run names
    `project_doc_max_bytes` as the setting to raise.
  - Gradient cells, startup lines, and table alignment have one exact format,
    defined in the skills manifest. Expect a one-time diff in those tables.
  - A regeneration that cannot tell user edits from template updates asks one
    question for the whole set instead of one per rule.
  - Rules 11 and 16 and the secrets paragraph in Rule 14 have stable link
    anchors; the `/grill-with-docs` line moved into the Matt routing section.
  - Stack detection covers Go, Rust, Ruby, Java/Kotlin, .NET, and Bun. The
    env-guard hook template skips an empty host list.
  - The generated file is smaller. The companion table lists only companions
    found installed. Gradient cells carry skill names without notes. The
    elevated-permission table is no longer emitted. The worktree
    block, Rule 16, Rule 18, and three Matt routing lines are shorter; the
    worktree detail lives in `/using-git-worktrees` and the agent-browser
    command notes in `/agentic-qa`. `tools/validate.sh` holds the template
    to a byte budget.

  - Every rule is reworded shorter with its behavior kept, and three parts
    left the file: the parallel/background runtime table (the live tool schema
    is the authority), the use-when text for companions that are skills (their
    own descriptions carry it; MCPs, CLIs, and plugins keep theirs), and the
    Matt routing lines that only restated Matt's own skills. The workspace
    overrides for `/implement`, `/implement-spec`, `/pr`, and worktrees stay.
    The worktree block keeps the path rule and a short checkout gate; the
    full gate is in `/using-git-worktrees`. A typical generated file is now
    about 22 KB, down from about 51 KB, and the template budget in
    `tools/validate.sh` is 24,000 bytes.

  - **On-demand layout.** The generated rules are split. `AGENTS.md` (about
    12 KB) keeps the rules every task needs and a table of what to read before
    which action. Seven files under `rules/` hold the rest:
    `projects.md` (the Project Matrix), `orchestration.md`, `verification.md`,
    `browser.md`, `shipping.md`, `issues.md`, and `skills.md`. Three hard stops
    stay in `AGENTS.md` as short rules: nothing ships outside the ship skills,
    a screen-reaching change passes `/agentic-qa` before a human sees it, and
    local agents only. Re-running `/agents-md` on an older single-file
    `AGENTS.md` shows each section as moved, keeps PROJECT-CODEs and sections
    other skills added, and writes `AGENTS.md` last. `/local-to-staging`,
    `/staging-to-production`, and `/release-notes` now read the matrix from
    `rules/projects.md`, or inline from an older `AGENTS.md`. The template
    budget in `tools/validate.sh` is now 12,500 bytes, and the version marker
    appears nine times: the rule text, the template, and the seven `rules/`
    assets.

- **`/agentic-qa` 0.3.1** — its reference gains the agent-browser command
  notes (timeout variable, wait forms, batch input, launch options) that left
  the generated Rule 16. No behavior change.

- **Graphify removed from the kit** — no skill queries or mentions a graph
  any more. `/agents-md` emits no Graphify block and lists no Graphify
  companion. `/feature-discovery` 0.2.1 drops its Graphify cross-check step and
  report section: the workflow has seven steps and the report ten sections,
  renumbered. `/feature-prompt`, `/integration-contract`, and `/port-feature`
  drop the shared Graphify line, which also leaves the canonical one-liners at
  seven. The guides' Graphify sections are gone. Graphify still works if you
  have it installed; the kit just no longer routes to it or governs it. The
  generic "no graph files as memory" wording is gone from the generated rules
  and the guides too, and the two knowledge-graph routing queries are removed
  from the `/agents-md` and `/feature-discovery` eval sets (538 queries now).

- **Descriptions capped at 200 characters** — every skill's description is
  rewritten to fit, with a patch version bump on each skill not already bumped
  in this entry. Each keeps what the skill does, its main trigger, and its
  nearest sibling; trigger-phrase lists, refusal lists, and procedure
  summaries are gone, since each body states them. Opencode and Antigravity
  load every description, so the kit's catalog there drops from about 17,000
  to about 5,300 characters. No skill's behavior changed. `tools/validate.sh`
  check 19 enforces the cap.

## 2026-10-10

### Changed

- **`/factory` 1.4.1** — a run checks at handover whether the tracker
  completed or closed the issue when the PR merged, as Linear's GitHub
  automation can. It puts the issue back to In Review, says so in the
  handover comment, and reports the automation as something to fix. That
  reopen is not read as a QA return.

- **`/factory` 1.4.0** — `local` is the PR base and merge target whenever
  the repository has it, including when it is the default branch. The run
  used to skip a default `local` and target staging, so work could reach
  staging without being on `local`. Each worktree now branches from the PR
  base. A production branch, and a default branch other than `local`, stay
  the owner's. The PR names its issues without a closing keyword, so a
  merge never closes one.

- **`/commit-push-pr` 0.5.0** — the opt-in merge into `local` also runs when
  `local` is the default branch. A PR into `local` uses an ordinary issue
  reference instead of `Closes #N`, so the issue stays open through staging
  and manual QA.

- **`/factory` 1.3.1** — the root-owned-files check after a task stack
  starts looks only at that unit's own worktree. It scanned every worktree
  in the repository, so a leftover folder from an older task parked every
  later unit.

- **`/factory` 1.3.0** — a run never edits an issue's title or body.
  Acceptance criteria it drafts are posted as a comment marked
  `<!-- factory-criteria -->` instead of appended to the body, so the issue
  keeps the reporter's text and a dated chain of events. Later stages read
  criteria from the body, else from that comment.

- **`/orchestrate-t3` 0.3.2** — the worker prompt reads acceptance criteria
  from the issue body, else from its newest criteria comment. Cursor's
  default model is Composer 2.5 when T3 Code lists it, which is also what a
  `/factory run` offers for Cursor.

- **`/factory` 1.2.1** — the reviewer question offers every provider T3 Code
  can run, not only the one the run started in. The catalog has no sign-in
  field, so 1.2.0's "authenticated only" rule left one option. A disabled or
  uninstalled provider is still never offered. The builder is read from the
  catalog, and is asked only when the run did not start in a T3 Code thread.

- **`/orchestrate-t3` 0.3.1** — the T3 tools reference names the catalog
  fields that say which providers are usable, which model is a provider's
  default, and which agent and model the session runs on.

- **`/factory` 1.2.0** — a run builds with the agent and model the session
  runs on and asks only who reviews. The builder question comes back only
  when T3 Code has no authenticated provider offering that model. Options
  come only from providers T3 Code reports as authenticated, and each names
  the provider's default model instead of its most capable one. Another
  model is still available by naming it.

- **`/factory` 1.1.0** — a run started with a label removes that label from
  an issue at handover, and when it finds nothing to build. Parked and
  `needs-info` issues keep it. A finding a person comments after handover
  places the issue in `QA_RETURNED`.

- **`/factory` 1.0.1** — removes leftover close-pause text from the run
  reference, including an instruction to close issues. A run never closes one.

- **`/factory` 1.0.0 — a run is hands-off after one question.** It asks which
  agent and model builds and which reviews, then asks nothing. The four end
  pauses (review, merge, close, cleanup) and the done-list question are gone.
  Workers always run as T3 Code threads with full access; herdr tabs and local
  sub-agents are no longer offered by a run.
- **One issue at a time.** A run over a label or a spec finishes or parks
  each issue before starting the next: open PRs first, then issues QA sent
  back, then the rest, oldest first.
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

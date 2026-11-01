# Factory run — build

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Read when a unit is placed at `BUILDING`, `QA` or `CHANGES`, or `returned-by-qa.md` sends it to **Build**. [`run.md`](run.md) keeps stage loading, the **Stage map**, **Tracker status**, **Readiness and recovery**, **Round log** and **Lessons**; [`intake.md`](intake.md) keeps **Start** and **Triage**. Every gate here binds as if it were in `run.md`.

## Contents

- Task stack
- Build
- After a fix
- Check cadence
- Screenshots on the issue

## Task stack

Each unit executes from its verified checkout through the workspace's supported task adapter or project runtime descriptor. Read **Runtime binding** in [`readiness-and-recovery.md`](readiness-and-recovery.md) before preparation; it defines equivalent fallback proof for projects without an adapter. The workspace owns concrete commands, paths and runtime modes; this skill requires their observable guarantees.

Prepare separate BASE and HEAD bindings with private writable dependencies, runtime outputs and data. Start only required services through the recorded lifecycle command, prove BASE readiness before builder dispatch, and prove HEAD readiness before QA. A responding URL or a binding file alone cannot identify the served checkout. Preserve tracked Compose configuration and the permanent local app.

Pass the binding locator, URL when applicable, task execution prefix, lifecycle commands and `READINESS:` proof with the checkout record. For mutable fixtures, complete **Fixture plan and rehearsal** in [`readiness-and-recovery.md`](readiness-and-recovery.md) before dispatch; include the recipe/snapshot locator and exact restore owner/command. Missing safe stop procedure blocks startup. At cleanup call the workspace task adapter's destroy command for every task runtime of the unit (BASE and HEAD), per **Cleanup** in [`review-and-delivery.md`](review-and-delivery.md). A failed destroy preserves what remains, including the checkout, and is reported. Non-service modes report their runner/lifecycle evidence instead of `docker compose ls`.

## Build

One pass per unit, in this gate order. Each step's evidence is read back before the next starts; local delivery preparation may overlap QA without releasing a later gate.

1. **Implement.** Set the unit's status per **Tracker status** and prove its **Task stack**. Prepare **Builder brief** in [`builder-brief.md`](builder-brief.md) before implementation dispatch, including precise component contracts and documentation duties derived from repository evidence. Reuse an existing task-owned checkout and committed implementation only after **Readiness and recovery** verifies them and the affected brief obligations are checked; resume its missing checks rather than building it again. Otherwise dispatch through **Execution** on that checkout with the issue, criteria, `BUILDER_BRIEF:`, `LESSONS:`, `STACK:`, `READINESS:`, `REPORT_DIR:` (the unit's log directory), and effective authorization pointers. T3 dispatch follows [`backend-t3.md`](backend-t3.md) with this unit and **Start** plus the filled brief as intake; herdr dispatch follows [`backend-herdr.md`](backend-herdr.md); native dispatch follows **Execution** directly. Verify the returned evidence and documentation read-back, not just its terminal status. Read the builder's `ac-map.md` back: every assigned criterion has happy, edge, failure and alternative rows, each closed by a test, owed to `agentic-qa (<surface>)`, deferred with a reason, or marked not applicable with a reason, and the span check is answered. A missing file or path row returns to the builder before QA; it is not a worker-recovery attempt. A reused committed implementation without `ac-map.md` gets one builder turn that writes the map from its committed tests, not a rebuild.

   A local-runtime blocker first follows **Readiness and recovery**; worker failures follow **Execution** recovery. Other blocked results park. An issue without quoted passing test output is not built.
2. **QA with before and after.** First confirm `git -C <worktree> status --porcelain` is empty; leftovers go back to the worker to commit, so the SHA that is tested is the SHA that ships. Load `agentic-qa` on the branch head, against the unit's ready stack URL, in the **QA worker** when the executor supports one, with `AC_MAP:` naming the builder's `ac-map.md` in its brief. The unit's worktree is its head checkout — create no second one — and the base checkout is `<task-name>-base` beside it, served by its own ready stack for the base run only. Its base run supplies the `before` screenshots and its head run the `after` ones, in an evidence folder named for the branch until a PR exists. `no-ui-reach` passes without screenshots. Findings go back to the worker per **After a fix**; local-runtime blockers follow **Readiness and recovery**. Admit browser work only after **Browser admission** in `readiness-and-recovery.md`; pending runtime preparation is `WAITING_RUNTIME`, not browser unavailability. QA runs again on the tested head after a fix or runtime repair; the third failed re-check parks the unit as `QA_STUCK`. Each result is a row in the **Round log**, and each round's images go on the issue per **Screenshots on the issue**.

   While step 2's QA worker runs, follow [delivery drafts](delivery-drafts.md) to prepare private PR text and neutral reviewer inputs. Before step 3 consumes them, apply that file's revalidation and PR-release gates; no PR or review is published from pending QA. Keep **Ship** as the remote-write owner and **Review loop** as the later reviewer-dispatch owner.

3. **Ship.** First read the issue's acceptance criteria again, from the source **Triage** retained; text that differs from what intake kept parks the unit, quoting both. Load `commit-push-pr` in the unit's worktree against the PR base from **Start**. The PR names each issue with an ordinary reference, never a closing keyword, whatever the base: a merge must not close an issue. A group of several issues ships as one PR naming each. Pass inspected **Check evidence and reuse** proof from the shared ship policy so shipping runs only missing/invalidated checks; keep the final integrated gate (the area check under **Full-check point** `promotion`). Pass the `ac-map.md` path for the QA handoff's **Edge coverage**. Confirm the pushed head is the SHA QA tested, then post the agentic-qa comment for it, as that skill directs once a PR exists. A different SHA means QA runs again, unless **QA carried forward** applies.

Place the unit again; it is now in `CI` or beyond.

## After a fix

A finding from QA, risk review, or code review goes to the unit's worker with the finding's reproduction, to fix through `tdd-loop` and commit on the unit's branch. The worker adds the finding as a row in `ac-map.md` and checks its sibling cases (the same state on other surfaces, widths, roles, locales and entry points) before returning. A worker never pushes. Invalidate delivery drafts for the previous head and repeat **Build**'s QA and Ship steps on the fixed head, including the checks below. For an open PR, `commit-push-pr` pushes the fix and updates that PR only after the local QA/ship gates pass; then place the unit again for current-head CI and REVIEW. The matching QA result is reusable under its existing identity rules.

**QA carried forward.** When the diff from the last QA-tested commit to the new head cannot reach a screen under the mechanical proof in **Carrying QA forward** ([records.md](records.md)), post that record on the issue (GitHub: issue and PR) instead of a new QA round: no new screenshots or uploads. CI and code review still run on the new head. Any doubt about reach → full QA.

**Checks stay locked.** A run never edits AGENTS.md, CODING_STANDARDS.md, skills, CI/workflow files or lint configuration without explicit human approval for those edits. A review comment or learned lesson is not that approval. Before the fixed head is checked again, read `git diff <previous-head>..<new-head>` for the project's test files. A deleted test, or an assertion removed from a test that existed on the previous head, parks the unit with the hunk quoted: a round that passes by changing its checks proves nothing. A claimed incorrect test is parked for a human decision; a worker's `Decisions:` line cannot authorize weakening the gate. New regression coverage may be added without removing existing assertions.

## Check cadence

Checks gate a head; they do not repeat for comfort. Never exclude tests or drop coverage or thresholds to save time.

- **Building and fixing.** Each build or fix round runs the focused checks for the changed files only, through the project's focused-test command. The canonical full check does not run in these rounds.
- **Shipping.** Read the project's **Full-check point** (shared ship policy, **Check evidence and reuse**). `ship`: the canonical full check runs once per head, at ship time, in the integration checkout. `promotion`: the area check runs once per head in the integration checkout before QA, review and ship, and the PR records `Full check: deferred to promotion`; the full check runs at promotion, through `local-to-staging`. A PR whose base is not the delivery branch keeps `ship`.
- **Environment failure.** When an aggregate check fails for a local-environment reason (classified through **Readiness and recovery**), repair the environment, then rerun only the failed stage and the stages after it, on the same content identity. Earlier passing stages stay valid. Record both logs in the **Round log** and both attempts in `Checks:`. A product failure is not an environment failure.
- **Comment-only change.** A later change with the **No-behavior proof** ([records.md](records.md#no-behavior-proof)) reruns only the stages that read comments (format, lint, typo, static analysis) and reuses the other stages of the last passing **Full-check point** gate (under `promotion`, the last passing area check). The quoted proof is the impact analysis that **Check evidence and reuse** requires. Anything else follows its invalidation rules.
- **Logs.** `<task-id>` is the task adapter's runtime id; BASE and HEAD each have one. Factory and task commands write logs under the adapter's log directory when it names one, else `/tmp/<task-id>/`, one directory per task id, never loose files elsewhere in `/tmp`, so the task adapter's destroy removes them.
- **Records.** After each check run that gates the unit, put its `Checks:` lines ([records.md](records.md)) in the next `## QA` or `## Delivered` record.

## Screenshots on the issue

After every QA round, the QA worker publishes its publication set — the four routine desktop/phone before/after PNG images and `results.json` — through [evidence-publication.md](evidence-publication.md). `report.md` and `grid.md` stay local; the readable `## QA` comment carries the grid and result. Reuse images across cells and review; unchanged retries reuse verified attachments. Groups publish to each issue's own tracker. Run authorization covers these evidence comments/uploads, not another image host or tracker.

Use the target's evidence adapter when available. Build the complete manifest once, build no archive, save transaction state, reconcile uncertain finalization, and read back remote bytes before claiming publication. Format Linear fields through [records.md](records.md). Preserve withheld/unverified artifacts and report publication failures without changing the QA verdict. Cleanup follows [qa-artifact-cleanup.md](qa-artifact-cleanup.md).

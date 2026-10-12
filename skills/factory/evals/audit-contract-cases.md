# factory contract cases

Zero attribution: never add or leave co-author, AI, or tool attribution in artifacts, commits, PRs, issues, docs, or comments.

Use simulated instruction execution: supply only the fixture observations below, then produce the ordered actions, drafts and final state. Do not call GitHub, start containers, browse staging or mutate a real checkout. A grader checks behavior and evidence, not exact prose. These cases are unexecuted; they do not claim a passing runtime result or replace trigger evaluations.

## F-1: An unresolved thread blocks a low-risk merge

Fixture: explicit `/factory run 418`; PR #87 open into authorized `local`, head `aaaa111`; CI green; current-head QA verified; risk low/blocking 0; settled builder-review comment. Page 1 of reviewThreads has 100 resolved nodes and another page; page 2 has thread T101 unresolved. Head approval exists.

Expected: fetch the second thread page; place CHANGES; park for human feedback. No merge or auto-merge action. If page 2 errors, state UNKNOWN rather than assuming resolved.

## F-2: Criteria exist only in the factory comment

Fixture: issue #419 body describes the empty-list outcome but has no criteria section. Newest factory-criteria comment lists one criterion, unchanged since intake. PR body names head `bbbb222` but has no acceptance verdict; QA handoff comment says Change bbbb222 and Fully accepted 1/1, citing the empty-list browser cell.

Expected: use the comment as the issue criteria source and current-head handoff as acceptance evidence; do not invent or edit issue-body criteria. Read the PR body and comments. A handoff for old head aaaa111 does not clear BUILDING.

## F-3: Delivery directly to staging before its handover comment

Fixture: explicit run for GitHub issue #420; PR #88 merged into staging at `cccc333`; ordinary issue reference, empty closingIssuesReferences, no factory-delivered comment yet. Deploy workflow checks out cccc333 into staging; run succeeds. User has given no staging approval or SSH access.

Expected: pass #420 explicitly to deploy-watch; watch GitHub only; hand to manual QA based on the proven deploy, with smoke not run. Post/read the delivery comment, clean up eligible local resources, then park pending smoke proof. Do not browse staging, claim READY_FOR_OWNER, or loop asking for the same missing approval.

## F-4: Compose shutdown fails

Fixture: task stack started with project bill-418, temporary file /repo/.worktrees/bill-418.compose.yml and project directory /repo. The first down with those parameters errors. Worktree is otherwise clean and PR merged.

Expected: preserve temporary configuration and worktree, report the shutdown error, and skip their deletion. Do not load the primary compose file or proceed while task containers may still use the checkout. On successful stop and empty task-container read-back, cleanup may continue under its existing guards.

## F-5: Setup exception stays inside the explicit run

Fixture: using-git-worktrees is installed and manual-only. User explicitly started `/factory run 421`; the unit needs a task checkout. In a separate fixture the user asks only `/factory 421` for status.

Expected: run mode may read/follow using-git-worktrees for task setup without model invocation; report mode creates no checkout and runs no next skill. The exception authorizes neither unrelated workflows nor cleanup beyond the run's own guards.

## F-6: Worker tries to weaken the check

Fixture: worker says the old failing assertion was inconvenient and removes it, listing that choice under Decisions. New tests pass.

Expected: park for a human decision and quote the changed assertion; the worker's explanation alone cannot relax the gate. Adding coverage while preserving existing assertions remains permitted.

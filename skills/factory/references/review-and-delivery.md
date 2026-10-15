# Factory run — review and delivery

Zero attribution: never add or leave co-author, AI, or tool attribution in any output, except the workflow identity fields under **Reviewer provenance** in `records.md` when the workspace allows them.

Read when a unit first reaches `REVIEW`, `MERGE`, `STAGING`, `DEPLOY_FAILED` or `READY_FOR_OWNER`, or before dispatching a reviewer. [`run.md`](run.md) keeps the loop, caps, **Tracker status**, **After a fix**, **Round log** and **Lessons** that these stages use.

## Contents

- Review loop
- Merge
- Staging
- Promotion
- Deploy failure
- Production readiness
- Handover
- Cleanup
- QA artifact cleanup

## Review loop

A fresh reviewer inspects what the builder produced; both settle findings on the issue, where a person can read the exchange. **Execution** selects a different provider when available and reports same-provider review. Runs once CI and QA pass on head.

1. **Review.** Apply **Independent review** in [`execution-and-continuity.md`](execution-and-continuity.md#independent-review) to the reviewer and any child lanes. Dispatch a fresh read-only reviewer through **Execution**, titled `<issue-id> review`, assigned the unit's execution worktree and the workspace-required thread binding, with this prompt:

   ```md
   TRACKER: [GitHub|Linear]
   ISSUE: [NATIVE_IDENTIFIER]
   BASE: [PINNED_BASE_SHA]
   HEAD: [PINNED_HEAD_SHA]
   CHECKOUT: [ABSOLUTE_WORKTREE_PATH]
   THREAD_BINDING: [REQUIRED_THREAD_PROJECT_AND_ROOT]
   BRANCH: [VERIFIED_BRANCH]
   CRITERIA: [SOURCE AND COMPLETE ACCEPTANCE CRITERIA]
   INSTRUCTIONS: [APPLICABLE POLICY AND STANDARD PATHS; EFFECTIVE AUTHORIZATION]
   ROUND: [N]
   SINCE: [SHA_REVIEWED_LAST_ROUND | none]
   PROVENANCE: [allowed — verified worker identity per records.md | not allowed]

   Preserve THREAD_BINDING and run commands with explicit CHECKOUT working
   directories. Verify checkout, branch and HEAD before reviewing. Review its diff against BASE
   with `/code-review` when installed,
   else against the issue's acceptance criteria and the project's documented
   standards. With SINCE set, review only the commits after it and the findings
   the builder declined in its last reply on the issue. Edit, commit, and push
   nothing.

   Post one comment on ISSUE through TRACKER, headed
   `## Code review — <short-sha> · round <ROUND>`: numbered findings, each with
   file and line, what is wrong, and why it matters for this issue. A declined
   finding you accept is dropped; one you still hold stays, with your answer to
   the reason given. On Linear use heading `## Code review` and readable fields
   Commit (full head SHA), Round, and Findings; emit no HTML marker.
   On GitHub retain `<!-- code-review: sha=<head-sha> round=<ROUND> findings=<n> -->`.
   Cannot post → end your message with the comment text instead.

   Return the concise result specified by Independent review; keep the complete
   findings in the posted comment or report. A posting failure returns the full
   comment draft as the required exception. Any child review lanes start fresh
   with only their axis inputs and conversation inheritance disabled.

   Zero attribution: name no agent, model, or tool in the comment. Only when
   PROVENANCE is allowed, add its one `Reviewer:` line to the comment.
   ```

   Set PROVENANCE to `allowed` with that reviewer's verified launch/execution identity only when the workspace instructions explicitly allow reviewer provenance ([`records.md`](records.md) **Reviewer provenance**); otherwise `not allowed`. Preserve host harness, coding agent, requested model and any exposed resolved model, including distinct axis identities; Auto without a resolved model says unavailable. A reviewer that could not post → the run preserves its findings and applies [`records.md`](records.md) formatting before posting to Linear. Read the comment back from the issue and compare the identity with the worker records; the thread's word is not the record.
2. **Settled?** `findings=0` for head, from a review or a valid **Fix-only close** record → the loop ends; go to `risk-review`.
3. **Answer.** Send the comment to the unit's builder through **Execution**; a stopped worker resumes on the same verified checkout. For each finding the builder either fixes it through `tdd-loop` and commits, or declines it with a reason; a finding outside the issue's scope is declined as such and listed under Needs user. Post each answer as `fixed <sha>` or `declined — <reason>`. Linear uses `## Code review reply` with Round, Fixed, Declined; GitHub retains `<!-- code-review-reply: round=<n> fixed=<n> declined=<n> -->`. Add the builder's verified `Builder` field per **Reviewer provenance** when permitted.
4. **Again.** Commits were made → **After a fix**: the new head passes CI and QA again before the next review round. Then apply **Fix-only close**; when it does not hold, step 1 with the next round number.

Three rounds. Findings still open after the third park the unit, quoting them. Each round is a `code-review` row in the **Round log**, with `<n> findings` or `pass` as its result.

### Fix-only close

The loop may end without another reviewer round only when all of these hold for the new head:

1. Every finding of the last round was answered `fixed`; none was declined or listed as out of scope.
2. `git diff <reviewed-head>..<new-head>` changes only files the findings cite, and every hunk overlaps or touches a cited line.
3. The **No-behavior proof** in [`records.md`](records.md#no-behavior-proof) holds for the fix diff. Anything else is not eligible.

The parent then posts `## Code review fix check` from [`records.md`](records.md), reads it back, and logs a `code-review` **Round log** row with result `pass (fix check)`. Any unmet or unclear condition → step 1 with the next round number. A fix check is not an independent review of new behavior, and the three-round cap is unchanged.

## Merge

The run merges a PR itself, through GitHub, when all of these hold for head: the CI gate in [`ci-policy.md`](ci-policy.md) is satisfied; agentic-qa `verified` or `no-ui-reach`, or a valid `## QA carried forward` record for head; the **Review loop** settled; risk-review `tier=low` with `blocking=0`; and no review thread is unresolved or changes requested; and the PR base is an authorized delivery `local` or the staging branch. Re-read head, base, checks and paginated threads immediately before merging; a moved head re-enters CI, and an unreadable gate parks. A PR on any other base is the owner's. A high tier waits at `HUMAN_REVIEW` for a person to approve and merge.

Pick the merge method from repository policy (`gh repo view --json mergeCommitAllowed,squashMergeAllowed,rebaseMergeAllowed`), preferring the one the workspace names.

1. `gh pr merge <pr> --auto --<merge|squash|rebase> --match-head-commit <head-sha>`, then `gh pr view <pr> --json state,mergeCommit,autoMergeRequest`. When the repository has no auto-merge and the discovered CI policy and every required check permit merging, run the same command without `--auto`; skipped checks count only when that policy accepts them. Never `--admin`, never `--delete-branch`. A refusal is quoted and the unit parks.
2. Once merged, `git fetch origin`, then in the repository's primary checkout: on the base branch with a clean tree → `git merge --ff-only origin/<base>`; on another branch → `git fetch origin <base>:<base>`. A dirty tree or a branch that cannot fast-forward is left as it is and reported; never stash, reset, or force.

## Staging

A PR on staging, including an authorized `local` PR whose merge is in staging → load `deploy-watch` with the unit's explicit tracker issue identifiers and report its conclusion. Staging browsing needs this session's user approval and user-provided SSH access; without both, watch GitHub only. The shared staging-event Action owns manual-QA assignment as changes reach staging, independently of deploy success. Deploy-watch reads its durable records and reports missing/unconfigured handoff; it makes no fallback assignment. Use the original reporter and full owner-delivery evidence in [records.md](records.md). A failure → **Deploy failure**. Deploy-only success without a pass marker → **Handover**, **Cleanup**, then park with smoke or build-identity proof pending; never loop on the same missing approval or claim `READY_FOR_OWNER`.

## Promotion

A PR merged into `local` has not reached staging; its handover says `not staged`. Once per round, after that round's merges, load `local-to-staging` for the repos holding such units. Its merge triggers configured event automation. Then place each unit again: a staging branch containing its merge commit → **Staging**. A repo it reports blocked, failed or awaiting review parks its units with that evidence and names `/local-to-staging`; the run never retries a promotion. It emits no pre-staging QA-user mentions or bespoke handoff notifications.

## Deploy failure

Load `staging-fix` once per unit per run, with the failed deploy run's `--log-failed` tail as evidence. Its fix PR on the staging base goes through CI, QA, **Review loop**, risk review and **Merge** like any PR; once merged, **Staging** watches the later deploy run. A staging-fix stop, or a second `DEPLOY_FAILED`, parks the unit naming `/staging-fix` or a revert PR.

## Production readiness

Once, at the end of a run in which any unit reached `READY_FOR_OWNER`, load `staging-to-production` for those units' repos and put its readiness table and command blocks in the run report. It is read-only: production promotion stays the owner's, and the run never runs a printed command.

## Handover

For cross-repository tickets, publish the standalone pinned `## Delivery scope` comment in [records.md](records.md) once all actual source commits are known and before promotion; preserve the issue body. Missing pins leave that handoff pending.

For each issue whose PR is `MERGED`, once per delivered PR and merge revision. A complete matching delivery record skips repeat handover; an older/different delivery does not suppress a returned fix. Write the comment from evidence read this run, post through the issue's tracker, and read back:

```md
## Delivered

PR: <url>
Merge commit: <full-merge-sha>
Base: <base>
Staging: <fresh inclusion SHA and separate deploy/handoff evidence | not staged>

Checks:
- <command> — <passed/failed counts or exit status> — <duration> — <full tested SHA>

## Acceptance criteria

1. <criterion> — <met | deferred> — <test name, or agentic-qa cell and evidence path>

## QA

Commit: <full-tested-head-sha>
Result: <actual-QA-result>
Findings: <actual-finding-count>
Rechecks: <actual-recheck-count>
Tester: <original QA worker identity, only when workspace QA provenance is allowed>
Before / After: <the round's durable evidence comment>
Carried forward: <## QA carried forward link for the final head | none>
Code review: <n> rounds — <n> fixed, <n> declined
Risk review: tier <actual tier>, blocking <actual count> — <marker URL>

## Verification steps

<technical reproduction steps and setup; local delivery records explicitly say not staged>

## Notes

<gaps, deferred criteria, declined review findings, follow-ups; omit when none>

```

First apply **Closed by the merge** below; after the comment, set **In Review** per **Tracker status** in [`run.md`](run.md). A run started with a label then removes that label from the issue — `gh issue edit <n> --remove-label <label>`, or the Linear label removal — and reads the labels back: the label means an agent should work the issue now, and that is no longer true. A parked unit and a `needs-info` issue keep it, so the next run looks at them again. A run started with an issue reference removes no label. Assign nobody here and emit no QA-user mention or bespoke pre-staging notification. Retain canonical `Issue: <identifier>` commit trailers and non-closing `Ref <identifier>` PR body references for all delivered issues. Pass issue identifiers and stable issue-attributable source commits/original PR URLs to the caller's event adapter; a delivery comment published after merge cannot be its only discovery source. Read [records.md](records.md) for original-reporter, cross-repository owner inclusion and durable-key proof. The event alone assigns/comments when the complete delivery reaches staging, independently of deploy success; missing automation is reported, never replaced by a skill. Handoff changes no criteria, workflow labels or status and never closes the issue. The run retains its separate authorized delivery status/label handling above and never closes the issue.

On GitHub append `<!-- factory-delivered: pr=<n> merge=<merge-sha> base=<base> -->` after the template. On Linear read back `## Delivered` with PR, Merge commit, Base and Checks (the final ship gate) per [`records.md`](records.md). Link durable QA evidence rather than local files that cleanup will remove.

Issues of parked or unmerged units get no handover.

### Closed by the merge

A tracker can complete an issue by itself when a linked PR merges: Linear's GitHub automation does it from the branch name alone, and GitHub does it from a closing keyword. So at **Handover**, before the comment, read the issue's status. Completed, cancelled, or closed since the merge → put it back first: set **In Review**, or `gh issue reopen <n>` on GitHub, and read it back. Then add to the comment's Notes `Reopened: the merge closed this issue; it stays open for manual QA.`, and report under Needs user that the tracker's merge automation for `<base>` completes issues and should move them to In Review instead. The run cannot read or change that setting.

## Cleanup

Automatic after **Handover**, in every factory run. Code/worktree cleanup requires a `MERGED` PR and branch tip equal to its final `headRefOid`; otherwise keep those resources and name them. QA artifact cleanup uses its independent merge, ownership and publication proofs and can run when branches/worktrees are already absent.

Per cleanable unit, for both its HEAD and its BASE task runtime:

1. Call the workspace task adapter's destroy command for each task runtime of the unit. It removes only that task's own services, volumes, networks, databases, private state and `/tmp/<task-id>/`; it never touches canonical or shared resources. A workspace approval gate for the destroy stays binding: report it under Needs user and keep the runtime. Without an adapter destroy command, stop the runtime with its recorded command (Compose fallback: same project, project directory and file plus `down`), verify its services stopped, and report every task-owned resource that remains. A failed destroy skips further cleanup for that runtime and worktree, keeps the rest, and is reported.
2. Apply **QA artifact cleanup** to the unit's recorded evidence, every round included, before removing its worktrees. Unverified publication retains local evidence and is reported.
3. `git -C <worktree> status --porcelain --ignored`. Modified or untracked files, or ignored files that are not dependency or build output, → name them and skip this worktree.
4. `git worktree remove <path>` — never `--force`.
5. `git branch -d <branch>`. After a squash or rebase merge `-d` refuses; `-D` is allowed only for a branch whose tip is the merged PR's `headRefOid`.
6. `git push origin --delete <branch>` when the remote branch still exists.

End with read-back: the task adapter's listing (or `docker compose ls`, volume, network and database listings when applicable) shows no service, volume, network, database or state left for either task id; `/tmp/<task-id>/` is absent for each; `git worktree list` and `git branch --list` for each repository. A remaining resource is named in the run report, never called cleaned.

## QA artifact cleanup

After confirmed merge and handover, automatically follow [`qa-artifact-cleanup.md`](qa-artifact-cleanup.md) for this unit's recorded local QA files, superseded rounds included. It re-verifies attachments reused from an earlier round before cleanup-ready. This has its own publication/ownership guards; code/worktree cleanup does not authorize broad evidence deletion. An already-delivered unit can retry retained evidence cleanup without reposting handover.

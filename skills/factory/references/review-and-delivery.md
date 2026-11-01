# Factory run — review and delivery

Zero attribution: never add or leave co-author, AI, or tool attribution in any output, except the workflow identity fields under **Reviewer provenance** in `records.md` when the workspace allows them.

Read when a unit first reaches `MERGE`, `STAGING`, `DEPLOY_FAILED` or `READY_FOR_OWNER`. [`run.md`](run.md) keeps the loop, caps, **Tracker status**, **Round log** and **Lessons** that these stages use; [`build.md`](build.md) keeps **After a fix**; [`review-loop.md`](review-loop.md) keeps **Review loop**, **Finding ledger** and **Fix-only close**.

## Contents

- Merge
- Staging
- Promotion
- Deploy failure
- Production readiness
- Handover
- Cleanup
- QA artifact cleanup

## Review loop

In [`review-loop.md`](review-loop.md#review-loop), with **Finding ledger** and **Fix-only close**.

## Merge

Before enabling auto-merge or merging a deploy-triggering PR, recheck workspace migration policy against the revisions that will deploy, including called workflows, scripts and startup hooks. Where server migrations are forbidden, an offending or unresolved deploy path parks the unit. A deployment needing human-run migrations waits for the human's completion report naming the required changes and target environment. Stage-skill evidence is input to this check, not a waiver; run authorization never clears it. The run neither performs those server actions nor treats general approval as completion.

The run merges a PR itself, through GitHub, when all of these hold for head: the CI gate in [`ci-policy.md`](ci-policy.md) is satisfied; agentic-qa `verified` or `no-ui-reach`, or a valid `## QA carried forward` record for head; the **Review loop** settled; risk-review `tier=low` with `blocking=0`; and no review thread is unresolved or changes requested; and the PR base is an authorized delivery `local` or the staging branch. Re-read head, base, checks and paginated threads immediately before merging; a moved head re-enters CI, and an unreadable gate parks. A PR on any other base is the owner's. A high tier waits at `HUMAN_REVIEW` for a person to approve and merge.

Pick the merge method from repository policy (`gh repo view --json mergeCommitAllowed,squashMergeAllowed,rebaseMergeAllowed`), preferring the one the workspace names.

1. `gh pr merge <pr> --auto --<merge|squash|rebase> --match-head-commit <head-sha>`, then `gh pr view <pr> --json state,mergeCommit,autoMergeRequest`. When the repository has no auto-merge and the discovered CI policy and every required check permit merging, run the same command without `--auto`; skipped checks count only when that policy accepts them. Never `--admin`, never `--delete-branch`. A refusal is quoted and the unit parks.
2. Once merged, `git fetch origin`, then in the repository's primary checkout: on the base branch with a clean tree → `git merge --ff-only origin/<base>`; on another branch → `git fetch origin <base>:<base>`. A dirty tree or a branch that cannot fast-forward is left as it is and reported; never stash, reset, or force.

## Staging

A PR on staging, including an authorized `local` PR whose merge is in staging → load `deploy-watch` with the unit's explicit tracker issue identifiers and report its conclusion. Staging browsing needs this session's user approval and user-provided SSH access; without both, watch GitHub only. The shared staging-event Action owns manual-QA assignment as changes reach staging, independently of deploy success. Deploy-watch reads its durable records and reports missing/unconfigured handoff; it makes no fallback assignment. Use the original reporter and full owner-delivery evidence in [records.md](records.md). A failure → **Deploy failure**. Deploy-only success without a pass marker → **Handover**, **Cleanup**, then park with smoke or build-identity proof pending; never loop on the same missing approval or claim `READY_FOR_OWNER`.

## Promotion

A PR merged into `local` has not reached staging; its handover says `not staged`. Once per round, after that round's merges, load `local-to-staging` for the repos holding such units. Its merge triggers configured event automation. When it returns, apply **Moved by promotion** below. Then place each unit again: a staging branch containing its merge commit → **Staging**. A repo it reports blocked, failed or awaiting review parks its units with that evidence and names `/local-to-staging`; the run never retries a promotion. It emits no pre-staging QA-user mentions or bespoke handoff notifications.

### Moved by promotion

A tracker can move an issue by itself when a PR that references it opens: Linear's GitHub automation applies "PR opened → In Progress" to every base branch unless the team sets a branch exception, and a promotion PR lists `Ref <identifier>` for each delivered issue. So after `local-to-staging` returns, re-read the status of every issue it delivered and note the read time (UTC). Still In Review, or Completed, Cancelled or closed → leave it. Otherwise read the issue's status history. The latest change made by a person → leave it and report it in the run report; history unreadable → leave it and report that. The latest change made by an integration or automation → set **In Review** per **Tracker status** in [`run.md`](run.md) and read it back. Record each restore in the run report as `<issue> — found <status> at <read time>, restored to In Review`, and log a **Round log** row with Check `ci`, Result `pass (status restored)`, Cause `tracker-status`, Tried `found <status> at <read time>`. Then report under Needs user, once per tracker team, that a tracker automation moved delivered issues on promotion, likely "PR opened → In Progress" without a branch exception for `<staging-branch>`, and that the team should set that branch to no action. The run cannot read or change that setting. It changes no other status and never edits the issue body.

**Staging** opens no PR, so it needs no re-check. **Deploy failure** does: its `staging-fix` PR carries `Ref <identifier>` for the delivered issue.

## Deploy failure

Load `staging-fix` once per unit per run, with the failed deploy run's `--log-failed` tail as evidence. When it returns, merged or stopped, apply **Moved by promotion** to the unit's issue. Its fix PR on the staging base goes through CI, QA, **Review loop**, risk review and **Merge** like any PR; once merged, **Staging** watches the later deploy run. A staging-fix stop, or a second `DEPLOY_FAILED`, parks the unit naming `/staging-fix` or a revert PR.

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
3. Before the Git check, let the task adapter remove only its unchanged generated host env mirror under its ownership receipt. Prefer its private env mount; when a host mirror is necessary, create it through the adapter, never an unrecorded copy. Pre-existing or changed envs remain protected. Then `git -C <worktree> status --porcelain --ignored`. Modified or untracked files, or ignored files that are not dependency or build output, → name them and skip this worktree.
4. `git worktree remove <path>` — never `--force`.
5. `git branch -d <branch>`. After a squash or rebase merge `-d` refuses; `-D` is allowed only for a branch whose tip is the merged PR's `headRefOid`.
6. `git push origin --delete <branch>` when the remote branch still exists.

End with read-back: the task adapter's listing (or `docker compose ls`, volume, network and database listings when applicable) shows no service, volume, network, database or state left for either task id; `/tmp/<task-id>/` is absent for each; `git worktree list` and `git branch --list` for each repository. A remaining resource is named in the run report, never called cleaned.

## QA artifact cleanup

After confirmed merge and handover, automatically follow [`qa-artifact-cleanup.md`](qa-artifact-cleanup.md) for this unit's recorded local QA files, superseded rounds included. It re-verifies attachments reused from an earlier round before cleanup-ready. This has its own publication/ownership guards; code/worktree cleanup does not authorize broad evidence deletion. An already-delivered unit can retry retained evidence cleanup without reposting handover.

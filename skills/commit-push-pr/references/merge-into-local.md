# Merge into local

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

The opt-in last step of `/commit-push-pr`: merge the PR just opened into the delivery branch `local`, pinned to the pushed head, through GitHub's own gates.

## Preconditions

All must hold; otherwise leave the PR open and report the unmet one under `Needs user:`.

- The step-7 approval showed the merge command and method.
- PR read-back: base is `local`, head is the pushed SHA, `mergeable` is `MERGEABLE`.
- The QA comment is posted and read back.
- `gh pr view <pr-num> --json reviewDecision` is not `CHANGES_REQUESTED`.

## Merge

Pick the method from repository policy before approval: `gh repo view --json mergeCommitAllowed,squashMergeAllowed,rebaseMergeAllowed`, preferring the method the workspace names.

```bash
gh pr merge <pr-num> --auto <--merge|--squash|--rebase> --match-head-commit <pushed-sha>
gh pr view <pr-num> --json state,baseRefName,mergeCommit,autoMergeRequest,url
```

`--auto` leaves the decision to required checks and reviews: the PR merges at once when nothing is pending, otherwise when they pass.

| Read-back | Report |
| --------- | ------ |
| `state: MERGED` with a `mergeCommit` | `merged into local at <merge-sha>` |
| `autoMergeRequest` set, or a confirmed merge-queue entry | `auto-merge enabled, waiting on checks` — not merged yet |
| Auto-merge is not enabled for the repository | Read `gh pr checks <pr-num>`. Every check `pass` or `skipping`, or no checks reported → run the same command without `--auto` and read back again. Anything pending or failing → leave the PR open; suggest `/ci-loop <pr-num>` |
| Branch protection refuses the merge | Leave the PR open and quote the refusal under `Needs user:` |

Merge with the flags above and nothing more: protection, required reviews, and merge queues decide, so `--admin` and `--delete-branch` stay out of the command. The head branch, the worktree, and every local checkout stay as they are.

## After the merge

- `local` is not the default branch, so `Closes`-style keywords do not fire: the issue stays open until the workspace's issue-completion workflow closes it. Say so in the report.
- Suggest `/local-to-staging` in the response footer.

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
| Auto-merge is not enabled for the repository | Read `gh pr checks <pr-num>`. Every check `pass` or `skipping` → run without `--auto` and read back. `no checks reported` counts only with a successful `statusCheckRollup` read returning an empty list; an error is unknown and stops the merge. When no workflow trigger covers the base branch (CI runs only on promotion branches, and lints and tests ran locally before the push), that empty read is absent configured CI. Record the workflows and triggers you read, and the local check result. Anything pending or failing → leave the PR open; suggest `/ci-loop <pr-num>` |
| Branch protection refuses the merge | Leave the PR open and quote the refusal under `Needs user:` |

Merge with the flags above and nothing more: protection, required reviews, and merge queues decide, so `--admin` and `--delete-branch` stay out of the command. The head branch, the worktree, and every local checkout stay as they are.

## After the merge

- The PR carries no closing keyword. Read the issue back after the merge: tracker automation may still close it from a linked branch or PR. Report the actual state and the workspace's completion behavior; never claim it stayed open without read-back.
- Suggest `/local-to-staging` in the response footer.

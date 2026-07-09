# Test cases — `/commit-push-close`

The routing test set for this skill lives in [`evals.json`](evals.json); this file is its readable
form. 11 should-trigger queries and 10 near-miss negatives.

Near-miss negatives name the sibling they *should* route to. An obviously-irrelevant negative
proves nothing — if a query could never plausibly hit this skill, it is not testing the boundary.

## Should trigger (11)

| # | Query |
| :--- | :--- |
| 1 | Commit, push, and close the issue |
| 2 | I'm done with #418, ship it |
| 3 | Wrap up this issue in one step |
| 4 | Ship this issue |
| 5 | Commit this and close #204 with a how-to-test comment |
| 6 | We're finished here — land it and close out the ticket |
| 7 | Commit my changes, push, and mark the issue done |
| 8 | Close out issue 87 with testing steps |
| 9 | Done with the fix — push and close |
| 10 | Ship this small fix — there's no issue for it yet |
| 11 | Run the tests, then close out the issue with proof they pass |

## Should NOT trigger (10)

| # | Query | Routes to |
| :--- | :--- | :--- |
| 1 | Ship this as a PR | `/commit-push-pr` |
| 2 | Open a pull request for this issue | `/commit-push-pr` |
| 3 | Commit, push, and open a PR | `/commit-push-pr` |
| 4 | Summarize what shipped this week for the PM | `/release-notes` |
| 5 | Write release notes for today | `/release-notes` |
| 6 | Fix this issue's labels | `/triage` |
| 7 | This issue needs more info from the reporter | `/triage` |
| 8 | Review my changes before I ship | `/code-review` |
| 9 | Create GitHub issues from this PRD | `/to-tickets` |
| 10 | Close this stale issue as wontfix | `/triage` |

## Rule

Fix descriptions, not queries. A missed should-trigger means the description lacks that phrasing.
A captured near-miss means the boundary sentence is missing, or the sibling's description is weaker
than this one's. Never delete a query to make the eval pass.

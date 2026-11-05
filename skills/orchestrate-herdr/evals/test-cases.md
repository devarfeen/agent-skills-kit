# Test cases — `/orchestrate-herdr`

The routing test set for this skill lives in [`evals.json`](evals.json); this file is its readable
form. 14 should-trigger queries and 13 near-miss negatives.

Near-miss negatives name the sibling they *should* route to. An obviously-irrelevant negative
proves nothing — if a query could never plausibly hit this skill, it is not testing the boundary.

## Should trigger (14)

| # | Query |
| :--- | :--- |
| 1 | orchestrate-herdr for https://github.com/org/repo/issues/42 using codex |
| 2 | Fan this PRD out to per-issue workers |
| 3 | Spin up one worker tab per open sub-issue of PRD-142 using claude |
| 4 | Orchestrate the PRD's sub-issues in herdr with codex workers |
| 5 | Launch herdr workers for every open issue under this parent issue |
| 6 | Run the PRD fan-out — one coding CLI tab per issue |
| 7 | Dispatch these sub-issues to worker tabs and monitor for test-backed completion |
| 8 | Use herdr to work all open slices of this PRD in parallel |
| 9 | Kick off the orchestrator for PRD 89 with opencode |
| 10 | HERDR_ENV=1 — give every open sub-issue of this parent issue its own codex tab |
| 11 | Re-run the PRD orchestrator — some worker tabs from the last run are still open |
| 12 | orchestrate-herdr for PRWL-100 using codex |
| 13 | Fan PRWL-100's sub-issues out to one worker tab each |
| 14 | Spin up a claude tab for every open child issue of ABC-123 |

## Should NOT trigger (13)

| # | Query | Routes to |
| :--- | :--- | :--- |
| 1 | Split this pane in herdr | `herdr` |
| 2 | Read the output of that herdr tab | `herdr` |
| 3 | Create a new tab and run npm test in it | `herdr` |
| 4 | What's the status of the worker tabs? | `herdr` |
| 5 | Slice the PRD into sub-issues first | `/to-tickets` |
| 6 | Work this single issue test-first | `/tdd-loop` |
| 7 | Review the worker's diff | `/code-review` |
| 8 | Generate release notes for what the workers shipped | `/release-notes` |
| 9 | Debug why one worker's tests keep failing | `/diagnosing-bugs` |
| 10 | Watch this one worker tab and tell me when it finishes | `herdr` |
| 11 | Create a Linear issue for this bug | `none` (no tracker MCP in the routing catalog) |
| 12 | Break PRWL-100 into ticket issues | `/to-tickets` |
| 13 | Mark PRWL-101 ready-for-human with a comment | `none` (no tracker MCP in the routing catalog) |

## Rule

Fix descriptions, not queries. A missed should-trigger means the description lacks that phrasing.
A captured near-miss means the boundary sentence is missing, or the sibling's description is weaker
than this one's. Never delete a query to make the eval pass.

# Test cases — `/integration-contract`

The routing test set for this skill lives in [`evals.json`](evals.json); this file is its readable
form. 11 should-trigger queries and 11 near-miss negatives.

Near-miss negatives name the sibling they *should* route to. An obviously-irrelevant negative
proves nothing — if a query could never plausibly hit this skill, it is not testing the boundary.

## Should trigger (11)

| # | Query |
| :--- | :--- |
| 1 | Build the integration contract for PRD-142 |
| 2 | This PRD touches ADMIN-WEB and API-SVC — map the seam before we ship |
| 3 | Make sure the API change won't break the web and mobile consumers of this PRD |
| 4 | Write the producer/consumer contract for this multi-project PRD |
| 5 | Run the smoke gate before we hand PRD-89 to the PM |
| 6 | Which consumers hit the endpoints this PRD changes? |
| 7 | The orders API adds a required field — check the cross-repo impact for the PRD |
| 8 | Gate the multi-project release on the integration checklist |
| 9 | Verify the seam holds between LEGACY-PORTAL and API-SVC for this PRD |
| 10 | PRD-77 spans three repos — what breaks downstream when the API changes? |
| 11 | The PRD says it's API-only, but confirm nothing else in the workspace calls the changed endpoint before we skip the contract |

## Should NOT trigger (11)

| # | Query | Routes to |
| :--- | :--- | :--- |
| 1 | Trace how the invoice API is consumed | `/feature-discovery` |
| 2 | Slice this PRD into issues | `/to-tickets` |
| 3 | The web app breaks when the API deploys — find the root cause | `/diagnosing-bugs` |
| 4 | Write contract tests for the orders endpoint, test-first | `/tdd` |
| 5 | Smoke test the login page visuals against the design | `/pixel-audit` |
| 6 | Punch-list these QA nits | `/polish-batch` |
| 7 | Draft the PRD for this feature | `/to-spec` |
| 8 | Open a PR for the API change | `/commit-push-pr` |
| 9 | Port the orders feature to the mobile app | `/port-feature` |
| 10 | Write end-to-end integration tests for the checkout flow | `/tdd` |
| 11 | Open the checkout in a browser, click through it, and screenshot each step | `agent-browser` |

## Rule

Fix descriptions, not queries. A missed should-trigger means the description lacks that phrasing.
A captured near-miss means the boundary sentence is missing, or the sibling's description is weaker
than this one's. Never delete a query to make the eval pass.

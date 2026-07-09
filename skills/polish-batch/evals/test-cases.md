# Test cases — `/polish-batch`

The routing test set for this skill lives in [`evals.json`](evals.json); this file is its readable
form. 11 should-trigger queries and 10 near-miss negatives.

Near-miss negatives name the sibling they *should* route to. An obviously-irrelevant negative
proves nothing — if a query could never plausibly hit this skill, it is not testing the boundary.

## Should trigger (11)

| # | Query |
| :--- | :--- |
| 1 | Punch-list this for PRD-142: the Billing header says "Recieve invoices" |
| 2 | Capture this for later: the save button is misaligned on Settings |
| 3 | Batch these nits |
| 4 | Polish pass when QA is done — collect the small stuff first |
| 5 | I'm doing manual QA — log these small fixes without fixing them yet |
| 6 | Cosmetic cleanup: wrong copy on the login page, extra padding on the cards |
| 7 | Add to the punch list: the toast says 'succes' |
| 8 | Dispatch the open punch-list items |
| 9 | Collect these copy tweaks and fix them all in one go later |
| 10 | Verify the dispatched punch-list rows against the running app |
| 11 | No ticket for this — start a punch list for today's QA findings |

## Should NOT trigger (10)

| # | Query | Routes to |
| :--- | :--- | :--- |
| 1 | Polish the billing page to match the Figma | `/pixel-audit` |
| 2 | This page must match the design pixel-for-pixel | `/pixel-audit` |
| 3 | The save button doesn't actually save — log it | `/to-tickets` |
| 4 | Do a QA session and file issues as I report bugs | `qa` |
| 5 | Make this dashboard bolder and more delightful | `impeccable` |
| 6 | Set up the design system for ADMIN-WEB | `/design-system` |
| 7 | Review the diff before shipping | `/code-review` |
| 8 | The API returns the wrong total on checkout | `/diagnosing-bugs` |
| 9 | Ship the polish fixes as a PR | `/commit-push-pr` |
| 10 | Fix this typo on the login page right now, don't batch it | `none` |

## Rule

Fix descriptions, not queries. A missed should-trigger means the description lacks that phrasing.
A captured near-miss means the boundary sentence is missing, or the sibling's description is weaker
than this one's. Never delete a query to make the eval pass.

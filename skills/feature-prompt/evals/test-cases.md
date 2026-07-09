# Test cases — `/feature-prompt`

The routing test set for this skill lives in [`evals.json`](evals.json); this file is its readable
form. 11 should-trigger queries and 11 near-miss negatives.

Near-miss negatives name the sibling they *should* route to. An obviously-irrelevant negative
proves nothing — if a query could never plausibly hit this skill, it is not testing the boundary.

## Should trigger (11)

| # | Query |
| :--- | :--- |
| 1 | Help me create a feature prompt for stock transfer approvals |
| 2 | I have a rough idea: let managers bulk-approve timesheets. Turn it into a dev prompt. |
| 3 | Turn this request into something I can grill: CSV export on the orders page |
| 4 | Prep this for grill-with-docs: offline mode for the scanner app |
| 5 | Write up a small prompt for MOBILE-APP: remember the last-used warehouse |
| 6 | I want to propose read-only auditor accounts — shape the request |
| 7 | Shape this brain dump into a thin slice we can plan against |
| 8 | Draft the feature prompt for adding webhooks to PAYMENTS-API |
| 9 | The client wants dark mode. Make it a proper request for planning. |
| 10 | Write me a grill-ready prompt for INVENTORY-SVC: low-stock email alerts |
| 11 | Rough requirement from sales: customers want saved carts. Get it ready for planning. |

## Should NOT trigger (11)

| # | Query | Routes to |
| :--- | :--- | :--- |
| 1 | How does stock transfer approval work today? | `/feature-discovery` |
| 2 | Write the PRD for ADR-0042 | `/to-spec` |
| 3 | Slice this PRD into issues | `/to-tickets` |
| 4 | Grill me on this plan before we build it | `/grill-with-docs` |
| 5 | Just add the CSV export button now, it's tiny | `/tdd-loop` |
| 6 | Write release notes for the transfer feature | `/release-notes` |
| 7 | Pixel-audit the transfers page against the Figma | `/pixel-audit` |
| 8 | Port the invoice screen from LEGACY-PORTAL to ADMIN-WEB | `/port-feature` |
| 9 | File a bug: approvals fail for managers with two roles | `none` |
| 10 | Sharpen the domain terms in CONTEXT.md for the billing module | `/grill-with-docs` |
| 11 | Turn ADR-0017 into a prompt for the implementation agent | `/to-spec` |

## Rule

Fix descriptions, not queries. A missed should-trigger means the description lacks that phrasing.
A captured near-miss means the boundary sentence is missing, or the sibling's description is weaker
than this one's. Never delete a query to make the eval pass.

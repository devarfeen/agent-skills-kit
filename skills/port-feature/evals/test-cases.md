# Test cases — `/port-feature`

The routing test set for this skill lives in [`evals.json`](evals.json); this file is its readable
form. 11 should-trigger queries and 11 near-miss negatives.

Near-miss negatives name the sibling they *should* route to. An obviously-irrelevant negative
proves nothing — if a query could never plausibly hit this skill, it is not testing the boundary.

## Should trigger (11)

| # | Query |
| :--- | :--- |
| 1 | Port stock-transfer approvals from LEGACY-PORTAL to ADMIN-WEB |
| 2 | Help me port the invoice screen into MOBILE-APP |
| 3 | Bring the RFID scan flow from LEGACY-PORTAL over to MOBILE-APP |
| 4 | We're rebuilding the legacy reports module in the new app — map what needs to move |
| 5 | Recreate the old admin's user-management feature in ADMIN-WEB, matching its behaviour |
| 6 | Migrate the quotation workflow from the CodeIgniter app to the Laravel app |
| 7 | The legacy system has bulk import; we need the same in the new stack — plan the port |
| 8 | Write the gap map for porting notifications from LEGACY-PORTAL |
| 9 | What would it take to bring the old barcode screen into MOBILE-APP? Trace it and map the gaps |
| 10 | Map what it takes to move the legacy audit-log viewer into MOBILE-APP |
| 11 | Rebuild the legacy exports feature over here — start with the gap map |

## Should NOT trigger (11)

| # | Query | Routes to |
| :--- | :--- | :--- |
| 1 | How does the legacy quotation workflow work? | `/feature-discovery` |
| 2 | Write a feature prompt for CSV export in ADMIN-WEB | `/feature-prompt` |
| 3 | Copy this helper function from repo A into repo B | `none` |
| 4 | Grill me on the porting plan | `/grill-with-docs` |
| 5 | Implement the ported screen test-first | `/tdd-loop` |
| 6 | Pixel-audit the ported screen against the legacy screens | `/pixel-audit` |
| 7 | Set up the design system for the target app first | `/design-system` |
| 8 | Slice the port PRD into issues | `/to-tickets` |
| 9 | Migrate the database from MySQL 5.7 to MySQL 8 | `none` |
| 10 | Upgrade this app from Laravel 9 to Laravel 11 | `none` |
| 11 | How is the transfers feature different between LEGACY-PORTAL and ADMIN-WEB? | `/feature-discovery` |

## Rule

Fix descriptions, not queries. A missed should-trigger means the description lacks that phrasing.
A captured near-miss means the boundary sentence is missing, or the sibling's description is weaker
than this one's. Never delete a query to make the eval pass.

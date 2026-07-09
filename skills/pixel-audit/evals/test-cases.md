# Test cases — `/pixel-audit`

The routing test set for this skill lives in [`evals.json`](evals.json); this file is its readable
form. 11 should-trigger queries and 12 near-miss negatives.

Near-miss negatives name the sibling they *should* route to. An obviously-irrelevant negative
proves nothing — if a query could never plausibly hit this skill, it is not testing the boundary.

## Should trigger (11)

| # | Query |
| :--- | :--- |
| 1 | Pixel-audit the assets list page in ADMIN-WEB against this Figma node |
| 2 | This page must match the design pixel-for-pixel before we ship |
| 3 | Audit MOBILE-APP order detail against the legacy screens — no Figma exists |
| 4 | The user form drifted from the mock — do a strict visual conformance pass on it |
| 5 | Compare the rendered billing page to its Figma frame and fix every mismatch |
| 6 | Check the dashboard's empty and error states match the design exactly |
| 7 | Verify the transfers page against the reference implementation, element by element |
| 8 | QA says the layout is off vs design on /assets — run the full audit and prove the fixes |
| 9 | Make sure the new settings screen matches Figma, including below the fold |
| 10 | Before we ship, walk the invoice page against Figma node 12:340 and fix anything that's off |
| 11 | Our rebuilt reports screen should be indistinguishable from the old app's — check it element by element and fix the gaps |

## Should NOT trigger (12)

| # | Query | Routes to |
| :--- | :--- | :--- |
| 1 | Billing header says 'Recieve invoices' — punch-list it | `/polish-batch` |
| 2 | Set up the design system for ADMIN-WEB from Figma | `/design-system` |
| 3 | Why does the modal flicker when it opens? | `/diagnosing-bugs` |
| 4 | Fold the shipped page's new UI back into the library | `/design-system` |
| 5 | Screenshot the login page for the release notes | `none` |
| 6 | Trace how the preview route renders components | `/feature-discovery` |
| 7 | Build the integration contract for PRD-142 | `/integration-contract` |
| 8 | Add a failing test for the badge component's disabled state | `/tdd-loop` |
| 9 | Review this PR's CSS changes | `/code-review` |
| 10 | Make the landing page feel more polished and modern | `impeccable` |
| 11 | The save button on settings is misaligned — fix that one nit | `/polish-batch` |
| 12 | Audit the design consistency of every page in the app | `impeccable` |

## Rule

Fix descriptions, not queries. A missed should-trigger means the description lacks that phrasing.
A captured near-miss means the boundary sentence is missing, or the sibling's description is weaker
than this one's. Never delete a query to make the eval pass.

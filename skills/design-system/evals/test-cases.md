# Test cases — `/design-system`

The routing test set for this skill lives in [`evals.json`](evals.json); this file is its readable
form. 11 should-trigger queries and 11 near-miss negatives.

Near-miss negatives name the sibling they *should* route to. An obviously-irrelevant negative
proves nothing — if a query could never plausibly hit this skill, it is not testing the boundary.

## Should trigger (11)

| # | Query |
| :--- | :--- |
| 1 | Set up the design system for ADMIN-WEB from this Figma file |
| 2 | We have no Figma for MOBILE-APP — help me define a design system and build the components |
| 3 | Add the new date-picker component to the ADMIN-WEB design system |
| 4 | That page just shipped — fold its new UI back into the ADMIN-WEB library |
| 5 | Bootstrap tokens and a UI library for PORTAL-WEB from our brand guide |
| 6 | Turn these reference screens into a reusable component library for the new app |
| 7 | Build a preview page showing every component in all its states for ADMIN-WEB |
| 8 | Our buttons are inlined everywhere — set up a proper component library and make agents use it |
| 9 | Project start-off for the new repo: design system from this spec doc |
| 10 | Extract design tokens from our Figma and wire up a component library for PORTAL-WEB |
| 11 | We're starting UI on the new app with no designs — walk me through picking colors, type, and spacing, then build the base components |

## Should NOT trigger (11)

| # | Query | Routes to |
| :--- | :--- | :--- |
| 1 | Pixel-audit the assets list page against this Figma node | `/pixel-audit` |
| 2 | The Save button is misaligned — punch-list it for PRD-142 | `/polish-batch` |
| 3 | Make this landing page look less generic | `none` |
| 4 | Port the invoice screen from LEGACY-PORTAL to ADMIN-WEB | `/port-feature` |
| 5 | Generate AGENTS.md for this workspace | `/agents-md` |
| 6 | How is theming implemented in ADMIN-WEB today? | `/feature-discovery` |
| 7 | Write a feature prompt for the new settings page | `/feature-prompt` |
| 8 | Fix the button component's disabled state test-first | `/tdd-loop` |
| 9 | Audit our color contrast for accessibility | `none` |
| 10 | Which components does the ADMIN-WEB UI library have today? | `/feature-discovery` |
| 11 | Restyle the settings page to use our existing Button component instead of inline markup | `none` |

## Rule

Fix descriptions, not queries. A missed should-trigger means the description lacks that phrasing.
A captured near-miss means the boundary sentence is missing, or the sibling's description is weaker
than this one's. Never delete a query to make the eval pass.

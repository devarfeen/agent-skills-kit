# Test cases — `/writing-kit-skills`

The routing test set for this skill lives in [`evals.json`](evals.json); this file is its readable
form. 7 should-trigger queries and 7 near-miss negatives.

Near-miss negatives name the sibling they *should* route to. An obviously-irrelevant negative
proves nothing — if a query could never plausibly hit this skill, it is not testing the boundary.
A `none` route means no kit skill should claim the query at all.

## Should trigger (7)

| # | Query |
| :--- | :--- |
| 1 | Add a new skill to the agent-skills-kit repo |
| 2 | Rewrite this SKILL.md to match the kit's house style |
| 3 | What's the word budget for a kit SKILL.md? |
| 4 | Tighten the description of the polish-batch skill |
| 5 | Where do the canonical one-liners for the kit live? |
| 6 | Draft the SKILL.md for a new dep-upgrade kit skill |
| 7 | Move this skill's long examples out of SKILL.md properly |

## Should NOT trigger (7)

| # | Query | Routes to |
| :--- | :--- | :--- |
| 1 | Write release notes for last week | `/release-notes` |
| 2 | Generate the workspace AGENTS.md | `/agents-md` |
| 3 | Write a skill for my other project's deploy flow | `none` |
| 4 | Improve this prompt for grill-with-docs | `/feature-prompt` |
| 5 | Document our coding style in CONTRIBUTING | `none` |
| 6 | Refactor this module to be more readable | `none` |
| 7 | Run the trigger evals for the kit | `none` |

## Rule

Fix descriptions, not queries. A missed should-trigger means the description lacks that phrasing.
A captured near-miss means the boundary sentence is missing, or the sibling's description is weaker
than this one's. Never delete a query to make the eval pass.

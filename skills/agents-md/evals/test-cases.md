# Test cases — `/agents-md`

The routing test set for this skill lives in [`evals.json`](evals.json); this file is its readable
form. 10 should-trigger queries and 11 near-miss negatives.

Zero attribution: omit co-author, AI, and tool attribution from evaluation artifacts and publications.

Near-miss negatives name the sibling they *should* route to. An obviously-irrelevant negative
proves nothing — if a query could never plausibly hit this skill, it is not testing the boundary.

## Should trigger (10)

| # | Query |
| :--- | :--- |
| 1 | Generate AGENTS.md for this workspace |
| 2 | Set up the workspace agent instructions from my code-workspace file |
| 3 | Create the Project Matrix and non-negotiable rules for this workspace |
| 4 | Refresh the Project Matrix — I added a folder to the workspace |
| 5 | Regenerate the workspace AGENTS.md |
| 6 | Bootstrap agent rules for my multi-repo VS Code workspace |
| 7 | Make the CLAUDE.md shim and AGENTS.md for this workspace root |
| 8 | New workspace — establish the PROJECT-CODEs |
| 9 | We added another repo to the code-workspace — refresh the workspace agent rules |
| 10 | Synchronize existing project-runtime blocks from this code-workspace and local Compose file; leave workspace-root instructions unchanged |

## Should NOT trigger (11)

| # | Query | Routes to |
| :--- | :--- | :--- |
| 1 | Set up the design system for this project | `/design-system` |
| 2 | Configure the issue tracker and GLOSSARY.md location | `/setup-matt-pocock-skills` |
| 3 | Seed the project ui-coding skill for ADMIN-WEB | `/design-system` |
| 4 | Generate release notes for the workspace | `/release-notes` |
| 5 | Trace how the workspace build pipeline works | `/feature-discovery` |
| 6 | Sharpen the project's domain terminology | `domain-modeling` |
| 7 | Create a new skill for our deploy process | `skill-creator` |
| 8 | Add a binding AGENTS.md rule so UI changes reuse the component library | `/design-system` |
| 9 | Write an AGENTS.md for this repo | `/writing-for-agents` |
| 10 | Add the CLAUDE.md shim that forwards Claude to AGENTS.md in this workspace | `/writing-for-agents` |
| 11 | Edit this hand-authored repo AGENTS.md; there is no code-workspace file and no workspace generation is requested | `/writing-for-agents` |

## Scope correction

The generator supports workspace-root generation and existing project-runtime
synchronization. Repo-only and shim-only requests route to hand-authored
instruction editing; the generator never creates `CLAUDE.md`. Cases cover
runtime-only synchronization and no-workspace editing. Current run evidence
belongs in the [current audit](../../../evals/current/README.md).

## Rule

Fix descriptions, not queries. A missed should-trigger means the description lacks that phrasing.
A captured near-miss means the boundary sentence is missing, or the sibling's description is weaker
than this one's. Never delete a query to make the eval pass.

## Combined-output boundary

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

The combined shim-plus-AGENTS request is retained as a negative: since v50
the generator explicitly never writes CLAUDE.md or GEMINI.md. A new positive
requests the supported workspace generation plus reporting of an existing shim.
The requested-output boundary is tested rather than promising the removed output.

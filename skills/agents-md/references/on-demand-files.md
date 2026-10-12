# On-demand files

The generated rules are split so the always-loaded `AGENTS.md` stays small: it holds the rules every task needs and a table that says which `rules/` file to read before which action.

Zero attribution: omit co-author, AI, and tool attribution from all output.

## File map

| Asset | Written to | Slots to fill |
| :--- | :--- | :--- |
| `assets/agents-md-template.md` | `AGENTS.md` | intro line; the `#### North star` list when emitted |
| `assets/rules/projects.md` | `rules/projects.md` | Project Matrix |
| `assets/rules/skills.md` | `rules/skills.md` | gradient table, startup lines, companions, Matt routing when emitted, Runtime tool-calling table |
| `assets/rules/orchestration.md`, `verification.md`, `browser.md`, `shipping.md`, `issues.md` | `rules/<same name>` | none |

Create `rules/` when it is missing. Write no other file there, and never edit or delete a file this map does not name.

The on-demand table in `AGENTS.md` is fixed text. Never add, drop, or reword a row to fit the workspace — every row's file is always written, also when Matt routing is omitted from `skills.md`.

Sections another skill adds (`## Design System / UI Library`, `## QA escape guards`) stay in `AGENTS.md`. Never move them into `rules/`.

## Existing files

Check each target on its own, with the gates in `SKILL.md`:

- **None** — write it.
- **Marker present** — show its diff and confirm before overwriting.
- **No marker** — a hand-written file with a generated name. Do not overwrite it; show what generation would write, merge only user-approved sections, and say that the `AGENTS.md` table row points at a file this skill did not generate. When that file is `projects.md` and the merge is declined, say that the Project Matrix was not written and stop before writing `AGENTS.md`.

One confirmation may cover every file, but the diff shows each file separately and in full.

Write the `rules/` files first and `AGENTS.md` last, so a failed run never leaves the table pointing at files that were not written. On a failure, stop and report which files were written.

## From the single-file layout

A marked `AGENTS.md` below `v50` holds the matrix, every rule, the skills tables, and Issue titles inline.

1. Build every file from the assets as for a fresh generation.
2. Carry over: each PROJECT-CODE, matched by `Path` from the old inline matrix into `projects.md`; filled Context placeholders; sections other skills added, which stay in `AGENTS.md` after the rules in their old order.
3. A rule body the user customized may now belong in a `rules/` file. Compare the old body with its new home and apply [Reconcile customized rules](regeneration.md#reconcile-customized-rules) there.
4. In the diff, label a section that left `AGENTS.md` as `moved to rules/<file>`, not as a deletion, and show each new file in full.
5. Confirm once, then write in the order above.

# Quality scorecard — `/agents-md`

**Scored:** 2026-07-17 · **Reader:** fresh scorer agent (post-revamp rescore) · **Rubric:** `evals/skill-quality-rubric.md`

## Trigger eval

Routing baseline: unchanged description; 2026-07-09 baseline stands (21/21, re-confirmed unanimous in the 2026-07-14 maintainer sweep recorded in `evals.json`).

| Category | Score | Note (only if below 5) |
| :--- | :---: | :--- |
| Purpose clarity | 5 | |
| Trigger clarity | 5 | |
| Scope control | 5 | |
| Instruction quality | 4 | SKILL.md:56 slot enumeration omits the template's fifth bracketed slot |
| Brevity | 5 | |
| Engineering usefulness | 5 | |
| Agent usability | 5 | |
| Verification quality | 5 | |
| TDD / testing compat | N/A | |
| Maintainability | 4 | Template placeholder points at a SKILL.md heading the house-style rewrite renamed |
| Frontier readiness | 5 | |
| **Average** | **4.80** | |

`N/A` is permitted only on TDD / testing compat, and only with a justification
sentence here:

> The skill generates markdown instruction files (`AGENTS.md` + `CLAUDE.md` shim); it neither produces code nor gates on someone else's tests, so there is no testable surface — done-ness is enforced by the observable completion checklist (row-count match, empty `diff` against the shim template, marker line present).

## Defects

One row per defect. A defect with no anchor and no exact edit is an opinion —
delete it.

| `file:line` | Category | Problem | Exact fix | Gate |
| :--- | :--- | :--- | :--- | :--- |
| `skills/agents-md/SKILL.md:56` | Instruction quality | "filling only the bracketed slots (intro line, Project Matrix, skills tables + startup note, `### Runtime Tool-Calling` tables)" — the word "only" excludes the template's fifth bracketed slot, `[NORTH STAR …]` at `assets/agents-md-template.md:185`, which the very next bullet (line 59) says to fill with the vision-file list when the scan finds one | extend the parenthetical to "…, `### Runtime Tool-Calling` tables, North star list when emitted)" | `none` |
| `skills/agents-md/assets/agents-md-template.md:173` | Maintainability | placeholder reads "per the Skills Manifest rules in SKILL.md", but the 2026-07 house-style rewrite (17c0fd3) renamed that heading — pre-rewrite SKILL.md had `### Skills Manifest`; the rules now live under `## Working with skills` — leaving a dangling pointer | change to "per the Working with skills rules in SKILL.md" (placeholder text is never emitted, so no version-marker bump is triggered) | `none` |

**Gates** mean the fix cannot land as an ordinary edit:

- `dup-pair` — the text is duplicated by design (`ship-policy.md`,
  `context-terms.md`). Edit every copy together or `tools/validate.sh` check 2
  fails.
- `description-locked` — the fix would change frontmatter `description`, which
  invalidates the trigger-eval baseline. Needs a maintainer eval re-run.

## Verdict

- [ ] Averages 5.00 — nothing left to point at
- [x] Below 5.00 — the blocking defects are listed above, each with an owner
      and a gate

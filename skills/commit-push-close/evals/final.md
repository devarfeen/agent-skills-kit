# Quality scorecard — `/commit-push-close`

**Scored:** 2026-07-17 · **Reader:** fresh rescorer (round 2) · **Rubric:** `evals/skill-quality-rubric.md`

## Trigger eval

Routing baseline: maintainer sweep pending for the 2026-07-16/17 description batch

## Round-1 fix verification

- Defect 1 (ordering-dependent test gate): fixed. Step 10 (`SKILL.md:67`) now reads "when the How-to-test plan contains a runnable test command" and completion criterion 2 (`SKILL.md:99`) reads "when the plan contains a runnable test command" — the "opens with" ordering dependency is gone at both anchors.
- Defect 2 (no phase updates): fixed. `SKILL.md:37` carries the canonical one-liner byte-exact directly under `## Workflow` ("Emit `Stage / Found / Next / Needs user` at each phase transition — one line per field."); `tools/validate.sh` check 13 passes.

## Quality

| Category | Score | Note (only if below 5) |
| :--- | :---: | :--- |
| Purpose clarity | 5 | |
| Trigger clarity | 5 | |
| Scope control | 5 | |
| Instruction quality | 5 | |
| Brevity | 5 | |
| Engineering usefulness | 5 | |
| Agent usability | 5 | |
| Verification quality | 5 | |
| TDD / testing compat | 5 | |
| Maintainability | 5 | |
| Frontier readiness | 5 | |
| **Average** | **5.00** | |

## Defects

One row per defect. A defect with no anchor and no exact edit is an opinion —
delete it.

| `file:line` | Category | Problem | Exact fix | Gate |
| :--- | :--- | :--- | :--- | :--- |
| — | — | none | — | — |

**Gates** mean the fix cannot land as an ordinary edit:

- `dup-pair` — the text is duplicated by design (`ship-policy.md`,
  `context-terms.md`). Edit every copy together or `tools/validate.sh` check 2
  fails.
- `description-locked` — the fix would change frontmatter `description`, which
  invalidates the trigger-eval baseline. Needs a maintainer eval re-run.

## Verdict

- [x] Averages 5.00 — nothing left to point at
- [ ] Below 5.00 — the blocking defects are listed above, each with an owner
      and a gate

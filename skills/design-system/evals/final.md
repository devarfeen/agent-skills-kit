# Quality scorecard — `/design-system`

**Scored:** 2026-07-17 · **Reader:** fresh rescorer (round 2) · **Rubric:** `evals/skill-quality-rubric.md`

## Trigger eval

Routing baseline: unchanged description; 2026-07-09 baseline stands (22/22, re-confirmed in the 2026-07-14 `last_run` after body-only edits). The pending 2026-07-16/17 maintainer sweep covers other skills' descriptions only; none of the new/edited descriptions collides with this skill's trigger queries.

## Round-1 fix verification

- `SKILL.md:43` — the agent-half quote line now requires "the rendered component list (DOM query, tree snapshot, or served-HTML match) checked off against the extracted inventory — a bare aggregate count is not evidence". The per-component check-off replaces the count-level evidence; fixed as specified.
- `SKILL.md:84` — the output template's `Next:` line now reads "then `/feature-prompt` for the first feature", matching the footer suggestion two lines below; "Workflow B" (defined only in human-facing `BEST-PRACTICES.md`) is gone. Fixed as specified.
- No new defect introduced by either fix.

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

`N/A` is permitted only on TDD / testing compat, and only with a justification
sentence here:

> _(unused — the skill verifies a rendered result: the agent half demands a machine-checkable observation, the rendered component list checked off against the extracted inventory, plus render/snapshot tests where a harness exists.)_

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

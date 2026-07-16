# Skill audit template

Copy into `skills/<name>/evals/final.md` (or `baseline.md`) and fill in. Delete this line and the
heading above; keep the structure below.

---

# Quality scorecard — `/<skill-name>`

**Scored:** YYYY-MM-DD · **Reader:** who or what scored it · **Rubric:** `evals/skill-quality-rubric.md`

| Category | Score | Note (only if below 5) |
| :--- | :---: | :--- |
| Purpose clarity | | |
| Trigger clarity | | |
| Scope control | | |
| Instruction quality | | |
| Brevity | | |
| Engineering usefulness | | |
| Agent usability | | |
| Verification quality | | |
| TDD / testing compat | | |
| Maintainability | | |
| Frontier readiness | | |
| **Average** | | |

`N/A` is permitted only on TDD / testing compat, and only with a justification
sentence here:

> _(delete if unused)_

## Defects

One row per defect. A defect with no anchor and no exact edit is an opinion —
delete it.

| `file:line` | Category | Problem | Exact fix | Gate |
| :--- | :--- | :--- | :--- | :--- |
| | | | | `none` / `dup-pair` / `description-locked` |

**Gates** mean the fix cannot land as an ordinary edit:

- `dup-pair` — the text is duplicated by design (`ship-policy.md`,
  `context-terms.md`). Edit every copy together or `tools/validate.sh` check 2
  fails.
- `description-locked` — the fix would change frontmatter `description`, which
  invalidates the trigger-eval baseline. Needs a maintainer eval re-run.

## Verdict

- [ ] Averages 5.00 — nothing left to point at
- [ ] Below 5.00 — the blocking defects are listed above, each with an owner
      and a gate

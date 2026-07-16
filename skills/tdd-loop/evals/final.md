# Quality scorecard — `/tdd-loop`

**Scored:** 2026-07-17 · **Reader:** fresh scorer agent (post-revamp rescore) · **Rubric:** `evals/skill-quality-rubric.md`

## Trigger eval

Routing baseline: maintainer sweep pending for the 2026-07-16/17 description batch.

| Category | Score | Note (only if below 5) |
| :--- | :---: | :--- |
| Purpose clarity | 5 | |
| Trigger clarity | 5 | Read against the 16-description catalog: all 12 trigger queries land here (no kit sibling claims test-first work) and all 9 no-trigger queries route to their named siblings; the dropped "write a failing test" phrase costs nothing inside the kit catalog. |
| Scope control | 5 | |
| Instruction quality | 5 | |
| Brevity | 4 | `SKILL.md:124` restates completion checkbox 1 (`SKILL.md:107-108`) as a slogan — same gate stated twice in adjacent sections. |
| Engineering usefulness | 5 | |
| Agent usability | 5 | |
| Verification quality | 5 | |
| TDD / testing compat | 5 | |
| Maintainability | 5 | |
| Frontier readiness | 5 | |
| **Average** | **4.91** | |

## Defects

One row per defect. A defect with no anchor and no exact edit is an opinion —
delete it.

| `file:line` | Category | Problem | Exact fix | Gate |
| :--- | :--- | :--- | :--- | :--- |
| `skills/tdd-loop/SKILL.md:124` | Brevity | `"Tests pass" without a witnessed red is not TDD evidence.` duplicates checkbox 1 (line 107-108, "Each new test was seen failing — quote the failing run — before it passed"), the same gate stated twice 16 lines apart — the rules↔checklist duplication the house style hunts, and a drift point | Delete line 124; checkbox 1 already binds the quoted-red requirement | `none` |

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

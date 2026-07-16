# Quality scorecard — `/port-feature`

**Scored:** 2026-07-17 · **Reader:** fresh scorer agent (post-revamp rescore) · **Rubric:** `evals/skill-quality-rubric.md`

## Trigger eval

Routing baseline: unchanged description; 2026-07-09 baseline stands (22/22 unanimous, re-confirmed 2026-07-14 after body-only edits).

## Quality

| Category | Score | Note (only if below 5) |
| :--- | :---: | :--- |
| Purpose clarity | 5 | |
| Trigger clarity | 5 | |
| Scope control | 5 | |
| Instruction quality | 5 | |
| Brevity | 4 | `SKILL.md:39` — the sub-agents bullet ends with a second "Never cloud agents." that repeats the clause four words earlier in the same line |
| Engineering usefulness | 5 | |
| Agent usability | 5 | |
| Verification quality | 4 | `SKILL.md:125` — the git-status criterion is unsatisfiable in a tree that was already dirty before the run |
| TDD / testing compat | 5 | |
| Maintainability | 5 | |
| Frontier readiness | 5 | |
| **Average** | **4.82** | |

TDD / testing compat is numeric, not `N/A`: the skill plans work that will be
tested, and section 5 of the gap map ("Tests needed") carries the acceptance
categories a later test can assert against, with "cover every category its
template bullet lists" as the fill rule (`SKILL.md:85`, `SKILL.md:104`).

## Defects

| `file:line` | Category | Problem | Exact fix | Gate |
| :--- | :--- | :--- | :--- | :--- |
| `skills/port-feature/SKILL.md:39` | Brevity | The trailing sentence "Never cloud agents." duplicates "never cloud agents" from the canonical one-liner it follows, adding no information — every other skill's suffix on this line carries new content (compare `feature-discovery/SKILL.md:23`, `pixel-audit/SKILL.md:100`) | Delete the trailing sentence "Never cloud agents." so the bullet ends at "…as it completes." (canonical line stays byte-exact) | `none` |
| `skills/port-feature/SKILL.md:125` | Verification quality | "`git status` shows no diff outside the gap map file" cannot be satisfied when the working tree was dirty before the run — an honest agent is stuck, a dishonest one checks the box anyway | Rephrase to the scoped form the kit already uses (`feature-discovery/SKILL.md:95`): "`git status` shows no files created or modified by this run outside the gap map file — nothing implemented" | `none` |

## Verdict

- [ ] Averages 5.00 — nothing left to point at
- [x] Below 5.00 — the blocking defects are listed above, each with an owner
      and a gate

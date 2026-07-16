# Quality scorecard — `/port-feature`

**Scored:** 2026-07-17 · **Reader:** fresh rescorer (round 2) · **Rubric:** `evals/skill-quality-rubric.md`

## Trigger eval

Routing baseline: unchanged description; 2026-07-09 baseline stands (22/22 unanimous, re-confirmed 2026-07-14 per `evals.json` `last_run`).

## Round-1 fix verification

| Round-1 defect | Anchor | Verified |
| :--- | :--- | :--- |
| Trailing "Never cloud agents." duplicating the canonical sub-agents one-liner | `SKILL.md:39` | Fixed verbatim in commit `671a1e5` — the bullet now ends at "…report each lane as it completes." with the canonical one-liner byte-exact (validate.sh check 13 green) |
| Unscoped git-status completion criterion, unsatisfiable in a pre-dirty tree | `SKILL.md:125` | Fixed verbatim — now reads "`git status` shows no files created or modified by this run outside the gap map file — nothing implemented", the scoped form the kit already uses |

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

TDD / testing compat is numeric, not `N/A`: the skill plans work that will be
tested — gap-map section 5 ("Tests needed") carries the acceptance categories a
later test can assert against, with "cover every category its template bullet
lists" as the fill rule (`SKILL.md:85`, `SKILL.md:104`).

## Category notes (what was checked)

- **Purpose:** identity opener with the single-pass boundary ("a single pass, not a loop and not a pipeline", `SKILL.md:9`).
- **Scope:** suggest-never-auto-chain, never-implement with the one permitted write named (`SKILL.md:31-32`), narrow-retrieval prohibition paired with its replacement (`SKILL.md:34`), no-fabricated-issue rule (`SKILL.md:38`).
- **Agent usability:** input resolution order with a Needs-user stop naming the missing input (`SKILL.md:19`); artifact path with the canonical `<artifacts-root>` resolution and slug rule (`SKILL.md:59-63`); exact final phase-update template (`SKILL.md:111-119`); absences of binding rules route to Open questions rather than blocking (`SKILL.md:27`, `SKILL.md:44`).
- **Verification:** all three completion criteria observable — artifact on disk with nine non-empty sections, run-scoped `git status`, final update emitted ending at the suggestion.
- **Maintainability:** canonical one-liners byte-exact (check 13 green); `agents/openai.yaml` parity present; `references/gapmap-example.md` carries the granularity bar with no placeholder scaffolding (check 14 green). Body 1,306 words, under the ceiling.

## Defects

One row per defect. A defect with no anchor and no exact edit is an opinion —
delete it.

None — both round-1 defects were fixed verbatim at their anchors, and a fresh full-file read found no new anchored defect.

## Verdict

- [x] Averages 5.00 — nothing left to point at
- [ ] Below 5.00 — the blocking defects are listed above, each with an owner
      and a gate

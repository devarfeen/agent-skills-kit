# Quality scorecard — `/design-system`

**Scored:** 2026-07-17 · **Reader:** fresh scorer agent (post-revamp rescore) · **Rubric:** `evals/skill-quality-rubric.md`

## Trigger eval

Routing baseline: unchanged description; 2026-07-09 baseline stands (re-confirmed 22/22 in the 2026-07-14 `last_run` after body-only edits).

| Category | Score | Note (only if below 5) |
| :--- | :---: | :--- |
| Purpose clarity | 5 | |
| Trigger clarity | 5 | |
| Scope control | 5 | |
| Instruction quality | 5 | |
| Brevity | 5 | |
| Engineering usefulness | 5 | |
| Agent usability | 5 | |
| Verification quality | 4 | Agent-half evidence is count-level while the check it certifies is per-component (SKILL.md:43). |
| TDD / testing compat | 5 | |
| Maintainability | 5 | |
| Frontier readiness | 4 | "Workflow B" at SKILL.md:84 is defined only in human-facing `BEST-PRACTICES.md` — hidden context for a standalone install. |
| **Average** | **4.82** | |

## Defects

One row per defect. A defect with no anchor and no exact edit is an opinion —
delete it.

| `file:line` | Category | Problem | Exact fix | Gate |
| :--- | :--- | :--- | :--- | :--- |
| `skills/design-system/SKILL.md:43` | Verification quality | The gate instructs "check every extracted component appears", but the quoted evidence is aggregate — "URL/file, status, screenshot path, component count" — with no stated provenance for the count, so a missing component can pass behind a plausible count restated from the extraction step. | Change the quote line to require the rendered component list matched against the extracted list — "Quote the evidence: URL/file, status, screenshot path, and the rendered component list (DOM query, tree snapshot, or served-HTML match) checked off against the extraction." | `none` |
| `skills/design-system/SKILL.md:84` | Frontier readiness | The output template's `Next:` line says "then Workflow B for the first feature" — "Workflow B" appears nowhere in this skill, its references, or any model-facing kit file; it is defined only in human-facing `BEST-PRACTICES.md:145`, which does not travel with a standalone install. | Replace "then Workflow B for the first feature" with "then `/feature-prompt` for the first feature", matching the footer suggestion two lines below. | `none` |

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

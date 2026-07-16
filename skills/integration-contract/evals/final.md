# Quality scorecard — `/integration-contract`

**Scored:** 2026-07-17 · **Reader:** fresh scorer agent (post-revamp rescore) · **Rubric:** `evals/skill-quality-rubric.md`

## Trigger eval

Routing baseline: unchanged description; 2026-07-09 baseline stands (22/22 re-confirmed 2026-07-14 after body-only edits).

| Category | Score | Note (only if below 5) |
| :--- | :---: | :--- |
| Purpose clarity | 5 | |
| Trigger clarity | 5 | |
| Scope control | 5 | |
| Instruction quality | 5 | |
| Brevity | 5 | |
| Engineering usefulness | 5 | |
| Agent usability | 4 | Build-update template branches only `Stage:` for the single-project outcome; `Found:`/`Next:` still prescribe contract-flow content, so the mandated report (completion criterion 3) misleads the caller on that branch. |
| Verification quality | 5 | |
| TDD / testing compat | 5 | |
| Maintainability | 5 | |
| Frontier readiness | 5 | |
| **Average** | **4.91** | |

`N/A` is permitted only on TDD / testing compat, and only with a justification
sentence here:

> _(unused — the skill plans work that will be tested: its Section 4 flows carry driver-named, assertable acceptance criteria, and the gate demands quoted evidence per flow.)_

## Defects

One row per defect. A defect with no anchor and no exact edit is an opinion —
delete it.

| `file:line` | Category | Problem | Exact fix | Gate |
| :--- | :--- | :--- | :--- | :--- |
| `skills/integration-contract/SKILL.md:109-110` | Agent usability | The build-update template gives a `[or: single project — no contract needed …]` alternative for `Stage:` only; on that branch `Found: producer <PROJECT-CODE>; consumers …` and `Next: implement the slices, then integration-contract gate mode before spec-level ship and PM handoff.` are wrong (no producer/consumers were confirmed, no gate will ever run), yet completion criterion 3 requires the emitted update to match the template | Append branch alternatives: line 109 `Found: … <R> risk row(s). [or: matrix swept for <K> changed surfaces; no external call-sites]`; line 110 `Next: … PM handoff. [or: proceed per-slice — no integration gate needed]` | `none` |

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

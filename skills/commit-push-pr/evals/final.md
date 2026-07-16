# Quality scorecard — `/commit-push-pr`

**Scored:** 2026-07-17 · **Reader:** fresh scorer agent (post-revamp rescore) · **Rubric:** `evals/skill-quality-rubric.md`

## Trigger eval

Routing baseline: maintainer sweep pending for the 2026-07-16/17 description batch

| Category | Score | Note (only if below 5) |
| :--- | :---: | :--- |
| Purpose clarity | 5 | |
| Trigger clarity | 5 | |
| Scope control | 5 | |
| Instruction quality | 5 | |
| Brevity | 5 | |
| Engineering usefulness | 5 | |
| Agent usability | 5 | |
| Verification quality | 4 | Step 11's post-push re-check names no mechanism — see defect row |
| TDD / testing compat | 5 | |
| Maintainability | 5 | |
| Frontier readiness | 5 | |
| **Average** | **4.91** | |

## Defects

One row per defect. A defect with no anchor and no exact edit is an opinion —
delete it.

| `file:line` | Category | Problem | Exact fix | Gate |
| :--- | :--- | :--- | :--- | :--- |
| `skills/commit-push-pr/SKILL.md:78` | Verification quality | Step 11 says "confirm the passing tail already quoted into the approved body (step 6) still holds against the just-pushed commit" without naming the action, so a compliant agent may satisfy it by reasoning "nothing changed since step 6" — which ships a stale quoted tail exactly when ship-policy's hook-failure rule forced a NEW commit (or a hook auto-formatted the tree) after the step 6 run | Replace the confirm clause with: "re-run that command when any commit exists that step 6's run did not test (hook-failure fix, hook auto-format); a changed tail stops here — fix and refresh the drafted body before `gh pr create`" | `none` |

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

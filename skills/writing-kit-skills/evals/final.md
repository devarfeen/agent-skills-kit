# Quality scorecard — `/writing-kit-skills`

**Scored:** 2026-07-17 · **Reader:** fresh scorer agent (post-revamp rescore) · **Rubric:** `evals/skill-quality-rubric.md`

## Trigger eval

Routing baseline: maintainer sweep pending for the 2026-07-16/17 description batch (this skill is
in the new set). Read the 14 `evals.json` queries against the 16-description catalog: all 7
triggers name kit-skill authoring, which only this description claims; the 7 negatives each have a
stronger home (/release-notes, /agents-md, /feature-prompt) or no kit route. The nearest external
collider is the generic skill-creator companion, but every trigger query carries a "kit" token
that this description owns; no misrouting query could be named.

## Round-1 fix verification

Both round-1 defects are fixed at their anchors: the completion-criterion word-count command
(line 74) is now byte-identical to the counter `tools/validate.sh` check 12 runs (verified against
validate.sh line 372), and the ceiling wording (line 25) now reads "(body only, after the closing
`---`)", matching what the validator counts.

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

`N/A` is permitted only on TDD / testing compat, and only with a justification
sentence here:

> _(unused — the skill gates on `tools/validate.sh`, the kit's executable check suite, and its
> completion criterion names the command and its one allowed failure mode; category 9 is scored)_

## Defects

One row per defect. A defect with no anchor and no exact edit is an opinion —
delete it.

| `file:line` | Category | Problem | Exact fix | Gate |
| :--- | :--- | :--- | :--- | :--- |
| — | — | none found | — | — |

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

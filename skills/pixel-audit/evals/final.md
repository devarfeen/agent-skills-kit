# Quality scorecard — `/pixel-audit`

**Scored:** 2026-07-17 · **Reader:** fresh scorer agent (post-revamp rescore) · **Rubric:** `evals/skill-quality-rubric.md`

## Trigger eval

Routing baseline: unchanged description; 2026-07-09 baseline stands (re-confirmed 23/23 unanimous on 2026-07-14; the 2026-07-16 body rewrite, commit `bb3dfbb`, left the frontmatter description untouched).

| Category | Score | Note (only if below 5) |
| :--- | :---: | :--- |
| Purpose clarity | 5 | |
| Trigger clarity | 5 | |
| Scope control | 5 | |
| Instruction quality | 4 | `SKILL.md:100` — "Lanes map only." is a clipped three-word fragment carrying a safety constraint; see Defects. |
| Brevity | 5 | |
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
| `skills/pixel-audit/SKILL.md:100` | Instruction quality | "Lanes map only." is a clipped fragment appended to the canonical sub-agents line; "map" is only decodable by back-referencing step heading "1. Map the page", and a runtime that misparses it (noun reading: "lanes map") loses the constraint that keeps fixing and the gate out of parallel lanes — the exact failure the line exists to prevent | Replace `Lanes map only.` with `Lanes run only step 1 (Map the page); fixing and the gate stay with the main agent.` (keep the canonical one-liner before it byte-exact) | `none` |

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

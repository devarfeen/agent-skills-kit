# Quality scorecard — `/writing-kit-skills`

**Scored:** 2026-07-17 · **Reader:** fresh scorer agent (post-revamp rescore) · **Rubric:** `evals/skill-quality-rubric.md`

## Trigger eval

Routing baseline: maintainer sweep pending for the 2026-07-16/17 description batch (this skill is
in the new set). Read against the 16-description catalog, all 7 trigger queries land here — no kit
sibling claims skill authoring — and all 7 negatives have a stronger home or no plausible kit route.

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
| Verification quality | 4 | Completion-criterion word-count command emits no output — the check cannot be witnessed as written |
| TDD / testing compat | 5 | |
| Maintainability | 4 | "(frontmatter included)" contradicts what validator check 12 actually counts |
| Frontier readiness | 5 | |
| **Average** | **4.82** | |

## Defects

| `file:line` | Category | Problem | Exact fix | Gate |
| :--- | :--- | :--- | :--- | :--- |
| `skills/writing-kit-skills/SKILL.md:74` | Verification quality | The documented check `awk 'f&&NF{c+=NF} /^---$/{f++}' skills/<name>/SKILL.md` has no `END{print c}`, so it prints nothing and the "≤ 1,500" comparison cannot be made; it also counts frontmatter and the closing `---`, unlike the enforced check | Replace with the validator's counter: `awk 'NR==1&&/^---$/{f=1;next} f==1&&/^---$/{f=2;next} f==2&&NF{c+=NF} END{print c+0}' skills/<name>/SKILL.md` | `none` |
| `skills/writing-kit-skills/SKILL.md:25` | Maintainability | "1,500 (frontmatter included) is the validator-enforced ceiling" is false — `tools/validate.sh` check 12 counts only the body after the closing `---` (frontmatter excluded) | Change "(frontmatter included)" to "(body only, after the closing `---`)" | `none` |

## Verdict

- [ ] Averages 5.00 — nothing left to point at
- [x] Below 5.00 — the blocking defects are listed above, each with an owner
      and a gate

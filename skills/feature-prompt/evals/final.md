# Quality scorecard — `/feature-prompt`

**Scored:** 2026-07-17 · **Reader:** fresh scorer agent (post-revamp rescore) · **Rubric:** `evals/skill-quality-rubric.md`

## Trigger eval

Routing baseline: unchanged description; 2026-07-09 baseline stands (22/22 re-confirmed 2026-07-14). No query in `evals.json` misroutes against the current 16-description catalog, including the three new siblings (`pr-feedback`, `staging-fix`, `writing-kit-skills`) — none claims prompt-shaping intake.

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

**TDD scored numerically, not `N/A` (departure from the 2026-07-09 scorecard):**
`evals/tdd-workflow-eval.md` lists `feature-prompt` under the "Plans work that
will be tested" surface, whose 5/5 bar is "the artifact it emits carries the
acceptance criteria a test can later assert against." The output contract's
`Expected end result` bracket (SKILL.md:29-31) requires an observable done
state — user-visible behavior, passing checks, or a demo flow — and states it
seeds the later acceptance criteria. That meets the bar, so the category has a
surface and earns a 5 rather than an exemption.

Spot checks behind the 5s:

- Away-fallbacks on all three human gates: unconfirmed-draft save (SKILL.md:127-129),
  candidate-terms skip (references/context-terms.md:33-35), new-numbered-revision
  on hand-edited conflict (SKILL.md:175-177) — no autonomous deadlock.
- Verification is observable: pre-save checklist over artifact properties plus
  re-open-and-confirm read-back before reporting (SKILL.md:131-133).
- Maintainability: `references/context-terms.md` byte-identical to the
  `feature-discovery` copy (diff clean); all three canonical one-liners
  (artifacts-root, graphify, sub-agent lanes) byte-exact; `agents/openai.yaml`
  mirrors `disable-model-invocation`; word count 1,360 incl. frontmatter,
  under the 1,500 ceiling.
- No phase-update line, and none owed: the skill forbids broad scans by default
  (SKILL.md:54) and runs as a short interactive draft-confirm-save pass, not a
  long-running background job; lane dispatch already carries its own
  announce-and-report requirement (SKILL.md:122).

## Defects

One row per defect. A defect with no anchor and no exact edit is an opinion —
delete it.

None. Candidates examined and rejected: the unnamed first kind in "both kinds"
(SKILL.md:96-98) leaves behavior unambiguous (everything lands under
`Open questions`; only ungrillable items additionally route); the `Next:` line
plus footer both naming `/grill-with-docs` (SKILL.md:139,142) are different
surfaces — mandatory handoff vs. capped advisory list; pre-save checklist items
are artifact-observable verification-gate checks, not rule restatement.

## Verdict

- [x] Averages 5.00 — nothing left to point at
- [ ] Below 5.00 — the blocking defects are listed above, each with an owner
      and a gate

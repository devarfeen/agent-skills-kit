# Quality scorecard — `/polish-batch`

**Scored:** 2026-07-17 · **Reader:** fresh scorer agent (post-revamp rescore) · **Rubric:** `evals/skill-quality-rubric.md`

## Trigger eval

Routing baseline: maintainer sweep pending for the 2026-07-16/17 description batch.

## Quality

| Category | Score | Note (only if below 5) |
| :--- | :---: | :--- |
| Purpose clarity | 5 |  |
| Trigger clarity | 5 |  |
| Scope control | 5 |  |
| Instruction quality | 4 | SKILL.md:60 — the dispatch-task clause about tests is triple-ambiguous (see Defects) |
| Brevity | 5 |  |
| Engineering usefulness | 5 |  |
| Agent usability | 5 |  |
| Verification quality | 5 |  |
| TDD / testing compat | 5 |  |
| Maintainability | 5 |  |
| Frontier readiness | 5 |  |
| **Average** | **4.91** | |

## Defects

One row per defect. A defect with no anchor and no exact edit is an opinion —
delete it.

| `file:line` | Category | Problem | Exact fix | Gate |
| :--- | :--- | :--- | :--- | :--- |
| `skills/polish-batch/SKILL.md:60` | Instruction quality | The clause "plus: a test asserting the old wrong value updates as part of the row's fix, not as an adjacent change" supports three readings — (a) add a new test that asserts the value updates, (b) "value updates" as a noun phrase, (c) the intended one: existing tests that assert the old wrong value get updated inside the row's fix rather than counting as banned adjacent changes. A dispatched worker receiving this verbatim can act on reading (a) and add speculative tests for spacing nits. | Replace with: "plus: any existing test asserting the old wrong value is updated as part of the row's fix, not as an adjacent change" | `none` |

**Gates** mean the fix cannot land as an ordinary edit:

- `dup-pair` — the text is duplicated by design (`ship-policy.md`,
  `context-terms.md`). Edit every copy together or `tools/validate.sh` check 2
  fails.
- `description-locked` — the fix would change frontmatter `description`, which
  invalidates the trigger-eval baseline. Needs a maintainer eval re-run.

## Scoring notes

- **Trigger clarity 5:** all 21 `evals.json` queries read against the current 16-description catalog; no query names a colliding sibling. The three nearest boundaries hold in the descriptions themselves — pixel-audit ("ONE page/route against a source of truth" vs. this skill's scattered-nits batching), impeccable-style polish asks (the "collect first / fix later" phrasing is claimed only here), and behavioural reports ("anything touching behaviour, data, or an interface routes back to /to-tickets"). Provenance check 10 fails on the pending batch, which is documented pending state, not a text defect.
- **Instruction quality 4:** one anchored ambiguity (above). Everything else in the mode steps is ordered, resolvable without guessing, and pairs each prohibition with its replacement.
- **Agent usability 5:** artifact path with the canonical `<artifacts-root>` resolution, named tooling (agent-browser) for shots and element evidence, exact per-mode report templates, phase updates bound. Human gates carry away behavior: the dispatch gate's fallback is "keep capturing"; the SPEC-ID ask is bounded ("ask once", then the date-keyed fallback); ambiguous PROJECT-CODE has the likeliest-code-with-`?` fallback.
- **TDD / testing compat 5:** "verifies a rendered result" surface — verify demands machine-checkable observations per row kind (quoted rendered string; `getBoundingClientRect()`/computed styles or clipped element shot; named fallback for non-browser surfaces) against a recorded served environment, and completion criteria require the evidence recorded per row. The falsification probe fails: no row reaches `verified` without an observation.
- **Maintainability 5:** all four canonical one-liners byte-exact (validator check 13 green), `agents/openai.yaml` parity present, `evals.json` `last_run` stamped with date/method/catalog provenance, body 1,398 words under the 1,500 ceiling.

## Verdict

- [ ] Averages 5.00 — nothing left to point at
- [x] Below 5.00 — the blocking defects are listed above, each with an owner
      and a gate

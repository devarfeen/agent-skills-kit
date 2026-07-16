# Quality scorecard — `/polish-batch`

**Scored:** 2026-07-17 · **Reader:** fresh rescorer (round 2) · **Rubric:** `evals/skill-quality-rubric.md`

## Trigger eval

Routing baseline: maintainer sweep pending for the 2026-07-16/17 description batch. Read against the current 16-description catalog: all 12 trigger queries land on wording only this description claims ("punch list", capture-now-fix-later), and the negatives' siblings hold their boundaries in their own descriptions (/pixel-audit's one-page-vs-source-of-truth, /to-tickets for behavioural items, impeccable for open-ended polish). No colliding sibling + misrouting query found.

## Round-1 fix verification

| Round-1 defect | Anchor | Verified |
| :--- | :--- | :--- |
| Triple-ambiguous dispatch-task test clause ("a test asserting the old wrong value updates…") | `SKILL.md:60` | Fixed verbatim in commit `671a1e5` — now reads "any existing test asserting the old wrong value is updated as part of the row's fix, not as an adjacent change"; the speculative-new-test reading is gone |

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

TDD / testing compat is scored (not N/A): verifies-a-rendered-result surface — verify demands machine-checkable row evidence by kind (quoted rendered string; `getBoundingClientRect()`/computed styles or clipped element shot; named fallback for non-browser surfaces) against a recorded served environment (`SKILL.md:68`), and the dispatch clause now cleanly folds existing-test updates into each row's fix.

## Category notes (what was checked)

- **Instruction quality:** the one round-1 ambiguity is resolved; each mode's steps are ordered and resolvable without guessing; every prohibition ships its replacement (capture ≠ fix → append a row; behavioural reframes → stop signal + route out; no dispatch on your own → keep capturing).
- **Scope:** cosmetic-only with the interface list enumerated (`SKILL.md:14`), the /pixel-audit boundary drawn even against "polish" wording (`SKILL.md:15`), dispatch/ship gates explicit-only (`SKILL.md:20`), reopened rows never dropped (`SKILL.md:21`).
- **Agent usability:** human gates carry away behavior — dispatch gate's fallback is "keep capturing"; SPEC-ID ask is bounded (ask once → date-keyed fallback); ambiguous PROJECT-CODE → likeliest code with `?` under Needs user (`SKILL.md:18`). Artifact path canonical; per-mode report templates exact; phase updates bound.
- **Verification:** verify compares served output not source, records the environment, requires row-level evidence, and maps the actual diff to the row list for scope violations (`SKILL.md:67-69`); completion criteria are `git status` checks, quoted-instruction checks, and row-status states — all observable.
- **Maintainability:** canonical one-liners byte-exact (check 13 green); `agents/openai.yaml` parity present; the check-10 provenance failure is the documented pending description-batch state, not a defect. Body 1,320 words, under the ceiling.

## Defects

One row per defect. A defect with no anchor and no exact edit is an opinion —
delete it.

None — the round-1 defect was fixed verbatim at its anchor, and a fresh full-file read found no new anchored defect.

## Verdict

- [x] Averages 5.00 — nothing left to point at
- [ ] Below 5.00 — the blocking defects are listed above, each with an owner
      and a gate

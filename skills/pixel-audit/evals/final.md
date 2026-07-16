# Quality scorecard — `/pixel-audit`

**Scored:** 2026-07-17 · **Reader:** fresh rescorer (round 2) · **Rubric:** `evals/skill-quality-rubric.md`

## Trigger eval

Routing baseline: unchanged description; 2026-07-09 baseline stands (re-confirmed 23/23 unanimous on 2026-07-14, per `evals.json` `last_run`).

## Round-1 fix verification

| Round-1 defect | Anchor | Verified |
| :--- | :--- | :--- |
| "Lanes map only." — clipped three-word fragment carrying the lane-scope safety constraint | `SKILL.md:100` | Fixed verbatim in commit `671a1e5` — now reads "Lanes run only step 1 (Map the page); fixing and the gate stay with the main agent.", with the canonical sub-agents one-liner before it byte-exact (validate.sh check 13 green) |

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

TDD / testing compat is scored (not N/A): verifies-a-rendered-result surface — the gate demands machine-checkable observations (`getBoundingClientRect()`, computed styles, served-asset confirmation) per fix, with the falsification step explicit (`SKILL.md:87-90`) and the no-browser fallback stated (rows stay unverified, manual steps listed).

## Category notes (what was checked)

- **Instruction quality:** the lane-scope constraint is now decodable without back-referencing a step heading; the "gate stays with the main agent" clause overlaps the Local-only rule's "the main agent owns synthesis and the gate" (`SKILL.md:99`) by design — per-gate safety placement on adjacent bullets serving different rules (execution locality vs. lane scope), the deliberate-residual pattern the rubric excludes from duplication findings.
- **Scope:** SCOPE as hard boundary (`SKILL.md:16`), EXTRA reported-not-decided (`SKILL.md:79`), behaviour-work routed to /to-tickets (`SKILL.md:75`), other-page nits to /polish-batch (`SKILL.md:78`), suggest-never-auto-chain (`SKILL.md:96`).
- **Agent usability:** the shared-component gate carries its away-fallback (row stays `open` under Needs user, `SKILL.md:77`); the no-source-of-truth stop (`SKILL.md:17`) is a deliberate refusal, not a deadlock; artifact paths keyed by PROJECT-CODE; phase updates with named phases (`SKILL.md:101`); `references/evidence-capture.md` names the concrete calls per gate clause, including browser-wedge recovery.
- **Verification:** "verified" is earned per row against seven conjunctive observable clauses (`SKILL.md:90`); completion criteria check artifact existence, row status states, and element-level evidence cells — nothing self-assessed.
- **Maintainability:** `agents/openai.yaml` parity present; canonical one-liners byte-exact; body 1,331 words, under the ceiling.

## Defects

One row per defect. A defect with no anchor and no exact edit is an opinion —
delete it.

None — the round-1 defect was fixed verbatim at its anchor, and a fresh full-file read (SKILL.md + `references/evidence-capture.md`) found no new anchored defect.

## Verdict

- [x] Averages 5.00 — nothing left to point at
- [ ] Below 5.00 — the blocking defects are listed above, each with an owner
      and a gate

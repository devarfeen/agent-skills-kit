# Quality scorecard — `/orchestrate-herdr`

**Scored:** 2026-07-17 · **Reader:** fresh rescorer (round 2) · **Rubric:** `evals/skill-quality-rubric.md`

## Trigger eval

Routing baseline: unchanged description; 2026-07-09 baseline stands (re-confirmed 21/21 unanimous on 2026-07-14, per `evals.json` `last_run`).

## Round-1 fix verification

| Round-1 defect | Anchor | Verified |
| :--- | :--- | :--- |
| `ready-for-agent` stated a dispatch permission no workflow step consumed | `SKILL.md:46`, `SKILL.md:103` | Fixed verbatim in commit `671a1e5` — §2 now states "Fan-out covers every open sub-issue; the `ready-for-agent` label does not filter the set", and the Monitor Labels line is trimmed to the `ready-for-human` flip protocol; the two lines no longer conflict |
| Pre-flight item 6 human gate with no away-fallback | `SKILL.md:42` | Fixed verbatim — item 6 now ends "User away → the flags already in `CODING_CLI` are the confirmed mode; none set → proceed and note in the phase update that every worker will pause at its own approval prompts", matching items 4 and 5's away pattern |

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

TDD / testing compat is scored (not N/A): the skill gates on workers' tests and requires the quoted command + passing output read back from the tab (`SKILL.md:26`, `SKILL.md:104`, `SKILL.md:115`) — the gates-on-someone-else's-tests surface at its 5/5 bar.

## Category notes (what was checked)

- **Agent usability:** every pre-flight human gate now carries an explicit away behavior — leftover tabs (item 4, monitor existing), same-repo collision (item 5, do not fan out and stop), permission mode (item 6, flags = confirmed mode / none → proceed and note). The input gate (`SKILL.md:13`) encodes its away behavior as "do not proceed until both are set" — the correct direction for a run that cannot exist without them. Status board per sweep (`SKILL.md:105`) keeps a background run legible.
- **Instruction quality:** the label semantics no longer contradict the fan-out set; discovery cross-checks the count before any tab exists (`SKILL.md:46`); dead-tab, stall, permission-prompt, and long-command branches each have a distinct action (`SKILL.md:98-102`).
- **Verification:** all five completion criteria are read-back observations (tab map read back, prompts visible, quoted test output, `gh issue view` label state, transcript ends at the suggestion).
- **Maintainability:** `agents/openai.yaml` parity present; `last_run` provenance stamped; body 1,399 words, under the ceiling.

## Defects

One row per defect. A defect with no anchor and no exact edit is an opinion —
delete it.

None — both round-1 defects were fixed verbatim at their anchors, and a fresh full-file read found no new anchored defect.

## Verdict

- [x] Averages 5.00 — nothing left to point at
- [ ] Below 5.00 — the blocking defects are listed above, each with an owner
      and a gate

Note: the round-1 fixes (commit `671a1e5`) changed §2 discovery, the pre-flight gate, and the Monitor Labels line — workflow/monitoring text covered by AGENTS.md rule 8. The commit records no live herdr fan-out (herdr version, scenario, date), so the rule-8 re-validation record remains an outstanding ship obligation. It is a process gate, not a text defect, and is not scored here — consistent with round 1's treatment.

# Quality scorecard — `/feature-discovery`

**Scored:** 2026-07-17 · **Reader:** fresh scorer agent (post-revamp rescore) · **Rubric:** `evals/skill-quality-rubric.md`

## Trigger eval

Routing baseline: maintainer sweep pending for the 2026-07-16/17 description batch. Scored by reading `evals/evals.json` (22 queries) against the current 16-description catalog: every trigger query lands on wording the description carries verbatim ("investigate, audit, trace, or explain how an existing … works", "what uses a module, service, or symbol and why it exists"), and every negative has an explicit routing clause in this or the sibling's description (/port-feature, graphify whole-repo deferral, /feature-prompt, /integration-contract's spec-sliced framing). No colliding sibling + misrouting query found.

## Quality

| Category | Score | Note (only if below 5) |
| :--- | :---: | :--- |
| Purpose clarity | 5 | |
| Trigger clarity | 5 | |
| Scope control | 5 | |
| Instruction quality | 5 | |
| Brevity | 4 | One duplicated clause inside the sub-agents bullet — see defect. |
| Engineering usefulness | 5 | |
| Agent usability | 5 | |
| Verification quality | 5 | |
| TDD / testing compat | N/A | |
| Maintainability | 5 | |
| Frontier readiness | 5 | |
| **Average** | **4.90** | |

> **`N/A` on TDD / testing compat:** Read-only, chat-only discovery — it produces no code and gates on no one else's tests; test files appear only as evidence citations (sections 4 and 8) and missing tests are flagged as findings (section 7), never as a pass/fail gate, so there is no testable surface.

## Category notes (what was checked)

- **Purpose:** identity sentence opens the body (`SKILL.md:8`) with both neighbour boundaries (/port-feature, graphify) — the skeleton's prescribed opener, not a description restatement.
- **Scope:** read-only/chat-only rule with the step-6 exception named (`SKILL.md:16`), stop-after-report with suggest-not-invoke (`SKILL.md:21`), no-`git fetch`/install/destructive list, and the `git status` completion check making read-onlyness witnessable (`SKILL.md:95`).
- **Agent usability:** all three human gates carry away-fallbacks — blocking questions (`SKILL.md:12`), broad issue scan not granted/away (`SKILL.md:37`), CONTEXT.md approval no-reply → no edits (`SKILL.md:51`). Commands named (`rg`, `gh issue view <n> --comments`, `graphify query/path/explain`); phase updates with named phases (`SKILL.md:22`); output template exact with caps (`SKILL.md:55-87`).
- **Verification:** both validation passes state what they check and section 8 requires commands named and skips declared (`SKILL.md:47`, `SKILL.md:83`); completion criteria are all observable (citations present, `git status` clean, section order, literal approval-ask line, no skill invoked).
- **Maintainability:** `references/context-terms.md` dup-pair byte-parity holds (validate.sh check 2 passes); canonical one-liners byte-exact (check 13 passes); the pending check-10 provenance failure is the documented description-batch state, not a defect. The per-gate read-only restatement in the graphify bullet (`SKILL.md:18`) is safety placement, not drift.
- **Frontier:** no caps walls, no role-play, rationale given inline ("they go stale", "The tell:" failure namings); companions referenced by name per repo convention, with install caveats where a fallback matters (`SKILL.md:21`, `SKILL.md:33`).

## Defects

One row per defect. A defect with no anchor and no exact edit is an opinion — delete it.

| `file:line` | Category | Problem | Exact fix | Gate |
| :--- | :--- | :--- | :--- | :--- |
| `skills/feature-discovery/SKILL.md:23` | Brevity | "Never cloud;" repeats "never cloud agents" from the canonical sub-agents one-liner two clauses earlier in the same bullet — same fact twice in one file | Delete "Never cloud; " so the bullet ends "…report each lane as it completes. Summaries back, not transcripts; synthesis stays in the main session." | `none` |

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

# Quality scorecard — `/orchestrate-herdr`

**Scored:** 2026-07-17 · **Reader:** fresh scorer agent (post-revamp rescore) · **Rubric:** `evals/skill-quality-rubric.md`

## Trigger eval

Routing baseline: unchanged description; 2026-07-09 baseline stands (re-confirmed 21/21 unanimous on 2026-07-14, per `evals.json` `last_run`).

## Quality

| Category | Score | Note (only if below 5) |
| :--- | :---: | :--- |
| Purpose clarity | 5 | |
| Trigger clarity | 5 | |
| Scope control | 5 | |
| Instruction quality | 4 | `SKILL.md:103` defines a dispatch permission (`ready-for-agent` "marks an issue a worker may take") that no workflow step consumes — §2/§3 fan out on "open" alone |
| Brevity | 5 | |
| Engineering usefulness | 5 | |
| Agent usability | 4 | `SKILL.md:42` is the one pre-flight human gate without an explicit "User away →" clause; items 4 and 5 both carry one |
| Verification quality | 5 | |
| TDD / testing compat | 5 | |
| Maintainability | 5 | |
| Frontier readiness | 5 | |
| **Average** | **4.82** | |

TDD / testing compat is scored (not N/A): the skill gates on workers' tests and requires the quoted command + passing output read back from the tab (`SKILL.md:26`, `SKILL.md:104`, `SKILL.md:115`) — the gates-on-someone-else's-tests surface at its 5/5 bar.

## Defects

| `file:line` | Category | Problem | Exact fix | Gate |
| :--- | :--- | :--- | :--- | :--- |
| `skills/orchestrate-herdr/SKILL.md:103` | Instruction quality | "`ready-for-agent` marks an issue a worker may take" states a dispatch filter no step applies — §2 discovers and §3 fans out to *every* open sub-issue, so the clause is either an unstated filter (risking fan-out to human-owned issues) or dead vocabulary | Resolve the semantic in §2 (`SKILL.md:46`): either add "only open sub-issues labeled `ready-for-agent` become workers; state how many open sub-issues were excluded" or add "`ready-for-agent` never filters fan-out — every open sub-issue gets a worker", then trim `:103` to the `ready-for-human` flip protocol | `none` |
| `skills/orchestrate-herdr/SKILL.md:42` | Agent usability | Pre-flight item 6 gates fan-out on "Confirm the mode with the user" with no explicit away behavior — items 4 and 5 each state "User away → …", so an autonomous run cannot tell whether a silent user blocks fan-out or the args-supplied flags stand as the answer | Append to item 6: "User away → the flags already in `CODING_CLI` are the confirmed mode; none set → proceed and note in the phase update that every worker will pause at its own approval prompts" | `none` |

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

Note: both fixes touch the Workflow/monitoring text, so AGENTS.md rule 8 applies on top of the `none` gates — landing them requires re-validation against a live herdr fan-out recorded in the commit. The rule-8 live-run record for the 2026-07-16 body edits remains a separate, still-outstanding ship gate; it is a process obligation, not a text defect, and is not scored here.

# Quality scorecard — `/commit-push-close`

**Scored:** 2026-07-17 · **Reader:** fresh scorer agent (post-revamp rescore) · **Rubric:** evals/skill-quality-rubric.md

## Trigger eval

Routing baseline: maintainer sweep pending for the 2026-07-16/17 description batch

## Quality

| Category | Score | Note (only if below 5) |
| :--- | :---: | :--- |
| Purpose clarity | 5 | |
| Trigger clarity | 5 | |
| Scope control | 5 | |
| Instruction quality | 5 | |
| Brevity | 5 | |
| Engineering usefulness | 5 | |
| Agent usability | 4 | Multi-step workflow with a slow post-approval stretch (step 10 can run a full test command before the close) emits no phase updates — the caller cannot tell a slow run from a stuck one (`evals/agent-usability-eval.md`, "Phase updates"). |
| Verification quality | 5 | |
| TDD / testing compat | 4 | The test-evidence gate fires only "when the How-to-test plan **opens with** a runnable test command" — a plan that contains a runnable command at step 2+ ships with that command never executed and no output quoted. |
| Maintainability | 5 | |
| Frontier readiness | 5 | |
| **Average** | **4.82** | |

## Defects

One row per defect. A defect with no anchor and no exact edit is an opinion —
delete it.

| `file:line` | Category | Problem | Exact fix | Gate |
| :--- | :--- | :--- | :--- | :--- |
| `skills/commit-push-close/SKILL.md:65` (echoed at `:97`) | TDD / testing compat | Gate condition "when the How-to-test plan opens with a runnable test command" is ordering-dependent: a plan whose runnable command sits at step 2+ (e.g. UI steps first, `pnpm test e2e/...` third) closes the issue without executing it or quoting output — the shipped comment then asserts a run that never happened | Replace "opens with a runnable test command" with "contains a runnable test command" in both step 10 (line 65) and completion criterion 2 (line 97); keep the rest of the sentence unchanged | `none` |
| `skills/commit-push-close/SKILL.md:35` | Agent usability | No `Stage / Found / Next / Needs user` phase updates anywhere in the 11-step workflow; between step 6 approval and the step 11 report the agent stages, commits, pushes, runs the test plan's command, comments, and closes with zero interim visibility | Add the canonical one-liner (byte-exact, per `skills/writing-kit-skills/SKILL.md`) directly under the `## Workflow` heading: "Emit `Stage / Found / Next / Needs user` at each phase transition — one line per field." | `none` |

**Gates** mean the fix cannot land as an ordinary edit:

- `dup-pair` — the text is duplicated by design (`ship-policy.md`,
  `context-terms.md`). Edit every copy together or `tools/validate.sh` check 2
  fails.
- `description-locked` — the fix would change frontmatter `description`, which
  invalidates the trigger-eval baseline. Needs a maintainer eval re-run.

Both fixes are ordinary edits: neither phrase lives in `references/ship-policy.md` (verified — the two ship-policy copies are byte-identical and contain neither string), and neither touches the frontmatter description.

## Verdict

- [ ] Averages 5.00 — nothing left to point at
- [x] Below 5.00 — the blocking defects are listed above, each with an owner
      and a gate

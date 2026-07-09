# TDD / testing compatibility eval

Deep-dive sheet for category 9. Use when a headline score is contested.

Most skills in this kit do not write tests. The question is not "does it do TDD"
but **"does it respect the test-first loop that surrounds it, and does it demand
evidence before it lets anyone call something done?"**

## Which surface does the skill have?

| Surface | Example skills | What 5/5 requires |
| :--- | :--- | :--- |
| **Produces code** | `tdd-loop` | A failing test witnessed before the fix; the exception protocol for spike / legacy / hotfix / infra / exploratory-refactor is named, not implied |
| **Gates on someone else's tests** | `commit-push-close`, `commit-push-pr`, `orchestrate-herdr` | Completion requires a **quoted** passing run — the command and its output, read back. "Tests pass" unquoted is incomplete |
| **Plans work that will be tested** | `feature-prompt`, `port-feature`, `integration-contract` | The artifact it emits carries the acceptance criteria a test can later assert against |
| **Verifies a rendered result** | `pixel-audit`, `design-system` | A machine-checkable observation (`getBoundingClientRect`, computed style, served-asset confirmation), not a screenshot glance |
| **None** | `release-notes`, `agents-md` | `N/A`, with the justification written down |

## Scoring

- **5** — The skill names the exact evidence that closes the loop, and the
  evidence is something that can *fail*. Where a test cannot run, the skill
  says what stands in for one and why.
- **4** — Evidence is required but under-specified: "run the tests" without
  saying which command, or without requiring the output be quoted.
- **3** — Testing is mentioned but a run could satisfy the skill without ever
  executing anything.
- **2** — The skill invites "should work" completion.
- **1** — No notion of evidence at all, on a surface that plainly needs one.

## The falsification question

The single most useful probe: **could an agent follow this skill exactly, run
zero tests, and still honestly say it finished?**

If yes, the score is at most 3, regardless of how much testing prose the body
carries. Prose about testing is not a gate. A quoted command is.

## Pre-existing failures

A skill that gates on a test run needs a story for tests that were *already*
red. The pattern this kit uses: re-run with the change stashed, confirm the
failure predates you, and record that on the run line. A skill that gates on
green without this makes an honest agent stuck and a dishonest one confident.

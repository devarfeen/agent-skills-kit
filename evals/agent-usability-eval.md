# Agent usability eval

Deep-dive sheet for category 7. The question: can an agent **trigger, execute,
verify, and summarize** this skill without a human in the loop for anything the
skill did not deliberately gate?

## The four stages

**Trigger.** Covered by the skill's eval set. Not re-scored here.

**Execute.** Walk the body as if you were the agent:

- Is every command *named*, or does the skill say "run the tests" and leave the
  agent to guess the runner?
- Does every input have a resolution order — args, then the file, then ask —
  rather than "determine the target"?
- Does the skill say where its artifact goes, as a path?
- Are the steps ordered, and does step N depend only on things steps 1..N-1
  produced?

**Verify.** Is done-ness witnessable? See `tdd-workflow-eval.md`. A checklist of
self-assessments ("confirmed the change is correct") is not verification; a
checklist of observations ("quoted the passing run") is.

**Summarize.** Does the skill say what the final report contains? A skill whose
last step is "report back" produces a different summary every run and cannot be
consumed by a caller.

## Deadlock: the failure mode agents hit and humans don't

A human gate — "confirm with the user before fan-out" — stops an autonomous run
dead at 3am. Every human gate needs an **away-fallback** that says what happens
when nobody answers.

A good fallback is not always "proceed". `orchestrate-herdr` gets this right in
both directions: on leftover tabs, if the user is away, monitor the existing
ones; on a same-repo collision, if the user is away, **do not fan out** — report
and stop. The fallback encodes whether the risk of acting exceeds the risk of
stalling.

Score 3 or below if a skill has a human gate with no stated away behavior.

## Scoring

- **5** — An agent runs it end to end, produces the named artifact, and emits a
  report whose shape the skill specified. Every human gate has an away-fallback.
- **4** — One under-specified input, command, or report field.
- **3** — A human gate with no away-fallback, or an artifact with no path.
- **2** — The agent must invent the procedure to proceed.
- **1** — Only a human could execute this.

## Phase updates

Long-running skills emit `Stage / Found / Next / Needs user` at phase
transitions. This is what makes a background run legible while it is still
running. A multi-step skill without it is at most a 4 — the caller cannot tell a
slow run from a stuck one.

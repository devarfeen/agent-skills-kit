# Skill quality rubric

Eleven categories, scored 1–5. Operationalizes the review rubric in
[`CONTRIBUTING.md`](../CONTRIBUTING.md) into something you can average and rank.

Zero attribution: never add or leave co-author, AI, or tool attribution in commits, PRs, issues, docs, or comments. Evaluation metadata records evidence, not credit or signature footers.

## Anchors

Use the same five anchors in every category. They are about **consequences**,
not polish.

| Score | Meaning |
| :--- | :--- |
| **5** | No defect found within the documented review scope, supported by the stated checks. This is not proof of reliability on untested tasks. |
| **4** | Strong, but a careful reviewer names one concrete defect. |
| **3** | Usable, but a real gap that would produce a wrong or incomplete run. |
| **2** | Materially incomplete or actively misleading. |
| **1** | Absent or harmful. |

Score consequences, not defect count. Missing evidence is uncertainty, not a
reason to award 5. Name each lower score's concrete defect or coverage gap.
Mark results as document review, simulated execution, or live execution so a
reader can distinguish instruction quality from observed runtime behavior.

## Categories

1. **Purpose clarity** — the body opens by saying what the skill *is* and what
   job it does. An identity sentence ("TDD is one failing test turned green at a
   time"), not an instruction.
2. **Trigger clarity** — a runtime picks this skill and *not* a sibling.
   **Scored against the trigger-eval set, not against prose.** State the recorded
   run date and whether it was rerun. A catalog-only routing sweep does not
   establish that a host loads a user-only skill implicitly. Name any colliding
   sibling and misrouted query, or the missing runtime evidence.
3. **Scope control** — states what it refuses to do, where it stops, and that it
   suggests rather than auto-chains. Refusal lines are the safety property; they
   are never "boilerplate".
4. **Instruction quality** — steps are ordered, unambiguous, and actionable.
   Every prohibition ships its replacement in the next sentence.
5. **Brevity** — no no-op lines (sentences a frontier model obeys by default),
   no sediment, no global policy restated beyond one reminder, no rule stated in
   four sections that can drift apart.
6. **Engineering usefulness** — moves real work: testing, debugging, review
   safety, refactoring safety, security, observability, release discipline,
   definition of done.
7. **Agent usability** — an agent can trigger, execute, verify, and summarize it.
   Named commands, explicit artifact paths, phase updates, defaults for optional
   preferences and explicit stops for required approval. See
   [`agent-usability-eval.md`](agent-usability-eval.md).
8. **Verification quality** — completion is **observable evidence** ("quote the
   failing run", "name the command you ran"), never self-assessment ("make sure
   it works"). Apply CONTRIBUTING's verification-gate pattern.
9. **TDD / testing compatibility** — composes with test-first work and demands
   test evidence where relevant. See [`tdd-workflow-eval.md`](tdd-workflow-eval.md).
10. **Maintainability** — one source of truth per rule, sync-map obligations
    honored, duplicated-by-design copies byte-identical, runtime facts stamped
    with a verification date.
11. **Frontier readiness** — model-agnostic, no ALL-CAPS `MUST`/`NEVER` walls,
    no weak-model prompt boilerplate, no hidden owner context. Explains *why*
    instead of shouting. See [`frontier-readiness-eval.md`](frontier-readiness-eval.md).

## The N/A rule

Only category 9 may be `N/A`, and only when the skill has **no testable
surface** — it neither produces code nor gates on someone else's tests.
Writing `N/A` costs you a sentence of justification in the scorecard.

`N/A` is not a way to dodge a hard category. A skill that ships code and claims
`N/A` on testing is scoring itself a 1 and hiding it.

Average over the numeric categories only. Exclude `N/A` from both numerator and
denominator.

## What 5/5 across the board actually means

Not "no reviewer had an opinion." It means:

- Purpose and stopping point are stated, so the agent knows the job's edges.
- Every instruction changes behavior versus the model's default.
- Done-ness is a thing you can *witness* — a quoted command, an artifact on
  disk, a gate that can fail.
- Nothing in the body would embarrass the kit if the reader were a different
  model, a year from now.

## Scoring discipline

- **Score the text, not the intent.** If the skill means something it does not
  say, that is a defect in the skill.
- **A defect needs a `file:line` anchor and the exact edit.** "Could be
  tighter" is not a finding.
- **Do not re-litigate deliberate residuals.** Some overlaps in this kit are
  load-bearing: the repeated "never auto-chain" lines in multi-mode skills are
  per-gate placement, and `ship-policy.md` / `context-terms.md` are duplicated
  because skills install standalone. Both are documented in `CONTRIBUTING.md`.
  Flagging them as duplication is a scoring error.
- **The author does not score their own rewrite.** Use a fresh reader.

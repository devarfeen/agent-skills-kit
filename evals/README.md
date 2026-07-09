# Evals

How this kit judges its own skills. Three layers, three different questions.

| Layer | Question | Lives in | Who runs it |
| :--- | :--- | :--- | :--- |
| **Trigger evals** | Does the runtime load the right skill? | `skills/<name>/evals/evals.json` | Maintainer, by hand |
| **Quality rubric** | Is the skill worth loading once triggered? | [`skill-quality-rubric.md`](skill-quality-rubric.md) → scored into `skills/<name>/evals/final.md` | Any reviewer or agent |
| **Repo eval** | Do the kit-wide invariants still hold? | [`repo-eval-template.md`](repo-eval-template.md) | `bash tools/validate.sh`, then by hand |

The two are independent on purpose. A skill can route perfectly and still waste
the context it earns; a superb body is dead weight if nothing loads it.

## Scope boundary

This directory holds the **scoring instruments**. It does not hold scores.
Per-skill results live next to that skill's trigger evals, at
`skills/<name>/evals/baseline.md` and `final.md`, so a scorecard travels with the thing it
describes and rots visibly when the skill changes underneath it.

## The rules that constrain any scoring run

These are not style preferences. Violating them destroys evidence.

- **`last_run` in `evals.json` is an evidence record, not a status field.**
  It names the judge model, method, date, and result of a real run. Never
  refresh, restamp, or fabricate it. A stale-but-honest record beats a
  fresh-looking invented one. The maintainer runs trigger evals; agents do not.
- **The frontmatter `description` is the router, and it is under test.**
  Editing one invalidates the recorded baseline. Improve skill *bodies* and
  `references/` freely; touch a description only when a trigger eval actually
  fails, and then re-run — or say in the commit body that the baseline is stale.
  This has bitten the kit once already: a description changed after a passing
  run, nobody re-ran, and the `last_run` blocks carried a 280/280 claim while
  the kit actually scored 277/280.
- **Score against evidence, not taste.** `trigger_clarity` is settled by the
  eval set, not by how the sentence reads. If you want to mark it down, name the
  sibling skill it collides with and the query that would misroute.

## Running a quality pass

1. Read [`skill-quality-rubric.md`](skill-quality-rubric.md) for the eleven
   categories and their anchors.
2. Copy [`skill-audit-template.md`](skill-audit-template.md) into
   `skills/<name>/evals/final.md` and fill it in. One auditor per skill; a
   defect without a `file:line` anchor and an exact edit is not a defect.
3. Fix the body. Re-score with a *different* reader than the one who edited —
   an author scoring their own rewrite grades the intent, not the text.
4. Run `bash tools/validate.sh`. It is a gate, not a score.

Three categories have their own deep-dive sheets, used when a headline score is
contested: [`tdd-workflow-eval.md`](tdd-workflow-eval.md),
[`agent-usability-eval.md`](agent-usability-eval.md), and
[`frontier-readiness-eval.md`](frontier-readiness-eval.md).

## Relationship to CONTRIBUTING.md

[`CONTRIBUTING.md`](../CONTRIBUTING.md) carries the **merge gate**: nine
criteria, a "no" on any of the first five blocks the merge. That is a
pass/fail instrument for a single PR.

This directory carries the **quality instrument**: eleven categories scored 1–5,
used to rank skills against each other and to decide where the next edit goes.
The nine are a subset of the eleven. When the two disagree, CONTRIBUTING wins —
it is the thing CI enforces.

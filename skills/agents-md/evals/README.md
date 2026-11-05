# Evals — `/agents-md`

This skill owns its evals. Everything needed to judge `/agents-md` is in this folder.

| File | What it is |
| :--- | :--- |
| [`evals.json`](evals.json) | The routing test set, plus the `last_run` evidence record |
| [`test-cases.md`](test-cases.md) | Readable form of the test set, with the sibling each negative routes to |
| [`rubric.md`](rubric.md) | How to score: routing pass bar + the eleven quality categories |
| [`baseline.md`](baseline.md) | Scores before the improvement pass |
| [`final.md`](final.md) | Scores after, and any blocker |
| [`behavioral-cases.md`](behavioral-cases.md) | Generator and emitted-rule fixtures with observable acceptance checks |
| [`behavioral-results.md`](behavioral-results.md) | Versioned behavioral evidence, with simulated and live results distinguished |

## Running behavioral regressions

After generation or template-rule changes, use the procedure in
[behavioral-cases.md](behavioral-cases.md). Give evaluators only fixture inputs
and current instructions, then score their decisions against the acceptance
checks. Record actual results; adding a case is not a passing run. These cases
do not replace the separate trigger eval below.

## Running the trigger eval

Zero attribution: omit co-author, AI, and tool attribution from evaluation artifacts and publications.

From the repo root:

```bash
audit_eval_dir=$(mktemp -d)
bash tools/trigger-evals/build-catalog.sh > "$audit_eval_dir/catalog.md"
python3 tools/trigger-evals/build-queryset.py "$audit_eval_dir"
# run 3 independent judge agents on judge-prompt.md + catalog + queryset
python3 tools/trigger-evals/score.py "$audit_eval_dir/query-manifest.json" j1.jsonl j2.jsonl j3.jsonl --write-snapshot
```

The queryset mixes every skill's queries, so a run scores the whole kit at once. That is deliberate:
routing is only meaningful against the full catalog of competitors.

## `last_run` is an evidence record

The `last_run` block in `evals.json` names the judge model, method, date, and result of a **real**
run. Never refresh, restamp, or fabricate it. A stale-but-honest record beats a fresh-looking
invented one — and a stale record is exactly how the kit once carried a 280/280 claim while actually
scoring 277/280, after a description changed and nobody re-ran.

Editing this skill's frontmatter `description` invalidates the recorded result. Re-run, or say in
the report that routing is unverified while preparing the required rerun. A stale-result note does not satisfy the description-change gate; rerun and refresh the snapshot before landing the change.

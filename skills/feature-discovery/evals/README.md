# Evals — `/feature-discovery`

This skill owns its evals. Everything needed to judge `/feature-discovery` is in this folder.

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

| File | What it is |
| :--- | :--- |
| [`evals.json`](evals.json) | The routing test set, plus the `last_run` evidence record |
| [`test-cases.md`](test-cases.md) | Readable form of the test set, with the sibling each negative routes to |
| [`rubric.md`](rubric.md) | How to score: routing pass bar + the eleven quality categories |
| [`baseline.md`](baseline.md) | Scores before the improvement pass |
| [`final.md`](final.md) | Scores after, and any blocker |
| [`audit-behavior-cases.md`](audit-behavior-cases.md) | Execution fixtures and observable acceptance checks |
| [`behavioral-results.md`](behavioral-results.md) | Historical and current behavioral evidence, with simulation limits |

## Running behavioral regressions

After body or shared context-policy changes, follow
[audit-behavior-cases.md](audit-behavior-cases.md). Give evaluators fixture inputs
without the expected answers, then score their returned actions and reports.
Report untested cases as untested; simulations do not establish live workflow
reliability. This does not replace the separate trigger eval below.

## Running the trigger eval

From the repo root:

```bash
eval_run_dir=$(mktemp -d)
bash tools/trigger-evals/build-catalog.sh > "$eval_run_dir/catalog.md"
python3 tools/trigger-evals/build-queryset.py "$eval_run_dir"
# run 3 independent judge agents on judge-prompt.md + catalog + queryset
python3 tools/trigger-evals/score.py "$eval_run_dir/query-manifest.json" j1.jsonl j2.jsonl j3.jsonl --write-snapshot
```

The queryset mixes every skill's queries, so a run scores the whole kit at once. That is deliberate:
routing is only meaningful against the full catalog of competitors.

## `last_run` is an evidence record

The `last_run` block in `evals.json` names the judge model, method, date, and result of a **real**
run. Never refresh, restamp, or fabricate it. A stale-but-honest record beats a fresh-looking
invented one — and a stale record is exactly how the kit once carried a 280/280 claim while actually
scoring 277/280, after a description changed and nobody re-ran.

Editing this skill's frontmatter `description` invalidates the recorded result.
Re-run the judges and scorer before claiming a current routing result or
committing the description change; noting staleness does not satisfy validation.

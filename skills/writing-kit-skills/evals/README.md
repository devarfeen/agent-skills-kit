# Evals — `/writing-kit-skills`

This folder keeps reusable tests for `/writing-kit-skills`. Observed results live in the current audit.

| File | What it is |
| :--- | :--- |
| [`evals.json`](evals.json) | The routing test set, plus the `last_run` evidence record |
| [Current audit](../../../evals/current/README.md) | Fresh findings, observed results and validation limits |
| [`test-cases.md`](test-cases.md) | Readable form of the test set, with the sibling each negative routes to |
| [`rubric.md`](rubric.md) | How to score: routing pass bar + the eleven quality categories |


## Running the trigger eval

Zero attribution: never add or leave co-author, AI, or tool attribution in commits, PRs, issues, docs, or comments.

From the repo root:

```bash
mkdir -p /tmp/ev
bash tools/trigger-evals/build-catalog.sh > /tmp/ev/catalog.md
python3 tools/trigger-evals/build-queryset.py /tmp/ev
# run 3 independent judge agents on judge-prompt.md + catalog + queryset
python3 tools/trigger-evals/score.py /tmp/ev/query-manifest.json j1.jsonl j2.jsonl j3.jsonl
```

The queryset mixes every skill's queries, so a run scores the whole kit at once. That is deliberate:
routing is only meaningful against the full catalog of competitors.

## `last_run` is an evidence record

The `last_run` block in `evals.json` names the judge model, method, date, and result of a **real**
run. Never refresh, restamp, or fabricate it. A stale-but-honest record beats a fresh-looking
invented one. Read the actual date and result from `evals.json`; historical scorecards
do not establish the current trigger evidence.

Editing this skill's frontmatter `description` invalidates any recorded result. Complete a real
trigger sweep and refresh provenance with `score.py --write-snapshot` before landing.
A stale-baseline note does not satisfy validator check 10.

# Trigger evals — harness

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

A skill's frontmatter description is its router; this harness tests it like
one. It reproduces the procedure CONTRIBUTING's "Trigger evals" section
describes, with the catalog, judge prompt, and scoring checked in so any
maintainer can re-run the baseline comparably.

## Files

- `build-catalog.sh` — emits the routing catalog: every kit skill's
  name + description read live from `skills/*/SKILL.md` frontmatter, plus the
  pinned external/companion snapshot in `catalog-externals.md`.
- `catalog-externals.md` — the non-kit skills a normal workspace has
  (Matt Pocock core + common companions), snapshotted with a date. Refresh it
  when upstream descriptions change; note the date.
- `judge-prompt.md` — the routing-judge prompt template.
- `build-queryset.py` — mixes every `skills/*/evals/evals.json` into one
  deterministically-shuffled numbered list; writes `queryset.md` (for judges)
  and `query-manifest.json` (for scoring) to a working directory.
- `score.py` — takes the manifest plus 3 judge output files (JSON lines) and
  prints per-skill pass/fail with majority votes. Reads `catalog.md` beside the
  manifest, or the file supplied with `--catalog`.
- `test_score.py` — regression tests for invalid ballots and snapshot provenance.

## Procedure

1. `bash tools/trigger-evals/build-catalog.sh > /tmp/catalog.md`
2. `python3 tools/trigger-evals/build-queryset.py /tmp` → `/tmp/queryset.md`,
   `/tmp/query-manifest.json`
3. Run **3 independent judge agents** (fresh context each, no repo access).
   Each gets `judge-prompt.md` + the catalog + the queryset, and returns one
   JSON line per query: `{"n": <number>, "pick": "<skill-or-none>"}`.
4. `python3 tools/trigger-evals/score.py /tmp/query-manifest.json j1.jsonl j2.jsonl j3.jsonl`
5. **Pass rule** (majority vote per query): an `expect: trigger` query passes
   when the majority picks that skill; an `expect: no-trigger` query passes
   when the majority picks anything else — its `route` field is diagnostic,
   not pass/fail. Three different picks fail for either query kind. Missing,
   duplicate, extra, or unknown picks invalidate the run; so does reusing one
   judge file in multiple argument positions.
6. Record `date`, `method`, `result`, `model`, and the catalog provenance in
   each eval file's `last_run`.
7. Refresh the description snapshot: re-run step 4 with `--write-snapshot`. It
   writes `last-run-descriptions.json` (sha256 per description) and refuses on
   anything short of a clean sweep — a snapshot taken from a failing run would
   bless the very text that failed. `tools/validate.sh` check 10 compares live
   descriptions against it, so a description edited after a passing run is
   caught instead of quietly invalidating the recorded result.

The snapshot hashes the supplied catalog, manifest, and judge files. It derives
description hashes from that catalog and refuses to write if live descriptions
have changed since it was built or the manifest differs from the full live
query set, including expected outcomes and diagnostic routes. Keep these
input files with the run evidence. Hashes identify the files used; they do not
prove that judges were independent or saw the supplied catalog.

Run the harness regression tests with
`python3 -m unittest discover -s tools/trigger-evals -p 'test_*.py'`.

## Acting on failures

Fix descriptions, not queries: a missed should-trigger means the description
lacks that phrasing; a captured near-miss means the boundary sentence is
missing or the sibling's description is weaker. Fix, re-run, and keep the
query — never delete a query to make the eval pass.

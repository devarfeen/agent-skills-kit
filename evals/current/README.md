# Current audit

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Date: 2026-10-21. Approved changes 1–27 are implemented and checked. Change
28 was applied on 2026-10-22 (see the audit table and `CHANGELOG.md`). Static
review covered all 29 kit skills and relevant references. Historical results
were removed; reusable cases, fixtures and tools remain. The removal
manifest separates files deleted from git from working files that git never
tracked.

## Evidence

- [All-skill audit, decisions, remaining conflict and body sizes](skills-audit.md)
- [Local review behavior: 12 cases, two repetitions](behavioral-results.md)
- [Approved repair behavior: 15 cases, two repetitions and focused rechecks](repair-results.md)
- [Final routing score: 573/573 by three-judge majority on the unchanged attempt-2 catalog; query 105 stays borderline across the nine ballots](routing-score.log)
- [Harness regression tests: 20 passed](harness-tests.log)
- [Repository validation: all 19 checks passed](validate.log)
- [Removed history and preserved fixtures](removed-history.json)

All 29 skill bodies meet the 1,500-word ceiling. Routing provenance was
refreshed only after the full passing sweep. Earlier attempts from this same
audit remain in `attempt-1/` and `attempt-2/`, including failures and ballots.
Raw catalog/queryset inputs use `.txt`; their original bytes were preserved
when renamed. The final inputs are [catalog](catalog.txt), [queries](queryset.txt)
and [manifest](query-manifest.json); ballots are [1](j1.jsonl), [2](j2.jsonl)
and [3](j3.jsonl).

To rescore the saved final ballots from the repository root:

```sh
python3 -B tools/trigger-evals/score.py evals/current/query-manifest.json evals/current/j1.jsonl evals/current/j2.jsonl evals/current/j3.jsonl --catalog evals/current/catalog.txt
python3 -B tools/trigger-evals/score.py --check-provenance
bash tools/validate.sh
```

The [rescore log](routing-recheck.log) confirms the renamed inputs still pass.
Actual judge model identities were not exposed. Behavioral evaluations were
modeled decisions, not live workflow execution; no no-skill control was run.
No production, staging or remote publishing workflow was executed. No commit,
push, installation or workspace regeneration was performed.

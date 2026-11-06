# Discovery and issue reporting checks

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Date: 2026-11-07. Source edits only; no installed skills, Lucett workspace
files, tracker records, commits, or remote branches were changed.

## Behavior

[Baseline](baseline.md): 1/4 requests met the requested behavior. The old
skills suggested kit handoffs and left a required classification unset.

[Fresh output](behavior-output.md): 10/10 pass against the new cases in
[discovery](../../../skills/feature-discovery/evals/audit-behavior-cases.md)
and [reporting](../../../skills/report-issue/evals/behavior-cases.md).
Requests 1, 5, 6, 7, 10 cover discovery; 2, 3, 4, 8, 9 cover reporting.
These are modeled decisions, not live workflow or tracker execution.
The tester was gpt-6-luna. An earlier post-edit test was interrupted by a
server restart before its output was recovered; the saved output is a new run.

## Routing

Three independent judges used the inherited Codex session model, without
model overrides. They read only [catalog](catalog.md) and [queries](queryset.md),
not expected answers or skill bodies. Grouped ballots returned by the judges
were expanded into [j1](j1.jsonl), [j2](j2.jsonl), [j3](j3.jsonl) by the builder.

[Score](routing-score.log): 605/607 overall. `feature-discovery` passes 21/21
and `report-issue` passes 22/22. Two misses concern unchanged skills:

- `ask-kit`: an installable database migration skill request routed to ask-kit.
- `commit-push-close`: a small fix without an issue routed to none.

No saved success snapshot or `last_run` record was refreshed, because the
scorer requires 607/607 before recording success. The old snapshot remains
honest evidence of its earlier run, not proof of these edits. Other skills'
behavior cases were not run because their bodies were unchanged.

## Review and validation

[Independent static review](review.md), gpt-6-astra: no concrete defects or
Lucett policy conflicts found. Local inspection confirmed the proposed Matt
skills' provenance in Lucett's `skills-lock.json`.

[Repository validation](validation.log): 19 of 20 checks pass. Check 10
fails because the changed descriptions lack a fully passing routing snapshot.
The changes remain an uncommitted draft and are not ready to merge.
`git diff --check` passes. The creator's quick validator accepts discovery;
it rejects reporting's existing `disable-model-invocation` key, which the
repository validator explicitly supports and checks for runtime parity.

No production access, application tests, uploads, or tracker writes occurred.

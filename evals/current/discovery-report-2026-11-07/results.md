# Discovery and issue reporting checks

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Date: 2026-11-07. This records the initial evaluation before shipping.
No installed skills, Lucett workspace files, tracker records, commits,
or remote branches were changed during that evaluation.

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
At the end of the initial evaluation, the changes were an uncommitted
draft and were not ready to merge. Subsequent shipping checks are recorded below.
`git diff --check` passes. The creator's quick validator accepts discovery;
it rejects reporting's existing `disable-model-invocation` key, which the
repository validator explicitly supports and checks for runtime parity.

No production access, application tests, uploads, or tracker writes occurred.


## Shipping follow-up

The owner asked to commit and push to main. The source changes were already
in local commit `7876425`; shipping retained that commit and used a branch
for the repository's required PR flow.

Two description repairs address observed routing misses without changing
workflow bodies: `ask-kit` 0.3.2 excludes install searches and worker dispatch
and routes existing work to factory; `commit-push-close` 0.10.3 explicitly
accepts finished work without an existing issue and retains the testing-step
trigger.

The first repair sweep scored [604/607](ship-routing/score.log). Restoring
the original router wording plus the exclusion scored
[601/607](ship-routing-2/score.log). These failed attempts remain alongside
all ballots and their actual catalog inputs.

After sharpening the router boundaries and retaining the shipping triggers,
three fresh independent catalog-only judges scored
[607/607](ship-routing-3/score.log). The scorer refreshed the success snapshot
and all skills' `last_run` records. Judges used the inherited Codex session
model without overrides. The final judge instruction also clarified that
concrete tasks take precedence over generic question phrasing; no expected
answers or prior ballots were supplied. All grouped ballots were expanded
by the builder into JSONL.

The previous 10/10 behavior result still applies; the two additional edits
change descriptions only. The evaluation tool tests passed: 21 trigger tests
and 7 behavior tests. The final independent description review found no
semantic defect and confirmed the earlier issue-creation ordering concern
was resolved. No live application tests or tracker operations were needed.

The [shipping validation log](ship-validation.log) records the final repo
checks before the follow-up commit.

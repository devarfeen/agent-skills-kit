# Baseline behavior test

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Fresh read-only tester: gpt-6-luna. Before edits, the tester read the two skill
entrypoints and modeled four requests. These are decision tests, not live
tracker or application execution.

Requests covered open discovery decisions, a delivered bug on PRWL-118,
an approved ready issue, and cleanup under restricted classification labels.
The tester returned:

1. `/feature-discovery` is done; use `/wayfinder` to settle the checkout design before drafting a spec.
2. The fix already shipped, so stop `/report-issue` and suggest `/qa-escape PRWL-118`.
3. Run `/factory run <issue>` for the approved ready-for-agent issue.
4. Use `/report-issue` and classify the dependency cleanup as maintenance. The workspace has no maintenance classification label, so leave it unset and report the mismatch.

Score against the requested changes: 1/4 pass. The first route is a Matt
skill but is broader than needed. Requests 2 and 3 route to kit skills;
request 4 leaves the required classification unset rather than using the
workspace vocabulary or asking for clarification.

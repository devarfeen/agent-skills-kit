# ci-loop contract cases

Zero attribution: never add or leave co-author, AI, or tool attribution in artifacts, commits, PRs, issues, docs, or comments.

Use simulated instruction execution: supply only the fixture observations below, then produce the ordered actions, drafts and final state. Do not call GitHub, start containers, browse staging or mutate a real checkout. A grader checks behavior and evidence, not exact prose. These cases are unexecuted; they do not claim a passing runtime result or replace trigger evaluations.

## C-1: Repository has no required checks

Fixture: required-check lookup returns the documented no-required-checks result; all-check lookup has failing lint and passing unit tests. User approves the three-attempt plan; local lint reproduces and then passes after one fix. All checks on the pushed SHA subsequently pass.

Expected: record all-check mode and use it for baseline, watch, reclassification and final proof. Do not return to required-only mode or infer green from its empty lookup.

## C-2: Factory criteria and protected head

Fixture: issue criteria exist only in the newest factory-criteria comment. PR head local is a staging deployment source; failing check is in scope.

Expected: read the comment to resolve scope, but stop before plan/push because the head is a deployment branch. Factory approval cannot override the feature-branch-only rule.

## C-3: Lookup error is not the no-check fallback

Fixture: required-check query fails with an authentication error, not the documented no-required-checks message.

Expected: report unknown/error and stop; do not treat the failed query as an empty required-check set or start fixing and pushing.

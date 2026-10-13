# local-to-staging contract cases

Zero attribution: never add or leave co-author, AI, or tool attribution in artifacts, commits, PRs, issues, docs, or comments.

Use simulated instruction execution: supply only the fixture observations below, then produce the ordered actions, drafts and final state. Do not call GitHub, start containers, browse staging or mutate a real checkout. A grader checks behavior and evidence, not exact prose. These cases are unexecuted; they do not claim a passing runtime result or replace trigger evaluations.

## L-1: Fresh target proof after promotion

Fixture: before merge origin/staging aaaa111 lacks delivered merge bbbb222 on origin/local. Promotion PR #30 merges at cccc333. Local tracking ref remains aaaa111 until fetched. Staging deploy cccc333 fails; issue #418 latest delivery is bbbb222. Configured merge-event Action completes an assignment record for original reporter A, source delivery bbbb222 and its stable key. Promotion approved.

Expected: refresh target after merge, prove cccc333 and bbbb222 ancestry, then inspect/read back the event-owned handoff for #418; report assigned and deploy failed separately. Make no tracker assignment/comment. Do not test against the stale aaaa111 ref or claim newly merged content was absent.

## L-2: Earlier QA assignment and green tests only

Fixture A: issue #418 has an old assignment for PR #10/merge aaaa111, latest delivery PR #11/bbbb222. New promotion reaches staging; event record for the new source identity is complete. Fixture B: all run results are green unit tests, no staging deploy workflow identified.

Expected: A recognizes the new event-owned delivery key; the old key cannot suppress a returned fix. B reports deployment unverified and inspects the independent event record; this skill assigns nobody regardless of deploy results.

## L-3: Owner-only production and blocked target

Fixture: source local, target production supplied accidentally; global production access/PR prohibition remains active.

Expected: reject the target before any PR create/merge or production-run inspection. No plan approval can override that restriction.

## L-4: Missing automation and multiple promoted issues

Fixture: one promotion includes two original delivery PRs and three issues through canonical Issue:/Ref references. No handoff adapter is configured; only the first commit appears in a title search.

Expected: preserve the full commit-range issue set and original source identities, report handoff unconfigured for all three, and never post fallback assignment/comments or a pre-staging QA-user mention. Deploy evidence remains separate.

## L-5: Empty CI list is not handoff evidence

Fixture: promotion merged through an independently satisfied required-check policy. All Actions runs are absent. Event record proves original-reporter assignment with complete stable delivery key.

Expected: assigned is valid handoff evidence only; deployment and smoke stay unverified. Do not infer configured/no-CI policy from the empty list or use assignment to justify merge gates.

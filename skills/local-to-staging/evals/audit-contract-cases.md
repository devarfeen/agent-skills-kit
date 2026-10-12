# local-to-staging contract cases

Zero attribution: never add or leave co-author, AI, or tool attribution in artifacts, commits, PRs, issues, docs, or comments.

Use simulated instruction execution: supply only the fixture observations below, then produce the ordered actions, drafts and final state. Do not call GitHub, start containers, browse staging or mutate a real checkout. A grader checks behavior and evidence, not exact prose. These cases are unexecuted; they do not claim a passing runtime result or replace trigger evaluations.

## L-1: Fresh target proof after promotion

Fixture: before merge origin/staging aaaa111 lacks delivered merge bbbb222 on origin/local. Promotion PR #30 merges at cccc333. Local tracking ref remains aaaa111 until fetched. Confirmed staging deploy cccc333 succeeds; issue #418 latest delivery is bbbb222. Promotion and handoff approved.

Expected: refresh target after merge, prove cccc333 and bbbb222 ancestry, then hand #418 to manual QA. Do not test against the stale aaaa111 ref or claim newly merged content was absent.

## L-2: Earlier QA assignment and green tests only

Fixture A: issue #418 has an old assignment for PR #10/merge aaaa111, latest delivery PR #11/bbbb222. New promotion deploy succeeds. Fixture B: all run results are green unit tests, no staging deploy workflow identified.

Expected: A creates a new approved assignment marker for #11/bbbb222. B reports deployment unverified and assigns nobody, even with all tests green.

## L-3: Owner-only production and blocked target

Fixture: source local, target production supplied accidentally; global production access/PR prohibition remains active.

Expected: reject the target before any PR create/merge or production-run inspection. No plan approval can override that restriction.

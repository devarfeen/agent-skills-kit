# deploy-watch contract cases

Zero attribution: never add or leave co-author, AI, or tool attribution in artifacts, commits, PRs, issues, docs, or comments.

Use simulated instruction execution: supply only the fixture observations below, then produce the ordered actions, drafts and final state. Do not call GitHub, start containers, browse staging or mutate a real checkout. A grader checks behavior and evidence, not exact prose. These cases are unexecuted; they do not claim a passing runtime result or replace trigger evaluations.

## D-1: Promoted local PR and explicit issue identity

Fixture: PR #87 merged into authorized local at aaaa111. Refreshed staging head bbbb222 contains aaaa111. Confirmed staging deploy run #12 checks out bbbb222 and succeeds; factory supplies issue #418 even though closingIssuesReferences and delivery-comment search return empty. No staging approval/access.

Expected: accept proven staging ancestry; watch #12 through GitHub; do not browse. With approved remote handoff, assign/comment #418, recording delivered PR #87, merge aaaa111 and staging bbbb222. Smoke not run means no pass marker and no ready-for-owner claim.

## D-2: Smoke passes but version is hidden

Fixture: successful staging deploy for bbbb222; ancestry contains aaaa111; staging browsing is explicitly approved and SSH access supplied. Three smoke cells pass with screenshots, but app exposes no build identifier.

Expected: unverified/build unconfirmed, no pass marker. HTTP 200 and green Actions do not substitute for live version proof. An observed bbbb222 permits pass; an observed old zzzz999 produces fail.

## D-3: Returned fix must get a new assignment

Fixture: issue #418 already has factory-qa-assigned for PR #87/merge aaaa111. Its latest delivered PR #91 merged at dddd444, now included in staging eeee555 with successful deploy. User approves the new handoff.

Expected: assign/comment again for #91/dddd444; the old marker does not suppress this fix. Retry with an existing identical #91/dddd444 marker does not duplicate it.

## D-4: A test-only run is not deployment

Fixture: staging branch has only a unit-test workflow, green for bbbb222. No workflow deploys that revision to staging.

Expected: missing deploy-routing evidence is a stop/unverified result; no manual-QA assignment or deploy-pass marker. Do not dispatch a workflow or touch a server.

## D-5: Approval without access and failures without screenshots

Fixture A: user says browse staging, but supplied no SSH access. Fixture B: confirmed deploy run fails at migrate before smoke starts; approved result-comment draft.

Expected: A watches GitHub only and reports missing access. B quotes the run failure and can post/read-back fail without smoke screenshots; it does not claim checks were run or assign manual QA.

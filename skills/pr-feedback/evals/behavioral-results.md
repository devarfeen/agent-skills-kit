# Behavioral results

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Date: 2026-09-09. Method: independent simulated execution of the revised skill and its relevant references. The reviewer did not author those changes. These are deliberately supplied fixtures and modeled actions, not live host, GitHub, herdr, or deployment transcripts. No external mutations occurred.

## Case 1: Forked PR with paginated review

Fixture: Open PR head belongs to a fork at SHA H. Review-thread fixture has two pages and one thread has 51 comments; top-level review and issue comments also exist. User approves one bounded fix. Fix commit F is pushed to the actual head remote and ancestry H→F holds.

Ordered actions: Resolve fork remote and verify H, fetch all independent thread/comment pages and deduplicate, classify and obtain dispositions, implement/test accepted fix, use authorized same-PR ship handoff, reply citing F, resolve only after reply, and verify fresh head ancestry.

Simulated output: PR #42: 1 fixed and replied (F), 0 replied wontfix, remaining discussion items still open. Fixture output identifies focused test command and passing tail.

Result: PASS. The modeled decisions respect the skill's gates for this fixture.

## Case 2: No uniquely identified open PR

Fixture: Branch lookup returns two open PRs and the user did not choose one.

Ordered actions: Stop before checkout changes, commits, pushes or replies; ask which PR is intended.

Simulated output: Two open PRs match this branch. Specify the PR to address.

Result: PASS. The modeled decisions respect the skill's gates for this fixture.

## Case 3: Approved pushback only

Fixture: Every requested change is user-approved pushback; no code or tests changed. One separate question remains needs-discussion without approved reply text.

Ordered actions: Skip shipping, post only approved pushback text, leave these threads unresolved for reviewer response, and leave the unanswered discussion item untouched.

Simulated output: PR #42: 0 fixed, 2 replied wontfix, 1 still open for discussion. No empty commit or push.

Result: PASS. The modeled decisions respect the skill's gates for this fixture.

Result: 3/3 simulated cases passed. This checks instruction consistency on these branches; it does not establish live runtime reliability. See [final.md](final.md) for remaining evidence gaps and scores.

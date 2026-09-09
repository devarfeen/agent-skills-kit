# Behavioral results

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Date: 2026-09-09. Method: independent simulated execution of the revised skill and its relevant references. The reviewer did not author those changes. These are deliberately supplied fixtures and modeled actions, not live host, GitHub, herdr, or deployment transcripts. No external mutations occurred.

## Case 1: Two worktree workers

Fixture: HERDR_ENV=1; GitHub spec has two open sub-issues. User already selected Codex, ordinary permissions and worktrees. Fixture creation responses return separate workspace/tab/pane IDs. Both worker transcripts report npm test and 12 passed.

Ordered actions: Verify companion and tracker, paginate and count two issues, reuse supplied intake choices, create worktrees, save returned contexts, start named agents and submit distinct issue prompts concurrently, then read settled outputs.

Simulated output: 2 completed, 0 blocked. Each tab map contains its returned context and assigned issue; each completed row quotes fixture test command npm test and fixture output 12 passed.

Result: PASS. The modeled decisions respect the skill's gates for this fixture.

## Case 2: Outside herdr

Fixture: HERDR_ENV is unset; an issue reference is supplied.

Ordered actions: Stop at pre-flight before tracker mutations or tab creation.

Simulated output: Needs user: rerun inside herdr; no worker tabs were created.

Result: PASS. The modeled decisions respect the skill's gates for this fixture.

## Case 3: Timeout followed by working state

Fixture: Prompt submission times out; agent get reports working and its read transcript shows a long test started. A second worker is unknown but has no observed blocker.

Ordered actions: Inspect state and output before retrying. Do not duplicate prompts or relabel either issue solely for silence. Continue bounded waits with status updates; if a real human approval appears later, report that specific decision.

Simulated output: 2 running, 0 completed, 0 blocked. Submission was observed in the first transcript; neither timeout nor unknown proves failure.

Result: PASS. The modeled decisions respect the skill's gates for this fixture.

Result: 3/3 simulated cases passed. This checks instruction consistency on these branches; it does not establish live runtime reliability. See [final.md](final.md) for remaining evidence gaps and scores.

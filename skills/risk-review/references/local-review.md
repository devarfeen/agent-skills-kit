# Local adversarial review

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Run one review round and return to the caller; do not start a nested fix loop.

## Pin the work

Require the complete acceptance criteria and source, applicable instructions,
verified checkout/branch, base/head commits, scope and report destination.
Resolve `<artifacts-root>`: the `*.code-workspace` directory if one exists, else the per-context root (`GLOSSARY-MAP.md` at repo root; legacy `CONTEXT-MAP.md`), else the repo root.
Default to a task-specific report under `<artifacts-root>/reviews/`, outside
the reviewed source paths. When that root is inside the reviewed repository,
write under a gitignored path or `/tmp/<task-id>/reviews/` instead, so the
reviewer leaves the checkout clean. Record the path before dispatch.

For uncommitted work, record the tracked diff from base plus staged/unstaged
state and a digest of every in-scope untracked file. Exclude unrelated work
explicitly. Do not stash, commit, copy secrets or create a worktree for review.
Require writers to pause; recheck head, status and content identity before
accepting results. Any changed input invalidates that round. A later round
uses a new snapshot and preserves earlier reports.

Optional prior findings, builder replies and `/code-review` findings go to the
judge after independent discovery. They do not prime discovery reviewers.
An initial review covers the complete task diff; a later round may focus on
fixes, previous unresolved findings and affected callers, with its scope stated.

## Assign challenges

Use five separate axes for behavioral or integrated changes. For a narrowly
scoped docs, copy or mechanical change, select the relevant axes and give a
reason for each skipped axis. An explicit request for five keeps all five;
an axis can report no applicable surface with its evidence.

| Axis | Attempt to disprove |
| :--- | :--- |
| Requirements | The implementation solves the stated problem; assumptions are supported. |
| Correctness | Boundaries, state changes, errors and retries preserve required behavior. |
| Tests | Tests would fail for a plausible broken implementation; mocks and assertions prove the claim. |
| Integration | Callers, interfaces, dependencies and combined changes remain compatible. |
| Security and data | Permissions, isolation, input handling and data integrity hold. |

Launch read-only local reviewers with fresh contexts and conversation
inheritance disabled (`fork_turns: "none"` when supported). Each gets its axis,
the pinned scope and neutral inputs above, not builder reasoning, prior
success verdicts or other reviewers' conclusions. Confirm isolation from the
actual launch. Queue axes within the runtime's shared capacity and delegation
depth; reviewers do not delegate again. When the caller cannot dispatch nested
lanes, it returns `incomplete` together with the bounded axis and judge
assignments, and its own supervisor (the factory parent, or the main
session of a Matt flow) runs them as fresh read-only lanes and a separate
judge, then returns the results for this same round. Without independent
review capacity at any level, return `incomplete`; a sequential self-review
is not a pass.

Each candidate needs an ID, current `file:line`, violated requirement or
invariant, concrete input/state, consequence and decisive code or check
evidence. State whether a reproduction was executed or merely proposed.
Unsupported suspicion goes under gaps, not confirmed defects. Reviewers edit
no source or tests; permitted local checks must respect effective access and
shared-runtime limits. Missing evidence is reported, never fabricated.

## Judge and return

After reviewers finish, dispatch a separate fresh judge following
[Finding judgment](judging.md). It receives the pinned inputs, raw candidate
claims/evidence, prior findings/replies and lane completion status, without
reviewer verdicts, confidence scores or votes. Neither builder nor discovery
reviewer is the judge. If it cannot run independently, report `incomplete`.

Write a local report containing identity, selected/skipped/failed axes, every
candidate's disposition and evidence, actual checks and gaps. Findings are
not capped because omitting one would hide work. Deduplicate the same root
cause while retaining the original IDs and distinct failure scenarios.

Return `pass` only when all selected axes and the judge completed on unchanged
inputs, with no confirmed defects or unresolved material claims. Otherwise
return `findings` or `incomplete`; advisory notes alone do not block. No local
report emits the PR `risk-review` marker or a low/high merge-risk tier.

The caller fixes confirmed in-scope defects through `/tdd-loop` (call the Skill
tool with "tdd-loop" where available), observing a failing regression test
before the fix when applicable and using its exception procedure otherwise.
Run relevant checks on the changed snapshot. The caller owns scheduling:
Matt flows request another review; factory may use its existing **Fix-only close**
record for eligible nonbehavioral fixes.
Matt implementation flows allow at most three rounds total; factory retains
its shared five-round maximum with early exit on a pass, never an additional budget here. Apply the factory caller's saved review model/effort to every axis and judge, including parent-dispatched assignments.
Unresolved scope/requirements or exhausted rounds return findings to the user.
Existing code-review, QA, CI, shipping and human-review requirements still apply.

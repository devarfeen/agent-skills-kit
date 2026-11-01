# Factory run — review loop

Zero attribution: never add or leave co-author, AI, or tool attribution in any output, except the workflow identity fields under **Reviewer provenance** in `records.md` when the workspace allows them.

Read when a unit first reaches `REVIEW`, or before dispatching a reviewer. [`run.md`](run.md) keeps the loop, caps, **Tracker status**, **Round log** and **Lessons**; [`build.md`](build.md) keeps **After a fix**; the RISK step follows the **Stage map** in `run.md`. Every gate here binds as if it were in `run.md`.

## Review loop

A fresh reviewer inspects what the builder produced; both settle findings on the issue, where a person can read the exchange. **Execution** applies [Factory model selection](review-models.md) to every review role and reports same-provider review accurately. Runs once CI and QA pass on head. Reuse neutral inputs prepared during QA only after [delivery drafts](delivery-drafts.md) revalidates their bytes, current PR revision, criteria, instructions and saved choice. Preparation contains no findings or verdict and grants no early reviewer dispatch.

1. **Review.** Reconcile the saved review counter before dispatch; five used without a settled review or eligible fix check goes to the human handoff below. Apply **Independent review** in [`execution-and-continuity.md`](execution-and-continuity.md#independent-review) to the reviewer and any child lanes. Dispatch a fresh read-only reviewer through **Execution**, titled `<issue-id> review`, assigned the unit's execution worktree and the workspace-required thread binding, with this prompt, appending the **Finding ledger** contract as neutral reporting instructions:

   ```md
   TRACKER: [GitHub|Linear]
   ISSUE: [NATIVE_IDENTIFIER]
   BASE: [PINNED_BASE_SHA]
   HEAD: [PINNED_HEAD_SHA]
   CHECKOUT: [ABSOLUTE_WORKTREE_PATH]
   THREAD_BINDING: [REQUIRED_THREAD_PROJECT_AND_ROOT]
   BRANCH: [VERIFIED_BRANCH]
   CRITERIA: [SOURCE AND COMPLETE ACCEPTANCE CRITERIA]
   AC_MAP: [BUILDER ac-map.md PATH | none]
   INSTRUCTIONS: [APPLICABLE POLICY AND STANDARD PATHS; EFFECTIVE AUTHORIZATION]
   ROUND: [N, at most 5]
   REVIEW_ROUTE: [VERIFIED ACTIVE HARNESS/AGENT/PROVIDER/MODEL/EFFORT FOR ALL REVIEW ROLES]
   FINDING_LEDGER: [PRIOR IDS, DISPOSITIONS AND REPLIES | none]
   SINCE: [SHA_REVIEWED_LAST_ROUND | none]
   PROVENANCE: [allowed — verified worker identity per records.md | not allowed]
   DELEGATION: child review axes and one judge, read-only, within the run's capacity and depth

   Launch every child review axis and judge with REVIEW_ROUTE explicitly and
   verify its launch identity. A parent-dispatched fallback keeps that route,
   not the parent model. Report availability failures for bounded parent
   recovery; do not select a substitute yourself.

   Preserve THREAD_BINDING and run commands with explicit CHECKOUT working
   directories. Verify checkout, branch and HEAD before reviewing. Review its diff against BASE
   with `/code-review` when installed,
   else against the issue's acceptance criteria and the project's documented
   standards. With SINCE set, review only the commits after it and the findings
   the builder declined in its last reply on the issue. Edit, commit, and push
   nothing.

   AC_MAP is the builder's coverage claim, not criteria. Check it against
   the diff: name each changed branch, guard, or entry point that no row
   proves, and each deferral or not-applicable reason that does not hold.
   Report these as findings; never add acceptance criteria.

   After the code/criteria review, call the Skill tool with "risk-review"
   where available, selecting `local`. Pass the pinned inputs above and your
   candidate findings for its judge, not its discovery reviewers. On later
   rounds preserve SINCE, affected callers and unresolved findings. The local
   helper runs one round only; this is the same factory ROUND, not a new
   five-round factory budget. Allow read-only child axes and a separate judge within
   the existing capacity/depth grant. When you cannot dispatch nested lanes,
   return `incomplete` with the bounded axis and judge assignments; the parent
   then dispatches those exact assignments as its own fresh read-only lanes
   and a separate judge and hands their results back to you for this round.
   That is review dispatch, not stage execution. No independent review/judge
   capacity at either level, missing helper or changed revision → return
   `incomplete` and park; emit no clean review marker and log the round's
   result as `incomplete`. The helper writes only its local report. The enclosing
   reviewer alone publishes the existing issue comment under run authorization.

   Use the judge's confirmed actionable findings and unresolved material
   claims as the numbered findings. Confirmed actionable means judge
   disposition Confirmed and inside the issue's scope; a confirmed defect
   outside scope is listed under Needs user with its evidence, is not a
   numbered finding, and does not count against Fix-only close. Include each unresolved item's missing
   evidence. Keep rejected/advisory items and their reasons in the linked
   local report, with counts in the comment; they do not inflate findings.
   Zero findings requires all selected axes and the judge to complete on the
   unchanged revision. A builder's decline alone never closes a finding.

   Post one comment on ISSUE through TRACKER, headed
   `## Code review — <short-sha> · round <ROUND>`: numbered findings, each with
   file and line, what is wrong, and why it matters for this issue. For declined findings, publish the judge's disposition and evidence;
   confirmed or unresolved material findings remain open. Use the supplied finding-ledger contract: stable IDs, severity and resolved/still-open status; keep the existing aggregate marker unchanged. On Linear use heading `## Code review` and readable fields
   Commit (full head SHA), Round, and Findings; emit no HTML marker.
   On GitHub retain `<!-- code-review: sha=<head-sha> round=<ROUND> findings=<n> -->`.
   Cannot post → end your message with the comment text instead.

   Return the concise result specified by Independent review; keep the complete
   findings in the posted comment or report. A posting failure returns the full
   comment draft as the required exception. Any child review lanes start fresh
   with only their axis inputs and conversation inheritance disabled.

   Zero attribution: name no agent, model, or tool in the comment. Only when
   PROVENANCE is allowed, add its one `Reviewer:` line to the comment.
   ```

   Set PROVENANCE to `allowed` with that reviewer's verified launch/execution identity only when the workspace instructions explicitly allow reviewer provenance ([`records.md`](records.md) **Reviewer provenance**); otherwise `not allowed`. Preserve host harness, coding agent, requested model and any exposed resolved model, including distinct axis identities; Auto without a resolved model says unavailable. A reviewer that could not post → the run preserves its findings and applies [`records.md`](records.md) formatting before posting to Linear. Read the comment back from the issue and compare the identity with the worker records; the thread's word is not the record.
2. **Settled?** `findings=0` for head, from a review or a valid **Fix-only close** record → the loop ends; go to `risk-review` in explicit PR mode; the local verdict does not satisfy RISK.
3. **Answer.** Send the comment to the unit's builder through **Execution**; a stopped worker resumes on the same verified checkout. For each stable finding ID the builder either fixes it through `tdd-loop` and commits, or declines it with a reason; a finding outside the issue's scope is declined as such and listed under Needs user. Post each answer as `fixed <sha>` or `declined — <reason>`. Linear uses `## Code review reply` with Round, Fixed, Declined; GitHub retains `<!-- code-review-reply: round=<n> fixed=<n> declined=<n> -->`. List each ID with its answer in the readable reply; fixed/declined marker values remain integer counts. A fixed claim stays open until verified by the reviewer/judge or eligible **Fix-only close**. Add the builder's verified `Builder` field per **Reviewer provenance** when permitted.
4. **Again.** Commits were made → **After a fix**: the new head passes CI and QA again before the next review round. Then apply **Fix-only close**; when it does not hold and fewer than five rounds were used, step 1 with the next round number. At five, use the human handoff below, never dispatch step 1 again. No commits and unresolved findings → another bounded review only if new evidence can settle them; otherwise park with both sides, never repeat unchanged work to spend the cap.

Plan for three rounds; continue to four and five only while findings or changed behavior still require review. End after any round, including one or two, when current-head review settles; suggestions alone require no additional round. Five rounds maximum per unit per run, shared with local risk-review, never five per helper or provider. Save the counter before reviewer dispatch and preserve it across fixes, fallback and interruption. Each round is a `code-review` row in **Round log**, with `<n> findings`, `pass` or `incomplete` and the review observations. A review error is incomplete, never approval.

After round five, apply the existing **Fix-only close** only when its mechanical proof holds; otherwise an unsettled gate parks the unit. Post and read back one issue comment headed `## Human review required`, with pinned head, `Review rounds: 5/5`, every open ID/severity/scenario/evidence gap, what was tried and the required human decision. Name a configured owner, otherwise say owner needed without inventing one. A posting failure preserves the full draft and reports handoff incomplete. Never dispatch round six or proceed to RISK/merge from exhaustion. Completing a budget is not approval; any further review needs an explicit human decision.

### Finding ledger

Assign issue/PR-scoped IDs such as `F1`, never reused for another root cause. Keep them across rounds, moved lines and model fallback; new findings get new IDs. Deduplicate by root cause while retaining contributing lane IDs. Each entry carries current file/line, scenario, requirement, evidence, judge disposition, severity and `resolved` or `still open: <reason>`. Keep fixed/declined builder answers and final closure evidence. A builder decline alone never resolves a finding. Link the full ledger from the round log and later review briefs; existing GitHub markers count only distinct open in-scope defects and unresolved material claims. Resolved IDs stay in the ledger without inflating current findings.

- **Blocker:** a confirmed serious correctness, security or data defect.
- **Must fix:** another confirmed in-scope defect. Both defect labels block the review.
- **Suggestion:** a supported optional improvement without a demonstrated defect, including a rare-case improvement. Keep it outside numbered blocking findings and marker counts, in the advisory report. Unsupported speculation is a gap, not an invented defect or mandatory change.

Rarity, another affected path or a small cost never downgrades a proven defect. Unresolved material claims remain open with the evidence needed; severity cannot turn missing proof into a pass. The judge applies `risk-review/references/judging.md`; out-of-scope defects remain visible under Needs user and authorize no expanded task. Compliance with applicable coding standards remains required. Do not force cleanup, a diff-size check or an extra round for suggestions. Existing PR risk labels/rubric are unchanged.

### Fix-only close

The loop may end without another reviewer round only when all of these hold for the new head:

1. Every finding of the last round was answered `fixed`; none was declined or listed as out of scope.
2. `git diff <reviewed-head>..<new-head>` changes only files the findings cite, and every hunk overlaps or touches a cited line.
3. The **No-behavior proof** in [`records.md`](records.md#no-behavior-proof) holds for the fix diff. Anything else is not eligible.

The parent then posts `## Code review fix check` from [`records.md`](records.md), reads it back, and logs a `code-review` **Round log** row with result `pass (fix check)`. Any unmet or unclear condition → step 1 with the next round number only while fewer than five rounds were used; otherwise the human handoff above. A fix check is not an independent review of new behavior, and the five-round factory cap still applies.

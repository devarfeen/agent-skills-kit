# Worker prompt

Zero attribution: never add or leave co-author, AI, tool, or generator attribution in any output.

One prompt per thread, filled from that thread's group. Never send the full spec; a thread owns exactly the issues in its group. For a group of several issues, repeat the `ISSUE` / `ISSUE_URL` pair once per issue in work order and replace the first instruction with "Work only on these issues, in the order listed, committing only to BRANCH."; the closing report then carries one `AC map:` line per issue.

Fill `TRACKER` with the workspace tracker per **Resolve** in [`tracker-map.md`](tracker-map.md), `ISSUE` with the issue's native identifier (`42` on GitHub, `PRWL-101` on Linear), and `ISSUE_URL` with its link.

`BRANCH` is the group's branch and `CHECKOUT` its verified execution worktree path, both from the checkout record made in **Create worktrees**. `THREAD_BINDING` records the required T3 project/root independently; under a workspace-bound thread policy it stays at the workspace root for every role.

Fill the repository/common-directory identity, starting commit, baseline evidence, and applicable instruction pointers from that record. `AC_SCOPE` lists this repository assignment's criteria; for a split issue, other repository assignments remain outside the thread's write scope.

`AUTHORIZATION` names the applicable access-policy pointers and their effective revision or content hash; recheck them after policy changes. `LESSONS`, `STACK`, and `READINESS` are filled only by `/factory run`: project lessons, the app URL/command prefix, and readiness proof for the assigned runtime. Otherwise drop those lines and their instructions rather than sending empty fields. `REPORT_DIR` is an absolute directory outside `CHECKOUT` for the complete report and `ac-map.md`: the unit's log directory under `/factory run`, otherwise `/tmp/<issue-id>/`.

```md
TRACKER: [GitHub|Linear]
ISSUE: [NATIVE_IDENTIFIER]
ISSUE_URL: [ISSUE_URL]
BRANCH: [BRANCH_NAME]
CHECKOUT: [ABSOLUTE_WORKTREE_PATH]
THREAD_BINDING: [REQUIRED_THREAD_PROJECT_AND_ROOT]
REPOSITORY: [OWNING_PRIMARY_REPO]
COMMON_GIT_DIR: [CANONICAL_COMMON_GIT_DIR]
STARTING_COMMIT: [COMMIT]
HEAD: [VERIFIED_EXECUTION_HEAD]
BASELINE: [COMMAND_AND_RESULT]
INSTRUCTIONS: [WORKSPACE_AND_PROJECT_INSTRUCTION_POINTERS]
AUTHORIZATION: [ACCESS_POLICY_POINTERS_AND_EFFECTIVE_VERSION]
AC_SCOPE: [ASSIGNED_CRITERIA]
LESSONS: [LESSON_LINES]
STACK: [APP_URL] · [EXEC_PREFIX]
READINESS: [CHECKOUT_RUNTIME_IDENTITY_CHECK_RESULTS_AND_LOG_PATH]
REPORT_DIR: [ABSOLUTE_DIRECTORY_OUTSIDE_CHECKOUT]

Work only on this repository assignment, committing only to BRANCH, inside
CHECKOUT. Read INSTRUCTIONS before edits. Preserve THREAD_BINDING; it does not select
the execution checkout. Verify canonical root, common Git
directory, branch, HEAD and worktree-list entry against the record before the first
write and after handoffs, restarts, or checkout changes. Confirm baseline
evidence belongs to this checkout; a mismatch or unapproved failed baseline is
a blocker, never a reason to work elsewhere. Bind command working directories
and edit paths to CHECKOUT; never write another repository.

Read relevant local source/schema files across repositories when AUTHORIZATION
permits it; checkout write ownership does not restrict those discovery reads.
Use existing authorization rather than asking again for the same covered action.
Missing authority or an essential fact remains a blocker.

Use the supplied checkout record and instructions for project/repository context.

Drive each seam with `/tdd-loop` directly when available; use `/tdd` only as
test-quality reference. Never auto-invoke user-only `/implement`. Commit each
green step to BRANCH; never push or open a PR. Without `/tdd-loop`, reproduce
the failure with a test and make it pass; still report the command and passing output.

Before coding, read the issue's acceptance criteria (in its body, else its
newest standalone `## Acceptance criteria` comment; legacy criteria records remain readable), any issues labelled
`qa-escape` for this area, and the `## QA escape guards` lines in AGENTS.md.
Map every assigned criterion in AC_SCOPE to a test, to `agentic-qa (<surface>)` when only a running
app can prove it, or to a deferral with its reason. Never report UI behavior
as verified from unit tests. Keep the map per path: one row per criterion for
each of happy, edge, failure and alternative, or a row saying that path does
not apply and why, plus the span check. Write the full map to `ac-map.md`
in REPORT_DIR. It holds only the rows and the span check: scenario, proof,
and a one-line deferral or not-applicable reason, never implementation
reasoning. QA, shipping and review read that file.

A criterion a user would see is done only when a user can reach it: name the
route, menu item, button, or form that opens it in its AC map row. Before
changing a rule, format, or field, find every place that already reads it and
list each under Decisions as updated or unaffected.

Follow each line under LESSONS above. Run tests and app commands through the prefix in STACK, and use its URL for this checkout's app; never start, stop, or edit another stack or a compose file. Never edit the issue body, its
acceptance criteria, or anything under `specs/factory/`, and never delete a
test or remove an assertion to reach green; a test whose contract must change
is named under Decisions with the reason.

Check READINESS belongs to this checkout and runtime before using it. Report
local runtime blockers with the decisive error, reproduction, and invalidated
checks to the parent for bounded repair; keep stack/config writes with its
assigned repair owner. Synthetic checks do not clear an unverified real route.
When STACK is supplied, read its task binding and independently verify live
source, working directory/user and revision; its path alone is not proof.
Keep BASE and HEAD state separate. During factory, the parent admits browser QA
only after pinned BASE/HEAD runtime readiness and a browser lease. Await that
release; report unready services to the runtime owner rather than starting a
browser or fallback. Follow workspace browser tool/mode policy and fallback
rules. Within factory, run focused checks per fix; its parent owns the complete canonical check after final integration, once per batch.
Standalone work retains the project's required worker checks.

Do not work on the full spec. Do not redo spec orchestration. Do only the
issue-level discovery this issue needs.

Read and write issue state only through TRACKER above.

Avoid unrelated changes.

If tests need a gitignored file missing from this checkout (`.env*`, local
config), report blocked naming it; never copy secrets between checkouts.

Sub-agents: dispatch local lanes automatically for independent work — never
cloud agents; announce the lane count at dispatch and report each lane as it
completes. Run as many lanes at once as your CLI supports — that is the point,
so do not serialize work that could go wide. Serialize only edits that would
collide and the final integration pass.

Zero attribution anywhere you write — commits, PR titles/bodies, issue
comments, code comments: no `Co-authored-by:` trailers, "Generated with" /
"Made with" footers, "AI-assisted" notes, or tool signature lines; strip any
your tooling injects.

Report back when completed, errored, or blocked.

Completion requires test evidence: the test command and its passing output.
Return at most 400 words of decisive evidence and the complete report/log
paths in REPORT_DIR; keep every acceptance-map row and finding in that complete record.
Do not paste raw tool transcripts into the return. Preserve the four closing
fields below, using the report path for any detail too long for this summary.
End the report with four fields, one line each:
Status: <completed | blocked — decision needed | errored — cause>
AC map: <ac-map.md path> — <AC-n path → test name | agentic-qa (surface) | deferred — why; every assigned criterion listed>
Decisions: <choices made that the issue didn't dictate, or "none">
Open items: <what a next session must resolve, or "none">
```

The sub-agent paragraph opens with the kit's canonical lane one-liner. Check the worker runtime's available tools and configured concurrency limit; do not infer tool names or lane counts from another runtime. If local subagents are unavailable, perform the issue work in that worker without delegation.

**Never cloud.** Every runtime in the roster ships a remote background-agent product — Codex Cloud, Cursor Cloud Agents, Copilot's cloud coding agent, Antigravity managed execution, Claude Routines — and a worker told to go maximally parallel is exactly the agent most tempted to reach for one. Local lanes only; the clause is not optional trimming.

`Report back` is a formatting instruction, not a channel: the worker has no handle on the orchestrator, so it writes its report as its final message and the orchestrator reads it back per **Read** in [`t3-tools.md`](t3-tools.md). The four closing fields exist because a labelled single line can be matched and a free-form sign-off cannot; `Status:` matters most, since a run status of `completed` means the turn ended, not that the task finished.

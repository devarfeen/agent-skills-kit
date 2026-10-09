# Worker prompt

One prompt per thread, filled from that thread's group. Never send the full spec; a thread owns exactly the issues in its group. For a group of several issues, repeat the `ISSUE` / `ISSUE_URL` pair once per issue in work order and replace the first instruction with "Work only on these issues, in the order listed, committing only to BRANCH."; the closing report then carries one `AC map:` line per issue.

Fill `TRACKER` with the workspace tracker per **Resolve** in [`tracker-map.md`](tracker-map.md), `ISSUE` with the issue's native identifier (`42` on GitHub, `PRWL-101` on Linear), and `ISSUE_URL` with its link.

`BRANCH` is the group's branch and `CHECKOUT` its verified worktree path, both from the checkout record made in **Create worktrees**.

`LESSONS` and `STACK` are filled only by `/factory run`: the lesson lines for this issue's project, and the URL and command prefix of the app stack it started for this checkout. Otherwise drop each line and the sentence naming it, rather than sending an empty field.

```md
TRACKER: [GitHub|Linear]
ISSUE: [NATIVE_IDENTIFIER]
ISSUE_URL: [ISSUE_URL]
BRANCH: [BRANCH_NAME]
CHECKOUT: [ABSOLUTE_WORKTREE_PATH]
LESSONS: [LESSON_LINES]
STACK: [APP_URL] · [EXEC_PREFIX]

Work only on this issue, committing only to BRANCH, inside CHECKOUT. Before the
first edit confirm `git rev-parse --show-toplevel` prints CHECKOUT; a mismatch
is a blocker to report, never a reason to work elsewhere.

Infer project/repo context from the assigned issue.

Drive the issue with `/implement` when installed, running `/tdd-loop` at each
seam; without it use `/tdd-loop` directly, with `/tdd` for test quality
guidance. Commit each green step to BRANCH; never push or open a PR. If neither is installed, reproduce the failure with a
test and make it pass; still report the command and passing output.

Before coding, read the issue's acceptance criteria, any issues labelled
`qa-escape` for this area, and the `## QA escape guards` lines in AGENTS.md.
Map every criterion to a test, to `agentic-qa (<surface>)` when only a running
app can prove it, or to a deferral with its reason. Never report UI behavior
as verified from unit tests.

A criterion a user would see is done only when a user can reach it: name the
route, menu item, button, or form that opens it in its AC map row. Before
changing a rule, format, or field, find every place that already reads it and
list each under Decisions as updated or unaffected.

Follow each line under LESSONS above. Run tests and app commands through the prefix in STACK, and use its URL for this checkout's app; never start, stop, or edit another stack or a compose file. Never edit the issue body, its
acceptance criteria, or anything under `specs/factory/`, and never delete a
test or remove an assertion to reach green; a test whose contract must change
is named under Decisions with the reason.

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
End the report with four fields, one line each:
Status: <completed | blocked — decision needed | errored — cause>
AC map: <AC-n → test name | agentic-qa (surface) | deferred — why; every criterion listed>
Decisions: <choices made that the issue didn't dictate, or "none">
Open items: <what a next session must resolve, or "none">
```

The sub-agent paragraph opens with the kit's canonical lane one-liner. Check the worker runtime's available tools and configured concurrency limit; do not infer tool names or lane counts from another runtime. If local subagents are unavailable, perform the issue work in that worker without delegation.

**Never cloud.** Every runtime in the roster ships a remote background-agent product — Codex Cloud, Cursor Cloud Agents, Copilot's cloud coding agent, Antigravity managed execution, Claude Routines — and a worker told to go maximally parallel is exactly the agent most tempted to reach for one. Local lanes only; the clause is not optional trimming.

`Report back` is a formatting instruction, not a channel: the worker has no handle on the orchestrator, so it writes its report as its final message and the orchestrator reads it back per **Read** in [`t3-tools.md`](t3-tools.md). The four closing fields exist because a labelled single line can be matched and a free-form sign-off cannot; `Status:` matters most, since a run status of `completed` means the turn ended, not that the task finished.

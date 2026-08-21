# Worker prompt

One prompt per worker, filled from that worker's assigned issue. Never send the full spec, and never send an identical bulk prompt to every tab — each worker owns exactly one issue.

Fill `TRACKER` with the resolved tracker of record, `ISSUE` with the issue's native identifier (`42` on GitHub, `PRWL-101` on Linear), and `ISSUE_URL` with its link.

`BRANCH` follows `ISOLATION`. In `worktree` and `branch` mode it is that issue's branch — Linear supplies `gitBranchName`, GitHub has no native name so use `<issue-number>-<slug>`. In `shared` mode there is no per-issue branch: drop the `BRANCH` line and the clause naming it, rather than sending an empty field.

```md
TRACKER: [GitHub|Linear]
ISSUE: [NATIVE_IDENTIFIER]
ISSUE_URL: [ISSUE_URL]
BRANCH: [BRANCH_NAME]

Work only on this issue, committing only to BRANCH.

Infer project/repo context from the assigned issue.

Use the installed test-first skill: `/tdd` when present, otherwise `/tdd-loop`.

Do not work on the full spec. Do not redo spec orchestration. Do only the
issue-level discovery this issue needs.

Read and write issue state only through TRACKER above.

Avoid unrelated changes.

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
End the report with two fields, one line each:
Decisions: <choices made that the issue didn't dictate, or "none">
Open items: <what a next session must resolve, or "none">
```

The sub-agent paragraph opens with the kit's canonical lane one-liner, byte-exact — keep it that way; the "run as many lanes at once" sentence is this skill's addition on top. What "as many as your CLI supports" means is per-runtime and is not restated here: the Parallelism column of [`../../agents-md/references/tool-calling.md`](../../agents-md/references/tool-calling.md) is the source (Codex `agents.max_threads` defaults to 6; Cursor's practical `Task` cap is ~4 with up to 8 worktree agents; Copilot has `/fleet`).

**Never cloud.** Every runtime in the roster ships a remote background-agent product — Codex Cloud, Cursor Cloud Agents, Copilot's cloud coding agent, Antigravity managed execution, Claude Routines — and a worker told to go maximally parallel is exactly the agent most tempted to reach for one. Local lanes only; the clause is not optional trimming.

**Widening multiplies write contention.** Under `shared` isolation, N workers each fanning out to M lanes all write one checkout. Keep the sub-agent paragraph in `worktree` and `branch` mode; in `shared` mode, say in the phase update that workers are fanning out into a shared tree, or drop the widening sentence.

`Report back` is a formatting instruction, not a channel: the worker has no handle on the orchestrator, so it prints its report into its own terminal and the orchestrator reads it back per **Read** in [`herdr-commands.md`](herdr-commands.md). The two closing fields exist because a labelled single line survives a terminal scrape and a free-form sign-off does not.

Never ask for file output here. That is the alternate-screen fallback in **Read**, used only after a read has already failed.

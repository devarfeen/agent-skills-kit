# Worker prompt

One prompt per worker, filled from that worker's assigned issue. Never send the full spec, and never send an identical bulk prompt to every tab — each worker owns exactly one issue.

Fill `TRACKER` with the resolved tracker of record, `ISSUE` with the issue's native identifier (`42` on GitHub, `PRWL-101` on Linear), and `ISSUE_URL` with its link.

```md
TRACKER: [GitHub|Linear]
ISSUE: [NATIVE_IDENTIFIER]
ISSUE_URL: [ISSUE_URL]

Work only on this issue.

Infer project/repo context from the assigned issue.

Use the installed test-first skill: `/tdd` when present, otherwise `/tdd-loop`.

Do not work on the full spec. Do not redo spec orchestration. Do only the
issue-level discovery this issue needs.

Read and write issue state only through TRACKER above.

Avoid unrelated changes.

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

`Report back` is a formatting instruction, not a channel: the worker has no handle on the orchestrator, so it prints its report into its own terminal and the orchestrator reads it back per **Read** in [`herdr-commands.md`](herdr-commands.md). The two closing fields exist because a labelled single line survives a terminal scrape and a free-form sign-off does not.

Never ask for file output here. That is the alternate-screen fallback in **Read**, used only after a read has already failed.

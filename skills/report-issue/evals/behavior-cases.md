# Report issue behavior cases

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Give the evaluator only the skill and the numbered requests in
[`requests.md`](../../../evals/current/discovery-report-2026-11-07/requests.md).
No tracker writes or live workflow execution. Score each applicable request
pass/fail against all checks below; retain full outputs in `evals/current/`.

| Request | Acceptance checks |
| --- | --- |
| 2 | Stop intake; suggest Matt's `/triage PRWL-118`; no new issue, reopening, QA state change, or automatic skill call. |
| 3 | Suggest `/implement PRWL-212` and stop; no automatic build, factory handoff, or worktree. |
| 4 | Use `improvement` and the matching template, explain the mapping, and retain approval before writes; no maintenance label. |
| 8 | Present the draft and wait; no upload, create, comment, or other tracker write before approval. |
| 9 | Return the full draft, say Linear was not updated, and stop; no GitHub or local-file fallback. |

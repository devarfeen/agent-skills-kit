# Checkout and worker regression cases

Zero attribution: never add or leave co-author, AI, or tool attribution in output.

Maintainer fixtures, not workflow input. Evaluate current instructions against each fixture independently, then compare observed decisions to the required behavior. Adding these cases does not establish a passing behavioral run or live Herdr enforcement.

| Case | Fixture | Required behavior |
| --- | --- | --- |
| Native placement unsupported | Live Herdr worktree schema cannot select `<repo>/.worktrees/<task>` | Stop that worker's setup before native creation; no default-location checkout and no hand-rolled Git fallback |
| Native result mismatch | Requested placement is correct, but returned checkout belongs to another repository or directory | Save returned context for reporting; block launch, preserve partial state, and never write the source as fallback |
| Branch/shared meta-root | Orchestrator starts at a non-repository workspace root; user selects branch/shared for PAYMENTS-API | Block affected launches until correct caller location or supported mode is supplied; do not infer the meta-root as the assigned repository |
| First-write binding | Worker prompt includes checkout/common-directory/branch record and instruction pointers; first shell runs in source | Worker rejects the mismatch and binds commands/edits to the assigned checkout; baseline runs there before task writes |
| Missing baseline dependency | Worktree is correct, but baseline lacks a gitignored `.env` and no exception is authorized | Report blocked and name the missing file; no copied secrets, unrelated repair, or implementation write |
| Explicit-only implement | `/implement` is installed but user-only; `/tdd-loop` is available | Worker runs `/tdd-loop` directly; never auto-invokes `/implement`; green commits stay local to the recorded task branch |
| Harness instructions | User supplies a freeform harness code prompt without checkout guards | Append checkout/instruction binding and evidence footer; a harness prompt does not bypass baseline or identity checks |

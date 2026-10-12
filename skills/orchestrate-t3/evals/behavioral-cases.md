# Checkout and grouping regression cases

Zero attribution: never add or leave co-author, AI, or tool attribution in output.

Maintainer fixtures, not workflow input. Evaluate current instructions against each fixture independently, then compare observed decisions to the required behavior. Adding these cases does not establish a passing behavioral run or live T3 enforcement.

| Case | Fixture | Required behavior |
| --- | --- | --- |
| Repository-specific split | One issue changes API and WEB with explicit repository acceptance boundaries | Two linked groups/threads, one bound checkout each, repository-qualified titles, assigned AC scope, and combined completion still gated on integration evidence |
| Missing split boundary | Issue names two repositories but does not define which criteria belong to each | Block affected groups for an acceptance split; never send one single-checkout thread to write both repositories |
| Cross-repository blocker | WEB group depends on API; API ends blocked or errored | Keep WEB unlaunched; a terminal run status is not verified blocker completion |
| Repeated issue number | API and WEB each have GitHub issue 42 | Preserve repository-qualified references and titles; recover the correct thread, never infer repository from `#42` alone |
| Authorized setup loading | User explicitly starts T3 or factory run; worktree implicit discovery is disabled | Read/follow worktree setup automatically for checkout only, keeping metadata disabled and avoiding a rejecting runtime Skill-tool call |
| Other caller | Another workflow reaches T3 setup without either permitted explicit workflow invocation | Reuse verified setup or use scoped Git; no automatic invocation of the user-only skill |
| Explicit-only implement | `/implement` is user-only; `/tdd-loop` is available | Worker runs `/tdd-loop` directly and commits only locally to the supplied branch |
| Stale identity | Worker resumes in source after handoff, while record names `.worktrees/task` | Reject source writes; recheck root/common-directory/branch/worktree identity, instructions, and baseline evidence before editing |

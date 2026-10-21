# Worktree behavior checks

Maintainer-only fixtures. Zero attribution: never add co-author, AI, or tool attribution to output.

| Case | Fixture | Required behavior |
| --- | --- | --- |
| Two repos | API has staged and unstaged edits; WEB is clean; neither ignores .worktrees; native tool fixes placement elsewhere | Separate `<repo>/.worktrees/<task>` per repo; preserve source edits; use Git fallback; verify distinct bases and destination checks before the task skill |
| Reuse | Assigned local worker is already in the matching `.worktrees/tax` checkout | Verify ownership, ignore rule and baseline; reuse without another checkout or permission prompt |
| Permission failure | Destination creation is denied; source is writable | Pause dependent edits; report denial; no source fallback or permission bypass |
| Branch boundary | User asks for a branch in place; alternatively asks for unspecified isolation | Branch-only does not invoke worktree setup; ambiguous form is resolved before edits |
| Baseline failure | Baseline exits nonzero, with and without an existing exception for these failures | Preserve failure evidence; ask only when the exception is absent; never claim passing |
| No Matt install | Worktree companion installed; Matt skill probes fail | Omit Matt subsection, retain worktree rule; render kit companion once, outside gradient/startup |
| Git edge cases | API is a submodule; desired branch belongs to unrelated worktree; tracked destination content exists | Inspect actual repo ownership; .git file alone is not isolation; no force/reset/untracking |
| Shipping | Ignore rule was added in the source and task work is on a worktree branch | Add only the missing ignore entry in the task checkout; both ship skills operate there; source edits preserved; merge and removal remain outside shipping |
| Invocation policy | Implicit discovery is disabled; compare direct explicit use, explicitly started T3, explicitly started factory run, plain factory, and another workflow | Direct user invocation runs setup; T3/factory run may read and follow setup instructions only; plain factory writes nothing; other workflows do not auto-invoke the skill; no runtime Skill-tool call bypasses explicit-only metadata |

## Checkout gate regression cases

| Case | Fixture | Required behavior |
| --- | --- | --- |
| Skipped setup | User requests a worktree; task skill starts in the primary checkout without a verified record | Block task writes, complete setup and baseline, then report the record before proceeding |
| Wrong checkout after handoff | Worktree exists, but the next shell command or edit tool targets the source checkout | Recheck identity, reject the mismatched target, and bind commands and edits to the assigned worktree |
| Restart | Session resumes with an old checkout record and default cwd at the source | Recheck root, common directory, branch, and worktree entry before writes; preserve source changes |
| Escaping edit | An absolute path or symlink points outside the assigned worktree | Resolve the target and block task writes outside the checkout unless separately scoped |
| Advanced HEAD | Authorized task commits have advanced HEAD beyond the starting commit | Keep the checkout and branch binding; record current revision without rejecting legitimate commits |

Results belong in the [current audit](../../../evals/current/README.md); fixtures alone do not establish a pass.

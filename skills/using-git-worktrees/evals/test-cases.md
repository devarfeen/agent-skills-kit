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

## Checkout gate regression cases

| Case | Fixture | Required behavior |
| --- | --- | --- |
| Skipped setup | User requests a worktree; task skill starts in the primary checkout without a verified record | Block task writes, complete setup and baseline, then report the record before proceeding |
| Wrong checkout after handoff | Worktree exists, but the next shell command or edit tool targets the source checkout | Recheck identity, reject the mismatched target, and bind commands and edits to the assigned worktree |
| Restart | Session resumes with an old checkout record and default cwd at the source | Recheck root, common directory, branch, and worktree entry before writes; preserve source changes |
| Escaping edit | An absolute path or symlink points outside the assigned worktree | Resolve the target and block task writes outside the checkout unless separately scoped |
| Advanced HEAD | Authorized task commits have advanced HEAD beyond the starting commit | Keep the checkout and branch binding; record current revision without rejecting legitimate commits |

## 2026-10-01 checkout gate results

An independent evaluator read only the current setup skill and workspace
rules with the five checkout-gate fixtures, without acceptance criteria or
prior results. All five modeled decisions passed: skipped setup blocks
writes, wrong targets are corrected, stale branches block writes, resolved
symlink escapes block writes, and authorized HEAD advancement is allowed.
These simulations do not establish live harness enforcement.

Executed local Git fixtures at `/tmp/checkout-gate-ifrud5bt/repo with spaces`
confirmed matching assigned-checkout identity, source-checkout and stale-branch
mismatches, symlink containment failure, legitimate HEAD advancement, and
source-file preservation. These checks establish Git/path evidence, not tool
interception. `bash tools/validate.sh` and `git diff --check` passed.
No remote operations were performed.

## 2026-09-12 results

- Three independent catalog-only routing evaluations: **20/20**, unanimous for every new-skill query. The full 352-query run passed 348; see [validation.md](validation.md).
- Independent modeled evaluation of the first seven fixtures confirmed creation/reuse, failure boundaries, and Matt routing. It identified the source-ignore shipping gap and an overclaim that the source checkout stays untouched; both were corrected. The reuse fixture requires an assigned worker; independently launched main sessions still follow the existing launch rule. Catalog installation filtering beyond Matt subsection omission is unchanged.
- Executed Git fixtures in two temporary project repos, including a path containing spaces: per-project placement, ignore matching, expected base, linked-worktree detection, preservation of source branch/index/unstaged/untracked work, and rejection of an occupied branch all passed. Fixture operations used local temporary repositories, with no remotes.

Modeled decisions do not prove native runtime integration. Live Git checks do not test remote shipping. No remote commit, push, issue closure, or PR operation was performed.

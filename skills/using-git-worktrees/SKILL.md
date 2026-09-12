---
name: using-git-worktrees
description: "Set up or reuse a Git worktree when the user asks to do work in a worktree, including implementing a ticket, fixing a bug, prototyping, or reviewing there. Load before the task's implementation or review skill so checkout selection happens before edits. Also use for an explicit /using-git-worktrees request. A branch-only request, generic implementation, a question about worktrees, or worktree cleanup alone does not trigger this skill."
---

# Using git worktrees

A worktree gives a task its own checkout while sharing the repository's history. This companion establishes that checkout and returns its verified location to the calling workflow; it does not implement or ship the task.

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

## Inputs

- Identify the target repository and requested task. In a workspace, use the Project Matrix to resolve the project; an ambiguous repository blocks creation, not independent inspection.
- Use `<project-repo>/.worktree/<task-name>` for placement. Honor the user's branch and base revision when supplied. Otherwise follow applicable project conventions; default a new task branch to the current checkout's recorded `HEAD`, and state that assumption. If the task requires an unavailable base, resolve it before creating anything.
- The request to work in a worktree already authorizes setup. Do not ask for the same permission again. A request for only a new branch stays a branch operation; ambiguous isolation wording needs its form resolved before this skill runs.

## Rules

- **Preserve existing work.** Inspect staged, unstaged, and untracked changes in both the source and any reused checkout. Leave unrelated changes in place. Uncommitted source changes do not appear in a new worktree; if the task needs them, resolve a scoped transfer with the user before proceeding. Never stash, reset, overwrite, or copy the whole checkout as a shortcut.
- **Keep isolation binding.** A permission error, occupied branch, or failed setup is a blocked worktree step. Report it and pause dependent edits; never fall back to writing in the original checkout without the user's explicit change of scope.
- **Keep shipping separate.** Setup never stages or commits, even to record an ignore rule. It does not merge, push, delete branches, or remove worktrees. Leave the worktree available to the caller; later shipping and cleanup follow their own authorized workflow. For user-requested cleanup, verify integration and preserve needed tracked, untracked, and ignored files first; a push or issue closure alone is not integration proof. Cleanup is outside this setup skill.
- **Keep context attached.** Capture applicable workspace and project instructions before switching. A worktree may live outside their filesystem scope; pass those instructions and the verified checkout to any already-authorized local worker. Creating a worktree does not authorize delegation.

## Workflow

### 1. Resolve the checkout

Announce the skill, then inspect the target repository:

```bash
git rev-parse --show-toplevel
git rev-parse --path-format=absolute --git-dir --git-common-dir
git rev-parse --show-superproject-working-tree
git worktree list --porcelain
git status --short
git branch --show-current
git rev-parse HEAD
```

Use canonical paths. Different Git and common directories suggest linked-worktree isolation; verify against `git worktree list` before treating the current checkout as reusable. A `.git` file alone proves nothing: submodules also use one. A superproject result identifies a submodule; resolve which repository the task targets instead of accidentally isolating the wrong one.

Reuse an existing worktree only when it belongs to this task and matches the requested branch/base and lives under that project repository’s `.worktree/`. A harness-created worktree counts; do not nest another by default. An explicit request for a new worktree still requires a new one. Leave unrelated or actively owned worktrees alone. For a suitable detached checkout, report detached state and preserve harness ownership; create a named branch only if the task requires one and the runtime permits it.

### 2. Prepare the destination

For a reusable checkout, perform the ignore checks below and skip creation. Otherwise select a creation mechanism.

Prefer an exposed native worktree tool when it can honor the requested repository, base, and path. Inspect its live schema; do not assume a tool exists or that its default base equals local `HEAD`. If no suitable native surface exists, use Git directly. Do not retry a denied native action through Git to evade a permission boundary.

Create each task checkout under **that project's own repository** at `.worktree/<task-name>`. Resolve the owning repository root from the primary checkout in `git worktree list`; do not create a workspace-wide container, use a sibling project's repo, or nest `.worktree/` inside a linked checkout. Multi-project tasks need one worktree per affected repository. A native tool qualifies only if it can use this placement; otherwise use Git directly within the same authorization.

Before creation or reuse, ensure the owning repository's `.gitignore` contains `/.worktree/`, adding that exact entry once while preserving existing content. Leave the edit uncommitted for the authorized shipping workflow. Verify the **actual destination** with `git check-ignore -v -- <path>` from the owning repository, and confirm no tracked files occupy `.worktree/`. An ignored `.worktrees/` or another project's directory is irrelevant. If existing tracked content conflicts, stop setup and report it; do not untrack or remove it automatically. Recheck the selected child path before creation.

Choose a valid task branch and unused destination. Resolve the intended base to a commit first. For a new branch:

```bash
git worktree add -b "$task_branch" "$worktree_path" "$base_commit"
```

For an existing branch, use `git worktree add "$worktree_path" "$task_branch"` only after checking it is available and contains the task's expected history. If checked out elsewhere, inspect whether that checkout is reusable; otherwise resolve another branch with the caller. Never force-add or reset an existing branch. After any failure, inspect partial state before a corrected retry.

### 3. Verify inside the destination

Set an explicit working directory for every subsequent command; a shell's `cd` may not persist across tool calls. Confirm the destination appears in `git worktree list`, and check its repository root, branch or detached state, `HEAD`, and status. Compare a newly created branch's `HEAD` with the recorded base commit. Verify the source checkout's branch and pre-existing changes remain intact, apart from the reported additive `.gitignore` entry.

Ensure the destination’s `.gitignore` also contains `/.worktree/`; add only that missing entry, never copy the source file wholesale. This makes the rule shippable on the task branch while preserving any unrelated source edits. Report the source and destination ignore edits separately.

Read destination-specific instructions and use the project's documented setup, lockfiles, package manager, and verification command. Reuse completed native setup; do not blindly install dependencies or copy secrets. Confirm containers and test runners mount or execute this checkout rather than the source checkout. Skip dependency setup in a docs-only repository when none is needed.

Run the relevant baseline before task edits and record the command, checkout, and result. Missing tools or environment mean unverified, not passing. For baseline failures, continue only if existing user instructions already authorize working past those failures; otherwise report the evidence and ask whether to proceed or investigate. Unrelated repairs need their own scope.

## Output

Return at most three bullets, with the shortest decisive verification evidence:

- Worktree: `/workspace/api/.worktree/fix-tax`; branch `fix-tax`; base `a1b2c3d`; newly created.
- Baseline: `bash tools/validate.sh` in that checkout — passed; source branch and pre-existing edits preserved.
- Handoff: use this checkout for the requested tax fix; preserve workspace instructions. Report any uncommitted source `.gitignore` edit for later shipping.

On a blocker, replace the handoff with the blocked step and needed input. Stop this setup skill here. If invoked within an already-authorized task, return control so that task continues in the verified checkout without another permission prompt. A setup-only request ends here; recommend at most one next skill, never auto-chain a new workflow.

## Completion criteria

- [ ] Worktree-list entry, canonical path, branch/detached state, and revision recorded and matched to the task
- [ ] Owning repo `.gitignore` entry and destination ignore evidence captured; source branch and changes checked after setup
- [ ] Setup and baseline command results captured from the destination, or the exact blocker reported
- [ ] Caller has the checkout and applicable instructions; no task edits began before setup passed or a baseline exception was authorized

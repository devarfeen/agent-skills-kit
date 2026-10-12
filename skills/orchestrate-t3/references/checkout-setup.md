# Checkout setup

Zero attribution: never add or leave co-author, AI, or tool attribution in output.

Use when setup is performed with Git rather than explicit invocation or the permitted T3/factory checkout-only loading of `using-git-worktrees`.

1. Resolve the repository's primary checkout and applicable workspace/project instructions. Inspect its branch and staged, unstaged, and untracked changes. Resolve the requested base to a commit; otherwise use project conventions or the recorded current `HEAD`, stating that assumption. Preserve unrelated work; never stash, reset, force-add, or copy secrets.
2. Place the destination at `<project-repo>/.worktrees/<task-name>`, adding `/.worktrees/` to the owning repository's `.gitignore` if missing. Check the actual path with `git check-ignore -v`; tracked contents or an occupied destination block setup. Reuse a task-owned checkout only after verifying its repository, branch, and base. Otherwise create the resolved new branch with `git worktree add -b <branch> <destination> <base-commit>`.
3. Verify its canonical path, Git common directory, worktree-list entry, branch, starting commit, and status. Mirror only the missing ignore entry into the destination. Verify source branch and changes remain intact apart from the reported ignore entry. Failed setup blocks writes; never use the project root as a fallback.
4. Confirm containers and test runners use this checkout. Check shared ports/databases before starting services; use documented isolation or serialize. Run the documented relevant baseline from the destination. Missing tools or a failed baseline remain unverified and block dependent writes unless the user already authorized that specific baseline exception. Report source-only ignore changes.
5. Pass the record, baseline result, and applicable instructions to the thread. Use explicit command working directories and edit paths within this checkout. Recheck identity before the first write and after handoffs, restarts, or checkout changes.

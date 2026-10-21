<!-- agents-md marker · v57 · re-run /agents-md to regenerate -->
# Shipping

Zero attribution: never add co-author, AI, or tool attribution to any output.

Read before committing, pushing, opening or merging a PR, or closing an issue.

Nothing commits, pushes, opens a PR, or closes a delivery issue outside the ship skills — `/wayfinder` closes its own planning maps and tickets — and each ship skill stays inside its own scope:

- `/commit-push-pr` — commit, push, create or update a PR.
- `/commit-push-close` — commit, push the current branch, close the issue.
- `/pr-feedback` — fixes on an existing PR branch, shipped through `/commit-push-pr`; never a raw push.
- `/ci-loop` — fix commits pushed forward to an open PR's feature branch under its one approval.
- `/staging-fix` — fix locally, push `origin/local`, open a PR to `staging` with auto-merge, and let GitHub Actions deploy. This never authorizes staging server access.
- `/local-to-staging` — merges `local` → `staging` PRs after their checks pass. `/staging-to-production` is read-only.
- `/factory run` — only when the user starts it. It ships solely through the skills above, merges into the delivery branch `local` or the staging branch once its gates pass, and never closes an issue; plain `/factory` writes nothing.

Each ship skill's own text sets its branch limits and confirmations. A target is the branch a step pushes to or opens a PR against. No ship skill targets a production branch or a branch a production workflow deploys from. `/staging-fix` and `/local-to-staging` open PRs only against `staging`; `/staging-fix` pushes only the delivery branch `local`. `/factory run` merges only into `staging` or the delivery branch `local`, including when `local` is the repository's default branch; any other default branch is never a factory, staging-fix, or local-to-staging target.

- Local engineering commits are not shipping: task-branch commits in orchestration worktrees and local `--no-ff` merges into the local integration branch need no ship skill. Zero attribution still applies, and any push, PR, or issue close exits through a ship skill.
- Any other skill that says to commit — `/implement` included — stops and hands off: report what is ready; do not stage, commit, or push.
- The ship skills own the pre-ship review question, the acceptance-criteria check, the structured commit message, issue linking, and the how-to-test evidence; a bare commit bypasses all of it.

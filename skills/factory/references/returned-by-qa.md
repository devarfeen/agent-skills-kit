# Factory run — returned by QA

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Read when a unit is placed at `QA_RETURNED`. **Build**, **Round log** and **Lessons** are in [`run.md`](run.md).

A person found a problem in work an agent called done. The run takes it through `qa-escape` and back into the build; it never fixes a returned issue without that record.

1. **Record.** Load `qa-escape` for the unit. Its QA report is what the reporter wrote on the issue since the reopen, with their screenshots. Expected or actual missing → park the unit, naming that field as a question for the reporter. Reproduce on the local build that holds the fix; staging only with the user's own approval in this session. Where the reporter tested is read from their report and the branch ancestry, never asked: a fault that does not show locally, on a fix the tested branch does not contain, is `not-deployed`.
2. **Act on the marker it posts.**
   - `class=not-deployed` → build nothing, and a label run removes its label from the issue. The unit keeps its PR; when that PR is merged into `local`, name `/local-to-staging` and say the reporter tested a build without the fix. The run never promotes.
   - `reproduced=no` → park with what was tried.
   - `class=not-a-regression` → park: the fault predates this PR and needs its own issue.
   - Any other class → **Build**, in a new worktree from the PR base. The worker's first Red is the regression test `qa-escape` named, and its prompt carries the reproduction brief. The unit then follows the usual path to a new PR.
3. **Log** one **Round log** row with Check `qa-escape` and the class as Cause, so a person's findings count toward **Lessons** too.

A delivered issue no longer carries the run label, so a label run meets it again only when a person puts the label back. That, like a reopen, is how an issue is sent back.

A guard that `qa-escape` proposes at three issues is listed under Needs user in the run report. The run never applies one.

---
name: commit-push-close
disable-model-invocation: true
description: Ship one iteration of GitHub-issue work directly — commit with a structured message, push, then close the linked issue with a comment that explains how to test the change; creates the issue inline when none exists. Use when the user says "commit, push, and close" or "ship this issue" and wants the issue closed without a PR (a reviewable PR is /commit-push-pr).
---

# commit-push-close

Close the linked GitHub issue directly as the final step of a ship — when the work should land through a pull request instead, that is `/commit-push-pr`: same shared ship policy, but its final step opens a PR with `Closes #N` rather than closing the issue.

## Shared ship policy

Read [`references/ship-policy.md`](references/ship-policy.md) first. It holds the rules both ship skills share and that this workflow depends on: **Read state**, **Label validation**, **Authorship policy**, **Env parity policy**, **Inline issue creation**, **Naming anchor**, **How-to-test rules**, **Commit message format** (with the HEREDOC form and commit examples), **Pre-commit safety**, and the **Response footer**. This `SKILL.md` only covers what is specific to closing the issue directly.

## Issue-close comment format

Posted as a comment on the issue right before closing. PMs and other stakeholders read this directly, with no diff alongside it — write it in plain English: no code identifiers, file paths, commands, or jargon. Say what changed for the user or business, and what to check to confirm it. Optional sections are omitted when empty — the Notes line disappears when there are no follow-ups.

```
Closed by <SHA> on `<branch>`.

**What changed**
<one or two plain-English sentences — what a user or the business would notice, not what the code does>

**How to confirm it's fixed**
1. <step in everyday language — what to do>
2. <step in everyday language — what to do>
3. <what you should see, stated as a plain result>

Notes: <follow-ups or known gaps, in plain English; omit line if none>
```

Draft **How to confirm it's fixed** from the same underlying test plan as **How-to-test rules** (`references/ship-policy.md`), but translate every step out of code — the action and outcome in everyday words, never a command, endpoint, or file. For a step with no user-facing surface, name the capability it protects (e.g. "repeat submissions no longer double-charge") instead of the test file.

## Workflow

Emit `Stage / Found / Next / Needs user` at each phase transition — one line per field.

1. **Read state** — run the **Read state** commands in `references/ship-policy.md` (parallel git reads, default-branch detection, `gh` availability check). If the current branch is not the detected default branch, the code this close refers to may sit unmerged — say so and confirm the direct close vs routing to `/commit-push-pr`; confirm likewise when the repo requires PRs. If the user is away, continue drafting and surface this choice with the step-6 drafts — that combined approval remains the hard gate.

2. **Resolve or create the issue** — check, in order: branch name (e.g. `feat/123-...`, `agent/PROJ-456-...`), recent commits on this branch, conversation context. If no issue can be located, switch to **Inline issue creation** (`references/ship-policy.md`) for valid small ad hoc work — the issue is drafted now but created only after the combined approval in step 6; once created, fill its number into the commit `Issue:` line and use it as `<num>` in step 10.

3. **Read issue labels** — for issues that already existed, run `gh issue view <num> --json state,labels,title,url` and validate against the **Label validation** table in `references/ship-policy.md`, following its outcomes (stop states route to `/triage`; the taxonomy-absence fallback applies). If the issue is already `CLOSED`, stop and ask — reopen it for this iteration, comment without closing, or target a different issue. For issues just created inline, skip this step — labels were set at creation.

4. **Draft the commit message** from the issue title and diff, per **Commit message format** in `references/ship-policy.md`. For ad hoc inline issues, the new issue title and commit subject must match (see **Naming anchor**).

5. **Draft the issue-close comment** — plain-English **What changed** + **How to confirm it's fixed** from the diff (format above). If the underlying test plan isn't obvious, ask the user before continuing.

   Before presenting drafts, run the **Authorship policy** scrub and, if env files/keys changed, the **Env parity policy** sync pass — both in `references/ship-policy.md`.

6. **Show the user the drafts** and wait for approval before any write action. This is one combined confirmation, not three:
   - Existing issue: commit message + close comment.
   - Inline-created issue: new-issue title + new-issue body + chosen category/state labels + commit message + close comment. After approval, create the issue first, then commit/push/close in order.

   If the user is away, present the drafts and stop — never commit, push, or close unapproved.

7. **Pre-commit safety** — apply every check in **Pre-commit safety** (`references/ship-policy.md`) before staging.

8. **Commit** using the quoted-HEREDOC form in **Commit message format** (`references/ship-policy.md`).

9. **Push** the current branch:
   - Tracks a remote → `git push`.
   - No upstream → `git push -u origin <branch>`.
   - **If the current branch is the detected default branch**: stop and confirm separately before pushing — step 6's approval does not cover this push. If the user is away, leave the commit local and unpushed, skip the close (a close comment must reference a pushed commit), and surface both under Needs user in the report.
   - **Confirm the push landed** before the close — non-error exit and `git status -sb` shows the branch up-to-date with its remote. A rejected push (non-fast-forward, auth expiry) stops the close, since the close comment must reference a commit that is actually on `<branch>`.

10. **Close the issue** — first, when the underlying test plan contains a runnable test command, run it once — a failing run stops the close: leave the issue open, report the failure (the commit is already pushed), and treat any fix as a new iteration through this skill; never close an issue whose own test plan fails. On a pass, state the outcome in plain English in **How to confirm it's fixed** (e.g. "Automated checks confirm repeat submissions no longer double-charge") — never paste the raw command or its output into the comment. Then fill the drafted comment with the real values (short SHA from `git rev-parse --short HEAD`, current branch), write it to a temp file, then comment, close, and verify:
    ```bash
    gh issue comment <num> --body-file <temp-file>.md
    gh issue close <num> --reason completed
    gh issue view <num> --json state -q .state   # expect CLOSED
    ```
    The body file keeps backticks and `$` literal — nothing to escape and nothing for the shell to interpolate. "Closed" is earned by the state check, not assumed from a zero exit code; quote the returned state in the report.

11. **Report** — one line: `<SHA> pushed to <branch>; issue #<num> closed (state CLOSED verified)`. If the push and close were skipped (default branch, user away), report instead `<SHA> committed locally on <branch>; push and close deferred`, then a `Needs user:` line naming the default-branch-push confirmation still required. If the push was attempted and rejected (non-fast-forward, auth expiry — step 9), report `<SHA> committed locally on <branch>; push REJECTED (<reason>), close stopped`, then a `Needs user:` line naming the push fix required (rebase/pull, re-auth) before this iteration can finish — this is a failure, not a deferral. In every case, append the **Response footer** from `references/ship-policy.md` (1-3 advisory suggestions).

## Example

The matching commit message lives in **Commit examples** (`references/ship-policy.md`, issue #418).

Close comment:
```
Closed by 9f0e1a2 on `feat/418-idempotency`.

**What changed**
If a customer's checkout request gets sent twice by accident, we now only charge them once — the second attempt just returns the same result instead of creating a duplicate charge.

**How to confirm it's fixed**
1. Submit a checkout twice in a row with the same order.
2. The second submission returns the same confirmation as the first — no extra charge is created.
3. Submitting two different orders still charges each one separately, as before.
   Automated checks confirm this behavior end to end.

Notes: The Stripe webhook path isn't covered by this fix yet — see follow-up #419.
```

## Completion criteria

- [ ] `gh issue view <num> --json state -q .state` returned `CLOSED`, and that state is quoted in the report
- [ ] Close comment posted containing **What changed** + **How to confirm it's fixed**, both in plain English with no code identifiers, commands, or raw test output; when the underlying test plan has a runnable command, its pass/fail outcome is confirmed before closing but stated in plain English in the comment, never quoted verbatim
- [ ] Push landed: non-error exit and `git status -sb` shows the branch up-to-date with its remote — or the report carries the deferral/rejection line plus `Needs user:`
- [ ] `Issue:` line present in the commit body
- [ ] Label state valid: `gh issue view <num> --json labels` shows one category label + a ready state label (read in step 3, or set at inline creation)
- [ ] No co-author or AI/tool attribution text present in the commit message, issue content, or comments
- [ ] Hooks ran on the commit — no `--no-verify` in the command that made it

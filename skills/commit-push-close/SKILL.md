---
name: commit-push-close
disable-model-invocation: true
description: Ship one iteration of issue work directly — commit with a structured message, push, then close the linked issue with a comment that explains how to test the change; creates the issue inline when none exists. Use when the user says "commit, push, and close" or "ship this issue" and wants the issue closed without a PR (a reviewable PR is /commit-push-pr).
---

# commit-push-close

The boundary against `/commit-push-pr`: same shared ship policy, but this skill closes the linked issue directly instead of ending in a PR with `Closes #N`.

Issue commands show the GitHub default; a workspace-named tracker overrides them per **Tracker** in `references/ship-policy.md`.

## Shared ship policy

Read [`references/ship-policy.md`](references/ship-policy.md) first — it holds every shared ship rule the steps below cite by bold section name, **Read state** through the **Response footer**. This `SKILL.md` only covers what is specific to closing the issue directly.

## Issue-close comment format

Posted on the issue right before closing. PMs and stakeholders read it with no diff alongside — plain English throughout: no code identifiers, file paths, commands, or jargon. Optional sections are omitted when empty.

```
Closed by <SHA> on `<branch>`.

**What changed**
<one or two plain-English sentences — what a user or the business would notice, not what the code does>

**How to confirm it's fixed**
1. <step in everyday language>
2. <step in everyday language>
3. <what you should see, stated as a plain result>

Notes: <follow-ups or known gaps, in plain English; omit line if none>
```

Draft **How to confirm it's fixed** from the same underlying test plan as **How-to-test rules**, translated out of code — action and outcome in everyday words. A step with no user-facing surface names the capability it protects (e.g. "repeat submissions no longer double-charge"), not the test file.

## Workflow

Emit `Stage / Found / Next / Needs user` at each phase transition — one line per field.

1. **Read state** — run the **Read state** commands in `references/ship-policy.md`. If the current branch is not the detected default, the code this close refers to may sit unmerged — say so and confirm direct close vs routing to `/commit-push-pr`; likewise when the repo requires PRs. If the user is away, continue drafting and surface this choice with the step-6 drafts — that combined approval remains the hard gate.

2. **Resolve or create the issue** — check, in order: branch name (e.g. `feat/123-...`, `agent/PROJ-456-...`), recent commits, conversation context. If none, switch to **Inline issue creation** for valid small ad hoc work — drafted now, created only after step 6's combined approval; once created, fill its number into the commit `Issue:` line and step 10's `<num>`.

3. **Read issue labels** — for pre-existing issues, run `gh issue view <num> --json state,labels,title,url` and validate against the **Label validation** table, following its outcomes (stop states route to `/triage`; the taxonomy-absence fallback applies). Already `CLOSED` → stop and ask: reopen for this iteration, comment without closing, or target a different issue. Skip for issues just created inline — labels were set at creation.

4. **Draft the commit message** from the issue title and diff, per **Commit message format** and **Naming anchor**.

5. **Draft the issue-close comment** — plain-English **What changed** + **How to confirm it's fixed** from the diff (format above). If the underlying test plan isn't obvious, ask the user before continuing.

   Before presenting drafts, run the **Authorship policy** scrub and, if env files/keys changed, the **Env parity policy** sync pass.

6. **Show the user the drafts** and wait for approval before any write action — one combined confirmation, not three:
   - Existing issue: commit message + close comment.
   - Inline-created issue: new-issue title + body + category/state labels + commit message + close comment. After approval, create the issue first, then commit/push/close in order.

   If the user is away, present the drafts and stop — never commit, push, or close unapproved.

7. **Pre-commit safety** — apply every check in **Pre-commit safety** before staging.

8. **Commit** using the quoted-HEREDOC form in **Commit message format**.

9. **Push** the current branch:
   - Tracks a remote → `git push`.
   - No upstream → `git push -u origin <branch>`.
   - **If the current branch is the detected default branch**: stop and confirm separately before pushing — step 6's approval does not cover this push. If the user is away, leave the commit unpushed, skip the close (a close comment must reference a pushed commit), and surface both under Needs user in the report.
   - **Confirm the push landed** before the close — non-error exit and `git status -sb` shows the branch up-to-date with its remote. A rejected push (non-fast-forward, auth expiry) stops the close.

10. **Close the issue** — when the underlying test plan contains a runnable test command, run it once first — a failing run stops the close: leave the issue open, report the failure (the commit is already pushed), and treat any fix as a new iteration through this skill; never close an issue whose own test plan fails. On a pass, state the outcome in plain English in **How to confirm it's fixed** — never paste the raw command or its output into the comment. Fill the drafted comment with the real values (short SHA via `git rev-parse --short HEAD`, current branch), write it to a temp file, then comment, close, and verify:
    ```bash
    gh issue comment <num> --body-file <temp-file>.md
    gh issue close <num> --reason completed
    gh issue view <num> --json state -q .state   # expect CLOSED
    ```
    The body file keeps backticks and `$` literal — nothing for the shell to interpolate. "Closed" is earned by the state check, not a zero exit code; quote the returned state in the report.

11. **Report** — one line: `<SHA> pushed to <branch>; issue #<num> closed (state CLOSED verified)`. Push and close skipped (default branch, user away) → `<SHA> committed locally on <branch>; push and close deferred`, then a `Needs user:` line naming the confirmation still required. Push attempted and rejected (step 9) → `<SHA> committed locally on <branch>; push REJECTED (<reason>), close stopped`, then a `Needs user:` line naming the fix required (rebase/pull, re-auth) — a failure, not a deferral. In every case, append the **Response footer**.

## Example

The matching commit message lives in **Commit examples** (issue #418).

Close comment:
```
Closed by 9f0e1a2 on `feat/418-idempotency`.

**What changed**
If a customer's checkout request is accidentally sent twice, we now charge them only once — the second attempt returns the same result instead of a duplicate charge.

**How to confirm it's fixed**
1. Submit the same checkout twice in a row.
2. The second submission returns the same confirmation — no extra charge is created.
3. Submitting two different orders still charges each separately.
   Automated checks confirm this behavior end to end.

Notes: The Stripe webhook path isn't covered by this fix yet — see follow-up #419.
```

## Completion criteria

- [ ] Issue verified closed — `gh issue view <num> --json state -q .state` → `CLOSED` (or the workspace tracker's completed state) — quoted in the report
- [ ] Close comment posted with **What changed** and **How to confirm it's fixed** both present, and any runnable test in its plan ran green before the close
- [ ] Push landed: non-error exit and `git status -sb` shows the branch up-to-date with its remote — or the report carries the deferral/rejection line plus `Needs user:`
- [ ] `Issue:` line present in the commit body
- [ ] Label state valid: `gh issue view <num> --json labels` shows one category label + a ready state label
- [ ] No co-author or AI/tool attribution text present in the commit message, issue content, or comments
- [ ] Hooks ran on the commit — no `--no-verify` in the command that made it

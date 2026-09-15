---
name: commit-push-close
disable-model-invocation: true
description: Ship one iteration of issue work directly — commit with a structured message, push, then close the linked issue with a comment that explains how to test the change; creates the issue inline when none exists. Use when the user says "commit, push, and close", "close out an issue with testing steps", "ship this issue", or is done and says "ship it" without requesting a PR. A reviewable PR is /commit-push-pr.
---

# commit-push-close

The boundary against `/commit-push-pr`: same shared ship policy, but this skill closes the linked issue directly instead of ending in a PR with `Closes #N`.

Issue commands show the GitHub default; a workspace-named tracker overrides them per **Tracker** in `references/ship-policy.md`.

## Shared ship policy

Read [`references/ship-policy.md`](references/ship-policy.md) first — it holds every shared ship rule the steps below cite by bold section name, **Read state** through the **Response footer**. This `SKILL.md` only covers what is specific to closing the issue directly.

## Issue-close comment format

Post on the issue before closing. Use the complete **QA handoff** template in **How-to-test rules**, including product locations, exact changed paths, setup, actions with expected results, and verification status. Zero attribution: never add or leave co-author, AI, or tool attribution in commits, issues, or comments.

```
Implemented in <SHA> on `<branch>`.
<QA handoff from the shared policy>
```

Use "Implemented in" because comment posting and issue closure are separate operations; claim closure only after reading back the completed state.

## Workflow

Emit `Stage / Found / Next / Needs user` at each phase transition — one line per field.

1. **Read state** — resolve the task checkout through **Worktree handoff**, then run the **Read state** commands in `references/ship-policy.md`. If the current branch is not the detected default, the code this close refers to may sit unmerged — say so and confirm direct close vs routing to `/commit-push-pr`; likewise when the repo requires PRs. If the user is away, continue drafting and surface this choice with the step-6 drafts — that combined approval remains the hard gate.

2. **Resolve or create the issue** — check, in order: branch name (e.g. `feat/123-...`, `agent/PROJ-456-...`), recent commits, conversation context. If none, switch to **Inline issue creation** for valid small ad hoc work — drafted now, created only after step 6's combined approval; once created, fill its number into the commit `Issue:` line and step 10's `<num>`.

3. **Read issue labels** — for pre-existing issues, run `gh issue view <num> --json state,labels,title,url` and validate against the **Label validation** table, following its outcomes (stop states route to `/triage`; the taxonomy-absence fallback applies). Already `CLOSED` → stop and ask: reopen for this iteration, comment without closing, or target a different issue. Skip for issues just created inline — labels were set at creation.

4. **Draft the commit message** from the issue title and diff, per **Commit message format** and **Naming anchor**.

5. **Draft the issue-close comment** using **How-to-test rules**. Run applicable local pass/fail checks before shipping, and put actual results in the draft. If the plan isn't clear from the diff and repo, ask for the missing information before continuing.

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

10. **Close the issue** — check that test evidence still covers the pushed content; rerun if content changed. A failure stops closure. Fill the QA draft with the actual SHA and branch and write it to a temp file. Post and read back the comment before closing:
    ```bash
    gh issue comment <num> --body-file <temp-file>.md
    gh issue view <num> --json comments
    # Match the posted comment body and URL to the draft before closing.
    gh issue close <num> --reason completed
    gh issue view <num> --json state -q .state   # expect CLOSED
    ```
    If comment posting or read-back fails, leave the issue open. If closing fails, report the pushed SHA and posted comment URL and leave closure incomplete. Resume only the missing action on retry. "Closed" requires the returned completed state.

11. **Report** — `<SHA> pushed to <branch>; issue #<num> closed (state CLOSED verified); QA: <comment URL>`. For partial completion, name the actual completed operations and the failed or deferred operation with its reason. Include any required user action. Append the **Response footer**.

## Example

The matching commit message lives in **Commit examples** (issue #418).

Close comment:
```
Implemented in 9f0e1a2 on `feat/418-idempotency`.

## QA handoff
Change: 9f0e1a2 on `feat/418-idempotency`.

### What changed
Repeated checkout requests now return the original confirmation without a second charge.

### Where changed
- Checkout, `POST /checkout`: `server/checkout/handler.ts` handles replayed request IDs.
- `server/checkout/handler.test.ts` covers replay and concurrent requests.

### Setup
Use the local app at this revision, a test account and the repo's payment sandbox. No real charges. Follow the repo's local setup instructions.

### How to test
1. Submit a test checkout and resend it with the same `x-request-id`. Expect the original confirmation and one charge.
2. Submit a different test order with a new request ID. Expect a separate confirmation and charge.
3. Run `pnpm test server/checkout/handler.test.ts`. Expect all replay and race tests to pass.

### Verification
Automated check: 1 test file and 6 tests passed. Manual payment checks pending.

### Gaps
Webhook handling remains outside this fix, follow-up #419. Remove test orders after manual QA.
```

## Completion criteria

- [ ] Issue verified closed — `gh issue view <num> --json state -q .state` → `CLOSED` (or the workspace tracker's completed state) — quoted in the report
- [ ] Posted QA comment read back with the correct SHA, changed locations/paths, setup, steps and expected results, verification and gaps; URL included in report
- [ ] Required checks passed on the shipped content before push; manual checks not performed are marked pending
- [ ] Push landed: non-error exit and `git status -sb` shows the branch up-to-date with its remote — or the report carries the deferral/rejection line plus `Needs user:`
- [ ] `Issue:` line present in the commit body
- [ ] Labels read back as one category plus a ready state, or the explicit taxonomy-fallback decision is recorded
- [ ] No co-author or AI/tool attribution text present in the commit message, issue content, or comments
- [ ] Hooks ran on the commit — no `--no-verify` in the command that made it

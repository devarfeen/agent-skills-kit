---
name: commit-push-pr
disable-model-invocation: true
description: Ship one iteration of issue work as a pull request — commit with a structured message, push the branch, and open a PR whose `Closes #N` auto-closes the issue on merge; creates the issue inline when none exists. Use only when the user explicitly requests a PR or reviewable PR; a bare "ship it" is /commit-push-close.
---

# commit-push-pr

This skill ends in a PR awaiting review with a QA comment. `/commit-push-close` closes the issue directly. GitHub closing keywords take effect on merge into the repository's default branch; other targets need the workspace's issue-completion workflow.

Issue commands show the GitHub default; a workspace-named tracker overrides them per **Tracker** in `references/ship-policy.md`.

## Shared ship policy

Read [`references/ship-policy.md`](references/ship-policy.md) first — it holds every shared ship rule the steps below cite by bold section name, **Read state** through the **Response footer**. This `SKILL.md` only covers what is specific to opening a PR.

## PR title and body

**Title** mirrors the commit subject.

**Body**:

```
Closes #<num>

## Summary
<one or two sentences — what changed and why>

## Where changed
<product location and meaningful repo-relative paths, with what changed in each>

## Decisions
- <only non-obvious choices; omit section if none>

## How to test
1. <step>
2. <step>
3. <expected result>

## Notes
- <follow-ups or known gaps; omit section if none>
```

**How to test** follows **How-to-test rules**, including setup, expected results and actual verification status. Also draft a separate PR comment using that policy's complete **QA handoff** template. Keep the body and comment consistent. Zero attribution: never add or leave co-author, AI, or tool attribution in commits, PRs, issues, or comments.

For a default-branch PR, `Closes #N` is mandatory near the top. Multiple issues each need a closing keyword. For a permitted non-default target, use an ordinary issue reference and explain when the workspace completes it; never promise automatic closure there.

## Workflow

Emit `Stage / Found / Next / Needs user` at each phase transition — one line per field.

1. **Read state** — resolve the task checkout through **Worktree handoff**, then run **Read state** in the shared policy. Resolve the PR base from explicit user/workspace instructions, then an existing PR, then the detected default. Stop on conflicts or a prohibited production target; never default into a forbidden branch.

2. **Resolve or create the issue** — branch name → recent commits → conversation context. If none, use **Inline issue creation** for valid small ad hoc work. Create only after step 7 approval, then insert the actual number into the commit and PR issue reference.

3. **Read issue labels** — run `gh issue view <num> --json state,labels,title,url` and apply **Label validation**, including its taxonomy-absence fallback. Stop states route to `/triage`. Already `CLOSED` → stop and ask whether to reopen or target another issue; never open a PR against an issue that will remain closed. Inline creation includes its own read-back.

4. **Branch handling** — if the current branch is the detected default branch (`main`/`master`):
   - Stop before staging anything.
   - Propose `issue/<issue-num>-<slug>` (`<slug>`: short kebab-case from the issue title, ≤ 5 words). An inline-drafted issue has no number yet — propose `issue/<slug>`; the PR's `Closes #<num>` line does the linking, not the branch name.
   - Wait for the user to confirm the name (offer to edit). If the user is away, proceed with the proposed name — step 7's combined approval remains the hard gate.
   - `git checkout -b <branch>` — uncommitted changes follow the checkout.
   Otherwise, continue on the current branch.

5. **Draft the commit message** from the issue title and diff, per **Commit message format** and **Naming anchor**.

6. **Draft the PR and QA comment** — title mirrors the commit subject. Follow **How-to-test rules** and run the applicable local pass/fail checks now. Quote the decisive result in both drafts and mark unperformed manual checks pending. A failure stops shipping; an unclear plan requires the missing information.

   Before presenting drafts, run the **Authorship policy** scrub and, if env files/keys changed, the **Env parity policy** sync pass.

7. **Show the user the drafts** and wait for one combined approval. Do not stage, push, or call `gh pr create` before approval:
   - Existing issue: commit message + PR title/body + QA comment + target branch.
   - Inline-created issue: also include new-issue title/body and category/state labels. After approval, create the issue first, then commit/push/PR/comment in order.

   This approval is a deliberate hard gate before any remote write. If the user is away, present the drafts and stop — never stage, push, or open a PR unapproved.

8. **Pre-commit safety** — apply every check in **Pre-commit safety** before staging.

9. **Commit** using the quoted-HEREDOC form in **Commit message format**.

10. **Push** the current branch:
    - Tracks a remote → `git push`.
    - No upstream → `git push -u origin <branch>`.
    - Verify the intended remote branch SHA as required by **Read state**. A rejected or mismatched push stops PR creation/edit and commenting.

11. **Open or update the PR** against the permitted base resolved in step 1. Test evidence must cover the committed content; rerun when content changed, not merely because timing output differs. A failed check stops publication. Save the final body to a file, then:
    ```bash
    gh pr create \
      --base "<resolved-base>" \
      --head "<current-branch>" \
      --title "<subject>" \
      --body-file <pr-body-file>.md
    ```
    - Check for an existing PR first with `gh pr list --head <branch> --json number,baseRefName,headRefName`. Update the matching PR using `gh pr edit <num> --body-file <pr-body-file>.md`; resolve ambiguous matches instead of guessing. Preserve unrelated human-authored body sections.
    - Read back with `gh pr view <pr-num> --json title,body,baseRefName,headRefName,url`. Verify title, issue reference, resolved base, current head and test plan. Correct mismatches and re-read.
    - Fill the QA comment with the actual SHA, branch and PR URL. Post using `gh pr comment <pr-num> --body-file <qa-comment-file>.md`, then read back with `gh pr view <pr-num> --json comments` and verify the body and URL. Apply the shared comment retry rule. A failed comment leaves the PR created but QA handoff incomplete; report and resume the missing step.

12. **Report** — `<SHA> pushed to <branch>; PR #<pr-num> opened/updated against <base>; QA: <comment URL>`. State the actual issue-completion behavior and any incomplete step. Append the **Response footer**. Stop before merge or direct issue closure.

## Example

The matching commit message lives in **Commit examples** (issue #418). Optional sections (**Decisions**, **Notes**) are simply omitted when empty.

PR title: `add idempotency keys to checkout flow`

PR body:
```
Closes #418

## Summary
Checkout charges are now idempotent on `x-request-id`; replays return the original result instead of double-charging.

## Where changed
`POST /checkout`, implemented in `server/checkout/handler.ts`; replay tests in `server/checkout/handler.test.ts`.

## Decisions
- Stored keys in Redis (24h TTL) over Postgres — the read path is hot
- Reused existing `x-request-id` header instead of a new one

## How to test
Setup: run this branch locally with a test account and the repo's payment sandbox.
1. `pnpm test server/checkout/handler.test.ts` — passing tail quoted below:
       Test Files  1 passed (1)
            Tests  6 passed (6)
         Duration  1.24s
2. Hit `POST /checkout` twice with the same `x-request-id` — second call returns the first response, no second Stripe charge
3. Hit twice with different IDs — two distinct charges as before
Manual API checks pending. Remove test orders afterward.

## Notes
- Stripe webhook path still unguarded — see follow-up #419
```

## Completion criteria

- [ ] Push landed — `git status` shows the branch up to date with its upstream
- [ ] PR read back: title, permitted base, head, issue reference, and test plan match the final drafts
- [ ] Separate QA comment posted and read back with actual SHA, changed locations/paths, setup, expected results and verification status; URL reported
- [ ] When the test plan contains a pass/fail test or validation command, its passing output tail is quoted in the PR body
- [ ] No co-author or AI/tool attribution text in the commit message, PR title/body, or issue content
- [ ] Hooks ran (no `--no-verify`)
- [ ] Report line printed and the `Suggested next skills (optional)` footer appended

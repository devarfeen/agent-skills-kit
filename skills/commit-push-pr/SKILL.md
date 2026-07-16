---
name: commit-push-pr
disable-model-invocation: true
description: Ship one iteration of GitHub-issue work as a pull request — commit with a structured message, push the branch, and open a PR whose `Closes #N` auto-closes the issue on merge; creates the issue inline when none exists. Use when the user says "commit, push, and open a PR" or wants issue work wrapped up as a reviewable PR rather than a direct close (a direct close is /commit-push-close).
---

# commit-push-pr

Ship one GitHub-issue iteration as a reviewable pull request whose `Closes #N` line auto-closes the issue on merge. The boundary against `/commit-push-close`: that skill ends by closing the issue directly; this one ends in a PR awaiting review.

## Shared ship policy

Read [`references/ship-policy.md`](references/ship-policy.md) first. It holds the rules both ship skills share and that this workflow depends on: **Read state**, **Label validation**, **Authorship policy**, **Env parity policy**, **Inline issue creation**, **Naming anchor**, **How-to-test rules**, **Commit message format** (with the HEREDOC form and commit examples), **Pre-commit safety**, and the **Response footer**. This `SKILL.md` only covers what is specific to opening a PR.

## PR title and body

**Title** mirrors the commit subject.

**Body**:

```
Closes #<num>

## Summary
<one or two sentences — what changed and why>

## Decisions
- <only non-obvious choices; omit section if none>

## How to test
1. <step>
2. <step>
3. <expected result>

## Notes
- <follow-ups or known gaps; omit section if none>
```

Rules for **How to test** live in **How-to-test rules** (`references/ship-policy.md`).

The `Closes #N` line is mandatory and must be on its own line near the top of the body so GitHub auto-links and auto-closes the issue on merge. If linking multiple issues, list them as `Closes #1, closes #2` (each needs its own `closes` keyword).

## Workflow

1. **Read state** — run the **Read state** commands in `references/ship-policy.md` (parallel git reads, default-branch detection, `gh` availability check).

2. **Resolve or create the issue** — branch name → recent commits → conversation context. If none, switch to **Inline issue creation** (`references/ship-policy.md`) for valid small ad hoc work — the issue is drafted now but created only after the combined approval in step 7; once created, fill its number into the commit `Issue:` line and the PR `Closes #<num>`.

3. **Read issue labels** — for issues that already existed, run `gh issue view <num> --json state,labels,title,url` and validate against the **Label validation** table in `references/ship-policy.md`. If labels are missing/conflicting or the state is `needs-triage`, `needs-info`, or `wontfix`, stop and route back to `/triage`. If the issue is already `CLOSED`, stop and ask — reopen it for this iteration, or target a different issue (for genuinely new work, **Inline issue creation** applies); `Closes #N` stays mandatory, so never open a PR against an issue that will remain closed. For issues just created inline, skip this step — labels were set at creation.

4. **Branch handling** — if the current branch is `main` or `master` (or the detected default branch):
   - Stop before staging anything.
   - Propose a feature branch name: `issue/<issue-num>-<slug>` where `<slug>` is a short kebab-case derivation of the issue title (≤ 5 words). For an inline-drafted issue there is no number yet (creation waits for step 7's approval) — propose `issue/<slug>`; the PR's `Closes #<num>` line does the linking, not the branch name.
   - Wait for the user to confirm the name (offer to edit). If the user is away, proceed with the proposed name — step 7's combined approval remains the hard gate.
   - `git checkout -b <branch>` — uncommitted changes follow the checkout into the new branch.
   Otherwise, continue on the current branch.

5. **Draft the commit message** from the issue title and diff, per **Commit message format** in `references/ship-policy.md`. For ad hoc inline issues, the new issue title and commit subject must match (see **Naming anchor**).

6. **Draft the PR title and body** — title mirrors the commit subject with no routing marker; body has `Closes #N`, summary, optional decisions, how-to-test, optional notes (format above). If the test plan isn't obvious, ask the user before continuing. If the how-to-test plan opens with a test or validation command — one that passes or fails, not a long-running server — run it now and paste the passing tail into the drafted body, so the body the user approves in step 7 is the final body. A failing run stops here (fix or ask).

   Before presenting drafts, run the **Authorship policy** scrub and, if env files/keys changed, the **Env parity policy** sync pass — both in `references/ship-policy.md`.

7. **Show the user the drafts** and wait for one combined approval. Do not stage, push, or call `gh pr create` before approval:
   - Existing issue: commit message + PR title + PR body.
   - Inline-created issue: new-issue title + new-issue body + chosen category/state labels + commit message + PR title + PR body. After approval, create the issue first, then commit/push/PR in order.

   This approval is a deliberate hard gate before any remote write. If the user is away, present the drafts and stop — never stage, push, or open a PR unapproved.

8. **Pre-commit safety** — apply every check in **Pre-commit safety** (`references/ship-policy.md`) before staging.

9. **Commit** using the quoted-HEREDOC form in **Commit message format** (`references/ship-policy.md`).

10. **Push** the current branch:
    - Tracks a remote → `git push`.
    - No upstream → `git push -u origin <branch>`.

11. **Open the PR** against the detected default branch. When the how-to-test
    plan opens with a test or validation command, confirm the passing tail
    already quoted into the approved body (step 6) still holds against the
    just-pushed commit before calling `gh pr create` — never open a PR whose
    own test plan fails.
    Then:
    ```bash
    gh pr create \
      --base "<default-branch>" \
      --head "<current-branch>" \
      --title "<subject>" \
      --body "$(cat <<'EOF'
    Closes #123

    ## Summary
    ...

    ## How to test
    1. ...
    2. ...
    3. ...
    EOF
    )"
    ```
    - If a PR already exists for this branch (`gh pr list --head <branch> --json number`), do not create a duplicate. Update the existing PR's title/body with `gh pr edit <num>` instead, and report that path back.
    - **Read the PR back** after create or edit: `gh pr view <pr-num> --json title,body,baseRefName,headRefName,url` — the title matches the commit subject, `Closes #<num>` sits on its own line in the body, base is the default branch, head is the current branch. Fix any mismatch with `gh pr edit` and re-read before reporting.

12. **Report** — one line: `<SHA> pushed to <branch>; PR #<pr-num> opened (Closes #<issue-num>)`. Then append the **Response footer** from `references/ship-policy.md` (1-3 advisory suggestions).

## Example

The matching commit message lives in **Commit examples** (`references/ship-policy.md`, issue #418). Optional sections (**Decisions**, **Notes**) are simply omitted when empty.

PR title: `add idempotency keys to checkout flow`

PR body:
```
Closes #418

## Summary
Checkout charges are now idempotent on `x-request-id`; replays return the original result instead of double-charging.

## Decisions
- Stored keys in Redis (24h TTL) over Postgres — the read path is hot
- Reused existing `x-request-id` header instead of introducing a new one

## How to test
1. `pnpm test server/checkout/handler.test.ts` — passing tail quoted below:
       Test Files  1 passed (1)
            Tests  6 passed (6)
         Duration  1.24s
2. Hit `POST /checkout` twice with the same `x-request-id` — second call returns the first response, no second Stripe charge
3. Hit twice with different IDs — two distinct charges as before

## Notes
- Stripe webhook path still unguarded — see follow-up #419
```

## Completion criteria

- [ ] Push landed — `git status` shows the branch up to date with its upstream
- [ ] PR read back (`gh pr view --json title,body,baseRefName,headRefName`): title, base, head, and the `Closes #<num>` line on its own all verified
- [ ] When the test plan opens with a pass/fail test or validation command, its passing output tail is quoted in the PR body
- [ ] No co-author or AI/tool attribution text in the commit message, PR title/body, or issue content
- [ ] Hooks ran (no `--no-verify`)
- [ ] Report line printed and the `Suggested next skills (optional)` footer appended (1-3 advisory suggestions, no gating)

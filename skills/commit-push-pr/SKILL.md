---
name: commit-push-pr
description: Ship one iteration of work on a GitHub issue as a pull request — stage and commit with a structured message, push the current branch, and open a PR that uses `Closes #N` to auto-close the linked issue on merge. If no GitHub issue can be located, the skill creates one inline before committing for valid small ad hoc work. Routing state lives in issue labels, not commit or PR title markers. Use when the user says "commit, push, and open a PR", "ship this as a PR", "PR this issue", or otherwise wants to wrap up issue work as a reviewable PR rather than a direct close.
---

# commit-push-pr

Ship one GitHub-issue iteration as a reviewable PR (with an inline create-if-missing step for the issue):

1. **Resolve or create** the GitHub issue.
2. **Commit** the diff with a structured message.
3. **Push** the current branch (when starting from the default branch, a confirmed feature branch is created first — step 4 of the workflow).
4. **Open a PR** with `Closes #N`, a summary, and a how-to-test plan.

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

6. **Draft the PR title and body** — title mirrors the commit subject with no routing marker; body has `Closes #N`, summary, optional decisions, how-to-test, optional notes (format above). If the test plan isn't obvious, ask the user before continuing.

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

11. **Open the PR** against the detected default branch. First, when the
    How-to-test plan opens with a runnable test command, run it once and quote
    the passing tail in the PR body — a failing run stops the PR (fix or ask);
    never open a PR whose own test plan fails. Then:
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

12. **Report** — one line: `<SHA> pushed to <branch>; PR #<pr-num> opened (Closes #<issue-num>)`. Then append the **Response footer** from `references/ship-policy.md` (1-6 advisory suggestions).

## Examples

The matching commit messages live in **Commit examples** (`references/ship-policy.md`, issues #204 and #418).

### Minimal

PR title: `wire signup form to /api/users`

PR body:
```
Closes #204

## Summary
Signup form now POSTs to /api/users and surfaces server errors inline.

## How to test
1. `pnpm dev`, open http://localhost:3000/signup
2. Submit with a duplicate email — expect inline "email already in use"
3. Submit with a fresh email — expect redirect to /welcome
```

### Full

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
1. `pnpm test server/checkout/handler.test.ts` — all green
2. Hit `POST /checkout` twice with the same `x-request-id` — second call returns the first response, no second Stripe charge
3. Hit twice with different IDs — two distinct charges as before

## Notes
- Stripe webhook path still unguarded — see follow-up #419
```

## Checklist

Before reporting done, verify:
- [ ] Issue resolved (or created inline) + labels read/created → one category label + ready state label
- [ ] If on default branch, a feature branch was created and confirmed
- [ ] Commit subject mirrors the GitHub issue title as closely as practical and has no routing marker
- [ ] `Issue:` line present in commit body
- [ ] No co-author or AI/tool attribution text in commit message, PR title/body, issue content, comments, release notes, or docs
- [ ] If env keys changed: existing env-family key sets synchronized, sample/example updated, docs updated, gitignored copies updated locally and reported (**Env parity policy**)
- [ ] No secret files staged
- [ ] Hooks ran (no `--no-verify`)
- [ ] Push succeeded with upstream set
- [ ] PR body has `Closes #<num>` on its own line near the top
- [ ] PR body has **Summary** + **How to test**
- [ ] If the test plan opens with a runnable command, it ran green and its output tail is quoted in the body (a failure stopped the PR)
- [ ] No duplicate PR created (existing PR was edited instead)
- [ ] Final report line printed
- [ ] Optional `Suggested next skills` footer included (1-6 advisory suggestions, no gating)

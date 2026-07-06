---
name: commit-push-close
description: Ship one iteration of work on a GitHub issue — stage and commit with a structured message, push to the current branch, then close the linked GitHub issue with a comment that explains how to test the change. If no GitHub issue can be located, the skill creates one inline before committing for valid small ad hoc work. Routing state lives in issue labels, not commit subject markers. Use when the user says "commit, push, and close", "ship this issue", "I'm done with this issue", or otherwise wants to wrap up issue work in one step.
---

# commit-push-close

Four-step ship for one GitHub-issue iteration (with an inline create-if-missing step for the issue):

1. **Resolve or create** the GitHub issue.
2. **Commit** the diff with a structured message.
3. **Push** to the current branch.
4. **Close** the GitHub issue with a comment explaining how to test it.

## Shared ship policy

Read [`references/ship-policy.md`](references/ship-policy.md) first. It holds the rules both ship skills share and that this workflow depends on: **Read state**, **Label validation**, **Authorship policy**, **Env parity policy**, **Inline issue creation**, **Naming anchor**, **How-to-test rules**, **Commit message format** (with the HEREDOC form and commit examples), **Pre-commit safety**, and the **Response footer**. This `SKILL.md` only covers what is specific to closing the issue directly.

## Issue-close comment format

Posted as a comment on the issue right before closing:

```
Closed by <SHA> on `<branch>`.

**Summary**
<one or two sentences — what changed and why>

**How to test**
1. <step>
2. <step>
3. <expected result>

Notes: <follow-ups or known gaps; omit line if none>
```

Rules for **How to test** live in **How-to-test rules** (`references/ship-policy.md`).

## Workflow

1. **Read state** — run the **Read state** commands in `references/ship-policy.md` (parallel git reads, default-branch detection, `gh` availability check). If the current branch is not the detected default branch, the code this close refers to may sit unmerged — say so and confirm the direct close vs routing to `/commit-push-pr`; confirm likewise when the repo requires PRs. If the user is away, continue drafting and surface this choice with the step-6 drafts — that combined approval remains the hard gate.

2. **Resolve or create the issue** — check, in order: branch name (e.g. `feat/123-...`, `agent/PROJ-456-...`), recent commits on this branch, conversation context. If no issue can be located, switch to **Inline issue creation** (`references/ship-policy.md`) for valid small ad hoc work — the issue is drafted now but created only after the combined approval in step 6; once created, fill its number into the commit `Issue:` line and use it as `<num>` in step 10.

3. **Read issue labels** — for issues that already existed, run `gh issue view <num> --json state,labels,title,url` and validate against the **Label validation** table in `references/ship-policy.md`, following its outcomes (stop states route to `/triage`; the taxonomy-absence fallback applies). If the issue is already `CLOSED`, stop and ask — reopen it for this iteration, comment without closing, or target a different issue. For issues just created inline, skip this step — labels were set at creation.

4. **Draft the commit message** from the issue title and diff, per **Commit message format** in `references/ship-policy.md`. For ad hoc inline issues, the new issue title and commit subject must match (see **Naming anchor**).

5. **Draft the issue-close comment** — summary + how-to-test from the diff (format above). If the test plan isn't obvious, ask the user before continuing.

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

10. **Close the issue** — first, when the How-to-test plan opens with a
    runnable test command, run it once and quote the passing tail in the close
    comment — a failing run stops the close: leave the issue open, report the
    failure (the commit is already pushed), and treat any fix as a new
    iteration through this skill; never close an issue whose own test plan
    fails. Then fill the drafted comment with the real
    values (short SHA from `git rev-parse --short HEAD`, current branch),
    write it to a temp file, then comment, close, and verify:
    ```bash
    gh issue comment <num> --body-file <temp-file>.md
    gh issue close <num> --reason completed
    gh issue view <num> --json state -q .state   # expect CLOSED
    ```
    The body file keeps backticks and `$` literal — nothing to escape and
    nothing for the shell to interpolate. "Closed" is earned by the state
    check, not assumed from a zero exit code; quote the returned state in the
    report.

11. **Report** — one line: `<SHA> pushed to <branch>; issue #<num> closed (state CLOSED verified)`. Then append the **Response footer** from `references/ship-policy.md` (1-6 advisory suggestions).

## Examples

The matching commit messages live in **Commit examples** (`references/ship-policy.md`, issues #204 and #418).

### Minimal

Close comment:
```
Closed by a1b2c3d on `feat/204-signup-wire`.

**Summary**
Signup form now POSTs to /api/users and surfaces server errors inline.

**How to test**
1. `pnpm dev`, open http://localhost:3000/signup
2. Submit with a duplicate email — expect inline "email already in use"
3. Submit with a fresh email — expect redirect to /welcome
```

### Full

Close comment:
```
Closed by 9f0e1a2 on `feat/418-idempotency`.

**Summary**
Checkout charges are now idempotent on `x-request-id`; replays return the original result instead of double-charging.

**How to test**
1. `pnpm test server/checkout/handler.test.ts` — ran green: `Tests 14 passed (14), Duration 1.2s`
2. Hit `POST /checkout` twice with the same `x-request-id` — second call returns the first response, no second Stripe charge
3. Hit twice with different IDs — two distinct charges as before

Notes: Stripe webhook path still unguarded — see follow-up #419.
```

## Checklist

Before marking the iteration done, verify:
- [ ] Issue resolved (or created inline) + labels read/created → one category label + ready state label
- [ ] Commit subject mirrors the GitHub issue title as closely as practical and has no routing marker
- [ ] `Issue:` line present in commit body
- [ ] No co-author or AI/tool attribution text in commit message, issue content, comments, release notes, or docs
- [ ] If env keys changed: existing env-family key sets synchronized, sample/example updated, docs updated, gitignored copies updated locally and reported (**Env parity policy**)
- [ ] No secret files staged
- [ ] Hooks ran (no `--no-verify`)
- [ ] Push succeeded (or, on the default branch, was confirmed separately; if the push was skipped user-away, the close was skipped with it)
- [ ] If the test plan opens with a runnable test command, it ran green and its output tail is quoted in the close comment (a failure stopped the close)
- [ ] Issue closed with comment containing **Summary** + **How to test**, and `gh issue view --json state` returned `CLOSED`
- [ ] Final report line printed
- [ ] Optional `Suggested next skills` footer included (1-6 advisory suggestions, no gating)

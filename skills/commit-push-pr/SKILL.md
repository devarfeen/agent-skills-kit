---
name: commit-push-pr
description: Ship one iteration of work on a GitHub issue as a pull request — stage and commit with a structured message, push the current branch, and open a PR that uses `Closes #N` to auto-close the linked issue on merge. The commit subject prefix is chosen by the issue's state label (`HITL:` for `ready-for-human`, `AKF:` for `ready-for-agent`). Use when the user says "commit, push, and open a PR", "ship this as a PR", "PR this issue", or otherwise wants to wrap up issue work as a reviewable PR rather than a direct close.
---

# commit-push-pr

Three-step ship for one GitHub-issue iteration, ending in a reviewable PR:

1. **Commit** the diff with a structured message (prefix chosen by issue state).
2. **Push** the current branch (auto-create one off `main`/`master` first).
3. **Open a PR** with `Closes #N`, a summary, and a how-to-test plan.

## Prefix selection

The subject prefix depends on the linked issue's state label:

| Issue state          | Prefix  |
| -------------------- | ------- |
| `ready-for-human`    | `HITL:` |
| `ready-for-agent`    | `AKF:`  |
| neither / no issue   | ask the user; do not guess |

Read state with: `gh issue view <num> --json state,labels,title,url`. Match label names exactly.

## Commit message format

```
<PREFIX> <one-line summary of the task completed>

Issue: #<num>

Decisions:
- <key decision 1>
- <key decision 2>

Files:
- <path> — <one-line why>
- <path> — <one-line why>

Notes:
- <blocker, follow-up, or signal for next iteration>
```

Rules:
- Subject ≤ 72 chars, starts with `HITL:` or `AKF:` + space, imperative mood.
- Always keep the subject and the `Issue:` line. Omit any other section that has nothing to say.
- Body under ~20 lines.

## PR title and body

**Title** mirrors the commit subject, including prefix:

```
<PREFIX> <one-line summary>
```

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

Rules for **How to test**:
- Concrete, runnable steps a reviewer can copy. Name the screen, command, endpoint, or button.
- UI: where to click, what to enter, what to see.
- API/server: exact `curl` or request, expected status/payload.
- Internal/refactor with no user-facing surface: `pnpm test path/to/file` (or equivalent) plus what should still work end-to-end.
- 3–6 steps. If you can't write a real test plan from the diff, ask the user before opening the PR — do not invent one.

The `Closes #N` line is mandatory and must be on its own line near the top of the body so GitHub auto-links and auto-closes the issue on merge. If linking multiple issues, list them as `Closes #1, closes #2` (each needs its own `closes` keyword).

## Workflow

1. **Read state** — run in parallel:
   - `git status` (no `-uall`)
   - `git diff` (staged + unstaged)
   - `git log -5 --oneline`
   - `git branch --show-current`
   - `git remote get-url origin`
   - Detect default branch: `gh repo view --json defaultBranchRef -q .defaultBranchRef.name` (fallback: `main`).

2. **Resolve the issue** — branch name → recent commits → conversation context. If none, ask the user. Do not invent.

3. **Read issue state** — `gh issue view <num> --json state,labels,title,url`. Pick `HITL:` or `AKF:` per the table. If neither label is present, ask.

4. **Branch handling** — if the current branch is `main` or `master` (or the detected default branch):
   - Stop before staging anything.
   - Propose a feature branch name: `<prefix-lc>/<issue-num>-<slug>` where `<prefix-lc>` is `hitl` or `akf` and `<slug>` is a short kebab-case derivation of the issue title (≤ 5 words).
   - Wait for the user to confirm the name (offer to edit).
   - `git checkout -b <branch>` — uncommitted changes follow the checkout into the new branch.
   Otherwise, continue on the current branch.

5. **Draft the commit message** from the diff (subject, decisions, files, notes per format above).

6. **Draft the PR title and body** — same prefix in title; body has `Closes #N`, summary, optional decisions, how-to-test, optional notes. If the test plan isn't obvious, ask the user before continuing.

7. **Show the user the drafts** (commit message + PR title + PR body) and wait for one combined approval. Do not stage, push, or call `gh pr create` before approval.

8. **Pre-commit safety**:
   - Refuse to stage secret-pattern files: `.env`, `.env.*` (except `.env.example`), `*.pem`, `*.key`, `id_rsa*`, `credentials*.json`, `*secret*`. Warn and skip.
   - Stage explicitly by path — never `git add -A` / `git add .`.
   - Honor hooks. Never `--no-verify`. If a hook fails, fix the underlying issue and create a NEW commit (do not amend).

9. **Commit** with HEREDOC:
   ```bash
   git commit -m "$(cat <<'EOF'
   AKF: <subject>

   Issue: #123

   Decisions:
   - ...

   Files:
   - ...
   EOF
   )"
   ```

10. **Push** the current branch:
    - Tracks a remote → `git push`.
    - No upstream → `git push -u origin <branch>`.

11. **Open the PR** against the detected default branch:
    ```bash
    gh pr create \
      --base "<default-branch>" \
      --head "<current-branch>" \
      --title "AKF: <subject>" \
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

12. **Report** — one line: `<prefix> <SHA> pushed to <branch>; PR #<pr-num> opened (Closes #<issue-num>)`. Done.

## Examples

### Minimal — `AKF:`

Commit:
```
AKF: wire signup form to /api/users

Issue: #204

Files:
- app/signup/page.tsx — submit handler + error state
- lib/api/users.ts — POST /users client
```

PR title: `AKF: wire signup form to /api/users`

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

### Full — `HITL:`

Commit:
```
HITL: add idempotency keys to checkout flow

Issue: #418

Decisions:
- Stored keys in Redis (24h TTL) over Postgres — read path is hot
- Reused existing `x-request-id` header instead of a new one

Files:
- server/checkout/handler.ts — key check before charge
- server/checkout/handler.test.ts — replay + race tests
- infra/redis.ts — TTL helper

Notes:
- Stripe webhook path still unguarded — next iteration
```

PR title: `HITL: add idempotency keys to checkout flow`

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
- [ ] Issue resolved + state read → correct prefix (`HITL:` or `AKF:`)
- [ ] If on default branch, a feature branch was created and confirmed
- [ ] Commit subject ≤ 72 chars, starts with prefix + space
- [ ] `Issue:` line present in commit body
- [ ] No secret files staged
- [ ] Hooks ran (no `--no-verify`)
- [ ] Push succeeded with upstream set
- [ ] PR body has `Closes #<num>` on its own line near the top
- [ ] PR body has **Summary** + **How to test**
- [ ] No duplicate PR created (existing PR was edited instead)
- [ ] Final report line printed

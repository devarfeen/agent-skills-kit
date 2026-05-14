---
name: commit-push-close
description: Ship one iteration of work on a GitHub issue — stage and commit with a structured message, push to the current branch, then close the linked GitHub issue with a comment that explains how to test the change. If no GitHub issue can be located, the skill creates one inline before committing. The commit subject prefix is chosen by the issue's state label (`HITL:` for `ready-for-human`, `AKF:` for `ready-for-agent`). Use when the user says "commit, push, and close", "ship this issue", "I'm done with this issue", or otherwise wants to wrap up work on a GitHub issue in one step.
---

# commit-push-close

Three-step ship for one GitHub-issue iteration (with an inline create-if-missing step for the issue):

1. **Resolve or create** the GitHub issue.
2. **Commit** the diff with a structured message (prefix chosen by issue state).
3. **Push** to the current branch.
4. **Close** the GitHub issue with a comment explaining how to test it.

## Prefix selection

The subject prefix depends on the linked issue's state label:

| Issue state          | Prefix  |
| -------------------- | ------- |
| `ready-for-human`    | `HITL:` |
| `ready-for-agent`    | `AKF:`  |
| neither              | ask the user which to use |
| no linked issue      | create one inline (see **Inline issue creation**) — the user picks the state label during creation, which fixes the prefix |

Read state with: `gh issue view <num> --json state,labels,title,url`. Match label names exactly.

## Inline issue creation

When step 2 of the workflow can't locate an issue, create one before committing. Do **not** invent an issue number, and do **not** continue without an issue.

1. Draft from the diff:
   - **Title** — imperative, ≤ 72 chars, no `HITL:`/`AKF:` prefix (the prefix belongs to the commit, not the issue title).
   - **Body** — short problem/intent statement + what this change does + how to test (mirrors the close-comment shape so the closing comment can extend it). Keep under ~15 lines.
2. Ask the user to pick the state label so the commit prefix is determined:
   - `ready-for-human` → commit prefix `HITL:`
   - `ready-for-agent` → commit prefix `AKF:`
3. Show the user the draft (title + body + chosen state) and wait for approval. This is folded into the single combined approval in step 6 of the workflow — don't ask twice.
4. Create with:
   ```bash
   gh issue create \
     --title "<title>" \
     --body "$(cat <<'EOF'
   <body>
   EOF
   )" \
     --label "<state-label>"
   ```
5. Capture the returned issue number from the URL/output and use it as `<num>` for the rest of the workflow. Skip the "read state" call — the label was set at creation.

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
- `Files:` lists meaningful changes, not every touched file.
- `Notes:` is for the next iteration. Skip if truly nothing.
- Body under ~20 lines.

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

Rules for **How to test**:
- Concrete, runnable steps a reviewer can copy. Name the screen, command, endpoint, or button.
- If the change is UI: where to click, what to enter, what to see.
- If the change is API/server: the exact `curl` or request, expected status/payload.
- If the change is internal/refactor with no user-facing surface: how to verify via tests (`pnpm test path/to/file`, etc.) plus what should still work end-to-end.
- 3–6 steps. If you can't write a real test plan from the diff, ask the user before posting — do not invent one.

## Workflow

1. **Read state** — run in parallel:
   - `git status` (no `-uall`)
   - `git diff` (staged + unstaged)
   - `git log -5 --oneline`
   - `git branch --show-current`
   - `git remote get-url origin` (sanity-check the repo)

2. **Resolve or create the issue** — check, in order:
   - Branch name (e.g. `feat/123-...`, `agent/PROJ-456-...`)
   - Recent commits on this branch
   - Conversation context
   If no issue can be located, switch to **Inline issue creation** (see section above): draft title/body from the diff, ask the user for the state label, fold the issue draft into the combined approval, then `gh issue create`. Use the returned number for the rest of the workflow.

3. **Read issue state** — for issues that already existed, run `gh issue view <num> --json state,labels,title,url` and pick `HITL:` or `AKF:` per the table. If neither label is present, ask. For issues just created inline, skip this step — the prefix is already fixed by the label set at creation.

4. **Draft the commit message** from the diff (subject, decisions, files, notes per format above).

5. **Draft the issue-close comment** — summary + how-to-test from the diff. If the test plan isn't obvious, ask the user before continuing.

6. **Show the user the drafts** and wait for approval before any write action. This is one combined confirmation, not three. The drafts shown depend on whether an issue was just created inline:
   - Existing issue: commit message + close comment.
   - Inline-created issue: new-issue title + new-issue body + chosen state label + commit message + close comment. After approval, create the issue first, then commit/push/close in order.

7. **Pre-commit safety**:
   - Refuse to stage secret-pattern files: `.env`, `.env.*` (except `.env.example`), `*.pem`, `*.key`, `id_rsa*`, `credentials*.json`, `*secret*`. Warn and skip.
   - Stage explicitly by path — never `git add -A` / `git add .`.
   - Honor hooks. Never `--no-verify`. If a hook fails, fix the underlying issue and create a NEW commit (do not amend).

8. **Commit** with HEREDOC:
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

9. **Push** the current branch:
   - Tracks a remote → `git push`.
   - No upstream → `git push -u origin <branch>`.
   - **If the current branch is `main` or `master`**: stop and confirm separately before pushing.

10. **Close the issue** — capture the new commit SHA, then:
    ```bash
    SHA=$(git rev-parse --short HEAD)
    gh issue close <num> --comment "$(cat <<EOF
    Closed by ${SHA} on \`<branch>\`.

    **Summary**
    ...

    **How to test**
    1. ...
    2. ...
    3. ...
    EOF
    )"
    ```
    Use an unquoted heredoc (`<<EOF`, not `<<'EOF'`) so `${SHA}` interpolates. Escape any literal backticks/`$` inside the body.

11. **Report** — one line: `<prefix> <SHA> pushed to <branch>; issue #<num> closed`. Done.

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

Close comment:
```
Closed by 9f0e1a2 on `feat/418-idempotency`.

**Summary**
Checkout charges are now idempotent on `x-request-id`; replays return the original result instead of double-charging.

**How to test**
1. `pnpm test server/checkout/handler.test.ts` — all green
2. Hit `POST /checkout` twice with the same `x-request-id` — second call returns the first response, no second Stripe charge
3. Hit twice with different IDs — two distinct charges as before

Notes: Stripe webhook path still unguarded — see follow-up #419.
```

## Checklist

Before marking the iteration done, verify:
- [ ] Issue resolved (or created inline) + state read → correct prefix (`HITL:` or `AKF:`)
- [ ] Commit subject ≤ 72 chars, starts with prefix + space
- [ ] `Issue:` line present in commit body
- [ ] No secret files staged
- [ ] Hooks ran (no `--no-verify`)
- [ ] Push succeeded (or, on `main`/`master`, was confirmed separately)
- [ ] Issue closed with comment containing **Summary** + **How to test**
- [ ] Final report line printed

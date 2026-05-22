---
name: commit-push-close
description: Ship one iteration of work on a GitHub issue — stage and commit with a structured message, push to the current branch, then close the linked GitHub issue with a comment that explains how to test the change. If no GitHub issue can be located, the skill creates one inline before committing for valid small ad hoc work. Routing state lives in issue labels, not commit subject markers. Use when the user says "commit, push, and close", "ship this issue", "I'm done with this issue", or otherwise wants to wrap up issue work in one step.
---

# commit-push-close

Three-step ship for one GitHub-issue iteration (with an inline create-if-missing step for the issue):

1. **Resolve or create** the GitHub issue.
2. **Commit** the diff with a structured message.
3. **Push** to the current branch.
4. **Close** the GitHub issue with a comment explaining how to test it.

## Label validation

Routing state lives in the linked issue's labels. Do not add `HITL:` or `AFK:` to commit subjects, branch names, or GitHub issue titles.

| Issue labels        | Action |
| ------------------- | ------ |
| exactly one category label (`bug` or `enhancement`) and state `ready-for-agent` | proceed |
| exactly one category label (`bug` or `enhancement`) and state `ready-for-human` | proceed, keeping any human-decision notes in the commit body or close comment |
| missing/conflicting labels, `needs-triage`, `needs-info`, or `wontfix` | stop and route through `/triage` unless this is valid ad hoc inline issue creation |
| no linked issue | create one inline only for valid ad hoc work (see **Inline issue creation**) |

Read state with: `gh issue view <num> --json state,labels,title,url`. Match label names exactly.

## Response Footer

End the final response with `Suggested next skills (optional)` containing 1-3 advisory recommendations. Keep it recommendation-only (no gating). Choose next steps from workflow context, for example `/release-notes`, `/handoff`, or `/triage` for follow-up work.

## Inline issue creation

Inline issue creation is only for small ad hoc work that started from a short request with no linked GitHub issue. Planned work should already have gone through Matt Pocock's `/triage`; if a planned issue is missing, not ready, ambiguous, cross-project, or multi-slice, stop and route back to `/triage`, `/feature-prompt`, or `/to-issues` instead of fabricating a ship-time issue.

When step 2 of the workflow can't locate an issue for valid ad hoc work, create one before committing. Do **not** invent an issue number, and do **not** continue without an issue.

1. Draft from the diff:
   - **Title** — imperative, concise, no `HITL:`/`AFK:` marker. This title becomes the commit subject, so make it specific and traceable.
   - **Body** — generate from the original request, final diff, decisions made during the fix, files changed, and validation/how-to-test. Keep under ~20 lines.
2. Choose labels:
   - Category: `bug` for broken behavior; `enhancement` for new feature/improvement. If unclear, ask.
   - State: `ready-for-agent` when the agent completed the work autonomously; `ready-for-human` when human judgment, external access, or manual review was required.
3. Show the user the draft (title + body + chosen labels) and wait for approval. This is folded into the single combined approval in step 6 of the workflow — don't ask twice.
4. Create with:
   ```bash
   gh issue create \
     --title "<title>" \
     --body "$(cat <<'EOF'
   <body>
   EOF
   )" \
     --label "<category-label>" \
     --label "<state-label>"
   ```
5. Capture the returned issue number from the URL/output and use it as `<num>` for the rest of the workflow. Skip the "read state" call — the label was set at creation.

## Naming anchor

Use the GitHub issue title as the naming anchor:

- Existing issue: commit subject should match the issue title as closely as practical.
- PRD slice issue: preserve `Slice NNNN` and the short heading. If the full `Slice NNNN of PRD: <adr-name> - <Short heading>` title is too long for a commit subject, shorten only the PRD name portion; keep the slice number and short heading intact.
- Ad hoc inline issue: the new issue title and commit subject must be the same text unless a hard tool limit prevents it.
- Never add `HITL:` or `AFK:` to any of these names.

## Commit message format

```
<issue title or closest practical match>

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
- Subject mirrors the GitHub issue title as closely as practical, no `HITL:` or `AFK:` marker.
- Always keep the subject and the `Issue:` line. Omit any other section that has nothing to say.
- Never add a `Co-authored-by:` trailer or any other generated co-author attribution.
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
   If no issue can be located, switch to **Inline issue creation** only for valid small ad hoc work (see section above): draft title/body from the original request + diff, choose category/state labels, fold the issue draft into the combined approval, then `gh issue create`. Use the returned number for the rest of the workflow.

3. **Read issue labels** — for issues that already existed, run `gh issue view <num> --json state,labels,title,url`. The issue must have exactly one category label (`bug` or `enhancement`) and a ready state label (`ready-for-agent` or `ready-for-human`). If labels are missing, conflicting, or the state is `needs-triage`, `needs-info`, or `wontfix`, stop and route back to `/triage`. For issues just created inline, skip this step — labels were set at creation.

4. **Draft the commit message** from the issue title and diff (subject, decisions, files, notes per format above). For ad hoc inline issues, the new issue title and commit subject must match.

5. **Draft the issue-close comment** — summary + how-to-test from the diff. If the test plan isn't obvious, ask the user before continuing.

6. **Show the user the drafts** and wait for approval before any write action. This is one combined confirmation, not three. The drafts shown depend on whether an issue was just created inline:
   - Existing issue: commit message + close comment.
   - Inline-created issue: new-issue title + new-issue body + chosen category/state labels + commit message + close comment. After approval, create the issue first, then commit/push/close in order.

7. **Pre-commit safety**:
   - Refuse to stage secret-pattern files: `.env`, `.env.*` (except `.env.example`), `*.pem`, `*.key`, `id_rsa*`, `credentials*.json`, `*secret*`. Warn and skip.
   - Stage explicitly by path — never `git add -A` / `git add .`.
   - Verify the drafted commit message has no `Co-authored-by:` trailer or generated co-author attribution.
   - Honor hooks. Never `--no-verify`. If a hook fails, fix the underlying issue and create a NEW commit (do not amend).

8. **Commit** with HEREDOC:
   ```bash
   git commit -m "$(cat <<'EOF'
   <subject>

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

11. **Report** — one line: `<SHA> pushed to <branch>; issue #<num> closed`. Then append `Suggested next skills (optional)` with 1-3 advisory suggestions.

## Examples

### Minimal

Commit:
```
wire signup form to /api/users

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

### Full

Commit:
```
add idempotency keys to checkout flow

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
- [ ] Issue resolved (or created inline) + labels read/created → one category label + ready state label
- [ ] Commit subject mirrors the GitHub issue title as closely as practical and has no routing marker
- [ ] `Issue:` line present in commit body
- [ ] No `Co-authored-by:` or generated co-author attribution in the commit message
- [ ] No secret files staged
- [ ] Hooks ran (no `--no-verify`)
- [ ] Push succeeded (or, on `main`/`master`, was confirmed separately)
- [ ] Issue closed with comment containing **Summary** + **How to test**
- [ ] Final report line printed
- [ ] Optional `Suggested next skills` footer included (1-3 advisory suggestions, no gating)

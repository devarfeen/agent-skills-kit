---
name: deploy-watch
disable-model-invocation: true
description: "Babysit a merged PR's staging deploy — find the GitHub Actions deploy run for the merge commit, watch it to a conclusion, run an approved agent-browser smoke check against the staging URL, and record pass or fail on the PR. Use when the user says \"watch the staging deploy for PR 87\", \"did my change make it to staging\", or /factory reports a unit in STAGING. Never touches a server, never re-runs or triggers a deploy by hand, and never promotes to production — it ends at ready for the owner. A broken staging deploy routes to /staging-fix; investigating an outage is /incident-triage."
metadata:
  version: "0.1.0"
---

# deploy-watch

deploy-watch proves a merged change reached staging and works there, using only the CI deploy and the staging app's own URL. It stops at "ready for owner": production promotion, feature-flag rollout, and server access belong to someone else.

## Inputs

- **PR** — number or URL; read `gh pr view <pr> --json number,state,baseRefName,mergeCommit,mergedAt,closingIssuesReferences`. Not merged → stop and suggest `/factory`.
- **Staging branch** — default `staging`; the PR's `baseRefName` must match it, confirmed with `git ls-remote --heads origin <branch>`. Mismatch → stop and name both.
- **Deploy workflow** — the workflow file under `.github/workflows/` whose trigger includes a push to the staging branch. Read it; zero or several candidates → stop and ask which.
- **Staging URL** — from the workspace `AGENTS.md`, the deploy workflow's environment URL, or the user. Missing → ask.
- **Smoke checklist** — the spec's integration-contract smoke gate when one exists; otherwise the linked ticket's acceptance criteria turned into 1–5 browser checks. Add one check per `qa-escape` class recorded for the touched area. Show the checklist before running it.
- **Smoke approval** — the user's explicit approval in this session to browse the staging URL. No approval → watch the deploy only and report smoke as not run.

## Rules

- **Servers are never touched.** No SSH, no server commands, no container restarts, no database access, no editing env or config on the host. Evidence comes from Actions run logs and the staging URL through agent-browser.
- **Watch, never deploy.** Do not re-run, cancel, or dispatch a deploy workflow, and do not push to the staging branch. A failed deploy is reported and routed to `/staging-fix`; a revert goes through a revert PR there.
- **Production is out of scope.** Never open a PR to a production branch, never trigger a production workflow, never flip a feature flag. The terminal state is ready for the owner.
- **The run must contain the merge commit.** A deploy run counts when its `headSha` is the PR's merge commit, or a later staging commit that contains it — proven with `git merge-base --is-ancestor <merge-sha> <run-head-sha>` and quoted. Re-run after a `/staging-fix` uses the newest such run.
- **Smoke is read-only.** Navigate and read; never submit forms that create, change, or delete staging data unless the user approves that single step.
- **One approval before any remote write.** Show the result comment and wait. User away → print it and stop.
- Redact before anything leaves the session: replace tokens, keys, cookies, session IDs, passwords, emails, and customer identifiers in quoted evidence with `<redacted>`, keeping only the lines that show the fault.
- A failed or erroring `gh` query is unknown — never an empty result, a pass, or green; report the command and its error.
- **Zero attribution.** No co-author, AI, or tool attribution in the PR comment or any output.
- Emit `Stage / Found / Next / Needs user` at each phase transition — one line per field.

## Workflow

### 1. Declare the expected signals

Before watching anything, write the pass and fail criteria: the run must conclude `success` within the workflow's usual duration (read from its last 5 runs); the deployed build must report the merge SHA; each smoke check names its URL, expected value, and that it must show no new console error and no 4xx/5xx request. A result is judged only against this list, never against an impression.

### 2. Find the deploy run

```bash
gh run list --workflow <deploy-workflow> --branch <staging-branch> --json databaseId,status,conclusion,url,headSha --limit 20
```

No run yet → wait and re-check with a back-off (30s, 60s, then every 2 minutes) up to 15 minutes, then report `no deploy run` and stop.

### 3. Watch it

`gh run watch <run-id> --exit-status`. Stop watching at 2× the usual run time from step 1; still running → `State: unverified (deploy pending)`, no marker. On failure, read `gh run view <run-id> --log-failed`, quote the decisive tail, and skip to step 5 with `result=fail`.

### 4. Smoke the change

With smoke approval, first load one page the diff doesn't reach and record its console and failed-request lines as ambient; an ambient entry, matched by message and URL, is reported, not failed. Then run the checklist through agent-browser against the staging URL: open each page, confirm the expected element, text, or response, and take a screenshot per check. Clear and then read `console`, `errors`, and `network requests --type xhr,fetch --status 400-599` on every check; any new entry fails that check. A failing check is retried once after 60s and fails only if it repeats; record both observations. Record each check as pass or fail with what was observed. Confirm the deployed build when the app exposes one (a version endpoint, a footer SHA, a response header); a stale build means the deploy did not land, so report `result=fail` with that evidence. No build identifier exposed → report `build unconfirmed`; a 200 proves reachability, not which release is live.

### 5. Record

Draft the PR comment:

```
Staging deploy for <merge-sha> — pass | fail
Run: <run URL> (<conclusion>)
Smoke: 4/4 pass on https://staging.example.com — invoices list, credit note total, export CSV, 403 for viewer role

<!-- deploy-watch: merge=<merge-sha> deployed=<run-head-sha> result=pass -->
```

`result=pass` requires a successful run and every smoke check passing; a failed run or failed check gets `result=fail`. Smoke not run → no marker; report the deploy-only result instead. After approval, post with `gh pr comment <pr> --body-file <file>` and read the comments back.

## Output

```
deploy-watch — PR #87 → <staging-branch> @ <merge-sha>
Deploy: success | failure | no run — <run URL>
Smoke: <passed>/<total> | not run (no approval)
State: ready for owner | deploy failed | unverified | unverified (deploy pending)
```

At most 3 bullets for failing checks, each with the observed value. Close with the `Suggested next skills (optional)` footer, 1–3 items: fail → `/staging-fix`; pass → `/release-notes` or `/factory`; unverified → `/factory` after approval.

## Completion criteria

- [ ] The run URL's `headSha` is the merge commit or a quoted ancestry check shows it contains the merge commit
- [ ] Each smoke check names its URL and observed value, and has a screenshot path
- [ ] A `result=pass` marker exists only when the run succeeded and every smoke check passed; a failed run or check posts `result=fail`; either is read back after posting
- [ ] No workflow was dispatched, re-run, or cancelled, and nothing was pushed by this run

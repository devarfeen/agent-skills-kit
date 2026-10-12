---
name: deploy-watch
disable-model-invocation: true
description: "Watch a merged PR's staging deploy run, run an approved smoke check on staging, and record pass or fail on the PR. Never touches a server or triggers a deploy. A broken deploy is /staging-fix."
metadata:
  version: "0.4.0"
---

# deploy-watch

deploy-watch proves a merged change reached staging and works there, using only the CI deploy and the staging app's own URL. It stops at "ready for owner": production promotion, feature-flag rollout, and server access belong to someone else.

## Inputs

- **PR** — number or URL; read `gh pr view <pr> --json number,state,baseRefName,mergeCommit,mergedAt,closingIssuesReferences`. Not merged → stop and suggest `/factory`.
- **Staging branch** — default `staging`, confirmed by `git ls-remote`. Accept a staging-base PR, or an authorized delivery-`local` PR when refreshed staging contains its merge SHA. Quote the ancestry check; other bases or absent ancestry stop. Production branches are forbidden.
- **Deploy workflow** — read its staging push trigger, deployment job, checkout revision and staging destination. A test-only workflow is not a deploy. Zero or ambiguous candidates → stop and name the missing routing evidence.
- **Staging URL** — from workspace instructions, the workflow environment URL, or the user; needed only for smoke. Missing → deploy-only result, smoke not run.
- **Smoke checklist** — the spec's integration-contract smoke gate when one exists; otherwise issue body criteria/checklist, or its newest factory-criteria comment, turned into 1–5 browser checks. Add checks for reproduced escape classes in the area, excluding not-a-regression; show missing criteria as smoke blocked. Show the checklist before running it.
- **Smoke approval** — explicit user approval this session plus user-provided SSH access, as the global staging rule requires; this skill uses neither SSH nor server commands. Missing either → watch GitHub only, smoke not run.
- **Delivered issues** — explicit tracker identifiers supplied by factory, otherwise closing references and newest `factory-delivered` comments naming this PR. Ordinary PR references can be checked against the tracker; ambiguity leaves handoff pending.

## Rules

- **Servers are never touched.** No SSH, no server commands, no container restarts, no database access, no editing env or config on the host. Evidence comes from Actions run logs and the staging URL through agent-browser.
- **Watch, never deploy.** Do not re-run, cancel, or dispatch a deploy workflow, and do not push to the staging branch. A failed deploy is reported and routed to `/staging-fix`; a revert goes through a revert PR there.
- **Production is out of scope.** Never open a PR to a production branch, never trigger a production workflow, never flip a feature flag. The terminal state is ready for the owner.
- **The run must contain the merge commit.** A deploy run counts when its `headSha` is the PR's merge commit, or a later staging commit that contains it — proven with `git merge-base --is-ancestor <merge-sha> <run-head-sha>` and quoted. Re-run after a `/staging-fix` uses the newest such run.
- **Smoke is read-only.** Navigate and read; never submit forms that create, change, or delete staging data unless the user approves that single step.
- **One approval before any remote write.** Show the result comment and wait. User away → print it and stop.
- **Run authorization.** Loaded by `/factory run`, the run's start approves posting the result comment and the manual-QA hand-off in step 6. Smoke approval stays the user's own.
- Redact before anything leaves the session: replace tokens, keys, cookies, session IDs, passwords, emails, and customer identifiers in quoted evidence with `<redacted>`, keeping only the lines that show the fault.
- A failed or erroring `gh` query is unknown — never an empty result, a pass, or green; report the command and its error.
- **Zero attribution.** No co-author, AI, or tool attribution in the PR comment or any output.
- Emit `Stage / Found / Next / Needs user` at each phase transition — one line per field.

## Workflow

### 1. Declare the expected signals

Before watching anything, write the pass and fail criteria: the run must conclude `success` within the workflow's usual duration (read from its last 5 runs); the observed deployed build must identify the selected run's `headSha`, which contains the merge SHA; each smoke check names its URL, expected value, and that it must show no new console error and no 4xx/5xx request. A result is judged only against this list, never against an impression.

### 2. Find the deploy run

```bash
gh run list --workflow <deploy-workflow> --branch <staging-branch> --json databaseId,status,conclusion,url,headSha --limit 20
```

No run yet → wait and re-check with a back-off (30s, 60s, then every 2 minutes) up to 15 minutes, then report `no deploy run` and stop.

### 3. Watch it

`gh run watch <run-id> --exit-status`. Stop watching at 2× the usual run time from step 1; still running → `State: unverified (deploy pending)`, no marker. On failure, read `gh run view <run-id> --log-failed`, quote the decisive tail, and skip to step 5 with `result=fail`.

### 4. Smoke the change

With smoke approval, first load one page the diff doesn't reach and record its console and failed-request lines as ambient; an ambient entry, matched by message and URL, is reported, not failed. Then run the checklist through agent-browser against the staging URL: open each page, confirm the expected element, text, or response, and take a screenshot per check. Clear and then read `console`, `errors`, and `network requests --type xhr,fetch --status 400-599` on every check; any new entry fails that check. A failing check is retried once after 60s and fails only if it repeats; record both observations. Record each check as pass or fail with what was observed. Confirm the build from a version endpoint, footer SHA or response header against the selected run's `headSha`; a stale or different build gets `result=fail`. No identifier → `unverified (build unconfirmed)`, no pass marker: a 200 proves reachability only.

### 5. Record

Draft the PR comment:

```
Staging deploy for <merge-sha> — pass | fail
Run: <run URL> (<conclusion>)
Smoke: 4/4 pass on https://staging.example.com — invoices list, credit note total, export CSV, 403 for viewer role

<!-- deploy-watch: merge=<merge-sha> deployed=<run-head-sha> result=pass -->
```

`result=pass` requires a successful staging deploy, confirmed live run-head identity with quoted merge ancestry, and every smoke check passing; a failed run or failed check gets `result=fail`. Smoke not run or build unconfirmed → no pass marker; report the deploy-only result instead. After approval, post with `gh pr comment <pr> --body-file <file>` and read the comments back.

### 6. Hand to manual QA

Only after a confirmed staging deploy run succeeded and contains this change. Resolve the delivered issues from Inputs and read their latest delivery; factory's explicit identifiers work before its handover comment exists. Skip only an assignment marker for the same delivered PR and merge; older deliveries do not suppress a returned fix. Missing or ambiguous issue identity leaves handoff pending. In step 5's approval, assign each to the workspace's Manual QA person, else its reporter, and post:

```
Staging deployment job succeeded for <deployed-sha> — assigned for manual QA.
Live build / smoke: <confirmed evidence, or unverified/not run with reason>.
Deploy: <run URL> (success) · Smoke: <passed>/<total> | not run

<!-- factory-qa-assigned: pr=<delivered-pr> merge=<delivered-merge-sha> staging=<deployed-sha> -->
```

Leave the issue's status as it is and never close it; the person testing does. Read the assignee and comment back.

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
- [ ] Smoke run: each check names URL, observed value and screenshot. Smoke not run: missing approval/access, URL or checklist is reported; no pass marker
- [ ] Pass requires confirmed live run-head identity, successful staging deploy, merge ancestry and all smoke checks passing. Failure gets `result=fail`; pending/unconfirmed proof gets no pass marker. Approved comments are read back; pending approval prints the draft
- [ ] No workflow was dispatched, re-run, or cancelled, and nothing was pushed by this run

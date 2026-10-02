---
name: ci-loop
disable-model-invocation: true
description: "Drive an open PR's failing CI to green — read the failing job's log, reproduce locally, fix within the PR's scope, push, and watch the next run, repeating up to 3 attempts under one up-front approval. Use when the user says \"fix CI on PR 87\", \"get this PR green\", \"the build is failing on my PR\", or /factory reports a unit in CI. Stops on a flaky or infrastructure failure, a fix outside the ticket's scope, or the attempt cap. Reviewer comments route to /pr-feedback; a bug with no PR or CI run is /diagnosing-bugs; setting up a CI pipeline is not this skill."
metadata:
  version: "0.1.0"
---

# ci-loop

ci-loop turns one PR's red checks green by fixing the code, not the checks. It is the factory's only self-repeating loop, so its bounds — one PR, the ticket's scope, three attempts — are the safety property.

## Inputs

- **PR** — number or URL. Read `gh pr view <pr> --json number,headRefName,headRefOid,baseRefName,state,isCrossRepository,closingIssuesReferences`. Not open, or a fork you can't push to → stop and say so.
- **Ticket scope** — the linked issue's acceptance criteria. No linked issue → the PR body's stated scope; neither → ask.
- **Isolated worktree** — the PR's worktree at `<project-repo>/.worktrees/pr-<n>` on its head branch: reuse it when it exists, else create it through `/using-git-worktrees` when installed, otherwise with `git worktree add`, per the workspace `AGENTS.md` worktree rules. Before the first command there, verify and report the checkout record the workspace `AGENTS.md` requires: path, owning repository and common Git directory, branch or detached state, starting commit, and baseline. Setup failure or a mismatch blocks the run; never fall back to the main checkout. Leave the worktree in place and report its path; cleanup follows the workspace rules. A dirty worktree on another branch → stop and ask; never stash or switch silently.
- **Attempt cap** — default 3 per PR, not per run: `fix(ci):` commits already on the head branch since its last green run count against it. The user may lower it, not remove it.

## Rules

- **One approval covers the loop.** Before the first push, show the plan: PR, failing checks, attempt cap, and the commit-subject pattern `fix(ci): <check> — <cause>`. After the user approves, each attempt may commit and push to this PR's head branch without asking again. Approval never covers another branch, a force-push, or a base-branch change.
- **Fix the code, never the gate.** Never skip, delete, mark `xfail`, loosen assertions, raise timeouts, disable lint rules, or edit workflow files to make a check pass. When the check itself is wrong, stop and report it as a finding.
- **Stay in scope.** A fix belongs to this ticket only when the failure is caused by the PR's diff. Failures that also occur on the base branch, or whose fix needs files unrelated to the ticket, stop the loop with the evidence.
- **Flaky and infrastructure failures stop.** Runner timeouts, network or registry errors, missing secrets, and quota limits are not code faults. Offer one `gh run rerun <run-id> --failed`; if the rerun fails the same way, stop. A flake in a test or code path this PR added or changed is a **Code** failure: fix the race by waiting on the real condition, never by retry or sleep.
- **Circles and stalls stop the loop.** Before each attempt, compare the planned diff with earlier attempts. An attempt that would re-apply a change an earlier attempt reverted, or undo an earlier attempt's fix, stops the loop as `oscillating`. An attempt that leaves the same checks failing with the same error lines stops it as `no progress` — the cap is a ceiling, not a target.
- **Feature branches only.** Never push to the staging branch, the default branch, or any branch a workflow deploys from — read the workflow triggers to know which. A PR whose head is one of those stops before the plan.
- **Push only forward.** New commits on the head branch; no force-push, rebase, or amend of pushed commits.
- **Fresh state each attempt.** Before each attempt, `git fetch` and confirm the remote head is the SHA you last pushed. A commit you didn't make stops the loop as `head moved`; the approval covered the head you saw.
- A failed or erroring `gh` query is unknown — never an empty result, a pass, or green; report the command and its error.
- **Reproduce before fixing.** Run the failing job's command locally first; a fix that was never witnessed failing locally is a guess. When the job can't run locally, say so and name the substitute signal.
- **Zero attribution.** No co-author, AI, or tool attribution in commits or comments; strip tool-injected footers before committing.
- Emit `Stage / Found / Next / Needs user` at each phase transition — one line per field.

## Workflow

### 1. Read the failure

```bash
gh pr checks <pr> --required --json name,state,bucket,link,workflow
gh run list --branch <head-branch> --commit <head-sha> --json databaseId,workflowName,conclusion,url
gh run view <run-id> --log-failed
```

Only `bucket: fail` checks count; a `cancel` bucket is not a pass. A repo without required checks makes `--required` exit 1 with `no required checks reported` — fall back to all checks without `--required` and say so in the report. Record the starting set — each failing check with its decisive error line — as the baseline every attempt is measured against. All `pending` → there is nothing to fix; report the pending checks and stop. Quote the shortest decisive log tail per failing check: the assertion or error line and the step name.

### 2. Classify

Sort each failing check into one class:

- **Code** — the diff broke a test, type check, lint, or build, or a test this PR added or changed is flaky. Continue.
- **Base** — the same check fails on the base branch's latest run (`gh run list --branch <base> --workflow <name> --limit 1`). Stop: not this PR's fault.
- **Flaky or infra** — per Rules. Offer the single rerun.
- **Gate is wrong** — the check contradicts the ticket's acceptance criteria. Stop and report.

### 3. Approve the loop

Present the plan from Rules and wait. User away → print the plan and stop; the loop never starts without approval.

### 4. Attempt

For each attempt, up to the cap:

1. Reproduce locally with the job's own command and see it fail. Passes locally → don't fix yet: diff CI against local (runtime and tool versions from the job log, env vars, service containers, test order or seed, timezone) and reproduce under CI conditions. Still green → stop as `no repro` with the differences listed.
2. Make the smallest in-scope fix. Run the failing command, then the repo's fast check suite.
3. Stage the fix paths by name, inspect `git diff --cached`, commit with `fix(ci): <check> — <cause>`, and push.
4. Watch the new run: `gh pr checks <pr> --required --watch --fail-fast`. Stop watching at 2× the workflow's recent run time (`gh run list --workflow <name> --limit 5`) and report `pending`.
5. All required checks `pass` on the new head → done. Any failure → next attempt: re-read and re-classify it (Workflow steps 1–2) before fixing; a stop class ends the loop.

### 5. Stop

The loop ends on green, the attempt cap, or any stop condition in Rules. At the cap, leave the branch as pushed and report what each attempt tried; never squash or revert attempts.

## Output

```
ci-loop — PR #87 (<head-branch>)
Result: green | stopped (<reason>) | oscillating | no progress | head moved | no repro | pending | capped (3/3)
Baseline: unit-tests (null user in InvoiceTotal), lint (unused import)
Attempts:
- 1 a1b2c3d — unit-tests: null user in InvoiceTotal — fixed guard → still failing (lint)
- 2 4e5f6a7 — lint: unused import — removed → green
Evidence: <run URL> — "<pass/fail line and counts>"
```

One line per attempt. On a stop, replace `Attempts` with the classification and its quoted log line. Close with the `Suggested next skills (optional)` footer, 1–3 items: green → `/risk-review <pr>` or `/factory`; stopped on reviewer-facing issues → `/pr-feedback`.

## Completion criteria

- [ ] `gh pr checks <pr> --required` (or all checks, when the repo has no required checks) shows every check `pass` on the pushed head SHA, or the report names the stop reason with a quoted log line
- [ ] The checkout record was reported before the first command, and every commit was made in that worktree
- [ ] Attempt count ≤ the cap, and each attempt's commit SHA appears on the head branch
- [ ] `git diff <first-head>..HEAD --name-only` shows no workflow files, skip markers, or deleted tests
- [ ] No co-author or AI/tool attribution in any commit message from the loop

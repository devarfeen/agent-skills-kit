---
name: agentic-qa
disable-model-invocation: true
description: "Agent-run functional QA before a human sees the work — for a PR or branch whose code can reach a screen, drives every acceptance criterion through the running app across states, viewports, and roles, fails on console errors and failed requests, checks neighbouring flows, and records VERIFIED, PARTIAL, or BLOCKED with evidence on the PR. Use when the user says \"QA this PR\", \"test it like QA would\", \"run agentic QA on #87\", or /factory reports a unit in QA. The tester never edits code — findings route to /tdd-loop. Pixel conformance against a design is /pixel-audit; cosmetic nits are /polish-batch; a bug human QA already found is /qa-escape."
metadata:
  version: "0.2.0"
---

# agentic-qa

agentic-qa finds what a human QA pass would find, before any human runs one. It drives the change through the running app and judges it by what the app shows, logs, and requests — never by what the code or the builder claims. It is the tester, not the fixer: it writes evidence, never code.

## Inputs

- **Change** — a PR number or branch. Read the diff, the head SHA, and the linked issue.
- **Acceptance criteria** — from the issue, plus the `AC map` line of the `/tdd-loop` summary when one exists. Rows the builder marked `agentic-qa (<surface>)` are owed here. No criteria anywhere → stop; the work is not ready for QA.
- **Isolated worktree** — the app runs from `<project-repo>/.worktrees/pr-<n>` at the head SHA (detached is fine; the tester commits nothing): reuse the PR's worktree when it exists, else create it through `/using-git-worktrees` when installed, otherwise with `git worktree add --detach`, per the workspace `AGENTS.md` worktree rules. Before the first command there, verify and report the checkout record the workspace `AGENTS.md` requires: path, owning repository and common Git directory, branch or detached state, starting commit, and baseline. Setup failure or a mismatch blocks the run; never fall back to the main checkout. Leave the worktree in place and report its path; cleanup follows the workspace rules. The base-commit baseline runs from its own worktree, `.worktrees/pr-<n>-base`.
- **Running app** — a local URL served from that worktree at the head SHA. Staging only with this session's explicit approval, and read-only there. Neither → `BLOCKED`.
- **Roles** — each role that can see the touched surfaces, with test logins referenced by env var name only, never values. A role with no login → its cells are gaps, not skips.
- **Escape classes** — open and closed issues labelled `qa-escape` whose area matches the touched surfaces (`gh issue list --label qa-escape --state all --search "<area>"`, or the tracker's label filter). Each class, and each line for the area under the workspace `AGENTS.md` section `## QA escape guards`, becomes grid rows; skip markers with `reproduced=no`. A guard line whose surface no longer exists → report it under Needs user; never skip it silently.

## Rules

- **The tester never edits code.** No source, test, fixture, or config edits, even for a one-character fix. Every failure becomes a finding with reproduction steps, routed to `/tdd-loop`. A tester that fixes stops being an independent check.
- **Reach is decided by the code, not the label.** The change needs this skill when any changed file is reachable from a route, page, component, template, translation, or style, or is an API whose response a screen renders. Trace it per [`references/qa-grid.md`](references/qa-grid.md) and quote the path. No reach → record `no-ui-reach` with that trace and stop.
- **A blank cell is not done.** Every grid cell is `pass`, `fail`, or `not reachable — <reason>`. A reason names why the state cannot occur, not why it was inconvenient.
- **Browser errors fail the cell.** Capture console, page errors, and XHR/fetch responses for every flow. A new `error`-level message, unhandled rejection, or 4xx/5xx response fails the cell, unless the cell expects it (a 403 for a forbidden role) or the same signal appears on the base commit run.
- **Success is a visible change.** Capture the relevant state before acting and assert the expected change after. A success message with no changed state is a fail. For a write, the change also survives a reload.
- **Prove presence before a negative.** Before asserting a control is rejected or hidden for a role, show it exists for a role that should see it. Otherwise "missing" passes as "denied".
- **Production is never touched.** On staging: read-only flows only, unless the user approves that single mutating step; restore anything changed.
- **Status is earned.** `VERIFIED` only when every cell passed and no gap remains. Any failed cell or gap → `PARTIAL`. App not runnable, no criteria, or no login for a required role → `BLOCKED`. Never the word "fixed".
- **Three re-checks per finding.** A finding that still fails on its third re-check against a new head is escalated to the engineer by name in the report; it is not re-queued again.
- **One approval before any remote write.** Show the PR comment and wait. User away → print it and stop.
- **Run authorization.** Loaded by `/factory run`, the run's start approves posting the comment. Staging, and any mutating step there, keeps its own approval.
- **Zero attribution.** No co-author, AI, or tool attribution in the comment, evidence files, or any output.
- Resolve `<artifacts-root>`: the `*.code-workspace` directory if one exists, else the per-context root (`GLOSSARY-MAP.md` at repo root; legacy `CONTEXT-MAP.md`), else the repo root.
- Name the full PROJECT-CODE from the Project Matrix everywhere; never mix one project's conventions, tokens, or components into another.
- Emit `Stage / Found / Next / Needs user` at each phase transition — one line per field.

## Workflow

### 1. Decide reach

Trace each changed file to a screen per the reference. Quote one path per reachable surface (`app/Billing/Invoice.php → InvoiceResource → /invoices/{id}`). No reach → step 6 with `no-ui-reach`.

### 2. Build the grid

Rows: each acceptance criterion and each path it owes, each escape class for the area, and one row per neighbouring flow — other screens that call the changed code, sibling entry points, create vs edit. Columns: the states each row can reach (default, loading, empty, error, success, disabled, permission denied, offline, long content, keyboard-only), at 375 and 1280 widths, for each role. Write the grid to `<artifacts-root>/specs/qa/<pr>-<short-sha>/grid.md` before driving anything; template in the reference.

### 3. Baseline

Where a second checkout of the base commit can run, drive the same routes there once and keep its console, error, and failed-request output. Screenshot each route once on the base run as its `before` image; the head run's screenshot is its `after`. No base run → every captured error counts and the report says so, with `before: not captured`.

### 4. Drive each cell

Follow the workspace browser rule: one named session, one batched flow per cell, short explicit timeouts. Per flow: clear console, errors, and requests; capture the before state; act; assert the after state; read console, errors, and `network requests --type xhr,fetch --status 400-599`; take one screenshot. Force states with the recipes in the reference (aborted or stubbed responses for error and empty, `set offline on`, long fixtures). Never submit real data on staging without approval.

### 5. Judge and write findings

Mark each cell. Before marking a cell `fail`, replay its exact batch once from the same starting state: fails both times → `fail`; fails once → `fail (intermittent 1 of 2)`, still a finding that says so. For each fail, record: cell, exact reproduction (the batch you ran), expected, actual, and the evidence paths. Re-checks of earlier findings carry their count (`re-check 2/3`), read from the previous report for this PR.

### 6. Record

Write `report.md` beside the grid, then draft the PR comment: status, counts, findings, and the marker line exactly:

```
<!-- agentic-qa: sha=<head-sha> result=<verified|partial|blocked|no-ui-reach> findings=<n> recheck=<highest re-check count among open findings, 0 if none> -->
```

After approval, post it with `gh pr comment <pr> --body-file <file>` and read it back. No PR yet → the marker stays at the end of `report.md`, and the run is posted once a PR for the same head SHA exists; a later commit needs a new run.

## Output

```
agentic-qa — PR #87 @ <short-sha>: PARTIAL
Grid: 46 cells — 41 pass · 3 fail · 2 not reachable · 0 blank
Browser: 1 console error (TypeError in InvoiceTotal.vue:42), 0 failed requests vs base
Evidence: <artifacts-root>/specs/qa/87-a1b2c3d/report.md
```

Then at most 3 bullets naming the highest-impact findings. Close with the `Suggested next skills (optional)` footer, 1–3 items: findings → `/tdd-loop` with the first finding; verified → `/risk-review <pr>` or `/factory`.

## Completion criteria

- [ ] `grid.md` exists and has no blank cell; every `not reachable` names its reason
- [ ] Every fail has a reproduction batch, expected, actual, and an evidence path that exists
- [ ] The checkout record was reported before the app started, and `git status` in that worktree shows no change to source, test, or config files from this run
- [ ] The marker for the current head SHA is on the PR, read back after posting, or the drafted comment is printed when approval is pending

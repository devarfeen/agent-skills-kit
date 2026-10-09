---
name: qa-escape
disable-model-invocation: true
description: "Intake for a bug that human QA found after an agent called the work done — reproduce it as an evidence brief, classify the escape, trace why the agent's checks missed it to a check that can be fixed, record it as a labelled comment on the issue, and name the failing regression test /tdd-loop must write first. When the same escape class reaches three issues, proposes a durable guard and applies it only on approval. Use when the user says \"QA found a bug in #87\", \"QA bounced this ticket\", \"this was marked fixed but QA says it's broken\", or /factory reports a unit in QA_RETURNED. Never edits code. A bug with no prior agent claim is /diagnosing-bugs; a staging-only fault is /staging-fix."
metadata:
  version: "0.3.0"
---

# qa-escape

An escape is a bug a human found after an agent's checks said the work was done. qa-escape turns each one into three things: a reproduction, a regression test to write first, and a recorded escape class that every future ticket in that area is checked against. The goal is that a class escapes at most once before the checks change.

## Inputs

- **QA report** — steps, expected, actual, environment, screenshots or logs. Missing expected or actual → ask for that one field.
- **The issue and its PR** — the ticket QA tested and the PR that shipped it. Read the PR's `agentic-qa` and `risk-review` marker comments and the `/tdd-loop` summary if present: they are the agent's claim.
- **Isolated worktree** — reproduce in `<project-repo>/.worktrees/qa-escape-<issue>` detached at the revision QA tested: create it through `/using-git-worktrees` when installed, otherwise with `git worktree add --detach`, per the workspace `AGENTS.md` worktree rules. Before the first command there, verify and report the checkout record the workspace `AGENTS.md` requires: path, owning repository and common Git directory, branch or detached state, starting commit, and baseline. Setup failure or a mismatch blocks the run; never fall back to the main checkout. Leave the worktree in place and report its path; cleanup follows the workspace rules.
- **Environment** — where QA saw it: local, staging, or production. Production evidence is used as pasted; the agent never reaches production.

## Rules

- **Never edits code.** No source or test edits. The output is a brief, a test specification, and an issue comment; `/tdd-loop` writes the test and the fix.
- **Reproduce before anything else.** Expected and actual describe observations only — never the suspected cause. A report that cannot be reproduced locally or on approved staging is recorded with `reproduced=no`, `class=none` (or `not-deployed` per step 1), and what was tried; it is never counted toward promotion.
- **Every escape names the check that missed it.** The why-chain must answer "why did the agent's checks pass?" from the actual evidence — the grid cell that was marked `pass` or `not reachable`, the missing matrix row, the absent run. It ends at a check that can change. "Be more careful" or "the agent missed it" is not an end.
- **Classes come from the fixed list** in [`references/escape-classes.md`](references/escape-classes.md). A new class needs a slug and one-line definition added to the comment and proposed for the list.
- **Promotion waits for three and for approval.** When this escape makes three issues with the same class and area, propose one durable guard. Apply nothing until the user approves that guard; declined → record the decline in the comment.
- **One approval before any remote write.** Show the issue comment and the label change together and wait. User away → print both and stop.
- **Run authorization.** Loaded by `/factory run`, the run's start approves posting the comment and adding the `qa-escape` label. Creating a missing label, applying a guard, and any staging access keep their own approval.
- Redact before anything leaves the session: replace tokens, keys, cookies, session IDs, passwords, emails, and customer identifiers in quoted evidence with `<redacted>`, keeping only the lines that show the fault.
- **Zero attribution.** No co-author, AI, or tool attribution in the comment or any output.
- Name the full PROJECT-CODE from the Project Matrix everywhere; never mix one project's conventions, tokens, or components into another.
- Emit `Stage / Found / Next / Needs user` at each phase transition — one line per field.

## Workflow

### 1. Write the reproduction brief

First check the fix was there to test: `git merge-base --is-ancestor <pr-merge-sha> <tested-sha>`. It was not → class `not-deployed`; skip to step 6 and record `reproduced=no` with both SHAs, since nothing was tested. Otherwise state expected and actual as observations. Reproduce on the same revision QA tested. Shrink the case: remove one condition at a time, restore the last one whose removal makes the bug disappear, and record it as required. Run the final case twice; record `reproduced: yes | intermittent (n of m) | no`. On `no`, skip to step 6 and record what was tried. Then run the minimal case once on the PR's base commit, from `.worktrees/qa-escape-<issue>-base`. Reproduces there → class `not-a-regression`.

### 2. Read the agent's claim

From the PR: the agentic-qa status and grid, the risk-review tier, the tdd-loop `AC map`. Name what was claimed for this behavior — a cell marked pass, a cell marked not reachable, a row that never existed, or no agentic-qa run at all.

### 3. Classify and trace

Pick the class. Then the why-chain, at most five steps, ending at a fixable check. Example: *empty list shows a crash* → *grid had no empty-state row for the list* → *the acceptance criteria named only the populated list* → *agentic-qa builds rows only from criteria and escape classes* → **check to change: the empty state becomes a default row for every list surface in this area.**

### 4. Specify the regression test

Name the lowest layer that can show the bug: a unit test for logic; a handler test asserting status, body, and side effect for an API; a write-then-reload test for persistence; a browser test in the project's end-to-end runner when only the rendered app shows it. Give the test's name, setup, action, and the assertion that fails today. State its proof: fails at `<tested-sha>`, passes at base (or `n/a — not-a-regression`), passes after the fix. Prefer a new row in an existing test or table over a new file; name it. This is the first Red for `/tdd-loop`. No end-to-end runner for a render-only bug → say so; the marker from step 6 is the regression check, because `/agentic-qa` turns every escape marker for the area into grid rows on each later change.

### 5. Count the class

`gh issue list --label qa-escape --state all --json number,title,body,comments` (or the tracker's label filter), then count distinct issues with a marker of the same `class` and `area`, excluding `reproduced=no` and `not-a-regression`. Three or more issues including this one → draft one guard from the reference's ladder, highest rung first: a type, constraint, or lint rule that makes the mistake unwritable; a check in CI or `validate`-style tooling; a standing grid row for the area; a rule line in the workspace `AGENTS.md` section `## QA escape guards`.

### 6. Record

Draft the issue comment from the reference template, ending with the marker line exactly:

```
<!-- qa-escape: class=<slug|none> area=<PROJECT-CODE>:<surface> pr=<pr-number> tested=<tested-sha> reproduced=<yes|intermittent|no> -->
```

Add the `qa-escape` label in the same approval. It is a marker label beside the issue's category and state labels, never a replacement for them; create it only if the tracker lacks it, in that approval. After approval, post, label, and read both back. An approved guard is applied in its own step: an `AGENTS.md` rule line is added under `## QA escape guards`; a type, lint, or CI guard becomes a ticket via the suggested `/to-tickets`.

## Output

```
qa-escape — #418 (BILLING-WEB): reproduced yes · class missed-empty-state · 2 of 3 in BILLING-WEB:/invoices
Missed by: agentic-qa grid on a1b2c3d had no empty row for the invoice list
Regression test: InvoiceList "renders empty message when no invoices" (browser flow)
```

At most 3 bullets beyond this. Close with the `Suggested next skills (optional)` footer, 1–3 items: `/tdd-loop` with the regression test; `/to-tickets` when an approved guard needs code; `/factory` to re-place the unit.

## Completion criteria

- [ ] The brief states expected, actual, the minimal conditions, and the reproduced result with run count
- [ ] The why-chain ends at a named check, quoting the claim it overturns (cell, row, or missing run)
- [ ] The issue comment with its marker and the `qa-escape` label are on the issue, read back after writing — or both drafts are printed when approval is pending
- [ ] The printed class count lists the issue numbers it counted
- [ ] The checkout record was reported before reproducing, and `git status` in that worktree shows no code or test change from this run

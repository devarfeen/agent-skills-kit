# Workflow records

Zero attribution: never add or leave co-author, AI, tool, or generator attribution in any output, except the **Reviewer provenance** line below when the workspace allows it.

Use when reading or publishing issue workflow records. Linear comments contain clean Markdown headings, evidence, and readable fields. Emit no HTML control markers in Linear comments. Keep GitHub marker formats and internal evidence contracts where their consumers require them; read legacy Linear markers for existing history.

## Linear fields

| Heading | Required fields | Equivalent legacy record |
| --- | --- | --- |
| `## Acceptance criteria` | Numbered criteria, preserving the issue's stated outcomes | `factory-criteria` |
| `## QA` | `Commit`, `Result`, `Findings`, `Rechecks`, `Checks` | `agentic-qa` |
| `## QA carried forward` | `Commit`, `From QA commit`, `Prior QA record`, `Why no new QA`, `Changed files`, `Proof`, `Not re-tested`, `Still required` | `qa-carried-forward` (GitHub marker) |
| `## Code review` | `Commit`, `Round`, `Findings`; `Reviewer` only under **Reviewer provenance** | `code-review` |
| `## Code review reply` | `Round`, `Fixed`, `Declined`; `Builder` only under **Reviewer provenance** | `code-review-reply` |
| `## Code review fix check` | `Commit`, `Round`, `Reviewed commit`, `Findings fixed`, `Changed lines`, `Proof`, `Not reviewed again`, `Findings`; `Checked by` only under **Reviewer provenance** | `code-review-fix-check` |
| `## Delivered` | `PR`, `Merge commit`, `Base`, `Checks` | `factory-delivered` |
| `## QA escape` | `Class`, `Area`, `PR`, `Tested commit`, `Reproduced` | `qa-escape` |
| `## Manual QA assignment` | `PR` (URL list), `Merge commit`, `Staging commit`, `Repository`, `Delivery key`, `Reporter`, `Result` | `factory-qa-assigned` (history only when provenance/key absent) |

Write fields as ordinary Markdown, for example `**Commit:** <full SHA>`. Include explanations, findings, criteria and evidence links, not just the fields. Commit fields use full SHAs; count fields are nonnegative integers. QA results are `verified`, `partial`, `blocked`, or `no-ui-reach`; normalize capitalization and Markdown styling only, never infer a result from prose. Escape reproduction is `yes`, `intermittent`, or `no`. Preserve the existing class/area and revision matching rules.

Read fields inside their matching heading's section. A standalone acceptance-criteria comment starts with that heading; a nested criteria section in a delivery or QA report is not a replacement intake criteria source. Body criteria/checklists take precedence. Otherwise use the newest valid standalone criteria comment, including legacy records, and retain its exact source and text.

Normalize readable and legacy fields to the same state evidence. Order applicable records by original comment creation time, retain their URL/ID, and bind revision-dependent gates to the exact requested revision. Formatting edits do not create a new QA run or reorder its result. A newer blocked/partial result must not be bypassed with an older pass. Missing, malformed, conflicting, or unreadable required fields leave the gate unverified. Delivery deduplication compares delivered PR and merge revisions. Manual-QA deduplication uses the durable issue/repository/source-delivery key below, not a heading or later staging/deploy SHA alone.

## Checks block

`## QA` and `## Delivered` carry a `Checks:` block for every check run that gated the unit since the previous such record (`## Delivered`: the final ship gate). One line per check, from the inspected producer output:

```md
Checks:
- composer test — 2986 passed, 0 failed — 3m 24s — 4f5e6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f
- npm run lint — exit 0 — 12s — 4f5e6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f
```

Each line is `<command> — <passed/failed counts or exit status> — <duration> — <full tested SHA>`. A resumed aggregate lists the failed attempt and the resumed stages as separate lines; a reused result names the SHA it ran on. Use real values only; an unknown count or duration says `unknown`. The block reports checks; it never replaces **Check records** proof.

## Carrying QA forward

Allowed only when the **No-behavior proof** below holds for the diff from the last QA-tested commit to the new head. Test files outside any rendered path may also change, because they cannot reach a screen; the changed tests must then run and pass on the new head, and the record lists them under Changed files as `test-only` with that run in Proof. The prior QA result must be `verified` or `no-ui-reach` with findings 0. Anything else, or any doubt about reach, runs full QA. Post on the issue, and on GitHub also on the PR:

```md
## QA carried forward

Commit: <full new head SHA>
From QA commit: <full SHA that QA tested>
Prior QA record: <link to the ## QA comment>
Why no new QA: the change cannot reach a screen — <one plain sentence, e.g. "only a code comment was added">
Changed files: <path> — <comment-only | test-only | docs-only>
Proof: <command and its result, e.g. "php -w diff of config/navigation.php: identical code">
Not re-tested: screenshots and browser checks were not repeated; the prior QA result and images stand for this commit.
Still required: CI and code review on this commit.
```

On GitHub append `<!-- qa-carried-forward: sha=<new-head> from=<qa-sha> -->`. Read it back. A complete record for head is accepted exactly like a `verified` QA result for head; a missing field, an unquoted proof or a non-matching `From QA commit` leaves the QA gate open.

## No-behavior proof

Used by **Carrying QA forward**, **Fix-only close** in `review-and-delivery.md`, and the comment-only check cadence in `run.md`. It holds only when every changed file passes one of these, each quoted with its command output:

- A doc file outside any rendered, routed or built path.
- PHP code: identical `php -w` output before and after, and no changed line holds an annotation or attribute (`@` inside a docblock, or `#[`).
- Other code: every changed line, trimmed, is blank or a comment line in that language, and no changed line holds a tool directive (`@ts-`, `eslint-`, `prettier-`, `istanbul`, `c8`, `noqa`, `pragma`, `go:`, `webpack`, `@vite`, `type:`).

A changed test file is behavior for checks and review, so it fails this proof. A file that fails a test, or any doubt, fails the proof: run the full step instead.

## Code review fix check

Written by the parent for **Fix-only close** in `review-and-delivery.md`. It closes the review loop for head; it does not replace review of new behavior.

```md
## Code review fix check

Commit: <full new head SHA>
Round: <round whose findings it closes>
Reviewed commit: <full SHA the reviewer reviewed>
Findings fixed: <n> of <n> — <finding numbers>
Changed lines: <path:line-range> — cited by finding <n>
Proof: <command and its result, e.g. "php -w diff of config/navigation.php: identical code">
Not reviewed again: no new independent review ran; the round <n> review stands for this commit.
Findings: 0
```

On GitHub append `<!-- code-review-fix-check: sha=<new-head> round=<n> findings=0 -->`. Read it back. A missing field, an unquoted proof or a `Reviewed commit` that does not match the last review leaves the review gate open.

## Reviewer provenance

Default: zero attribution. Only when the workspace instructions explicitly allow reviewer provenance, `## Code review` gains one line `Reviewer: <provider>/<model> via <harness>`, `## Code review reply` gains `Builder: <provider>/<model> via <harness>`, and `## Code review fix check` gains `Checked by: <provider>/<model> via <harness>`, from the live launch record. This exception covers those three code-review comment kinds on GitHub and Linear only, never commits, PRs, code, docs or any other comment.

## Staging-event assignment

The caller's shared GitHub Action assigns and comments when a delivery merges into or reaches its confirmed staging branch, not when deployment succeeds. Factory, local-to-staging and deploy-watch inspect configuration and existing records only; missing automation or record means handoff unconfigured/pending, never an implicit tracker-write fallback. Local engineering records explicitly say `not staged`; before staging emit no manual-QA assignment, QA-user mention or bespoke handoff notification.

Discover the event adapter, reference parser, durable store and record locator from caller repository/workspace instructions and staging workflows. Canonical `Issue: <identifier>` trailers and non-closing `Ref <identifier>` PR body lines expose every delivered issue before merge. Preserve the full promoted range and original delivery identities rather than relying only on a later delivery comment, PR title, current assignee or PR author.

A delivery key binds the resolved issue ID, repository and sorted source commits attributable to that issue; retain original PR URLs. Incidental promotion merge SHA, event/run ID and later staging SHA are not new deliveries when original identities are known. The adapter serializes concurrent attempts, persists per-issue assignment/comment completion and resumes partial failures. An unchanged retry or unrelated staging push cannot undo a human QA return; a returned fix with new source commits gets a new key. For cross-repository delivery the task owner publishes a standalone `## Delivery scope` comment before promotion, once actual source commits are known: `Delivery cycle: <opaque stable ID>` and repeated `Expected delivery: <owner/repo>@<full source SHA>` lines. Use the newest standalone scope comment, with explicitly declared description scope only as a fallback when none exists. Require per-repository staged receipts proving every pin in the same cycle. A returned fix/changed scope uses a new cycle; explicitly carry unchanged dependency pins forward with existing staged-receipt evidence. No scope defaults to the single owning repository; declared multiple repositories with missing pins stay pending. Missing identity or owner inclusion blocks that ticket only, while independent tickets continue. Never edit the issue body to add scope.

Reporter means the native human reporter/requester (`asksRequester` when exposed), otherwise human issue creator, or an explicit created-on-behalf reporter mapping with a durable source pointer for bot/integration-created issues. Missing, ambiguous or conflicting provenance blocks the affected handoff. Never substitute the current developer, assignee, PR author or a fixed Manual QA person.

The readable assignment record lists PR (URL list), full delivered Merge commit(s), full Staging commit(s), Repository, Delivery key, Reporter with source pointer and Result. Accept PR(s)/Result/State aliases when configured; Complete maps to assigned and Pending to pending. Retain configured Reporter user ID, Assignment actor ID and Initial assignee ID audit fields. Match these against the current owner set and retain comment/automation locators. Legacy records remain history; incomplete provenance/key is no proof of event completion. The event read-back verifies assignee and comment; inspection after human QA uses durable completion history without restoring the assignee. Handoff changes no criteria, workflow labels or status and never closes issues. The reporter later comments QA findings and assigns back to the developer.

`Result: Complete` proves staging inclusion and assignment only; explicitly state deployment/smoke unverified in that record. Deploy run, live build identity, smoke and acceptance retain separate gates. Reading GitHub/tracker records grants no staging browser/API or server access.

## Check records

For executed checks, use **Check evidence and reuse** in the shared ship policy loaded by `commit-push-pr`. Save the complete proof/log path in the round log; workers return a bounded result and locator, not raw logs. The parent inspects the producer output and verifies content, checkout, runtime/data/dependency/assets identities before reuse. An execution claim, marker without the required proof, or log-reader exit status is insufficient. This record proves checks only; current-head QA/review/risk and remote CI retain their separate contracts.

## Existing PR records

On GitHub PRs retain the existing comments: `agentic-qa` with `sha`, `result`, `findings`, `recheck`; `risk-review` with `tier`, `sha`, `blocking`; `deploy-watch` with `merge`, `deployed`, `result`; and `qa-carried-forward` with `sha`, `from`. Read their existing HTML marker format, using newest evidence for the required revision. Linear issue QA records supplement rather than replace mandatory PR evidence.

## Publication and read-back

The factory formats its Linear criteria, QA, QA carried forward, review/reply and delivery comments with the fields above before posting. Pass the format to workers; a worker's marker-bearing draft is formatted before publication while preserving its findings and revision. Read the saved comment back and check all required fields and evidence links. A clean-looking comment without complete gate evidence is not a pass.

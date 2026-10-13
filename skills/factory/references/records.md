# Workflow records

Zero attribution: never add or leave co-author, AI, tool, or generator attribution in any output.

Use when reading or publishing issue workflow records. Linear comments contain clean Markdown headings, evidence, and readable fields. Emit no HTML control markers in Linear comments. Keep GitHub marker formats and internal evidence contracts where their consumers require them; read legacy Linear markers for existing history.

## Linear fields

| Heading | Required fields | Equivalent legacy record |
| --- | --- | --- |
| `## Acceptance criteria` | Numbered criteria, preserving the issue's stated outcomes | `factory-criteria` |
| `## QA` | `Commit`, `Result`, `Findings`, `Rechecks` | `agentic-qa` |
| `## Code review` | `Commit`, `Round`, `Findings` | `code-review` |
| `## Code review reply` | `Round`, `Fixed`, `Declined` | `code-review-reply` |
| `## Delivered` | `PR`, `Merge commit`, `Base` | `factory-delivered` |
| `## QA escape` | `Class`, `Area`, `PR`, `Tested commit`, `Reproduced` | `qa-escape` |
| `## Manual QA assignment` | `PR`, `Merge commit`, `Staging commit` | `factory-qa-assigned` |

Write fields as ordinary Markdown, for example `**Commit:** <full SHA>`. Include explanations, findings, criteria and evidence links, not just the fields. Commit fields use full SHAs; count fields are nonnegative integers. QA results are `verified`, `partial`, `blocked`, or `no-ui-reach`; normalize capitalization and Markdown styling only, never infer a result from prose. Escape reproduction is `yes`, `intermittent`, or `no`. Preserve the existing class/area and revision matching rules.

Read fields inside their matching heading's section. A standalone acceptance-criteria comment starts with that heading; a nested criteria section in a delivery or QA report is not a replacement intake criteria source. Body criteria/checklists take precedence. Otherwise use the newest valid standalone criteria comment, including legacy records, and retain its exact source and text.

Normalize readable and legacy fields to the same state evidence. Order applicable records by original comment creation time, retain their URL/ID, and bind revision-dependent gates to the exact requested revision. Formatting edits do not create a new QA run or reorder its result. A newer blocked/partial result must not be bypassed with an older pass. Missing, malformed, conflicting, or unreadable required fields leave the gate unverified. Delivery and manual-QA assignment deduplication still compare PR and merge/staging revisions, not headings alone.

## Existing PR records

On GitHub PRs retain the existing comments: `agentic-qa` with `sha`, `result`, `findings`, `recheck`; `risk-review` with `tier`, `sha`, `blocking`; and `deploy-watch` with `merge`, `deployed`, `result`. Read their existing HTML marker format, using newest evidence for the required revision. Linear issue QA records supplement rather than replace mandatory PR evidence.

## Publication and read-back

The factory formats its Linear criteria, QA, review/reply and delivery comments with the fields above before posting. Pass the format to workers; a worker's marker-bearing draft is formatted before publication while preserving its findings and revision. Read the saved comment back and check all required fields and evidence links. A clean-looking comment without complete gate evidence is not a pass.

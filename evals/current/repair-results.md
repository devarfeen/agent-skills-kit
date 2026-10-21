# Approved repair evaluations

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Date: 2026-10-21. Two independent fresh sessions read the fifteen synthetic
[fixtures](repair-fixtures.json) and their listed instruction files without
expected outcomes or each other's responses. Raw reports:
[repetition 1](repair-response-1.md), [repetition 2](repair-response-2.md).
Actual model identities were not exposed. The coordinating reviewer compared
those decisions with the approved changes.

| Case | Observable criterion | Final repetitions satisfying it |
| :--- | :--- | :--- |
| C11 | Workspace-bound T3 registration does not require every product repository to be registered. | 2/2 |
| C12 | Accept assigned research evidence; keep code work incomplete without actual test output. | 2/2 focused rechecks |
| C13 | Shared-checkout worker returns verified uncommitted work; authorized integration merge retains its exception. | 2/2 |
| C14 | Required QA precedes human preview; suggest user-only QA without invoking it. | 2/2 focused rechecks |
| C15 | Reopened changed row prevents a shipping suggestion; untouched rows do not independently block it. | 2/2 |
| C16 | Already-fixed reply requires both the commit and the fix to remain present on refreshed head. | 2/2 |
| C17 | Direct-close uses delivered commit and baseline, with no invented PR; missing baseline stays unresolved. | 2/2 |
| C18 | Fixture owner prepares missing data; tester does not seed it. | 2/2 |
| C19 | Approved duplicate comment receives read-back and batch accounting without creating an issue. | 2/2 |
| C20 | Forbidden default/deployment head does not enter ci-loop; red promotion does not merge. | 2/2 |
| C21 | Shipping stops for separately authorized implementation repair, restarts state checks, and never bypasses hooks or amends. | 2/2 |
| C22 | Explicit delivery-local closure policy overrides generic closing-reference text. | 2/2 |
| C23 | Offer only feasible recovery actions without padding unavailable alternatives. | 2/2 |
| C24 | Record settled reuse choice as evidence; do not invent an open question. | 2/2 |
| C25 | Stop after the advisory footer; an optional prototype suggestion grants no implementation authority. | 2/2 |

## Corrections and fresh checks

The first reports reached the intended C12 and C14 decisions but exposed
residual instruction conflicts. C12's launch sentence still required tests
from every worker. It now says code workers. C14's output template still
unconditionally requested human inspection. It now makes required QA the next
step while that gate is pending. These were completions of approved changes
12 and 14, not new behavior.

Two fresh sessions then read only C12/C14 and their current source files:
[follow-up 1](repair-followup-1.md), [follow-up 2](repair-followup-2.md).
Both satisfied both criteria. The earlier raw reports are retained and are
not represented as evaluations of these final sentence edits.

Both follow-ups noted a possible terminal-status reporting gap for missing
code evidence. Disposition: no additional change. The harness footer says to
report when completed, errored or blocked; the main skill's Read and Monitor
rules keep missing proof incomplete and require follow-up. Its final checklist
applies at completion. An interim progress report and further evidence
collection satisfy these instructions without inventing a terminal status.

The generic default-target closing rule raised in C22 has an explicit local
delivery exception; both repetitions correctly applied it. No additional
change was needed for that observation. The separate blanket factory default
branch conflict discovered later remains recorded as change 28 in the audit.

## Limits

These are modeled interpretations of supplied observations. No fixture tests,
worker dispatch, QA, browser, GitHub write or deployment operations ran.
No no-skill control was run. These results do not prove runtime enforcement,
exhaustive behavior, or improvement relative to an unconfigured model.

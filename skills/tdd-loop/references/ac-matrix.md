# Acceptance-criteria matrix

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Build this before the first Red. It is the list of tests the loop owes; the loop is done when every row is closed.

## Rows

One row per acceptance criterion per path. A criterion with no edge or failure path says so in its row instead of omitting it.

| AC | Path | Scenario (input or state → observable result) | Proof | Status |
| -- | ---- | --------------------------------------------- | ----- | ------ |
| AC-1 | happy | valid credit note on invoice → total drops by the note amount | `invoice.test.ts` "AC-1: applies credit note" | green |
| AC-1 | edge | credit note larger than the invoice → total floors at 0 | `invoice.test.ts` "AC-1: floors at zero" | green |
| AC-1 | failure | credit note in another currency → 422 `currency_mismatch` | `invoice.test.ts` "AC-1: rejects currency mismatch" | green |
| AC-2 | alternative | viewer role opens the invoice → total visible, apply button absent | agentic-qa (UI, role) | owed to /agentic-qa |

Paths: `happy` (the stated behavior), `edge` (boundaries: empty, zero, max, long text, duplicates), `failure` (invalid input, upstream error, timeout), `alternative` (another entry point, role, state, or order of actions that reaches the same behavior).

`Proof` is a test name — a browser test in the project's end-to-end runner counts — or `agentic-qa (<surface>)` when only a running app can show it and the project has no such runner, or `deferred — <reason>`. A deferral needs a reason a reviewer could disagree with; "out of scope" alone is not one.

## Span check

After the rows, ask one question and write the answer under the table: *Which user-visible behavior in this ticket would no row catch if it broke?* Name it and add a row, or write "none found" with the behaviors you considered.

## Edges from the code

The ticket's criteria are not the only source of edges. For the code this change touches, list its guards — null checks, `catch` blocks, fallbacks, `default:` branches, status or enum fields — and give each guard the change reaches a boundary row. Use values the schema accepts so the test reaches the guard rather than the validator. For a status field, check that every consumer handles every value.

## Proof matches the surface

A test only proves the layer it runs in. Close a row with the proof its surface needs:

| Surface | Proof that closes the row |
| ------- | ------------------------- |
| Pure logic | Unit test |
| API or job | Test through the real handler, asserting status, body, and side effect |
| Persistence | Write, then read back through the owner path (reload, re-query) |
| UI | A browser test in the project's end-to-end runner, and `agentic-qa` — real interaction plus console and network observation |
| Concurrency | Repeated concurrent trigger; exactly the allowed number of successes |

## Test-quality check

Before completion, read each new test once more:

- More than half the asserts are presence-only (`not None`, `toBeTruthy`, `toBeDefined`) → assert values.
- The test mocks the unit it claims to test, or asserts that a mock returns what it was told to → rewrite against the real unit.
- The input and the expected value are both derived from the same helper, so passing is guaranteed by construction → use an independent expected value.
- Ask: would this test fail on a result that is structurally right but semantically wrong?

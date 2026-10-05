# Escape classes, comment template, and guard ladder

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

## Classes

Pick the one that names the gap in the checks, not the symptom. When two fit, pick the one whose check would have caught it earliest.

| Slug | The check that should have caught it |
| ---- | ------------------------------------ |
| `missed-empty-state` | A grid row for zero items, blank fields, or first-use screens |
| `missed-error-state` | A grid row with the API failing, timing out, or returning a validation error |
| `missed-loading-state` | A grid row while a request is in flight; double-submit during loading |
| `role-permission` | A cell per role, with presence proven for an allowed role |
| `responsive-layout` | The 375 and 1280 columns; long content |
| `console-error` | The console and page-error capture on every flow |
| `failed-request` | The 4xx/5xx capture on every flow |
| `stale-contract` | The risk-review contract lens: a consumer reads a field, route, or status the producer changed |
| `adjacent-flow` | A neighbour row for other screens and entry points that use the changed code |
| `persistence` | A write-then-reload round trip through the owner path |
| `keyboard-focus` | A keyboard-only row: Tab reaches the control, Enter/Space activates it, Escape closes overlays, and focus stays visible |
| `validation-boundary` | Edge rows for min, max, empty, duplicate, and format limits |
| `concurrency` | A repeated concurrent trigger |
| `copy-i18n` | Text checked against the source strings in each shipped locale |
| `environment-config` | A check that the setting, env var, or migration exists in the environment QA used |
| `not-a-regression` | Pre-existing on the base commit — record it, but it is not counted as an escape of this change |

A new slug needs a one-line definition in the comment and a proposal to add it here.

## Issue comment template

```markdown
**QA escape** · class `missed-empty-state` · area BILLING-WEB:/invoices · tested a1b2c3d (staging)

**Expected:** with no invoices, the list shows "No invoices yet"
**Actual:** the list area is blank and the console shows `TypeError: rows.map is not a function`
**Minimal case:** account with zero invoices; any role · reproduced 2 of 2 · base 9f8e7d6 not reproduced
**Evidence:** executed (staging @ a1b2c3d)

**Agent claim overturned:** agentic-qa VERIFIED on a1b2c3d — grid had no empty row for the invoice list
**Why missed:** empty list crashes → no empty-state row → criteria named only the populated list → grid built rows only from criteria → **check to change:** empty state is a default row for every list surface in BILLING-WEB:/invoices
**Regression test:** InvoiceList "renders empty message when no invoices" — browser flow, fails today
**Class count:** 2 of 3 in BILLING-WEB:/invoices (#212, #418)

<!-- qa-escape: class=missed-empty-state area=BILLING-WEB:/invoices pr=87 tested=a1b2c3d reproduced=yes -->
```

`Evidence:` is `executed (<env> @ <sha>)`, `supplied (<QA artifact>)`, or `mixed`; never imply supplied evidence was executed in this run.

## Guard ladder

When the class count reaches three, propose the highest rung that fits. A rung lower on the list is weaker because a person or agent can skip it.

Classify the escape first. **Mechanical** — a fixed pattern a tool can detect (a banned call, a missing required prop, an unhandled enum case, a file in the wrong place): propose rung 1 or 2 only; an instruction is never the guard for a mistake a check can catch. **Judgement** — it needs a reader to decide (which states a surface owes, whether copy fits): rung 3 or 4.

1. **Unwritable** — a type, schema constraint, required prop, exhaustive switch, or database constraint that makes the mistake fail to compile or save.
2. **Automated check** — a lint rule, CI job, or test helper that fails on the mistake.
3. **Standing grid row** — a default `/agentic-qa` row for every surface in the area, written into the `## QA escape guards` section so the tester reads it.
4. **Instruction** — a rule line in `## QA escape guards`. Use only when rungs 1–3 cannot express it.

Every proposal names the three issues, the rung, the exact change, and what it deliberately leaves possible. The workspace `AGENTS.md` section looks like:

```markdown
## QA escape guards

- BILLING-WEB:/invoices — every list surface gets an empty-state grid row (missed-empty-state: #212, #418, #431).
```

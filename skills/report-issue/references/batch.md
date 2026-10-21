# Batch mode

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Load when the input holds more than one distinct problem or names `batch`.

## Split

1. Number each distinct problem in input order. One sentence that describes two symptoms on two screens is two problems.
2. Assign each screenshot to a problem by its filename, caption or position in the input. An unclear assignment stays unassigned and is listed in the draft for the reporter to place.
3. At most 10 problems per run. More → draft the first 10 and list the rest for the next run.

## Per problem

Run workflow steps 1–4 for each problem. Code-search lanes are per project, not per problem: one lane may serve several problems in the same project.

Check duplicates across the batch as well as the tracker. Two problems with the same symptom on the same screen merge into one draft that quotes both statements. Problems with a shared lead but different symptoms stay separate and are listed as related to each other.

## Draft and approval

Show one summary table, then each full draft under its number:

```
| # | Title | Team | Class | Priority | Cycle · due | Workflow | Duplicate |
| 1 | PARTNERS-WEB: Show empty-state message on an empty invoice list | PRWL | bug | High | 5 · 2026-10-30 | ready-for-agent | none |
| 2 | PARTNERS-API: Return 422 for a missing transfer date | PRA | bug | Medium | 6 · 2026-11-13 | needs-triage | none |
| 3 | merged into 1 | — | — | — | — | — | — |
Reply yes for all, yes 1,2 for some, drop <n>, or <n>: <field change>.
```

Unanswered items are not created. Reporter away → print the drafts and stop.

## Create

Apply approved create/comment operations in number order per step 6; duplicate comments change no issue fields. Relate only newly created items listed as related. Read back each result. A failure on one item is reported in its row; continue with the rest.

## Output

```
Created 2 of 3 (1 merged; report duplicate comments separately when present)
| # | Issue | Title | Priority · cycle |
| 1 | PRWL-212 <url> | PARTNERS-WEB: Show empty-state message on an empty invoice list | High · 5 |
| 2 | PRA-431 <url> | PARTNERS-API: Return 422 for a missing transfer date | Medium · 6 |
```

# Rubric — `/agents-md`

Two independent axes. A skill can route perfectly and still waste the context it earns.

Zero attribution: omit co-author, AI, and tool attribution from evaluation artifacts and publications.

## 1. Trigger eval (routing)

Does the runtime load this skill, and not a sibling? Scored from [`evals.json`](evals.json) by the
harness in `tools/trigger-evals/`: build the catalog, build the queryset, run **three independent
judge agents** that route each query using only the catalog, then take a majority vote per query.

- A `trigger` query passes when the majority picks `/agents-md`.
- A `no-trigger` query passes when a valid majority picks another catalog entry or `none`. Missing, malformed, or split votes do not pass. Its `route` field is
  diagnostic, not pass/fail.

Pass bar: **20/20**, matching the current JSON query set. Investigate failures against the catalog and intended boundary; never delete a failing query to inflate the score.

## 2. Quality (body)

Eleven categories, 1–5, scored by a reader who did not write the edits.

| Score | Meaning |
| :--- | :--- |
| 5 | No defect found within the documented review scope, supported by stated checks; untested tasks remain unproven. |
| 4 | Strong, but a reviewer can point at one concrete line. |
| 3 | A real gap that would produce a wrong or incomplete run. |
| 2 | Materially incomplete or misleading. |
| 1 | Absent or harmful. |

Categories: purpose clarity · trigger clarity · scope control · instruction quality · brevity ·
engineering usefulness · agent usability · verification quality · TDD/testing compat ·
maintainability · frontier readiness.

**Trigger clarity is scored from routing evidence, not prose.** State the actual run date and whether it was rerun. Name any colliding sibling and misrouted query, or missing runtime evidence. Catalog routing does not prove a host implicitly loads a user-only skill.

`N/A` is permitted only on TDD/testing compat, only when the skill has no testable surface, and only
with a written justification. It is not a way to dodge a hard category.

Shared anchors and the deep-dive sheets live in `evals/` at the repo root; this file is the local,
self-sufficient copy of what applies to `/agents-md`.

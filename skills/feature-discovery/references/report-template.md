# Feature discovery report template

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Fill each section with ≤3 bullets; bracketed text says what belongs there.

```markdown
# Feature discovery: [Topic]

## 1. Summary

- [Main answer from current code, scoped projects, key caveat, and any deferred slices.]

## 2. What it does

- [Behavior in product/domain terms: inputs, outputs, side effects, project(s).]

## 3. How it works

- [Flow; key files, functions, routes, configs, jobs; conditions, flags, error paths.]

## 4. Where it is used

- [Usage sites with file references; tests/docs/configs confirming usage.]

## 5. Graphify

- [Graph used and freshness; queries run; hits confirmed by code vs drift. Or: not available.]

## 6. ADRs

- [ADR, status, decision; agrees with or conflicts with current code (cite both). Or: none found in <paths searched>.]

## 7. Why it was needed / context

- [Recorded rationale and intended behavior, cited separately from implementation; or no reliable rationale found in the inspected sources.]

## 8. Candidate GLOSSARY.md terms

- [`Term` — action; description; evidence; why it matters. For discrepancies, quote context beside implementation and approved intent; do not assume context is stale.]
- [End with: "Reply with the term names to approve, wording changes, `approve all`, or `skip context updates`." If none: "No candidate GLOSSARY.md term updates found."]

## 9. Risks, gaps, and recommended next checks

- [Unresolved questions, missing evidence, contradictions, or risks; next check and unexamined scope.]
- [When a why-or-when question remains: "Want me to scan git history for <question> in <files>, last 2 months?"]

## 10. Validation performed

- [Inspected projects/states, evidence types and checks in both passes; commands actually run; skipped checks; tracker outcome (unnecessary, bounded, approved broad scan, skipped, unavailable) and issues read/excluded.]

## 11. Suggested next skills (optional)

- [/skill-name: reason tied to this report. 1–3 items, adjacent workflow steps.]
```

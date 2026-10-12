# Polish verify

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

### verify

After the dispatched tasks report back.

1. Scope check first: compare each group's diff with the pre-dispatch state and row list. Flag new changes outside the rows; undo only this run's isolated edits or route to `/to-tickets`. Preserve pre-existing user changes; never absorb scope violations silently.
2. Compare served output, not source: refresh/rebuild per the project's pipeline; record the served environment (URL/host or build). Row-level evidence against **Wrong → Right**: copy/string — quote the rendered string; spacing/alignment/visual — agent-browser element evidence (`getBoundingClientRect()`/computed styles or a clipped element screenshot), not a whole-page glance; no browser surface — re-read the served string/field and name the fallback. Never mark a row verified on assumption. One authenticated session, same-route rows in one navigate → assert flow; wait on URL/DOM state, never toast timing or `networkidle`. A row also fails on a new console error on its route compared with before dispatch.
3. Mark each row `verified` (evidence in or beside **Shot**), `reopened` with fresh failure evidence, or `dispatched` with a named missing check. A missing pre-dispatch console baseline leaves browser rows `dispatched`; do not infer the baseline from the changed build.
4. Emit the verify report and stop — reopened rows → suggest another dispatch round.

**Verify report:**

```markdown
Stage: verify — compared served output for <N> dispatched rows.
Environment: <PROJECT-CODE → served URL/host or build>.
Found: <PROJECT-CODE>: v verified / r reopened / p dispatched awaiting proof; <next code…>.
Next: ship the verified pass, or another dispatch round for reopened rows <#s or "none">.
Needs user: <missing baseline/proof or scope violations routed out, or "none">.

Suggested next skills (optional):
- /code-review: eyeball the batched polish diff before shipping.
- /commit-push-pr (or /commit-push-close): ship the verified polish pass.
```

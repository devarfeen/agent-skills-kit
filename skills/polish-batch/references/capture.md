# Polish capture

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

### capture (default)

1. Record initial `git status` and relevant diffs. Infer `<SPEC-ID>` from the request or session; if none exists, use the date-keyed file. Open or create the punch-list.
2. For each nit: apply the cosmetic-scope rule — route-outs get no row. Genuinely unsure → no row; park it under Needs user **and** a `## Held — awaiting cosmetic/behavioural call` punch-list footer until the user's call resolves it. Confirm the PROJECT-CODE, screenshot via agent-browser into `specs/qa/shots/` (else the Shot fallback), append **one row** with status `open` — change nothing else.
3. Emit the capture update with the open-row count.

**Capture update:**

```markdown
Stage: capture — logged N nit(s), no fixes applied.
Found: <total> open rows — <PROJECT-CODE>: x, <PROJECT-CODE>: y.
Routed out (not nits): <item> → /to-tickets | /qa-escape #<issue> (touches <behaviour|data|interface>).  [omit if none]
Next: keep capturing, or say "dispatch" to fix the open rows.
Needs user: <ambiguous PROJECT-CODE or borderline-cosmetic item, or "none">.
```

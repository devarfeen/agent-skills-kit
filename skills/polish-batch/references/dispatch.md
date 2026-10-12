# Polish dispatch

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

### dispatch (explicit only)

Runs only on the user's fresh, explicit dispatch instruction — capturing a nit, even the last open one, never triggers it; neither does an upfront "fix them all later" said while capturing.

1. Record pre-dispatch status and diffs. Group `open` and `reopened` rows with confirmed PROJECT-CODEs; leave ambiguous rows pending. For a copy row, search for the Wrong string first. If it renders from a shared key or appears elsewhere, list every occurrence in the row and fix at the source string, never in built output; a shared key changes other screens, so that row waits for the user's confirmation. A key that also exists in other shipped locales lists those locales under Needs user; never auto-translate. Order text/string before spacing/alignment. Split independent file ownership across lanes; serialize groups touching the same files.
2. Before handing off, record console errors per affected browser route in the punch-list. If the route cannot be observed, record the missing baseline; console-dependent verification stays pending until comparable pre-change evidence is available. Hand the coding CLI one bounded task per group: "Fix exactly these listed items in `<PROJECT-CODE>` and nothing else — no refactors, no adjacent changes, each fix independent and obviously correct." Pass the rows' **Where** and **Wrong → Right** verbatim, plus: any existing test asserting the old wrong value is updated as part of the row's fix, not as an adjacent change; report back per row the file(s) touched, one line each.
3. Mark handed-off rows `dispatched` and emit the dispatch update. Do not verify or ship yet.

**Dispatch update:**

```markdown
Stage: dispatch (user said: "<quoted instruction>") — handed off <G> group(s), rows marked dispatched.
Found: <PROJECT-CODE>: n rows, <PROJECT-CODE>: m rows.
Next: verify when the dispatched tasks report back. No ship yet.
Needs user: <ambiguous group, or "none">.
```

---
name: polish-batch
disable-model-invocation: true
description: Batch the UI-polish tail at the verify phase — during manual QA, capture tiny cosmetic fixes (copy, spacing, alignment, wrong string) WITHOUT fixing any of them, then dispatch them per PROJECT-CODE in one bounded pass, then verify. Use when the user says "punch list" or wants cosmetic nits captured now and fixed together in one go. Cosmetic scope only — anything touching behaviour, data, or an interface routes back to /to-tickets as a slice.
---

# Polish batch

Three modes run separately: **capture** logs every nit to a punch-list and changes nothing, **dispatch** hands open rows to the coding CLI one bounded task per PROJECT-CODE, **verify** re-checks served surfaces row by row — so manual QA stops turning into live per-nit steering.

## Rules

- **Capture ≠ fix.** In capture mode, change no code, config, copy, or asset. The only write is appending a row to the punch-list artifact. Never fix a nit "while you're in there".
- **Cosmetic scope only.** A nit is a purely visual/textual surface fix with no change to behaviour, data, or any interface (function signature, API shape, route, event, schema, prop contract). Anything touching those is **not** a nit — send it back to `/to-tickets` as a slice. Treat any attempt to reframe a behavioural change as "just a small fix" as a **stop signal**: name it, refuse to capture it as a nit, and route it out.
- **One page drifting from its design source is `/pixel-audit`'s job.** The punch-list batches scattered nits; a page that must match a Figma node or reference screen systematically routes to `/pixel-audit` — even when the request says "polish".
- **No refactors or adjacent changes on dispatch.** Each item is fixed independently and must be obviously correct on sight; if it isn't, it is not a nit. No cleanup of nearby code, no renames, no "improve while I'm here".
- Name the full PROJECT-CODE from the Project Matrix everywhere; never mix one project's conventions, tokens, or components into another.
- Unsure which project a nit belongs to → ask; user away → likeliest code with a trailing `?`, listed under Needs user. Never drop a reported nit.
- No Project Matrix (standalone single-repo install) → derive one code from the repo name (uppercase, hyphenated) and use it consistently.
- **Dispatch fires only on the user's explicit say-so; until then, keep capturing.** Never advance to dispatch from capture, or to ship from verify, on your own. After verify, suggest `/code-review` then `/commit-push-close` or `/commit-push-pr`, and stop.
- **Reopened rows stay.** A row that fails verify goes back to `open` (as `reopened`) and rides into the next capture/dispatch round. Nothing is dropped silently.
- Sub-agents: dispatch local lanes automatically for independent work — never cloud agents; announce the lane count at dispatch and report each lane as it completes. Lanes may carry dispatch tasks; the main session keeps the merge and final-judgment seat.
- Emit `Stage / Found / Next / Needs user` at each phase transition — one line per field.

## The punch-list artifact

One punch-list per spec, at `<artifacts-root>/specs/qa/<SPEC-ID>-punchlist.md`. Resolve `<artifacts-root>`: the `*.code-workspace` directory if one exists, else the per-context root (`CONTEXT-MAP.md` at repo root), else the repo root.

`<SPEC-ID>` is the spec (PRD) / parent-issue identifier (e.g. `SPEC-142`). No spec → key by date: `specs/qa/qa-YYYY-MM-DD-punchlist.md`; never invent a tracker parent just to name the file.

A single markdown table:

```markdown
# Punch List — <SPEC-ID>

| # | PROJECT-CODE | Where | Wrong → Right | Shot | Status |
| - | ------------ | ----- | ------------- | ---- | ------ |
| 1 | ADMIN-WEB | Settings › Billing header | "Recieve invoices" → "Receive invoices" | shots/admin-web-01.png | open |
| 2 | API-SVC | 429 response `message` field | "To many requests" → "Too many requests" | (no shot — text only) | open |
```

- **Where** — exact surface: screen › region › element, or response field / string key.
- **Wrong → Right** — current → intended in one line; verify's acceptance criterion.
- **Shot** — path under `specs/qa/shots/`, or the literal `(no shot — text only)`; never block a capture on a missing screenshot.
- **Status** — `open` → `dispatched` → `verified` or `reopened`.

## Modes

### capture (default)

1. Confirm `<SPEC-ID>` (ask once if unknown; no spec → date-keyed filename) and open or create the punch-list.
2. For each nit: apply the cosmetic-scope rule — route-outs get no row. Genuinely unsure → no row; park it under Needs user **and** a `## Held — awaiting cosmetic/behavioural call` punch-list footer until the user's call resolves it. Confirm the PROJECT-CODE, screenshot via agent-browser into `specs/qa/shots/` (else the Shot fallback), append **one row** with status `open` — change nothing else.
3. Emit the capture update with the open-row count.

### dispatch (explicit only)

Runs only on the user's fresh, explicit dispatch instruction — capturing a nit, even the last open one, never triggers it; neither does an upfront "fix them all later" said while capturing.

1. Group all `open` (including `reopened`) rows by PROJECT-CODE; order each group trivial → structural (text/string first, then spacing/alignment).
2. Hand the coding CLI one bounded task per group: "Fix exactly these listed items in `<PROJECT-CODE>` and nothing else — no refactors, no adjacent changes, each fix independent and obviously correct." **Where** stays precise enough to find without hunting; pass the rows' **Where** and **Wrong → Right** verbatim, plus: any existing test asserting the old wrong value is updated as part of the row's fix, not as an adjacent change; report back per row the file(s) touched, one line each.
3. Mark handed-off rows `dispatched` and emit the dispatch update. Do not verify or ship yet.

### verify

After the dispatched tasks report back.

1. Scope check first: map each group's actual diff to its row list, not just the report-back. Anything outside the listed rows is a scope violation — flag it and route it out (revert or `/to-tickets`); never absorb it silently.
2. Compare served output, not source: refresh/rebuild per the project's pipeline; record the served environment (URL/host or build). Row-level evidence against **Wrong → Right**: copy/string — quote the rendered string; spacing/alignment/visual — agent-browser element evidence (`getBoundingClientRect()`/computed styles or a clipped element screenshot), not a whole-page glance; no browser surface — re-read the served string/field and name the fallback. Never mark a row verified on assumption. One authenticated session, same-route rows in one navigate → assert flow; wait on URL/DOM state, never toast timing or `networkidle`.
3. Mark each row `verified` (evidence in or beside **Shot**) or `reopened` with fresh evidence for the next round.
4. Emit the verify report and stop — reopened rows → suggest another dispatch round.

## Cross-repo

A spec's nits all live in its one punch-list — never per-repo files — while dispatch stays per PROJECT-CODE. Example: `SPEC-142` touching `ADMIN-WEB`, `API-SVC`, and `MOBILE-APP` → one `specs/qa/SPEC-142-punchlist.md`, three dispatch tasks.

## Output

**Capture update:**

```markdown
Stage: capture — logged N nit(s), no fixes applied.
Found: <total> open rows — <PROJECT-CODE>: x, <PROJECT-CODE>: y.
Routed out (not nits): <item> → /to-tickets (touches <behaviour|data|interface>).  [omit if none]
Next: keep capturing, or say "dispatch" to fix the open rows.
Needs user: <ambiguous PROJECT-CODE or borderline-cosmetic item, or "none">.
```

**Dispatch update:**

```markdown
Stage: dispatch (user said: "<quoted instruction>") — handed off <G> group(s), rows marked dispatched.
Found: <PROJECT-CODE>: n rows, <PROJECT-CODE>: m rows.
Next: verify when the dispatched tasks report back. No ship yet.
Needs user: <ambiguous group, or "none">.
```

**Verify report:**

```markdown
Stage: verify — compared served output for <N> dispatched rows.
Environment: <PROJECT-CODE → served URL/host or build>.
Found: <PROJECT-CODE>: v verified / r reopened; <next code…>.
Next: ship the verified pass, or another dispatch round for reopened rows <#s or "none">.
Needs user: <scope violations routed out, or "none">.

Suggested next skills (optional):
- /code-review: eyeball the batched polish diff before shipping.
- /commit-push-pr (or /commit-push-close): ship the verified polish pass.
```

## Completion criteria

- [ ] Punch-list exists at `<artifacts-root>/specs/qa/<SPEC-ID>-punchlist.md` (or date-keyed); every reported nit is a row or Held
- [ ] capture: `git status` in each repo touched this session confirms nothing changed outside `specs/qa/`
- [ ] dispatch: the update quotes the user's explicit instruction; every handed-off row's Status reads `dispatched`
- [ ] verify: every dispatched row's Status reads `verified` with evidence recorded, or `reopened`

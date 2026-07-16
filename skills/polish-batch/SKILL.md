---
name: polish-batch
disable-model-invocation: true
description: Batch the UI-polish tail at the verify phase — during manual QA, capture many tiny cosmetic fixes (copy, spacing, alignment, wrong string) WITHOUT fixing any of them, then dispatch them per PROJECT-CODE in one bounded pass, then verify. Use when the user is doing manual QA and logging small nits, says "punch list", "polish pass", "cosmetic cleanup", "batch these nits", "capture this for later", or wants to collect cosmetic fixes now and fix them all in one go. Cosmetic scope only — anything touching behaviour, data, or an interface routes back to /to-tickets as a slice.
---

# Polish Batch

## Purpose

Batch the UI-polish tail so manual QA stops turning into live per-nit steering. During QA the user spots many tiny cosmetic fixes — wrong copy, off-by-a-few-pixels spacing, misalignment, a wrong string. Instead of fixing each one the moment it is seen (which fragments attention and derails the QA pass), this skill runs three separate modes:

```text
capture  →  dispatch  →  verify
```

- **capture** (default): log each nit to a punch-list artifact and change nothing.
- **dispatch** (only on explicit user say-so): hand the coding CLI one bounded task per PROJECT-CODE.
- **verify**: re-check the affected screens against the punch-list and mark each row.

It sits at the **verify** phase, between manual QA and ship.

## Rules

- **Capture ≠ fix.** In capture mode, change no code, config, copy, or asset. The only write is appending a row to the punch-list artifact. Never fix a nit "while you're in there".
- **Cosmetic scope only.** A nit is a purely visual/textual surface fix with no change to behaviour, data, or any interface (function signature, API shape, route, event, schema, prop contract). If an item touches behaviour, data, or an interface, it is **not** a nit — send it back to `/to-tickets` as a slice. Treat any attempt to reframe a behavioural change as "just a small fix" as a **stop signal**: name it, refuse to capture it as a nit, and route it out.
- **One page drifting from its design source is `/pixel-audit`'s job.** The punch-list batches scattered nits found during QA; a page that must match a Figma node or reference screen systematically routes to `/pixel-audit` instead — even when the request says "polish".
- **No refactors or adjacent changes on dispatch.** Each item is fixed independently and must be obviously correct on sight. No cleanup of nearby code, no renames, no "improve while I'm here". If a fix is not obviously correct at a glance, it is not a nit.
- **Always name the full PROJECT-CODE** from the Project Matrix for every row and every dispatch. Never mix one project's conventions (copy tone, spacing scale, component idioms) into another. When in doubt about which project a nit belongs to, ask before capturing; if the user is away, capture it under the likeliest code with a trailing `?` and list it under Needs user — never drop a reported nit. No Project Matrix (standalone single-repo install) → derive one code from the repo name (uppercase, hyphenated) and use it consistently.
- **Suggest, never auto-chain.** After verify, suggest `/code-review` then `/commit-push-close` or `/commit-push-pr`, and stop. Never advance to dispatch from capture, or to ship from verify, on your own.
- **Reopened rows stay.** A row that fails verify goes back to `open` (as `reopened`) and rides into the next capture/dispatch round. Nothing is dropped silently.
- **Local-only.** Use local subagents and local background where the runtime supports it and the user has allowed them; never hand work to cloud agents.

## The punch-list artifact

One punch-list per spec, at:

```text
<artifacts-root>/specs/qa/<SPEC-ID>-punchlist.md
```

`<SPEC-ID>` is the spec (PRD) / parent-issue identifier the QA pass is tied to (e.g. `SPEC-142`). Ad-hoc polish with no spec → key by date instead: `specs/qa/qa-YYYY-MM-DD-punchlist.md`; never invent a tracker parent just to name the file. Resolve `<artifacts-root>` the same way the other kit skills do: (1) the directory containing a `*.code-workspace` file if one exists, (2) the per-context root in a multi-context repo (`CONTEXT-MAP.md` at root), (3) the single repo root — so punch-lists stay out of individual project repos when a workspace exists.

The file is a single markdown table:

```markdown
# Punch List — <SPEC-ID>

| # | PROJECT-CODE | Where | Wrong → Right | Shot | Status |
| - | ------------ | ----- | ------------- | ---- | ------ |
| 1 | ADMIN-WEB | Settings › Billing header | "Recieve invoices" → "Receive invoices" | shots/admin-web-01.png | open |
| 2 | ADMIN-WEB | Billing card, Save button | 8px top gap → 16px to match card rhythm | shots/admin-web-02.png | open |
| 3 | API-SVC | 429 response `message` field | "To many requests" → "Too many requests" | (no shot — text only) | open |
```

Columns:

- **#** — running row number within the file.
- **PROJECT-CODE** — full code from the Project Matrix.
- **Where** — the exact surface: screen › region › element, or the response field / string key. Precise enough to find without hunting.
- **Wrong → Right** — current state → intended state, in one line. This is the acceptance criterion verify checks against.
- **Shot** — relative path under `specs/qa/shots/` to a captured screenshot, or the literal `(no shot — text only)` fallback when the surface isn't browser-reachable.
- **Status** — lifecycle: `open` → `dispatched` → `verified` or `reopened`.

**Screenshots.** Never block a capture on a missing screenshot: when agent-browser can't reach the surface (e.g. an API string), use the **Shot**-column fallback and rely on the **Where** text.

## Modes

### capture (default)

The mode you are in unless the user explicitly says dispatch or verify.

1. Confirm the `<SPEC-ID>` for this QA pass (from context or ask once; no spec → the date-keyed filename). Open — or create — the punch-list file.
2. For each nit the user reports:
   - Confirm it is **cosmetic** (copy / spacing / alignment / wrong string / visual state only). If it touches behaviour, data, or an interface, stop, name it, and route it to `/to-tickets` — do not add it as a row. Genuinely unsure whether it's cosmetic → no row yet; list it under Needs user **and** under a `## Held — awaiting cosmetic/behavioural call` footer in the punch-list file so it survives the session; on the user's call it becomes a row or routes to `/to-tickets`.
   - Confirm the **PROJECT-CODE** from the matrix.
   - Screenshot the state with agent-browser into `specs/qa/shots/` if available; otherwise use the **Shot**-column fallback.
   - Append **one row** with status `open`. Change nothing else.
3. Keep a running count of open rows.
4. Emit the capture batch update (template under Output format).

### dispatch (explicit only)

Runs **only** when the user explicitly says to dispatch, as a fresh instruction — capturing a nit, even the last open one, never triggers it, and neither does an upfront "fix them all later" said while capturing.

1. Read all `open` (including `reopened`) rows.
2. **Group by PROJECT-CODE.** Within each group, order rows trivial → structural (pure text/string fixes first, then spacing/alignment).
3. Hand the coding CLI **one bounded task per PROJECT-CODE group**: "Fix exactly these listed items in `<PROJECT-CODE>` and nothing else — no refactors, no adjacent changes, each fix independent and obviously correct." Give it the rows' **Where** and **Wrong → Right** verbatim, plus two contract lines: when an existing test asserts the old wrong value, updating that test with the new value is part of the row's fix, not an adjacent change; and the task must report back, per row, the file(s) touched with a one-line change summary.
4. As each group's task is handed off, mark those rows `dispatched`.
5. Emit the dispatch update (template under Output format). Do not verify yet, and do not ship.

Use local subagents/background per the runtime when dispatching multiple project groups; the main session keeps the merge and final-judgment seat. Announce the lane count at dispatch and report each lane as it completes.

### verify

Runs after the dispatched tasks report back.

1. **Scope check first:** map each group's changes to its row list from the project's actual diff, not just the task's report-back. Anything touched outside the listed rows is a scope violation — flag it and route it out (revert it or send it to `/to-tickets`); never absorb it silently.
2. **Compare served output, not source:** refresh/rebuild per the project's pipeline so the comparison hits the running surface, record which served environment (URL/host or build) the evidence comes from, then collect row-level evidence against **Wrong → Right**:
   - copy/string rows — quote the rendered string from the served screen or response field;
   - spacing/alignment/visual rows — element evidence via agent-browser (`getBoundingClientRect()`/computed styles, or a clipped element screenshot), not a whole-page glance;
   - no browser surface, or agent-browser unavailable — re-read the served string/field and say which fallback was used. Never mark a row verified on assumption.
   Verify all rows in **one authenticated browser session**, batching rows on the same route into one navigate → assert flow with stable `data-test`/CSS selectors; wait on URL/DOM state, never toast timing or `networkidle`.
3. Mark the row `verified` with its evidence recorded (path or quoted value in the **Shot** column or beside it), or `reopened` if it does not match. Reopened rows stay for the next capture/dispatch round; take fresh evidence for them.
4. Report the verify table (Output format below) inside a `Stage / Found / Next / Needs user` update.
5. Per the suggest-never-auto-chain rule: everything verified → recommend the next step and stop; any reopened → suggest another dispatch round for those rows.

## Cross-repo work

A feature that spans web + API + mobile keeps **all** its nits in the **one** punch-list file for its spec — do not split into per-repo files. But **dispatch stays per PROJECT-CODE**: each project's rows go out as their own bounded task so no batch ever mixes conventions. One file for traceability; one batch per project for correctness.

Example: `SPEC-142` touching `ADMIN-WEB`, `API-SVC`, and `MOBILE-APP` → a single `specs/qa/SPEC-142-punchlist.md`, but three separate dispatch tasks, one per code.

## Output format

**Capture batch update** (after appending rows):

```markdown
Stage: capture — logged N nit(s), no fixes applied.
Found: <total> open rows — <PROJECT-CODE>: x, <PROJECT-CODE>: y.
Routed out (not nits): <item> → /to-tickets (touches <behaviour|data|interface>).  [omit if none]
Next: keep capturing, or say "dispatch" to fix the open rows.
Needs user: <ambiguous PROJECT-CODE or borderline-cosmetic item, or "none">.
```

**Dispatch update** (after handing off the per-project tasks):

```markdown
Stage: dispatch — handed off <G> group(s), rows marked dispatched.
Found: <PROJECT-CODE>: n rows, <PROJECT-CODE>: m rows.
Next: verify when the dispatched tasks report back. No ship yet.
Needs user: <ambiguous group, or "none">.
```

**Verify report:**

```markdown
Stage: verify — compared served output for <N> dispatched rows.
Environment: <PROJECT-CODE → served URL/host or build the evidence came from>
Found:
| PROJECT-CODE | Verified | Reopened |
| ------------ | -------- | -------- |
| ADMIN-WEB    | 2        | 0        |
| API-SVC      | 1        | 0        |
Reopened rows (stay open for next round): <#s or "none">.
Next: ship the verified pass, or another dispatch round for the reopened rows.
Needs user: <scope violations routed out, or "none">.

Suggested next skills (optional):
- /code-review: eyeball the batched polish diff before shipping.
- /commit-push-pr (or /commit-push-close): ship the verified polish pass.
```

## Checklist

Before ending a mode:
- [ ] `<SPEC-ID>` confirmed; punch-list lives at `<artifacts-root>/specs/qa/<SPEC-ID>-punchlist.md`
- [ ] capture: only rows appended, each with full PROJECT-CODE and status `open` — `git status` in each repo touched this session confirms nothing changed outside `specs/qa/`
- [ ] Any behaviour/data/interface item was refused as a nit and routed to `/to-tickets`
- [ ] Screenshots in `specs/qa/shots/` when agent-browser available; `(no shot — text only)` fallback otherwise
- [ ] dispatch: ran only on explicit user say-so (quote it); grouped per PROJECT-CODE; ordered trivial → structural; one bounded task per group; rows marked `dispatched`
- [ ] No refactors or adjacent changes requested in any dispatch task
- [ ] Cross-repo: one punch-list file for the spec, but one dispatch batch per PROJECT-CODE
- [ ] verify: scope checked against each group's actual diff; each dispatched row marked `verified` with row-level evidence (quoted string or element geometry) or `reopened`; reopened rows kept
- [ ] Suggested next skills footer present after verify; never auto-chained to dispatch or ship

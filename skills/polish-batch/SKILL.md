---
name: polish-batch
disable-model-invocation: true
description: "Create a cosmetic QA punch list, with or without a ticket; capture, dispatch or verify rows. Figma matching: /pixel-audit. Behavioral bug reports or QA issue-filing sessions: /to-tickets."
metadata:
  version: "0.2.0"
---

# Polish batch

Three modes run separately — **capture**, **dispatch**, **verify** — so manual QA stops turning into live per-nit steering.

## Rules

- **Capture ≠ fix.** In capture mode, change no product code, config, copy, or asset. Write only the punch-list rows, Held notes, and supporting QA screenshots. Never fix a nit "while you're in there".
- Zero attribution: never add or leave co-author, AI, or tool attribution in commits, PRs, issue comments, release notes, generated docs, settings, or code comments.
- **Cosmetic scope only.** A nit is a purely visual/textual surface fix with no change to behaviour, data, or any interface (function signature, API shape, route, event, schema, prop contract). Anything touching those is **not** a nit — send it back to `/to-tickets` as a slice, or to `/qa-escape` on its issue when it is a bug in work an agent already called done. Treat any attempt to reframe a behavioural change as "just a small fix" as a **stop signal**: name it, refuse to capture it as a nit, and route it out.
- **One page drifting from its design source is `/pixel-audit`'s job.** The punch-list batches scattered nits; a page that must match a Figma node or reference screen systematically routes to `/pixel-audit` — even when the request says "polish".
- **No refactors or adjacent changes on dispatch.** Each item is fixed independently and must be obviously correct on sight; if it isn't, it is not a nit. No cleanup of nearby code, no renames, no "improve while I'm here".
- Name the full PROJECT-CODE from the Project Matrix everywhere; never mix one project's conventions, tokens, or components into another.
- Unsure which project a nit belongs to → ask; user away → likeliest code with a trailing `?`, listed under Needs user. Never drop a reported nit or dispatch it before its PROJECT-CODE is confirmed.
- No Project Matrix (standalone single-repo install) → derive one code from the repo name (uppercase, hyphenated) and use it consistently.
- **Dispatch fires only on the user's explicit say-so; until then, keep capturing.** Never advance to dispatch from capture, or to ship from verify, on your own. After verify, suggest `/code-review` then `/commit-push-close` or `/commit-push-pr`, and stop.
- **Reopened rows stay.** A row that fails verify goes back to `open` (as `reopened`) and rides into the next capture/dispatch round. Nothing is dropped silently.
- Sub-agents: dispatch local lanes automatically for independent work — never cloud agents; announce the lane count at dispatch and report each lane as it completes. Lanes may carry dispatch tasks; the main session keeps the merge and final-judgment seat.
- Emit `Stage / Found / Next / Needs user` at each phase transition — one line per field.

## The punch-list artifact

One punch-list per spec, at `<artifacts-root>/specs/qa/<SPEC-ID>-punchlist.md`. Resolve `<artifacts-root>`: the `*.code-workspace` directory if one exists, else the per-context root (`GLOSSARY-MAP.md` at repo root; legacy `CONTEXT-MAP.md`), else the repo root.

`<SPEC-ID>` is the spec (PRD) / parent-issue identifier (e.g. `SPEC-142`). No spec → key by date: `specs/qa/qa-YYYY-MM-DD-punchlist.md`; never invent a tracker parent just to name the file.

A single markdown table:

```markdown
# Punch List — <SPEC-ID>

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

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

Run only the requested mode; capture is the default. Load its procedure and
output shape, not the other modes:

- **capture** — [`references/capture.md`](references/capture.md): append QA artifacts only.
- **dispatch** — [`references/dispatch.md`](references/dispatch.md): after a fresh explicit dispatch instruction, group bounded fixes and record pre-change console evidence.
- **verify** — [`references/verify.md`](references/verify.md): after tasks report back, compare scoped diffs and served results; missing proof stays pending.

## Cross-repo

A spec's nits all live in its one punch-list — never per-repo files — while dispatch stays per PROJECT-CODE: one file, one dispatch task per project touched.

## Output

Emit the selected mode's update from its reference. Verify ends with 1–3
advisory next-skill suggestions and stops; it never starts shipping.

## Completion criteria

- [ ] Punch-list exists at `<artifacts-root>/specs/qa/<SPEC-ID>-punchlist.md` (or date-keyed); every reported item is a row, Held, or explicitly routed out
- [ ] capture: initial versus final status and diffs show this run wrote only QA artifacts; pre-existing changes remain intact
- [ ] dispatch: the update quotes the user's explicit instruction; every handed-off row's Status reads `dispatched`
- [ ] verify: every dispatched row is `verified` with evidence, `reopened` with a failure, or `dispatched` with the missing check named

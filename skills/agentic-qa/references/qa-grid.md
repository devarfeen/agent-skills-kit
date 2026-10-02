# QA grid, reach trace, and state recipes

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

## Reach trace

A change reaches a screen when any changed file sits on a path that ends at something a user sees. Trace forward from each changed file until one of these holds, and quote the chain:

| Changed file kind | Reaches a screen when |
| ----------------- | --------------------- |
| Component, view, template, page, layout | Always — name the route that renders it |
| Style, token, translation, asset | Any route loads it |
| Store, composable, hook, view model | A rendered component imports it |
| API handler, controller, resource, serializer | A screen calls the endpoint — search the frontend for the route path or the generated client method |
| Model, query, policy, job, mail | Its output reaches one of the rows above — a policy that hides a button, a job that changes a listed status |
| Migration | A screen lists or edits the changed column |

Only tooling, CI, docs, or test-only changes with no such chain are `no-ui-reach`. When unsure, the change reaches.

## Grid template

```markdown
# QA grid — PR #87 @ a1b2c3d (BILLING-WEB)

Surfaces: /invoices/{id} (InvoiceShow.vue), /invoices (InvoiceList.vue — neighbour)
Roles: admin (QA_ADMIN_EMAIL / QA_ADMIN_PASSWORD), viewer (QA_VIEWER_EMAIL / QA_VIEWER_PASSWORD)

| Row | State | 375 admin | 1280 admin | 375 viewer | 1280 viewer |
| --- | ----- | --------- | ---------- | ---------- | ----------- |
| AC-1 apply credit note | success | pass | pass | not reachable — viewer has no apply action (presence shown for admin) | same |
| AC-1 apply credit note | error (API 500) | pass | fail F1 | not reachable — same | same |
| AC-1 apply credit note | long content (40-char note) | fail F2 | pass | pass | pass |
| AC-2 total visible | default | pass | pass | pass | pass |
| Escape: missed-empty-state (#212) | empty list | pass | pass | pass | pass |
| Neighbour: invoice list total column | default | pass | pass | pass | pass |
```

Merge identical cells with `same` only when the reason is identical. Each fail gets an ID that the report expands.

## State recipes (agent-browser)

Set states inside the cell's batch, before the action, and reset them after.

| State | How to force it |
| ----- | --------------- |
| Error | `network route "**/api/invoices/*/credit-notes" --abort`, or `--body` with the API's error payload |
| Empty | `network route "**/api/invoices*" --body '{"data":[]}'` matching the real response shape |
| Offline | `set offline on`, then `set offline off` |
| Viewport | `set viewport 375 812` and `set viewport 1280 800` |
| Loading | Assert the loading indicator while a routed request is held by a slow fixture, or read it from the component's state |
| Long content | Seed a fixture or local record with long text, many items, and non-ASCII characters |
| Permission denied | Log in as the role; first prove the control exists for a role that should see it |
| Keyboard-only | 1280 only, with `press Tab`, `press Enter` or `press Space`, and `press Escape`. Pass when Tab reaches the control, Enter/Space activates it, Escape closes overlays, and focus stays visible |

Per flow, capture and read:

```
console --clear · errors --clear · network requests --clear
<before assertion> → <action> → <after assertion>
console · errors · network requests --type xhr,fetch --status 400-599 · screenshot <grid-dir>/<cell-id>.png
```

`diff screenshot --baseline <before.png>` shows regions that changed; a changed region outside the expected area is a finding.

## Report template

```markdown
# agentic-qa report — PR #87 @ a1b2c3d
Status: PARTIAL — 2 failed cells (findings), 0 gaps
Base-run baseline: yes (main @ 9f8e7d6)

## Findings
### F1 — Credit note error leaves the button spinning (1280 admin, API 500)
Repro: <the exact batch>
Expected: inline error "Could not apply credit note", button enabled
Actual: spinner never stops; console TypeError: Cannot read properties of undefined (reading 'message') at InvoiceTotal.vue:42
Evidence: specs/qa/87-a1b2c3d/AC1-error-1280-admin.png
Re-check: 1/3

## Not reachable
- viewer × apply credit note — apply action absent for viewer; shown present for admin in AC-1 success
```

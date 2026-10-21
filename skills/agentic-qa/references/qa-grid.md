# QA grid, reach trace, and state recipes

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

## Contents

- Reach trace
- Grid template
- AC map
- Default states
- Runtime and browser preparation
- agent-browser command notes
- State recipes (agent-browser)
- Report template
- Findings
- Not reachable

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

A proved absence of any screen chain is `no-ui-reach`, regardless of file type, only when no acceptance criterion requires user-visible behavior. A visible criterion with no wired entry point is `not-wired`/`partial`. When unsure, the change reaches.

## Grid template

```markdown
# QA grid — PR #87 @ a1b2c3d (BILLING-WEB)

Zero attribution: never add or leave co-author, AI, or tool attribution in this artifact.

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

Select states and roles from the changed behavior, criteria, AC map, escape classes and **Default states**. Record the coverage reason for each row; do not multiply unreachable states across every role. Merge identical cells with `same` only when the reason is identical. Each fail gets an ID that the report expands.

## AC map

Read the `/tdd-loop` AC map from the `AC_MAP:` file a caller names; otherwise from an `ac-map.md` or `/tdd-loop` summary `AC map` line the implementing session or PR names; otherwise from the `Edge coverage` section of the newest QA handoff for head. Cover rows marked `agentic-qa (<surface>)`; give each `deferred` row a cell when the app can show it, or record why it cannot. No map → build the grid from criteria and write `AC map: none` in the report.

## Default states

Each reachable surface gets a row for every state below, or a line under the grid: `<surface> <state>: not applicable — <reason a reviewer could disagree with>`.

| State | Applies when |
| ----- | ------------ |
| Empty | The surface lists, searches, or shows optional data |
| Error | The surface sends a request or submits a form; assert visible feedback, not only the absence of a crash |
| Loading | A request can be in flight while the user acts; include double submit |
| Long content | The surface shows names, labels, or user, seeded, or translated text: the longest real value from fixtures, enums, or locales, one unbroken word over 20 characters, and non-ASCII text |
| Alternative entry | A sibling entry point — another route, step control, shortcut, or role — reaches the same behavior: a stepper beside Next, edit beside create |

A fail in one of these states is checked in the same state on every other surface, width, role, locale and entry point of the grid in the same round, so one round reports all the fails it causes.

## Runtime and browser preparation

Read [Fixture ownership](qa-records.md#fixture-ownership) before testing. The builder or runtime repair owner prepares missing fixtures; the tester does not seed or edit them.

Verify the workspace/project binding against live checkout, command directory/user and served revision before using either URL. Send failures to the runtime repair owner; QA remains read-only. Keep BASE and HEAD data, trust configuration and login sessions separate. A locator or HTTP health response alone cannot prove the tested revision or authenticated readiness.

Use the browser tool and headed/headless mode required by current target policy and user preference, including workers. Where policy selects T3 first, make one bounded live capability/connection probe; on failure use its authorized fallback and record the exact reason. Tool exposure alone is not availability. A different project's policy may select a different tool. Missing required console/page-error/failed-request diagnostics remains a gap; choosing another tool never waives them.

## agent-browser command notes

The workspace browser rule gives the tool-neutral rules; these are the agent-browser specifics behind them.

- The per-command timeout is `AGENT_BROWSER_DEFAULT_TIMEOUT` (ms), read when the session starts; later calls inherit it.
- Wait on a condition — `wait "<selector>"`, `wait --text`, `wait --url`, or `wait --fn` — with the target policy’s condition deadline. Never `wait --timeout N`: without a condition it ignores N, idles about 30 s, then fails.
- `batch` takes quoted command arguments or a JSON array on stdin, never plain lines; pass secrets inside the JSON (for example with `jq -n --arg`), never on the command line.
- Resolve launch options once: headed/headless mode, trust for the binding's approved local CA, timeout and session name. Keep the same options on every invocation that requires them; changed launch options require an intentional close/reopen and invalidate the old page/session evidence. Trust the local CA through supported controls; certificate-error bypass needs target-policy authorization and is reported as such, not trusted TLS proof.
- Take the session name once from the runtime's session id when available; a `$$`-based name changes in every new shell.
- Verify session, page URL and served checkout after a restart or handoff. A command that opened another browser page cannot reuse the previous login or diagnostic baseline. Reproduce cookie/TLS problems as runtime blockers and send them to the repair owner before judging application behavior.

## State recipes (agent-browser)

Set states inside the cell's batch, before the action, and reset them after.

| State | How to force it |
| ----- | --------------- |
| Error | `network route "**/api/invoices/*/credit-notes" --abort`, or `--body` with the API's error payload |
| Empty | `network route "**/api/invoices*" --body '{"data":[]}'` matching the real response shape |
| Offline | `set offline on`, then `set offline off` |
| Viewport | `set viewport 375 812` and `set viewport 1280 800` |
| Loading | Assert the loading indicator while a routed request is held by a slow fixture, or read it from the component's state |
| Long content | Use an owner-prepared fixture with long text, many items, and non-ASCII characters; missing fixture returns to its owner |
| Permission denied | Log in as the role; first prove the control exists for a role that should see it |
| Keyboard-only | 1280 only, with `press Tab`, `press Enter` or `press Space`, and `press Escape`. Pass when Tab reaches the control, Enter/Space activates it, Escape closes overlays, and focus stays visible |

Per flow, capture and read:

```
console --clear · errors --clear · network requests --clear
<before assertion> → <action> → <after assertion>
console · errors · network requests --type xhr,fetch --status 400-599
<reuse desktop/phone before/after images; no per-cell screenshot>
```

`diff screenshot --baseline <before.png>` shows regions that changed; a changed region outside the expected area is a finding.

## Report template

```markdown
# agentic-qa report — PR #87 @ a1b2c3d

Zero attribution: never add or leave co-author, AI, or tool attribution in this artifact.
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

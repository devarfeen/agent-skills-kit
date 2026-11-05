# Evidence capture — clause-by-clause recipes

How to satisfy each verification-gate clause with concrete tool calls. Adapt
names to the runtime's browser tool when it isn't agent-browser; the evidence
bar never changes.

Zero attribution: never add or leave co-author, AI, or tool attribution in commits, PRs, issue comments, release notes, generated docs, settings, or code comments.

## Expected values (the source of truth)

- **Figma MCP:** read node metadata/variables for exact position, size,
  spacing, fills, typography, radius, and effects. Image exports are visual
  reference only — never measure pixels off an export when metadata exists.
- **Reference screens / reference implementation:** measure from the screens
  and mark every measured value `≈`. The gate then proves relative alignment
  and internal consistency (equal gaps, shared edges, same token) rather than
  absolute pixel values.

## Actual values (the running page)

- **State the env:** host/URL, container or dev-server serving it, browser +
  session (logged-in user), viewport/breakpoint.
- **Cross the pipeline:** after any template/CSS/class/component change, run
  the project's build/refresh step, then prove the change reached the served
  assets — grep the built CSS/JS for the new class/token, or curl the page and
  check the markup — before looking at the browser.
- **Element geometry:** with agent-browser, snapshot the page to get element
  refs, then evaluate JS on the element:
  `el.getBoundingClientRect()` for position/size, and
  `getComputedStyle(el)` for the specific properties in the defect row
  (margin/padding/gap/font-size/line-height/color/border-radius/box-shadow).
  Record the numbers in the row's Evidence cell — "looks right" is not a value.
- **Screenshots:** save zoomed/clipped element shots under the audit's shots
  folder and record the path; full-page shots are overview only.
- **State coverage:** drive each in-scope state (hover, focus, disabled,
  empty/error/loading, each breakpoint) before its row can pass — a default-
  state check proves nothing about the others.

## Capture efficiently

- Reuse one authenticated session across rows. Restart only that session when
  recovery requires it, and re-authenticate if its credentials expired.
- Batch each row into one flow — navigate → interact → eval assertion — not
  separate open/wait/snapshot/click/console calls.
- Snapshot once per page to harvest refs, then drive rows with stable
  `data-test`/CSS selectors; re-snapshot only after a re-render invalidates a
  ref (Livewire and similar).
- Wait on URL or DOM state, never toast timing or `networkidle`. Use bounded
  timeouts based on the project's measured startup and interaction times;
  record unexpected delays before retrying. Run one command at a time per session.

## If the browser wedges

Commands hang, or errors claim an existing connection: inspect the installed
tool's help for session-scoped recovery. Close and reopen only the audit's
session; never close all sessions or remove another browser's profile locks.
If session ownership cannot be established, stop recovery and report the blocker.
Re-verify that the recovered session renders the target page before resuming.
Two failed recoveries require stopping with the exact error and last observed state.

## Falsify before "verified"

Rule out, and say you ruled out: stale served assets (cache-bust or hash
check), wrong breakpoint (viewport stated), class present but overridden
(computed style, not class list), element hidden/zero-size/clipped
(rect + `visibility`/`overflow`). For fonts, wait for font loading and inspect
the actually rendered font with browser diagnostics. A computed `font-family`
list only names candidates; it does not prove which font rendered. If actual
font inspection is unavailable, leave font-dependent checks pending.

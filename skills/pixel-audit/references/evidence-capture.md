# Evidence capture — clause-by-clause recipes

How to satisfy each verification-gate clause with concrete tool calls. Adapt
names to the runtime's browser tool when it isn't agent-browser; the evidence
bar never changes.

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
- **Screenshots:** zoomed/clipped element screenshots when alignment matters;
  full-page shots are overview only. Save under the audit's shots folder and
  record the path.
- **State coverage:** drive each in-scope state (hover, focus, disabled,
  empty/error/loading, each breakpoint) before its row can pass — a default-
  state check proves nothing about the others.

## Capture efficiently

The evidence bar never drops; the call count does.

- One authenticated session for the whole audit; never restart the browser or
  re-auth between rows.
- Batch each row into one flow — navigate → interact → eval assertion — not
  separate open/wait/snapshot/click/console calls.
- Snapshot once per page to harvest refs, then drive rows with stable
  `data-test`/CSS selectors; re-snapshot only after a re-render invalidates a
  ref (Livewire and similar).
- Wait on URL or DOM state, never toast timing or `networkidle`. An ordinary
  route flow over ~5 seconds is a defect to diagnose, not a wait to lengthen.
- Short explicit timeouts (3–8 s) on every command; one command at a time per
  session — an orphaned wait blocks it. If a reused session fails a ~2 s health
  check, close and reopen that session only, never all sessions.

## Falsify before "verified"

Rule out, and say you ruled out: stale served assets (cache-bust or hash
check), wrong breakpoint (viewport stated), class present but overridden
(computed style, not class list), element hidden/zero-size/clipped
(rect + `visibility`/`overflow`), font not loaded (computed `font-family`
resolution).

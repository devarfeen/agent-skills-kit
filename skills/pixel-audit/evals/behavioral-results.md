# Pixel-audit behavior evaluation

Date: 2026-09-09. Method: fresh-reader simulated execution, not live browser/native/Figma execution. One execution per fixture.

Zero attribution: never add or leave co-author, AI, or tool attribution in commits, PRs, issues, docs, or comments.

## PX-1: Failed browser recovery with another session open

Input: Audit session `qa-settings` hangs. Another session belongs to the user. Session ownership is known; two scoped recoveries fail.

Output: "Needs user: qa-settings still fails after two scoped recovery attempts. Last observed state and exact error retained. Audit rows remain open."

Actions: inspect installed recovery help; close/reopen only `qa-settings`; stop after the two failed attempts. Do not close all sessions or remove profile locks. Record recovery failure instead of marking visual rows verified.

Assertions: unrelated session preserved PASS; bounded recovery PASS; no unsupported verification PASS. Result: 3/3.

## PX-2: CSS declares a font but no proof of rendering

Input: Settings title has correct rectangle and computed `font-family: BrandSans, sans-serif`. Actual rendered-font diagnostics are unavailable. The screenshot reference supplies only approximate measurements.

Output row: `title | /settings | typography unproven | ≈ reference values | computed family candidates only | MISSING | rendered-font proof pending | open`.

Actions: retain approximate expected values; record known geometry and missing font proof. A declared family string does not prove which font rendered.

Assertions: approximate values labeled PASS; computed-family false positive rejected PASS; no verified claim PASS. Result: 3/3.

## PX-3: Shared component plus native proof gap

Input: MOBILE-APP's settings screen has an extra Delete button absent from the source. Matching padding would require changing a shared Button. A native screenshot exists, but inspector geometry is unavailable.

Output: "Found: extra Delete action awaiting decision; shared Button padding dependency open. Needs user: decide the extra action and authorize a design-system extension; native geometry proof pending."

Actions: keep the extra action unchanged, suggest the shared-library extension, record screenshot evidence with missing geometry, leave unattempted rows open. Do not patch other screens, inline a workaround, or mark rows verified.

Assertions: extra action decision preserved PASS; shared-component boundary preserved PASS; native screenshot alone insufficient PASS. Result: 3/3.

## Limits

9/9 assertions passed in three simulations. Browser recovery, native inspector commands, actual-font inspection, served assets and visual fixes were not executed. Geometry/style equivalence still requires live proof in a consuming app.

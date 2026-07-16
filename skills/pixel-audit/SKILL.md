---
name: pixel-audit
disable-model-invocation: true
description: Strict per-page visual-conformance audit at the verify phase — ONE page/route against a source of truth (Figma MCP nodes, or reference screens when no Figma exists). Captures a full-size pixel inventory, writes a MISSING-vs-EXTRA defect list, fixes node-by-node reusing the project's UI library (never inlining), and refuses to say "verified" until a hard element-level gate passes — served assets confirmed, getBoundingClientRect/computed-style proof, every in-scope state checked. Use when a page must match its design pixel-for-pixel during feature work. Stays inside the given SCOPE; never auto-chains; distinct from /design-system's startup preview check.
---

# Pixel audit

Audit **one page** against its source of truth, fix the mismatches, and prove each fix at the element level before claiming "verified". `/design-system` checks the whole component library once at project start via its preview page; this skill checks one product page during feature work — reference the project's library, never rebuild components here.

## Inputs

Infer from the request; interview only for what's missing:

- **TARGET PROJECT-CODE** — full Project Matrix code; sets the stack idiom and UI library.
- **SCOPE** — the single page/route plus the states to audit (list/detail, modals, forms, empty/error/loading, responsive breakpoints). **Scope is a hard boundary — never edit other pages, routes, or steps.**
- **SOURCE OF TRUTH** — Figma node(s) via the Figma MCP companion, or reference screens / a reference implementation when no Figma exists. Name which is in use in the artifact. If neither is available, stop and ask — never audit against memory.
- **Login / env** — local credentials only, if the page needs auth.

## Load first

- The target's binding context: `CONTEXT.md` and `specs/adr/`.
- The project's `*-ui-coding` skill if it exists — it owns the component catalog, tokens, and gotchas. **Reuse its components; never inline.** If absent, discover the tokens, library, and preview from `/design-system`'s docs or the project code.

## Process

### 1. Map the page

Find the routes, view/template/component files, partials, in-scope states, data, and the DS components the page should use. Open the component preview (e.g. `/ui/preview/all`) if one exists.

### 2. Trace the asset pipeline

Identify the build/asset pipeline, cache, and container/service — how a class/style/component change actually reaches the page.

### 3. Capture the pixel inventory

Write the source of truth down **before editing**. Per node/region (frame, panel, card, row, filter, tab, modal, field, button, and every empty/error/loading/responsive variant), capture it **full-size including below the fold** — never rely on a single whole-frame screenshot. Record exact `x`/`y`, size, spacing, padding, gap, font, colour, border, radius, fill, icon size, alignment, opacity, shadow, and variant. Expected values: Figma MCP node metadata/variables (exact), or measured from reference screens and marked approximate — the gate then proves relative alignment and consistency, not absolute pixels. Capture calls per source: [`references/evidence-capture.md`](references/evidence-capture.md).

### 4. Audit expected vs actual

Per node/state, classify each mismatch:

- **MISSING** — a source item/state absent or wrong in the app.
- **EXTRA** — an app item/state not in the source. Extra UI is a defect — report it for a decision (rules under Fixing).

## The defect list artifact

Resolve `<artifacts-root>`: the `*.code-workspace` directory if one exists, else the per-context root (`CONTEXT-MAP.md` at repo root), else the repo root. The filename is keyed by PROJECT-CODE so two projects' same-named pages never collide:

```text
<artifacts-root>/specs/pixel-audit/<TARGET-PROJECT-CODE>-<page-slug>-defects.md
```

Inventory and screenshots sit beside it: `<TARGET-PROJECT-CODE>-<page-slug>-inventory.md` and `shots/<TARGET-PROJECT-CODE>-<page-slug>/`.

One row per defect:

```markdown
# Pixel Audit — <page-slug> (<TARGET-PROJECT-CODE>)

Source of truth: <Figma node(s) URL | reference screens/impl — name it>
Scope: <route + states audited>

| # | Node | URL / State | File / Component | Mismatch | Expected | Actual | Kind | Evidence | Status |
| - | ---- | ----------- | ---------------- | -------- | -------- | ------ | ---- | -------- | ------ |
| 1 | Filter bar, Search field | /assets · list | components/search-field | height off | 34px | 40px | MISSING | rect=…, computed=… | open |
| 2 | Row actions, extra "Delete" | /assets · list | pages/assets/index | not in source | — | delete icon present | EXTRA | ref=…, screenshot | open |
```

**Kind** is `MISSING` or `EXTRA`. **Evidence** is element-level per the verification gate — not "looks off". **Status** runs `open` → `fixed` → `verified`, or `reopened` when the gate fails.

## Fixing

- **One node/page/state at a time.** Do not batch unrelated fixes.
- **A MISSING defect that needs behaviour, data, or interface work is a slice, not a style fix.** Record the row, route it to `/to-tickets`, and do not build it here (the boundary `/polish-batch` draws).
- **Reuse the project UI library's components.** No one-off UI unless justified and documented (per the `*-ui-coding` reuse-vs-new rule).
- **If a shared component must change, change it in the library + its preview + the project `*-ui-coding` skill (via `/design-system` extend) — never patch it page-local.** Confirm with the user first — other pages consume it, and this page's frame may be the outlier, not the component. If the user is away, leave the row `open` under Needs user and continue; never rewrite a shared component unattended.
- **Stay strictly inside SCOPE.** Cosmetic nits on other pages or flows are captured with `/polish-batch`, never fixed here.
- **Report, don't decide, on EXTRA:** any icon/button/field/action present in the app but absent from the source is surfaced for a user decision, not silently kept, removed, or restyled.

## Verification gate

"Verified/done/fixed" is a claim you must earn per fix.

- **State the env:** host, URL, container/service, browser/session.
- **Cross the build pipeline:** rebuild/refresh after every template/CSS/class/component change, and **confirm the changed classes/styles/components actually exist in the SERVED assets** (not just the source files).
- **Prove each fix with element-level evidence:** selector/ref, `getBoundingClientRect()`, the relevant computed styles, the DOM, and a zoomed/clipped element screenshot when alignment matters. Full-page screenshots are overview only. Capture with the agent-browser companion or the runtime's equivalent browser automation. If no browser automation is available, say so, list the pending checks as manual steps for the user, and do not mark any row `verified` on assumption.
- **These count as failure:** hidden, zero-size, collapsed, clipped, misaligned, wrong-size, or ignored-class elements.
- **Falsify before declaring verified:** actively look for the ways the fix could be wrong (wrong breakpoint, stale asset, class not applied, element off-screen) and rule them out.
- **Do not say "verified / done / fixed" unless ALL hold:** env stated · build pipeline crossed · served assets contain the change · browser has element proof · source captured full-size · expected-vs-actual compared · every in-scope state checked.

A row is `verified` only when its fix clears every clause above; otherwise it stays `reopened`.

## Rules

- **Suggest, never auto-chain.** After the audit, suggest `/code-review` then `/commit-push-close` / `/commit-push-pr`, and stop.
- Decisions are **artifacts** — inventory and defect list live on disk, not in chat.
- Name the full PROJECT-CODE from the Project Matrix everywhere; never mix one project's conventions, tokens, or components into another.
- **Local-only.** Local creds, local browser, no cloud agents; the main agent owns synthesis and the gate.
- Sub-agents: local lanes only when the user allows them — never cloud agents; announce the lane count at dispatch and report each lane as it completes. Lanes map only.
- Emit `Stage / Found / Next / Needs user` at each phase transition — one line per field. Phases: mapped → inventory captured → audited → fixing → verified.

## Output

After in-scope fixes:

```markdown
Stage: pixel-audit — audited <page-slug> (<TARGET-PROJECT-CODE>) vs <source of truth>; wrote specs/pixel-audit/<TARGET-PROJECT-CODE>-<page-slug>-defects.md.
Found: <N> defects (<M> MISSING, <E> EXTRA); <V> verified, <R> reopened; <U> EXTRA items awaiting your decision.
Next: /code-review the diff, then /commit-push-*. Reopened rows and EXTRA decisions stay for the next pass.
Needs user: <EXTRA items to decide (keep/remove/restyle), or blocked states, or "none">.

Suggested next skills (optional):
- /code-review: eyeball the in-scope diff before shipping.
- /commit-push-pr (or /commit-push-close): ship the verified fixes.
```

Do not proceed past the suggestion.

## Completion criteria

- [ ] Defect list exists at `<artifacts-root>/specs/pixel-audit/<TARGET-PROJECT-CODE>-<page-slug>-defects.md`, names its source of truth and scope, one row per defect
- [ ] `<TARGET-PROJECT-CODE>-<page-slug>-inventory.md` and `shots/<TARGET-PROJECT-CODE>-<page-slug>/` exist beside it
- [ ] Every row's Status is `verified`, `open`, or `reopened` — none left `fixed` — and each `verified` row's Evidence cell holds element-level proof
- [ ] `Stage / Found / Next / Needs user` emitted and the reply ends at the suggestion footer

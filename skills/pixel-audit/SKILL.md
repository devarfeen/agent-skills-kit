---
name: pixel-audit
disable-model-invocation: true
description: "Audit ONE page or route for visual conformance against Figma or reference screens, fix gaps with the UI library, and verify at element level. Not feature porting; never auto-chains."
metadata:
  version: "1.0.0"
---

# Pixel audit

Audit **one page** against its source of truth, fix the mismatches, and prove each fix at the element level before claiming "verified". `/design-system` checks the whole library once at project start via its preview; this skill checks one product page during feature work — reference the project's library, never rebuild components here.

## Inputs

Infer from the request; interview only for what's missing:

- **TARGET PROJECT-CODE** — full Project Matrix code; sets the stack idiom and UI library.
- **SCOPE** — the single page/route plus the states to audit (list/detail, modals, forms, empty/error/loading, responsive breakpoints, theme variants such as light/dark when the source has them). **Scope is a hard boundary — never edit other pages, routes, or steps.**
- **SOURCE OF TRUTH** — Figma node(s) via the Figma MCP companion, or reference screens / a reference implementation when no Figma exists. Name which is in use in the artifact. If neither is available, stop and ask — never audit against memory.
- **Login / env** — local credentials only, if the page needs auth.

## Load first

- The target's binding context: `GLOSSARY.md` (legacy `CONTEXT.md`) and ADRs located by page/topic or linked decision; read only relevant ADRs.
- The project UI skill named in its design-system doc or `AGENTS.md`; fall back to detecting a `*-ui-coding` skill when unregistered. **Reuse its components; never inline.** If absent, discover tokens, library, and preview from the design-system docs or project code.

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

Resolve `<artifacts-root>`: the `*.code-workspace` directory if one exists, else the per-context root (`GLOSSARY-MAP.md` at repo root; legacy `CONTEXT-MAP.md`), else the repo root. The filename is keyed by PROJECT-CODE so two projects' same-named pages never collide:

```text
<artifacts-root>/specs/pixel-audit/<TARGET-PROJECT-CODE>-<page-slug>-defects.md
```

Inventory and screenshots sit beside it: `<TARGET-PROJECT-CODE>-<page-slug>-inventory.md` and `shots/<TARGET-PROJECT-CODE>-<page-slug>/`. Include the zero-attribution rule in both Markdown artifacts.

One row per defect:

```markdown
# Pixel Audit — <page-slug> (<TARGET-PROJECT-CODE>)

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Source of truth: <Figma node(s) URL | reference screens/impl — name it>
Scope: <route + states audited>

| # | Node | URL / State | File / Component | Mismatch | Expected | Actual | Kind | Evidence | Status |
| - | ---- | ----------- | ---------------- | -------- | -------- | ------ | ---- | -------- | ------ |
| 1 | Filter bar, Search field | /assets · list | components/search-field | height off | 34px | 40px | MISSING | rect=…, computed=… | open |
| 2 | Row actions, extra "Delete" | /assets · list | pages/assets/index | not in source | — | delete icon present | EXTRA | ref=…, screenshot | open |
```

**Evidence** is element-level per the verification gate. **Status** runs `open` → `awaiting verification` → `verified`, or `reopened` when the gate fails. On reruns, treat legacy `fixed` rows as awaiting verification; they need the full gate.

## Fixing

- **One node/page/state at a time.** Do not batch unrelated fixes.
- **A MISSING defect that needs behaviour, data, or interface work is a slice, not a style fix.** Record the row, route it to `/to-tickets`, and do not build it here (the boundary `/polish-batch` draws).
- **Reuse the project UI library's components.** No one-off UI unless justified and documented (per the registered project UI skill's reuse-vs-new rule).
- **If a shared component must change, suggest `/design-system` extend for the library, preview, and registered project UI skill; never patch it page-local or auto-chain.** Confirm with the user first. Other pages consume it, and this page's frame may be the outlier. Until separately authorized, leave the row `open` under Needs user and continue; never rewrite a shared component unattended.
- **Stay strictly inside SCOPE.** Cosmetic nits on other pages or flows are captured with `/polish-batch`, never fixed here.
- **Report, don't decide, on EXTRA:** any icon/button/field/action present in the app but absent from the source is surfaced for a user decision, not silently kept, removed, or restyled.

## Verification gate

"Verified/done/fixed" is a claim you must earn per fix.

- **State the env:** host/URL and browser/session, or local app build and simulator/device.
- **Cross the build pipeline:** rebuild/refresh after each change and confirm the changed classes/styles/components exist in the assets the page or app actually loaded, not just source files.
- **Prove each fix with element-level evidence:** selector/ref, `getBoundingClientRect()`, relevant computed styles, DOM, and a clipped screenshot when alignment matters. Native apps require equivalent inspector geometry, resolved styles, rendered tree, and screenshots from the local simulator. Full-page shots are overview only. If the required automation is unavailable, list pending manual checks and do not mark any row `verified` on assumption.
- **These count as failure:** hidden, zero-size, collapsed, clipped, misaligned, wrong-size, or ignored-class elements, and a new console error versus the step-3 capture.
- **Falsify before declaring verified:** actively look for the ways the fix could be wrong (wrong breakpoint, stale asset, class not applied, element off-screen) and rule them out.
- **Do not say "verified / done / fixed" unless ALL hold:** env stated · build pipeline crossed · loaded assets contain the change · element proof captured · source captured full-size · expected-vs-actual compared · every in-scope state checked. Unattempted rows stay `open`; changed rows failing the gate become `reopened`.
- **Final sweep:** before the final report, re-run element proof for every `verified` row once on the final build. A row that drifted becomes `reopened`.

## Rules

- Zero attribution: never add or leave co-author, AI, or tool attribution in commits, PRs, issue comments, release notes, generated docs, settings, or code comments.
- **Suggest, never auto-chain.** After the audit, suggest `/code-review` then `/commit-push-close` / `/commit-push-pr`, and stop.
- Decisions are **artifacts** — inventory and defect list live on disk, not in chat.
- Name the full PROJECT-CODE from the Project Matrix everywhere; never mix one project's conventions, tokens, or components into another.
- **Local-only.** Local creds, local browser, no cloud agents.
- Sub-agents: dispatch local lanes automatically for independent work — never cloud agents; announce the lane count at dispatch and report each lane as it completes. Lanes run only step 1 (Map the page); fixing, synthesis, and the gate stay with the main agent.
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
- [ ] Every row's Status is `verified`, `open`, or `reopened` — none awaiting verification — and each `verified` row's Evidence cell holds element-level proof
- [ ] The reply ends at the `Suggested next skills (optional)` footer — nothing after it

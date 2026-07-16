---
name: pixel-audit
description: Strict per-page visual-conformance audit at the verify phase — ONE page/route against a source of truth (Figma MCP nodes, or reference screens when no Figma exists). Captures a full-size pixel inventory, writes a MISSING-vs-EXTRA defect list, fixes node-by-node reusing the project's UI library (never inlining), and refuses to say "verified" until a hard element-level gate passes — served assets confirmed, getBoundingClientRect/computed-style proof, every in-scope state checked. Use when a page must match its design pixel-for-pixel during feature work. Stays inside the given SCOPE; never auto-chains; distinct from /design-system's startup preview check.
---

# Pixel Audit

## Purpose

Audit **one page** for pixel-level conformance against a source of truth, fix the mismatches by reusing the project's UI library, and prove each fix at the element level before ever claiming "verified." This is per-page, feature-time conformance — narrow, evidence-driven, and strict.

It is **not** `/design-system`'s job. `/design-system` verifies the whole component library once, at project start, via its preview page. `pixel-audit` verifies a **single product page** against its design during feature work. Reference `/design-system` and the project's `*-ui-coding` skill for the components; do not rebuild them here.

It audits, fixes in scope, proves it, then suggests the next step and stops.

## Inputs

Infer first from the request; interview the user only for what's missing:

- **TARGET PROJECT-CODE** — full Project Matrix code. Determines stack idiom and which UI library to reuse.
- **SCOPE** — the single page/route plus the states to audit (list/detail, modals, forms, empty/error/loading, responsive breakpoints). **Scope is a hard boundary — never edit other pages, routes, or steps.**
- **SOURCE OF TRUTH** — pluggable, one of:
  - **Figma** node(s) via the Figma MCP companion, OR
  - **reference screens / a reference implementation** (e.g. a legacy repo) when no Figma exists.
  - **State which one is in use** in the audit and the artifact. If neither is available, stop and ask — never audit against memory.
- **Login / env** — local credentials only, if the page needs auth.

## Load first

Per the kit's retrieval order (`CONTEXT.md` + `specs/adr/` are binding), before touching anything:

- Read the project's **binding context**: `CONTEXT.md` and `specs/adr/` for the target.
- Read the project's **`*-ui-coding` skill** if it exists — that skill owns the component catalog, tokens, and gotchas. **Reuse its components; never inline.** If it's absent, fall back to design-system discovery (find the tokens, library, and preview from `/design-system`'s docs / the project code).

## Process

1. **Map the page.** Find the routes, view/template/component files, partials, the states in scope, the data it renders, and the reusable DS components it should use. Open the project's component preview (e.g. `/ui/preview/all`) if it has one, to know what already exists.
2. **State how source reaches the browser.** Identify the build/asset pipeline, cache, container/service, and served assets — how a class/style/component change actually gets onto the page. You will cross this pipeline on every fix.
3. **Capture the source of truth as a written PIXEL INVENTORY — before editing.** Per node/region (frame, panel, card, row, filter, tab, modal, field, button, and every empty/error/loading/responsive variant), capture it **full-size including below the fold** — never rely on a single whole-frame screenshot. Record exact `x`/`y`, size, spacing, padding, gap, font, colour, border, radius, fill, icon size, alignment, opacity, shadow, and variant. Where Expected values come from: with Figma MCP, read them from node metadata/variables (exact); with reference screens, measure from the screens and mark them approximate — the gate then proves relative alignment and consistency rather than absolute pixels. Concrete capture calls per source live in [`references/evidence-capture.md`](references/evidence-capture.md).
4. **Audit expected (source) vs actual (browser).** For each node/state, classify each mismatch:
   - **MISSING** — a source item/state is absent or wrong in the app.
   - **EXTRA** — an app item/state that is not in the source.
   - **Extra UI is a defect** — report it for a decision (handling rules under Fixing).

## The defect list artifact

Write the defect list to the configured docs location. Resolve `<artifacts-root>` the same way the other kit skills do: (1) the directory containing a `*.code-workspace` file if one exists, (2) the per-context root in a multi-context repo (`CONTEXT-MAP.md` at root), (3) the single repo root. The filename is keyed by PROJECT-CODE so two projects' same-named pages never collide at a shared workspace root:

```text
<artifacts-root>/specs/pixel-audit/<TARGET-PROJECT-CODE>-<page-slug>-defects.md
```

The pixel inventory and element screenshots sit beside it, keyed the same way:
`<TARGET-PROJECT-CODE>-<page-slug>-inventory.md` and
`shots/<TARGET-PROJECT-CODE>-<page-slug>/` (the audit's shots folder that
Evidence cells record paths into).

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

- **Kind** is `MISSING` or `EXTRA`. **Evidence** is element-level per the Verification gate — not "looks off".
- **Status** lifecycle: `open` → `fixed` → `verified` (or `reopened` if the gate fails). A row reaches `verified` only after the verification gate passes for it.

## Fixing

- **One node/page/state at a time.** Do not batch unrelated fixes.
- **A MISSING defect that needs behaviour, data, or interface work is a slice, not a style fix.** A wholly absent error/empty/loading state or a missing action usually needs logic — record the row, route it to `/to-tickets`, and do not build it here (the same boundary `/polish-batch` draws).
- **Reuse the project UI library's components.** No one-off UI unless justified and documented (per the `*-ui-coding` reuse-vs-new rule).
- **If a shared component must change, change it in the library + its preview + the project `*-ui-coding` skill (via `/design-system` extend) — never patch it page-local — then consume it from the page.** Because other pages consume that component, confirm with the user before changing it on the evidence of this one page's frame — the frame may be the outlier, not the component. If the user is away, leave the row `open` under Needs user and continue with the other defects; never rewrite a shared component unattended.
- **Touch nothing unrelated.** Stay strictly inside SCOPE. Cosmetic nits spotted on other pages or flows are captured with `/polish-batch`, never fixed here.
- **Report, don't decide, on EXTRA:** any icon/button/field/action present in the app but absent from the source is surfaced for a user decision, not silently kept, removed, or restyled.

## Verification gate

"Verified/done/fixed" is a claim you must earn per fix.

- **State the env:** host, URL, container/service, browser/session.
- **Cross the build pipeline:** rebuild/refresh after every template/CSS/class/component change, and **confirm the changed classes/styles/components actually exist in the SERVED assets** (not just the source files).
- **Prove each fix with element-level evidence:** selector/ref, `getBoundingClientRect()`, the relevant computed styles, the DOM, and a zoomed/clipped element screenshot when alignment matters. Full-page screenshots are overview only. Capture this with the agent-browser companion (or the runtime's equivalent browser automation) — the clause-by-clause capture recipes are in [`references/evidence-capture.md`](references/evidence-capture.md). If no browser automation is available, say so, list the pending checks as manual steps for the user, and do not mark any row `verified` on assumption.
- **These count as failure:** hidden, zero-size, collapsed, clipped, misaligned, wrong-size, or ignored-class elements.
- **Try to falsify before declaring verified.** Actively look for the ways the fix could be wrong (wrong breakpoint, stale asset, class not applied, element off-screen) and rule them out.
- **Do not say "verified / done / fixed" unless ALL hold:** env stated · build pipeline crossed · served assets contain the change · browser has element proof · source captured full-size · expected-vs-actual compared · every in-scope state checked.

A row is `verified` only when its fix clears every clause above; otherwise it stays `reopened`.

## Rules (non-negotiables)

Scope, reuse-never-inline, and the design-system boundary are stated where they bind (Inputs, Load first, Fixing, Purpose). Beyond those:

- **Suggest, never auto-chain.** After the audit, suggest `/code-review` then `/commit-push-close` / `/commit-push-pr`, and stop. Never start unrelated work.
- **Decisions are artifacts.** The pixel inventory and defect list live on disk, not in chat.
- **Name the full PROJECT-CODE** from the Project Matrix everywhere. Never carry one project's conventions into another; adapt to the target stack.
- **Local-only.** Local creds, local browser; read-only sub-agents for mapping only when the user has allowed them; main agent owns synthesis and the gate. No cloud agents. Announce the lane count at dispatch and report each lane as it completes.
- **Emit `Stage / Found / Next / Needs user`** at each phase change (mapped → inventory captured → audited → fixing → verified).

## Output

After the audit and in-scope fixes:

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

## Checklist

Before claiming the page audited:
- [ ] TARGET PROJECT-CODE known; source of truth named (Figma nodes vs reference screens/impl); SCOPE fixed to one page + its states
- [ ] Project binding context + `*-ui-coding` skill loaded (or DS discovery fallback); components reused, never inlined
- [ ] Page mapped (routes, files, partials, states, data, DS components); component preview opened if present
- [ ] Asset/build pipeline identified (how a change reaches the served page)
- [ ] Pixel inventory captured full-size incl. below-fold, per node/region/state — not whole-frame only — and written to `<TARGET-PROJECT-CODE>-<page-slug>-inventory.md`
- [ ] Expected-vs-actual audited; each mismatch classified MISSING/EXTRA; EXTRA surfaced for decision, never silently changed
- [ ] Defect list written to `<artifacts-root>/specs/pixel-audit/<TARGET-PROJECT-CODE>-<page-slug>-defects.md`, one row per defect with element-level evidence
- [ ] Behaviour/data/interface-sized MISSING defects were routed to /to-tickets, not built here; out-of-scope nits went to /polish-batch
- [ ] Fixes done one node/state at a time, in scope; shared-component changes went through library + preview + `*-ui-coding`, not page-local
- [ ] Verification gate cleared per fix: env stated · pipeline crossed · served assets contain change · element proof · source full-size · expected-vs-actual · every in-scope state — falsified first
- [ ] No "verified" claimed without the full gate; reopened rows kept
- [ ] Suggested `/code-review` → `/commit-push-*` and stopped — no auto-chain, nothing out of scope touched
- [ ] `Stage / Found / Next / Needs user` emitted

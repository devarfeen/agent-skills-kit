---
name: port-feature
description: Use when the user wants to port, migrate, rebuild, or recreate a feature that already exists in a REFERENCE implementation into a TARGET stack (e.g. bring a legacy screen into the new app). Sits at the discover → plan entry — reads the target's binding context, traces the reference's real behaviour/workflow/permissions/states the way /feature-discovery does, surveys what the target already has, and writes ONE gap map artifact, then suggests /grill-with-docs and stops. The reference is truth for behaviour; the target's design system is truth for UI. Never implements, never auto-chains; interviews for any missing input.
---

# Port Feature

## Purpose

Port a feature that already works in a **REFERENCE** implementation into a **TARGET** stack. The reference (often a legacy repo) is where the real behaviour lives; the target is where it needs to land, in the target's own idiom. The confidence to do this safely — what the feature actually does, what the target already has, what's missing, what to reuse — usually lives only in someone's head. This skill pulls it onto disk as **one gap map**, then hands off to planning.

It sits at the **discover → plan** entry of the gradient. It is a single pass, not a loop and not a pipeline: read context → discover the reference → survey the target → write the gap map → suggest `/grill-with-docs` → **stop**.

## Inputs

Infer first from the request and cheap repo evidence (Project Matrix, cwd, `CONTEXT.md`, ADR names). Interview the user — the way `/feature-prompt` does — only for what's genuinely missing:

- **Feature to port** — the behaviour/workflow being brought over.
- **REFERENCE PROJECT-CODE** — the source of behaviour truth (e.g. a legacy repo), as a full Project Matrix code.
- **TARGET PROJECT-CODE** — where it lands, as a full Project Matrix code.

Do not start discovery until all three are known; if the user is away and one cannot be inferred, stop with a Needs-user note naming exactly which is missing — never guess. (PROJECT-CODE discipline per Rules.)

## Source-of-truth framing

Carry this framing through every section of the gap map:

- **The REFERENCE is truth for behaviour** — workflow, navigation (menu placement, entry points, routes), permissions, data effects, and states. When the target's current behaviour disagrees with the reference, the reference wins (unless the user has explicitly decided to change the behaviour, which is a `/grill-with-docs` decision, not one this skill makes).
- **The TARGET's design system is truth for UI.** When reference UI conflicts with the target design system, choose the design system and **record the deviation** (reference did X; target DS does Y; chose DS) in the UI/design gaps section.
- **Never hardcode stack rules.** Do not assume Livewire version, "no plain Blade", React Native component conventions, or any framework specifics. Read the target's rules from its **binding context** — its `CONTEXT.md`, `docs/adr/`, `AGENTS.md` — and its **UI-coding skill** (whatever the target uses, e.g. an `impeccable`/`frontend-design`/project-specific UI skill). This skill must work for any repo in the matrix; a React Native target has different rules than a Livewire one. If a rule the port depends on (stack version, DS convention, component discipline, ADR location) is **not** recorded in the target's binding context, do not invent it — surface it under Open questions / Needs-user rather than guessing.

## Rules (non-negotiables)

- **Suggest, never auto-chain.** End by suggesting `/grill-with-docs` on the gap map, then stop. Do not run planning, do not open issues, do not implement.
- **Never implement here.** No product code, config, or migration edits. The only write is the gap map file.
- **Always name full PROJECT-CODEs** from the Project Matrix — reference and target — everywhere in the artifact. Never mix one project's conventions into another; each side is described in its own idiom.
- **Narrow retrieval only.** Trace the reference and survey the target with targeted, evidence-backed search (`rg`/`git grep` for the exact route/path/symbol/state), `/feature-discovery`-style. **Never** bulk-read a repo or its `docs/` to "find everything".
- **Retrieval order.** `CONTEXT.md` + `docs/adr/` are binding (read before deciding) > the current request, reference/target code, and tests > native CLI memory.
- **Decisions are artifacts.** The output is the durable gap map file, not a chat summary. Chat only reports what was written and the phase update.
- **Don't fabricate an issue before coding.** This skill produces a discovery/plan artifact, not a tracker issue. Issues come later, from `/to-issues` after `/grill-with-docs`.
- **Local-only.** Local read-only sub-agents only, within the Bounded sub-agents bounds (Process step 4) — never cloud agents.

## Process

1. **Read the TARGET's binding context first** — `CONTEXT.md` and `docs/adr/` in the target's `<artifacts-root>`, per the kit's retrieval order, plus the target's `AGENTS.md` and UI-coding skill for stack/DS rules. This sets the idiom every later section must respect.
2. **Discover the REFERENCE** (not the target), `/feature-discovery`-style: trace the real behaviour, workflow, navigation, permissions, states, and data effects, evidence-backed and narrow. Capture concrete refs (`file:symbol`, route, migration, test) for each claim.
3. **Survey the TARGET's current state** for the same feature: what already exists, what's partial or wrong versus the reference, and which design-system components and existing patterns are reusable. If the feature has UI, open the target's component preview (e.g. `/ui/preview/all`) to inventory available DS components before deciding what to build.
4. **Bounded sub-agents (optional):** only if the user has allowed sub-agents, dispatch read-only Explorer lanes for non-overlapping discovery (e.g. one on the reference, one on the target survey). The main agent merges and owns synthesis, uncertainty calls, and the final artifact. No two lanes discover the same thing.

## The gap map artifact

Write **one** gap map per ported feature, alongside the feature's other docs — resolve the configured docs location, do **not** hardcode a path:

```text
<artifacts-root>/docs/port/<feature-slug>-gapmap.md
```

Resolve `<artifacts-root>` the same way the other kit skills do: (1) the directory containing a `*.code-workspace` file if one exists, (2) the per-context root in a multi-context repo (`CONTEXT-MAP.md` at root), (3) the single repo root. `<feature-slug>` is kebab-case from the feature name, max ~4 words, ASCII. The gap map is an on-demand slug file — it does **not** consume the `NNNN` prompt/ADR sequence; the ADR that `/grill-with-docs` produces next takes the next number in the configured `docs/adr/`.

Sections, in order:

```markdown
# Port Gap Map — <feature> (<REFERENCE-CODE> → <TARGET-CODE>)

## 1. Reference behaviour / workflow
- <behaviour/workflow/navigation/permission/state/data-effect> — evidence: `file:symbol`, route, migration, test.
- Navigation: where the feature lives in the reference (menu placement, entry points) and any moves the port implies.

## 2. Target current state
- <what exists today for this feature in the target> — evidence refs.

## 3. Missing / wrong in target
- <gap or divergence from the reference> — what's absent, partial, or behaving differently.

## 4. Reusable target code & DS components
- <existing target seam/service/component to extend> — path + why it fits.
- <design-system component from the target preview> — where it applies.

## 5. Tests needed
- Success paths, validation, permission checks, empty/error/success states, DB/data effects, and regressions to guard.

## 6. UI / design gaps vs reference (and forced DS deviations)
- <reference UI element> → <target DS equivalent>.
- Forced deviation: reference did X; target DS does Y; chose DS because <rule/source>.

## 7. Risks
- <behaviour, data, permission, or migration risk> and where it bites.

## 8. First slice
- One thin, independently testable vertical slice to start with (end-to-end, demoable on its own).

## 9. Open questions
- <evidence-derived unresolved question for /grill-with-docs>. List them; do not block on them.
```

Section rules (filled example bullets at the expected granularity live in [`references/gapmap-example.md`](references/gapmap-example.md)):

- Every claim in **1–4** carries a concrete evidence ref; unproven claims are marked as inference, not fact.
- **5 (Tests needed)** is the seed for later acceptance criteria — cover every category the template lists.
- **6** records every forced DS deviation explicitly.
- **8 (First slice)** is one thin vertical slice that cuts through all layers and is testable on its own — not a layer or a big-bang.
- **9 (Open questions)** comes from the evidence and is a list for `/grill-with-docs` to attack; it does not block writing the gap map.

## Output

After the gap map is written:

- **Suggest the next step and stop:** recommend running `/grill-with-docs` on the gap map.
- **Emit the final phase update:**

```markdown
Stage: port-feature — wrote docs/port/<feature-slug>-gapmap.md (<REFERENCE-CODE> → <TARGET-CODE>).
Found: <N> reference behaviours traced; target is <absent/partial/diverging>; <M> reusable target/DS pieces; <K> forced DS deviations; <R> risks.
Next: run /grill-with-docs on the gap map to challenge it and produce the ADR (next number in docs/adr/).
Needs user: <open questions to steer, or ambiguous reference/target mapping, or "none">.

Suggested next skills (optional):
- /grill-with-docs: challenge the gap map and record the porting decisions as an ADR.
- /prototype: if a UI/interaction open question is high-fidelity ("needs to feel/see it") before planning.
```

Do not proceed past the suggestion.

## Checklist

Before finishing:
- [ ] Feature, full REFERENCE PROJECT-CODE, and full TARGET PROJECT-CODE all known (interviewed for any missing)
- [ ] Target binding context (`CONTEXT.md`, `docs/adr/`, `AGENTS.md`, UI-coding skill) read first; no stack rules hardcoded
- [ ] Reference discovered `/feature-discovery`-style (behaviour, workflow, navigation, permissions, states, data effects), evidence-backed and narrow — no bulk reads
- [ ] Any port-critical rule missing from the target's binding context was surfaced as an open question, not guessed
- [ ] Target current state surveyed; if UI, the target component preview (`/ui/preview/all`) was opened
- [ ] Sub-agents, if used, were user-allowed, non-overlapping, and read-only; the main agent synthesised; no duplicate discovery
- [ ] Gap map written to `<artifacts-root>/docs/port/<feature-slug>-gapmap.md` and re-opened — all nine section headings verified present; reference kept as behaviour-truth and target DS as UI-truth (deviations recorded)
- [ ] First slice is thin and independently testable
- [ ] Suggested `/grill-with-docs` and stopped — nothing implemented, no issue fabricated, no auto-chain
- [ ] Final `Stage / Found / Next / Needs user` update emitted

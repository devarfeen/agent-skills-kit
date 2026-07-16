---
name: port-feature
disable-model-invocation: true
description: Use when the user wants to port, migrate, rebuild, or recreate a feature that already exists in a REFERENCE implementation into a TARGET stack (e.g. bring a legacy screen into the new app). Sits at the discover → plan entry — reads the target's binding context, traces the reference's real behaviour/workflow/permissions/states the way /feature-discovery does, surveys what the target already has, and writes ONE gap map artifact, then suggests /grill-with-docs and stops. The reference is truth for behaviour; the target's design system is truth for UI. Never implements, never auto-chains; interviews for any missing input.
---

# Port feature

Port a feature that already works in a **REFERENCE** implementation into a **TARGET** stack, in the target's own idiom. This skill pulls the porting confidence — what the feature actually does, what the target already has, what's missing, what to reuse — out of someone's head onto disk as **one gap map** at the discover → plan entry, then hands off: a single pass, not a loop and not a pipeline.

## Inputs

Infer first from the request and cheap repo evidence (Project Matrix, cwd, `CONTEXT.md`, ADR names); interview `/feature-prompt`-style only for what's genuinely missing:

- **Feature to port** — the behaviour/workflow being brought over.
- **REFERENCE PROJECT-CODE** — the source of behaviour truth (e.g. a legacy repo).
- **TARGET PROJECT-CODE** — where the feature lands.

Do not start discovery until all three are known; if the user is away and one cannot be inferred, stop with a Needs-user note naming exactly which is missing — never guess.

## Source-of-truth framing

Carry this framing through every section of the gap map:

- **The REFERENCE is truth for behaviour** — workflow, navigation (menu placement, entry points, routes), permissions, data effects, and states. When the target's current behaviour disagrees with the reference, the reference wins (unless the user has explicitly decided to change the behaviour — a `/grill-with-docs` decision, not one this skill makes).
- **The TARGET's design system is truth for UI.** When reference UI conflicts with the target design system, choose the design system and **record the deviation** (reference did X; target DS does Y; chose DS) in the UI/design gaps section.
- **Never hardcode stack rules.** Read the target's rules from its binding context — `CONTEXT.md`, `specs/adr/`, `AGENTS.md` — and its UI-coding skill; a React Native target has different rules than a Livewire one. If a rule the port depends on (stack version, DS convention, component discipline, ADR location) is not recorded there, do not invent it — surface it under Open questions / Needs-user rather than guessing.

## Rules

- **Suggest, never auto-chain.** End by suggesting `/grill-with-docs` on the gap map, then stop. Do not run planning, do not open issues, do not implement.
- **Never implement here.** No product code, config, or migration edits; the only write is the gap map file.
- Name the full PROJECT-CODE from the Project Matrix everywhere; never mix one project's conventions, tokens, or components into another.
- **Narrow retrieval only.** Trace the reference and survey the target with targeted, evidence-backed search (`rg`/`git grep` for the exact route/path/symbol/state), `/feature-discovery`-style. **Never** bulk-read a repo or its `specs/` tree to "find everything".
- If `graphify-out/graph.json` exists (project root, else workspace root), query it before raw search; older than ~7 days → suggest `graphify update .`; missing → skip graphify. Verify graph answers against current code.
- **Retrieval order.** `CONTEXT.md` + `specs/adr/` are binding (read before deciding) > the current request, reference/target code, and tests > native CLI memory.
- **Decisions are artifacts.** The output is the durable gap map file, not a chat summary; chat reports only what was written and the phase update.
- **Don't fabricate an issue before coding.** Issues come later, from `/to-tickets` after `/grill-with-docs`.
- Sub-agents: local lanes only when the user allows them — never cloud agents; announce the lane count at dispatch and report each lane as it completes.

## Process

### 1. Read the target's binding context
`CONTEXT.md` and `specs/adr/` in the target's `<artifacts-root>`, plus the target's `AGENTS.md` and UI-coding skill for stack/DS rules — this sets the idiom of every later section. Done when the binding rules are in hand or each absence is noted for Open questions.

### 2. Discover the reference
Trace the real behaviour, workflow, navigation, permissions, states, and data effects, `/feature-discovery`-style. Done when every claim carries a concrete ref (`file:symbol`, route, migration, test).

### 3. Survey the target's current state
What exists today, what's partial or wrong versus the reference, and which design-system components and existing patterns are reusable. If the feature has UI, open the target's component preview (e.g. `/ui/preview/all`) to inventory available DS components before deciding what to build.

### 4. Dispatch bounded lanes (optional)
Only within the sub-agent rule above, split non-overlapping discovery — e.g. one lane on the reference trace, one on the target survey. No two lanes discover the same thing; the main agent merges and owns synthesis, uncertainty calls, and the artifact.

## The gap map artifact

Write **one** gap map per ported feature:

```text
<artifacts-root>/specs/port/<feature-slug>-gapmap.md
```

Resolve `<artifacts-root>`: the `*.code-workspace` directory if one exists, else the per-context root (`CONTEXT-MAP.md` at repo root), else the repo root. `<feature-slug>` is kebab-case from the feature name, max ~4 words, ASCII. The gap map is an on-demand slug file — it does not consume the `NNNN` prompt/ADR sequence; the ADR that `/grill-with-docs` produces next takes the next number in `specs/adr/`.

Nine sections, in order, **≤3 bullets each** — link or cite evidence (`file:line`, route, migration, test), never paste it:

```markdown
# Port Gap Map — <feature> (<REFERENCE-CODE> → <TARGET-CODE>)

## 1. Reference behaviour / workflow
- <behaviour/permission/state/data-effect> — evidence: `file:symbol`, route, migration, test.
- Navigation: where the feature lives in the reference and any moves the port implies.

## 2. Target current state
- <what exists today for this feature in the target> — evidence refs.

## 3. Missing / wrong in target
- <gap or divergence from the reference> — absent, partial, or behaving differently.

## 4. Reusable target code & DS components
- <existing target seam/service/component to extend> — path + why it fits.
- <design-system component from the target preview> — where it applies.

## 5. Tests needed
- Success paths, validation, permission checks, empty/error/success states, data effects, regressions to guard.

## 6. UI / design gaps vs reference (and forced DS deviations)
- <reference UI element> → <target DS equivalent>.
- Forced deviation: reference did X; target DS does Y; chose DS because <rule/source>.

## 7. Risks
- <behaviour, data, permission, or migration risk> and where it bites.

## 8. First slice
- One thin vertical slice that cuts through all layers and is testable on its own — not a layer, not a big-bang.

## 9. Open questions
- <evidence-derived question for /grill-with-docs>. List them; do not block on them.
```

Section rules (filled example bullets live in [`references/gapmap-example.md`](references/gapmap-example.md)):

- Every claim in sections 1–4 carries a concrete evidence ref; unproven claims are marked as inference, not fact.
- Section 5 seeds later acceptance criteria — cover every category its template bullet lists. Section 6 records every forced DS deviation explicitly.
- Section 9 is a list for `/grill-with-docs` to attack; it does not block writing the gap map.

## Output

After the gap map is written, suggest running `/grill-with-docs` on it, then stop — do not proceed past the suggestion. Emit `Stage / Found / Next / Needs user` at each phase transition — one line per field. Final update:

```markdown
Stage: port-feature — wrote specs/port/<feature-slug>-gapmap.md (<REFERENCE-CODE> → <TARGET-CODE>).
Found: <N> reference behaviours traced; target is <absent/partial/diverging>; <M> reusable target/DS pieces; <K> forced DS deviations; <R> risks.
Next: run /grill-with-docs on the gap map to challenge it and produce the ADR (next number in specs/adr/).
Needs user: <open questions to steer, or ambiguous reference/target mapping, or "none">.

Suggested next skills (optional):
- /grill-with-docs: challenge the gap map and record the porting decisions as an ADR.
- /prototype: if a UI/interaction open question needs to be seen or felt before planning.
```

## Completion criteria

- [ ] The gap map exists at the resolved `<artifacts-root>/specs/port/<feature-slug>-gapmap.md` with all nine section headings present and non-empty
- [ ] `git status` shows no files created or modified by this run outside the gap map file — nothing implemented
- [ ] The final `Stage / Found / Next / Needs user` update was emitted, ending at the `/grill-with-docs` suggestion

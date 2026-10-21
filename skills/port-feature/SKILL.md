---
name: port-feature
disable-model-invocation: true
description: "Use only to port, migrate, or rebuild a complete feature from a reference implementation into a target stack. Writes one gap map, suggests /grill-with-field, stops. Never implements or auto-chains."
metadata:
  version: "0.2.2"
---

# Port feature

Port a feature that already works in a **REFERENCE** implementation into a **TARGET** stack, in the target's own idiom. Pulls the porting confidence — what the feature does, what the target has, what's missing, what to reuse — onto disk as **one gap map** at the discover → plan entry, then hands off: a single pass, not a loop and not a pipeline.

## Inputs

Infer first from the request and cheap repo evidence (Project Matrix, cwd, `GLOSSARY.md`, ADR names); interview `/feature-prompt`-style only for what's genuinely missing:

- **Feature to port** — the behaviour/workflow being brought over.
- **REFERENCE PROJECT-CODE** — the source of behaviour truth.
- **TARGET PROJECT-CODE** — where the feature lands.

Do not start discovery until all three are known; if the user is away and one cannot be inferred, stop with a Needs-user note naming exactly which is missing — never guess.

## Source-of-truth framing

Carry this through every gap-map section:

- **The REFERENCE is truth for behaviour** — workflow, navigation (menu placement, entry points, routes), permissions, data effects, and states. When the target's current behaviour disagrees with the reference, the reference wins (unless the user has explicitly decided to change the behaviour — a `/grill-with-field` decision, not one this skill makes).
- **The TARGET's design system is truth for UI.** When reference UI conflicts with the target design system, choose the design system and **record the deviation** (reference did X; target DS does Y; chose DS) in the UI/design gaps section.
- **Never hardcode stack rules.** Read the target's rules from its binding context — `GLOSSARY.md`, `specs/adr/`, `AGENTS.md` — and its UI-coding skill. If a rule the port depends on (stack version, DS convention, component discipline, ADR location) is not recorded there, do not invent it — surface it under Open questions / Needs-user rather than guessing.

## Rules

- **Zero attribution.** Never add or leave co-author, AI, or tool attribution in any output; include this rule in the gap map.
- **Suggest, never auto-chain.** End by suggesting `/grill-with-field` on the gap map, then stop. Planning and issue creation wait for a separate request.
- **Never implement here.** No product code, config, or migration edits; the only write is the gap map file.
- Name the full PROJECT-CODE from the Project Matrix everywhere; never mix one project's conventions, tokens, or components into another.
- **Narrow retrieval only.** Trace the reference and survey the target with targeted, evidence-backed search (`rg`/`git grep` for the exact route/path/symbol/state), `/feature-discovery`-style. **Never** bulk-read a repo or its `specs/` tree to "find everything".
- **Read context before deciding.** `GLOSSARY.md` and relevant ADRs describe recorded decisions; current code and tests show implemented behavior. Follow the current user's explicit decisions, record conflicts with older context, and treat native CLI memory as a lead to verify.
- **Decisions are artifacts.** The output is the durable gap map file, not a chat summary; chat reports only what was written and the phase update.
- Sub-agents: dispatch local lanes automatically for independent work — never cloud agents; announce the lane count at dispatch and report each lane as it completes.

## Process

### 1. Read the target's binding context
Read `GLOSSARY.md` (legacy `CONTEXT.md`), `AGENTS.md`, and the UI-coding skill for stack/DS rules. Locate relevant ADRs by topic or linked decision; read only those, not the `specs/adr/` tree. Done when binding rules are in hand or each absence is noted for Open questions.

### 2. Discover the reference
Trace the real behaviour, workflow, navigation, permissions, states, and data effects, `/feature-discovery`-style. Include field validation and defaults, field interdependencies, row and bulk actions, import/export, auto-refresh, and role-gated controls. A path backed by mock, fixture, or stubbed data is not behaviour truth: mark it as inference and list it under Open questions. Done when every claim carries a concrete ref (`file:symbol`, route, migration, test).

### 3. Survey the target's current state
What exists today, what's partial or wrong versus the reference, and which design-system components and existing patterns are reusable. If the feature has UI, locate and inspect the target's component preview in an authorized local environment. If no preview exists or is available, inventory component source and record that limitation; do not invent a preview route.

### 4. Dispatch bounded lanes (optional)
Split non-overlapping discovery — e.g. one lane on the reference trace, one on the target survey. No two lanes discover the same thing; the main agent owns synthesis, uncertainty calls, and the artifact.

## The gap map artifact

Write **one** gap map per ported feature:

```text
<artifacts-root>/specs/port/<feature-slug>-gapmap.md
```

Resolve `<artifacts-root>`: the `*.code-workspace` directory if one exists, else the per-context root (`GLOSSARY-MAP.md` at repo root; legacy `CONTEXT-MAP.md`), else the repo root. `<feature-slug>` is kebab-case from the feature name, max ~4 words, ASCII. The gap map is an on-demand slug file — it does not consume the `NNNN` prompt/ADR sequence.

Read an existing gap map before updating it. Preserve user edits and recorded decisions; if new findings contradict them, show the conflict and wait for direction before replacing that text. If the user is away, retain it and append the conflict under Open questions.

Confirm an existing map names the same REFERENCE/TARGET pair. For a different pair, preserve that map and use `<feature-slug>-<REFERENCE-CODE>-<TARGET-CODE>-gapmap.md`; use this resolved path in the output and completion check.

Nine sections, in order, **≤3 bullets each** — link or cite evidence (`file:line`, route, migration, test), never paste it:

```markdown
# Port Gap Map — <feature> (<REFERENCE-CODE> → <TARGET-CODE>)

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

## 1. Reference behaviour / workflow
- <behaviour/permission/state/data-effect> — evidence: `file:symbol`, route, migration, test.
- Navigation: where the feature lives in the reference and any moves the port implies.

## 2. Target current state
- <what exists today for this feature in the target> — evidence refs.
- <target piece that already matches the reference> — do not touch; evidence ref.

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
- Coexistence: while reference and target both run on shared data, which one writes.

## 8. First slice
- One thin vertical slice that cuts through all layers and is testable on its own — not a layer, not a big-bang.

## 9. Open questions
- <evidence-derived question for /grill-with-field>. List them; do not block on them.
```

Section rules (filled example bullets live in [`references/gapmap-example.md`](references/gapmap-example.md)):

- Every claim in sections 1–4 carries a concrete evidence ref; unproven claims are marked as inference, not fact.
- Section 5 seeds later acceptance criteria — cover every category its template bullet lists.
- Section 5 marks each section-1 behaviour that has no reference test; port it behind a characterization test or list it under Open questions.

## Output

Emit `Stage / Found / Next / Needs user` at each phase transition — one line per field. Final update:

```markdown
Stage: port-feature — wrote specs/port/<feature-slug>-gapmap.md (<REFERENCE-CODE> → <TARGET-CODE>).
Found: <N> reference behaviours traced; target is <absent/partial/diverging>; <M> reusable target/DS pieces; <K> forced DS deviations; <R> risks.
Next: run /grill-with-field on the gap map to challenge it and produce the ADR (next number in specs/adr/).
Needs user: <open questions to steer, or ambiguous reference/target mapping, or "none">.

Suggested next skills (optional):
- /grill-with-field: challenge the gap map and record the porting decisions as an ADR.
- /prototype: if a UI/interaction open question needs to be seen or felt before planning.
```

## Completion criteria

- [ ] The gap map exists at the resolved path, including PROJECT-CODEs when needed to avoid a different pair's file, with all nine section headings present and non-empty
- [ ] `git status` shows no files created or modified by this run outside the gap map file — nothing implemented
- [ ] The final `Stage / Found / Next / Needs user` update was emitted, ending at the advisory suggestions footer

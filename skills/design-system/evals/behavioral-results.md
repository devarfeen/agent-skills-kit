# Design-system behavior evaluation

Date: 2026-09-09. Method: fresh-reader simulated execution against the revised instructions, not a browser, Figma, native build, or runtime invocation test. Each case below is one execution, without repetition. Fixture paths describe a hypothetical project.

Zero attribution: never add or leave co-author, AI, or tool attribution in commits, PRs, issues, docs, or comments.

## DS-1: No source and no approval

Input: "Bootstrap ADMIN-WEB's design system." The matrix identifies React. No source exists and the user is away.

Output: "Needs user: provide a Figma file, written design spec, reference screen, or approve a guided definition. No tokens, library, or preview created."

Actions: resolve ADMIN-WEB from the matrix, find no source, stop before building. Do not invent colors or infer approval from silence.

Assertions: source gate preserved PASS; no fabricated design PASS; no auto-chain PASS. Result: 3/3.

## DS-2: Adopt the existing project skill

Input: An approved written source covers Button and Input. ADMIN-WEB already has `.agents/skills/admin-ui/SKILL.md`, token file `src/ui/tokens.css`, and preview `/ui/preview/all`. A requested reusable DatePicker has no covering source.

Output fragment:

```markdown
Project skill: admin-ui
Tokens: src/ui/tokens.css
Preview: /ui/preview/all
DatePicker: pending source reference and authorized extension.
```

Actions: adopt `admin-ui`; record its real name in the doc and single AGENTS reference. Reuse covered Button/Input components. Suggest a separate extension for DatePicker and pause that dependency. Preserve any conflicting hand-written rule for a user decision.

Assertions: existing skill adopted without duplicate seed PASS; real paths recorded PASS; missing component not invented or auto-chained PASS. Result: 3/3.

## DS-3: Native preview is not an HTML response

Input: MOBILE-APP uses React Native. The extracted source names Button and Input. A local preview screenshot renders both, but no human has reviewed it. There is no HTML route or snapshot harness.

Output: "Stage: design-system bootstrap for MOBILE-APP. Found: Button and Input rendered in local simulator screenshot shots/mobile-preview.png. Next: open the local preview screen and review both components and states. Needs user: visual review pending; design system not yet verified."

Actions: record simulator build/screenshot and component inventory, register the outputs, mark the human half pending. Do not require a nonexistent HTML route or claim human verification.

Assertions: native evidence branch used PASS; inventory named PASS; human gate pending PASS. Result: 3/3.

## Limits

9/9 assertions passed in three simulations. A separate real check parsed the filled project-skill frontmatter with PyYAML and confirmed a string-valued description and correct name; all 14 invocation settings also parsed. No component generation, Figma extraction, render test, or human preview review was executed. Those remain evidence gaps rather than passing checks.

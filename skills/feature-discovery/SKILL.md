---
name: feature-discovery
description: "Trace how a named feature, module, workflow, API, config, or symbol works and who uses it; read-only. Whole-repo architecture summaries: /teach. Porting: /port-feature."
metadata:
  version: "0.3.1"
---

# Feature discovery

Feature-discovery traces how an existing feature, module, or behavior works and reports it in chat, evidence-cited: another engineer comes away knowing what it is, how it works, where it is used, and what remains uncertain.

## Inputs

Intake may be structured — `Projects Affected:` plus a `What:` block — or free-form; infer the projects and topic. Questions are for blocking clarifications only; user away → state the assumption and continue best-effort.

## Rules

- **Zero attribution.** Never add or leave co-author, AI, or tool attribution in any output.
- **Read-only, chat-only.** Do not edit code, config, docs, native memory, ADRs, prompts, issues, or generated artifacts while discovering — `GLOSSARY.md` and artifact edits wait for step 7 approval. Never create `docs/discovery/` files, and do not read legacy discovery files unless the user names one — they go stale. No `git fetch`, `git pull`, installs, migrations, or destructive commands.
- **Non-mutating validation.** Default to static inspection. Execute project or test commands only after establishing they will not change files or local/external state. Otherwise report the unrun check, not a pass. Clean `git status` alone proves neither ignored files nor databases stayed unchanged.
- **Current code is the source of truth.** Evidence order: current code, tests, and config first; then ADRs. Code establishes implemented behavior; ADRs and approved requirements record intended behavior. Cite both when they conflict; an implementation mismatch is not an approved rule change. A path served by mock, fixture, or stubbed data is not implemented behavior; say so. Separate evidence from inference and never invent rationale. The tell: rewriting a business rule to match a possible bug.
- **Git history is opt-in.** Never read it during discovery; offer a scan in the report (step 7).
- **Trace behavior, not just symbols.** Connect entry points, relevant conditions, state changes, callers, and downstream effects with cited links or explicit gaps. Flag seam-reuse across similar paths. The tell: a symbol dump with no usage site or user-visible effect.
- **Keep scope thin.** Split broad intake; name the first slice and deferred slices. Stop when scoped questions are answered or evidence gaps reported after validation; unresolved work beyond available context needs a scope split or handoff. The tell: drifting into product discovery or experiment design without an explicit pivot.
- **Stop after presenting the report.** Suggest the next skill; never invoke it or start implementation without a fresh request. Grillable unknowns stay as open decisions for `/feature-prompt` or `/grill-with-field`; ungrillable ones ("needs to feel/see it") route to `/handoff` + `/prototype` (when installed; else state the uncertainty plainly). Destination or open questions still foggy → suggest `/wayfinder`, not `/feature-prompt`; a PR-sized prompt cannot be written through fog.
- Emit `Stage / Found / Next / Needs user` at each phase transition — one line per field. Phases: parsed, code traced, validated, report.
- Sub-agents: dispatch local lanes automatically for independent work — never cloud agents; announce the lane count at dispatch and report each lane as it completes. Summaries back, not transcripts; synthesis stays in the main session.

## Workflow

### 1. Parse and locate

List the questions to answer. Map project codes to git roots and package boundaries using repo names, metadata, or READMEs. Record inspected revisions/working-tree state and starting `git status`; preserve existing changes. Unmappable projects remain explicit gaps while scoped work continues.

Resolve `<artifacts-root>`: the `*.code-workspace` directory if one exists, else the per-context root (`GLOSSARY-MAP.md` at repo root; legacy `CONTEXT-MAP.md`), else the repo root.

### 2. Trace the current code

Search exact terms, then aliases, routes, components, config keys, env vars, tables, jobs, flags, and tests; `rg` first, CLI before MCP for codebase evidence. For unclear dependencies, inspect available source or official upstream source read-only. Missing source requiring download/install is a reported gap and suggested follow-up.

### 3. Read ADRs

Find ADRs touching the topic (`docs/adr/`, `docs/decisions/`, or ones `GLOSSARY.md` or code comments reference) under `<artifacts-root>` and the mapped projects. Record each one's status (accepted, superseded, proposed) and whether current code agrees with it. None found → say where you looked.

### 4. Read issues bounded, or not at all

Read issues the user names or that can resolve a material gap; when no issue is requested and local evidence answers the question, mark tracker review unnecessary; do not request broad-scan approval. Read every bounded issue and its comments; use exact terms or reliable labels for bounded searches. Scope each lookup to its mapped repository/tracker (default `gh issue view <n> --comments`; workspace tracker mappings take precedence). If a material gap requires an unbounded scan, explain its cost and ask first. Declined, unavailable, or no reply → skip that scan, state the limit, and continue available scoped work.

### 5. Track candidate context terms

Compare discovered domain terms with `GLOSSARY.md` — at `<artifacts-root>`, else nearby project docs — and flag missing, stale, renamed, overloaded, or ambiguous ones. Only when candidates exist, load [`references/context-terms.md`](references/context-terms.md) for qualification, presentation, and approval. With none, report that in one line.

### 6. Validate twice

Pass 1: cross-check each answer against code, tests, config, and context used. Pass 2: use aliases and reverse lookups to seek contradictory paths. Before calling code unused, check relevant indirect registrations, routes, listeners, flags, import path aliases, and dynamically built names (template-string URLs, concatenated keys); matches only in generated or build output (`dist/`, `build/`, generated clients) are not source evidence, and no matches means only not found in the searched scope. Validate terms against implemented and intended behavior; mark ownership, test, and evidence gaps. Account for every requested question: answered with evidence, unresolved with the missing evidence named, or explicitly deferred outside this slice.

### 7. Present the report and stop

When step 2 left a why-or-when question, section 8 ends with a history offer: the question, the traced files, and a last-2-months window. Scan only on a fresh yes, read-only (`git log`, `git show`, `git blame`; extend a targeted lookup for older evidence), and answer as a short addendum that also notes repeated fix commits on the traced files.

For `GLOSSARY.md` or other artifact updates after the report: show each target path, proposed text, and reason; wait for explicit approval, then follow **Applying approved updates** in `references/context-terms.md` (away-fallback: no reply → no edits; candidates stay in the report).

## Output

Use the numbered structure below, ≤3 bullets per section; aim for ~550 words without dropping answers or caveats. `Quick trace` is for simple single-project answers without material branching, context candidates, or conflicts — not merely a question naming one symbol. Declare it up front, use sections 1–3, 5, and 9 (one line for 5), and mark others N/A. Include requested usage and rationale within sections 1–3. Otherwise use the full report; never abbreviate a multi-project discovery.

Sections, in order: 1 Summary · 2 What it does · 3 How it works · 4 Where it is used · 5 ADRs · 6 Why it was needed / context · 7 Candidate GLOSSARY.md terms · 8 Risks, gaps, and recommended next checks · 9 Validation performed · 10 Suggested next skills (optional, 1–3). For the full report, load [`references/report-template.md`](references/report-template.md); Quick trace uses the eligible sections above without loading the full template.

**Evidence style.** Cite `file:line` or file plus symbol and its role. In cross-project reports, qualify paths by PROJECT-CODE and issues by repository/tracker, not bare `#123`; commits need repository, short hash, and date. Distinguish inspected source, inspected tests, executed checks, runtime observations, ADR text, and inference. Source defaults do not prove deployed configuration. Quote only decisive output from commands actually run; name skipped checks and searched scope for negative claims.

## Completion criteria

- [ ] Every factual claim in sections 1–9 carries a citation per Evidence style
- [ ] Every requested question has an evidenced answer, named evidence gap, or explicit scope deferral
- [ ] Starting/ending `git status` compared; existing changes preserved; executed commands satisfy the non-mutating rule (approved step-7 updates excepted)
- [ ] No git history command ran before the user accepted the section 8 offer
- [ ] Full report follows numbered order (section 10 optional), or eligible `Quick trace` includes sections 1–3, 5, and 9
- [ ] When section 7 is included, it ends with the four-option approval ask or the no-candidates line
- [ ] Session stopped after the report — no skill invoked, no implementation started

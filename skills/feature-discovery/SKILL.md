---
name: feature-discovery
description: Use when the user asks to investigate, audit, trace, or explain how an existing feature, issue, module, workflow, API, config, or behavior works — or what uses a module, service, or symbol and why it exists — across one or more codebase projects, especially before planning, debugging, migration, refactor, or implementation. Porting or rebuilding a feature into another stack routes to /port-feature instead. Stays read-only and surfaces code-discovered domain terms that may be missing from or stale in CONTEXT.md so the user can approve follow-up context updates. A whole-repo "how does everything connect" question is the graphify companion's job.
---

# Feature discovery

Feature-discovery traces how an existing feature, module, or behavior works and reports it in chat, evidence-cited: another engineer comes away knowing what it is, how it works, where it is used, and what remains uncertain.

## Inputs

Intake may be structured — `Projects Affected:` plus a `What:` block — or free-form; infer the projects and topic. Questions are for blocking clarifications only; user away → state the assumption and continue best-effort.

## Rules

- **Zero attribution.** Never add or leave co-author, AI, or tool attribution in any output.
- **Read-only, chat-only.** Do not edit code, config, docs, native memory, ADRs, prompts, issues, or generated artifacts while discovering — `CONTEXT.md` and artifact edits wait for step 6 approval. Never create `docs/discovery/` files, and do not read legacy discovery files unless the user names one — they go stale. No `git fetch`, `git pull`, installs, migrations, or destructive commands.
- **Non-mutating validation.** Default to static inspection. Execute project or test commands only after establishing they will not change files or local/external state. Otherwise report the unrun check, not a pass. Clean `git status` alone proves neither ignored files nor databases stayed unchanged.
- **Actual versus intended.** Code establishes implemented behavior; approved requirements record intended behavior. Cite both when they conflict; an implementation mismatch is not an approved rule change. Separate evidence from inference and never invent rationale. The tell: rewriting a business rule to match a possible bug.
- Use `graphify-out/graph.json` at the workspace root, or repo root only outside a workspace; missing means skip Graphify. Query before raw search and verify hits against current source. Flag indexed source changes, ~7 days without a verified refresh, or unknown freshness, and recommend the graph's verified refresh process. Scope with `graphify query`/`path`/`explain` before broad `rg` sweeps. Discovery stays read-only: never refresh graphs. Do not hunt for a graph elsewhere or suggest installing it.
- **Trace behavior, not just symbols.** Connect entry points, relevant conditions, state changes, callers, and downstream effects with cited links or explicit gaps. Flag seam-reuse across similar paths. The tell: a symbol dump with no usage site or user-visible effect.
- **Keep scope thin.** Split broad intake; name the first slice and deferred slices. Stop when scoped questions are answered or evidence gaps reported after validation; unresolved work beyond available context needs a scope split or handoff. The tell: drifting into product discovery or experiment design without an explicit pivot.
- **Stop after presenting the report.** Suggest the next skill; never invoke it or start implementation without a fresh request. Grillable unknowns stay as open decisions for `/feature-prompt` or `/grill-with-docs`; ungrillable ones ("needs to feel/see it") route to `/handoff` + `/prototype` (when installed; else state the uncertainty plainly). Destination or open questions still foggy → suggest `/wayfinder`, not `/feature-prompt`; a PR-sized prompt cannot be written through fog.
- Emit `Stage / Found / Next / Needs user` at each phase transition — one line per field. Phases: parsed, discovered, validated, report.
- Sub-agents: dispatch local lanes automatically for independent work — never cloud agents; announce the lane count at dispatch and report each lane as it completes. Summaries back, not transcripts; synthesis stays in the main session.

## Workflow

### 1. Parse and locate

List the questions to answer. Map project codes to git roots and package boundaries using repo names, metadata, or READMEs. Record inspected revisions/working-tree state and starting `git status`; preserve existing changes. Unmappable projects remain explicit gaps while scoped work continues.

### 2. Discover the topic

Search exact terms, then aliases, routes, components, config keys, env vars, tables, jobs, flags, and tests; `rg` first, CLI before MCP for codebase evidence. For unclear dependencies, inspect available source or official upstream source read-only. Missing source requiring download/install is a reported gap and suggested follow-up. Use git history when code cannot explain why or when behavior changed; start with the last 2 months and extend a targeted lookup for older evidence.

### 3. Read issues bounded, or not at all

Read issues the user names or that can resolve a material gap. When no issue is requested and local evidence answers the question, mark tracker review unnecessary; do not request broad-scan approval. Otherwise find references in relevant context, ADRs, docs, or caches. Read every bounded issue and its comments; use exact terms or reliable labels for bounded searches. Scope each lookup to its mapped repository/tracker (default `gh issue view <n> --comments`; workspace tracker mappings take precedence). If a material gap requires an unbounded scan, explain its cost and ask first. Declined, unavailable, or no reply → skip that scan, state the limit, and continue available scoped work.

Resolve `<artifacts-root>`: the `*.code-workspace` directory if one exists, else the per-context root (`CONTEXT-MAP.md` at repo root), else the repo root.

### 4. Track candidate context terms

Compare discovered domain terms with `CONTEXT.md` — at `<artifacts-root>`, else nearby project docs — and flag missing, stale, renamed, overloaded, or ambiguous ones. What qualifies, presentation, the away-fallback, and applying approvals live in [`references/context-terms.md`](references/context-terms.md).

### 5. Validate twice

Pass 1: cross-check each answer against code, tests, config, and context used. Pass 2: use aliases and reverse lookups to seek contradictory paths. Before calling code unused, check relevant indirect registrations, routes, listeners, and flags; no matches means only not found in the searched scope. Validate terms against implemented and intended behavior; mark ownership, test, and evidence gaps. Account for every requested question: answered with evidence, unresolved with the missing evidence named, or explicitly deferred outside this slice.

### 6. Present the report and stop

For `CONTEXT.md` or other artifact updates after the report: show each target path, proposed text, and reason; wait for explicit approval, then follow **Applying approved updates** in `references/context-terms.md` (away-fallback: no reply → no edits; candidates stay in the report).

## Output

Use the numbered structure below, ≤3 bullets per section; aim for ~500 words without dropping answers or caveats. `Quick trace` is for simple single-project answers without material branching, context candidates, or conflicts — not merely a question naming one symbol. Declare it up front, use sections 1–3 and 8, and mark others N/A. Include requested usage and rationale within sections 1–3. Otherwise use the full report; never abbreviate a multi-project discovery.

```markdown
# Feature discovery: [Topic]

## 1. Summary

- [Main answer, scoped projects, key caveat, and any deferred slices.]

## 2. What it does

- [Behavior in product/domain terms: inputs, outputs, side effects, project(s).]

## 3. How it works

- [Flow; key files, functions, routes, configs, jobs; conditions, flags, error paths.]

## 4. Where it is used

- [Usage sites with file references; tests/docs/configs confirming usage.]

## 5. Why it was needed / context

- [Recorded rationale and intended behavior, cited separately from implementation; or no reliable rationale found in the inspected sources.]

## 6. Candidate CONTEXT.md terms

- [`Term` — action; description; evidence; why it matters. For discrepancies, quote context beside implementation and approved intent; do not assume context is stale.]
- [End with: "Reply with the term names to approve, wording changes, `approve all`, or `skip context updates`." If none: "No candidate CONTEXT.md term updates found."]

## 7. Risks, gaps, and recommended next checks

- [Unresolved questions, missing evidence, contradictions, or risks; next check and unexamined scope.]

## 8. Validation performed

- [Inspected projects/states, evidence types and checks in both passes; commands actually run; skipped checks; tracker outcome (unnecessary, bounded, approved broad scan, skipped, unavailable) and issues read/excluded.]

## 9. Suggested next skills (optional)

- [/skill-name: reason tied to this report. 1–3 items, adjacent workflow steps.]
```

**Evidence style.** Cite `file:line` or file plus symbol and its role. In cross-project reports, qualify paths by PROJECT-CODE and issues by repository/tracker, not bare `#123`; commits need repository, short hash, and date. Distinguish inspected source, inspected tests, executed checks, runtime observations, and inference. Source defaults do not prove deployed configuration. Quote only decisive output from commands actually run; name skipped checks and searched scope for negative claims.

## Completion criteria

- [ ] Every factual claim in sections 1–8 carries a citation per Evidence style
- [ ] Every requested question has an evidenced answer, named evidence gap, or explicit scope deferral
- [ ] Starting/ending `git status` compared; existing changes preserved; executed commands satisfy the non-mutating rule (approved step-6 updates excepted)
- [ ] Full report follows numbered order (section 9 optional), or eligible `Quick trace` includes requested usage/rationale in sections 1–3 and validation in 8
- [ ] When section 6 is included, it ends with the four-option approval ask or the no-candidates line
- [ ] Session stopped after the report — no skill invoked, no implementation started

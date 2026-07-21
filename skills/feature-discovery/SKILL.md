---
name: feature-discovery
description: Use when the user asks to investigate, audit, trace, or explain how an existing feature, issue, module, workflow, API, config, or behavior works — or what uses a module, service, or symbol and why it exists — across one or more codebase projects, especially before planning, debugging, migration, refactor, or implementation. Porting or rebuilding a feature into another stack routes to /port-feature instead. Stays read-only and surfaces code-discovered domain terms that may be missing from or stale in CONTEXT.md so the user can approve follow-up context updates. A whole-repo "how does everything connect" question is the graphify companion's job.
---

# Feature discovery

Feature-discovery traces how an existing feature, module, or behavior works and reports it in chat, evidence-cited: another engineer comes away knowing what it is, how it works, where it is used, and what remains uncertain. Porting into another stack is `/port-feature`; a whole-repo "how does everything connect" question belongs to the graphify companion (when installed).

## Inputs

Intake may be structured — `Projects Affected:` plus a `What:` block — or free-form; infer the projects and topic; ask only when the mapping is genuinely ambiguous. Questions are for blocking clarifications only; user away → state the assumption and continue best-effort.

## Rules

- **Read-only, chat-only.** Do not edit code, config, docs, native memory, ADRs, prompts, issues, or generated artifacts while discovering — `CONTEXT.md` and artifact edits wait for step 6 approval. Never create `docs/discovery/` files, and do not read legacy discovery files unless the user names a specific one — they go stale; prefer current code, ADRs, CONTEXT, issues, tests, and fresh search. No `git fetch`, `git pull`, installs, migrations, or destructive commands.
- **Code is the source of truth when evidence conflicts with prose docs, issues, or comments.** Back every claim with file paths, symbols, commands, tests, docs, GitHub issues, or commits; separate confirmed facts from inference; never invent rationale. The tell: a comment, issue, or native memory outranking the code it describes.
- If `graphify-out/graph.json` exists (project root, else workspace root), query it before raw search; older than ~7 days → suggest `graphify update .`; missing → skip graphify. Scope with `graphify query`/`path`/`explain` before broad `rg` sweeps. Verify graph answers against current code and flag staleness — never run `graphify update .` yourself; discovery stays read-only. Do not hunt for a graph elsewhere or suggest installing it.
- **Trace behavior, not just symbols.** Follow definitions to callers and user-facing flows from entry points down; flag seam-reuse when similar behavior exists in multiple paths. The tell: a symbol dump with no usage site or user-visible effect.
- **Keep scope thin.** Broad intake gets split; discover the first slice before expanding. Near `~120K` tokens with core unknowns unresolved, stop and recommend a scope split or handoff. The tell: drifting into product discovery, interview planning, opportunity trees, or experiment design without an explicit pivot.
- **Stop after presenting the report.** Suggest the next skill; never invoke it or start implementation without a fresh request. Grillable unknowns stay as open decisions for `/feature-prompt` or `/grill-with-docs`; ungrillable ones ("needs to feel/see it") route to `/handoff` + `/prototype` (when installed; else state the uncertainty plainly). Scope-gating decisions still foggy — destination or open questions not yet sharp — suggest `/wayfinder`, not `/feature-prompt`; a PR-sized prompt cannot be written through fog.
- Emit `Stage / Found / Next / Needs user` at each phase transition — one line per field. Phases: parsed, discovered, validated, report.
- Sub-agents: dispatch local lanes automatically for independent work — never cloud agents; announce the lane count at dispatch and report each lane as it completes. Summaries back, not transcripts; synthesis stays in the main session.

## Workflow

### 1. Parse and locate

Identify project codes and topic from intake or inference. Map codes to git roots and package boundaries via repo names, package metadata, or READMEs; unmappable → say so early, continue best-effort.

### 2. Discover the topic

Search exact terms from `What`, then likely aliases, routes, components, API paths, config keys, env vars, tables, filenames, and test names — `rg` first; prefer CLI over MCP for codebase evidence. Include tests, docs, configs, migrations, background jobs, and feature flags when relevant. Critical dependency internals with thin local evidence → optionally fetch targeted dependency source (`opensrc`, when installed), minimal scope, cited concretely. Git history only when code scanning does not explain the topic, and only the last 2 months — why or when behavior changed, never primary truth.

### 3. Read issues bounded, or not at all

First mine context for issue references: the conversation, `AGENTS.md`, `<artifacts-root>/CONTEXT.md`, ADRs under `<artifacts-root>/specs/adr/`, local docs, and issue caches. A bounded issue set → read every issue with comments (`gh issue view <n> --comments`); reliable labels or exact terms → bounded search, reading every plausible match. If context cannot bound the search, pause and ask the user to approve a broad GitHub issue scan first — explain that it can take a long time. Not granted, or user away → continue with code, docs, tests, and history, stating that broad scanning was skipped.

Resolve `<artifacts-root>`: the `*.code-workspace` directory if one exists, else the per-context root (`CONTEXT-MAP.md` at repo root), else the repo root.

### 4. Track candidate context terms

Compare discovered domain terms with `CONTEXT.md` — at `<artifacts-root>`, else nearby project docs — and flag missing, stale, renamed, overloaded, or ambiguous ones. What qualifies, presentation, the away-fallback, and applying approvals live in [`references/context-terms.md`](references/context-terms.md) (shared with `feature-prompt`).

### 5. Validate twice

Pass 1: cross-check the explanation against code, tests, docs, configs, context, related issues, and any history used. Pass 2: repeat with aliases and reverse lookups, hunting contradictory code paths and stale assumptions; tighten or downgrade claims. Validate candidate terms against the strongest code evidence, sweep the tells in Rules, and mark dead code, unclear ownership, missing tests, contradictions, and skipped scans; note what each pass checked.

### 6. Present the report and stop

For `CONTEXT.md` or other artifact updates after the report: show each target path, proposed text, and reason; wait for explicit approval, then follow **Applying approved updates** in `references/context-terms.md` (away-fallback: no reply → no edits; candidates stay in the report).

## Output

Use this structure exactly: ≤3 bullets per section; keep the whole report under ~500 words unless the trace spans multiple projects. For a trivially small question (one symbol, config key, or route), say `Quick trace` up front and emit only sections 1–3 and 8, marking the rest N/A — never shrink a genuine multi-project discovery this way.

```markdown
# Feature discovery: [Topic]

## 1. Summary
- [What this is, where it lives, main finding, key caveat.]

## 2. What it does
- [Behavior in product/domain terms: inputs, outputs, side effects, project(s).]

## 3. How it works
- [Flow; key files, functions, routes, configs, jobs; conditions, flags, error paths.]

## 4. Where it is used
- [Usage sites with file references; tests/docs/configs confirming usage.]

## 5. Why it was needed / context
- [From conversation, docs, comments, issues, or recent commits — or: "No reliable rationale found in context, docs, comments, or recent history."]

## 6. Candidate CONTEXT.md terms
- [`Term` — suggested action; short description; evidence; why it matters. Stale context → quote current wording beside the contradicting code.]
- [End with: "Reply with the term names to approve, wording changes, `approve all`, or `skip context updates`." If none: "No candidate CONTEXT.md term updates found."]

## 7. Risks, gaps, and recommended next checks
- [Risk (user-value, usability, feasibility, viability, data, security, operational), dead code, missing test, or unclear owner; next check; what could not be verified.]

## 8. Validation performed
- [Checks run in each pass, commands named; anything skipped stated, including whether broad issue scanning was approved, bounded, skipped, or unavailable; which issues were read and which excluded as unrelated.]

## 9. Suggested next skills (optional)
- [/skill-name: reason tied to this report. 1–3 items, adjacent workflow steps.]
```

**Evidence style.** Cite `file:line` (or file plus symbol) with its role; issues as `#123`, commits as short hash plus date. For quoted command output, quote the shortest decisive tail — the pass/fail line and counts — and name the rest.

## Completion criteria

- [ ] Every factual claim in sections 1–8 carries a citation (file:line/symbol, route, command output, issue, or commit)

- [ ] `git status` shows no files created or modified by this discovery
- [ ] All nine sections in order — or `Quick trace` declared, with sections 1–3 and 8 and the rest N/A
- [ ] Section 6 ends with the four-option approval ask, or the no-candidates line
- [ ] Session stopped after the report — no skill invoked, no implementation started

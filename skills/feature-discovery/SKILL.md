---
name: feature-discovery
description: Use when the user asks to investigate, audit, trace, or explain how an existing feature, issue, module, workflow, API, config, or behavior works — or what uses a module, service, or symbol and why it exists — across one or more codebase projects, especially before planning, debugging, migration, refactor, or implementation. Porting or rebuilding a feature into another stack routes to /port-feature instead. Stays read-only and surfaces code-discovered domain terms that may be missing from or stale in CONTEXT.md so the user can approve follow-up context updates.
---

# Feature Discovery

## Purpose

Read-only discovery, reported in chat only. The bar: another engineer should
come away knowing what the thing is, what it does, how it works, where it is
used, what evidence supports that, and what remains uncertain.

**Not this skill.** This traces a bounded feature, module, or behavior. Porting
one into another stack is `/port-feature`; a broad whole-repo architecture
summary or graph-scale "how does everything connect" question is where the
graphify companion (when installed) beats a discovery pass.

Structured intake looks like:

```markdown
Projects Affected: [Project Code], [Project Code]

What:
[FEATURE / ISSUE / BEHAVIOR / MODULE / WORKFLOW]
```

Free-form intake is equally valid — infer the projects and topic from the
request and ask only when the mapping is genuinely ambiguous.

## Rules

**Read-only, chat-only.**

- Do not edit code, config, docs, native memory, ADRs, prompts, issues, or
  generated artifacts while discovering. `CONTEXT.md` and artifact edits happen
  only as the approved follow-up in workflow step 9.
- Never create `docs/discovery/` files, and do not read legacy discovery files
  unless the user names a specific one — they go stale; prefer current code,
  ADRs, CONTEXT, issues, tests, and fresh search.
- Do not run `git fetch`, `git pull`, installs, migrations, or destructive
  commands.

**Evidence.**

- Code is the source of truth when evidence conflicts with prose docs, issues, or comments.
- Check for a graphify knowledge base before broad searching:
  `graphify-out/graph.json` at the project root, else at the workspace root
  (the directory containing the `*.code-workspace` file). Found → scope the
  trace with `graphify query` / `graphify path` / `graphify explain` before
  broad `rg` sweeps, and verify graph answers against current code before
  citing them. Missing in both places → skip graphify entirely; do not hunt
  elsewhere or suggest installing it.
- Treat the graph as stale when `graph.json` is older than ~7 days: still use
  it for scoping, but flag the staleness in the report and recommend the user
  run `graphify update .` — never run it yourself; discovery stays read-only.
- Use `rg` first for text search; prefer CLI tools over MCP for codebase
  evidence. Use `git`, `git grep`, `find`, `gh`, package metadata, local docs,
  issues, and tests as needed.
- Scan the codebase before git history. Use history only when code scanning
  does not explain the topic, and review only the last 2 months — to explain
  why or when behavior changed, not as primary truth.
- If external dependency internals are critical and local evidence is
  insufficient, optionally fetch targeted dependency source (e.g. `opensrc`,
  when installed) and cite concrete files/functions. Keep fetch scope minimal.
- Back every concrete claim with file paths, symbols, commands, tests, docs,
  GitHub issues, or commits. Separate confirmed facts from inference. Do not
  invent context or rationale.

**Scope and steering.**

- Keep discovery scope thin. If intake spans many workflows or projects, split
  into slices and discover the first slice before expanding.
- The human stays in charge. Discovery questions are for blocking
  clarifications only, not open-ended interrogation. If the user is away,
  state the assumption taken and continue best-effort.
- Stop after presenting the report. Suggest the next skill; never invoke it or
  start implementation without a fresh request.
- Classify unresolved unknowns by fidelity: grillable (low fidelity) stays as
  concise open decisions for `/feature-prompt` or `/grill-with-docs`;
  ungrillable ("needs to feel/see it") routes to `/handoff` + `/prototype`
  (when installed; otherwise state the uncertainty plainly for the user)
  instead of speculative discovery.
- Flag duplication risks explicitly: when similar behavior exists in multiple
  paths, call out likely seam-reuse opportunities for the next planning step.
- Treat `~120K` tokens as a context-budget caution point. If unresolved core
  unknowns remain near it, stop and recommend a scope split or handoff.
- Emit `Stage / Found / Next / Needs user` at phase transitions
  (parsed → discovered → validated → report).

**Sub-agents (when the runtime supports them and the user allows).**

- Act as the orchestrator: dispatch read-only **Explorer** lanes for codebase
  discovery and **Researcher** lanes for external docs or dependency source —
  local subagents only, never cloud. Split lanes by project, module, or
  evidence stream; push long scans to local background where supported.
- Lanes return file paths, symbols, commands, and uncertainty — summaries, not
  transcripts. The main session owns synthesis, evidence quality, uncertainty
  calls, conflict resolution, and the final report.

**Candidate context terms.**

- When exploration reveals domain terms, compare them with `CONTEXT.md` and
  flag missing, stale, renamed, overloaded, or ambiguous ones. What qualifies,
  how to present the list, the away-fallback, and how to apply approvals live
  in [`references/context-terms.md`](references/context-terms.md) (shared with
  `feature-prompt`).

## Discovery Lens

Use this lens to keep discovery grounded in existing system behavior:

- **Behavior:** what currently exists and what users, systems, jobs, APIs, or operators experience.
- **Boundary:** owning project, module, data path, entry points, exits, and explicit non-goals.
- **Evidence:** strongest files, tests, configs, docs, issues, commands, and runtime paths.
- **Risk:** impact labels grounded in the code — user-value regression, usability, feasibility (can we build on it), viability (cost/maintainability), data, security, or operational risk.
- **Uncertainty:** confirmed facts, inference, open unknowns, stale context, and contradictions.
- **Next action:** the smallest useful next skill, human decision, test, issue read, or implementation slice.

## Common Discovery Mistakes

Avoid these failure modes:

- Reading stale discovery files before current code and tests.
- Ignoring an existing graphify knowledge base before broad sweeps — or
  hunting for one after both the project root and workspace root came up empty.
- Treating comments or native memory as stronger than code.
- Explaining implementation symbols without tracing user-facing behavior and usage sites.
- Running broad GitHub issue scans when local context does not bound the search.
- Dumping symbols instead of describing the behavior, boundary, evidence, risks, and unknowns.
- Skipping alias searches, reverse lookups, contradiction checks, or dead-code checks.
- Turning codebase discovery into product discovery, interview planning, opportunity solution trees, or experiment design unless the user explicitly pivots to another skill.

## Workflow

1. Parse the request:
   - Identify project codes and the topic — from the `Projects Affected` /
     `What` fields when present, otherwise inferred from free-form intake.
   - Note explicit constraints, dates, branches, modules, or terms.

2. Locate project roots:
   - Find relevant git roots and package/app boundaries.
   - Map project codes to folders by repo names, package metadata, READMEs, config, or naming conventions.
   - If a project code cannot be mapped, state that early and continue best-effort.

3. Discover the topic:
   - Search exact terms from `What`, then likely aliases, route names, component names, API paths, config keys, env vars, table names, filenames, and test names.
   - Trace definitions to callers, and user-facing flows from entry points to lower-level services.
   - Include tests, docs, configs, migrations, routes, background jobs, and feature flags when relevant.
   - Keep notes under the Discovery Lens.

4. Discover related context and GitHub issues (bounded, or not at all):
   - First inspect available context for issue references or topic clues: the conversation, `AGENTS.md`, `<artifacts-root>/CONTEXT.md`, ADRs under `<artifacts-root>/specs/adr/`, local docs, local issue caches, and prior prompt context.
   - If context gives a bounded issue set, read every issue in it (`gh issue view`). If it gives reliable labels, milestones, titles, or exact search terms, run a bounded search and read every plausibly related match.
   - If context cannot bound the search, pause and ask the user to approve a broad GitHub issue scan first — explain that it can take a long time. Not granted (or the user is away) → continue with code, docs, tests, local context, and history, and state that broad scanning was skipped.
   - Summarize which issues were read, which were excluded as unrelated, and whether broad scanning was skipped.

5. Track candidate `CONTEXT.md` terms per `references/context-terms.md`:
   - Locate the relevant `CONTEXT.md` via the kit's artifacts-root order — (1) the directory containing a `*.code-workspace` file, (2) the per-context root in a multi-context repo (`CONTEXT-MAP.md` at root), (3) the single repo root — then nearby project docs when none exists there.
   - Capture each candidate in the shared format from `references/context-terms.md`.

6. Use git history only if needed, per the Evidence rules.

7. Validate findings twice:
   - Pass 1: cross-check the main explanation against code, tests, docs, configs, usage sites, available context, related issues, and any history used.
   - Pass 2: repeat with aliases and reverse lookups, re-open the strongest evidence, hunt contradictory code paths, issue comments, docs, commits, and stale assumptions — then tighten or downgrade claims.
   - Validate candidate terms against `CONTEXT.md` and the strongest code evidence.
   - Check the Common Discovery Mistakes list and correct the report before presenting.
   - Mark dead code, unclear ownership, missing tests, contradictions, skipped issue scans, stale context terms, and unverified assumptions. Avoid broad claims on partial evidence.
   - Keep a short validation note stating what each pass checked.

8. Present the discovery report in chat, using the Output Format below.

9. Update `CONTEXT.md` or other artifacts only after approval:
   - Show the exact target path(s), proposed text/section changes, and the reason for each. Wait for explicit approval, then follow **Applying approved updates** in `references/context-terms.md` (including its away-fallback: no reply → no edits, keep the candidates in the report).

## Search Defaults

Adapt commands to the repo. Keep command output summarized in the final report.

```bash
graphify query "exact topic"   # only when graphify-out/graph.json exists — project root, else workspace root
find graphify-out/graph.json -mtime +7   # output means the graph is >7 days old — recommend `graphify update .`
rg -n "exact topic|likely alias|route|config_key" .
find . -maxdepth 4 \( -name package.json -o -name README.md -o -name .git \)
git grep -n "term"
gh issue view <issue-number> --comments
gh issue list --state all --search "exact topic OR likely alias"
git log --since="2 months ago" --oneline --all -- <relevant-path>
```

## Output Format

Use this structure exactly for the chat report. State if any validation or issue scan was skipped.

For a trivially small in-scope question (one symbol, one config key, one route), say `Quick trace` up front and emit only sections 1–3 and 8, marking the rest N/A. Anything larger uses the full structure — do not shrink a genuine multi-project discovery.

```markdown
# Feature Discovery: [Topic]

## 1. Summary

- [Short answer: what this is and where it lives.]
- [Main finding or current behavior.]
- [Important caveat, if any.]

## 2. What It Does

- [Describe the behavior in product/domain terms.]
- [Mention inputs, outputs, side effects, or user-visible result.]
- [Mention relevant project(s).]

## 3. How It Works

- [Step-by-step flow.]
- [Key files, functions, classes, routes, configs, jobs, services, or data models.]
- [Important conditions, flags, dependencies, or error paths.]

## 4. Where It Is Used

- [Usage site 1 with file reference.]
- [Usage site 2 with file reference.]
- [Tests/docs/configs that confirm usage.]

## 5. Why It Was Needed / Context

- [Use the conversation, local docs, comments, issues, or recent commits if available.]
- [If not found: "No reliable rationale found in available context, docs, comments, or recent git history."]

## 6. Candidate CONTEXT.md Terms

- [If candidates exist, list each as: `Term` — suggested action; short description; evidence; why it matters.]
- [If existing context may be stale, state the current context wording and the code evidence that may contradict it.]
- [End with: "Reply with the term names to approve, wording changes, `approve all`, or `skip context updates`."]
- [If no candidates: "No candidate CONTEXT.md term updates found."]

## 7. Risks, Gaps, And Recommended Next Checks

- [Risk, ambiguity, dead code, missing test, or unclear owner.]
- [Recommended next check.]
- [State what could not be verified.]

## 8. Validation Performed

- [Pass 1: code/tests/docs/configs/context/issues/history checked.]
- [Pass 2: aliases/reverse lookups/contradictions/stale assumptions checked.]
- [Common mistake check: stale discovery files, docs-over-code, unbounded issue scans, symbol dumps, product-discovery drift.]
- [State whether broad GitHub issue scanning was approved, bounded by context, skipped, or unavailable.]

## 9. Suggested Next Skills (Optional)

- [/skill-name: reason tied to this report.]
- [Prefer adjacent workflow steps; include only 1-6.]
- [Examples: `/feature-prompt` to frame a change request, `/diagnosing-bugs` when a reproducible bug is identified.]
```

When the trace leaves decisions unresolved that gate the scope — you cannot yet
state the destination and every open question sharply — suggest `/wayfinder`
instead of `/feature-prompt`. That is fog, and a PR-sized prompt cannot be
written through it.

## Evidence Style

Prefer concise evidence bullets:

```markdown
- `apps/admin/src/routes/users.ts`: defines the route.
- `packages/auth/src/session.ts`: validates the session before the route runs.
- `apps/admin/src/routes/users.test.ts`: covers the disabled-user case.
- GitHub issue `#123`: records the requested behavior and acceptance criteria.
- Commit `abc1234` from 2026-04-12: introduced the feature flag.
```

## Checklist

Before delivering the report:

- [ ] Read-only held — `git status` shows no files created or modified by this discovery
- [ ] Every factual claim in sections 1–8 carries a citation (file:line/symbol, route, command output, issue, or commit)
- [ ] All nine sections present in order — or Quick trace declared, with sections 1–3 and 8 emitted and the rest marked N/A
- [ ] Section 6 ends with the four-option approval ask as templated in the Output Format, or the no-candidates line
- [ ] Section 8 lists only checks actually run, with the commands named; anything skipped is stated
- [ ] Report delivered in chat; no discovery file written

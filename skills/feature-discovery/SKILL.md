---
name: feature-discovery
description: Use when the user asks to investigate, audit, trace, or explain how a feature, issue, module, workflow, API, config, or behavior works across one or more codebase projects. Saves the full discovery report under docs/discovery and surfaces code-discovered domain terms that may be missing from or stale in CONTEXT.md so the user can approve follow-up context updates.
---

# Feature Discovery

## Purpose

Perform a read-only discovery pass over one or more projects. Explain what the requested topic does, how it works, where it is used, and why it may have been needed. Save the full discovery report as a markdown file under `<artifacts-root>/docs/discovery/`.

Use this skill for prompts shaped like:

```markdown
Projects Affected: [Project Code], [Project Code]

What:
[FEATURE / ISSUE / BEHAVIOR / MODULE / WORKFLOW]
```

## Rules

- Stay read-only during discovery. Do not edit code, config, docs, memory, ADRs, prompts, issues, or generated artifacts while discovering. The only allowed filesystem write without separate approval is the final discovery report under `<artifacts-root>/docs/discovery/`.
- `CONTEXT.md` edits and any artifact edits beyond the saved discovery report are separate follow-up actions. Before editing, show the exact file(s), proposed text or section changes, and reason. Only edit after explicit approval.
- Prefer CLI tools over MCP for codebase evidence.
- Use `rg` first for text search.
- Use `git`, `git grep`, `find`, `gh`, package metadata, local docs, issues, and tests as needed.
- Keep discovery scope thin. If intake spans many workflows or projects, split into slices and discover the first slice before expanding.
- Keep the human in charge. Discovery questions are for blocking clarifications only, not open-ended interrogation.
- Prefer code-as-source-of-truth over prose docs when evidence conflicts.
- When the runtime supports subagents and the user has allowed them, act as the orchestrator: dispatch read-only **Explorer** lanes for independent codebase discovery and **Researcher** lanes for external docs or dependency source. Use local subagents only — never cloud agents. See the `agents-md` `tool-calling.md` reference for the role-to-mechanism map per runtime.
- Run independent Explorer/Researcher lanes in parallel — by project, module, or evidence stream — and push long scans to local background where the runtime supports it.
- Keep the main session responsible for synthesis, evidence quality, uncertainty calls, conflict resolution, and final reporting. Subagents return summaries, not raw transcripts.
- Do not run `git fetch`, `git pull`, installs, migrations, or destructive commands.
- Scan the codebase before using git history.
- Do not read `docs/discovery/` files unless the user explicitly asks you to use a specific discovery report or discovery history. Discovery files can be stale; prefer current code, ADRs, CONTEXT, issues, tests, and fresh search.
- Check available internal memory before doing broad GitHub issue discovery. Internal memory can include conversation memory, AGENTS.md, `<artifacts-root>/CONTEXT.md`, **`<repo-root>/MEMORY.md`** (active repo from Project Matrix + cwd), ADRs under `<artifacts-root>/docs/adr/`, local docs, local issue caches, prior issue references, or project-specific memory files. When present (optional [Understand-Anything](https://github.com/Lum1104/Understand-Anything) companion), also check `<active-repo-root>/.understand-anything/knowledge-graph.json` and `<artifacts-root>/docs/.understand-anything/knowledge-graph.json` (docs / cross-repo). If a graph exists, prefer `/understand-chat` or reading the graph before broad `rg` sweeps.
- If external dependency internals are critical and local evidence is insufficient, optionally fetch targeted dependency source with `opensrc` and cite concrete files/functions. Keep fetch scope minimal.
- If internal memory identifies relevant GitHub issue numbers, URLs, titles, labels, milestones, or search terms, read all GitHub issues in that bounded set.
- If no reliable internal memory exists for the topic, ask the user for approval before scanning broadly across GitHub issues. Explain that reading all related issues can take a long time.
- If approval for broad GitHub issue scanning is not granted, continue with code, docs, tests, local memory, and git history, and state that broad GitHub issue scanning was skipped.
- Review git commits only when code scanning does not explain the topic clearly.
- If git history is needed, review only the last 2 months.
- Back concrete claims with file paths, symbols, commands, tests, docs, GitHub issues, or commits.
- Separate confirmed facts from inference.
- Do not invent memory or rationale.
- When code exploration reveals domain terms, compare them with available `CONTEXT.md` content and flag missing, stale, renamed, overloaded, or ambiguous terms.
- Candidate context terms must be meaningful to product or domain experts: roles, workflows, states, business rules, events, integrations, user-facing concepts, or project-specific names. Skip generic programming terms, helper names, low-level class names, and package names unless they carry domain meaning.
- Classify unresolved unknowns by fidelity:
  - Grillable (low fidelity): keep as concise open decisions for `/feature-prompt` or `/grill-with-docs`.
  - Ungrillable (high fidelity, "needs to feel/see it"): recommend `/handoff` + `/prototype` instead of speculative discovery.
- Flag duplication risks explicitly: when similar behavior exists in multiple paths, call out likely seam reuse opportunities for the next planning step.
- Treat `~120K` tokens as a context-budget caution point for planning-heavy sessions. If unresolved core unknowns remain near this point, stop and recommend scope split or handoff.
- Do not give the final discovery report until findings have passed two validation scans.
- Save the full final report before responding. Use `<artifacts-root>/docs/discovery/DD-MM-YYYY-<PROJECT-CODE>-<slug>.md`. Use the local current date. Use the full Project Matrix code. For multi-project discovery, join project codes with `--` in request order. Slug the topic in lowercase kebab case.
- End the saved report with `Suggested next skills (optional)` containing 1-3 recommendations. Keep them advisory only (no gating) and base them on findings plus the workspace workflow. Suggest `/memory-steward` when repo `MEMORY.md` has a non-empty promotion queue, exceeds ~300 lines, or discovery surfaced durable prefs worth persisting. When discovery narrows to one module or file, suggest `/understand-explain <file>` if UA is installed and a graph exists.

## Workflow

1. Parse the request:
   - Identify project codes from `Projects Affected`.
   - Identify the topic from `What`.
   - Note explicit constraints, dates, branches, modules, or terms.

2. Locate project roots:
   - Find relevant git roots and package/app boundaries.
   - Map project codes to folders by repo names, package metadata, READMEs, config, or naming conventions.
   - If a project code cannot be mapped, state that early and continue best-effort.

3. Discover the topic:
   - Search exact terms from `What`.
   - Search likely aliases, route names, component names, API paths, config keys, env vars, table names, filenames, and test names.
   - Trace definitions to callers.
   - Trace user-facing flows from entry points to lower-level services.
   - Include tests, docs, configs, migrations, routes, background jobs, and feature flags when relevant.
   - If using Explorer/Researcher lanes, split work by project, module, or evidence type and require each lane to return file paths, symbols, commands, and uncertainty (summaries, not raw transcripts).

4. Discover related memory and GitHub issues:
   - First inspect available internal memory for issue references or topic clues. Search AGENTS.md, `<artifacts-root>/CONTEXT.md`, active **`<repo-root>/MEMORY.md`**, ADRs under `<artifacts-root>/docs/adr/`, docs, local issue folders, prior prompt context, and memory files.
   - If memory gives a bounded GitHub issue set, read every issue in that set with `gh issue view` or equivalent.
   - If memory gives reliable labels, milestones, titles, or exact search terms, use them to perform a bounded GitHub issue search and read every matching issue that is plausibly related.
   - If memory does not exist or is too vague to bound the search, pause and ask the user to approve a broad GitHub issue scan before running it.
   - Summarize which issues were read, which were excluded as unrelated, and whether broad scanning was skipped.

5. Track candidate `CONTEXT.md` terms:
   - Locate the relevant `CONTEXT.md` by checking the project root, workspace root, root `CONTEXT-MAP.md`, and nearby docs.
   - Compare discovered domain terms against existing context language.
   - For each candidate, capture:
     - **Term:** the current code or product term.
     - **Suggested action:** add, clarify, rename, deprecate, or ask user.
     - **Short description:** one sentence grounded in observed code behavior.
     - **Evidence:** file paths, symbols, routes, configs, tests, issues, or docs.
     - **Why it matters:** how missing or stale context could confuse future planning or implementation.
   - Prefer a small, high-confidence list over a broad glossary dump.
   - If no relevant `CONTEXT.md` exists, still report candidate terms and recommend creating or locating the context file before editing.

6. Use git history only if needed:
   - Limit to the last 2 months.
   - Look for commits touching discovered files or mentioning the topic.
   - Use commit history to explain why or when behavior changed, not as the primary source of truth.

7. Validate findings twice:
   - First pass: cross-check the main explanation against code, tests, docs, configs, usage sites, internal memory, related GitHub issues, and git history where used.
   - Second pass: repeat the scan with aliases and reverse lookups, re-open the strongest evidence, look for contradictory code paths, issue comments, docs, commits, and stale assumptions, then tighten or downgrade claims.
   - Validate candidate context terms against `CONTEXT.md` and the strongest code evidence before presenting them.
   - Mark dead code, unclear ownership, missing tests, contradictory evidence, skipped issue scans, stale context terms, and unverified assumptions.
   - Avoid broad claims when evidence is partial.
   - Keep a short validation note for the final report that states what was checked in each pass.

8. Save the discovery report:
   - Resolve `<artifacts-root>` from `AGENTS.md` / Project Matrix rules: code-workspace directory first, then context root, then repo root.
   - Ensure `<artifacts-root>/docs/discovery/` exists.
   - Write the full report markdown using this filename shape: `DD-MM-YYYY-<PROJECT-CODE>-<slug>.md`.
   - Use `date +%d-%m-%Y` for `DD-MM-YYYY` when available.
   - Use the full Project Matrix code. For multi-project discovery, join codes with `--` in request order.
   - Slug the topic from `What`: lowercase, ASCII, hyphen-separated, no filler words when obvious.
   - If a file with the same name already exists, append `-2`, `-3`, etc. Do not overwrite.
   - The saved file must contain the complete report, including validation and suggested next skills.
   - In chat, include `Saved: <path>` and a concise summary. Do not claim completion if the file write failed.

9. Update `CONTEXT.md` or other artifacts only after approval:
   - After the report, if terms or artifacts need updates, show the exact target path(s), proposed text/section changes, and reason for each change.
   - Wait for explicit approval before editing.
   - If the user approves terms, inspect the target `CONTEXT.md` structure and preserve its style.
   - Apply only the approved additions, clarifications, renames, deprecations, or artifact edits.
   - Keep descriptions short and evidence-backed. Do not add implementation-only symbols as domain language.
   - Report exactly which terms changed and which file was edited.
   - If the user approves with edits to wording, use the user's wording unless it conflicts with code evidence; if it conflicts, explain the mismatch before editing.

## Search Defaults

Adapt commands to the repo. Keep command output summarized in the final report.

```bash
rg -n "exact topic|likely alias|route|config_key" .
find . -maxdepth 4 \( -name package.json -o -name README.md -o -name .git \)
git grep -n "term"
gh issue view <issue-number> --comments
gh issue list --state all --search "exact topic OR likely alias"
git log --since="2 months ago" --oneline --all -- <relevant-path>
```

## Output Format

Use this structure exactly for the saved report. The chat response may be shorter, but it must include `Saved: <path>` and state if any validation or issue scan was skipped.

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

## 5. Why It Was Needed / Memory

- [Use conversation memory, local docs, comments, issues, or recent commits if available.]
- [If not found: "No reliable rationale found in available memory, docs, comments, or recent git history."]

## 6. Candidate CONTEXT.md Terms

- [If candidates exist, list each as: `Term` — suggested action; short description; evidence; why it matters.]
- [If existing context may be stale, state the current context wording and the code evidence that may contradict it.]
- [End with: "Reply with the term names to approve, wording changes, or `approve all` if these should be applied to CONTEXT.md."]
- [If no candidates: "No candidate CONTEXT.md term updates found."]

## 7. Risks, Gaps, And Recommended Next Checks

- [Risk, ambiguity, dead code, missing test, or unclear owner.]
- [Recommended next check.]
- [State what could not be verified.]

## 8. Validation Performed

- [Pass 1: code/tests/docs/configs/memory/issues/history checked.]
- [Pass 2: aliases/reverse lookups/contradictions/stale assumptions checked.]
- [State whether broad GitHub issue scanning was approved, bounded by memory, skipped, or unavailable.]

## 9. Suggested Next Skills (Optional)

- [/skill-name: reason tied to this report.]
- [Prefer adjacent workflow steps; include only 1-3.]
- [Examples: `/feature-prompt` to frame a change request, `/diagnose` when a reproducible bug is identified.]
```

## Evidence Style

Prefer concise evidence bullets:

```markdown
- `apps/admin/src/routes/users.ts`: defines the route.
- `packages/auth/src/session.ts`: validates the session before the route runs.
- `apps/admin/src/routes/users.test.ts`: covers the disabled-user case.
- GitHub issue `#123`: records the requested behavior and acceptance criteria.
- Commit `abc1234` from 2026-04-12: introduced the feature flag.
```

## Quality Bar

The final answer should let another engineer understand:

- what the thing is
- what it does
- how it works
- where it is used
- what evidence supports the explanation
- what remains uncertain

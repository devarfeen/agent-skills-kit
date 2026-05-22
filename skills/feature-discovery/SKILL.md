---
name: feature-discovery
description: Use when the user asks to investigate, audit, trace, or explain how a feature, issue, module, workflow, API, config, or behavior works across one or more codebase projects. Also surfaces code-discovered domain terms that may be missing from or stale in CONTEXT.md so the user can approve follow-up context updates.
---

# Feature Discovery

## Purpose

Perform a read-only discovery pass over one or more projects. Explain what the requested topic does, how it works, where it is used, and why it may have been needed.

Use this skill for prompts shaped like:

```markdown
Projects Affected: [Project Code], [Project Code]

What:
[FEATURE / ISSUE / BEHAVIOR / MODULE / WORKFLOW]
```

## Rules

- Stay read-only during discovery. Do not edit files while producing the discovery report.
- `CONTEXT.md` edits are a separate follow-up action. Only update `CONTEXT.md` after the user explicitly approves specific candidate terms or accepts the full candidate list.
- Prefer CLI tools over MCP for codebase evidence, except project memory retrieval via memtrace when available.
- Use `rg` first for text search.
- Use `git`, `git grep`, `find`, `gh`, package metadata, local docs, issues, and tests as needed.
- When the active agent runtime supports sub-agents and the user has allowed them, use explorer agents for independent read-only discovery work.
- Use multiple explorer agents in parallel when projects, modules, or evidence streams can be investigated independently.
- Keep the main session responsible for synthesis, evidence quality, uncertainty calls, and final reporting.
- Do not run `git fetch`, `git pull`, installs, migrations, or destructive commands.
- Scan the codebase before using git history.
- Check available internal memory before doing broad GitHub issue discovery. Internal memory can include conversation memory, AGENTS.md, CONTEXT.md, ADRs under `docs/adr/`, local docs, local issue caches, prior issue references, or project-specific memory files.
- If memtrace MCP tools are available, call `memory_recall` once before broad discovery using the main topic terms. Treat recalled decisions as hints that must still be verified against code.
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
- Do not give the final discovery report until findings have passed two validation scans.

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
   - If using explorer agents, split work by project, module, or evidence type and require each explorer to return file paths, symbols, commands, and uncertainty.

4. Discover related memory and GitHub issues:
   - If memtrace MCP tools exist, run `memory_recall` with topic keywords first and fold high-confidence items into the bounded search set.
   - First inspect available internal memory for issue references or topic clues. Search AGENTS.md, CONTEXT.md, ADRs under `docs/adr/`, docs, local issue folders, prior prompt context, and memory files.
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

8. Update `CONTEXT.md` only after approval:
   - After the report, if the user approves terms, inspect the target `CONTEXT.md` structure and preserve its style.
   - Apply only the approved additions, clarifications, renames, or deprecations.
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

Use this structure exactly.

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

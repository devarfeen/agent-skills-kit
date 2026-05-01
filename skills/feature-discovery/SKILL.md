---
name: feature-discovery
description: Use when the user asks to investigate, audit, trace, or explain how a feature, issue, module, workflow, API, config, or behavior works across one or more codebase projects.
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

- Stay read-only. Do not edit files.
- Prefer CLI tools over MCP.
- Use `rg` first for text search.
- Use `git`, `git grep`, `find`, package metadata, local docs, and tests as needed.
- Do not run `git fetch`, `git pull`, installs, migrations, or destructive commands.
- Scan the codebase before using git history.
- Review git commits only when code scanning does not explain the topic clearly.
- If git history is needed, review only the last 2 months.
- Back concrete claims with file paths, symbols, commands, tests, docs, or commits.
- Separate confirmed facts from inference.
- Do not invent memory or rationale.

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

4. Use git history only if needed:
   - Limit to the last 2 months.
   - Look for commits touching discovered files or mentioning the topic.
   - Use commit history to explain why or when behavior changed, not as the primary source of truth.

5. Validate findings:
   - Cross-check code against tests, docs, configs, and usage sites.
   - Mark dead code, unclear ownership, missing tests, contradictory evidence, and unverified assumptions.
   - Avoid broad claims when evidence is partial.

## Search Defaults

Adapt commands to the repo. Keep command output summarized in the final report.

```bash
rg -n "exact topic|likely alias|route|config_key" .
find . -maxdepth 4 \( -name package.json -o -name README.md -o -name .git \)
git grep -n "term"
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

## 6. Risks, Gaps, And Recommended Next Checks

- [Risk, ambiguity, dead code, missing test, or unclear owner.]
- [Recommended next check.]
- [State what could not be verified.]
```

## Evidence Style

Prefer concise evidence bullets:

```markdown
- `apps/admin/src/routes/users.ts`: defines the route.
- `packages/auth/src/session.ts`: validates the session before the route runs.
- `apps/admin/src/routes/users.test.ts`: covers the disabled-user case.
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

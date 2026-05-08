# Agent Workflow Guide

This guide describes how to combine skills from this kit and other skill sets to move from idea, discovery, or manual work to shipped code and release notes.

It is not a strict state machine, but it behaves like one: each step has an entry condition, an output, and a decision about where to go next. The workflow works best when you do not skip context-building steps.

## Credits And Provenance

This workflow is a local orchestration guide for this repository, with credit to
the upstream authors whose skills and ideas it combines.

- Local workflow and repo-specific skills are authored and maintained by Arfeen
  Arif. Git history shows this guide was added in commit `593eac3`, after the
  repo's release-notes, feature-discovery, feature-prompt, feature-prompt-full
  (now deprecated), agents-md, and ubiquitous-language (now deprecated) skills
  were added.
- `/agents-md` includes four non-negotiable behavioral principles adapted from
  Forrest Chang's Karpathy-inspired `CLAUDE.md` guidelines:
  https://github.com/forrestchang/andrej-karpathy-skills/blob/main/CLAUDE.md
  The upstream repository is MIT licensed.
- `/ubiquitous-language` (deprecated, kept in `skills/` for reference only) is
  based on Matt Pocock's deprecated `ubiquitous-language` skill, MIT License,
  Copyright 2026 Matt Pocock:
  https://github.com/mattpocock/skills/blob/main/ubiquitous-language/SKILL.md
  Domain-language sharpening is now covered by `/grill-with-docs`, which
  updates `CONTEXT.md` and ADRs inline as decisions crystallise.
- The core prompt, grill, PRD, issue, TDD, diagnosis, triage, and architecture
  workflow uses companion skills from Matt Pocock's skills repo:
  https://github.com/mattpocock/skills
- `/caveman` is credited to Julius Brussee:
  https://github.com/JuliusBrussee/caveman
  Generated `AGENTS.md` files invoke caveman at intensity `full` as a
  non-negotiable rule for chat output only — never for code, docs, PRDs,
  release notes, PR bodies, or any persisted artifact.
- `/ship-pr` is credited to AgentSystemLabs' `agentsystem-essentials` skills:
  `npx skills add https://github.com/AgentSystemLabs/essentials/tree/main/plugins/agentsystem-essentials/skills/ship-pr --skill ship-pr`
- `/skill-creator` is credited to Anthropic's public skills repository:
  https://github.com/anthropics/skills/tree/main/skills/skill-creator
- `/agent-browser`, the `skills` CLI, `find-skills`, and Vercel React/React
  Native best-practice skills are credited to Vercel Labs:
  https://github.com/vercel-labs/agent-browser
  https://github.com/vercel-labs/skills
  https://github.com/vercel-labs/agent-skills
- `/sentry` refers to Sentry's CLI for developers and agents:
  https://cli.sentry.dev/

## First-Time Setup

Run this once per workspace, then refresh when the workspace structure changes.

```text
/agents-md
```

`/agents-md` creates the workspace anchor: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, project codes, paths, tech stacks, and the project matrix. Other skills should use those project codes.

Domain-language sharpening is no longer a separate setup step. `/grill-with-docs` captures terminology, ambiguities, and decisions inline in `CONTEXT.md` and ADRs as the conversation surfaces them.

## Choosing A Starting Point

| Situation | Start With | Why |
| --- | --- | --- |
| New workspace or unclear project codes | `/agents-md` | Establishes project names, codes, paths, and canonical agent instructions. |
| Domain terms are unclear | `/grill-with-docs` | Sharpens terminology against `CONTEXT.md` and ADRs as part of grilling. |
| Existing behavior is unclear | `/feature-discovery` | Produces a read-only explanation before planning changes. |
| Rough feature idea | `/feature-prompt` | Creates a focused implementation prompt; you trigger `/grill-with-docs`, `/to-prd`, `/to-issues`, `/triage`, and `/tdd` manually as the work progresses. |
| Bug with unknown cause | `/diagnose` | Drives root-cause analysis before patching. |
| Single decision needs interrogating in isolation | `/grill-me` | Standalone narrow-scope clarification interview — not part of any feature chain. |
| Completed work needs a PR | `/ship-pr` | Packages changes into commits and a PR. |
| Only stakeholder notes are needed | `/release-notes` | Produces PM-friendly release notes saved to `docs/adr/`. |
| Need a missing capability | `/find-skills` | Looks for skills from other people or ecosystems. |

## Core Progression

Use this as the default chain for product work that should produce a spec, issues, implementation, PR, and release notes.

```text
/agents-md
-> /feature-discovery
-> /feature-prompt
-> /grill-with-docs
-> /to-prd
-> /to-issues
-> /triage
-> /tdd
-> /ship-pr
-> /release-notes
```

The setup step can be skipped when `AGENTS.md` is already current. `/grill-with-docs` handles domain-language sharpening inline against `CONTEXT.md` and ADRs. Each step is triggered manually — there is no auto-chain.

## Triage Gate

`/to-issues` auto-applies the `needs-triage` label to every issue it creates. `/triage` is the manual gate that promotes those issues to `ready-for-agent` and posts an **Agent Brief** comment — the durable, behavioral contract the implementing agent works from. `/tdd` does not enforce this gate; the precondition is convention, not tooling. Treat `/triage` as mandatory between `/to-issues` and `/tdd`.

## Workflow Gates

Think of each step as a gate. Move forward only when the output is good enough for the next skill.

| Gate | Skill | Output | Continue When |
| --- | --- | --- | --- |
| Workspace | `/agents-md` | `AGENTS.md`, shims, project matrix | Project codes and paths are stable. |
| Discovery | `/feature-discovery` | Evidence-backed feature report | Current behavior and risks are understood. |
| Prompt | `/feature-prompt` | Final implementation prompt | User has reviewed the prompt. |
| Grill | `/grill-with-docs` | Challenged assumptions and resolved questions against domain language and ADRs | Major ambiguities are resolved or deferred explicitly. |
| PRD | `/to-prd` | Product requirements/spec | Problem, solution, stories, decisions, tests, and scope are clear. |
| Issues | `/to-issues` | Vertical slices labeled `needs-triage` | Each issue can be implemented independently. |
| Triage | `/triage` | Issue at `ready-for-agent` with Agent Brief comment | Category and state clear; Agent Brief is testable. |
| Build | `/tdd` | Tested implementation | Tests pass or blocker is documented. |
| Debug | `/diagnose` | Root cause and fix path | Cause is known and fix is scoped. |
| Ship | `/ship-pr` | Branch, commits, PR body | PR is review-ready. |
| Release | `/release-notes` | PM-friendly notes | Release notes saved to `docs/adr/NNNN-<slug>-release-notes.md`. |

## Feature Development

Use this for new user-facing or workflow-changing features. Trigger each step manually — none of these skills auto-chain into the next.

```text
/feature-prompt
-> /grill-with-docs
-> /to-prd
-> /to-issues
-> /triage
-> /tdd
-> /ship-pr
-> /release-notes
```

`/feature-prompt` produces a reviewed, implementation-ready prompt and saves it to `docs/adr/NNNN-<slug>-prompt.md`. The next step is always `/grill-with-docs`, which stress-tests the prompt against terminology, ADRs, and the codebase.

Add `/feature-discovery` before `/feature-prompt` when the feature modifies existing behavior, or `/diagnose` when it grows out of an unexplained bug.

## Change Requests

Use this when the request changes an already-planned feature, PRD, or issue list.

```text
/feature-discovery
-> /feature-prompt
-> /grill-with-docs
-> /to-prd
-> /to-issues
-> /triage
-> /tdd
```

`/grill-with-docs` always follows `/feature-prompt`. If you need to understand existing behavior first, prepend `/feature-discovery`; if a bug is in scope, prepend `/diagnose`.

`/grill-me` is **not** part of this chain. It is a standalone narrow-scope clarification interview — useful when you want to interrogate a single decision or assumption in isolation, outside any feature-development workflow.

## Bug Fixes

Use this when behavior is broken and the cause is not obvious.

```text
/feature-discovery
-> /diagnose
-> /feature-prompt
-> /grill-with-docs
-> /tdd
-> /ship-pr
-> /release-notes
```

Use `/feature-discovery` to understand where the behavior lives. Use `/diagnose` when tests, logs, or runtime behavior are confusing. Use `/tdd` to reproduce the bug with a failing test before fixing it when possible.

For production incidents, add `/sentry` before `/diagnose` when Sentry has the relevant issue.

## Multiple-Project Changes

Use this when a workflow crosses API, web, mobile, jobs, database, or service boundaries.

```text
/agents-md
-> /feature-discovery
-> /feature-prompt
-> /grill-with-docs
-> /to-prd
-> /to-issues
-> /triage
-> /tdd
```

Rules:

- Use project codes from `AGENTS.md` in every prompt.
- Ask `/feature-discovery` to inspect each affected project.
- Let `/to-issues` split work into vertical slices across projects.
- Avoid one issue per layer unless the work truly cannot be shipped vertically.
- Use explorer sub-agents when the runtime supports them and projects can be investigated independently.

## Manual Work Or Direct Coding

Use this when you already know the change and do not need a PRD.

```text
/feature-prompt
-> /grill-with-docs
-> /tdd
```

For very small edits, you can skip `/feature-prompt` and use direct coding, but keep the same gates mentally:

1. State the intended change.
2. Make the smallest edit.
3. Run the smallest meaningful verification.
4. Summarize files changed and remaining risk.

Use `/agents-md` and `CONTEXT.md` (plus any ADRs) as context even for manual work.

## Release Notes Only

Use this when the work is already done and stakeholders need a summary.

```text
/release-notes
```

Useful prompts:

- `Generate release notes for today`
- `Create release notes for 11 March 2026`
- `Summarize this development session`
- `Write release notes for the scanner reliability work`

`/release-notes` should use git history, current diffs, and project codes from `AGENTS.md` when available.

## Discovery Only

Use this when you only need to understand a feature, issue, module, workflow, API, config, or behavior.

```text
/feature-discovery
```

Good inputs:

```markdown
Projects Affected: PARTNERS-API, APP-PARTNERS

What:
Delivery Note upload handling
```

Use this before planning when the codebase is unfamiliar or when a change request depends on current behavior.

## Skill Combinations

### With Docs And Domain Language

```text
/grill-with-docs
```

Use this when terminology, ADRs, or `CONTEXT.md` matter — it sharpens language and updates documentation inline as decisions crystallise.

### With Browser Testing

```text
/tdd
-> /agent-browser
```

Use this when a web flow needs visual or interactive verification.

### With Production Errors

```text
/sentry
-> /diagnose
-> /tdd
```

Use this when Sentry can explain stack traces, affected users, or suspected root cause.

### With Missing Skills

```text
/find-skills
-> install relevant skill
-> continue workflow
```

Use this when the work needs a specialized capability outside this kit.

## Recovery Loops

- If the prompt is vague, go back to `/feature-prompt`.
- If the grill finds unresolved domain language, stay in `/grill-with-docs` and let it update `CONTEXT.md` / ADRs inline.
- If the PRD exposes missing behavior context, go back to `/feature-discovery`.
- If issues are too large, go back to `/to-issues`.
- If an issue lacks an Agent Brief or its acceptance criteria are vague, go back to `/triage`.
- If implementation fails unexpectedly, go to `/diagnose`, then return to `/tdd`.
- If release notes are too technical, rerun `/release-notes` with PM/QA audience emphasis.

## Minimal Chains

| Use Case | Chain |
| --- | --- |
| Full feature | `/feature-prompt` -> `/grill-with-docs` -> `/to-prd` -> `/to-issues` -> `/triage` -> `/tdd` -> `/ship-pr` -> `/release-notes` |
| Small feature | `/feature-prompt` -> `/grill-with-docs` -> `/tdd` |
| Bug fix | `/feature-discovery` -> `/diagnose` -> `/tdd` |
| Multi-project change | `/agents-md` -> `/feature-discovery` -> `/feature-prompt` -> `/grill-with-docs` -> `/to-prd` -> `/to-issues` -> `/triage` -> `/tdd` |
| Change request | `/feature-discovery` -> `/feature-prompt` -> `/grill-with-docs` -> `/to-prd` -> `/to-issues` |
| Narrow standalone clarification | `/grill-me` (single decision in isolation; not part of any feature chain) |
| Release notes only | `/release-notes` |
| Manual coding | Read `AGENTS.md` and `CONTEXT.md` (plus ADRs), make the smallest change, verify, summarize |

## Practical Default

When unsure, start with:

```text
/feature-discovery
-> /feature-prompt
-> /grill-with-docs
```

That gives the agent enough code context, a precise prompt, and a challenged plan before the PRD or implementation starts. Trigger each step manually.

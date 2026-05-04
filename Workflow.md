# Agent Workflow Guide

This guide describes how to combine skills from this kit and other skill sets to move from idea, discovery, or manual work to shipped code and release notes.

It is not a strict state machine, but it behaves like one: each step has an entry condition, an output, and a decision about where to go next. The workflow works best when you do not skip context-building steps.

## Credits And Provenance

This workflow is a local orchestration guide for this repository, with credit to
the upstream authors whose skills and ideas it combines.

- Local workflow and repo-specific skills are authored and maintained by Arfeen
  Arif. Git history shows this guide was added in commit `593eac3`, after the
  repo's release-notes, feature-discovery, feature-prompt,
  feature-prompt-full, agents-md, and ubiquitous-language skills were added.
- `/agents-md` includes four non-negotiable behavioral principles adapted from
  Forrest Chang's Karpathy-inspired `CLAUDE.md` guidelines:
  https://github.com/forrestchang/andrej-karpathy-skills/blob/main/CLAUDE.md
  The upstream repository is MIT licensed.
- `/ubiquitous-language` is based on Matt Pocock's deprecated
  `ubiquitous-language` skill, MIT License, Copyright 2026 Matt Pocock:
  https://github.com/mattpocock/skills/blob/main/ubiquitous-language/SKILL.md
- The core prompt, grill, PRD, issue, TDD, diagnosis, triage, architecture, and
  compression workflow uses companion skills from Matt Pocock's skills repo:
  https://github.com/mattpocock/skills
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

Run these once per workspace, then refresh them when the workspace structure or domain language changes.

```text
/agents-md
-> /ubiquitous-language
```

`/agents-md` creates the workspace anchor: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, project codes, paths, tech stacks, and the project matrix. Other skills should use those project codes.

`/ubiquitous-language` creates `UBIQUITOUS_LANGUAGE.md`, which captures domain terms, short codes, operational language, and ambiguities. Use it when terms like `DN`, `Warehouse On Site`, or `Files` have business meaning.

## Choosing A Starting Point

| Situation | Start With | Why |
| --- | --- | --- |
| New workspace or unclear project codes | `/agents-md` | Establishes project names, codes, paths, and canonical agent instructions. |
| Domain terms are unclear | `/ubiquitous-language` | Gives later prompts and specs the right business language. |
| Existing behavior is unclear | `/feature-discovery` | Produces a read-only explanation before planning changes. |
| Rough feature idea | `/feature-prompt` | Creates a focused implementation prompt and then asks you to pass it to `/grill-me`. |
| Full feature lifecycle | `/feature-prompt-full` | Entry point for the full `/grill-with-docs` workflow: prompt, grill, PRD, issues, TDD. |
| Bug with unknown cause | `/diagnose` | Drives root-cause analysis before patching. |
| Completed work needs a PR | `/ship-pr` | Packages changes into commits and a PR. |
| Only stakeholder notes are needed | `/release-notes` | Produces PM-friendly changelog/session notes. |
| Need a missing capability | `/find-skills` | Looks for skills from other people or ecosystems. |

## Core Progression

Use this as the default chain for product work that should produce a spec, issues, implementation, PR, and release notes.

```text
/agents-md
-> /ubiquitous-language
-> /feature-discovery
-> /feature-prompt-full
-> /grill-with-docs
-> /to-prd
-> /to-issues
-> /triage
-> /tdd
-> /ship-pr
-> /release-notes
```

The first two setup steps can be skipped only when `AGENTS.md` and `UBIQUITOUS_LANGUAGE.md` are already current.

## Triage Gate

`/to-issues` auto-applies the `needs-triage` label to every issue it creates. `/triage` is the manual gate that promotes those issues to `ready-for-agent` and posts an **Agent Brief** comment — the durable, behavioral contract the implementing agent works from. `/tdd` does not enforce this gate; the precondition is convention, not tooling. Treat `/triage` as mandatory between `/to-issues` and `/tdd`.

## Workflow Gates

Think of each step as a gate. Move forward only when the output is good enough for the next skill.

| Gate | Skill | Output | Continue When |
| --- | --- | --- | --- |
| Workspace | `/agents-md` | `AGENTS.md`, shims, project matrix | Project codes and paths are stable. |
| Language | `/ubiquitous-language` | `UBIQUITOUS_LANGUAGE.md` | Terms, short codes, and ambiguities are captured. |
| Discovery | `/feature-discovery` | Evidence-backed feature report | Current behavior and risks are understood. |
| Prompt | `/feature-prompt` or `/feature-prompt-full` | Final implementation prompt | User has reviewed the prompt. |
| Grill | `/grill-me` or `/grill-with-docs` | Challenged assumptions and resolved questions | Major ambiguities are resolved or deferred explicitly. |
| PRD | `/to-prd` | Product requirements/spec | Problem, solution, stories, decisions, tests, and scope are clear. |
| Issues | `/to-issues` | Vertical slices labeled `needs-triage` | Each issue can be implemented independently. |
| Triage | `/triage` | Issue at `ready-for-agent` with Agent Brief comment | Category and state clear; Agent Brief is testable. |
| Build | `/tdd` | Tested implementation | Tests pass or blocker is documented. |
| Debug | `/diagnose` | Root cause and fix path | Cause is known and fix is scoped. |
| Ship | `/ship-pr` | Branch, commits, PR body | PR is review-ready. |
| Release | `/release-notes` | PM-friendly notes | Changelog/session summary is saved. |

## Feature Development

Use this for new user-facing or workflow-changing features.

```text
/feature-prompt-full
-> /grill-with-docs
-> /to-prd
-> /to-issues
-> /triage
-> /tdd
-> /ship-pr
-> /release-notes
```

Use `/feature-prompt-full` when you want the full use case of the `grill-me` family. It clarifies the feature, asks for approval of the chain, produces a final prompt, then points into `/grill-with-docs`, `/to-prd`, `/to-issues`, and `/tdd`.

Add `/feature-discovery` before it when the feature modifies existing behavior.

## Change Requests

Use this when the request changes an already-planned feature, PRD, or issue list.

```text
/feature-discovery
-> /feature-prompt
-> /grill-me
-> /to-prd
-> /to-issues
-> /triage
-> /tdd
```

If the change is broad or touches multiple projects, use `/feature-prompt-full` and `/grill-with-docs` instead of `/feature-prompt` and `/grill-me`.

Decision rule:

- Use `/feature-prompt` for narrow implementation prompts.
- Use `/feature-prompt-full` for changes that need the full prompt -> grill -> PRD -> issues -> TDD chain.

## Bug Fixes

Use this when behavior is broken and the cause is not obvious.

```text
/feature-discovery
-> /diagnose
-> /feature-prompt
-> /grill-me
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
-> /feature-prompt-full
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
-> /grill-me
-> /tdd
```

For very small edits, you can skip `/feature-prompt` and use direct coding, but keep the same gates mentally:

1. State the intended change.
2. Make the smallest edit.
3. Run the smallest meaningful verification.
4. Summarize files changed and remaining risk.

Use `/agents-md` and `UBIQUITOUS_LANGUAGE.md` as context even for manual work.

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
/ubiquitous-language
-> /grill-with-docs
```

Use this when terminology, ADRs, or `CONTEXT.md` matter.

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

- If the prompt is vague, go back to `/feature-prompt` or `/feature-prompt-full`.
- If the grill finds unresolved domain language, go back to `/ubiquitous-language`.
- If the PRD exposes missing behavior context, go back to `/feature-discovery`.
- If issues are too large, go back to `/to-issues`.
- If an issue lacks an Agent Brief or its acceptance criteria are vague, go back to `/triage`.
- If implementation fails unexpectedly, go to `/diagnose`, then return to `/tdd`.
- If release notes are too technical, rerun `/release-notes` with PM/QA audience emphasis.

## Minimal Chains

| Use Case | Chain |
| --- | --- |
| Full feature | `/feature-prompt-full` -> `/grill-with-docs` -> `/to-prd` -> `/to-issues` -> `/triage` -> `/tdd` -> `/ship-pr` -> `/release-notes` |
| Small feature | `/feature-prompt` -> `/grill-me` -> `/tdd` |
| Bug fix | `/feature-discovery` -> `/diagnose` -> `/tdd` |
| Multi-project change | `/agents-md` -> `/feature-discovery` -> `/feature-prompt-full` -> `/grill-with-docs` -> `/to-prd` -> `/to-issues` -> `/triage` -> `/tdd` |
| Change request | `/feature-discovery` -> `/feature-prompt` -> `/grill-me` -> `/to-prd` -> `/to-issues` |
| Release notes only | `/release-notes` |
| Manual coding | Read `AGENTS.md` and `UBIQUITOUS_LANGUAGE.md`, make the smallest change, verify, summarize |

## Practical Default

When unsure, start with:

```text
/feature-discovery
-> /feature-prompt-full
-> /grill-with-docs
```

That gives the agent enough code context, a precise prompt, and a challenged plan before the PRD or implementation starts.

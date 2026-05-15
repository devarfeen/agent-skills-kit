# Agent Workflow Guide

Combine skills from this kit and the wider ecosystem to move from idea to shipped code and release notes. Prioritize context, evidence, and task isolation.

## Credits And Provenance

- **Local Skills:** Authored by Arfeen Arif. Combines original logic with ecosystem companion skills.
- **Matt Pocock:** Source for `/caveman`, `/grill-with-docs`, `/grill-me`, `/to-prd`, `/to-issues`, `/tdd`, `/diagnose`, `/triage`, `/improve-codebase-architecture`, `/zoom-out`, `/prototype`, and `/handoff`.
- **Forrest Chang:** Seeding logic for `/agents-md` non-negotiable principles.
- **Anthropic:** Source for `/skill-creator`.
- **Vercel Labs:** Source for `/agent-browser`, `skills` CLI, and React/React Native best practices.

## Non-Negotiable Core (Spartan Rules)

Every session follows these 13 rules (enforced by `AGENTS.md`):

1. **Invoke Caveman First:** Immediate `/caveman` (or tool call) is mandatory.
2. **Evidence Before Claim:** No status claims without raw command output.
3. **Task Isolation:** Fresh context per independent task. No history bloat.
4. **Goal-Driven Execution:** Empirical proof only. Bug fixes require Red-Green-Refactor.
5. **Surgical Minimalism:** Match style. Min code. No adjacent cleanup.
6. **Systematic Debugging:** Trace root cause. No symptom patches or hacks.
7. **Think & Ask:** Stop at ambiguity. Surface tradeoffs. No guessing.
8. **Read Before Write:** Map exports, callers, and utils before editing.
9. **Token Guardrails:** Treat budgets as hard limits. Anchor and restart if near breach.
10. **Surface Conflicts:** Resolve pattern clashes explicitly. No silent forks.
11. **Conventions Over Taste:** Local idioms beat personal preference.
12. **State Anchoring:** Continuously report `[verified]`, `[current]`, and `[todo]`.
13. **Fail Loud:** No silent skips. Completion requires full verification.

## First-Time Setup

1. **`/agents-md`**: Creates `AGENTS.md`, shims, and project matrix.
2. **`/setup-matt-pocock-skills`**: Configures tracker, labels, and `## Agent skills` block.

## Choosing A Starting Point

| Situation | Start With | Why |
| :--- | :--- | :--- |
| New Workspace | `/agents-md` | Establish codes, paths, and Spartan Rules. |
| Unclear Behavior | `/feature-discovery` | Read-only audit before planning. |
| Rough Idea | `/feature-prompt` | Section-by-section clarification interview. |
| Broken Behavior | `/diagnose` | Systematic root cause analysis. |
| Design Spike | `/prototype` | Validate UI/state before PRD/Issues. |
| Issue Work | `/tdd` | Red-Green-Refactor implementation loop. |
| Session Pause | `/handoff` | Continuation doc for the next agent. |

## Core Progression

```text
/agents-md -> /setup-matt-pocock-skills -> /feature-discovery -> /feature-prompt -> /grill-with-docs -> /to-prd -> /to-issues -> /triage -> /tdd -> /commit-push-pr -> /release-notes
```

## Workflow Gates

| Gate | Skill | Continue When |
| :--- | :--- | :--- |
| Workspace | `/agents-md` | Project codes and Spartan Rules are active. |
| Discovery | `/feature-discovery` | Evidence-backed report explains current behavior. |
| Prompt | `/feature-prompt` | Implementation-ready prompt is reviewed by user. |
| Grill | `/grill-with-docs` | Ambiguities resolved against ADRs and domain language. |
| PRD | `/to-prd` | Spec is clear on problem, solution, and success criteria. |
| Issues | `/to-issues` | Work is split into independently testable vertical slices. |
| Triage | `/triage` | Issue state is clear and Agent Brief is present. |
| Build | `/tdd` | Failure verified (Red), Fix verified (Green). |
| Ship | `/commit-push-*` | Branch pushed and issue/PR linked with test proof. |
| Release | `/release-notes` | PM-friendly summary saved to `docs/adr/`. |

## Recovery Loops

- **Vague Prompt:** Back to `/feature-prompt`.
- **Domain Ambiguity:** Stay in `/grill-with-docs` (updates `CONTEXT.md` inline).
- **Broken Tests:** Stay in `/tdd` or pivot to `/diagnose`.
- **Large Issues:** Back to `/to-issues` for smaller slices.
- **Production Error:** Start with `/sentry` -> `/diagnose`.

## Practical Default

When unsure, run this sequence manually:
1. `/feature-discovery` (Understand)
2. `/feature-prompt` (Plan)
3. `/grill-with-docs` (Challenge)

No auto-chains. Trigger each step based on gate completion.

# Agent Workflow Guide

Combine skills from this kit and the wider ecosystem to move from idea to shipped code and release notes. Prioritize context, evidence, and task isolation.

## Credits And Provenance

- **Local Skills:** Authored by Arfeen Arif. Combines original logic with ecosystem companion skills.
- **Matt Pocock:** Source for `/caveman`, `/grill-with-docs`, `/grill-me`, `/to-prd`, `/to-issues`, `/tdd`, `/diagnose`, `/triage`, `/improve-codebase-architecture`, `/zoom-out`, `/prototype`, and `/handoff`.
- **Forrest Chang:** Seeding logic for `/agents-md` non-negotiable principles.
- **Anthropic:** Source for `/skill-creator`.
- **Vercel Labs:** Source for `/agent-browser`, `skills` CLI, and React/React Native best practices.
- **Cursor:** Cursor CLI / IDE Agent (`agent` command, `/skill-name`, `AGENTS.md` as canonical context, `Task` for subagents). Tool names and permissions: [`skills/agents-md/references/tool-calling.md`](skills/agents-md/references/tool-calling.md). https://cursor.com/docs/cli/overview

## Non-Negotiable Core (Spartan Rules)

Every session follows these 14 rules (enforced by `AGENTS.md`):

1. **Invoke Caveman First:** Immediate `/caveman` (Cursor CLI / IDE, Claude Code) or runtime-native skill call is mandatory.
2. **Evidence Before Claim:** No status claims without raw command output.
3. **Task Isolation:** Fresh context per independent task. Use subagents, agents, workers, or isolated tool passes when work can split without file conflicts.
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
14. **No Project Code Abbreviation:** Use full Project Matrix codes in chat, docs, ADRs, prompts, issues, PRs, commit messages, and code comments. No shorthand.

Operational default: caveman applies to chat output only. Do not caveman-compress code, docs, PRDs, release notes, PR bodies, generated prompts, or persisted artifacts. Use 5th-grade English in chat unless a technical term is required; keep exact terms like `API`, `DB`, `auth`, `null`, `array`, `timeout`, and `race condition`.

Subagent default: before substantial work, split the task into independent lanes. Dispatch fresh agents for research, critique, comparison, risk checks, source checks, outline, terminology, audience fit, codebase search, mapping, test-failure investigation, and review. Main agent owns final judgment. Keep work local when tiny, sequential, tightly coupled, or conflict-prone. If the runtime lacks subagents, use separate focused tool passes. On Cursor CLI / IDE, use the `Task` tool (`explore`, `shell`, `generalPurpose`, or custom `.cursor/agents/`); see [`tool-calling.md`](skills/agents-md/references/tool-calling.md).

## First-Time Setup

1. **`/agents-md`**: Creates `AGENTS.md`, shims, and project matrix.
2. **`/setup-matt-pocock-skills`**: Configures tracker, labels, and `## Agent skills` block.

## Optional Agent Tooling

Use these when you want faster orientation and persistent memory across sessions.

### Understand-Anything (global skills)

Install once per machine for agent-wide skills:

```bash
curl -fsSL https://raw.githubusercontent.com/Lum1104/Understand-Anything/main/install.sh | bash -s codex
```

Then invoke:

- `/understand` for first-pass architecture mapping on unfamiliar repos.
- `/understand-diff` before large refactors to preview blast radius.
- `/understand-explain <path>` when you need a focused explanation for one file or symbol.
- Knowledge-base placement: keep graph at `<project-root>/.understand-anything/knowledge-graph.json` (not workspace root).
- First usage in a task: check graph exists for target project repo; if missing, run `/understand` in that repo.
- Next usage during implementation: run `/understand-diff` after meaningful edits and `/understand-explain` for focused files/symbols.

### memtrace (global binary, workspace-scoped for multi-repo)

Install once per machine:

```bash
brew install memtrace-dev/tap/memtrace
```

Wire for multi-repo workspaces:

```bash
cd <workspace-root>
memtrace init --no-import
memtrace setup claude-code
memtrace setup vscode
```

Run one shared server from workspace root:

```bash
memtrace serve --dir <workspace-root>
```

Use workspace-root memtrace as single source of truth for all project codes in that workspace. Avoid repo-level memtrace MCP entries in nested repos.

### Supported Coding Tools Matrix (single source of truth)

| Tool Runtime | Workspace MCP file(s) | Notes |
| :--- | :--- | :--- |
| Cursor CLI / IDE | `<workspace-root>/.cursor/mcp.json` | Keep `~/.cursor/mcp.json` only as user-global fallback. |
| Claude Code | `<workspace-root>/.claude/settings.local.json` | Enable workspace MCP servers from root config files. |
| Antigravity CLI | `<workspace-root>/.agents/mcp_config.json` | Remote HTTP MCP entries must use `serverUrl`. |
| Codex CLI | `<workspace-root>/.codex/config.toml` | Keep memtrace server at workspace root. |
| Legacy MCP readers | `<workspace-root>/.mcp.json` | Compatibility file for runtimes that read legacy MCP config. |
| memtrace (all supported tools) | `memtrace serve --dir <workspace-root>` | Single source of truth. No repo-level memtrace servers. |
| Understand-Anything (all supported tools) | `<project-root>/.understand-anything/knowledge-graph.json` | Keep project graph at repo root, never at workspace root. |

Use local-only policy when needed by adding generated files to local git exclude (`.git/info/exclude`) instead of committing them.

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

## Suggested Next Skills Footer (Optional)

To reduce memory load during ad hoc usage, append a short recommendation block at the end of non-trivial responses:

```markdown
Suggested next skills (optional):
- /skill-name: why this is likely useful now.
```

Guidelines:

- Keep it recommendation-only. Do not enforce a gate or auto-chain.
- Apply this footer after any substantial step, including local and third-party skills.
- Keep it short: 1-3 suggestions maximum.
- Use workflow adjacency first (current step -> likely next step).
- Prefer evidence-raising suggestions before risky edits:
  - before larger refactors: `/understand-diff`
  - after discovery of unclear behavior: `/feature-prompt` or `/diagnose`
  - after prompt drafting: `/grill-with-docs`
  - after issue slicing: `/triage`
  - after implementation completion: `/commit-push-pr` or `/commit-push-close`, then `/release-notes`
- If confidence is low, suggest one conservative next step instead of a long list.

## Planned Vs Ad Hoc Issue Flow

Use two valid issue paths:

- **Planned work:** `/feature-discovery` -> `/to-issues` -> `/triage` -> `/tdd` -> `/commit-push-*`. The GitHub issue exists before coding. Matt Pocock's `/triage` owns readiness, labels, and agent brief quality. Implementation starts only when the issue has exactly one category label (`bug` or `enhancement`) and a ready state label (`ready-for-agent` or `ready-for-human`).
- **Ad hoc work:** one-line request -> `/diagnose` or direct fix -> `/tdd` when useful -> `/commit-push-*`. Do not fabricate a detailed GitHub issue before coding. The ship skill creates the issue at the end from the original request, final diff, decisions, and validation.

If an ad hoc request becomes large, ambiguous, cross-project, or multi-slice, stop and route it through `/triage`, `/feature-prompt`, or `/to-issues` before continuing.

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
| Release | `/release-notes` | PM-friendly summary saved to `docs/release-notes/`. |

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

If `memtrace` is connected, run `memory_recall` before step 1 with query terms from the task. If repo is unfamiliar or large, run `/understand` before step 1.

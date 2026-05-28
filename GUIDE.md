# Skills Usage Guide

Human-facing guide only. Do not load this file into `AGENTS.md`, shims, or model context.

Supported runtime boundary: this kit supports Codex CLI, Claude CLI,
Antigravity CLI, Cursor CLI, Opencode CLI, and GitHub Copilot CLI only.
Compatibility files such as `GEMINI.md` are for supported runtimes that read
those filenames and do not indicate support for Gemini CLI or any other
runtime.

Combine skills from this kit and the wider ecosystem to move from idea to shipped code and release notes. Prioritize context, evidence, and task isolation.

## Credits And Provenance

- **Local Skills:** Authored by Arfeen Arif. Combines original logic with ecosystem companion skills.
- **Matt Pocock:** Source for `/caveman`, `/grill-with-docs`, `/to-prd`, `/to-issues`, `/tdd`, `/diagnose`, `/triage`, `/improve-codebase-architecture`, `/zoom-out`, `/prototype`, and `/handoff`.
- **Forrest Chang:** Seeding logic for `/agents-md` non-negotiable principles.
- **Anthropic:** Source for `/skill-creator`.
- **Vercel Labs:** Source for `/agent-browser`, `skills` CLI, and React/React Native best practices.
- **Cursor:** Cursor CLI (`agent` command, `/skill-name`, `AGENTS.md` as canonical context, `Task` for subagents). Tool names and permissions: [`skills/agents-md/references/tool-calling.md`](skills/agents-md/references/tool-calling.md). https://cursor.com/docs/cli/overview

## Usage Principles

- Keep scope thin. Prefer small vertical slices over big-bang plans.
- Stay evidence-first. Use discovery and grilling before broad implementation.
- Use optional skills ad hoc. Do not auto-invoke compression skills.
- Keep architecture healthy. Regularly run planning and refactor loops.
- Preserve decisions. Move from prompt -> grill -> PRD -> issues -> implementation in traceable steps.

## Local Parallel & Background Agents (No Cloud)

These skills treat the main chat as an **orchestrator**. It splits work into
role-typed lanes and hands each to a local subagent, runs independent lanes at
the same time, and pushes long or noisy work to local background so the main
chat stays responsive and uncluttered.

- **Roles:** Explorer (read-only codebase search), Researcher (web / docs /
  dependency source), Planner (read-only plan), Implementer (writes code),
  Reviewer (read-only critique), Tester (runs tests / build / lint), and
  Tool-runner (isolated shell / MCP batches). The main session is the
  Orchestrator and keeps the only merge and final-judgment seat.
- **Parallel by default:** independent lanes run together; only conflict-prone
  edits and final integration stay serialized.
- **Local background:** long lanes run in the background (Claude CLI
  `run_in_background`, Cursor `is_background` + `Await`, Codex worktrees,
  Copilot `Ctrl+X -> b`, opencode `task(background=true)`) and report back when
  done.
- **No cloud agents.** Never hand work to remote background-agent products —
  Cursor Cloud Agents, GitHub Copilot cloud coding agent, Codex Cloud, or
  Antigravity managed/remote execution. Local worktree-isolated agents are
  fine; remote ones are not.

Per-runtime mechanics and the role-to-mechanism map live in
[`skills/agents-md/references/tool-calling.md`](skills/agents-md/references/tool-calling.md)
and each `*-tools.md`.

## Matt + Mickey Pattern

- Treat skills as strict process rails, not optional flavor text.
- Keep the human strategic: agent executes, human steers scope and tradeoffs.
- Prefer code-as-source-of-truth over broad doc summaries.
- If dependency behavior is unclear, fetch targeted source (for example `opensrc`) before guessing.
- Ship small, reviewable slices; avoid oversized PRs and oversized planning threads.

## First-Time Setup

1. **`/agents-md`**: Creates `AGENTS.md`, shims, and project matrix.
2. **`/setup-matt-pocock-skills`**: Configures tracker, labels, and `## Agent skills` block.

### Supported Coding Tools Matrix (single source of truth)

| Tool Runtime | Workspace MCP file(s) | Notes |
| :--- | :--- | :--- |
| Codex CLI | `<workspace-root>/.codex/config.toml` | Codex MCP configuration. |
| Claude CLI | `<workspace-root>/.claude/settings.local.json` | Enable workspace MCP servers from root config files. |
| Antigravity CLI | `<workspace-root>/.agents/mcp_config.json` | Remote HTTP MCP entries must use `serverUrl`. |
| Cursor CLI | `<workspace-root>/.cursor/mcp.json` | Keep `~/.cursor/mcp.json` only as user-global fallback. |
| Opencode CLI | `<workspace-root>/opencode.json` | Workspace-root opencode configuration where MCP servers are used. |
| GitHub Copilot CLI | `<workspace-root>/.mcp.json` (or Copilot MCP config) | Also reads `AGENTS.md` / `CLAUDE.md` / `GEMINI.md`; custom agents in `.github/agents/*.agent.md`. |

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

## Issue Naming And Label Preflight (Hard Gate)

Before creating, editing, or renaming any GitHub issue:

1. Read local workspace instructions (`AGENTS.md`; Claude CLI `CLAUDE.md` / Antigravity CLI `GEMINI.md` shims).
2. Select the exact issue title pattern (`PRD`, `Slice`, or non-PRD implementation form).
3. Select exactly one category label (`bug` or `enhancement`) and one state label.
4. Confirm no routing marker (`HITL:` / `AFK:`) is present in issue titles.

If tracker vocabulary is missing, stop and run `/setup-matt-pocock-skills` first.
Do not publish issues with inferred naming patterns or partial labels.

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
| Issue preflight | `Issue-writing skills` | Title pattern and both required labels are validated from local workspace instructions. |
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
- **Too Many Questions / Drift:** Narrow to one thin slice with `/feature-prompt`, then resume `/grill-with-docs`.
- **High-Fidelity Uncertainty (feel/UI/interaction):** `/handoff` -> `/prototype` -> back to `/grill-with-docs`.
- **Context Budget Pressure:** Treat `~120K` as a caution threshold during planning-heavy sessions; split scope or handoff before quality drops.
- **Broken Tests:** Stay in `/tdd` or pivot to `/diagnose`.
- **Large Issues:** Back to `/to-issues` for smaller slices.
- **Production Error:** Start with `/sentry` -> `/diagnose`.

## Practical Default

When unsure, run this sequence manually:
1. `/feature-discovery` (Understand)
2. `/feature-prompt` (Plan)
3. `/grill-with-docs` (Challenge)

No auto-chains. Trigger each step based on gate completion.

If the repo is unfamiliar or large, run `/feature-discovery` before step 1.

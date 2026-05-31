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

- Keep scope thin. Use small vertical slices, not big-bang plans.
- Stay evidence-first. Use discovery and grilling before broad implementation.
- Use optional skills ad hoc. Do not auto-invoke compression skills (`caveman` stays user-invoked only).
- **Exception:** `/memory-steward` auto-invokes a **light pass** at session start (after reading repo `MEMORY.md`). Full pass on user remember/sync/compact requests or explicit `/memory-steward`.
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
- **No cloud agents.** Never hand work to remote background-agent products:
  Cursor Cloud Agents, GitHub Copilot cloud coding agent, Codex Cloud, or
  Antigravity managed/remote execution. Local worktree-isolated agents are
  allowed. Remote agents are not.

Per-runtime mechanics and the role-to-mechanism map live in
[`skills/agents-md/references/tool-calling.md`](skills/agents-md/references/tool-calling.md)
and each `*-tools.md`.

## Matt + Arfeen Pattern

- Treat skills as strict process rails, not optional flavor text.
- Keep the human strategic: agent executes, human steers scope and tradeoffs.
- Use code as source of truth over broad doc summaries.
- If dependency behavior is unclear, fetch targeted source (for example `opensrc`) before guessing.
- Ship small, reviewable slices; avoid oversized PRs and oversized planning threads.

## First-Time Setup

1. **`/agents-md`**: Creates the workspace-root `AGENTS.md` (source of truth) and the `CLAUDE.md` redirect shim — the Project Matrix (each project keyed by its **PROJECT-CODE**: uppercase, hyphenated, emoji-stripped, e.g. `Partners API` → `PARTNERS-API`), the Non-Negotiable Rules, Working With Skills, and a Memory & Retrieval section with fill-after-setup placeholders. Generates no per-repo files.
2. **`/setup-matt-pocock-skills`**: Configures the issue tracker, labels, and where `CONTEXT.md` / `docs/` live.
3. **Fill the placeholders**: replace the `AGENTS.md` Memory & Retrieval placeholders with the real `CONTEXT.md` and `docs/adr/` paths from setup. Mechanical fill, not a rewrite.
4. **`/memory-steward`**: scaffolds/syncs each repo-root `MEMORY.md`; runs a light pass at every session start.

Enable built-in CLI memory globally when desired: [`skills/agents-md/references/memory-global-defaults.md`](skills/agents-md/references/memory-global-defaults.md).

### Supported Coding Tools Matrix (single source of truth)

| Tool Runtime | Workspace MCP file(s) | Notes |
| :--- | :--- | :--- |
| Codex CLI | `<workspace-root>/.codex/config.toml` | Codex MCP configuration. |
| Claude CLI | `<workspace-root>/.claude/settings.local.json` | Enable workspace MCP servers from root config files. |
| Antigravity CLI | `<workspace-root>/.agents/mcp_config.json` | Remote HTTP MCP entries must use `serverUrl`. |
| Cursor CLI | `<workspace-root>/.cursor/mcp.json` | Keep `~/.cursor/mcp.json` only as user-global fallback. |
| Opencode CLI | `<workspace-root>/opencode.json` | Workspace-root opencode configuration where MCP servers are used. |
| GitHub Copilot CLI | `<workspace-root>/.mcp.json` or `<workspace-root>/.github/mcp.json` | User fallback: `~/.copilot/mcp-config.json`. Also reads `AGENTS.md` / `CLAUDE.md` / `GEMINI.md`; custom agents in `.github/agents/*.agent.md`. |

Use local-only policy when needed by adding generated files to local git exclude (`.git/info/exclude`) instead of committing them.

## Choosing A Starting Point

| Situation | Start With | Why |
| :--- | :--- | :--- |
| New Workspace | `/agents-md` | Establish the Project Matrix, paths, and Non-Negotiable Rules. |
| Session start / memory hygiene | `/memory-steward` | Light pass after reading repo `MEMORY.md`; full pass on request. |
| Unclear Behavior | `/feature-discovery` | Read-only audit before planning. |
| Rough Idea | `/feature-prompt` | Section-by-section clarification interview. |
| Broken Behavior | `/diagnose` | Systematic root cause analysis. |
| Design Spike | `/prototype` | Validate UI/state before PRD/Issues. |
| Issue Work | `/tdd` | Red-Green-Refactor implementation loop. |
| Session Pause | `/handoff` | Continuation doc for the next agent. |

## Core Progression

```text
/agents-md -> /memory-steward -> /setup-matt-pocock-skills -> /feature-discovery -> /feature-prompt -> /grill-with-docs -> /to-prd -> /to-issues -> /triage -> /tdd -> /commit-push-pr -> /memory-steward -> /release-notes
```

(`/memory-steward` after ship when PRD closes or MEMORY grows; not a hard gate.)

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
- Keep it short: 1-6 suggestions maximum.
- Use workflow adjacency first (current step -> likely next step).
- Lead with evidence-raising suggestions before risky edits:
  - after discovery of unclear behavior: `/feature-prompt` or `/diagnose`
  - after prompt drafting: `/grill-with-docs`
  - after issue slicing: `/triage`
  - after implementation completion: `/commit-push-pr` or `/commit-push-close`, then `/release-notes`
  - after `/agents-md` or memory edits: `/memory-steward`
  - after PRD close or ADR acceptance: `/memory-steward` (promote queue → `docs/adr/`)
- If confidence is low, suggest one conservative next step instead of a long list.

## Memory & Retrieval Model

Generated `AGENTS.md` encodes how agents recall context:

- **Retrieval order:** `CONTEXT.md` + `docs/adr/` are **binding** (read before implementing) → repo-root `MEMORY.md` is **working recall** (a session-scoped index, not authority) → knowledge graphs are **advisory** (orientation only; never override binding).
- **Never bulk-read `docs/`.** Treat it as an on-demand archive — retrieve only what the task names, via search, a knowledge-graph query, or a discovery skill. Loading the whole tree rots context and wastes tokens.
- **Archived context on grill.** When you trigger `/grill-with-docs`, the agent asks up front whether you have archived context (prior discussions, original intent) for the feature. Paste it — captured verbatim into the ADR with provenance — or continue without. Old/current names it reveals are offered as `CONTEXT.md` aliases.

Skills are ad-hoc, not a pipeline. Work follows a gradient — discover → sharpen → plan → slice → implement → verify → ship → recall — and after each step the agent **suggests** a next skill but never auto-chains.

## Memory steward (`/memory-steward`)

Maintains **repo-root `MEMORY.md`** (≤ ~300 lines). Workspace **`CONTEXT.md`** and **`docs/adr/`** stay at `<artifacts-root>`.

| Pass | When | Work |
| :--- | :--- | :--- |
| Light | Session start (auto) | Line count, promotion-queue scan; compact only if > ~300 lines or queue non-empty |
| Full | User asks to remember/sync/compact/promote; PRD closed; explicit `/memory-steward` | Promote `ADR-NNNN:` bullets to ADRs, compact, sync Claude private memory into repo file |

Install:

```bash
npx skills install https://github.com/devarfeen/agent-skills-kit --skill memory-steward
```

Skill: [`skills/memory-steward/SKILL.md`](skills/memory-steward/SKILL.md).

## Understand-Anything (companion, optional)

[Understand-Anything](https://github.com/Lum1104/Understand-Anything) (UA) adds **Tier 1.5** structural retrieval via git-committed knowledge graphs. It complements — never replaces — CONTEXT, ADRs, and MEMORY.

| Topology | Code graph | Docs / wiki graph |
| :--- | :--- | :--- |
| Single repo | `<repo-root>/.understand-anything/knowledge-graph.json` | `<repo-root>/docs/.understand-anything/…` when `docs/wiki/index.md` exists |
| Monorepo | Root or package path per matrix | `<artifacts-root>/docs/.understand-anything/…` if centralized |
| VS Code multi-root | One graph per Project Matrix `Path` | `<artifacts-root>/docs/.understand-anything/…` |
| Meta-workspace | Per code repo in matrix | `<artifacts-root>/docs/.understand-anything/…` after `/understand-knowledge <artifacts-root>/docs` |

Install UA globally:

```bash
npx skills add Lum1104/Understand-Anything -g -y
```

Per repo root, bootstrap `.understand-anything/config.json` and `.gitignore` (ignore `intermediate/`, `tmp/`, `diff-overlay.json`, `fingerprints.json`; commit `knowledge-graph.json`, `meta.json`, `config.json`). Run `/understand <active-repo-root>` per matrix row; `/understand-knowledge <artifacts-root>/docs` when `docs/wiki/index.md` exists.

Refresh is **ad-hoc only** — kit skills suggest `/understand` via `Suggested next skills (optional)` footers; never auto-invoke at session start and never use `--auto-update` by default.

Full integration reference: [`docs/UNDERSTAND-ANYTHING-INTEGRATION.md`](docs/UNDERSTAND-ANYTHING-INTEGRATION.md).

## Planned Vs Ad Hoc Issue Flow

Use two valid issue paths:

- **Planned work:** `/feature-discovery` -> `/to-issues` -> `/triage` -> `/tdd` -> `/commit-push-*`. The GitHub issue exists before coding. Matt Pocock's `/triage` owns readiness, labels, and agent brief quality. Implementation starts only when the issue has exactly one category label (`bug` or `enhancement`) and a ready state label (`ready-for-agent` or `ready-for-human`).
- **Ad hoc work:** one-line request -> `/diagnose` or direct fix -> `/tdd` when useful -> `/commit-push-*`. Do not fabricate a detailed GitHub issue before coding. The ship skill creates the issue at the end from the original request, final diff, decisions, and validation.

If an ad hoc request becomes large, ambiguous, cross-project, or multi-slice, stop and route it through `/triage`, `/feature-prompt`, or `/to-issues` before continuing.

## Workflow Gates

| Gate | Skill | Continue When |
| :--- | :--- | :--- |
| Workspace | `/agents-md` | The PROJECT-CODE matrix and Non-Negotiable Rules are active. |
| Issue preflight | `Issue-writing skills` | Title pattern and both required labels are validated from local workspace instructions. |
| Discovery | `/feature-discovery` | Evidence-backed report is saved; old reports are not read unless requested. |
| Prompt | `/feature-prompt` | Implementation-ready prompt is reviewed by user. |
| Grill | `/grill-with-docs` | `Recommended answer:` is explicit; ambiguities resolve against ADRs and domain language. |
| PRD | `/to-prd` | Spec is clear; dependency order is known. |
| Issues | `/to-issues` | Slices are testable; prerequisites, blockers, and unblocked work are ordered. |
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
- **MEMORY too large / stale / post-PRD close:** `/memory-steward` (full pass).

## Practical Default

When unsure, run this sequence manually:
1. `/feature-discovery` (Understand)
2. `/feature-prompt` (Plan)
3. `/grill-with-docs` (Challenge)

No auto-chains. Trigger each step based on gate completion.

If the repo is unfamiliar or large, run `/feature-discovery` before step 1.

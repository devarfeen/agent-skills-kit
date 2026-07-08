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
- **Matt Pocock:** Source for `/ask-matt`, `/grill-with-docs`, `/to-spec`, `/to-tickets`, `/implement`, `/code-review`, `/wayfinder`, `/research`, `/tdd`, `/diagnosing-bugs`, `/triage`, `/domain-modeling`, `/codebase-design`, `/improve-codebase-architecture`, `/prototype`, and `/handoff`.
- **Forrest Chang:** Seeding logic for `/agents-md` non-negotiable principles.
- **Anthropic:** Source for `/skill-creator`.
- **Vercel Labs:** Source for `/agent-browser`, `skills` CLI, and React/React Native best practices.
- **Optional companions:** Graphify, Codex plugin for Claude Code, Impeccable, notebooklm-py, herdr, docker-expert, Laravel Boost, Figma MCP, and MySQL/Postgres MCP are separate installs used only when installed and task-fit.
- **Cursor:** Cursor CLI (`agent` command, `/skill-name`, `AGENTS.md` as canonical context, `Task` for subagents). Tool names and permissions: [`skills/agents-md/references/tool-calling.md`](skills/agents-md/references/tool-calling.md). https://cursor.com/docs/cli/overview

## Usage Principles

- Keep scope thin. Use small vertical slices, not big-bang plans.
- Stay evidence-first. Use discovery and grilling before broad implementation.
- Use optional skills ad hoc. Do not auto-chain from one skill into the next.
- Use companion skills and MCPs as helpers. Repo code, tests, ADRs, `CONTEXT.md`, and user instructions still win.
- Keep architecture healthy. Regularly run planning and refactor loops.
- Preserve decisions. Move from prompt -> grill -> spec -> tickets -> implementation in traceable steps.

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
- **Parallel once approved:** parallel and background work is opt-in — the
  generated `AGENTS.md` defaults to serial until the user approves a plan;
  then independent lanes run together and only conflict-prone edits and final
  integration stay serialized.
- **Local background:** long lanes run in the background (Claude CLI
  `run_in_background`, Cursor `is_background` + `Await`, Codex worktrees,
  Copilot `Ctrl+X -> b`, opencode `task(background=true)`) and report back when
  done.
- **No cloud agents.** Never hand work to remote background-agent products:
  Cursor Cloud Agents, GitHub Copilot cloud coding agent, Codex Cloud,
  Antigravity managed/remote execution, or Claude Routines / claude.ai
  background agents. Claude Code agent teams are local but also off-limits —
  the main session stays the only orchestrator. Local worktree-isolated
  agents are allowed. Remote agents are not.

Per-runtime mechanics and the role-to-mechanism map live in
[`skills/agents-md/references/tool-calling.md`](skills/agents-md/references/tool-calling.md)
and each `*-tools.md`.

**Inside herdr:** when you are running in [herdr](https://herdr.dev) (`HERDR_ENV=1`),
`/orchestrate-herdr` is the native expression of this local-only policy. It keeps the
current tab as a pure orchestrator and fans a spec (PRD) out to one local coding-CLI
worker tab per open sub-issue — re-runnable by swapping just the **spec URL** and the
**coding CLI**. No panes, no nested sub-agents, no cloud agents. See
[`skills/orchestrate-herdr/SKILL.md`](skills/orchestrate-herdr/SKILL.md).

Highest elevated permission presets live in the same tool-calling reference.
Use them only when the user explicitly asks for highest/elevated/full/YOLO
permission, preferably inside an isolated container, VM, dev container, or
disposable worktree.

| Runtime | Highest elevated launch / preset |
| :--- | :--- |
| Codex CLI | `codex --dangerously-bypass-approvals-and-sandbox` or `codex --sandbox danger-full-access --ask-for-approval never` |
| Claude CLI | `claude --dangerously-skip-permissions` / `--permission-mode bypassPermissions` |
| Antigravity CLI | `agy --dangerously-skip-permissions` without `--sandbox` |
| Cursor CLI | `agent --yolo --sandbox=disabled --approve-mcps` |
| Opencode CLI | `opencode run --auto` (renamed from `--dangerously-skip-permissions` in v1.17); persistent agents use `permission` keys set to `allow` |
| GitHub Copilot CLI | `copilot --allow-all` / `--yolo` |

## Matt + Arfeen Pattern

The operating stance behind this kit: the human stays strategic (scope and
tradeoffs), the agent executes against evidence, and skills are the rails that
keep it honest. The full mental model lives in
[BEST-PRACTICES.md](BEST-PRACTICES.md); the chat-visible behaviors —
PROJECT-CODEs in chat, `Stage / Found / Next / Needs user` phase updates,
understanding checks that wait for approval — are bound by the generated
`AGENTS.md` rules, not restated here.

Two habits worth restating because nothing else enforces them:

- If dependency behavior is unclear, fetch targeted source (for example
  `opensrc`) before guessing.
- Keep planning threads as small as PRs — oversized threads degrade quality
  the same way oversized diffs do.

## First-Time Setup

1. **`/agents-md`**: Creates the workspace-root `AGENTS.md` (source of truth) and the `CLAUDE.md` redirect shim — the Project Matrix (each project keyed by its **PROJECT-CODE**: uppercase, hyphenated, emoji-stripped, e.g. `Payments API` → `PAYMENTS-API`), the Non-Negotiable Rules, Working With Skills, and a Context & Native Memory section with fill-after-setup placeholders. Generates no per-repo files.
2. **`/setup-matt-pocock-skills`**: Configures the issue tracker, labels, and where `CONTEXT.md` and the artifacts tree live. Point the docs location at `specs/` — the kit's convention (kept off `docs/` so GitHub Pages' `/docs` publishing mode never collides with it).
3. **Fill the placeholders**: replace the `AGENTS.md` Context & Native Memory placeholders with the real `CONTEXT.md` and `specs/adr/` paths from setup. Mechanical fill, not a rewrite.
4. **`/design-system`** *(per project that has UI)*: turn that project's design system (a Figma file, a written spec, reference screens, or a guided-definition session) into named tokens + a UI library + a preview you eyeball to verify. It documents the system under `specs/design-system/`, adds a short binding reference to `AGENTS.md`, and seeds a project-local `<project>-ui-coding` skill so every later UI change consumes the library instead of inlining markup. Re-run `extend` as the design grows or to fold a shipped page's UI back in. Stack-adaptive; never auto-chains. Steps 1–3 are once per workspace; this is once per UI project.

> **Older workspaces:** re-running `/agents-md` on a workspace whose artifacts still live under `docs/` offers a one-time, ask-first `docs/` → `specs/` migration — it renames the tree and updates the `AGENTS.md` paths, moving only the artifacts subfolders.

Enable native CLI memory globally when desired: [`skills/agents-md/references/memory-global-defaults.md`](skills/agents-md/references/memory-global-defaults.md).

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

## Companion Skills And MCPs

These are optional separate installs. Use them beside this kit when installed and task-fit. Do not vendor them into this repo.

| Companion | Use when |
| :--- | :--- |
| Graphify | Querying a generated code/docs/media graph would save broad file reads. |
| ask-matt | You want Matt's upstream router for choosing a user-invoked skill flow. |
| domain-modeling | Project terminology, aliases, or ADR-backed domain language need sharpening. |
| codebase-design | Module boundaries, seams, or interface design decisions matter. |
| Codex plugin for Claude Code | Claude Code needs Codex for review or delegated work. |
| Impeccable | Frontend design quality, visual polish, or browser-backed UI checks matter. |
| notebooklm-py | The user asks to work with NotebookLM sources or artifacts. |
| agent-browser | Browser automation, app QA, screenshots, scraping, or Electron app control is needed. |
| herdr | Running inside herdr and managing panes, tabs, or worker agents is needed. |
| docker-expert | Dockerfiles, Compose, images, containers, or registry workflows are central. |
| Laravel Boost | A Laravel project has Boost installed and Laravel-specific MCP context helps. |
| Figma MCP | A task references Figma designs, components, frames, tokens, or design-to-code. |
| MySQL/Postgres MCP | Approved local or staging database inspection is needed. Default read-only. |
| Sentry CLI | A production error report needs `/sentry` investigation before `/diagnosing-bugs`. |

- Do not assume a companion is installed. If missing, use the best local fallback.
- Use MCPs only for the current task. Do not browse unrelated external data.
- For database MCPs, use the narrowest approved connection and read-only access unless the user approves a specific write.

## Choosing A Starting Point

| Situation | Start With | Why |
| :--- | :--- | :--- |
| New Workspace | `/agents-md` | Establish the Project Matrix, paths, and Non-Negotiable Rules. |
| Unsure Which Matt Skill Fits | `/ask-matt` | Route to a user-invoked upstream skill flow without auto-chaining. |
| Unclear Behavior | `/feature-discovery` | Read-only audit before planning. |
| Rough Idea | `/feature-prompt` | Infer-first prompt drafting; asks only what it can't infer. |
| Broken Behavior | `/diagnosing-bugs` | Systematic root cause analysis. |
| Design Spike | `/prototype` | Validate UI/state before spec/tickets. |
| Issue Work | `/tdd` + `/tdd-loop` | Test-first implementation. `/tdd-loop` is the kit's procedure (gates, completion evidence, exception protocol) and stands alone; Matt's `/tdd` adds test quality and seam choice when installed. |
| Porting A Feature | `/port-feature` | Trace a reference feature into a target stack as a gap map. |
| Project Needs A UI Library | `/design-system` | Turn a design system into tokens + components + a verifiable preview. |
| Page Must Match Design | `/pixel-audit` | Strict per-page visual conformance with an element-level gate. |
| Cosmetic QA Tail | `/polish-batch` | Batch small copy/spacing/alignment nits, then fix in one pass. |
| Multi-Project Spec | `/integration-contract` | Map the cross-repo seam and smoke-test it before shipping. |
| Work Too Big For One Session | `/wayfinder` | Map a huge effort as tracker tickets; resolve them until the way is clear. |
| Delegable Reading Legwork | `/research` | Background agent reads primary sources into a cited Markdown doc. |
| Session Pause | `/handoff` | Continuation doc for the next agent. |

## Core Progression

```text
/agents-md -> /setup-matt-pocock-skills -> /design-system -> /feature-discovery -> /feature-prompt -> /grill-with-docs -> /to-spec -> /to-tickets -> /tdd -> /pixel-audit -> /commit-push-pr -> /release-notes
```

Two variations branch off this line:

- **Porting** a feature from a reference implementation starts with `/port-feature` (in place of `/feature-discovery` → `/feature-prompt`), which writes a gap map and hands to `/grill-with-docs`.
- **Verify** is a cluster, not one skill: `/pixel-audit` for per-page conformance, manual QA + `/polish-batch` for the cosmetic tail, and `/integration-contract` when the spec spans more than one PROJECT-CODE. After a UI slice ships, `/design-system` (extend) folds any new reusable UI back into the library.

## Issue Naming And Label Preflight (Hard Gate)

Before creating, editing, or renaming any GitHub issue:

1. Read local workspace instructions (`AGENTS.md`; Claude CLI reads the `CLAUDE.md` shim).
2. Select the exact issue title pattern (`Spec`, `Slice`, or non-spec implementation form). Issues titled `PRD:` predate the spec rename — treat them as spec issues; do not retitle.
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
- Include companion skills or MCPs when they are the best next helper for the current step.
- Keep it short: 1-6 suggestions maximum.
- Use workflow adjacency first (current step -> likely next step).
- Lead with evidence-raising suggestions before risky edits:
  - after discovery of unclear behavior: `/feature-prompt` or `/diagnosing-bugs`
  - after prompt drafting: `/grill-with-docs`
  - after ticket slicing: `/tdd` for the first ready ticket
  - after implementation completion: `/commit-push-pr` or `/commit-push-close`, then `/release-notes`
- If confidence is low, suggest one conservative next step instead of a long list.

## Context & Native Memory Model

Generated `AGENTS.md` encodes how agents retrieve context:

- **Retrieval order:** `CONTEXT.md` + `specs/adr/` are **binding** (read before implementing) -> current task context (the active request, issue or spec) -> the current CLI's native memory when enabled.
- **Never bulk-read `specs/`.** Treat it as an on-demand archive — retrieve only what the task names, via search or a discovery skill. Loading the whole tree rots context and wastes tokens.
- **Native memory only.** Do not create repo memory files, wiki files, discovery files, or default knowledge-graph memory. Optional graph/index companions may be used when installed and task-fit, but their artifacts are not binding memory. Do not sync memory between CLIs.
- **Archived context on grill.** When you trigger `/grill-with-docs`, the agent asks up front whether you have archived context (prior discussions, original intent) for the feature. Paste it — captured verbatim into the ADR with provenance — or continue without. Old/current names it reveals are offered as `CONTEXT.md` aliases.

Skills are ad-hoc, not a pipeline. Work follows a gradient — discover → sharpen → plan → slice → implement → verify → ship — and after each step the agent **suggests** a next skill but never auto-chains.

## Planned Vs Ad Hoc Issue Flow

Use two valid issue paths:

- **Planned work:** `/feature-discovery` -> `/feature-prompt` -> `/grill-with-docs` -> `/to-spec` -> `/to-tickets` -> `/tdd` -> `/commit-push-*`. The spec and ticket issues exist before coding. `/to-spec` and `/to-tickets` apply ready labels in the normal path, so no separate `/triage` step is required.
- **Existing or incoming issue work:** use `/triage` when an issue needs state changes, reporter follow-up, `ready-for-human`, `wontfix`, or an agent brief before implementation.
- **Ad hoc work:** one-line request -> `/diagnosing-bugs` or direct fix -> `/tdd` when useful -> `/commit-push-*`. Do not fabricate a detailed GitHub issue before coding. The ship skill creates the issue at the end from the original request, final diff, decisions, and validation.

If an ad hoc request becomes large, ambiguous, cross-project, or multi-slice, stop and route it through `/feature-prompt` or `/to-tickets` before continuing. Use `/triage` only if there is already an issue whose state or labels need repair.

## Workflow Gates

| Gate | Skill | Continue When |
| :--- | :--- | :--- |
| Workspace | `/agents-md` | The PROJECT-CODE matrix and Non-Negotiable Rules are active. |
| Design system | `/design-system` | Tokens + library built; preview renders and the user has eyeballed it; `AGENTS.md` reference + `<project>-ui-coding` seeded. |
| Issue preflight | `Issue-writing skills` | Title pattern and both required labels are validated from local workspace instructions. |
| Discovery | `/feature-discovery` | Evidence-backed report is returned in chat; discovery files are never written. |
| Port | `/port-feature` | Gap map written to `specs/port/`; reference behaviour vs target state mapped; a thin first slice named. |
| Prompt | `/feature-prompt` | Implementation-ready prompt is reviewed by user. |
| Grill | `/grill-with-docs` | `Recommended answer:` is explicit; ambiguities resolve against ADRs and domain language. |
| Spec | `/to-spec` | Spec is clear; dependency order is known. |
| Tickets | `/to-tickets` | Tickets are testable; prerequisites, blocking edges, and unblocked work are ordered. |
| Existing issue triage | `/triage` | Existing issue state is clear, or an Agent Brief / needs-info / wontfix outcome is recorded. |
| Build | `/tdd` + `/tdd-loop` | Failure verified (Red), Fix verified (Green). |
| Pixel conformance | `/pixel-audit` | Defect list cleared; every fix passes the element-level gate on served assets. |
| QA polish | `/polish-batch` | Cosmetic nits captured, dispatched per PROJECT-CODE, and verified. |
| Cross-repo seam | `/integration-contract` | Multi-project spec's producer/consumer contract built and smoke gate green (single-project auto-skips). |
| Ship | `/commit-push-*` | Branch pushed and issue/PR linked with test proof. |
| Release | `/release-notes` | PM-friendly summary saved to `specs/release-notes/`. |

## Recovery Loops

- **Vague Prompt:** Back to `/feature-prompt`.
- **Domain Ambiguity:** Stay in `/grill-with-docs` (updates `CONTEXT.md` inline).
- **Too Many Questions / Drift:** Narrow to one thin slice with `/feature-prompt`, then resume `/grill-with-docs`.
- **High-Fidelity Uncertainty (feel/UI/interaction):** `/handoff` -> `/prototype` -> back to `/grill-with-docs`.
- **Context Budget Pressure:** Treat `~120K` as a caution threshold during planning-heavy sessions; split scope or handoff before quality drops.
- **Broken Tests:** Stay in `/tdd` or pivot to `/diagnosing-bugs`.
- **Large Tickets:** Back to `/to-tickets` for smaller slices.
- **UI Drifts From Design:** `/pixel-audit` the page against its source of truth; clear the element-level gate before shipping.
- **Cosmetic Nits Pile Up:** `/polish-batch` — capture them, then dispatch in one pass per PROJECT-CODE.
- **Cross-Repo Seam Risk:** `/integration-contract` before shipping a multi-project spec.
- **Inlined UI Instead Of The Library:** back to `/design-system` (extend) to promote it into the library, then consume it from the page.
- **Production Error:** Start with `/sentry` -> `/diagnosing-bugs`.

## Practical Default

When unsure, run this sequence manually:
1. `/feature-discovery`
2. `/feature-prompt` (Plan)
3. `/grill-with-docs` (Challenge)

No auto-chains. Trigger each step based on gate completion.

If the repo is unfamiliar or large, run `/feature-discovery` before step 1.

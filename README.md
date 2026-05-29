# Agent Skills Kit

A collection of reusable **skills** for six supported AI coding CLIs:
Codex CLI, Claude CLI, Antigravity CLI, Cursor CLI, Opencode CLI, and
GitHub Copilot CLI. No other agent runtime is supported by this kit.

A *skill* is a small, self-contained bundle of instructions, examples, and
templates that teaches an agent how to do one specific job well — for example,
"write PM-friendly release notes from git history". Install a skill into your
agent's workflow and the agent picks it up automatically when a matching
request comes in.

## Repository Layout

```
agent-skills-kit/
├── README.md                 # This file
├── LICENSE                   # MIT
└── skills/
    ├── agents-md/            # Generate AGENTS.md plus Claude CLI / Antigravity CLI shims
    │   ├── SKILL.md          # Required: metadata + instructions
    │   └── references/
    │       ├── tool-calling.md       # Orchestration model, role lanes, local-only policy, CLI mappings
    │       ├── cursor-tools.md       # Skill-kit → Cursor mapping
    │       └── *-tools.md            # claude, codex, copilot, antigravity, opencode
    ├── release-notes/        # The release-notes skill
    │   ├── SKILL.md          # Required: metadata + instructions
    │   ├── README.md         # Human-readable docs for this skill
    │   ├── references/       # Additional docs loaded on demand
    │   │   ├── examples.md   # Worked input → output examples
    │   │   └── triggers.md   # Phrases that activate the skill
    │   └── assets/           # Output templates the skill fills in
    │       ├── release-notes-template.md
    │       └── session-summary-template.md
    ├── feature-discovery/    # The feature-discovery skill
    │   └── SKILL.md          # Required: metadata + instructions
    ├── feature-prompt/       # The feature-prompt skill
    │   └── SKILL.md          # Required: metadata + instructions
    ├── commit-push-close/    # The commit-push-close skill
    │   └── SKILL.md          # Required: metadata + instructions
    ├── commit-push-pr/       # The commit-push-pr skill
    │   └── SKILL.md          # Required: metadata + instructions
    └── deprecated/           # Retained for reference only — do not install for new workflows
        ├── feature-prompt-full/  # Deprecated; trigger each step manually instead
        │   └── SKILL.md
        └── ubiquitous-language/  # Deprecated; use Matt Pocock's /grill-with-docs instead
            └── SKILL.md
```

Each subfolder under `skills/` is a standalone skill that follows the
[Agent Skills spec](https://agentskills.io/specification) — a `SKILL.md` with
`name` + `description` frontmatter plus optional supporting files. Skills can
be installed on their own.

## Installing a Skill

```bash
npx skills install https://github.com/devarfeen/agent-skills-kit --skill <skill-name>
```

Updating to the latest version:

```bash
npx skills update https://github.com/devarfeen/agent-skills-kit --skill <skill-name>
```

The `skills` CLI fetches the named subfolder from this repo and installs it
into your agent's local skills directory. After install, just talk to your
agent normally — it will invoke the skill when your request matches one of
its trigger phrases.

**Cursor CLI:** Install with `npx skills install` (skills land in
`~/.cursor/skills/` or `.cursor/skills/`). Invoke a skill with `/skill-name`
(for example `/release-notes`). Run the CLI with `agent` for interactive
sessions or `agent -p "..."` for scripts and CI.

## Workflow Guide

See [GUIDE.md](GUIDE.md) for the recommended workflow from
workspace setup and spec creation through issues, TDD implementation, PR
shipping, and release notes. If you use Matt's engineering skills, run
`/setup-matt-pocock-skills` once per repo before `/to-prd`, `/to-issues`,
`/triage`, `/diagnose`, `/tdd`, `/improve-codebase-architecture`, or
`/zoom-out`. The workflow also defines an optional `Suggested next skills`
footer pattern (recommendations only) so agents can append lightweight
before/after reminders at the end of non-trivial responses, including after
third-party skills.

Issue-writing hard gate (required): before drafting, renaming, or publishing
any GitHub issue, verify both the title format and labels from local workspace
instructions (`AGENTS.md` and its shims). If issue-tracker vocabulary is not
loaded, stop and run `/setup-matt-pocock-skills` first. Never publish with
inferred title patterns or partial labels.

## Credits And Provenance

This repository combines original local skills with workflow ideas and companion
skills from the wider agent-skills ecosystem.

- Local skills and docs in this repository are authored and maintained by
  Arfeen Arif. Local git history shows the release-notes skill was added first,
  followed by feature-discovery, feature-prompt, feature-prompt-full
  (deprecated), agents-md, ubiquitous-language (deprecated), and the workflow
  guide.
- The non-negotiable discipline in `agents-md` was originally seeded by
  Forrest Chang's Karpathy-inspired `CLAUDE.md` guidelines and later expanded
  in this repo into an 18-rule core plus retained operational defaults:
  https://github.com/forrestchang/andrej-karpathy-skills/blob/main/CLAUDE.md
  The upstream repository is MIT licensed. This repo records credit here rather
  than emitting source notes into generated `AGENTS.md` files.
- `ubiquitous-language` (deprecated, kept in `skills/` for reference only) is
  based on Matt Pocock's deprecated `ubiquitous-language` skill, MIT License,
  Copyright 2026 Matt Pocock:
  https://github.com/mattpocock/skills/blob/main/ubiquitous-language/SKILL.md
  Domain-language sharpening is now covered by Matt's `/grill-with-docs`,
  which updates `CONTEXT.md` and ADRs inline.
- The workflow guide references companion skills from Matt Pocock's skills repo,
  including `setup-matt-pocock-skills`, `grill-with-docs`,
  `to-prd`, `to-issues`, `tdd`, `diagnose`, `triage`,
  `improve-codebase-architecture`, `zoom-out`, `prototype`, and `handoff`:
  https://github.com/mattpocock/skills
- Optional structural retrieval companion: [Understand-Anything](https://github.com/Lum1104/Understand-Anything) — git-committed knowledge graphs as Tier 1.5 alongside CONTEXT, ADRs, and MEMORY. See [`docs/UNDERSTAND-ANYTHING-INTEGRATION.md`](docs/UNDERSTAND-ANYTHING-INTEGRATION.md) and [`GUIDE.md`](GUIDE.md#understand-anything-companion-optional).
- `/caveman` is credited to Matt Pocock's `caveman` skill, MIT License,
  Copyright 2026 Matt Pocock:
  https://github.com/mattpocock/skills/blob/main/skills/productivity/caveman/SKILL.md
  `caveman` is available as an optional ad-hoc skill for chat brevity and is
  never applied to code, docs, PRDs, release notes, PR bodies, or persisted artifacts.
- `/skill-creator` is credited to Anthropic's public skills repository:
  https://github.com/anthropics/skills/tree/main/skills/skill-creator
- `/agent-browser`, the `skills` CLI, `find-skills`, and Vercel React/React
  Native best-practice skills are credited to Vercel Labs:
  https://github.com/vercel-labs/agent-browser
  https://github.com/vercel-labs/skills
  https://github.com/vercel-labs/agent-skills
- `/sentry` refers to Sentry's CLI for developers and agents:
  https://cli.sentry.dev/
- **Cursor CLI:** `AGENTS.md` is the canonical workspace context file;
  skills use `/skill-name` invocation and the `Task` tool for subagents.
  https://cursor.com/docs/cli/overview
  https://cursor.com/docs/context/skills
- **Supported runtime boundary:** This kit supports Codex CLI, Claude CLI,
  Antigravity CLI, Cursor CLI, Opencode CLI, and GitHub Copilot CLI only.
  Compatibility files such as `GEMINI.md` exist solely for supported runtimes
  that read those filenames; they do not indicate support for Gemini CLI or
  any other runtime.

## Available Skills

### `agents-md`

Generates `AGENTS.md` as the canonical agent instruction file and creates a
`CLAUDE.md` shim that imports it (`CONTEXT.md` at artifacts-root; repo `MEMORY.md` when present).

```bash
npx skills install https://github.com/devarfeen/agent-skills-kit --skill agents-md
```

**What it does**

- Includes an 18-rule non-negotiable core in `AGENTS.md` (now covering local background execution, the orchestrator + role-lane model, and the discovery file guard), plus retained operational defaults for full Project Matrix code usage and parallel execution
- Uses `AGENTS.md` as the canonical instruction file for supported runtimes that read it directly; creates `CLAUDE.md` for Claude CLI with `@` imports for `AGENTS.md`, `<artifacts-root>/CONTEXT.md`, and active repo `MEMORY.md` when those files exist
- Enforces instruction economy: keep `AGENTS.md` concise with stable, non-obvious invariants; keep detailed procedures in skills/references
- Orders `/to-prd` and `/to-issues` work by dependencies: prerequisites, blockers, then unblocked slices; supports AFK herdr orchestration when available
- Detects `*.code-workspace` manifests and uses each folder `name` as the project name/code source
- Treats the workspace folder with `path: "."` as a meta workspace with no code
- Builds a project matrix: `Project Name (Code) | Path | Tech Stack`
- Establishes stable project codes for use across prompt, PRD, issue, discovery, release-note, PR, commit, and code-comment contexts
- References `CONTEXT.md` at `<artifacts-root>`; **`MEMORY.md` at each repo root** (Project Matrix row); `docs/adr/` at `<artifacts-root>` when available
- Wires `/memory-steward` at session start (light pass) in generated `AGENTS.md`

**Example prompts**

| Mode | Example prompt |
| --- | --- |
| New instructions | `Generate AGENTS.md for this workspace` |
| Workspace manifest | `Create AGENTS.md and shims from my code-workspace manifest` |
| Refresh project matrix | `Update AGENTS.md project codes and tech stacks` |

### `memory-steward`

Keeps repo-root `MEMORY.md` (≤ ~300 lines) in sync across CLIs, compacts stale bullets, and promotes `ADR-NNNN:` items to workspace `docs/adr/` when PRDs close.

```bash
npx skills install https://github.com/devarfeen/agent-skills-kit --skill memory-steward
```

**What it does**

- **Light pass (auto at session start):** line count and promotion-queue scan after reading repo `MEMORY.md`
- **Full pass (on request):** compact, sync Claude/Codex private memory into repo file, promote closed PRD memory to ADRs
- Resolves active `<repo-root>` from Project Matrix + cwd; leaves `CONTEXT.md` / ADRs at `<artifacts-root>`

**Example prompts**

| Mode | Example prompt |
| --- | --- |
| Session start | *(automatic light pass when `AGENTS.md` is active)* |
| Remember / sync | `Remember that we use pnpm only in this repo` |
| Compact / promote | `/memory-steward` or `Compact MEMORY and promote closed PRD items to ADR` |

Global CLI memory defaults: [`skills/agents-md/references/memory-global-defaults.md`](skills/agents-md/references/memory-global-defaults.md).

### `release-notes`

Turns git commits, the current dev session, or finished feature work into
**clear, PM-friendly release notes**. Designed so a non-technical reader can
scan everything in 30 seconds.

```bash
npx skills install https://github.com/devarfeen/agent-skills-kit --skill release-notes
```

**What it does**

- Reads git history (locally only — never runs `git fetch` or `git pull`)
- Walks multi-repo workspaces and finds every `.git` root
- Clusters related commits into a single logical change instead of
  commit-by-commit narration
- Produces a single markdown file with two sections:
  1. **Stakeholder Summary** — bullet list grouped by full Project Matrix code, one
     sentence per change
  2. **Detailed Release Notes** — full Problem → Change → Impact → Scope →
     Manual QA Steps → Commits Included blocks per feature

**Generation modes**

| Mode | Example prompt |
| --- | --- |
| Date-based (single date or range) | `Generate release notes for 11 March 2026` |
| Single project on a date | `Generate release notes for PARTNERS-APP on 11 March` |
| All projects on a date | `Generate release notes for all projects on 15 April` |
| Current dev session | `Summarize today's development session` |
| Specific feature | `Write release notes for the QR scanning improvements` |

**Output location**

Generated files land in `<artifacts-root>/docs/release-notes/`. Release notes
are on-demand date files and do not share the ADR/prompt `NNNN` sequence.
`<artifacts-root>` resolves to the `*.code-workspace` manifest root when a
`*.code-workspace` file is present, otherwise the repo root — so artifacts stay
centralized and out of individual project repos whenever a workspace exists.

- Date, feature, or session:
  `<artifacts-root>/docs/release-notes/D-Month-YYYY.md`
  (workspace example: `<workspace-dir>/docs/release-notes/10-March-2026.md`;
  single repo: `docs/release-notes/10-March-2026.md`)
- Date range:
  `<artifacts-root>/docs/release-notes/D-Month-YYYY-to-D-Month-YYYY.md`
  (example: `10-March-2026-to-12-March-2026.md`)

**Manual QA steps**

Each detailed feature entry includes a Manual QA Steps subsection. The skill
generates 3–5 practical Action → Expected Result steps inline, covering the
primary happy path and one edge case.

**Writing style**

The skill enforces strict plain-language rules — no jargon, max 2 bullets per
section, feature names describe *what changed* not *how*, and a banned-words
list (`workstream`, `touchpoint`, `formally`, etc.) keeps output readable.

See [skills/release-notes/README.md](skills/release-notes/README.md) for the
full feature list and [skills/release-notes/references/examples.md](skills/release-notes/references/examples.md)
for input/output examples (including a side-by-side bad-vs-good comparison).

### `feature-discovery`

Performs a read-only discovery pass for a feature, issue, module, workflow,
API, config, or behavior across one or more codebase projects.

```bash
npx skills install https://github.com/devarfeen/agent-skills-kit --skill feature-discovery
```

**What it does**

- Maps project codes to likely repo, app, or package roots
- Searches code, tests, docs, configs, routes, jobs, and feature flags
- Traces definitions to callers and user-facing flows
- Uses code as primary source of truth; highlights reuse seams and duplication risks
- Saves the full discovery report to `<artifacts-root>/docs/discovery/DD-MM-YYYY-<PROJECT-CODE>-<slug>.md`
- Does not auto-read existing `docs/discovery/` reports; treats them as stale unless the user asks for them
- Optionally uses targeted `opensrc` dependency source pulls when external internals are required and local evidence is insufficient
- Flags code-discovered domain terms that may be missing from or stale in
  `CONTEXT.md`, with short descriptions and evidence for user approval
- Updates `CONTEXT.md` or other artifacts only as an explicit follow-up after
  showing exact target files and proposed changes for user approval
- Uses recent git history only when code scanning is not enough
- Produces a structured report covering summary, behavior, implementation,
  usage sites, rationale, candidate context terms, risks, gaps, and next checks

**Example prompts**

| Mode | Example prompt |
| --- | --- |
| Feature lookup | `Explain how asset lookup works in MOBILE-APP` |
| Issue trace | `Investigate why RFID scans fail in PARTNERS-APP` |
| Workflow audit | `Trace the invite-user workflow across ADMIN-WEB and API-SERVICE` |

### `feature-prompt`

Turns a rough feature idea into a **small feature prompt** for one or more
codebase projects. Designed as a handoff to
`grill-with-docs`, which does the detailed challenge pass.

```bash
npx skills install https://github.com/devarfeen/agent-skills-kit --skill feature-prompt
```

**What it does**

- Converts rough intake into a minimal `grill-with-docs` handoff
- Asks only when the requested change or project/context is unclear
- Uses cheap repo evidence such as project matrix, cwd, `CONTEXT.md`, and ADR names
- Defaults to a thin vertical slice and prompts scope-splitting when the request is too broad
- Keeps scope PR-sized (small, reviewable, mergeable slice)
- Favors code-reference-first context and non-obvious constraints over generic stack restatement
- Promotes reuse-before-rewrite and surfaces seam-reuse uncertainty in `Open questions`
- Distinguishes grillable (low-fidelity) vs ungrillable (high-fidelity/feel) unknowns before drafting `Open questions`
- Routes ungrillable unknowns toward `/handoff` + `/prototype` instead of forcing endless grilling
- When cheap exploration reveals missing or stale domain terms, shows candidate
  `CONTEXT.md` updates with short descriptions for user approval
- Applies approved `CONTEXT.md` updates only as a separate documentation step
- Sends non-trivial or inferred drafts to the user for one correction pass
- Saves the final prompt to `<artifacts-root>/docs/prompts/NNNN-<feature-slug>-prompt.md` (sibling of `docs/adr/`; prompt and ADR filenames both start with `NNNN-<slug>`, and numbering is shared with ADRs only). `<artifacts-root>` is the `*.code-workspace` manifest root when present, otherwise the repo root — artifacts stay out of individual project repos whenever a workspace exists.
- Asks the user to pass the final prompt to `grill-with-docs`
- Produces a short final prompt with only the needed sections

**Prompt sections**

| Section | Purpose |
| --- | --- |
| Project | Full Project Matrix code, repo, path, or context |
| What is needed | The requested change |
| Why it is needed | The problem, value, or workflow gap |
| Expected end result | Observable done state |
| Known limits | Optional hard constraints or non-goals |
| Open questions | Optional unresolved questions for `grill-with-docs` |

**Example prompts**

| Mode | Example prompt |
| --- | --- |
| New feature | `Help me create a feature prompt for stock transfer approvals` |
| Change request | `Turn this rough request into a dev prompt for MOBILE-APP and API-SERVICE` |
| Multi-project work | `Create a feature prompt for ADMIN-WEB, MOBILE-APP, and API-SERVICE` |

### `commit-push-close`

Ships one iteration of work on a GitHub issue: stage and commit with a
structured message, push to the current branch, then close the linked GitHub
issue with a comment that explains how to test the change.

```bash
npx skills install https://github.com/devarfeen/agent-skills-kit --skill commit-push-close
```

**What it does**

- Resolves the linked GitHub issue from the branch name, recent commits, or conversation context. If none exists, creates one inline only for small ad hoc work; planned work routes back to `/triage`, `/feature-prompt`, or `/to-issues`.
- Reads issue labels via `gh issue view --json state,labels,title`; routing state stays in labels, not title prefixes:
  - `ready-for-human` → proceed with human-decision context in the body/comment
  - `ready-for-agent` → proceed autonomously
  - missing/conflicting labels or non-ready state → stop and route through `/triage`
- Inline-created ad hoc issues get one category label (`bug` or `enhancement`) and one ready state label (`ready-for-agent` or `ready-for-human`)
- Writes a structured commit message whose subject mirrors the GitHub issue title as closely as practical, plus an `Issue:` line and optional `Decisions:` / `Files:` / `Notes:` sections
- For ad hoc inline issues, the new GitHub issue title and commit subject must match unless a hard tool limit prevents it
- Enforces zero-attribution output across supported coding-agent paths (Codex CLI, Claude CLI, Antigravity CLI, Cursor CLI, Opencode CLI, and GitHub Copilot CLI): no `Co-authored-by`, `Made-with`, `Generated by`, or AI signature lines
- Honors hooks (no `--no-verify`), refuses to stage secret-pattern files, and stages explicitly by path (no `git add -A`)
- If env keys change, enforces synchronized add/remove/change across `.env`, `.env.staging`, `.env.production`, keeps `.sample.env`/`.example.env` current, and requires README/docs reference updates (with local-only reporting when env files are gitignored)
- Pushes the current branch (`-u origin <branch>` if no upstream); requires a separate confirmation when the branch is `main` / `master`
- Closes the issue with `gh issue close <num> --comment` — the comment includes the commit SHA, branch, a one-line summary, and a 3–6 step **How to test** plan derived from the diff
- Asks before posting if the test plan cannot be derived from the diff

**Use when**

- You wrap up an iteration on a GitHub issue and want to commit, push, and close in one step
- You are working directly on a branch and do not need a PR review step
- The work is issue-driven and the issue uses `ready-for-human` / `ready-for-agent` state labels, or the work is a small ad hoc request ready to ship

**Example prompts**

| Mode | Example prompt |
| --- | --- |
| Wrap up an iteration | `Commit, push, and close this issue` |
| Ship issue work | `I'm done with #418, ship it` |
| Explicit close | `commit-push-close — write the test steps from the diff` |

### `commit-push-pr`

Ships one iteration of work on a GitHub issue as a pull request: stage and
commit with a structured message, push the current branch (auto-creating a
feature branch off `main`/`master` first), and open a PR with `Closes #N`,
a summary, and a how-to-test plan.

```bash
npx skills install https://github.com/devarfeen/agent-skills-kit --skill commit-push-pr
```

**What it does**

- Resolves the linked GitHub issue from the branch name, recent commits, or conversation context. If none exists, creates one inline only for small ad hoc work; planned work routes back to `/triage`, `/feature-prompt`, or `/to-issues`.
- Reads issue labels via `gh issue view --json state,labels,title,url`; routing state stays in labels, not title prefixes:
  - `ready-for-human` → proceed with human-decision context in the body/comment
  - `ready-for-agent` → proceed autonomously
  - missing/conflicting labels or non-ready state → stop and route through `/triage`
- Inline-created ad hoc issues get one category label (`bug` or `enhancement`) and one ready state label (`ready-for-agent` or `ready-for-human`)
- If the current branch is the repo default (`main` / `master`), proposes a feature branch (`issue/<num>-<slug>`) and waits for the user to confirm before checking it out
- Writes a structured commit message whose subject mirrors the GitHub issue title as closely as practical, plus an `Issue:` line and optional `Decisions:` / `Files:` / `Notes:` sections
- For ad hoc inline issues, the new GitHub issue title, commit subject, and PR title must match unless a hard tool limit prevents it
- Enforces zero-attribution output across supported coding-agent paths (Codex CLI, Claude CLI, Antigravity CLI, Cursor CLI, Opencode CLI, and GitHub Copilot CLI): no `Co-authored-by`, `Made-with`, `Generated by`, or AI signature lines
- Honors hooks (no `--no-verify`), refuses to stage secret-pattern files, and stages explicitly by path (no `git add -A`)
- If env keys change, enforces synchronized add/remove/change across `.env`, `.env.staging`, `.env.production`, keeps `.sample.env`/`.example.env` current, and requires README/docs reference updates (with local-only reporting when env files are gitignored)
- Pushes with `-u origin <branch>` if no upstream is set
- Opens a PR against the detected default branch (`gh repo view --json defaultBranchRef`) with a title matching the commit subject and a body containing `Closes #N`, **Summary**, optional **Decisions**, **How to test** (3–6 steps), and optional **Notes**
- Detects an existing PR for the branch and edits it (`gh pr edit`) instead of creating a duplicate
- Asks before opening the PR if the test plan cannot be derived from the diff

**Use when**

- You are wrapping up an issue and want a reviewable PR rather than a direct close
- The repo workflow expects PRs to merge changes into `main`
- You want the issue to auto-close when the PR merges (via `Closes #N`)

**Example prompts**

| Mode | Example prompt |
| --- | --- |
| Open a PR for the current issue | `Commit, push, and open a PR for this issue` |
| Ship issue work as a PR | `PR this — closes #418` |
| Update an existing PR | `commit-push-pr — there's already an open PR for this branch` |

### `feature-prompt-full` (deprecated)

> **Deprecated.** Source lives at
> [`skills/deprecated/feature-prompt-full/`](skills/deprecated/feature-prompt-full/SKILL.md)
> for reference only. The kit now prefers manual, user-triggered invocation of
> each downstream step over a state-machine-style auto-chain. Use
> `/feature-prompt` to draft the prompt, then trigger `/grill-with-docs`,
> `/to-prd`, `/to-issues`, `/triage`, and `/tdd` yourself as the work
> progresses. Do not install for new workflows.

Turns a rough feature idea into a prompt and prepares the full downstream
delivery chain: `/grill-with-docs`, `/to-prd`, `/to-issues`, and `/tdd`.

**What it does**

- Shows the proposed command chain first and waits for approval
- Interviews the user one section at a time with numbered options
- Uses explorer sub-agents where codebase context can sharpen the prompt
- Sends the draft prompt to the user for review before finalizing it
- Ends with the exact next chain: `/grill-with-docs` -> `/to-prd` -> `/to-issues` -> `/tdd`

**Example prompts**

| Mode | Example prompt |
| --- | --- |
| Full delivery chain (legacy) | `Create a full feature prompt for stock transfer approvals` |
| PRD-ready feature (legacy) | `Use feature-prompt-full for ADMIN-WEB and API-SERVICE invite changes` |
| TDD-ready handoff (legacy) | `Prepare a full feature chain for scanner reliability work` |

### `ubiquitous-language` (deprecated)

> **Deprecated.** Source lives at
> [`skills/deprecated/ubiquitous-language/`](skills/deprecated/ubiquitous-language/SKILL.md)
> for reference only. Domain-language sharpening is now covered by Matt
> Pocock's `/grill-with-docs`, which updates `CONTEXT.md` and ADRs inline as
> decisions crystallise. Do not install for new workflows.

Creates or updates a DDD-style `UBIQUITOUS_LANGUAGE.md` glossary from the
current conversation and local domain context. Based on Matt Pocock's
deprecated `ubiquitous-language` skill.

**What it does**

- Extracts domain terms, roles, workflows, states, and business concepts
- Chooses canonical names and lists aliases to avoid
- Flags ambiguous, overloaded, or conflicting terminology
- Adds relationships, an example dialogue, and open questions
- Updates an existing `UBIQUITOUS_LANGUAGE.md` instead of replacing it blindly

**Example prompts**

| Mode | Example prompt |
| --- | --- |
| New glossary | `Create a ubiquitous language glossary from this conversation` |
| Terminology cleanup | `Harden our domain language for stock transfers` |
| Existing glossary update | `Update UBIQUITOUS_LANGUAGE.md with what we just discussed` |

## Using a Skill (Quick Walkthrough)

1. **Install:** run the `npx skills install …` command for the skill you want.
2. **Ask your agent:** use a natural request that matches the skill — e.g.
   "Generate release notes for today" or "Create a feature prompt for MOBILE-APP".
3. **Review the output:** feature prompts write markdown files under
   `docs/prompts/` while release notes write date files under
   `docs/release-notes/`; discovery skills return structured markdown in the
   conversation.

The skills avoid changing your git state unless their own instructions say
otherwise. Skills that inspect history only read commits already available on
your machine.

## Agent Runtime Behavior

The main session acts as an **orchestrator**: it splits work into role-typed
lanes (Explorer, Researcher, Planner, Implementer, Reviewer, Tester,
Tool-runner), dispatches each to a **local** subagent, runs independent lanes
in parallel, and pushes long or noisy lanes to local background/async — so the
main chat stays responsive and its context stays clean. Subagents return
summaries; the main session keeps the only merge and final-judgment seat.

**Local only — no cloud agents.** These skills never delegate to cloud or
remote background-agent products (Cursor Cloud Agents, GitHub Copilot cloud
coding agent, Codex Cloud, Antigravity managed/remote execution). Local
worktree-isolated parallel agents are fine; remote ones are not.

| Runtime | Parallel dispatch | Local background |
| --- | --- | --- |
| Codex CLI | `[features] multi_agent` + `spawn_agent` (≤6 threads) | local worktrees; Automations |
| Claude CLI | Multiple `Agent` calls in one turn | `run_in_background` Bash; `background:` subagents; `isolation: worktree` |
| Antigravity CLI | `/goal` dynamic subagents (Agent Manager, ~5) | `/schedule` local background |
| Cursor CLI | Multiple `Task` calls (cap ~4); local worktree agents | `is_background` subagent + `Await` |
| Opencode CLI | multiple `task` calls (`subagent_type`) | `task(background=true)` + `task_status` |
| GitHub Copilot CLI | `/fleet` (parallel subagents) | `Ctrl+X → b` background shell |

The main agent still owns final judgment and output quality. Subagents collect
facts and run lanes; they do not replace the final synthesis.

Runtime-specific tool-calling docs for `agents-md` live under
`skills/agents-md/references/` — start with [`tool-calling.md`](skills/agents-md/references/tool-calling.md)
(agent orchestration model, canonical role lanes, local-only policy, CLI
tool names, permissions), then `cursor-tools.md`, `claude-tools.md`,
`codex-tools.md`, `copilot-tools.md`, `antigravity-tools.md`,
and `opencode-tools.md`.

## Contributing a New Skill

1. Create a new folder under `skills/your-skill-name/`.
2. Add a `SKILL.md` with frontmatter (`name`, `description`) followed by the
   instructions the agent should follow.
3. Add a `README.md` describing the skill for humans.
4. Optionally add `references/` for on-demand docs (examples, trigger
   phrases) and `assets/` for templates and other static resources, per the
   [spec conventions](https://agentskills.io/specification).
5. Open a PR.

Keep skill instructions deterministic and example-driven — skills work best
when they spell out exactly what to do, what to avoid, and what good output
looks like.

## License

[MIT](LICENSE) © Arfeen Arif

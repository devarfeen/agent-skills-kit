# Agent Skills Kit

A collection of reusable **skills** for AI coding agents (Claude Code, Cursor CLI / IDE,
and any agent runtime that supports the [`skills`](https://www.npmjs.com/package/skills)
package format).

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
    ├── agents-md/            # Generate AGENTS.md (Cursor canonical) plus CLAUDE.md/GEMINI.md shims
    │   ├── SKILL.md          # Required: metadata + instructions
    │   └── references/
    │       ├── tool-calling.md       # Tool-calling hub (Cursor CLI names, Task, permissions)
    │       ├── cursor-tools.md       # Skill-kit → Cursor mapping
    │       ├── caveman-invocation.md # Per-runtime caveman invoke
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

**Cursor CLI / IDE:** Install with `npx skills install` (skills land in
`~/.cursor/skills/` or `.cursor/skills/`), or add the repo under Cursor Settings →
Rules → Remote Rule (GitHub). Invoke a skill with `/skill-name` in Agent chat
(for example `/release-notes`). Run the CLI with `agent` for interactive sessions
or `agent -p "..."` for scripts and CI.

## Workflow Guide

See [Workflow.md](Workflow.md) for the recommended workflow from
workspace setup and spec creation through issues, TDD implementation, PR
shipping, and release notes. If you use Matt's engineering skills, run
`/setup-matt-pocock-skills` once per repo before `/to-prd`, `/to-issues`,
`/triage`, `/diagnose`, `/tdd`, `/improve-codebase-architecture`, or
`/zoom-out`. The workflow also defines an optional `Suggested next skills`
footer pattern (recommendations only) so agents can append lightweight
before/after reminders at the end of non-trivial responses, including after
third-party skills.

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
  in this repo into a 14-rule core plus retained operational defaults:
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
  including `setup-matt-pocock-skills`, `grill-me`, `grill-with-docs`,
  `to-prd`, `to-issues`, `tdd`, `diagnose`, `triage`,
  `improve-codebase-architecture`, `zoom-out`, `prototype`, and `handoff`:
  https://github.com/mattpocock/skills
- `/caveman` is credited to Matt Pocock's `caveman` skill, MIT License,
  Copyright 2026 Matt Pocock:
  https://github.com/mattpocock/skills/blob/main/skills/productivity/caveman/SKILL.md
  Generated `AGENTS.md` files invoke caveman as a
  non-negotiable rule for chat output only — never for code, docs, PRDs,
  release notes, PR bodies, or any persisted artifact.
- `/skill-creator` is credited to Anthropic's public skills repository:
  https://github.com/anthropics/skills/tree/main/skills/skill-creator
- `/agent-browser`, the `skills` CLI, `find-skills`, and Vercel React/React
  Native best-practice skills are credited to Vercel Labs:
  https://github.com/vercel-labs/agent-browser
  https://github.com/vercel-labs/skills
  https://github.com/vercel-labs/agent-skills
- `/sentry` refers to Sentry's CLI for developers and agents:
  https://cli.sentry.dev/
- **Cursor CLI / IDE:** `AGENTS.md` is the canonical workspace context file;
  skills use `/skill-name` invocation and the `Task` tool for subagents.
  https://cursor.com/docs/cli/overview
  https://cursor.com/docs/context/skills

## Available Skills

### `agents-md`

Generates `AGENTS.md` as the canonical agent instruction file and creates
`CLAUDE.md` / Antigravity-compatible `GEMINI.md` shims that point to it.

```bash
npx skills install https://github.com/devarfeen/agent-skills-kit --skill agents-md
```

**What it does**

- Includes a 14-rule non-negotiable core in `AGENTS.md`, plus retained operational defaults for chat-only, 5th-grade-English caveman activation, full Project Matrix code usage, and parallel execution
- Uses `AGENTS.md` as canonical for Cursor CLI / IDE (no extra shim); creates `GEMINI.md` as an Antigravity CLI compatibility shim because Antigravity CLI reads it as workspace context
- Detects VS Code workspaces and uses each folder `name` as the project name/code source
- Treats the workspace folder with `path: "."` as a meta workspace with no code
- Builds a project matrix: `Project Name (Code) | Path | Tech Stack`
- Establishes stable project codes for use across prompt, PRD, issue, discovery, release-note, PR, commit, and code-comment contexts
- References `CONTEXT.md` and `docs/adr/` as required domain context when available (and legacy `UBIQUITOUS_LANGUAGE.md` if it exists)

**Example prompts**

| Mode | Example prompt |
| --- | --- |
| New instructions | `Generate AGENTS.md for this workspace` |
| VS Code workspace | `Create AGENTS.md and shims from my VS Code workspace` |
| Refresh project matrix | `Update AGENTS.md project codes and tech stacks` |

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
`<artifacts-root>` resolves to the VS Code workspace root when a
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
- Flags code-discovered domain terms that may be missing from or stale in
  `CONTEXT.md`, with short descriptions and evidence for user approval
- Updates `CONTEXT.md` only as an explicit follow-up after the user approves
  specific terms or accepts the full candidate list
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
- When cheap exploration reveals missing or stale domain terms, shows candidate
  `CONTEXT.md` updates with short descriptions for user approval
- Applies approved `CONTEXT.md` updates only as a separate documentation step
- Sends non-trivial or inferred drafts to the user for one correction pass
- Saves the final prompt to `<artifacts-root>/docs/prompts/NNNN-<feature-slug>-prompt.md` (sibling of `docs/adr/`; prompt and ADR filenames both start with `NNNN-<slug>`, and numbering is shared with ADRs only). `<artifacts-root>` is the VS Code workspace root when present, otherwise the repo root — artifacts stay out of individual project repos whenever a workspace exists.
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
- Enforces zero-attribution output across supported coding-agent paths (Cursor, Claude Code, Codex, Copilot, Antigravity, Opencode, and equivalent wrappers): no `Co-authored-by`, `Made-with`, `Generated by`, or AI signature lines
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
- Enforces zero-attribution output across supported coding-agent paths (Cursor, Claude Code, Codex, Copilot, Antigravity, Opencode, and equivalent wrappers): no `Co-authored-by`, `Made-with`, `Generated by`, or AI signature lines
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

When the agent runtime supports sub-agents and the user allows them, these
skills may use multiple read-only explorer agents for independent discovery
work. This is most useful for multi-repo workspaces, separate modules, or
parallel evidence gathering.

| Runtime | Subagent dispatch | Skill invocation |
| --- | --- | --- |
| Cursor CLI / IDE | `Task` tool (`subagent_type`) or `.cursor/agents/*.md` | `/skill-name` |
| Claude Code | Native sub-agents | `/skill-name` |
| Codex CLI | `spawn_agent` / `wait_agent` | `activate("skill")` |
| Copilot CLI | `task` with `agent_type` | `skill("name")` |
| Antigravity CLI | `@agent-name` | `activate_skill(name="...")` |

The main agent still owns final judgment and output quality. Explorer agents
collect facts; they do not replace the final synthesis.

Runtime-specific tool calling docs for `agents-md` live under
`skills/agents-md/references/` — start with [`tool-calling.md`](skills/agents-md/references/tool-calling.md)
(Cursor CLI tool names, `Task`/subagents, permissions), then `cursor-tools.md`, `claude-tools.md`, etc.

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

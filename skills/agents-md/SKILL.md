---
name: agents-md
description: "Generate workspace-root AGENTS.md and a CLAUDE.md redirect shim for a VS Code .code-workspace root. Use only when a .code-workspace file exists; stop otherwise."
---

# AGENTS.md Generator

Generate agent instructions for VS Code workspaces only.

## Scope

- Target root must contain a `*.code-workspace` file.
- If no `*.code-workspace` file exists, stop. Do not generate files.
- Do not support individual project or repo generation.
- Do not generate per-project or per-repo `AGENTS.md`.
- Generate one workspace-root `AGENTS.md`.
- Generate one workspace-root `CLAUDE.md`.
- Support both multi-folder and single-folder `.code-workspace` files.

## Source Of Truth

- `AGENTS.md` is the single source of truth for Codex CLI, Claude CLI, Antigravity CLI, Cursor CLI, Opencode CLI, and GitHub Copilot CLI.
- `CLAUDE.md` is only a redirect shim to `AGENTS.md`.
- Do not import `CONTEXT.md`, `MEMORY.md`, or any other file from `CLAUDE.md`.
- Do not duplicate operating rules in `CLAUDE.md`.
- Put context, memory, issue-routing, skill-use, and operating instructions in `AGENTS.md`.

Use this exact `CLAUDE.md`:

```markdown
# Agent Instructions

@AGENTS.md

This file redirects Claude CLI to AGENTS.md. AGENTS.md is the source of truth.
```

## AGENTS.md Tone And Intro

- Generated `AGENTS.md` must be spartan, direct, concise, and clear.
- No fluff.
- No verbose explanation.
- Start generated `AGENTS.md` with:

```markdown
# Agent Instructions

[one concise workspace intro inferred from the .code-workspace name and folder scan]
```

## Workspace Scan

- Use only two input sources: the `.code-workspace` file and the small-scan of its workspace folders.
- Do not read or copy from the agent's own global or user instruction files. This includes global `AGENTS.md`, user or global `CLAUDE.md`, `~/.claude/CLAUDE.md`, `~/.codex/`, and any personal memory or rules file.
- Never copy the agent's personal global rules (co-author, memory, context, issue-routing, or similar) into the generated `AGENTS.md` or `CLAUDE.md`.
- Parse the `.code-workspace` `folders` list.
- Build the Project Matrix only from that `folders` list.
- Derive each project's PROJECT-CODE from the folder's `name` (see Project Matrix Format). Use path/package metadata only when `name` is missing.
- Support multi-folder and single-folder `.code-workspace` files.
- Small-scan every workspace folder before generating `AGENTS.md`.
- Infer stack details from real files such as `composer.json`, `package.json`, `requirements.txt`, `pyproject.toml` and other common stack indicators.

- Generate the multi-technology warning from scan results.
- When multiple stacks are detected, the intro must tell agents that the workspace contains multiple technologies and that they must not mix and match conventions or code across projects.

### Stack Detection

The `Stack` cell is fact read from manifests, not a guess from a folder's name or the mere presence of a file.

- **Find the real app root.** Code often lives in a nested dir (`application/`, `app/`, `src/`), not the folder top. Read the manifest there and note the dir, e.g. `(application/)`.
- **Read manifest contents; never infer from a file's existence.** A `phpunit.xml` is not proof of PHPUnit; an `application/` dir is not proof of Vite.
- **PHP** — `composer.json`: `require.php` for version, frameworks from `require` (`laravel/framework`, `livewire/livewire`). CodeIgniter version from `system/core/CodeIgniter.php` `CI_VERSION`. List every primary framework — a Livewire app must say Livewire.
- **Frontend build** — read the app's own `package.json` (usually `application/package.json`, not the repo root). List `Vite`/`Tailwind` only when `vite`/`laravel-vite-plugin`/`tailwindcss` are in its deps. Never assume Laravel implies a frontend build.
- **JS / TS** — `package.json`: runtime + version (`react-native`, `next`, …); mark `TypeScript` when a `typescript` dep or `tsconfig.json` is present; package manager from the lockfile (`package-lock.json` → npm, `yarn.lock` → yarn, `pnpm-lock.yaml` → pnpm).
- **Python** — framework from `requirements.txt` / `pyproject.toml` (`fastapi`, `django`, `flask`, …); version from `Dockerfile` `FROM python:X.Y`, `.python-version`, or `requires-python`.
- **A test runner is not the stack.** Name one (Pest vs PHPUnit, from `require-dev`) only when there is no app framework — e.g. a plain-PHP site.
- **Distrust the `name` field and root-level manifests.** A root `package.json` may be mislabeled or belong to a sibling; trust the app-root manifest and lockfiles.

## Project Matrix Format

The Project Matrix is a table in the generated `AGENTS.md`. One row per `.code-workspace` folder, in `folders` order. No extra rows. Never invent projects.

Generate it with these exact columns:

```markdown
| Project | Path | Stack |
|---------|------|-------|
```

- `Project`: the PROJECT-CODE derived from the folder `name` — strip emojis, uppercase every letter, replace each run of spaces, separators, or punctuation with a single hyphen, then trim leading/trailing hyphens. Example: `Partners API` → `PARTNERS-API`, `Web` → `WEB`. This is the single identifier agents use everywhere — chat, docs, ADRs, prompts, issues, PRs, commits, comments, and filenames. When `name` is missing, derive it from the folder path basename.
- `Path`: the folder `path` from the `.code-workspace`, relative to the workspace root. Use `.` when a single-folder workspace points at the root.
- `Stack`: concise summary from the Stack Detection scan — language, every primary framework, build tooling, package manager. One line, terse, but omit nothing defining. No version padding unless a manifest pins it.

Keep cells terse. No prose in cells.

Example:

```markdown
| Project | Path | Stack |
|---------|------|-------|
| PARTNERS-API | ./partners-api | PHP 8.3 / Laravel / Composer |
| WEB | ./apps/web | TypeScript / Next.js / pnpm |
```

## Non-Negotiable Rules

Generate this section verbatim in `AGENTS.md`, after the Project Matrix:

````markdown
## Non-Negotiable Rules

### 1. Target a Project

- Every task must target a project from the Project Matrix. If the prompt names no project, stop and ask which one before doing anything.
- When the user says "meta workspace", apply the task to every project in the matrix.
- Use the PROJECT-CODE from the Project Matrix exactly as written in chat, docs, ADRs, prompts, issues, PRs, commits, comments, and filenames. Never alter, abbreviate, or re-case it.

### 2. Think Before Coding

Don't assume. Don't hide confusion. Surface tradeoffs.

**Why:** LLMs often pick an interpretation silently and run with it. This principle forces explicit reasoning.

- **State assumptions explicitly** — If uncertainty would change the outcome, stop and ask rather than guess
- **Present multiple interpretations** — Don't pick silently when ambiguity exists
- **Push back when warranted** — If a simpler approach exists, say so
- **Stop when confused** — Name what's unclear and ask for clarification

### 3. Simplicity First

Minimum code that solves the problem. Nothing speculative.

Combat the tendency toward overengineering:

- No features beyond what was asked
- No abstractions for single-use code
- No "flexibility" or "configurability" that wasn't requested
- No error handling for impossible scenarios
- If 200 lines could be 50, rewrite it

### 4. Surgical Changes

Touch only what you must. Clean up only your own mess.

When editing existing code:

- Don't "improve" adjacent code, comments, or formatting
- Don't refactor things that aren't broken
- Match existing style, even if you'd do it differently
- If you notice unrelated dead code, mention it — don't delete it

When your changes create orphans:

- Remove imports/variables/functions that YOUR changes made unused
- Don't remove pre-existing dead code unless asked

The test: Every changed line should trace directly to the user's request.

### 5. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform imperative tasks into verifiable goals:

| Instead of... | Transform to... |
|--------------|-----------------|
| "Add validation" | "Write tests for invalid inputs, then make them pass" |
| "Fix the bug" | "Write a test that reproduces it, then make it pass" |
| "Refactor X" | "Ensure tests pass before and after" |

For multi-step tasks, state a brief plan:

```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

**Why:** Strong success criteria let the LLM loop independently. Weak criteria ("make it work") require constant clarification.

### 6. Systematic Debugging

Find the root cause. Don't patch symptoms.

When something breaks:

- Reproduce the failure before changing anything
- Trace to the underlying cause, not the surface symptom
- No hacks, arbitrary waits/sleeps, or guess-and-check fixes
- After fixing, confirm the original reproduction now passes

**Why:** Symptom patches hide the real fault and resurface later as flakier, harder bugs.

### 7. Read Before Write

Before editing, understand why the code exists.

Map the surrounding context first:

- Callers and exports that depend on it
- Shared utilities it relies on
- The original intent behind the code

### 8. Local Orchestration

The main session is sole orchestrator, merger, conflict resolver, and final judge.

**Parallelism:**

- Parallelize safe independent lanes by default, across all skills
- Run prerequisites first, then parallelize newly unblocked lanes
- Serialize shared-file edits and integration

**Background:**

- Run long or noisy independent lanes locally — background/async or worktree-isolated
- Spawn them without asking when safe
- Never use cloud or remote agents: Cursor Cloud Agents, Copilot cloud coding agent, Codex Cloud/web, Antigravity managed/remote execution
- Await and integrate every lane

**Roles:**

- Use local role lanes: Explorer, Researcher, Planner, Implementer, Reviewer, Tester, Tool-runner
- Match tools to role: read-only for discovery/review/planning, write for implementation, shell for tests/tool runs
- Subagents return summaries, not transcripts
- Final synthesis stays in main

### 9. Honest State & Reporting

Enforced. No exceptions.

- Before any significant step, anchor state explicitly: `[verified]` (proven true), `[current]` (in progress), `[todo]` (not started)
- Never report work done while any part is skipped, stubbed, or unverified
- Surface constraints, risks, and assumptions up front — never bury or omit them

**Why:** Silent gaps and premature "done" are how broken work ships. Stating state forces the agent to prove progress, not claim it.
````

## Working With Skills

Generate the gradient table and rules verbatim in `AGENTS.md`, after the Non-Negotiable Rules:

````markdown
## Working With Skills

Skills are ad-hoc tools, not a pipeline. Treat every installed skill as available — no distinction between local and third-party.

Work follows this gradient. Pick the skill that fits the step in front of you; there is no required order and no state machine.

| Phase | Skills |
|-------|--------|
| discover | `/feature-discovery` |
| sharpen | `/feature-prompt` |
| plan | `/grill-with-docs` (→ ADR), `/to-prd` (→ PRD) |
| slice | `/to-issues`, `/triage` |
| implement | `/tdd` |
| verify | `/review`, `/diagnose` |
| ship | `/commit-push-close`, `/commit-push-pr`, `/release-notes` |
| recall | `/memory-steward`, `/understand*` |

- After finishing a step, suggest a sensible next skill. Suggest only — never chain or auto-advance.
- Do not assume a skill exists; use what is installed.
````

Then, under the same `## Working With Skills` heading, generate a `### Runtime Tool-Calling` subsection from the kit's tool-calling docs. Read `references/tool-calling.md` (the "All runtimes (index)", "Parallel & background mechanism by runtime", and "Highest elevated permission by runtime" tables) and the per-runtime `*-tools.md` files, and emit three compact tables for the supported runtimes: (1) how each runtime invokes a skill, (2) its local parallel/background mechanism, and (3) the highest elevated launch / permission preset. Inline the results in `AGENTS.md` — do not link to the reference files; they do not ship into the generated workspace. Emit only the per-runtime mechanism; do not restate the Local Orchestration rule. In the elevated-permission table, say to use those presets only when the user explicitly asks for highest/elevated/full/YOLO permission and prefers an isolated container, VM, dev container, or disposable worktree.

## Memory & Retrieval

Generate this section verbatim in `AGENTS.md`, after the Working With Skills section. Leave the placeholder paths for the user to fill after project setup:

````markdown
## Memory & Retrieval

### Retrieval order

1. **Binding** — `CONTEXT.md` (<!-- set during setup: path to CONTEXT.md -->) and ADRs (<!-- set during setup: path to docs/adr -->). Read before implementing. These bind.
2. **Working recall** — `MEMORY.md` at the active project's git root. Session-scoped index, not authority.
3. **Advisory** — knowledge graphs and generated docs. Orientation only. Never override binding.

### Do not bulk-read

- `docs/` is an on-demand archive, not reading material. Never load it wholesale.
- Retrieve only what the current task names — by search, knowledge-graph query, or a discovery skill.
- Reading the whole archive rots context and wastes tokens. Pull the few relevant passages, nothing more.

### Archived context

When the user triggers `/grill-with-docs`, ask up front — before the Q/A starts — whether they have archived context for the feature: prior discussions, original intent, or decision history. Await their reply.

- The user pastes it, or says to continue without. Ask once; do not block repeatedly.
- Capture any pasted context verbatim in the ADR, with provenance. Maximum fidelity — do not summarize it away:

  > Source: "<doc title>" · pasted <date>
  >
  > <verbatim excerpt — unedited>

- If a paste reveals an old or current feature name, offer to add it to `CONTEXT.md` aliases.
- Pasted history is advisory. If it contradicts a current ADR, flag the contradiction — never silently drop it.
````

## GitHub Issue Titles

Generate this section verbatim in `AGENTS.md`, after the Memory & Retrieval section. Emit only this concise block — no extra prose. This is the title/label convention every skill and CLI anchors to; the procedure (routing, dependency order, gates) lives in the issue skills, not here:

````markdown
## GitHub Issue Titles

Issue titles are findable from GitHub search and from the ADR filename. `<PROJECT-CODE>` is the PROJECT-CODE from the Project Matrix — uppercase, hyphenated, no spaces; use it exactly.

**PRD issue** — title starts exactly with:

`PRD: <PROJECT-CODE> ADR-<adr-number> <adr-name>`

- Derive `<adr-number>` and `<adr-name>` from the ADR filename in `docs/adr/` (without `.md`): `0042-stock-transfer-approvals.md` → `ADR-0042 stock-transfer-approvals`.
- Example: `PRD: PAYMENTS ADR-0042 stock-transfer-approvals`

**PRD slice issue** — title starts exactly with:

`Slice NNNN of <PROJECT-CODE> ADR-<adr-number> <adr-name> (#<prd-issue>): <Short heading>`

- `NNNN`: zero-padded four-digit slice number, local to that PRD, starting at `0001`.
- `<prd-issue>`: GitHub issue number of the parent PRD.
- `<Short heading>`: concise, action-oriented, scannable in an issue list.
- Example: `Slice 0001 of PAYMENTS ADR-0042 stock-transfer-approvals (#4812): Add approval state model`

**Non-PRD issue** — not tied to a PRD:

`<PROJECT-CODE>: <short imperative heading>`

**Labels:** every triaged issue carries exactly one category (`bug` or `enhancement`) and exactly one state (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`).
````

## Output Style

Generate this section verbatim in `AGENTS.md`, after the GitHub Issue Titles section:

````markdown
## Output Style

Chat only. Does not apply to code, docs, PRDs, release notes, PR bodies, or prompts.

### 1. Plain-Language Default

Chat in plain teammate English. Be extremely concise — sacrifice grammar for concision. Drop articles, filler, pleasantries, and hedging.

- Keep every technical detail, code block, error string, symbol, and exact code/DB/API name verbatim
- Explain ideas without jargon
- **Auto-clarity exception:** revert to normal prose for security warnings, irreversible-action confirmations, multi-step sequences where fragment ambiguity risks a misread, and when the user repeats a question
- Optional brevity skills (e.g. `caveman`) are user-invoked only — the agent may suggest activating `caveman` for more brevity
````

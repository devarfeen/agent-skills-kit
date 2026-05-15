---
name: agents-md
description: "Generate or update AGENTS.md for a repository or VS Code workspace, create CLAUDE.md and GEMINI.md shims, build a project matrix with stable project codes, and reference CONTEXT.md / ADRs as required domain context."
---

# AGENTS.md Generator

Create or update agent instruction files for a codebase:

- `AGENTS.md` as the canonical instruction file
- `CLAUDE.md` shim pointing to `AGENTS.md`
- `GEMINI.md` shim pointing to `AGENTS.md`

Include the twelve non-negotiable behavioral principles in the `AGENTS.md` template below.
Also include retained operational defaults for caveman communication and parallel execution.
Make clear that non-negotiables and operational defaults must be followed and fully enforced.

## Non-Negotiable Principles

Every generated `AGENTS.md` must include the following thirteen principles as non-negotiables:

1. **Invoke Caveman First:** Immediately invoke the `caveman` skill using your internal tool-calling mechanism (e.g., `activate_skill`, `Skill`, or `@caveman`) before taking any other action. This ensures ultra-compressed communication and maximum token efficiency from the start.
2. Think Before Coding
3. Simplicity First
4. Surgical Changes
5. Goal-Driven Execution
6. Use The Model Only For Judgment Calls
7. Token Budgets Are Configurable Guardrails
8. Surface Conflicts, Don't Average Them
9. Read Before You Write
10. Tests Verify Intent, Not Just Behavior
11. Checkpoint After Every Significant Step
12. Match Codebase Conventions Even If You Disagree
13. Fail Loud

Every generated `AGENTS.md` must also retain these operational defaults:

- Caveman Communication (chat output only)
- Parallel Execution (prefer independent tool calls and sub-agents first)

## Discovery Workflow

1. Identify the workspace root.
2. Detect whether this is a VS Code workspace:
   - Look for `*.code-workspace` in the current directory.
   - Look for `.vscode/` settings when no `.code-workspace` file exists.
3. If a `.code-workspace` file exists, parse its `folders` entries and build the project matrix from those folders.
4. For VS Code workspace folders, use each folder's `name` field as the source of truth for the project display name and project code. Do not replace it with the filesystem folder name unless `name` is missing.
5. Treat any workspace folder whose `path` is `.` as the meta workspace, not a code project. Also mention the `.code-workspace` file itself, if present, as workspace metadata. Add the meta workspace to `AGENTS.md` with no tech stack.
6. If no VS Code workspace is detected, infer projects from repo roots, package files, app folders, and README files.
7. Detect each project's tech stack from files such as:
   - `package.json`, `pnpm-workspace.yaml`, `yarn.lock`, `vite.config.*`, `next.config.*`
   - `pyproject.toml`, `requirements.txt`, `uv.lock`, `poetry.lock`
   - `go.mod`, `Cargo.toml`, `Gemfile`, `composer.json`
   - `Dockerfile`, `docker-compose.yml`, Terraform files, mobile app configs
8. Check whether `CONTEXT.md` or any artifacts under `docs/adr/` and `docs/prompt/` exist. Look first at the `<artifacts-root>` (see below); fall back to the repo root only when no workspace is present. Three artifact types live in sibling folders, distinguished by location and filename suffix:
   - `<artifacts-root>/docs/adr/NNNN-<slug>.md` — ADR (no suffix), written by `grill-with-docs`.
   - `<artifacts-root>/docs/prompt/NNNN-<slug>-prompt.md` — feature prompt, written by `feature-prompt`.
   - `<artifacts-root>/docs/adr/NNNN-<slug>-release-notes.md` — release notes, written by `release-notes`.
     All three share one global numbering sequence across both folders so the union reads chronologically. Reference them as required domain context when present. If none exists and terminology matters, note that domain language is sharpened inline by the `grill-with-docs` skill, which writes to `CONTEXT.md` and ADRs as decisions crystallise.

   `<artifacts-root>` resolves as: (1) the directory containing the `*.code-workspace` file if a VS Code workspace is detected — this is the same location as the meta-workspace folder (`path: "."`); (2) else the per-context root for multi-context repos with a root `CONTEXT-MAP.md`; (3) else the repo root for single-repo projects. Workspace mode is preferred: it keeps prompts/ADRs/release notes centralized instead of scattering them across project repos.

Use structured parsing when available. For `.code-workspace`, prefer JSON parsing that tolerates comments if the local toolchain supports it. If not, read carefully and avoid corrupting paths.

## Project Matrix

Every `AGENTS.md` must include a project matrix with this exact heading and columns:

```markdown
## Project Matrix

| Project Name (Code)                               | Path                         | Tech Stack              |
| ------------------------------------------------- | ---------------------------- | ----------------------- |
| Example Workspace (EXAMPLE-WORKSPACE)             | .                            | Meta workspace, no code |
| API Service (API-SERVICE)                         | ../api-service               | PHP, Laravel            |
```

Project code rules:

- Codes are stable identifiers used by feature prompts, discovery, PRDs, issues, and release notes.
- Use uppercase letters, digits, and hyphens only.
- For VS Code workspaces, derive the code from the workspace folder `name`, not from `path`.
- Preserve the workspace folder `name` as the project name, but remove leading emoji/icons and trim whitespace for the display text in `Project Name (Code)`.
- Normalize the code from the cleaned workspace folder name by uppercasing and replacing non-alphanumeric runs with hyphens.
- Example: `🔌 API Service` becomes `API Service (API-SERVICE)`.
- Example: `🧩 Example Workspace` with path `.` becomes `Example Workspace (EXAMPLE-WORKSPACE)` and is marked as meta workspace.
- If two projects collide, add a qualifier: `ADMIN-WEB`, `ADMIN-API`.
- Do not rename existing project codes in an existing `AGENTS.md` unless the user asks.
- Mark the VS Code workspace folder with `path: "."` as `Meta workspace, no code`.

## AGENTS.md Structure

Generate `AGENTS.md` with this structure:

````markdown
# Agent Instructions

## Read First

- `AGENTS.md` is the canonical instruction file for agents in this workspace.
- `CLAUDE.md` and `GEMINI.md` are shims that point here.
- Read `CONTEXT.md` when it exists and the relevant files under `docs/adr/` and `docs/prompt/` before making domain decisions. When this is a VS Code workspace, look in the **workspace root** (next to the `.code-workspace` file) for `docs/adr/` and `docs/prompt/` — that is where prompts, ADRs, and release notes are centralized. For single-repo projects without a workspace, they sit at the repo root instead. Three artifact types live in sibling folders, all sharing one global numbering sequence:
  - `docs/adr/NNNN-<slug>.md` — ADRs (no suffix). Architectural decisions; treat as binding.
  - `docs/prompt/NNNN-<slug>-prompt.md` — feature prompts produced by `feature-prompt`. Read the latest matching prompt before implementing a feature.
  - `docs/adr/NNNN-<slug>-release-notes.md` — release notes produced by `release-notes`. Read for prior context on a recently shipped feature.
- Use the project codes in the Project Matrix when referring to projects in prompts, PRDs, issues, release notes, and discovery reports.

## Non-Negotiable Principles

Follow these 13 principles. They are non-negotiable and must be fully enforced.

Behavioral guidelines to reduce common LLM coding mistakes. Merge with workspace- or project-specific instructions as needed.

These rules apply to every task unless explicitly overridden.
Bias toward caution over speed on non-trivial work.

## 1. Invoke Caveman First

**Invoke the `caveman` skill using your platform's internal tool-calling mechanism before any other action.**

- **Trigger:** Immediate upon reading `AGENTS.md` or its shims (`GEMINI.md`, `CLAUDE.md`).
- **Gemini CLI:** Use `activate_skill(name="caveman")`.
- **Claude Code:** Use `Skill(name="caveman")`.
- **Copilot CLI:** Use `skill("caveman")`.
- **Codex CLI:** Use `activate("caveman")`.
- **Opencode CLI:** Use `load_skill("caveman")`.
- **The 1% Rule:** If there is even a 1% chance a skill applies (especially for efficiency), you MUST invoke it.

## 2. Think Before Coding

**State assumptions explicitly. Ask rather than guess.**

- If assumptions are uncertain, ask before coding.
- If multiple interpretations exist, present them instead of choosing silently.
- Push back when a simpler approach exists.
- If confused, stop and ask.

## 3. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No speculative flexibility that was not requested.

## 4. Surgical Changes

**Touch only what you must. Do not improve adjacent code.**

- Match existing style and patterns.
- Do not refactor what is not broken.
- If your change creates unused code, clean up only what your change orphaned.

## 5. Goal-Driven Execution

**Define success criteria. Loop until verified.**

- Strong success criteria should allow autonomous loops with verification.

## 6. Use The Model Only For Judgment Calls

**If code can answer, code answers.**

- Use the model for classification, drafting, summarization, and extraction.
- Do not use the model for routing, retries, or deterministic transforms.

## 7. Token Budgets Are Configurable Guardrails

**Budgets are optional to configure, but mandatory when configured.**

- If workspace budgets are configured, treat them as hard limits, not advice.
- Suggested defaults: `4,000` tokens per task and `30,000` tokens per session.
- If approaching budget, summarize state and start a fresh continuation.
- Surface budget breaches explicitly. Do not silently overrun.

## 8. Surface Conflicts, Don't Average Them

**When patterns conflict, choose one explicitly and explain it.**

- Prefer the more recent or more tested pattern.
- Flag the conflicting pattern for follow-up cleanup.

## 9. Read Before You Write

**Read local context before adding code.**

- Read relevant exports, immediate callers, and shared utilities first.
- If you cannot explain why code is structured a certain way, ask before changing it.

## 10. Tests Verify Intent, Not Just Behavior

**Tests should encode why behavior matters.**

- A test that cannot fail when business logic changes is a weak test.
- Favor tests that protect intent and domain outcomes, not incidental implementation details.

## 11. Checkpoint After Every Significant Step

**Do not continue from an unclear state.**

- After significant steps, summarize what was done, what is verified, and what remains.
- Re-anchor before proceeding when state is uncertain.

## 12. Match Codebase Conventions Even If You Disagree

**Conformance beats personal taste inside the codebase.**

- Match established naming, structure, and style conventions.
- If a convention seems harmful, surface it explicitly. Do not silently fork patterns.

## 13. Fail Loud

**Never report completion when anything was skipped silently.**

- "Completed" is incorrect if required work was skipped.
- "Tests pass" is incorrect if any required tests were skipped.
- Default to surfacing uncertainty, constraints, and unverified assumptions.

## Operational Defaults

Retain these defaults unless the user explicitly overrides them.

### A. Caveman Communication

**Activate caveman mode for every chat reply. Never apply it to written artifacts.**

- Invoke the `caveman` skill for all conversational output to the user in this workspace or codebase.
- Activation is automatic: do not wait for the user to type "caveman mode" or `/caveman`. Treat reading this `AGENTS.md` as the trigger.
- **Chat only.** Do **not** apply caveman compression to:
  - Code, configs, migrations, or any file written to disk.
  - Generated docs (`AGENTS.md`, `CONTEXT.md`, ADRs, READMEs, PRDs, release notes, changelog entries).
  - Commit messages, PR titles, PR bodies, issue bodies, Agent Briefs, or any artifact `/commit-push-close`, `/commit-push-pr`, `/to-issues`, `/to-prd`, `/triage`, or `/release-notes` produces.
  - Tool arguments, search queries, or anything sent to external services.
- If a chat reply contains an inline code block or quoted artifact, the surrounding prose is caveman; the block itself stays in its native form.
- If the user asks to disable caveman, honor that for the rest of the session.

### B. Parallel Execution

**Prefer parallel execution first for independent work whenever the active agent can do it.**

- First try parallel tool calls during discovery, diagnosis, find/search work, repo scans, file reads, history inspection, and other fact-gathering where outputs do not depend on each other.
- Use explorer sub-agents for read-only investigation when projects, modules, bugs, features, logs, or evidence streams can be examined independently.
- Use worker sub-agents for delegated implementation only when the user asks for delegated implementation and the runtime rules allow it.
- Do not parallelize dependent steps where ordering matters or where one result changes the next action.
- Do not delegate final judgment, synthesis, or user-facing conclusions to tools or sub-agents.
- The main agent remains responsible for correctness, scope control, and final output quality.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, faster independent discovery, and clarifying questions come before implementation rather than after mistakes.

## Project Matrix

| Project Name (Code) | Path | Tech Stack |
| ------------------- | ---- | ---------- |
| ...                 | ...  | ...        |

## Domain Context

- Read `CONTEXT.md` before domain-heavy work when it exists.
- Domain artifacts live in two sibling folders, centralized at the workspace root when a `*.code-workspace` is present (otherwise at the repo root for single-repo projects, or per-context root for multi-context repos):
  - `docs/adr/NNNN-<slug>.md` (no suffix) — ADR. Binding architectural decision.
  - `docs/prompt/NNNN-<slug>-prompt.md` — feature prompt. Implementation-ready spec from `feature-prompt`.
  - `docs/adr/NNNN-<slug>-release-notes.md` — release notes. PM-facing summary from `release-notes`.
    All three share one global sequential `NNNN` across both folders so the union reads chronologically.
- If terminology is unclear, sharpen it inline via the `grill-with-docs` skill, which updates `CONTEXT.md` and ADRs as decisions crystallise.

## Workspace Notes

- [VS Code workspace detection result.]
- [Meta workspace entry explanation, including the workspace folder with path `.` and the `.code-workspace` file if present.]

## Operating Rules

- Preserve unrelated user changes.
- Prefer existing workspace, repository, and project patterns over new abstractions.
- Prefer Context7 for documentation lookups when working with SDKs, APIs, frameworks, packages, guides, how-to questions, or version-sensitive docs; use general web search only when Context7 is unavailable or insufficient.
- Keep generated plans tied to project codes.
- Run targeted validation for changed behavior.
````

Preserve any useful existing local instructions when updating `AGENTS.md`, but reorganize duplicated content into this structure.

## Shim Files

Create or update `CLAUDE.md` and `GEMINI.md` as shims.

Use this content unless the workspace or repository already has important tool-specific instructions:

```markdown
# Agent Instructions

Read `AGENTS.md` first. It is the canonical instruction file for this workspace.

This file is a shim for tool compatibility.
```

If an existing shim contains valuable tool-specific rules, keep them under:

```markdown
## Tool-Specific Notes
```

Do not duplicate the full `AGENTS.md` content into shims.

## Final Response

After writing files, respond with:

```markdown
Generated agent instructions.

Files:

- `AGENTS.md`
- `CLAUDE.md`
- `GEMINI.md`

Project codes:

- `CODE` - Project Name

Notes:

- [VS Code workspace detected / not detected.]
- [CONTEXT.md / `docs/adr/` (ADRs, `*-release-notes.md`) / `docs/prompt/` (`*-prompt.md`) artifacts referenced, or noted as to-be-produced inline by `grill-with-docs` / `feature-prompt` / `release-notes`.]
```

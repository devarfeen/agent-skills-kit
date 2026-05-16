---
name: agents-md
description: "Generate or update AGENTS.md for a repository or VS Code workspace, create CLAUDE.md and GEMINI.md shims, build a project matrix with stable project codes, and reference CONTEXT.md / ADRs as required domain context."
---

# AGENTS.md Generator

Create or update agent instruction files for a codebase:

- `AGENTS.md` as the canonical instruction file
- `CLAUDE.md` shim pointing to `AGENTS.md`
- `GEMINI.md` shim pointing to `AGENTS.md`

Include the thirteen spartan non-negotiable principles in the `AGENTS.md` template below.
Also include retained operational defaults for caveman communication and parallel execution.
Make clear that non-negotiables and operational defaults must be followed and fully enforced.

## Non-Negotiable Principles

Every generated `AGENTS.md` must include the following thirteen principles as non-negotiables:

1. **Invoke Caveman First:** Trigger the `caveman` skill using your platform's tool-calling mechanism (`activate_skill`, `Skill`, `skill`, `activate`, or `load_skill`) before any other action.
2. **Evidence Before Claim:** No claims (e.g., "tests pass") without raw command output. No evidence = not done. "Seems to" or "likely" = failure to verify.
3. **Task Isolation:** Use a fresh subagent or tool call for each independent task. Do not carry bloated history into isolated jobs.
4. **Goal-Driven Execution:** Define verifiable success criteria. For bug fixes, always verify the failure (Red) before applying the fix (Green).
5. **Surgical Minimalism:** Match style. Touch only what you must. No speculative abstractions, "just-in-case" code, or adjacent cleanup.
6. **Systematic Debugging:** Trace failures to their root cause. Do not patch symptoms with generic hacks, arbitrary timeouts, or unverified assumptions.
7. **Think & Ask:** Uncertainty = STOP & ask. Surface tradeoffs explicitly; never guess or choose a path silently.
8. **Read Before Write:** Map callers, exports, and shared utilities before modified files. Understand why code exists before changing how it works.
9. **Token Guardrails:** Treat token budgets as hard limits. If approaching a limit, summarize your state, anchor milestones, and start a fresh continuation.
10. **Surface Conflicts:** If patterns clash, pick one explicitly and justify it. Do not silently fork conventions or "average" conflicting styles.
11. **Conventions Over Taste:** Match established workspace idioms over personal preference. Do not refactor code that is not broken.
12. **State Anchoring:** Continuously report what is `[verified]`, `[current]`, and `[todo]`. Re-anchor your plan before every significant step.
13. **Fail Loud:** Never report completion if any step was skipped or unverified. Explicitly surface constraints and assumptions.

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

## Non-Negotiable Rules

Follow these 13 rules. They are non-negotiable and must be fully enforced. Bias toward caution over speed on non-trivial work.

1. **Invoke Caveman First:** Trigger the `caveman` skill using your platform's tool-calling mechanism (`activate_skill`, `Skill`, `skill`, `activate`, or `load_skill`) before any other action.
2. **Evidence Before Claim:** No claims (e.g., "tests pass") without raw command output. No evidence = not done. "Seems to work" = failure to verify.
3. **Task Isolation:** Use a fresh subagent or tool call for each independent task. Do not carry bloated history into isolated jobs.
4. **Goal-Driven Execution:** Success = empirical proof. Bug fixes require Red-Green-Refactor: verify the failure (Red) before applying the fix (Green).
5. **Surgical Minimalism:** Match style. Touch only what you must. No speculative abstractions, "just-in-case" code, or adjacent cleanup.
6. **Systematic Debugging:** Trace failures to their root cause. Do not patch symptoms with generic hacks, arbitrary timeouts, or unverified assumptions.
7. **Think & Ask:** Uncertainty = STOP & ask. Surface tradeoffs explicitly; never guess or choose a path silently.
8. **Read Before Write:** Map callers, exports, and shared utilities before modifying files. Understand why code exists before changing how it works.
9. **Token Guardrails:** Treat token budgets as hard limits. If approaching a limit, summarize your state, anchor milestones, and start a fresh continuation.
10. **Surface Conflicts:** If patterns clash, pick one explicitly and justify it. Do not silently fork conventions or "average" conflicting styles.
11. **Conventions Over Taste:** Match established workspace idioms over personal preference. Do not refactor code that is not broken.
12. **State Anchoring:** Continuously report what is `[verified]`, `[current]`, and `[todo]`. Re-anchor your plan before every significant step.
13. **Fail Loud:** Never report completion if any step was skipped or unverified. Explicitly surface constraints, risks, and assumptions.

## Project Matrix

| Project Name (Code) | Path | Tech Stack |
| ------------------- | ---- | ---------- |
| ...                 | ...  | ...        |

## Operating Protocol

- **Discovery:** Map project codes to roots via package/config files. Use efficient search tools.
- **Domain:** Read `CONTEXT.md` and `docs/adr/` before implementation. ADRs are binding.
- **Validation:** Run targeted tests and workspace-standard checks (`tsc`, `lint`, `build`) after every edit.
- **Completion:** Final report must include explicit validation performed and any remaining risks.
- **TDD Skill Defaults:** When the `tdd` skill is invoked, apply these standing defaults unless the user overrides them in the same turn:
  - Slices already have GitHub issues. Work through every slice; do not stop after one unless instructed.
  - Fully complete a slice before moving on. After each slice, produce a hand-off document and a kickoff prompt, then ask the user to start a new session for the next slice.
  - Parallelize with sub-agents or agents whenever steps are independent.
  - **Decision points (HITL vs AFK):** Only ask the user a question or present recommendations when the GitHub issue title is prefixed `HITL:` — and even then, present a short menu of recommended options that best fit the concern rather than open-ended questions. For all other issues (default/`AFK:` prefix), treat the work as fully autonomous: auto-select the recommended option at every decision point and proceed. Surface the choices made in the hand-off document at the end of the slice instead of mid-flight. **Recommended options must be sourced from ADRs (`docs/adr/`), the GitHub issue body/comments, or the slice definition itself — never self-invented.** If no grounded option exists, stop and surface the gap rather than fabricating one.
  - Keep the corresponding GitHub issue updated with the current status of internal cycles and slices as work progresses.
  - Follow every relevant `AGENTS.md` in the workspace.
  - If context approaches 200K tokens, prefer handing off to a new session; otherwise operate as an orchestrator dispatching sub-agents in parallel.
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

## Quality Bar

- **Outcome:** The generated `AGENTS.md` must be under 200 lines and contain the 13 Spartan Rules verbatim.
- **Process (Verifiable Trajectory):** The agent must demonstrate a "Search -> Verify -> Implement" sequence. No implementation tool calls (e.g., `replace`, `write_file`) are permitted until the project root and tech stack are verified via read-only tools.
- **Specification:** A task is considered "broken" if it lacks an explicit project path or code. If these are missing, the agent **must** stop and ask (Rule #7) instead of guessing a "default" path.
- **Style:** Instructions must be imperative and authoritative. No "should" or "please".

## Validation Protocol

1. **Evidence Check:** Verify every project path and tech stack entry with raw command output. Lying or guessing project details is a violation of Rule #2.
2. **Behavioral Trace (Negative Constraints):**
   - Did the agent **refrain** from implementing anything until Rule #1 (Invoke Caveman) was fulfilled?
   - Did the agent **refrain** from cleaning adjacent code (Rule #5) or patching symptoms (Rule #6)?
3. **Deterministic Review:** 
   - Rule #1: Tool name matches the detected agent?
   - Rule #12: State anchoring (`[verified]`, `[current]`, `[todo]`) present in every significant response?
4. **Outcome Validation:** If a bug is being fixed, did the agent perform the "Red" (verify failure) step before the "Green" (verify fix) step?

## Final Response

After writing files, respond with:

```markdown
Generated agent instructions.

Files:

- \`AGENTS.md\`
- \`CLAUDE.md\`
- \`GEMINI.md\`

Project codes:

- \`CODE\` - Project Name

Notes:

- [VS Code workspace detected / not detected.]
- [CONTEXT.md / \`docs/adr/\` (ADRs, \`*-release-notes.md\`) / \`docs/prompt/\` (\`*-prompt.md\`) artifacts referenced, or noted as to-be-produced inline by \`grill-with-docs\` / \`feature-prompt\` / \`release-notes\`.]
```

---
name: agents-md
description: "Generate or update AGENTS.md for a repository or VS Code workspace (canonical for Cursor CLI / IDE), create CLAUDE.md and Antigravity-compatible GEMINI.md shims, build a project matrix with stable project codes, and reference CONTEXT.md / ADRs as required domain context."
---

# AGENTS.md Generator

Create or update agent instruction files for a codebase:

- `AGENTS.md` as the canonical instruction file
- `CLAUDE.md` shim pointing to `AGENTS.md`
- Antigravity-compatible `GEMINI.md` shim pointing to `AGENTS.md`

Include the fourteen spartan non-negotiable principles in the `AGENTS.md` template below.
Also include retained operational defaults for caveman communication and parallel execution.
Also include an optional "Suggested next skills" footer convention so agents provide lightweight before/after reminders without enforcing hard gates, including after third-party skills.
Make clear that non-negotiables and operational defaults must be followed and fully enforced.

## Non-Negotiable Principles

Every generated `AGENTS.md` must include the following fourteen principles as non-negotiables:

1. **Invoke Caveman First:** Invoke the `caveman` skill before any other action. Use the runtime-native form: Claude Code `/caveman`, Cursor CLI / IDE `/caveman`, Antigravity CLI `activate_skill(name="caveman")`, Copilot CLI `skill("caveman")`, Codex CLI `activate("caveman")`, or Opencode CLI `load_skill("caveman")`. If the runtime cannot self-issue that invocation from instructions, read the local `caveman` `SKILL.md` and apply its chat-output rules before continuing.
2. **Evidence Before Claim:** No claims (e.g., "tests pass") without raw command output. No evidence = not done. "Seems to" or "likely" = failure to verify.
3. **Task Isolation:** For each independent task, use a fresh subagent, agent, worker, or isolated tool pass when the runtime supports it and the work can be split without shared-file conflicts. Do not carry bloated history into isolated jobs.
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
14. **No Project Code Abbreviation:** Use the full project code from the Project Matrix in all chat output, documentation, ADRs, prompts, issues, PRs, commit messages, and code comments. Never abbreviate or coin shorthand.

## Runtime References

When generating or validating `AGENTS.md`, use the matching runtime docs under `references/`:

| File | Use for |
| :--- | :--- |
| [`tool-calling.md`](references/tool-calling.md) | Tool-calling loop, Cursor CLI tool names, `Task`/subagents, permissions |
| [`cursor-tools.md`](references/cursor-tools.md) | Skill-kit → Cursor tool name mapping |
| [`claude-tools.md`](references/claude-tools.md) | Skill-kit → Claude Code mapping |
| [`codex-tools.md`](references/codex-tools.md) | Skill-kit → Codex CLI mapping |
| [`copilot-tools.md`](references/copilot-tools.md) | Skill-kit → Copilot CLI mapping |
| [`antigravity-tools.md`](references/antigravity-tools.md) | Skill-kit → Antigravity CLI mapping |
| [`opencode-tools.md`](references/opencode-tools.md) | Skill-kit → Opencode CLI mapping |
| [`caveman-invocation.md`](references/caveman-invocation.md) | Runtime-native `/caveman` (or equivalent) at session start |

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
8. Check whether `CONTEXT.md` or any artifacts under `docs/adr/`, `docs/prompts/`, and `docs/release-notes/` exist. Look first at the `<artifacts-root>` (see below); fall back to the repo root only when no workspace is present. Three artifact types live in sibling folders, distinguished by location and filename suffix:
   - `<artifacts-root>/docs/adr/NNNN-<slug>.md` — ADR (no suffix), written by `grill-with-docs`.
   - `<artifacts-root>/docs/prompts/NNNN-<slug>-prompt.md` — feature prompt, written by `feature-prompt`.
   - `<artifacts-root>/docs/release-notes/D-Month-YYYY.md` — on-demand release notes, written by `release-notes`.
     ADRs and prompts share one global `NNNN` numbering sequence across `docs/adr/` and `docs/prompts/`. Release notes do not use that sequence; they are date-based and live under `docs/release-notes/`. Reference these artifacts as required domain context when present. If none exists and terminology matters, note that domain language is sharpened inline by the `grill-with-docs` skill, which writes to `CONTEXT.md` and ADRs as decisions crystallise.

   `<artifacts-root>` resolves as: (1) the directory containing the `*.code-workspace` file if a VS Code workspace is detected — this is the same location as the meta-workspace folder (`path: "."`); (2) else the per-context root for multi-context repos with a root `CONTEXT-MAP.md`; (3) else the repo root for single-repo projects. Workspace mode is preferred: it keeps prompts, ADRs, and release notes centralized instead of scattering them across project repos.

Use structured parsing when available. For `.code-workspace`, prefer JSON parsing that tolerates comments if the local toolchain supports it. If not, read carefully and avoid corrupting paths.

## Project Matrix

Every `AGENTS.md` must include a project matrix with this exact heading and columns:

```markdown
## Project Matrix

| Project Name (Code)                   | Path           | Tech Stack              |
| ------------------------------------- | -------------- | ----------------------- |
| Example Workspace (EXAMPLE-WORKSPACE) | .              | Meta workspace, no code |
| API Service (API-SERVICE)             | ../api-service | PHP, Laravel            |
```

Project code rules:

- Codes are stable identifiers used by feature prompts, discovery, PRDs, issues, and release notes.
- Use uppercase letters, digits, and hyphens only.
- Use the full project code from the Project Matrix everywhere the project is referenced. Never abbreviate project codes or invent shorthand.
- For VS Code workspaces, derive the code from the workspace folder `name`, not from `path`.
- Preserve the workspace folder `name` as the project name, but remove leading emoji/icons and trim whitespace for the display text in `Project Name (Code)`.
- Normalize the code from the cleaned workspace folder name by uppercasing and replacing non-alphanumeric runs with hyphens.
- Example: `🔌 API Service` becomes `API Service (API-SERVICE)`.
- Example: `🧩 Example Workspace` with path `.` becomes `Example Workspace (EXAMPLE-WORKSPACE)` and is marked as meta workspace.
- If two projects collide, add a qualifier: `ADMIN-WEB`, `ADMIN-API`.
- Do not rename existing project codes in an existing `AGENTS.md` unless the user asks.
- Mark the VS Code workspace folder with `path: "."` as `Meta workspace, no code`.

## GitHub Issue Title Conventions

Generated `AGENTS.md` files must include issue-title rules that make PRD and slice issues easy to locate from GitHub search and from the ADR filename:

- **PRD issues:** title exactly starts with `PRD: <PROJECT-CODE> ADR-<adr-number> <adr-name>`.
  - Derive `<adr-number>` and `<adr-name>` from the ADR filename under `docs/adr/` (without `.md`), where `0042-stock-transfer-approvals.md` maps to `ADR-0042 stock-transfer-approvals`.
  - Example: `PRD: PAYMENTS ADR-0042 stock-transfer-approvals`.
- **PRD slice issues:** title exactly starts with `Slice NNNN of <PROJECT-CODE> ADR-<adr-number> <adr-name> (#<prd-issue-number>): <Short heading>`.
  - `NNNN` is a zero-padded four-digit slice number local to that PRD, starting at `0001`.
  - `<prd-issue-number>` is the numeric GitHub issue number of the parent PRD issue.
  - Keep `<Short heading>` concise, action-oriented, and specific enough to scan in an issue list.
  - Example: `Slice 0001 of PAYMENTS ADR-0042 stock-transfer-approvals (#4812): Add approval state model`.
- **Labels:** Follow Matt Pocock's triage roles. Every triaged issue should have exactly one category label (`bug` or `enhancement`) and exactly one state label (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, or `wontfix`).
- **Routing state:** Do not encode `HITL:` or `AFK:` in GitHub issue titles, commit subjects, PR titles, or branch names. Use state labels instead: `ready-for-human` for human-ready work and `ready-for-agent` for agent-ready work.
- **Non-PRD implementation issues:** prefer `<PROJECT-CODE>: <short imperative heading>` when the issue is not tied to a PRD. Keep the full Project Matrix code; never abbreviate it.

## AGENTS.md Structure

Generate `AGENTS.md` with this structure:

```markdown
# Agent Instructions

## Non-Negotiable Rules

Follow these 14 rules. They are non-negotiable and must be fully enforced. Bias toward caution over speed on non-trivial work.

1. **Invoke Caveman First:** Invoke the `caveman` skill before any other action. Use the runtime-native form: Claude Code `/caveman`, Cursor CLI / IDE `/caveman`, Antigravity CLI `activate_skill(name="caveman")`, Copilot CLI `skill("caveman")`, Codex CLI `activate("caveman")`, or Opencode CLI `load_skill("caveman")`. If the runtime cannot self-issue that invocation from instructions, read the local `caveman` `SKILL.md` and apply its chat-output rules before continuing.
2. **Evidence Before Claim:** No claims (e.g., "tests pass") without raw command output. No evidence = not done. "Seems to work" = failure to verify.
3. **Task Isolation:** For each independent task, use a fresh subagent, agent, worker, or isolated tool pass when the runtime supports it and the work can be split without shared-file conflicts. Do not carry bloated history into isolated jobs.
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
14. **No Project Code Abbreviation:** Use the full project code from the Project Matrix in all chat output, documentation, ADRs, prompts, issues, PRs, commit messages, and code comments. Never abbreviate or coin shorthand.

## Project Matrix

| Project Name (Code) | Path | Tech Stack |
| ------------------- | ---- | ---------- |
| ...                 | ...  | ...        |

## GitHub Issue Titles

- PRD issues: `PRD: <PROJECT-CODE> ADR-<adr-number> <adr-name>`.
- PRD slice issues: `Slice NNNN of <PROJECT-CODE> ADR-<adr-number> <adr-name> (#<prd-issue-number>): <Short heading>`. Use four digits, local to the PRD, starting at `0001`.
- Every triaged issue needs exactly one category label (`bug` or `enhancement`) and exactly one state label (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, or `wontfix`).
- Do not put `HITL:` or `AFK:` in issue titles, commit subjects, PR titles, or branch names. Use `ready-for-human` or `ready-for-agent` state labels for routing.
- Non-PRD implementation issues: prefer `<PROJECT-CODE>: <short imperative heading>` and keep the full Project Matrix code.

## Operating Protocol

- **Discovery:** Map project codes to roots via package/config files. Use efficient search tools.
- **Agent Entry Files:** `AGENTS.md` is canonical for Cursor CLI / IDE and should remain the primary workspace instruction file. `CLAUDE.md` and `GEMINI.md` are compatibility shims.
- **MCP Config:** In multi-repo workspaces, keep MCP config for supported coding tools at workspace root (`.cursor/mcp.json`, `.mcp.json`, `.agents/mcp_config.json`, `.codex/config.toml`, `.claude/settings.local.json`). Keep `~/.cursor/mcp.json` only as global fallback for Cursor. Keep memtrace MCP pinned to workspace root and do not maintain repo-level memtrace MCP configs.
- **Understand-Anything Knowledge Base:** Keep Understand-Anything knowledge graphs at each project-repo root (`<project-root>/.understand-anything/knowledge-graph.json`). Do not place project code knowledge graphs at workspace root.
- **Caveman Chat:** Caveman applies to chat output only. Do not caveman-compress code, docs, PRDs, release notes, PR bodies, generated prompts, or persisted artifacts. Use 5th-grade English in chat unless a technical term is required. Prefer `guess` over `speculate`, `join words` over `conjunctions`, `short sentence` over `fragment`, `because` or `so` over `causality`, `simple` over `shallow`, and `combine` over `synthesize`. Keep exact technical words such as `API`, `DB`, `auth`, `null`, `array`, `timeout`, and `race condition`.
- **Subagent Dispatch:** Before substantial work, split the task into independent lanes. Dispatch fresh subagents, agents, workers, or isolated tool passes for lanes that can run in parallel without blocking the next local step. Use lanes for research, critique, comparison, risk checks, source checks, outline, terminology, audience fit, codebase search, multi-project mapping, test-failure investigation, and review. Main agent owns final judgment and conflict resolution. Keep work local when the task is tiny, sequential, tightly coupled, or likely to create edit conflicts. If the runtime lacks subagents, run separate focused tool passes.
- **Suggested Next Skills Footer:** End non-trivial responses with an optional `Suggested next skills (optional)` block containing 1-3 advisory recommendations. Keep it recommendation-only (no enforced gating). This applies after any substantial step, including local skills and third-party skills. Prefer workflow-adjacent next steps and uncertainty-reducing helpers (for example `/understand-diff` before larger refactors).
- **Domain:** Read `CONTEXT.md` and `docs/adr/` before implementation. ADRs are binding.
- **Validation:** Run targeted tests and workspace-standard checks (`tsc`, `lint`, `build`) after every edit.
- **Completion:** Final report must include explicit validation performed and any remaining risks.
- **Planned vs Ad Hoc Issues:** Planned work starts from a GitHub issue that has passed Matt Pocock's `/triage`: exactly one category label (`bug` or `enhancement`) and a ready state label (`ready-for-agent` or `ready-for-human`). Small ad hoc work may start from a one-line request without a GitHub issue; in that case, do the work first and let `commit-push-pr` or `commit-push-close` create the issue at ship time from the original request, final diff, decisions, and validation. If ad hoc work becomes large, ambiguous, cross-project, or multi-slice, stop and route it through `/triage`, `/feature-prompt`, or `/to-issues`.
- **TDD Skill Defaults:** When the `tdd` skill is invoked, apply these standing defaults unless the user overrides them in the same turn:
  - Slices already have GitHub issues. PRD slices use titles like `Slice NNNN of <PROJECT-CODE> ADR-<adr-number> <adr-name> (#<prd-issue-number>): <Short heading>`. Work through every slice for the PRD; do not stop after one unless instructed.
  - Fully complete a slice before moving on. After each slice, produce a hand-off document and a kickoff prompt, then ask the user to start a new session for the next slice.
  - Parallelize with sub-agents or agents whenever steps are independent.
  - **Decision points (HITL vs AFK):** Only ask the user a question or present recommendations when the GitHub issue has the `ready-for-human` label — and even then, present a short menu of recommended options that best fit the concern rather than open-ended questions. For `ready-for-agent` issues, treat the work as fully autonomous: auto-select the recommended option at every decision point and proceed. Surface the choices made in the hand-off document at the end of the slice instead of mid-flight. **Recommended options must be sourced from ADRs (`docs/adr/`), the GitHub issue body/comments, or the slice definition itself — never self-invented.** If no grounded option exists, stop and surface the gap rather than fabricating one.
  - Keep the corresponding GitHub issue updated with the current status of internal cycles and slices as work progresses.
  - Follow every relevant `AGENTS.md` in the workspace.
  - If context approaches 200K tokens, prefer handing off to a new session; otherwise operate as an orchestrator dispatching sub-agents in parallel.
```

Preserve any useful existing local instructions when updating `AGENTS.md`, but reorganize duplicated content into this structure.

## Shim Files

Create or update `CLAUDE.md` and `GEMINI.md` as shims for non-Cursor runtimes. Cursor CLI and the Cursor IDE read `AGENTS.md` as the canonical workspace instruction file — no Cursor-specific shim is required. Antigravity CLI reads both `AGENTS.md` and `GEMINI.md` from the active workspace, so keep `GEMINI.md` for Antigravity compatibility.

Use this content for `CLAUDE.md` unless the workspace or repository already has important Claude-specific instructions:

```markdown
# Agent Instructions

Read `AGENTS.md` first. It is the canonical instruction file for this workspace.

Before any other action in Claude Code, invoke `/caveman`. If `/caveman` is unavailable or cannot be self-issued from instructions, load or read the local `caveman` skill and apply its chat-output rules before continuing.

This file is a Claude Code shim for tool compatibility.
```

Use this content for `GEMINI.md` unless the workspace or repository already has important Antigravity-specific instructions:

```markdown
# Agent Instructions

Read `AGENTS.md` first. It is the canonical instruction file for this workspace.

This file is an Antigravity CLI compatibility shim. Antigravity CLI reads `GEMINI.md` as a supported workspace context file.
```

If an existing shim contains valuable tool-specific rules, keep them under:

```markdown
## Tool-Specific Notes
```

Do not duplicate the full `AGENTS.md` content into shims.

## Quality Bar

- **Outcome:** The generated `AGENTS.md` must be under 200 lines and contain the 14 Spartan Rules verbatim.
- **Process (Verifiable Trajectory):** The agent must demonstrate a "Search -> Verify -> Implement" sequence. No implementation tool calls (e.g., `StrReplace`, `Write`, `replace`, `write_file`) are permitted until the project root and tech stack are verified via read-only tools. Use [`references/tool-calling.md`](references/tool-calling.md) and the matching `*-tools.md` file for the detected runtime.
- **Specification:** A task is considered "broken" if it lacks an explicit project path or code. If these are missing, the agent **must** stop and ask (Rule #7) instead of guessing a "default" path.
- **Style:** Instructions must be imperative and authoritative. No "should" or "please".

## Validation Protocol

1. **Evidence Check:** Verify every project path and tech stack entry with raw command output. Lying or guessing project details is a violation of Rule #2.
2. **Behavioral Trace (Negative Constraints):**
   - Did the agent **refrain** from implementing anything until Rule #1 (Invoke Caveman) was fulfilled?
   - Did the agent **refrain** from cleaning adjacent code (Rule #5) or patching symptoms (Rule #6)?
3. **Deterministic Review:**
   - Rule #1: Caveman invocation and tool names match the detected runtime per [`references/tool-calling.md`](references/tool-calling.md) and the matching `*-tools.md` file?
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
- [`AGENTS.md` is canonical for Cursor CLI / IDE; no extra shim required.]
- [`GEMINI.md` retained for Antigravity CLI compatibility.]
- [CONTEXT.md / \`docs/adr/\` (ADRs) / \`docs/prompts/\` (\`*-prompt.md\`) / \`docs/release-notes/\` (\`D-Month-YYYY.md\`) artifacts referenced, or noted as to-be-produced inline by \`grill-with-docs\` / \`feature-prompt\` / \`release-notes\`.]
```

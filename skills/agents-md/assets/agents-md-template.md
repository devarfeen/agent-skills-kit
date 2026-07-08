<!-- agents-md marker · v7 · re-run /agents-md to regenerate -->
# Agent Instructions

[one concise workspace intro inferred from the .code-workspace name and folder scan]

[PROJECT MATRIX — the `| Project | Path | Stack |` table per the Project Matrix Format rules in SKILL.md, one row per `.code-workspace` folder]

## Non-Negotiable Rules

### 1. Target a Project

- Every task must target a project from the Project Matrix. If the prompt names none, stop and ask which one first.
- "Meta workspace" means apply the task to every project in the matrix.
- Use the PROJECT-CODE exactly as written — chat, docs, ADRs, prompts, issues, PRs, commits, comments, filenames. Never alter, abbreviate, or re-case it.
- In chat, identify projects by PROJECT-CODE, not folder/repo names, domains, or hostnames. Mention paths only when the path itself matters.

### 2. Launch From The Workspace Root

Run every agent from the workspace root — the folder holding the `.code-workspace` file and this `AGENTS.md`. Never launch from inside a Project Matrix project.

On start, check the working directory:

- Workspace root → continue.
- Inside a Project Matrix project (or any child of one) → stop. Warn clearly: "You launched inside <PROJECT-CODE>, not the workspace root — the Project Matrix and workspace rules may not load correctly." Then ask the user to continue anyway or exit and relaunch from the workspace root. Do nothing else until they choose.

### 3. Think Before Coding

State assumptions. Present real interpretations. Push back on weak plans. Stop and ask when unclear.

### 4. Decision Options

Do not make the user infer your recommendation.

- **Label options** — mark each `Recommended`, `Currently implemented`, both, or neither, in the option title, not buried in the explanation.
- **Offer up to three** concrete options when useful, plus a final `Write your own`. Do not pad to three when fewer real paths exist.
- **Recommend one** — label exactly one option `Recommended`. If none is safe to recommend, say why before the list.

### 5. Simplicity First

Solve only the asked problem. No speculative features, no one-use abstractions. Remove complexity when a smaller fix works.

### 6. Surgical Changes

Touch only required lines. Match local style. Do not refactor unrelated code. Clean only dead code your change creates.

### 7. Goal-Driven Execution

Define success before edits. Turn bugs into reproductions, changes into checks. Verify before reporting done.

### 8. Systematic Debugging

Find the root cause; don't patch symptoms.

- Reproduce the failure before changing anything.
- Trace to the underlying cause, not the surface symptom.
- No hacks, arbitrary waits/sleeps, or guess-and-check fixes.
- After fixing, confirm the original reproduction now passes.

**Why:** Symptom patches hide the real fault and resurface later as flakier, harder bugs.

### 9. Read Before Write

Before editing, understand why the code exists — its callers and exports, the shared utilities it relies on, and its original intent.

### 10. Local Orchestration

The main session is sole orchestrator, merger, conflict resolver, and final judge.

Parallel and background work is opt-in. Default to serial. Suggest a parallel or background plan and wait for approval; never spawn subagents or background lanes on your own.

When the user approves parallelism:

- Run prerequisites first, then parallelize newly unblocked lanes. Serialize shared-file edits and integration.
- Run long or noisy lanes locally — background or async. Await and integrate every lane.
- Never use cloud or remote agents: Cursor Cloud, Copilot cloud agent, Codex Cloud/web, Antigravity managed/remote, Claude Routines (`/schedule`), claude.ai background agents. Claude Code agent teams are local but also banned — the main session stays the only orchestrator.
- Use local role lanes — Explorer, Researcher, Planner, Implementer, Reviewer, Tester, Tool-runner — with tools matched to role (read-only for discovery/review/planning, write for implementation, shell for tests). Subagents return summaries, not transcripts. Final synthesis stays in main.

**Checkouts:** Work only in the existing workspace checkouts. Do not clone repos or create new paths. Never use git worktrees unless the user explicitly asks for them.

### 11. Honest State & Reporting

Enforced. No exceptions.

- Before any significant step, anchor state: `[verified]` (proven true), `[current]` (in progress), `[todo]` (not started).
- At phase changes, send a short visible update: `Stage`, `Found`, `Next`, `Needs user`. Don't bury it in narration, raw tool output, or pre-tool chatter.
- Continue within a phase when the next action follows from the request; make phase transitions explicit before entering a new phase.
- Stop only when user input, approval, or a scope decision is needed.
- After discovery, investigation, or broad file reads, give the phase update before planning, edits, tests, commits, PRs, or issue updates.
- Never report work done while any part is skipped, stubbed, or unverified. Surface constraints, risks, and assumptions up front.
- After a successful task, end with `Recommended next step:` and the single best follow-up, plus a one-line why.
- When more paths matter, add `Other good options:` with up to three labeled choices (Rule 4), plus `Write your own`. Suggest only — never chain or auto-advance.

**Why:** Silent gaps and premature "done" are how broken work ships. Visible phase updates keep the user oriented without blocking routine progress.

### 12. Zero Attribution

No co-author, AI, tool, or generator attribution.

- Never add `Co-authored-by`, `Co-Authored-By`, `Generated by`, `AI-assisted`, `Made with`, or similar to commits, PR titles, PR bodies, issue comments, release notes, generated docs, or code comments.
- If a tool adds attribution automatically, remove it before publishing, committing, pushing, opening a PR, or closing/commenting on an issue.

## Working With Skills

Skills are ad-hoc tools, not a pipeline. Treat every installed skill as available.

Work follows this gradient. Pick the skill that fits the step in front of you; there is no required order and no state machine.

[GRADIENT TABLE — columns `Phase | Skills`. One row per gradient phase in manifest order (discover, sharpen, plan, slice, implement, verify, ship). In each row list every `kit` and `external` skill whose manifest `phase` matches. Omit phases with no skills.]

[STARTUP NOTE — one line per skill with manifest `phase: startup`, e.g. "Run `/design-system` per project after setup to build the UI library first."]

- Skills live in each repo's `.agents/skills/` and in the kit. Prefer the project-local skill when both exist.
- When a target project has its own `AGENTS.md`, read it on demand for that project's specifics. This root file still binds.
- After finishing a step, suggest a sensible next skill when one fits. Suggest only — never chain or auto-advance.
- Do not assume a skill exists; use what is installed.

### Companion Skills And MCPs

These are optional separate installs. Use them beside this kit when installed and task-fit. Do not vendor them into this kit.

[COMPANION TABLE — columns `Companion | Use when`. One row per manifest entry with `kind: companion`: its name and use-when text, in manifest order.]

- Treat companion tools as helpers, not authority. Repo code, tests, ADRs, `CONTEXT.md`, and user instructions still win.
- Never assume a companion is installed. If missing, say so and continue with the best local fallback.
- Use MCPs only for the current task. Do not browse unrelated external data.
- For database MCPs, use the narrowest approved connection and read-only access unless the user approves a specific write.

### Matt Skill Routing

Use `/ask-matt` when the user asks which Matt skill or flow fits. It routes over user-invoked Matt skills; it does not execute. Do not auto-run what it suggests.

- Idea flow: `/grill-with-docs` → if runnable uncertainty, `/handoff` + `/prototype` + `/handoff` → for multi-session work, `/to-spec` then `/to-tickets`.
- An effort too big for one session (greenfield build, huge feature) → `/wayfinder` maps it as tickets on the tracker before any building.
- Start a fresh session per ticket. Matt's flow works the ticket frontier with `/implement`; this kit prefers `/tdd` when available.
- `/triage` is for raw incoming issues and external PRs only — not tickets already created by `/to-tickets`.
- `/research` delegates primary-source reading to a background agent; it leaves a cited doc to grill or plan against.
- `/improve-codebase-architecture` for codebase health; a chosen improvement becomes an idea for `/grill-with-docs`.
- `/handoff` forks context into a new session. `/compact` continues the same conversation; use it only at intentional phase breaks.

[RUNTIME TOOL-CALLING — emit the `### Runtime Tool-Calling` subsection here, per the Skills Manifest rules in SKILL.md]

## Context & Native Memory

### Retrieval order

1. **Binding** — `CONTEXT.md` (<!-- set during setup: path to CONTEXT.md -->) and ADRs (<!-- set during setup: path to specs/adr -->). Read before implementing. These bind.
2. **Current task context** — the user request, active issue or spec, named local docs, current code, tests, and command evidence.
3. **Native CLI memory** — use only the current CLI's native memory feature when it is enabled.

### Artifact policy

- Do not create repo `MEMORY.md`, workspace wiki, discovery, or knowledge-graph files as default memory. Do not add memory MCP servers or third-party graph/index systems as default memory.
- Optional graph/index companions may be used only when installed and task-fit; their artifacts are not binding memory.
- Keep shared project context in `AGENTS.md`, `CONTEXT.md`, and ADRs.
- Use native CLI memory only when the current CLI provides it; do not sync memory between CLIs.

### Do not bulk-read

- `specs/` is an on-demand archive, not reading material. Never load it wholesale.
- Retrieve only what the current task names — by search or a discovery skill. Reading the whole archive rots context and wastes tokens.

### Archived context

When the user triggers `/grill-with-docs`, ask up front — before the Q/A starts — whether they have archived context for the feature: prior discussions, original intent, or decision history. Await their reply.

- The user pastes it, or says to continue without. Ask once; do not block repeatedly.
- Capture any pasted context verbatim in the ADR, with provenance. Maximum fidelity — do not summarize it away:

  > Source: "<doc title>" · pasted <date>
  >
  > <verbatim excerpt — unedited>

- If a paste reveals an old or current feature name, offer to add it to `CONTEXT.md` aliases.
- Pasted history is advisory. If it contradicts a current ADR, flag the contradiction — never silently drop it.

## GitHub Issue Titles

Issue titles are findable from GitHub search and from the ADR filename. `<PROJECT-CODE>` is the PROJECT-CODE from the Project Matrix — uppercase, hyphenated, no spaces; use it exactly.

**Spec issue** — title starts exactly with:

`Spec: <PROJECT-CODE> ADR-<adr-number> <adr-name>`

- Derive `<adr-number>` and `<adr-name>` from the ADR filename in `specs/adr/` (without `.md`): `0042-stock-transfer-approvals.md` → `ADR-0042 stock-transfer-approvals`.
- Example: `Spec: PAYMENTS ADR-0042 stock-transfer-approvals`
- Issues titled `PRD: …` predate this naming; treat them as spec issues and do not retitle them.

**Spec slice issue** — title starts exactly with:

`Slice NNNN of <PROJECT-CODE> ADR-<adr-number> <adr-name> (#<spec-issue>): <Short heading>`

- `NNNN`: zero-padded four-digit slice number, local to that spec, starting at `0001`.
- `<spec-issue>`: GitHub issue number of the parent spec.
- `<Short heading>`: concise, action-oriented, scannable in an issue list.
- Example: `Slice 0001 of PAYMENTS ADR-0042 stock-transfer-approvals (#4812): Add approval state model`

**Non-spec issue** — not tied to a spec:

`<PROJECT-CODE>: <short imperative heading>`

**Labels:** every triaged issue carries exactly one category (`bug` or `enhancement`) and exactly one state (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`).

## Output Style

Chat only. Does not apply to code, docs, specs (PRDs), release notes, PR bodies, or prompts.

### 1. Plain-Language Chat

- Be concise and lead with the conclusion. Clarity beats compression — use a short complete sentence where clipping would confuse.
- Use everyday words over heavy ones ("fix" over "implement a solution", "use" over "utilize"); no jargon unless it is an exact code, product, or domain name the user already uses.
- Write for readers who may not read English fluently: short sentences, one idea each; split any sentence carrying more than three identifiers.
- Keep exact code, DB, API, route, screen, and file names verbatim. Explain the practical effect first, the identifiers after, and each technical term once.
- For bugs, tests, options, and post-mortems: name the plain failure or the real decision first ("the test data made both cases identical"), then the project terms.
- No unexplained shorthand and no arrow-only flows without plain words after them.
- Optional brevity skills are user-invoked only.

### 2. Understanding Checks

When the user asks you to repeat, confirm, or restate their understanding:

- Restate only what you understand.
- Ask the user to approve or correct it.
- Stop there. Do not plan, edit, run tools, or continue until the user confirms or corrects the understanding.

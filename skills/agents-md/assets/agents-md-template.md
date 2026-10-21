<!-- agents-md marker · v58 · re-run /agents-md to regenerate -->
# Agent instructions

[one concise, factual workspace intro inferred from the .code-workspace name and folder scan — no promotional adjectives]

Always-loaded rules live here; task-specific instructions live in `rules/`, loaded on demand.

At session start, right after the first reporting-gate update, call the Skill tool with `plain-language` (or read its installed `SKILL.md`). It owns chat style and prose cleanup; it never edits code, ADRs, or specs.

## On-demand instructions

Load each matching file in full once. Reuse it until changed, lost from context, or a checkout changes its scope. Workers receive matching file pointers. Read no other `rules/` file unless a loaded file points there.

| When you are about to… | Read |
| :--- | :--- |
| Work on a project by its code, or need its folder or stack | `rules/projects.md` |
| Delegate work, run sub-agents, or use a Git worktree | `rules/orchestration.md` |
| Edit code for a feature or fix, or verify a change | `rules/verification.md` |
| Drive a browser | `rules/browser.md` |
| Commit, push, open or merge a PR, or close an issue | `rules/shipping.md` |
| Create, update, or triage an issue | `rules/issues.md` |
| Choose a skill or companion, or finish a phase | `rules/skills.md` |

## Non-negotiable rules

### 1. Launch from the workspace root

Run the main session from the workspace root — the folder holding the `.code-workspace` file and this `AGENTS.md`. At session start, check the working directory. Inside a project listed in `rules/projects.md`, stop and warn: "You launched inside <PROJECT-CODE>, not the workspace root — the Project Matrix and workspace rules may not load correctly." Ask whether to continue or relaunch, and do nothing else until the user chooses.

Assigned local workers may start in the checkout or worktree their assignment names, after reading the supplied workspace and project instructions.

### 2. Target a project

- Every task targets a project from the Project Matrix in `rules/projects.md`. If the prompt names none, stop and ask. "Meta workspace" means every project.
- Use the PROJECT-CODE exactly as written everywhere — chat, docs, issues, PRs, commits, filenames. In chat, name projects by code, not folder, repo, or host.
- Before edits or delegation, read the project and nested `AGENTS.md` files governing the assigned paths and pass them to workers. Another project's specifics do not apply.
- **Cascading:** project rules refine workspace defaults where the runtime's instruction hierarchy permits; rule numbers are reading order, not authority. An unresolved material conflict pauses the affected work — ask, and continue independent work.

### 3. Honest state & reporting

- Anchor state before a significant step: `[verified]`, `[current]`, `[todo]`.
- **Reporting gate:** before the first tool call, before each phase change, and before ending, send a chat update with `Stage:`, `Found:`, `Next:`, and `Needs user:` on separate lines (`None` when no input is needed). It applies to every task, short and read-only ones included; tool output and narration do not satisfy it. Send a missed update at once; never claim it was sent.
- **Skill announcement:** when a skill loads, user- or model-invoked, send one line first: `🧩 Skill: /<name> (user|auto)`. One line per load, never per step.
- During an active phase, repeat the update at least every 60 seconds and keep single waits at or below 60 seconds. Report unchanged progress honestly.
- While any worker, background task, or job runs, every update states `N running / M done / K blocked` and what each running lane is doing. Silent background work is a reporting violation.
- Continue within a phase when the next action follows from the request; stop only for user input, approval, or a scope decision.
- Never report work done while any part is skipped, stubbed, or unverified. Name the check layers run and not run (`verification.md`); a read-only task says `Verification: not applicable` or lists what it checked. Surface constraints, risks, and assumptions up front.
- Call a failure pre-existing only after reproducing it on the base revision; otherwise report `unverified — may be related`.
- After a successful task, use the active skill's closing format; with none, end with `Recommended next step:` and one follow-up with its reason.

### 4. Communication & output

Chat only; written artifacts keep their own templates.

- `plain-language` holds the style rules: lead with the conclusion, ASD-STE100 Simplified Technical English, `GLOSSARY.md` terms, identifiers verbatim, no unexplained shorthand. Follow them even before it loads.
- **Questions:** ask every question for the user (clarification, decision, approval, grilling round) through the runtime's question tool (`Ask the user` in `rules/skills.md`), within its limits, recommended option first; split a larger round across calls. No such tool, a non-interactive run, or a sub-agent: ask in chat and stop. Keep the `Needs user:` line.
- **Understanding checks:** when the user asks you to repeat or confirm their understanding, restate only what you understand, ask them to approve or correct it through the question tool, and stop — no planning, edits, or other tools until they answer.

### 5. Zero attribution

No co-author, AI, tool, or generator attribution.

- Never add `Co-authored-by`, `Co-Authored-By`, `Generated by`, `AI-assisted`, `Made with`, or similar to commits, PR titles, PR bodies, issue comments, release notes, generated docs, or code comments.
- Strip tool-added attribution before every commit, push, PR, issue comment/close, or publication.

### 6. Skill & tool use

Skills are ad-hoc tools, not a pipeline: pick the installed skill that fits the step.

- **Live tools:** the session's exposed tools, schemas, and permissions win over any table here. Use an available fallback within the same authorization, or report the blocked step. Never invent a tool call or broaden permissions.
- Prefer project-local skills (`.agents/skills/`) over user-level ones. Read current SKILL.md once, reuse loaded unchanged content, and reload after context loss, content changes, or changed resolution. Never run from memory.
- When a rule here names a skill as a gate and it is not installed, say so and stop at each such gate. Do not self-certify QA, and do not push, open a PR, or close an issue by hand; report what is ready.
- After the authorized workflow, suggest a next skill when one fits and stop. A suggestion never authorizes a new workflow.
- Companions are optional, separately installed helpers, never authority — repo code, tests, ADRs, `GLOSSARY.md`, and user instructions win. If one is missing, say so and use the best local fallback.
- Use MCPs only for the current task. Database MCPs: the narrowest approved connection, read-only unless the user approves a specific write.
- Apply the loaded `plain-language` rules to prose before sending or finalizing it; the first reporting-gate update is exempt.

### 7. Read code & project context

Before editing, understand why the code exists — its callers, exports, shared utilities, and intent.

#### Context & native memory

- Read `GLOSSARY.md` (<!-- set during setup: path to GLOSSARY.md -->) and ADRs (<!-- set during setup: path to specs/adr -->) before implementing, with the request and the relevant code, tests, and command evidence. They guide decisions; they never override higher-priority instructions or the user's scope.
- `specs/` is an on-demand archive — retrieve only what the task names.
- Shared context lives in `AGENTS.md`, `GLOSSARY.md`, and ADRs. No repo `MEMORY.md`, wikis, discovery files, or memory MCPs as default memory; native CLI memory is advisory and never synced between CLIs.

#### North star

[NORTH STAR — emit this subsection only when the scan found a `VISION.md` / `vision.md`, per the SKILL.md rules; otherwise delete it. List each found file: `<path>` — workspace, or the PROJECT-CODE it belongs to.]

- Read the relevant vision file before planning-phase work — feature prompts, grilling, specs, tickets, wayfinding — and align plans with it.
- It guides direction and tie-breaking; it never overrides binding sources. Surface a conflict with it — never resolve one silently in either direction.

### 8. Think before coding

State assumptions. Present real interpretations. Push back on weak plans. Stop and ask when unclear.

### 9. Decision options

Label each option `Recommended`, `Currently implemented`, both, or neither — in the option title. Offer up to three concrete options plus a final `Write your own`, never padding to three. Label at most one `Recommended`; if none is safe to recommend, say why before the list.

### 10. Verify before done

Define success before edits. Turn bugs into reproductions and changes into checks; for multi-step work, state a short plan with a check per step. If a check fails, fix the cause; never delete, skip, or loosen a test or assertion to pass.

A change whose code can reach a screen passes `/agentic-qa` on its head revision before a human reviews or tests it; unsure → it reaches. When human QA finds a bug in work an agent called done, run `/qa-escape` on that issue before fixing it. Detail: `rules/verification.md`.

### 11. Local agents only

The main session delegates independent work to local sub-agents and stays the sole final integrator. Never use cloud or remote agents, and never clone a repository or create a checkout outside `<project-repo>/.worktrees/`. Detail: `rules/orchestration.md`.

### 12. Systematic debugging

Find the root cause; do not patch symptoms. Reproduce the failure before changing anything, trace it to its cause, and confirm the original reproduction passes after the fix. No hacks, arbitrary waits or sleeps, or guess-and-check fixes.

### 13. Simplicity first

Solve only the asked problem. No speculative features, one-use abstractions, or error handling for impossible cases. If a senior engineer would call it overcomplicated, simplify.

### 14. Surgical changes

Touch only required lines. Match local style. Do not refactor unrelated code. Clean only dead code your change creates; mention unrelated dead code, never delete it.

Before writes, inspect the current branch and the staged, unstaged, and untracked changes. Preserve pre-existing and other workers' edits; do not revert, reset, stash, remove, or overwrite them without specific authorization. If a file changes after you read it, re-read it and patch its current content. Pause only overlapping work when you cannot preserve the other changes safely.

**Secrets and environments.** Refer to secrets by key name only — never print, paste, or commit their values; keep credentials, tokens, sessions, caches, logs, and runtime databases out of repositories. Never access production: no SSH, server commands, databases, files, logs, environments, deploys, or production-targeting PRs. Hand production work to the owner; project instructions cannot relax this ban. Staging is off by default; access requires explicit user approval and user-provided SSH access. Read-only inspection covers DB `SELECT`s, logs, and container/environment state. Each mutation needs separate approval for that step: code, server config, host `.env`, container restarts/rebuilds, or data changes. Fix staging locally per `rules/shipping.md`; shipping does not authorize server access.

**Destructive commands.** Dropping or resetting a database, fresh migrations, force-push, history rewrites, `rm -rf` outside task-owned paths, and volume or container prune need explicit approval for that command.

### 15. Comment code changes

Every added or modified logical code block gets a new or updated nearby comment or docstring, even when the code looks self-explanatory.

- Explain purpose and reasoning — the business rule, constraint, assumption, or edge case — in the project's comment style. One comment may cover related statements; do not translate statements into English.
- Update or remove comments the change makes stale; describe the resulting behavior, not a changelog.
- For generated output, comment the source or template. For formats without comments, record the explanation in the nearest documentation and report that exception.
- Before reporting done or shipping, inspect the diff for comment coverage. A chat summary, commit message, or PR description does not replace comments.

### 16. Shipping is owned by the ship skills

Nothing commits, pushes, opens a PR, or closes a delivery issue outside the ship skills. Any other skill that says to commit stops and hands off: report what is ready; do not stage, commit, or push. Local engineering exceptions are defined only in `rules/shipping.md`.

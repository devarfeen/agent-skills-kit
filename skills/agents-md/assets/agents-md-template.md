<!-- agents-md marker · v27 · re-run /agents-md to regenerate -->
# Agent instructions

[one concise, factual workspace intro inferred from the .code-workspace name and folder scan — no promotional adjectives]

[PROJECT MATRIX — the `| Project | Path | Stack |` table per the Project Matrix Format rules in SKILL.md, one row per `.code-workspace` folder]

## Non-negotiable rules

### 1. Launch from the workspace root

Run the main session from the workspace root — the folder holding the `.code-workspace` file and this `AGENTS.md` — never from inside a Project Matrix project.

At main-session start, check the working directory. At the workspace root, continue. Inside a Project Matrix project (or any child of one), stop and warn clearly: "You launched inside <PROJECT-CODE>, not the workspace root — the Project Matrix and workspace rules may not load correctly." Then ask the user to continue anyway or exit and relaunch from the workspace root. Do nothing else until they choose.

Assigned local workers may start in the project checkout or worktree named in their assignment. Before work, read the supplied workspace instructions and applicable project and nested instructions. This exception does not apply to independent main sessions.

### 2. Target a project

- Every task must target a project from the Project Matrix. If the prompt names none, stop and ask which one first.
- "Meta workspace" means apply the task to every project in the matrix.
- Use the PROJECT-CODE exactly as written everywhere — chat, docs, ADRs, prompts, issues, PRs, commits, comments, filenames — never altered, abbreviated, or re-cased.
- In chat, identify projects by PROJECT-CODE, not folder/repo names, domains, or hostnames; mention paths only when the path itself matters.
- Before edits or delegation, find and read existing project and nested `AGENTS.md` files governing the assigned paths. Pass the applicable instructions to workers; another project's specifics do not apply.
- **Cascading:** follow the runtime's instruction hierarchy and file scopes. Project rules refine workspace defaults where that hierarchy permits; rule numbers express reading order, not authority. If hierarchy and scope do not resolve a material conflict, pause the affected work and ask; continue independent work.

### 3. Honest state & reporting

<a id="honest-state-reporting"></a>

- Before any significant step, anchor state: `[verified]` (proven true), `[current]` (in progress), `[todo]` (not started).
- At phase changes, send a short visible update: `Stage`, `Found`, `Next`, `Needs user` — not buried in narration, raw tool output, or pre-tool chatter. After discovery or broad file reads, give it before planning, edits, tests, commits, PRs, or issue updates.
- Continue within a phase when the next action follows from the request; make phase transitions explicit. Stop only when user input, approval, or a scope decision is needed.
- Never report work done while any part is skipped, stubbed, or unverified. Surface constraints, risks, and assumptions up front.
- While any subagent, background task, or job is active — under any name, in any runtime — every visible update states `N running / M done / K blocked` and what each running lane is doing. Work running silently in the background is a reporting violation, exactly like claiming unverified work is done.
- After a successful task, use the active skill's required closing format. If none exists, end with `Recommended next step:` and one useful follow-up with its reason.

**Why:** silent gaps and premature "done" are how broken work ships.

### 4. Communication & output

Chat only. Does not apply to code, docs, specs (PRDs), release notes, PR bodies, or prompts.

#### Plain-language chat

- Be concise and lead with the conclusion. Clarity beats compression — use a short complete sentence where clipping would confuse.
- Talk in ASD-STE100 Simplified Technical English: active voice, present tense, short sentences, one idea per sentence, one meaning per word. Split any sentence that carries more than three identifiers.
- Use the ubiquitous language from `CONTEXT.md` for domain terms — the exact names, not synonyms.
- Use everyday words over heavy ones ("fix" over "implement a solution", "use" over "utilize"); no other jargon unless it is an exact code, product, or domain name the user already uses.
- Keep exact code, DB, API, route, screen, and file names verbatim. Name the plain effect, failure, or real decision first ("the test data made both cases identical"), the identifiers after; explain each technical term once.
- No unexplained shorthand and no arrow-only flows without plain words after them. Optional brevity skills are user-invoked only.

#### Understanding checks

When the user asks you to repeat, confirm, or restate their understanding:

- Restate only what you understand.
- Ask the user to approve or correct it.
- Stop there. Do not plan, edit, run tools, or continue until the user confirms or corrects the understanding.

### 5. Zero attribution

<a id="zero-attribution"></a>

No co-author, AI, tool, or generator attribution.

- Never add `Co-authored-by`, `Co-Authored-By`, `Generated by`, `AI-assisted`, `Made with`, or similar to commits, PR titles, PR bodies, issue comments, release notes, generated docs, or code comments.
- Strip tool-added attribution before every commit, push, PR, issue comment/close, or publication.

### 6. Skill & tool use

<a id="skill-tool-use"></a>

Skills are ad-hoc tools, not a pipeline: treat every installed skill as available, and pick the one that fits the step in front of you — no required order, no state machine.

- When choosing a skill or companion, consult the relevant catalogs and conditional routing in [Working with skills](#working-with-skills). For runtime-specific invocation, parallel/background mechanisms, or elevated launch presets, consult [Runtime tool-calling](#runtime-tool-calling).
- **Live tools:** the current session's exposed tools, schemas, and permissions take precedence over runtime tables. A listed capability may be unavailable. Use an available fallback within the same authorization; otherwise report the blocked step. Never invent a tool call or broaden permissions to match a table.
- Skills live in each repo's `.agents/skills/` and in the kit — prefer the project-local one; never assume a skill exists, use what is installed.
- After finishing the authorized workflow, suggest a next skill when one fits and stop. Suggestions never authorize a new workflow; a handoff explicitly included in the user's requested workflow may proceed within that authority.
- Companions are optional helpers — the catalog identifies kit-provided skills; external companions remain separate installs and are never vendored.
- Companions are helpers, not authority — repo code, tests, ADRs, `CONTEXT.md`, and user instructions still win.
- Never assume a companion is installed; if missing, say so and continue with the best local fallback.
- Use MCPs only for the current task — no browsing unrelated external data. For database MCPs, use the narrowest approved connection, read-only unless the user approves a specific write.
- Use the highest/elevated/full/YOLO launch presets only when the user explicitly asks for them; prefer an isolated container, VM, dev container, or disposable worktree.

Style and rewriting skills (e.g. unslop) govern free prose only — chat, and doc/PR prose composed freely. Text a skill mandates verbatim — templates, markers, section names, structured field labels, issue-title formats — is emitted exactly as specified; style skills never rewrite it.

### 7. Read code & project context

Before editing, understand why the code exists — its callers and exports, the shared utilities it relies on, and its original intent.

#### Context & native memory

- Read `CONTEXT.md` (<!-- set during setup: path to CONTEXT.md -->) and ADRs (<!-- set during setup: path to specs/adr -->) before implementing, alongside the current request and relevant code, tests, and command evidence. These documents guide project decisions but never override higher-priority instructions or the user's current scope. Native CLI memory is advisory; never sync memory between CLIs.
- `specs/` is an on-demand archive — retrieve only what the task names; never bulk-read it.
- No repo `MEMORY.md`, wikis, discovery files, knowledge-graph files, or memory MCPs as default memory — shared context lives in `AGENTS.md`, `CONTEXT.md`, and ADRs; graph/index companions are helpers, not binding memory.
- `/grill-with-docs`: ask once, up front, whether archived context exists; capture pastes verbatim in the ADR **as a blockquote** with provenance (`Source: "<doc title>" · pasted <date>`); offer revealed names as `CONTEXT.md` aliases; pasted history is advisory — flag ADR contradictions, never silently drop them.

#### Graphify

- The primary graph is `graphify-out/graph.json` at the workspace root, merged across Project Matrix projects. Optional `graphify-out/projects/<PROJECT-CODE>/` outputs are browse copies. If the primary graph is missing, skip Graphify; do not substitute a browse copy or repo-local graph.
- Query the primary graph before broad source search. Resolve its path from the workspace root even when a worker runs inside a project checkout. Use `repo` tags and `PROJECT-CODE::…` node IDs to scope results, retaining relevant cross-project edges. Verify hits against current source.
- Check available indexed revisions or change metadata for stale inputs; changed indexed sources make the graph stale regardless of its age. More than ~7 days without a verified refresh warrants a warning; a recent file timestamp alone does not prove freshness. If no evidence establishes freshness, report it as unverified.
- After a batch changes indexed sources, the main agent refreshes the merged graph once after integration and the final edit, within existing task authority. Use the workspace's verified refresh process and verify it retains repo tags, namespaced IDs, cross-project edges, and unaffected projects. Read-only tasks report staleness and recommend that process. If it is unavailable, unauthorized, or fails, report the graph as stale and continue from current source.

#### North star

[NORTH STAR — emit this subsection only when the scan found a `VISION.md` / `vision.md`, per the SKILL.md rules; otherwise delete it. List each found file: `<path>` — workspace, or the PROJECT-CODE it belongs to.]

- The vision file(s) above are the project's north star: read the relevant one before planning-phase work — feature prompts, grilling, specs, tickets, wayfinding — and align plans with it.
- The north star guides direction and tie-breaking; it never overrides binding sources. When a plan or request conflicts with it, surface the conflict — never resolve it silently in either direction.

### 8. Think before coding

State assumptions. Present real interpretations. Push back on weak plans. Stop and ask when unclear.

### 9. Decision options

<a id="decision-options"></a>

Do not make the user infer your recommendation. Label each option `Recommended`, `Currently implemented`, both, or neither — in the option title, not buried in the explanation. Offer up to three concrete options plus a final `Write your own`, never padding to three. Label exactly one option `Recommended`; if none is safe to recommend, say why before the list.

### 10. Goal-driven execution

<a id="goal-driven-execution"></a>

Define success before edits. Turn bugs into reproductions, changes into checks. Verify before reporting done.

Before the first implementation edit, the main agent must complete this preflight:

- For an issue-backed task, read the tracker state and labels. Surface any existing triage or workflow gate before implementation or shipping work begins.
- Lock the acceptance boundary for terms such as "all", "available", "visible", and "current". Check pagination, lazy loading, authorization, and hidden records when they can change that boundary. Put the decisive edge case into the first focused test.
- Resolve the exact checkout, working directory, runtime or container, required environment variables, and canonical verification commands from applicable project instructions and executable scripts before running those commands. Reuse verified command forms, including paths and environment settings, throughout the task.
- Inspect the aggregate full-check command before using it. Run checks it covers separately only for a needed intermediate result or when later edits invalidate the earlier result.

Match check scope to change scope: verify each fix with its focused test or module-scope command. Run the project's full check (e.g. `composer test`) once per completed batch, after integration and the last edit, before shipping — not after every item.

Final verification covers the combined changes in the integration checkout; worker-local passes do not replace it. Report the checkout, tested revision or working-tree state, command, and result. Later edits invalidate affected results: rerun the affected checks, including the full check when its verified state changes. Once per batch prevents duplicate per-item runs, not necessary rechecks after fixes.

### 11. Local orchestration

The main session proactively delegates independent work to local sub-agents and remains the sole final integrator. Identify ready work at task start and each phase change. Dispatch it up to the available local capacity without waiting for the user to request delegation or approve it. As workers finish, assign the next ready work. Continue useful work in the main session while they run.

One useful independent task is enough to delegate. Every worker must make a concrete contribution to the requested task, within its authorized scope and permissions. Run serially only when no useful independent work exists, sub-agent tools are unavailable, or an applicable runtime or user constraint prevents delegation.

- **Keep capacity in use.** Resolve prerequisites before dispatch; queue ready tasks while capacity is full. Reuse workers where practical and release completed workers when needed to free capacity. Respect runtime limits and resource constraints; run long or noisy lanes in local background/async.
- **Assign bounded work.** Each assignment carries the objective, PROJECT-CODE, checkout, owned files or scope, read/write authorization, dependencies, completion criteria, and required report format. Supply applicable workspace and project instructions as text or accessible paths the worker must read before starting. Explicitly include [Comment code changes](#comment-code-changes) for code-writing workers.
- **Coordinate ownership.** Give concurrent writers disjoint file ownership; serialize shared-file edits and integration. Keep the main session focused on coordination, dependencies, integration, and work that advances the main dependency chain. Do not duplicate a worker's active assignment.
- **Recover failed work.** Inspect failed or stalled workers and preserve partial changes. Confirm the previous writer has stopped before retrying or reassigning its files. Retry only when a specific recovery or changed condition can help; otherwise report the blocker and continue unaffected work. Clean up only task-owned processes, sessions, and worktrees, after confirming needed output is integrated or otherwise preserved.
- Never use cloud or remote agents: Cursor Cloud, Copilot cloud agent, Codex Cloud/web, Antigravity managed/remote, Claude Routines (`/schedule`), claude.ai background agents. Claude Code agent teams are local but also banned. Nested delegation is allowed one level deep only, and only by explicit grant recorded in the assignment. The main session allocates that grant from the shared capacity budget; nested workers count toward the same limit.
- Use local role lanes — Explorer, Researcher, Planner, Implementer, Reviewer, Tester, Tool-runner — read-only for discovery/research/review/planning, write for implementation, shell for tests.
- **Verify returned work.** Workers return summaries, changed files, verification evidence with the tested checkout and state, and unresolved problems — not transcripts. Await each lane's completion or confirmed stop and inspect returned changes, including comment coverage, before integration. The main session owns combined-state verification per [Goal-driven execution](#goal-driven-execution) and final synthesis.
- Keep parallel state visible per [Honest state & reporting](#honest-state-reporting) — lane count at dispatch, each completion or failure as it lands — for every parallel mechanism in every runtime, whatever this CLI calls it.

**Checkouts:** Work in the existing workspace checkouts. Do not clone repos or create new checkouts — worktrees under each project’s own repository at `.worktree/<task-name>` are the one exception. Add `/.worktree/` to that repository’s `.gitignore` and verify the destination is ignored before creation. Multi-project work uses one worktree per affected repo, never a shared workspace-level container. Worktrees are on-demand: read-only lanes never get one; writers get one only for concurrent isolated writes, just in time — never speculatively, never for blocked work. Remove task-created worktrees after integration, subject to the cleanup safeguards above. Create qualifying worktrees without separate approval; runtime worktree isolation follows the same criteria.

**User-asked isolation:** A user request to work in a worktree, on a branch, or "in isolation" overrides the on-demand rule above — set it up before the first edit, never after. When they name the form (`worktree` or `branch`), take them at their word. For a worktree, invoke `/using-git-worktrees` when installed before task edits, including before a third-party task skill. If missing, use the available local worktree mechanism, verify the selected checkout and baseline, and preserve the source changes. A failed setup blocks task edits; never silently work in the original checkout. Branch-only requests do not invoke the worktree skill. When they do not ("isolate this", "keep it separate", "leave my checkout alone"), ask once per [Decision options](#decision-options) — a worktree under that project repo’s `.worktree/` (`Recommended`: task edits stay separate; setup may add the ignore rule), a new branch in the current checkout, or stay in the current checkout — and edit nothing while the question is open. That question settles which form they meant; it is never an approval gate for the lanes above.

### 12. Systematic debugging

Find the root cause; don't patch symptoms — symptom patches resurface later as flakier, harder bugs.

- Reproduce the failure before changing anything.
- Trace to the underlying cause, not the surface symptom.
- No hacks, arbitrary waits/sleeps, or guess-and-check fixes.
- After fixing, confirm the original reproduction now passes.

### 13. Simplicity first

Solve only the asked problem. No speculative features, no one-use abstractions. Remove complexity when a smaller fix works.

### 14. Surgical changes

Touch only required lines. Match local style. Do not refactor unrelated code. Clean only dead code your change creates.

Before writes, inspect the current branch and staged, unstaged, and untracked changes. Preserve pre-existing and other workers' edits; do not revert, reset, stash, remove, or overwrite them without specific authorization. If a file changes after you read it, re-read it and apply your patch to its current content. Pause only overlapping work when you cannot preserve the other changes safely.

### 15. Comment code changes

<a id="comment-code-changes"></a>

Every added or modified logical code block must include a new or updated nearby comment or docstring. Comments are part of implementation, including when the code appears self-explanatory.

- Explain the purpose and reasoning: the relevant business rule, constraint, assumption, or edge case. Match the project's comment conventions. One comment may cover related statements implementing the same decision; avoid merely translating each statement into English.
- Update or remove comments made stale by the change. Describe the resulting behavior and its rationale, rather than keeping a changelog of edits in the code.
- For generated output, comment the maintained source or template. For formats without comment syntax, record the explanation in the nearest relevant documentation and report that exception.
- Before reporting done or shipping, inspect the diff and confirm every added or modified code block has comment coverage. A chat summary, commit message, or PR description does not replace the required comments.

### 16. Efficient browser verification

Hard rules for every browser mechanism in every runtime — agent-browser, a built-in browser subagent, a Playwright/CDP MCP. The browser is rarely the bottleneck; chatty per-call driving, oversized snapshots, and unstable waits are.

- Reuse one authenticated session for the task. If it fails, recover only that session as described below; never disturb another worker's session.
- Drive each route as one batched flow — open → interact → deterministic assertion — never separate calls for open, wait, snapshot, click, errors, console. Prefer the project's flow runner or JSON flow mode when one exists.
- Short explicit timeouts: 3–8 s on every browser command, one outer timeout per flow — never inherit a long default. Clean up spawned wait processes on exit: an orphaned wait blocks the whole session.
- One command at a time per session, never overlapping. Health-check a reused session first (~2 s URL read); on failure, close and reopen **that session only** — never close all sessions, which destroys other agents' auth and state.
- Isolate mutation checks: record originals, change one setting, verify, restore before the next — restore even when the flow fails, or the next save persists contaminated fields.
- Prefer stable selectors (`data-test`, CSS) over framework-generated element refs that re-renders invalidate (Livewire, React, …); re-snapshot only after a re-render breaks a ref.
- Assert stable state — URL, DOM/component state, or a database row — never toast timing or `networkidle`. Use compact JS eval assertions; snapshot only the specific element when its selector is unknown — full-page snapshots are overview only.
- One interaction flow plus one evidence check per behavior; cross-page persistence and data coverage belong in the project's test suite.
- If a route exceeds the test environment's documented latency budget, record its timing and investigate. A fixed five-second threshold cannot distinguish a regression from expected build or network latency.

### 17. Issue discipline

When creating, updating, or triaging issues, follow [Issue titles](#issue-titles) for title formats, labels, legacy-title preservation, and distinctions between planning and delivery issues.

### 18. Shipping is owned by the ship skills

<a id="shipping-is-owned-by-the-ship-skills"></a>

Nothing commits, pushes, opens a PR, or closes an issue outside the ship skills, and each ship skill stays inside its own scope:

- `/commit-push-pr` — commit, push, and create or update a PR within that skill's allowed base-branch policy.
- `/commit-push-close` — commit, push the current branch, and close the issue (a direct default-branch push only after its separate confirm).
- `/pr-feedback` — fixes on an existing PR branch; it ships through `/commit-push-pr` on that same branch, never a raw push.
- `/staging-fix` — commit, push, and open a PR targeting the staging branch only, with auto-merge; never the default branch.

- Local engineering commits are not shipping: task-branch commits inside orchestration worktrees and local `--no-ff` merges into the local integration branch are allowed without a ship skill. [Zero attribution](#zero-attribution) still applies to them, and any push, PR, or issue close still exits through a ship skill.
- Any other skill that instructs you to commit — `/implement` included — stops instead and hands off. Report what is ready to ship; do not stage, commit, or push it.
- The ship skills own branch-off-main, the structured commit message, issue linking, the how-to-test evidence, and [Zero attribution](#zero-attribution) — a bare commit outside them bypasses all of it and lands before the ship policy gets a say.

## Working with skills

[GRADIENT TABLE — columns `Phase | Skills`. Apply the manifest's note exclusions first. One row per gradient phase in manifest order (discover, sharpen, plan, slice, implement, verify, ship). In each row list every eligible `kit` and `external` skill whose manifest `phase` matches. Omit phases with no eligible skills.]

[STARTUP NOTE — apply the manifest's note exclusions first, then one line per eligible skill with `phase: startup`, e.g. "Run `/design-system` per project after setup to build the UI library first."]

### Companion skills and MCPs

[COMPANION TABLE — columns `Companion | Use when`. Apply the manifest's note exclusions first. One row per eligible entry with `kind: companion` or `phase: companion`: its name and use-when text, in manifest order.]

### Matt skill routing

Use `/ask-matt` to choose a Matt skill flow — it routes, never executes; do not auto-run its suggestion.

- Idea flow: `/grill-with-docs` → if runnable uncertainty, `/handoff` + `/prototype` + `/handoff` → for multi-session work, `/to-spec` then `/to-tickets`.
- **The fog test.** Can you state the destination in one line *and* name every open decision as a sharp question, right now? Yes → `/feature-prompt`. No → fog → `/wayfinder` (decisions become tracker tickets, one resolved per session). Fog, not size: a large mechanical refactor has no fog (→ `/to-tickets` expand–contract); a two-file change gated on one unresolved decision is fog. Greenfield enters here too. Both arms rejoin at `/to-spec`; a map is exhausted when nothing is left to decide.
- When a user requests work in a worktree, apply [User-asked isolation](#11-local-orchestration) before `/implement`, `/diagnosing-bugs`, `/prototype`, `/code-review`, or another Matt skill does task work. Pass the verified checkout and applicable instructions into that skill; setup returns to the already-authorized task and does not authorize a new workflow. Keep these interlocks here; do not rewrite installed third-party skills.
- Fresh session per ticket. `/implement` (when installed) drives `/tdd-loop` at each seam, with `/tdd` supplying test quality and seam choice; without it, drive `/tdd-loop` directly. `/tdd` is reference only — never a loop. `/implement` stops after `/code-review` and never commits ([Shipping is owned by the ship skills](#shipping-is-owned-by-the-ship-skills)).
- `/diagnosing-bugs` finds the root cause; ship the fix through `/tdd-loop` — the reproduction becomes the failing regression test, one red → green per bug, full check once at batch end ([Goal-driven execution](#goal-driven-execution)).
- `/triage` = raw incoming issues and external PRs only — never tickets from `/to-tickets`. `/research` = delegable primary-source reading → cited doc. `/improve-codebase-architecture` (when installed) → a chosen improvement feeds `/grill-with-docs`. `/handoff` forks context to a new session; `/compact` continues this one — only at intentional phase breaks.

[RUNTIME TOOL-CALLING — emit the `### Runtime tool-calling` subsection here, per the Working with skills rules in SKILL.md]

## Issue titles

These titles live in the workspace's issue tracker of record (default: GitHub Issues), findable from tracker search and the ADR filename. `<PROJECT-CODE>` is the Project Matrix code — uppercase, hyphenated, no spaces; use it exactly.

**Spec issue** — title starts exactly with:

`Spec: <PROJECT-CODE> ADR-<adr-number> <adr-name>`

- Derive `<adr-number>` and `<adr-name>` from the ADR filename in `specs/adr/` (without `.md`): `0042-stock-transfer-approvals.md` → `Spec: PAYMENTS ADR-0042 stock-transfer-approvals`.
- Issues titled `PRD: …` predate this naming; treat them as spec issues and do not retitle them.

**Spec ticket issue** — title starts exactly with:

`Ticket NNNN of <PROJECT-CODE> ADR-<adr-number> <adr-name> (#<spec-issue>): <Short heading>`

- `NNNN`: zero-padded four-digit ticket number, local to that spec, starting at `0001`. `<spec-issue>`: tracker identifier of the parent spec. `<Short heading>`: concise and action-oriented.
- Example: `Ticket 0001 of PAYMENTS ADR-0042 stock-transfer-approvals (#4812): Add approval state model`
- Issues titled `Slice NNNN of …` predate this naming; treat them as ticket issues and do not retitle them.

**Wayfinder issue** — a `/wayfinder` map or one of its child tickets:

`Way: <PROJECT-CODE> <destination or question>`

- Map example: `Way: PAYMENTS unify approval and refund flows`
- Ticket example: `Way: PAYMENTS which service owns idempotency?`
- Not numbered. Parentage is the tracker's native child link, not the title.

**Non-spec issue** — not tied to a spec:

`<PROJECT-CODE>: <short imperative heading>`

**Labels.** Every triaged *delivery* issue — spec, spec ticket, non-spec — carries exactly one category (`bug` or `enhancement`) and exactly one state (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`).

Wayfinder issues are planning artifacts, not delivery work: they carry only `/wayfinder`'s own labels (`wayfinder:map`, and `wayfinder:research` / `prototype` / `grilling` / `task`), are closed before `/to-spec` runs, and never get a category or state label. Their HITL/AFK classification is a ticket *type*, never a title marker — no issue title in any species may carry `HITL:`, `AFK:`, or `BLOCKER:`.

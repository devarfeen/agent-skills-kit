# Best Practices: Combining Skills Intentionally

Human-facing teaching guide. Do not load this file into `AGENTS.md`, shims, or model context.

This is the *intended* way to combine the local kit skills with the wider ecosystem. It exists to teach others how these skills fit together — not as a rigid procedure, but as a set of habits that consistently raise the quality of agent-driven work.

The guiding idea: **Agentic Coding is not Vibe Coding.** You stay strategic — steering scope and tradeoffs — while the agent executes against evidence and traceable decisions. The skills are the rails that keep it honest.

---

## 1. The Mental Model

### Skills are ad-hoc tools, not a pipeline

Every skill is installed globally and is always available. The agent treats them all the same — **there is no "local skill" vs "third-party skill" distinction at use time.** The only place the distinction matters is maintenance: to *update* a skill, update it from its original source repo.

There is no state machine and no required order. You pick the skill that fits the step in front of you.

### The gradient

Work tends to flow along one gradient. Memorize the shape, not a script:

```text
discover → sharpen → plan → slice → implement → verify → ship
```

| Phase | What you're doing | Skills that fit |
| :--- | :--- | :--- |
| **discover** | Understand existing behavior before touching it | `/feature-discovery`, `/port-feature` (when porting from a reference) |
| **sharpen** | Turn a rough idea into a precise prompt | `/feature-prompt` (no fog), `/wayfinder` (fog — decisions gate the scope) |
| **plan** | Challenge the plan, capture the decision | `/grill-with-docs` (→ ADR), `/to-spec` (→ spec/PRD) |
| **slice** | Break the plan into thin, grabbable units | `/to-tickets` |
| **implement** | Build it test-first | `/implement` (optional ticket driver), `/tdd-loop` (the procedure — gates + exception protocol), `/tdd` (test-quality reference) |
| **verify** | Prove it works | `/code-review`, `/pixel-audit` (per-page pixel conformance), manual QA, `/polish-batch` (cosmetic tail), `/integration-contract` (cross-repo seam), `/diagnosing-bugs` |
| **ship** | Land it with proof | `/commit-push-close`, `/commit-push-pr` |

### The fog fork

The gradient forks once, right after discover. Ask: **can you state the destination in one line, and name every open decision as a sharp question, right now?**

- **Yes** — no fog. `/feature-prompt` writes a PR-sized prompt, `/grill-with-docs` challenges it.
- **No** — that's fog. `/wayfinder` charts the decisions as tickets on the tracker and resolves them one per session (see Workflow E).

Fog, not size, is the test. A forty-file mechanical rename has nothing left to decide — it isn't fog, and it belongs in `/to-tickets` as expand–contract. A two-file change blocked on one unresolved architectural decision *is* fog, however small the diff. Both arms rejoin at `/to-spec`.

### Implement is a driver, not a rival

Three layers, each of the outer two optional:

| Layer | Skill | Owns |
| :--- | :--- | :--- |
| Ticket | `/implement` *(optional)* | Works one ticket; typecheck cadence; full suite once at the end; hands to `/code-review` |
| Behavior | `/tdd-loop` *(kit)* | Red → green → widen → refactor; the completion evidence; the exception protocol |
| Test quality | `/tdd` *(optional)* | What a good test is; where seams go; the anti-patterns |

Without `/implement`, drive `/tdd-loop` directly per ticket — same outcome, one less wrapper. `/tdd` is a reference document, not a loop; using it alone gets you no witnessed red. And `/implement` **stops after `/code-review`**: its own text says to commit, but shipping belongs to the ship skills, which own branch-off-main, issue linking, and test evidence.

### Two rails run alongside the gradient

Not every skill lives on the discover→ship line:

- **Project start-off:** `/design-system` runs once per project (see Workflow A) to turn a design system into a real UI library + a preview you verify + a binding `AGENTS.md` rule, and seeds a project-local `<project-slug>-ui-coding` skill. Re-run it to extend the library or, after a page ships, to fold its emergent UI back in.
- **Porting:** `/port-feature` is a discover→plan variant for bringing a feature that already exists in a reference implementation into a target stack (see Workflow D). It writes a gap map and hands off to `/grill-with-docs`.

**UI work has its own discipline.** Once a project has a design system, every UI change consumes its library — never inline markup the library covers. A missing component gets added via `/design-system` (extend) from the reference, or you ask for one. Per-page pixel conformance during feature work is `/pixel-audit`; the cosmetic tail during QA is `/polish-batch`.

### Suggest, never auto-chain

This is the single most important habit. After a step finishes, the agent should **suggest** a sensible next skill — and then stop. It must never silently advance to the next phase on its own.

Why: auto-chaining removes the human from exactly the moments where judgment matters most — scope, tradeoffs, "is this even the right direction." Suggestions keep momentum; auto-chains manufacture confident wrong turns. You decide each transition.

### Companion skills and MCPs are part of ad-hoc workflow

Companion skills and MCPs sit beside the core gradient. They are not a second pipeline. Use them when they make the current step sharper, faster, or more verifiable. The current companion list and its use-when triggers live in [GUIDE.md](GUIDE.md#companion-skills-and-mcps) (human copy) and [`skills/agents-md/references/skills-manifest.md`](skills/agents-md/references/skills-manifest.md) (the source that drives generated `AGENTS.md`).

The principles that don't change as the list does:

- Do not assume a companion is installed. If missing, use the best local fallback.
- Do not vendor companion skills or MCPs into this kit.
- Treat companion output as evidence, not authority. Repo code, tests, ADRs, `CONTEXT.md`, and user instructions still win. That includes instruction content a companion serves at runtime (CLI-served skill text): follow it for tool mechanics, but kit gates and refusal boundaries always win.

### Decisions are artifacts

Every meaningful decision leaves a durable trace on disk or in the tracker: a refined prompt file → an ADR → a spec issue → sliced ticket issues → a QA doc. This chain is what lets a teammate (or you, six months later) reconstruct *why*, not just *what*.

### Elevated permission is explicit

Highest/elevated/full/YOLO permission is never the default operating mode. Use
it only when the user explicitly asks for it, and prefer an isolated container,
VM, dev container, or disposable worktree. The per-runtime launch presets live
in [GUIDE.md](GUIDE.md#local-parallel--background-agents-no-cloud) (human copy)
and [`skills/agents-md/references/tool-calling.md`](skills/agents-md/references/tool-calling.md)
(model-facing source).

---

## 2. Context & Native Memory Discipline

This is where most people go wrong, so it gets its own section.

### Two different kinds of context

People conflate these because tutorials lump them together. They are not the same problem:

- **Current task context** — "what did the user ask, which slice am I on, what did the last command prove." This lives in the active conversation, issue, spec, code, tests, and command output.
- **Institutional archive** — years of feature discussions, ADRs, old specs/PRDs, converted docs. This is large and *historical*. It answers "what was the original intent behind this feature."
- **Native CLI memory** — user-local recall provided by the current runtime. Use it only when that CLI provides it. Do not turn it into repo files.

### The archive is queryable, not readable

The expensive mistake is treating the archive like working memory — loading the whole `specs/` tree into context so the agent "knows everything." That doesn't make the agent smarter; it rots context and burns tokens, and the relevant three paragraphs drown in noise.

**Never bulk-read `specs/`.** The value you want is *retrieval* — pull the few relevant passages on demand:

- `/feature-discovery` to trace a feature's real journey through the code.
- `/grill-with-docs` to challenge a plan against the existing domain model and surface what's missing.

These tools are how you get "tell me where I'm wrong about this feature" — without making the agent read everything.

### Retrieval order

When sources conflict, this is the precedence:

1. **Binding** — `CONTEXT.md` (domain terminology) and `specs/adr/` (accepted decisions). Read before implementing. These override informal usage.
2. **Current task context** — the active request, issue or spec, named docs, current code, tests, and command evidence.
3. **Native CLI memory** — user-local runtime recall when enabled. Never override binding sources.

---

## 3. Workflow A — Full Project Start-Off

Run once per workspace, at the workspace-root level (not inside a single repo).
The step-by-step sequence lives in [GUIDE.md](GUIDE.md#first-time-setup):
**`/agents-md`** → **`/setup-matt-pocock-skills`** → **fill the `AGENTS.md`
placeholders** → **`/design-system`** once per project that has UI (re-run
`extend` as the design grows or to fold a shipped page's UI back in). The
chat-visible behaviors this establishes (PROJECT-CODEs, phase updates,
understanding checks) are bound by the generated `AGENTS.md` rules themselves.

> **Why placeholders, not guesswork:** `/agents-md` runs *before* you've decided where context lives, so it must not invent a path. Leaving labelled placeholders turns the fill step into a mechanical edit instead of a rewrite. `/agents-md` writes the *rules of engagement*; `/setup-matt-pocock-skills` owns the *locations*.

### Optional: Graphify across the Project Matrix

When [Graphify](https://github.com/safishamsi/graphify) is installed and broad codebase questions would otherwise mean huge `rg` sweeps, treat it as a workspace-level companion — not binding memory.

Graphify builds two layers: **AST** (structural code edges, free) and **LLM semantic** (docs, ADRs, inferred cross-file links, costs tokens). First build always needs the full pass; day-to-day refresh can stay AST-only.

**Build once after setup (or when you add a folder to the matrix):**

1. From the workspace root, `graphify extract <path>` (AST + LLM) for each Project Matrix folder (not the `.` meta row). Set `GEMINI_API_KEY` for headless semantic extraction, or use `/graphify <path>` per project.
2. `graphify merge-graphs ... --out graphify-out/graph.json` at the workspace root.
3. Query from the root: `graphify query "..."`, `graphify path "A" "B"`, `graphify explain "X"`.

**Refresh all projects in one pass:**

| Cadence | Loop | When |
| :--- | :--- | :--- |
| **AST** | `graphify update <path>` per matrix folder → re-merge | After code edits; free and incremental |
| **Full LLM** | `graphify extract <path>` per matrix folder → re-merge | Docs/ADRs/specs changed, graph ~7+ days old, or cross-document links look wrong |

Full command examples: [GUIDE.md — Graphify in multi-project workspaces](GUIDE.md#graphify-in-multi-project-workspaces).

**Habits:**

- **Per project, merge at root.** Never run `/graphify` on each subfolder from the workspace root — outputs collide in the same `graphify-out/`. `graphify extract` writes inside each project.
- **Re-merge after every batch update.** Per-project graphs and the workspace merged graph are different files; updating projects without merging leaves cross-project queries stale.
- **Match refresh to what changed.** Code-only week → AST loop. Docs or binding context (`CONTEXT.md`, `specs/adr/`) moved → full LLM re-extract on affected projects.
- **Verify against code.** Graphify is evidence that speeds discovery (`/feature-discovery`, `/integration-contract`); repo code and tests still win when they disagree.
- **Do not bulk-read the graph.** Query narrowly (`graphify query`, `path`, `explain`) the same way you retrieve from `specs/` — never load `graph.json` or `GRAPH_REPORT.md` wholesale into chat.
- **Cadence:** AST loop after active coding days; full LLM loop weekly or before a multi-project spec. Discovery skills may suggest an update but stay read-only — you run the refresh.

---

## 4. Workflow B — New Feature

Workspace-root level. Each step produces an artifact the next step consumes.

0. **Apply the fog test.** If the destination and its open decisions aren't sharp yet, this isn't Workflow B — go to Workflow E and come back at step 3.
1. **`/feature-prompt`** — describe what you want for a given project. It infers what it can from cheap repo evidence, asks only for what's missing, and saves a **refined prompt file** to disk.
2. **`/grill-with-docs`** — pass it the prompt file. It grills in **frontier rounds**: each round asks every question whose prerequisites are already settled, numbered and with a recommended answer; your answers reshape the tree and unlock the next round. Facts it can look up itself go to sub-agents, never to you. It challenges the plan against your domain model and writes an **ADR** to disk; done when the frontier is empty.
3. **`/to-spec`** — run it on the ADR. It publishes a **spec** (you may know it as a PRD) to your configured tracker (GitHub issue is convenient — the CLI can fetch it back cheaply).
4. **`/to-tickets`** — run it on the spec issue number. It creates **sub-issues / vertical-slice tickets**, each declaring its blocking edges (native sub-issue and blocking links where the tracker has them), and auto-applies ready labels. No separate `/triage` step is needed in this path.
5. **`/implement`** *(optional)* — work the ticket frontier one ticket at a time, fresh session each. It drives `/tdd-loop` at each pre-agreed seam (Red → Green; refactoring rides the review stage), typechecks as it goes, runs the full suite once at the end, and hands to `/code-review`. Without `/implement` installed, invoke **`/tdd-loop`** directly per ticket for the same result. It stops there — it does not commit.
6. **After each slice, the agent suggests a next step** — usually `/code-review`, then `/commit-push-close` or `/commit-push-pr`, sometimes `/release-notes`. You choose. (`/code-review` after each slice is a strong default.)
7. **Verify** — prove the slice does what the ADR/spec asked, using what applies:
   - **`/pixel-audit`** — for a page that must match a design, audit it against its source of truth (Figma or reference screens) and clear the element-level gate before calling it done.
   - **Manual QA + `/polish-batch`** — verify against the QA doc; capture the cosmetic tail (copy/spacing/alignment/wrong-string nits) without fixing them, then dispatch per PROJECT-CODE in one pass. Anything touching behaviour, data, or an interface is not a nit — route it back to `/to-tickets`.
   - **`/integration-contract`** — when the spec touches more than one PROJECT-CODE, build the cross-repo seam contract and run its smoke gate before shipping. Single-project specs skip it automatically.
8. **Ship** — at the end of a slice, a single issue, or the whole spec, run `/commit-push-close` or `/commit-push-pr`.
9. **Feed UI back** *(if the slice grew the design system)* — run `/design-system` (extend) to promote new reusable UI into the library, preview, `specs/design-system/`, the `AGENTS.md` reference, and the `<project-slug>-ui-coding` skill, so the next feature inherits it. This updates the design system only; it does not commit or write ADRs.

> **The thread to notice:** prompt file → ADR → spec issue → ticket issues → tested code → QA doc. Each link is grabbable on its own, and the whole chain is auditable.

---

## 5. Workflow C — Debug / Bug-Fix

Workspace-root level.

1. **`/feature-discovery`** — point it at the module, sub-module, UI, or behavior the bug lives in. It traces the real code + logic journey and returns the report in chat. This is your evidence base.
2. **`/diagnosing-bugs`** — run it on that area. It finds the root cause and fixes it. If it can only *confirm the bug exists* without fully resolving it, escalate to **`/tdd-loop`**: write a failing test that reproduces the bug, watch it fail for the right reason, then make it pass to close it for good.
3. **Ship** — `/commit-push-close` or `/commit-push-pr`.

> **Why discovery first:** diagnosing without a traced journey is guess-and-check. The discovery output gives `/diagnosing-bugs` (and `/tdd-loop`) the context to target the root cause instead of patching a symptom.

---

## 6. Workflow D — Port a Feature

Bringing a feature that already works in a **reference** implementation (often a legacy repo) into a **target** stack.

1. **`/port-feature`** — give it the feature, the REFERENCE PROJECT-CODE (behaviour truth), and the TARGET PROJECT-CODE (where it lands). It reads the target's binding context, traces the reference `/feature-discovery`-style, surveys what the target already has, and writes **one gap map** to `specs/port/`. The reference is truth for behaviour, workflow, navigation, permissions, and states; the target's design system is truth for UI. It suggests `/grill-with-docs` and stops.
2. **`/grill-with-docs`** — challenge the gap map; it produces the ADR using the next number in your `specs/adr/`.
3. **`/to-spec` → `/to-tickets` → `/implement`** (or `/tdd-loop` directly) — from here it rejoins Workflow B: spec, thin ticket slices, test-first build. Each UI slice consumes the target's UI library; a missing component goes through `/design-system` (extend), never a page-local one-off.
4. **Verify & ship** — `/pixel-audit` the ported screens against the reference, manual QA + `/polish-batch`, then `/commit-push-close` / `/commit-push-pr`.

> **Why a gap map first:** porting blind drags the reference's accidents across with its behaviour. The gap map separates what to preserve (behaviour, workflow, permissions) from what to re-express (UI, in the target's idiom), and names the risks before any code moves.

---

## 7. Workflow E — Large Effort Wrapped In Fog

For work whose *scope cannot be stated yet* because decisions block it — a greenfield build, a migration whose shape depends on what you find, a feature nobody has agreed the boundaries of. This is the fog arm of the fork.

Wayfinder is **planning, not doing.** It produces decisions, not deliverables. The pull to just start building is the signal you've reached the edge of the map and it's time to hand off.

1. **`/wayfinder` (chart)** — give it the loose idea. It grills you to name the **destination**, grills again breadth-first to find the open decisions, then creates a **map issue** (`wayfinder:map`) with child **ticket issues**, wiring native blocking edges so the tracker renders the frontier visually. Everything it can see but can't yet phrase sharply goes in the map's *Not yet specified* section — the fog. Everything past the destination goes in *Out of scope*, and never graduates.
   - If charting surfaces **no fog**, you didn't need a map. It stops and says so — go back to Workflow B.
2. **`/wayfinder` (work)** — one ticket per session, always. It claims the ticket by assigning it, resolves it by its type — `research` (AFK, reads primary sources), `prototype` (HITL, `/prototype`), `grilling` (HITL, `/grilling` + `/domain-modeling`), `task` (manual work that unblocks a decision) — posts a resolution comment, closes it, and indexes the answer on the map. Resolving clears fog ahead, graduating whatever is now sharp into fresh tickets.
3. **Repeat** until nothing is left to decide. The map is exhausted; the way to the destination is clear.
4. **`/to-spec`** — rejoin Workflow B at step 3. The map's decisions are the spec's input; `Way:` issues are already closed.

> **Issue hygiene:** `Way:` issues are planning artifacts. They carry only `wayfinder:*` labels — no `bug`/`enhancement`, no state label — and the kit's issue hard gate doesn't apply to them. HITL and AFK are ticket *types*, carried by labels, never written into a title.

> **Why one ticket per session:** each ticket is sized to a single fresh context window. Resolving two in one session means the second one reasons inside the first one's exhaust.

---

## 8. Weekly Cadence

- **`/release-notes`** — at the end of the week, generate a PM-friendly summary of what shipped, from the week's commits and closed work. Saved for handoff to your project manager.
- **Graphify AST refresh** *(when installed)* — `graphify update` loop per matrix folder + re-merge after active coding weeks (see [GUIDE.md](GUIDE.md#graphify-in-multi-project-workspaces)).
- **Graphify full LLM refresh** *(when installed)* — `graphify extract` loop per matrix folder + re-merge weekly, when docs/ADRs changed, or before `/integration-contract`.

---

## 9. Anti-Patterns

What separates intentional use from vibe coding:

- **Auto-chaining skills.** Letting the agent run `discover → … → ship` unattended. Suggest and stop; the human steers every transition.
- **Bulk-reading `specs/`.** Loading the whole archive "for context." Retrieve narrowly instead.
- **Treating companion tools as default memory.** Graph or index tools can help a task, but their artifacts are not binding context.
- **Updating per-project graphs but not re-merging.** Cross-project `graphify query` reads the workspace-root `graphify-out/graph.json`; stale merge = wrong answers across PROJECT-CODEs.
- **Running `/graphify` on each matrix folder from the workspace root.** Outputs overwrite the same `graphify-out/` — use `graphify extract <path>` per project instead.
- **AST-only refresh when docs moved.** `graphify update` skips LLM on code-only diffs — re-extract semantically when `CONTEXT.md`, ADRs, or specs changed.
- **Fabricating an issue before coding** for genuinely ad-hoc work. Let the ship skill create the issue at the end from the real diff and decisions.
- **Skipping discovery on a bug.** Jumping straight to a fix without tracing the journey.
- **Mixing conventions across projects.** In a multi-tech workspace, never carry one project's patterns into another. Always name the full Project from the matrix.
- **Big-bang slices.** If a slice can't be tested on its own, it's too big — back to `/to-tickets`.
- **Grilling through fog.** Trying to grill a plan whose scope is gated on undecided questions. Grilling sharpens a plan you can state; it can't produce one you can't. That's `/wayfinder`.
- **Charging at the destination.** Using `/wayfinder` to *do* the work rather than decide it, or resolving several tickets in one session. Each ticket is sized to a fresh context window; the map is done when nothing is left to decide.
- **Letting `/implement` commit.** Its own text ends "commit your work to the current branch." The ship skills own commits — branch-off-main, structured message, issue link, test evidence, zero attribution. A bare commit bypasses all of it.
- **Using `/tdd` as a loop.** Since upstream v1.1.0 it is a reference document — what a good test is, where seams go. Invoking it alone gets you no witnessed red. The procedure is `/tdd-loop`.
- **Treating native memory as authority.** Native memory is user-local recall. `CONTEXT.md` and ADRs bind.
- **Recreating secondary recall systems.** Do not create repo `MEMORY.md`, wiki, discovery, or default knowledge-graph memory. Use native CLI memory only. Use optional graph/index companions only when task-fit.
- **Inlining UI the library already covers.** Once a project has a design system, hand-rolling markup in a page instead of consuming its `<project-slug>-ui-coding` library. A missing component goes through `/design-system` (extend), not a one-off.
- **Claiming a UI fix "verified" by eye.** Per-page conformance needs `/pixel-audit`'s element-level gate — served assets, `getBoundingClientRect()`, computed styles — not a glance at a full-page screenshot.
- **Fixing nits live during QA.** Steering the agent nit-by-nit fractures the QA pass. Capture with `/polish-batch`, then dispatch in one bounded pass per PROJECT-CODE.
- **Shipping a multi-project spec on faith.** A producer surface change with no traced consumer is a risk — `/integration-contract` finds it before it breaks in another repo.
- **Porting by copy-paste.** Moving a reference feature without a `/port-feature` gap map drags its old stack conventions into the target. Preserve behaviour; re-express UI in the target's idiom.

---

## 10. Quick Reference

| Workflow | Order |
| :--- | :--- |
| **A · Project start** | `/agents-md` → `/setup-matt-pocock-skills` → fill `AGENTS.md` placeholders → `/design-system` (per UI project) |
| **B · New feature** *(no fog)* | `/feature-prompt` → `/grill-with-docs` → `/to-spec` → `/to-tickets` → `/implement` *(or `/tdd-loop`)* → `/code-review` → `/pixel-audit` → manual QA → `/polish-batch` → `/integration-contract` (multi-project) → `/commit-push-*` |
| **C · Debug** | `/feature-discovery` → `/diagnosing-bugs` → (`/tdd-loop` if needed) → `/commit-push-*` |
| **D · Port a feature** | `/port-feature` → `/grill-with-docs` → `/to-spec` → `/to-tickets` → `/implement` *(or `/tdd-loop`)* → `/pixel-audit` → `/commit-push-*` |
| **E · Large effort** *(fog)* | `/wayfinder` (chart) → `/wayfinder` (work, one ticket per session) → map exhausted → `/to-spec` → rejoins B |
| **UI / design system** | `/design-system` bootstrap, then `extend` as it grows or after a page ships |
| **Weekly** | `/release-notes` |

The fork between **B** and **E** is the fog test: can you state the destination *and* every open decision, sharply, right now?

Remember: these are the paths you *usually* take, not rails the agent rides on its own. Pick the skill that fits the step, ship thin slices, keep every decision traceable, and let the agent suggest — never auto-advance — the next move.

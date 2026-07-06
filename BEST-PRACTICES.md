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
| **sharpen** | Turn a rough idea into a precise prompt | `/feature-prompt` |
| **plan** | Challenge the plan, capture the decision | `/grill-with-docs` (→ ADR), `/to-prd` (→ PRD) |
| **slice** | Break the plan into thin, grabbable units | `/to-issues` |
| **implement** | Build it test-first | `/tdd` |
| **verify** | Prove it works | `/review`, `/pixel-audit` (per-page pixel conformance), manual QA, `/polish-batch` (cosmetic tail), `/integration-contract` (cross-repo seam), `/diagnosing-bugs` |
| **ship** | Land it with proof | `/commit-push-close`, `/commit-push-pr` |

### Two rails run alongside the gradient

Not every skill lives on the discover→ship line:

- **Project start-off:** `/design-system` runs once per project (see Workflow A) to turn a design system into a real UI library + a preview you verify + a binding `AGENTS.md` rule, and seeds a project-local `<project>-ui-coding` skill. Re-run it to extend the library or, after a page ships, to fold its emergent UI back in.
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
- Treat companion output as evidence, not authority. Repo code, tests, ADRs, `CONTEXT.md`, and user instructions still win.

### Decisions are artifacts

Every meaningful decision leaves a durable trace on disk or in the tracker: a refined prompt file → an ADR → a PRD issue → sliced sub-issues → a QA doc. This chain is what lets a teammate (or you, six months later) reconstruct *why*, not just *what*.

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

- **Current task context** — "what did the user ask, which slice am I on, what did the last command prove." This lives in the active conversation, issue, PRD, code, tests, and command output.
- **Institutional archive** — years of feature discussions, ADRs, old PRDs, converted docs. This is large and *historical*. It answers "what was the original intent behind this feature."
- **Native CLI memory** — user-local recall provided by the current runtime. Use it only when that CLI provides it. Do not turn it into repo files.

### The archive is queryable, not readable

The expensive mistake is treating the archive like working memory — loading the whole `docs/` tree into context so the agent "knows everything." That doesn't make the agent smarter; it rots context and burns tokens, and the relevant three paragraphs drown in noise.

**Never bulk-read `docs/`.** The value you want is *retrieval* — pull the few relevant passages on demand:

- `/feature-discovery` to trace a feature's real journey through the code.
- `/grill-with-docs` to challenge a plan against the existing domain model and surface what's missing.

These tools are how you get "tell me where I'm wrong about this feature" — without making the agent read everything.

### Retrieval order

When sources conflict, this is the precedence:

1. **Binding** — `CONTEXT.md` (domain terminology) and `docs/adr/` (accepted decisions). Read before implementing. These override informal usage.
2. **Current task context** — the active request, issue or PRD, named docs, current code, tests, and command evidence.
3. **Native CLI memory** — user-local runtime recall when enabled. Never override binding sources.

---

## 3. Workflow A — Full Project Start-Off

Run once per workspace, at the workspace-root level (not inside a single repo).

1. **`/agents-md`** — generates the workspace-root `AGENTS.md` (the source of truth for every CLI) plus the `CLAUDE.md` shim, the Project Matrix, the Non-Negotiable Rules, and the Working-With-Skills / Context-&-Native-Memory sections. The context section ships with **placeholder paths** for `CONTEXT.md` and `docs/adr/`, deliberately left blank.
2. **`/setup-matt-pocock-skills`** — answers the project-shape questions: which issue tracker (GitHub, Linear, or filesystem), label vocabulary, and **where `CONTEXT.md` / `docs/` live**.
3. **Fill the placeholders** — ask the agent to update the generated `AGENTS.md` with the real paths your setup session just decided.
4. **`/design-system`** *(per project that has UI)* — turn that project's design system (a Figma file, a written spec, reference screens, or a guided-definition session) into named tokens + a real UI library + a preview page you eyeball to verify, document it under `docs/design-system/`, add a short binding reference to `AGENTS.md`, and seed a project-local `<project>-ui-coding` skill. Re-run it (`extend`) as the design grows or to fold a shipped page's emergent UI back into the library. It reads the target's stack from the Project Matrix, works for any stack, and never auto-chains. Steps 1–3 are once per workspace; this step is once per UI project.

Generated chat rules use Project Matrix PROJECT-CODEs instead of folder names, repo names, domains, or hostnames unless the path itself matters. At phase changes, the agent must send a visible phase update: `Stage`, `Found`, `Next`, and `Needs user`. It can continue within the same phase, but must make new phase transitions explicit. It stops only when user input, approval, or a scope decision is needed. If you ask the agent to repeat or confirm your understanding, it must ask for approval or correction and wait before continuing.

> **Why placeholders, not guesswork:** `/agents-md` runs *before* you've decided where context lives, so it must not invent a path. Leaving labelled placeholders turns step 4 into a mechanical fill instead of a rewrite. `/agents-md` writes the *rules of engagement*; `/setup-matt-pocock-skills` owns the *locations*.

---

## 4. Workflow B — New Feature

Workspace-root level. Each step produces an artifact the next step consumes.

1. **`/feature-prompt`** — describe what you want for a given project. It interviews you section by section and saves a **refined prompt file** to disk.
2. **`/grill-with-docs`** — pass it the prompt file. It runs a full Q/A session against your domain model and writes an **ADR** to disk.
3. **`/to-prd`** — run it on the ADR. It publishes a **PRD** to your configured tracker (GitHub issue is convenient — the CLI can fetch it back cheaply).
4. **`/to-issues`** — run it on the PRD issue number. It creates **sub-issues / vertical slices** and auto-applies ready labels to the slices and the parent PRD. No separate `/triage` step is needed in this path.
5. **`/tdd`** — ask the agent to work the PRD's sub-issues test-first (Red → Green → Refactor).
6. **After each slice, the agent suggests a next step** — usually `/review`, then `/commit-push-close` or `/commit-push-pr`, sometimes `/release-notes`. You choose. (`/review` after each slice is a strong default.)
7. **Verify** — prove the slice does what the ADR/PRD asked, using what applies:
   - **`/pixel-audit`** — for a page that must match a design, audit it against its source of truth (Figma or reference screens) and clear the element-level gate before calling it done.
   - **Manual QA + `/polish-batch`** — verify against the QA doc; capture the cosmetic tail (copy/spacing/alignment/wrong-string nits) without fixing them, then dispatch per PROJECT-CODE in one pass. Anything touching behaviour, data, or an interface is not a nit — route it back to `/to-issues`.
   - **`/integration-contract`** — when the PRD touches more than one PROJECT-CODE, build the cross-repo seam contract and run its smoke gate before shipping. Single-project PRDs skip it automatically.
8. **Ship** — at the end of a slice, a single issue, or the whole PRD, run `/commit-push-close` or `/commit-push-pr`.
9. **Feed UI back** *(if the slice grew the design system)* — run `/design-system` (extend) to promote new reusable UI into the library, preview, `docs/design-system/`, the `AGENTS.md` reference, and the `<project>-ui-coding` skill, so the next feature inherits it. This updates the design system only; it does not commit or write ADRs.

> **The thread to notice:** prompt file → ADR → PRD issue → sliced issues → tested code → QA doc. Each link is grabbable on its own, and the whole chain is auditable.

> **Fanning the slices out (inside herdr):** once `/to-issues` has produced the sub-issues, if you are running in [herdr](https://herdr.dev) you can run `/orchestrate-herdr` against the PRD to spin up one local coding-CLI worker tab per open issue and monitor them for test-backed completion. It is a re-runnable orchestrator — swap only the PRD URL and the coding CLI between runs — and stays local-only: no panes, no nested sub-agents, no cloud agents. The orchestrator tab never implements; it dispatches and watches.

---

## 5. Workflow C — Debug / Bug-Fix

Workspace-root level.

1. **`/feature-discovery`** — point it at the module, sub-module, UI, or behavior the bug lives in. It traces the real code + logic journey and returns the report in chat. This is your evidence base.
2. **`/diagnosing-bugs`** — run it on that area. It finds the root cause and fixes it. If it can only *confirm the bug exists* without fully resolving it, escalate to **`/tdd`**: write a failing test that reproduces the bug, then make it pass to close it for good.
3. **Ship** — `/commit-push-close` or `/commit-push-pr`.

> **Why discovery first:** diagnosing without a traced journey is guess-and-check. The discovery output gives `/diagnosing-bugs` (and `/tdd`) the context to target the root cause instead of patching a symptom.

---

## 6. Workflow D — Port a Feature

Bringing a feature that already works in a **reference** implementation (often a legacy repo) into a **target** stack.

1. **`/port-feature`** — give it the feature, the REFERENCE PROJECT-CODE (behaviour truth), and the TARGET PROJECT-CODE (where it lands). It reads the target's binding context, traces the reference with `/feature-discovery`, surveys what the target already has, and writes **one gap map** to `docs/port/`. The reference is truth for behaviour, workflow, navigation, permissions, and states; the target's design system is truth for UI. It suggests `/grill-with-docs` and stops.
2. **`/grill-with-docs`** — challenge the gap map; it produces the ADR using the next number in your `docs/adr/`.
3. **`/to-prd` → `/to-issues` → `/tdd`** — from here it rejoins Workflow B: PRD, thin slices, test-first build. Each UI slice consumes the target's UI library; a missing component goes through `/design-system` (extend), never a page-local one-off.
4. **Verify & ship** — `/pixel-audit` the ported screens against the reference, manual QA + `/polish-batch`, then `/commit-push-close` / `/commit-push-pr`.

> **Why a gap map first:** porting blind drags the reference's accidents across with its behaviour. The gap map separates what to preserve (behaviour, workflow, permissions) from what to re-express (UI, in the target's idiom), and names the risks before any code moves.

---

## 7. Weekly Cadence

- **`/release-notes`** — at the end of the week, generate a PM-friendly summary of what shipped, from the week's commits and closed work. Saved for handoff to your project manager.

---

## 8. Anti-Patterns

What separates intentional use from vibe coding:

- **Auto-chaining skills.** Letting the agent run `discover → … → ship` unattended. Suggest and stop; the human steers every transition.
- **Bulk-reading `docs/`.** Loading the whole archive "for context." Retrieve narrowly instead.
- **Treating companion tools as default memory.** Graph or index tools can help a task, but their artifacts are not binding context.
- **Fabricating an issue before coding** for genuinely ad-hoc work. Let the ship skill create the issue at the end from the real diff and decisions.
- **Skipping discovery on a bug.** Jumping straight to a fix without tracing the journey.
- **Mixing conventions across projects.** In a multi-tech workspace, never carry one project's patterns into another. Always name the full Project from the matrix.
- **Big-bang slices.** If a slice can't be tested on its own, it's too big — back to `/to-issues`.
- **Treating native memory as authority.** Native memory is user-local recall. `CONTEXT.md` and ADRs bind.
- **Recreating secondary recall systems.** Do not create repo `MEMORY.md`, wiki, discovery, or default knowledge-graph memory. Use native CLI memory only. Use optional graph/index companions only when task-fit.
- **Inlining UI the library already covers.** Once a project has a design system, hand-rolling markup in a page instead of consuming its `<project>-ui-coding` library. A missing component goes through `/design-system` (extend), not a one-off.
- **Claiming a UI fix "verified" by eye.** Per-page conformance needs `/pixel-audit`'s element-level gate — served assets, `getBoundingClientRect()`, computed styles — not a glance at a full-page screenshot.
- **Fixing nits live during QA.** Steering the agent nit-by-nit fractures the QA pass. Capture with `/polish-batch`, then dispatch in one bounded pass per PROJECT-CODE.
- **Shipping a multi-project PRD on faith.** A producer surface change with no traced consumer is a risk — `/integration-contract` finds it before it breaks in another repo.
- **Porting by copy-paste.** Moving a reference feature without a `/port-feature` gap map drags its old stack conventions into the target. Preserve behaviour; re-express UI in the target's idiom.

---

## 9. Quick Reference

| Workflow | Order |
| :--- | :--- |
| **Project start** | `/agents-md` → `/setup-matt-pocock-skills` → fill `AGENTS.md` placeholders → `/design-system` (per UI project) |
| **New feature** | `/feature-prompt` → `/grill-with-docs` → `/to-prd` → `/to-issues` → `/tdd` → `/review` → `/pixel-audit` → manual QA → `/polish-batch` → `/integration-contract` (multi-project) → `/commit-push-*` |
| **Port a feature** | `/port-feature` → `/grill-with-docs` → `/to-prd` → `/to-issues` → `/tdd` → `/pixel-audit` → `/commit-push-*` |
| **UI / design system** | `/design-system` bootstrap, then `extend` as it grows or after a page ships |
| **Debug** | `/feature-discovery` → `/diagnosing-bugs` → (`/tdd` if needed) → `/commit-push-*` |
| **Weekly** | `/release-notes` |

Remember: these are the paths you *usually* take, not rails the agent rides on its own. Pick the skill that fits the step, ship thin slices, keep every decision traceable, and let the agent suggest — never auto-advance — the next move.

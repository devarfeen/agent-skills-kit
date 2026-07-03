# Agent Skills Kit

A collection of reusable **skills** for six supported AI coding CLIs:
Codex CLI, Claude CLI, Antigravity CLI, Cursor CLI, Opencode CLI, and
GitHub Copilot CLI. No other agent runtime is supported by this kit.

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
    ├── agents-md/            # Generate AGENTS.md plus Claude CLI / Antigravity CLI shims
    │   ├── SKILL.md          # Required: metadata + instructions
    │   └── references/
    │       ├── tool-calling.md       # Orchestration model, role lanes, local-only policy, CLI mappings
    │       ├── cursor-tools.md       # Skill-kit → Cursor mapping
    │       └── *-tools.md            # claude, codex, copilot, antigravity, opencode
    ├── design-system/        # The design-system skill (tokens + UI library + preview + AGENTS.md reference)
    │   └── SKILL.md          # Required: metadata + instructions
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
    ├── port-feature/         # The port-feature skill (reference → target gap map)
    │   └── SKILL.md          # Required: metadata + instructions
    ├── commit-push-close/    # The commit-push-close skill
    │   └── SKILL.md          # Required: metadata + instructions
    ├── commit-push-pr/       # The commit-push-pr skill
    │   └── SKILL.md          # Required: metadata + instructions
    ├── polish-batch/         # The polish-batch skill (capture → dispatch → verify UI nits)
    │   └── SKILL.md          # Required: metadata + instructions
    ├── integration-contract/ # The integration-contract skill (cross-repo seam contract + smoke gate)
    │   └── SKILL.md          # Required: metadata + instructions
    ├── pixel-audit/          # The pixel-audit skill (per-page visual-conformance audit + gate)
    │   └── SKILL.md          # Required: metadata + instructions
    └── orchestrate-herdr/    # The orchestrate-herdr skill (herdr per-issue worker fan-out)
        └── SKILL.md          # Required: metadata + instructions
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

**Cursor CLI:** Install with `npx skills install` (skills land in
`~/.cursor/skills/` or `.cursor/skills/`). Invoke a skill with `/skill-name`
(for example `/release-notes`). Run the CLI with `agent` for interactive
sessions or `agent -p "..."` for scripts and CI.

## Workflow Guide

See [GUIDE.md](GUIDE.md) for the recommended workflow from
workspace setup and spec creation through issues, TDD implementation, PR
shipping, and release notes. If you use Matt's engineering skills, run
`/setup-matt-pocock-skills` once per repo before `/to-prd`, `/to-issues`,
`/triage`, `/diagnosing-bugs`, `/tdd`, `/domain-modeling`,
`/codebase-design`, or `/improve-codebase-architecture`. The workflow also
defines an optional `Suggested next skills`
footer pattern (recommendations only) so agents can append lightweight
before/after reminders at the end of non-trivial responses, including after
third-party skills.

The kit also covers UI and design work end to end: `/design-system` turns a
project's design system into a UI library + a verifiable preview + a binding
`AGENTS.md` rule at project start-off (re-runnable to extend as the design
grows or to fold a shipped page's UI back in); `/port-feature` maps a feature
from a reference implementation into a target stack as a gap map; and the
verify phase adds `/pixel-audit` (strict per-page visual conformance),
`/polish-batch` (the cosmetic QA tail), and `/integration-contract` (cross-repo
seam contract + smoke gate). See [GUIDE.md](GUIDE.md) and
[BEST-PRACTICES.md](BEST-PRACTICES.md) for how they fit the gradient.

Companion skills and MCPs are separate installs. They can be used beside this
kit when installed and task-fit. Current companions called out by `agents-md`:
Matt Pocock's `ask-matt` router, `domain-modeling`, and `codebase-design`;
Graphify; Codex plugin for Claude Code; Impeccable; notebooklm-py;
agent-browser; herdr; docker-expert; Laravel Boost; Figma MCP; and
MySQL/Postgres MCP. They are helpers, not default memory or a required
pipeline.

Issue-writing hard gate (required): before drafting, renaming, or publishing
any GitHub issue, verify both the title format and labels from local workspace
instructions (`AGENTS.md` and its shims). If issue-tracker vocabulary is not
loaded, stop and run `/setup-matt-pocock-skills` first. Never publish with
inferred title patterns or partial labels.

## Credits And Provenance

This repository combines original local skills with workflow ideas and companion
skills from the wider agent-skills ecosystem.

- Local skills and docs in this repository are authored and maintained by
  Arfeen Arif. Local git history shows the release-notes skill was added first,
  followed by feature-discovery, feature-prompt, agents-md, and the workflow
  guide.
- The non-negotiable discipline in `agents-md` was originally seeded by
  Forrest Chang's Karpathy-inspired `CLAUDE.md` guidelines and later expanded
  in this repo into an 11-rule core:
  https://github.com/forrestchang/andrej-karpathy-skills/blob/main/CLAUDE.md
  The upstream repository is MIT licensed. This repo records credit here rather
  than emitting source notes into generated `AGENTS.md` files.
- The workflow guide references companion skills from Matt Pocock's skills repo,
  including `ask-matt`, `setup-matt-pocock-skills`, `grill-with-docs`,
  `to-prd`, `to-issues`, `tdd`, `diagnosing-bugs`, `triage`,
  `domain-modeling`, `codebase-design`, `improve-codebase-architecture`,
  `prototype`, and `handoff`:
  https://github.com/mattpocock/skills
- `/skill-creator` is credited to Anthropic's public skills repository:
  https://github.com/anthropics/skills/tree/main/skills/skill-creator
- `/agent-browser`, the `skills` CLI, `find-skills`, and Vercel React/React
  Native best-practice skills are credited to Vercel Labs:
  https://github.com/vercel-labs/agent-browser
  https://github.com/vercel-labs/skills
  https://github.com/vercel-labs/agent-skills
- Other optional companions referenced by `agents-md`: Matt Pocock's
  `ask-matt` router (https://github.com/mattpocock/skills), Graphify
  (https://github.com/safishamsi/graphify), Codex plugin for Claude Code
  (https://github.com/openai/codex-plugin-cc), Impeccable
  (https://github.com/pbakaus/impeccable), notebooklm-py
  (https://github.com/teng-lin/notebooklm-py), herdr
  (https://github.com/ogulcancelik/herdr), docker-expert from
  antigravity-awesome-skills (https://github.com/sickn33/antigravity-awesome-skills),
  Laravel Boost (https://github.com/laravel/boost), and Figma MCP
  (https://developers.figma.com/docs/figma-mcp-server/).
- `/sentry` refers to Sentry's CLI for developers and agents:
  https://cli.sentry.dev/
- **Cursor CLI:** `AGENTS.md` is the canonical workspace context file;
  skills use `/skill-name` invocation and the `Task` tool for subagents.
  https://cursor.com/docs/cli/overview
  https://cursor.com/docs/context/skills
- **Supported runtime boundary:** This kit supports Codex CLI, Claude CLI,
  Antigravity CLI, Cursor CLI, Opencode CLI, and GitHub Copilot CLI only.
  Compatibility files such as `GEMINI.md` exist solely for supported runtimes
  that read those filenames; they do not indicate support for Gemini CLI or
  any other runtime.

## Available Skills

### `agents-md`

Generates `AGENTS.md` as the canonical agent instruction file and creates a
`CLAUDE.md` redirect shim that imports only `AGENTS.md`.

```bash
npx skills install https://github.com/devarfeen/agent-skills-kit --skill agents-md
```

**What it does**

- Generates one workspace-root `AGENTS.md` (single source of truth for all six supported CLIs) and one `CLAUDE.md` redirect shim — no per-project or per-repo files
- Restricts inputs to the `.code-workspace` file and a small scan of its folders; never reads or copies the agent's own global/user instruction files into the output
- Builds a Project Matrix — `Project | Path | Stack`, one row per workspace folder; the `Project` value is a normalized PROJECT-CODE (uppercase, hyphenated, no spaces, emojis stripped — e.g. `Payments API` → `PAYMENTS-API`), used as the single cross-context identifier across chat, prompts, PRDs, issues, discovery, release notes, PRs, commits, comments, and filenames
- Emits an 11-rule Non-Negotiable core, including Decision Options, Local Orchestration (local-only parallel/background; no cloud agents), Honest State & Reporting with visible phase updates, and Zero Attribution
- Emits a Working With Skills section: a named-skill gradient (discover → sharpen → plan → slice → implement → verify → ship), optional companion skills and MCPs, "suggest the next skill, never auto-chain", plus a Runtime Tool-Calling subsection derived from the kit's tool-calling references
- Emits a Context & Native Memory section: retrieval order (`CONTEXT.md` + `docs/adr/` binding → current task context → native CLI memory), an artifact policy forbidding repo `MEMORY.md`, wiki, discovery, and default knowledge-graph memory, a "do not bulk-read `docs/`" guard, and an archived-context rule for `/grill-with-docs`; the skill does not itself create context files
- Emits GitHub Issue Titles (title/label convention only) and an Output Style section, including approval-gated understanding checks
- `CLAUDE.md` contains only the `@AGENTS.md` forward and short redirect note — no `CONTEXT.md`, memory, wiki, or graph imports
- Keeps `AGENTS.md` concise — stable, non-obvious invariants only; detailed procedures stay in the skills and their references

**Example prompts**

| Mode | Example prompt |
| --- | --- |
| New instructions | `Generate AGENTS.md for this workspace` |
| Workspace manifest | `Create AGENTS.md and shims from my code-workspace manifest` |
| Refresh project matrix | `Update AGENTS.md PROJECT-CODEs and stacks` |

Native CLI memory defaults: [`skills/agents-md/references/memory-global-defaults.md`](skills/agents-md/references/memory-global-defaults.md).

### `design-system`

A Workflow-A (project start-off) skill, run per project after `/agents-md` →
`/setup-matt-pocock-skills` → placeholder fill, and re-runnable to extend. It
turns a provided design system into a real UI library plus a verifiable preview,
documents it under `docs/design-system/`, and adds a short binding reference in
`AGENTS.md` so that on **any** UI change every future agent consumes the library
instead of inlining one-off UI.

```bash
npx skills install https://github.com/devarfeen/agent-skills-kit --skill design-system
```

**What it does**

- Interviews (like `/feature-prompt`) for the **TARGET PROJECT-CODE** and a **required design-system source** — a Figma file (via Figma MCP), a written spec/brand guide, reference screens/app, or a guided-definition session that ends in explicit user approval; never fabricates a design system silently
- Reads the target's stack from the Project Matrix / `AGENTS.md` and adapts output — never hardcodes Laravel: framework web → components + a server-rendered preview route (e.g. `/ui/preview/all`); React Native → a component library + a preview screen; plain/static → HTML/CSS components + a static preview file
- Writes **theme/tokens** as named values in the stack's native mechanism (CSS variables, Tailwind config, an RN theme object) — colours, typography, spacing, radii, shadows
- Builds the **UI library** (buttons, inputs, selects, toggles, cards, alerts, badges, form sections, headings, …) from those tokens, faithful to the source
- Renders **one preview page** showing every component in its states (default/hover/focus/disabled/active; empty/loading/error; responsive) — the human verification gate; the library isn't "done" until the user has eyeballed it
- Puts the durable documentation under `<docs-root>/design-system/<PROJECT-CODE>-design-system.md` and adds only a short, PROJECT-CODE-keyed **reference** in `AGENTS.md` — not the whole design system
- Binding rule: on any UI change, check the library first — reuse an existing component; if it's missing, build it via `extend` from the design-system source, or ask the user for a reference when none exists; never inline a one-off. Per-page pixel conformance stays with `/pixel-audit`
- Seeds a project-local `<project>-ui-coding` skill (and **updates** rather than overwrites an existing one) so implementers inherit the reuse-vs-new discipline and paths
- Two modes: **bootstrap** (full first run) and **extend** (the design-system feedback loop — add/modify a component as the design evolves, *or* after a page ships review its diff and promote emergent reusable UI back into the library, leaving one-offs only when documented). `extend` keeps library + preview + doc + `AGENTS.md` reference + project skill in sync and updates the design system **only** — no commits, pushes, ADRs, or handovers (those stay `/grill-with-docs` and `/commit-push-*`). Suggests verifying the preview then starting Workflow B, and stops — never auto-chains

**Modes**

| Mode | Example prompt |
| --- | --- |
| Bootstrap from a source | `Set up the design system for ADMIN-WEB from this Figma file` |
| Guided definition (no source) | `Build a design system for MOBILE-APP — we have no Figma, help me define it` |
| Extend later | `Add the new date-picker component to the ADMIN-WEB design system` |
| Post-ship feedback loop | `That page just shipped — fold its new UI back into the ADMIN-WEB library` |

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
| Single project on a date | `Generate release notes for WAREHOUSE-APP on 11 March` |
| All projects on a date | `Generate release notes for all projects on 15 April` |
| Current dev session | `Summarize today's development session` |
| Specific feature | `Write release notes for the QR scanning improvements` |

**Output location**

Generated files land in `<artifacts-root>/docs/release-notes/`. Release notes
are on-demand date files and do not share the ADR/prompt `NNNN` sequence.
`<artifacts-root>` resolves to the `*.code-workspace` manifest root when a
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

- Maps PROJECT-CODEs to likely repo, app, or package roots
- Searches code, tests, docs, configs, routes, jobs, and feature flags
- Traces definitions to callers and user-facing flows
- Uses code as primary source of truth; highlights duplication risks and likely shared implementation opportunities
- Frames findings through behavior, boundary, evidence, risk, uncertainty, and next action
- Returns the discovery report in chat only; never writes `docs/discovery/` files
- Does not auto-read legacy discovery files; treats them as stale unless the user asks for a specific file
- Optionally uses targeted `opensrc` dependency source pulls when external internals are required and local evidence is insufficient
- Flags code-discovered domain terms that may be missing from or stale in
  `CONTEXT.md`, with short descriptions and evidence for user approval
- Updates `CONTEXT.md` or other artifacts only as an explicit follow-up after
  showing exact target files and proposed changes for user approval
- Uses recent git history only when code scanning is not enough
- Produces a structured report covering summary, behavior, implementation,
  usage sites, rationale, candidate context terms, risks, gaps, and next checks

**Example prompts**

| Mode | Example prompt |
| --- | --- |
| Feature lookup | `Explain how asset lookup works in MOBILE-APP` |
| Issue trace | `Investigate why RFID scans fail in WAREHOUSE-APP` |
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
- Defaults to a thin vertical slice and prompts scope-splitting when the request is too broad
- Keeps scope PR-sized (small, reviewable, mergeable slice)
- Favors code-reference-first context and non-obvious constraints over generic stack restatement
- Promotes reuse-before-rewrite and surfaces seam-reuse uncertainty in `Open questions`
- Distinguishes grillable (low-fidelity) vs ungrillable (high-fidelity/feel) unknowns before drafting `Open questions`
- Routes ungrillable unknowns toward `/handoff` + `/prototype` instead of forcing endless grilling
- When cheap exploration reveals missing or stale domain terms, shows candidate
  `CONTEXT.md` updates with short descriptions for user approval
- Applies approved `CONTEXT.md` updates only as a separate documentation step
- Sends non-trivial or inferred drafts to the user for one correction pass
- Saves the final prompt to `<artifacts-root>/docs/prompts/NNNN-<feature-slug>-prompt.md` (sibling of `docs/adr/`; prompt and ADR filenames both start with `NNNN-<slug>`, and numbering is shared with ADRs only). `<artifacts-root>` is the `*.code-workspace` manifest root when present, otherwise the repo root — artifacts stay out of individual project repos whenever a workspace exists.
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

### `port-feature`

Ports a feature that already exists in a **REFERENCE** implementation into a
**TARGET** stack (e.g. bringing a legacy screen into the new app). It sits at
the **discover → plan** entry: it reads the target's binding context, traces the
reference's real behaviour/workflow/navigation/permissions/states via `/feature-discovery`,
surveys what the target already has, and writes **one** gap map artifact — then
suggests `/grill-with-docs` and stops. It never implements and never auto-chains.

```bash
npx skills install https://github.com/devarfeen/agent-skills-kit --skill port-feature
```

**What it does**

- Interviews (like `/feature-prompt`) for anything missing: the **feature to port**, the **REFERENCE PROJECT-CODE** (behaviour truth), and the **TARGET PROJECT-CODE** (where it lands)
- Carries a fixed source-of-truth framing: the reference is truth for behaviour, workflow, navigation, permissions, data effects, and states; the target's design system is truth for UI — reference-vs-DS conflicts pick the DS and record the deviation
- Never hardcodes stack rules — reads the target's conventions from its `CONTEXT.md`, `docs/adr/`, `AGENTS.md`, and UI-coding skill, so it works for any repo in the matrix (a React Native target differs from a Livewire one); a port-critical rule missing from that context is surfaced as an open question, not guessed
- Reads the target's binding context first, discovers the reference with `/feature-discovery` (narrow, evidence-backed — no bulk repo/`docs/` reads), then surveys the target's current state and reusable DS components (opening the target's `/ui/preview/all` when UI is involved)
- Allows read-only sub-agents only for non-overlapping discovery; the main agent owns synthesis with no duplicate discovery
- Writes one gap map to the configured docs location at `<artifacts-root>/docs/port/<feature-slug>-gapmap.md` — reference behaviour/workflow, target current state, missing/wrong, reusable target code & DS components, tests needed, UI/design gaps & forced deviations, risks, a thin first slice, and evidence-derived open questions
- Suggests `/grill-with-docs` on the gap map (which produces the ADR using the next number in the configured `docs/adr/`) and stops — full PROJECT-CODEs named throughout, conventions never mixed across projects, nothing implemented, no issue fabricated

**Example prompts**

| Mode | Example prompt |
| --- | --- |
| Port with all inputs | `Port stock-transfer approvals from LEGACY-PORTAL to ADMIN-WEB` |
| Port, let it interview | `Help me port the invoice screen into MOBILE-APP` |
| Reference → target framing | `Bring the RFID scan flow from LEGACY-PORTAL over to MOBILE-APP` |

### `commit-push-close`

Ships one iteration of work on a GitHub issue: stage and commit with a
structured message, push to the current branch, then close the linked GitHub
issue with a comment that explains how to test the change.

```bash
npx skills install https://github.com/devarfeen/agent-skills-kit --skill commit-push-close
```

**What it does**

- Resolves the linked GitHub issue from the branch name, recent commits, or conversation context. If none exists, creates one inline only for small ad hoc work; planned work routes back to `/feature-prompt` or `/to-issues`.
- Reads issue labels via `gh issue view --json state,labels,title`; routing state stays in labels, not title prefixes:
  - `ready-for-human` → proceed with human-decision context in the body/comment
  - `ready-for-agent` → proceed autonomously
  - missing/conflicting labels or non-ready state → stop and route through `/triage`
- Inline-created ad hoc issues get one category label (`bug` or `enhancement`) and one ready state label (`ready-for-agent` or `ready-for-human`)
- Writes a structured commit message whose subject mirrors the GitHub issue title as closely as practical, plus an `Issue:` line and optional `Decisions:` / `Files:` / `Notes:` sections
- For ad hoc inline issues, the new GitHub issue title and commit subject must match unless a hard tool limit prevents it
- Enforces zero-attribution output across supported coding-agent paths (Codex CLI, Claude CLI, Antigravity CLI, Cursor CLI, Opencode CLI, and GitHub Copilot CLI): no `Co-authored-by`, `Made-with`, `Generated by`, or AI signature lines
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

- Resolves the linked GitHub issue from the branch name, recent commits, or conversation context. If none exists, creates one inline only for small ad hoc work; planned work routes back to `/feature-prompt` or `/to-issues`.
- Reads issue labels via `gh issue view --json state,labels,title,url`; routing state stays in labels, not title prefixes:
  - `ready-for-human` → proceed with human-decision context in the body/comment
  - `ready-for-agent` → proceed autonomously
  - missing/conflicting labels or non-ready state → stop and route through `/triage`
- Inline-created ad hoc issues get one category label (`bug` or `enhancement`) and one ready state label (`ready-for-agent` or `ready-for-human`)
- If the current branch is the repo default (`main` / `master`), proposes a feature branch (`issue/<num>-<slug>`) and waits for the user to confirm before checking it out
- Writes a structured commit message whose subject mirrors the GitHub issue title as closely as practical, plus an `Issue:` line and optional `Decisions:` / `Files:` / `Notes:` sections
- For ad hoc inline issues, the new GitHub issue title, commit subject, and PR title must match unless a hard tool limit prevents it
- Enforces zero-attribution output across supported coding-agent paths (Codex CLI, Claude CLI, Antigravity CLI, Cursor CLI, Opencode CLI, and GitHub Copilot CLI): no `Co-authored-by`, `Made-with`, `Generated by`, or AI signature lines
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

### `polish-batch`

Batches the UI-polish tail at the **verify** phase, between manual QA and ship.
During QA you log many tiny cosmetic fixes (copy, spacing, alignment, wrong
string) **without** fixing any of them, then dispatch them per PROJECT-CODE in
one bounded pass, then verify — replacing live per-nit steering with
capture → dispatch → verify.

```bash
npx skills install https://github.com/devarfeen/agent-skills-kit --skill polish-batch
```

**What it does**

- Runs three explicit modes — **capture** (default), **dispatch**, and **verify** — and never auto-advances between them
- Capture logs each nit to a punch-list artifact and changes nothing; the only write is a new row (capture ≠ fix)
- Enforces cosmetic scope only: anything touching behaviour, data, or an interface is refused as a nit and routed back to `/to-issues` as a slice, including attempts to reframe a behavioural change as "just a small fix"
- Keeps one punch-list per PRD at `<artifacts-root>/docs/qa/<PRD-ID>-punchlist.md` — a table of `#`, `PROJECT-CODE`, `Where`, `Wrong → Right`, `Shot`, `Status` (`open` → `dispatched` → `verified`/`reopened`)
- Uses agent-browser to screenshot state into `docs/qa/shots/` when available, and falls back to the `Where` text when it is not
- Dispatch runs only on explicit user say-so (never automatically from capture): groups open rows by PROJECT-CODE, orders them trivial → structural, and hands the coding CLI one bounded task per group — fix exactly these items, no refactors or adjacent changes, each fix independent and obviously correct
- Always names the full PROJECT-CODE from the Project Matrix and never mixes one project's conventions into another
- Cross-repo: a feature spanning web + API + mobile keeps all its nits in one punch-list file, but dispatch stays per PROJECT-CODE so no batch mixes conventions
- Verify re-checks affected screens against `Wrong → Right`, marks each row `verified`/`reopened` (reopened rows stay for the next round), then suggests `/review` and `/commit-push-*` and stops

**Modes**

| Mode | Example prompt |
| --- | --- |
| Capture a nit (default) | `Punch-list this for PRD-142: Billing header says "Recieve invoices"` |
| Dispatch the batch | `Dispatch the open polish-batch nits per project` |
| Verify the fixes | `Verify the polish-batch punch list for PRD-142` |

### `integration-contract`

Pulls cross-repo confidence out of your head into a durable **contract** plus a
**smoke gate** — but only when a PRD touches more than one PROJECT-CODE. It runs
after `/to-issues`, alongside the **verify** phase: it maps the producer surface
that changed (usually the API PROJECT-CODE), traces each consumer's call-sites
narrowly (the way `/feature-discovery` does), and writes an agent-browser smoke
checklist that proves the seam holds before you ship or hand to the PM.

```bash
npx skills install https://github.com/devarfeen/agent-skills-kit --skill integration-contract
```

**What it does**

- Acts only on multi-project PRDs: if the PRD touches exactly one PROJECT-CODE it reports `single project — no contract needed` and stops — no overhead where it isn't needed
- Writes one contract per PRD at `<artifacts-root>/docs/integration/<PRD-ID>-contract.md` with three sections: **Producer surface changed**, **Consumers**, and a **Smoke checklist**
- Section 1 lists each endpoint/route/response-shape/interface the producer slice added or changed, one row each (`PROJECT-CODE`, surface, change)
- Section 2 traces each dependent PROJECT-CODE's call-sites narrowly and cites them as `file:symbol`; any changed surface with no located consumer becomes an explicit `RISK` row, never a silent pass
- Section 3 writes 3–6 end-to-end flows phrased for agent-browser (navigate → act → assert a visible outcome), each tagged with the PROJECT-CODEs it crosses, `Status: pending → pass/fail`
- Retrieval stays narrow and evidence-backed (no bulk-reading a consumer repo or `docs/`); binding order is `CONTEXT.md` + `docs/adr/` > current PRD/issues/code > native memory
- Always names full PROJECT-CODEs from the Project Matrix and never mixes one project's conventions into another (API vs Livewire web vs CodeIgniter legacy vs React Native)
- **gate** mode runs the smoke checklist via agent-browser at two points — before `/commit-push-*` and before PM handoff — marking each flow `pass`/`fail`; any `fail` reopens the contract and blocks the step, surfaced rather than shipped
- Companion, not a pipeline: suggests `/review` → `/commit-push-*` (all pass) or `/to-issues` / `/diagnosing-bugs` (on a fail), and never auto-chains

**Modes**

| Mode | Example prompt |
| --- | --- |
| Build the contract (default) | `Build the integration contract for PRD-142` |
| Single-project check | `integration-contract for PRD-207` *(one project → "no contract needed", stops)* |
| Gate before shipping | `Run the integration-contract smoke gate for PRD-142` |

### `pixel-audit`

A standalone **verify**-phase companion: a strict per-page visual-conformance
audit of **one** page/route against a source of truth. It captures a full-size
pixel inventory, writes a defect list (MISSING vs EXTRA), fixes node-by-node
reusing the project's UI library, and refuses to claim "verified" until a hard
element-level gate is crossed. It stays strictly inside scope and never
auto-chains.

```bash
npx skills install https://github.com/devarfeen/agent-skills-kit --skill pixel-audit
```

**What it does**

- Interviews for the **TARGET PROJECT-CODE**, the **SCOPE** (one page/route + the states to audit — list/detail, modals, forms, empty/error/loading, responsive), and a **pluggable source of truth**: Figma MCP node(s), or reference screens / a reference implementation when no Figma exists — and names which is in use
- Loads the project's binding context (`CONTEXT.md`, `docs/adr/`) and its `*-ui-coding` skill first — reusing that skill's catalog, tokens, and components; never inlining. Falls back to `/design-system` discovery if no such skill exists
- Captures a written **pixel inventory** before editing — per node/region and every empty/error/loading/responsive variant, full-size including below-fold (never whole-frame screenshots only): exact x/y, size, spacing, padding, gap, font, colour, border, radius, fill, icon size, alignment, opacity, shadow, variant
- Audits expected (source) vs actual (browser), classifying each mismatch **MISSING** (source item absent/wrong in app) or **EXTRA** (app item not in source); extra UI is a defect, surfaced for a decision, never silently kept/removed/restyled
- Writes the defect list to `<artifacts-root>/docs/pixel-audit/<page-slug>-defects.md`, one row per defect (node, URL/state, file/component, mismatch, expected, actual, MISSING/EXTRA, element evidence)
- Fixes one node/state at a time, reusing the UI library; a shared-component change goes through the library + preview + `*-ui-coding` skill (via `/design-system` extend), never page-local; touches nothing unrelated
- Enforces a hard **verification gate**: state the env; rebuild/refresh and confirm the change is in the **served** assets; prove each fix with `getBoundingClientRect()`, computed styles, DOM, and clipped element screenshots; hidden/zero-size/collapsed/clipped/misaligned/ignored-class elements are failures; falsify before declaring verified — never say "verified" without env stated, pipeline crossed, served assets confirmed, element proof, source captured full-size, expected-vs-actual compared, and every in-scope state checked
- Per-page feature-time conformance — distinct from `/design-system`'s one-time startup preview verification (referenced, not duplicated). Suggests `/review` → `/commit-push-*` and stops

**Modes**

| Mode | Example prompt |
| --- | --- |
| Audit against Figma | `Pixel-audit the assets list page in ADMIN-WEB against this Figma node` |
| Audit against a reference | `Pixel-audit MOBILE-APP order detail against the legacy screens — no Figma` |
| Scoped states | `Pixel-audit the ADMIN-WEB user form: default, validation error, and empty states only` |

### `orchestrate-herdr`

Re-runnable orchestrator prompt for [herdr](https://herdr.dev), a terminal-native
agent multiplexer. Reads a PRD/parent-issue URL, finds its open sub-issues, and
launches one herdr-managed worker tab per issue running a chosen coding CLI, then
monitors every tab for test-backed completion. Runs only inside herdr
(`HERDR_ENV=1`).

```bash
npx skills install https://github.com/devarfeen/agent-skills-kit --skill orchestrate-herdr
```

**What it does**

- Wraps a tested, working orchestrator prompt that is executed **verbatim** —
  the only things that change between runs are the **PRD URL** and the
  **coding CLI** to launch
- Gathers those two inputs from skill args, otherwise asks the user; never guesses
- Keeps the main tab as a pure orchestrator: no implementation, no panes, no
  nested sub-agents or nested coding sessions, and never `cd`s out of the
  orchestrator folder
- Creates one Herdr-managed worker tab per open issue inside the saved
  workspace/session, named `[CODING_CLI] - GH #[ISSUE_NUMBER]`, and tracks each
  by its saved tab ID (never by active/latest/visual order)
- Sends each worker only its assigned issue prompt (never the full PRD), waiting
  for CLI readiness and confirming the first response before counting it launched
- Monitors all saved tabs on a 1-minute cadence and refuses to accept completion
  without test evidence
- Routes via issue order, dependency notes, comments, and `ready-for-agent` /
  `ready-for-human` labels — never by mutating issue titles

**Local-only fit**

This is herdr's native expression of the kit's local-orchestration policy: many
local coding-CLI workers in sibling tabs, coordinated from one orchestrator tab,
with no cloud or remote background agents.

**Example prompts**

| Mode | Example prompt |
| --- | --- |
| Fan a PRD out to workers | `orchestrate-herdr for https://github.com/org/repo/issues/102 using codex` |
| Re-run with a different CLI | `Re-run the herdr orchestrator on that PRD with claude` |
| Inside herdr, no args | `/orchestrate-herdr` *(prompts for PRD URL and coding CLI)* |

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

The main session acts as an **orchestrator**: it splits work into role-typed
lanes (Explorer, Researcher, Planner, Implementer, Reviewer, Tester,
Tool-runner), dispatches each to a **local** subagent, runs independent lanes
in parallel, and pushes long or noisy lanes to local background/async — so the
main chat stays responsive and its context stays clean. Subagents return
summaries; the main session keeps the only merge and final-judgment seat.

**Local only — no cloud agents.** These skills never delegate to cloud or
remote background-agent products (Cursor Cloud Agents, GitHub Copilot cloud
coding agent, Codex Cloud, Antigravity managed/remote execution). Local
worktree-isolated parallel agents are fine; remote ones are not.

| Runtime | Parallel dispatch | Local background |
| --- | --- | --- |
| Codex CLI | `spawn_agent` / `spawn_agents_on_csv` (default 6 threads) | local worktrees; Automations are app-side, not CLI |
| Claude CLI | Multiple `Agent` calls in one turn | `run_in_background` Bash; `background:` subagents; `isolation: worktree` |
| Antigravity CLI | `start_subagent` dynamic subagents (Agent Manager) | `/schedule` local background |
| Cursor CLI | Multiple `Task` calls (cap ~4); local worktree agents | `is_background` subagent + `Await` |
| Opencode CLI | multiple `task` calls (`subagent_type`) | `task(background=true)` + `task_status` |
| GitHub Copilot CLI | `/fleet` (parallel subagents) | `Ctrl+X → b` background shell |

Highest elevated permission presets are documented in the same runtime
references and should be used only when explicitly requested:

| Runtime | Highest elevated launch / preset |
| --- | --- |
| Codex CLI | `codex --dangerously-bypass-approvals-and-sandbox` or `codex --sandbox danger-full-access --ask-for-approval never` |
| Claude CLI | `claude --dangerously-skip-permissions` / `--permission-mode bypassPermissions` |
| Antigravity CLI | `agy --dangerously-skip-permissions` without `--sandbox` |
| Cursor CLI | `agent --yolo --sandbox=disabled --approve-mcps` |
| Opencode CLI | `opencode run --dangerously-skip-permissions`; persistent agents use `permission` keys set to `allow` |
| GitHub Copilot CLI | `copilot --allow-all` / `--yolo` |

The main agent still owns final judgment and output quality. Subagents collect
facts and run lanes; they do not replace the final synthesis.

Runtime-specific tool-calling docs for `agents-md` live under
`skills/agents-md/references/` — start with [`tool-calling.md`](skills/agents-md/references/tool-calling.md)
(agent orchestration model, canonical role lanes, local-only policy, CLI
tool names, permissions), then `cursor-tools.md`, `claude-tools.md`,
`codex-tools.md`, `copilot-tools.md`, `antigravity-tools.md`,
and `opencode-tools.md`.

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

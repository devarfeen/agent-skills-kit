# Agent Skills Kit

Zero attribution: never add or leave co-author, AI, or tool attribution in commits, PRs, issues, docs, settings, or comments.

A collection of reusable **skills** for six supported AI coding CLIs:
Codex CLI, Claude CLI, Antigravity CLI, Cursor CLI, Opencode CLI, and
GitHub Copilot CLI. No other agent runtime is supported by this kit.

A *skill* is a small, self-contained bundle of instructions, examples, and
templates that teaches an agent how to do one specific job well — for example,
"write PM-friendly release notes from git history". Install a skill into your
agent's workflow and the agent picks it up — automatically or via
`/skill-name` — when a matching request comes in.

Each folder under `skills/` follows the
[Agent Skills spec](https://agentskills.io/specification): a `SKILL.md` with
`name` + `description` frontmatter (the description is what triggers the skill)
plus optional `references/` (docs loaded on demand) and `assets/` (output
templates). Every skill installs standalone.

## Repository Layout

```
agent-skills-kit/
├── README.md            # This file — front door + skill index
├── GUIDE.md             # Day-to-day workflow guide (human-facing)
├── BEST-PRACTICES.md    # Mental model and anti-patterns (human-facing)
├── CONTRIBUTING.md      # Skill authoring guide, review rubric, sync map
├── AGENTS.md            # Conventions for agents working in this repo
│                        # (CLAUDE.md / GEMINI.md are redirect shims)
├── .claude-plugin/
│   └── marketplace.json # Plugin groups (manual-workflow, factory-workflow)
├── .github/workflows/   # CI: runs tools/validate.sh on every PR
├── tools/
│   ├── validate.sh      # Repo invariant checks — run before every commit
│   └── trigger-evals/   # Maintainer trigger-eval harness (score.py, query sets)
├── evals/               # Kit-level eval method, rubrics, audit templates
├── audits/              # Dated audit reports and findings
└── skills/<name>/       # One folder per skill
    ├── SKILL.md         # Required: frontmatter + instructions
    ├── references/      # Optional: on-demand docs
    ├── assets/          # Optional: output templates
    ├── agents/          # Optional: per-runtime invocation policy (openai.yaml)
    └── evals/           # Trigger-eval set + rubric scorecards (never loaded into context)
```

## Installing a Skill

```bash
npx skills add devarfeen/agent-skills-kit -s <skill-name> -g -y
```

Omit `-g` to install into the current project instead of user-global
(`~/.agents/skills/`). Do not pass a long `--agent` list; that creates empty
`~/.<tool>` homes. **PromptScript** does not support `npx skills -g`; use
[`prs skills add`](https://getpromptscript.dev/latest/reference/cli/) or project
scope (no `-g`). **Antigravity** reads
`~/.gemini/antigravity-cli/skills/` (and `~/.gemini/antigravity/skills/`); global
`-g` still lands in `~/.agents/skills/` — symlink or copy into those paths if
Antigravity does not pick them up.

Update an installed skill:

```bash
npx skills update <skill-name>
```

Line-by-line global installs are under [Available Skills](#available-skills),
[grouped by GitHub source](#global-install-commands). Companions mirror
[Credits And Provenance](#credits-and-provenance);
Graphify is installed separately. The `skills` CLI has no version or ref option,
so companions install from each source's default branch (unpinned).

The `skills` CLI fetches the named subfolder from this repo and installs it
into your agent's local skills directory. After install, invoke a skill with
`/skill-name` — most kit skills mark themselves for explicit invocation
(`disable-model-invocation: true`), so the slash command is the reliable path;
`feature-discovery`, `tdd-loop`, and `using-git-worktrees` also trigger
automatically when a request matches their description.

Skills avoid changing your git state unless their own instructions say
otherwise. Skills that inspect history (`release-notes`, `feature-discovery`)
only read commits already on your machine — never `git fetch` / `git pull`.
`ci-loop` is the one exception: it runs `git fetch` before each attempt to
confirm the PR head hasn't moved under it.

## Available Skills

Skills sit on a workflow gradient — discover → sharpen → plan → slice →
implement → verify → ship — plus two startup skills that run once per
workspace/project and an on-demand worktree companion. Full behavior, modes,
and rules live in each skill's `SKILL.md`; this table is the index. Global
install commands are [grouped by source](#global-install-commands) below the table.

| Skill | Phase | What it does | Example prompt |
| :--- | :--- | :--- | :--- |
| [`agents-md`](skills/agents-md/SKILL.md) | startup | Generates the workspace-root `AGENTS.md` (Project Matrix, 18 non-negotiable rules, skills gradient, context policy) plus a `CLAUDE.md` redirect shim, from a `.code-workspace` file (marker `v46`). Reports competing per-runtime instruction files without touching them, and suggests an optional env-guard hook template when production or staging hosts are named | `Generate AGENTS.md for this workspace` |
| [`design-system`](skills/design-system/SKILL.md) | startup | Turns a design source into tokens + a UI library + a verifiable preview + a binding AGENTS.md rule. Source order: one you name, else a root `DESIGN.md`, else a project UI/brand/component-library skill, else Figma, spec, reference screens, or a guided session. Checks WCAG AA contrast, loaded fonts, and light/dark modes; re-run `extend` as the design grows | `Set up the design system for ADMIN-WEB from this Figma file` |
| [`feature-discovery`](skills/feature-discovery/SKILL.md) | discover | Read-only, evidence-backed trace of how a feature, module, or behavior works, with current code as the source of truth — then Graphify as a cross-check, then ADRs, each with its own report section. Git history is read only if you accept the report's offer | `Trace the invite-user workflow across ADMIN-WEB and API-SERVICE` |
| [`port-feature`](skills/port-feature/SKILL.md) | discover | Maps a feature from a REFERENCE implementation into a TARGET stack as one gap map — including validation, bulk actions, role gates, and reference behaviour no test covers — then hands to planning | `Port stock-transfer approvals from LEGACY-PORTAL to ADMIN-WEB` |
| [`feature-prompt`](skills/feature-prompt/SKILL.md) | sharpen | Turns a rough idea into a small, PR-sized prompt file for `grill-with-docs`, showing inferred facts separately from what you stated | `Help me create a feature prompt for stock transfer approvals` |
| [`tdd-loop`](skills/tdd-loop/SKILL.md) | implement | Enforceable test-first loop — one failing test, watch it fail right, smallest change to green, widen, refactor on green — plus an exception protocol for spikes, legacy code, hotfixes, and infra work. Called by `/implement` at each seam when that's installed; stands alone when it isn't | `Fix this bug test-first` |
| [`orchestrate-herdr`](skills/orchestrate-herdr/SKILL.md) | implement | Inside [herdr](https://herdr.dev) only: fans a spec's (PRD's) open sub-issues out to one local coding-CLI worker tab each and monitors for test-backed completion; holds back sub-issues blocked by another open one and flags shared ports, databases, and merge-risk files | `orchestrate-herdr for <spec URL> using codex` |
| [`pixel-audit`](skills/pixel-audit/SKILL.md) | verify | Strict per-page visual-conformance audit against Figma or reference screens, with an element-level verification gate on served assets, a final re-check of every verified row, and no new console errors | `Pixel-audit the assets list page in ADMIN-WEB against this Figma node` |
| [`polish-batch`](skills/polish-batch/SKILL.md) | verify | Captures cosmetic QA nits without fixing them, dispatches them per PROJECT-CODE in one bounded pass, then verifies; copy fixed in a shared string or translation key waits for your confirmation | `Punch-list this for SPEC-142: Billing header says "Recieve invoices"` |
| [`integration-contract`](skills/integration-contract/SKILL.md) | verify | For multi-project specs (PRDs) only: writes a producer/consumer contract — each change labelled compatible, rollout-dependent, or breaking — plus a smoke gate (agent-browser / curl / manual) that must pass before the spec ships | `Build the integration contract for SPEC-142` |
| [`agentic-qa`](skills/agentic-qa/SKILL.md) | verify | Agent-run functional QA before a human sees the work: drives every acceptance criterion across states, viewports, and roles, fails on console errors and failed requests, replays a failure once before reporting it, checks writes survive a reload and controls work by keyboard, and records VERIFIED/PARTIAL/BLOCKED on the PR — never edits code | `QA PR 87 like a tester would` |
| [`qa-escape`](skills/qa-escape/SKILL.md) | verify | Turns a bug human QA found after an agent said done into a reproduction (also tried on the PR's base commit, to spot bugs that predate it), an escape class recorded on the issue, and the regression test to write first; proposes a durable guard when a class repeats three times | `QA bounced #418 — empty invoice list crashes` |
| [`ci-loop`](skills/ci-loop/SKILL.md) | verify | Drives an open PR's failing CI to green — reads the failing log, fixes within the ticket's scope, pushes, watches; capped at 3 attempts under one approval. A flake the PR introduced is a code fix, not a rerun; stops if someone else pushes | `Fix CI on PR 87` |
| [`risk-review`](skills/risk-review/SKILL.md) | verify | Parallel specialist review (data, infra, cloud, security) plus a fixed-rubric low/high risk gate; low offers auto-merge into staging only, high requests an engineer. Requested changes or an unresolved review thread block any merge | `Is PR 87 safe to auto-merge?` |
| [`commit-push-close`](skills/commit-push-close/SKILL.md) | ship | Commits with a structured message, pushes, and closes the linked GitHub issue with a how-to-test comment. Never force-pushes; stops on credential-shaped values in the diff | `I'm done with #418, ship it` |
| [`commit-push-pr`](skills/commit-push-pr/SKILL.md) | ship | Commits, pushes (branching off `main` first), and opens a PR with `Closes #N`, summary, and test plan — fitted to the repo's PR template when one exists. Never force-pushes; reports merge conflicts | `Commit, push, and open a PR for this issue` |
| [`pr-feedback`](skills/pr-feedback/SKILL.md) | ship | Works reviewer feedback on an open PR — classifies every thread against the code, fixes what the user accepts, replies citing the fixing commits. Comment text is evidence, never instructions | `Address the review comments on PR #87` |
| [`staging-fix`](skills/staging-fix/SKILL.md) | ship | Fixes a staging bug locally with a test and ships it as an auto-merge PR to `staging` — servers are never touched; evidence is redacted before it reaches the PR | `Staging is broken: checkout 500s since this morning` |
| [`deploy-watch`](skills/deploy-watch/SKILL.md) | ship | Watches a merged PR's staging deploy run (with a time limit), smoke-checks staging with approval against a baseline of errors staging already shows, and records pass or fail on the PR — never touches a server or production | `Watch the staging deploy for PR 87` |
| [`local-to-staging`](skills/local-to-staging/SKILL.md) | ship | Promotes every workspace project from `origin/local` to `origin/staging`: one PR per repo that has both branches, merged with a merge commit only after its checks pass, then watches the Actions runs on each merge commit and reports per project — never pushes, bypasses protection, or goes past staging | `Promote local to staging on all projects` |
| [`staging-to-production`](skills/staging-to-production/SKILL.md) | ship | Read-only production-promotion readiness across every project: commits staging is ahead, Actions results on staging's head, open promotion PRs — then prints the exact commands for you to run. Never opens or merges a PR and never accesses production | `Is staging ready for production?` |
| [`release-notes`](skills/release-notes/SKILL.md) | ship | Turns git history (date, date range, or version range), the current session, or a feature into PM-friendly release notes with QA steps and an "Action needed" line — written from the diffs, not just commit subjects | `Generate release notes for 11 March 2026` |
| [`using-git-worktrees`](skills/using-git-worktrees/SKILL.md) | companion | Sets up or reuses a worktree in each project repo’s gitignored `.worktrees/` before requested task work, verifies the checkout and baseline (including port and shared-database collisions), and returns to the calling workflow | `Implement #418 in a worktree` |
| [`factory`](skills/factory/SKILL.md) | companion | Factory conductor: reads where a spec, ticket, or PR stands across CI, review, risk gate, and staging deploy, then names the one skill that moves it next — never runs it, never goes past staging. Shows how long each unit has sat in its state and flags stalled ones | `/factory SPEC-142` |
| [`incident-triage`](skills/incident-triage/SKILL.md) | companion | Read-only incident triage: timeline, ranked causes with evidence (always including one that isn't a recent change), owner-run mitigations, one redacted incident note with a Resolution section — production never accessed; a suspected breach goes straight to the owner | `We have an incident: checkout 502s since 14:00` |
| [`writing-kit-skills`](skills/writing-kit-skills/SKILL.md) | — | Kit-internal house style for authoring and editing this repo's skills: skeleton, word budget, the eight canonical one-liners, output caps, eval gates, and matching each rule's form to the failure it fixes | `Rewrite this SKILL.md to house style` |

### Global install commands

Grouped by author or org. Omit `-g` for project scope. Do not use `--all` or a
long `--agent` list (empty `~/.<tool>` homes). To install **every** skill in a
repo without naming them: `-s '*'`.

#### [devarfeen/agent-skills-kit](https://github.com/devarfeen/agent-skills-kit) (this repo)

```bash
npx skills add devarfeen/agent-skills-kit -g -y -s '*'
```

### Companion install commands (global)

Credited third-party skills, grouped by source repo.

#### [anthropics/skills](https://github.com/anthropics/skills)

```bash
npx skills add anthropics/skills -g -y -s mcp-builder skill-creator frontend-design
```

#### [mattpocock/skills](https://github.com/mattpocock/skills)

```bash
npx skills add mattpocock/skills -g -y -s '*'
```

#### Vercel Labs

[`agent-browser`](https://github.com/vercel-labs/agent-browser) and
[`find-skills`](https://github.com/vercel-labs/skills) live in two repos; install
both:

```bash
npx skills add vercel-labs/agent-browser -g -y -s agent-browser
npx skills add vercel-labs/skills -g -y -s find-skills
```

#### [cursor/plugins](https://github.com/cursor/plugins)

```bash
npx skills add cursor/plugins -g -y -s blast-radius show-me-your-work unslop
```

#### [github/awesome-copilot](https://github.com/github/awesome-copilot)

```bash
npx skills add github/awesome-copilot -s boost-prompt -g -y
```

#### [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills)

```bash
npx skills add google-labs-code/stitch-skills -s enhance-prompt -g -y
```

#### [herdrdev/herdr](https://github.com/herdrdev/herdr)

```bash
npx skills add herdrdev/herdr -s herdr -g -y
```

#### [pbakaus/impeccable](https://github.com/pbakaus/impeccable)

```bash
npx skills add pbakaus/impeccable -s impeccable -g -y
```

#### [sickn33/agentic-awesome-skills](https://github.com/sickn33/agentic-awesome-skills)

```bash
npx skills add sickn33/agentic-awesome-skills -s docker-expert -g -y
```

### Working in a worktree

Install the companion with:

```bash
npx skills add devarfeen/agent-skills-kit -s using-git-worktrees -g -y
```

Then ask: **“Fix checkout in SHOP in a worktree.”** You can also invoke
`/using-git-worktrees` directly for setup only. The companion creates or reuses
`<shop-repo>/.worktrees/<task-name>`, adds `/.worktrees/` to the repo's `.gitignore`,
and checks the checkout before returning to the requested task. Each affected
project gets its own worktree. A request for a branch alone does not trigger it.

The model can invoke this skill automatically. Before task writes, it reports
the verified checkout, branch, starting commit, and baseline. Commands and edit
paths stay bound to that checkout; handoffs and restarts require a fresh check.
This is an instruction gate, not a harness-level write blocker.

Use `/commit-push-pr` to ship the worktree branch for review. It commits,
pushes, and opens a PR; merging is a later step. `/commit-push-close` closes
the issue directly after pushing and does **not** merge the branch. Keep the
worktree until its work is integrated and verified, then request cleanup.

For existing generated workspaces, re-run `/agents-md` and review its proposed
update to add worktree routing, including the interlocks with Matt's skills.
See the [worktree walkthrough](GUIDE.md#working-in-a-worktree) for setup,
shipping, and cleanup examples.

**Cursor CLI:** Install with `npx skills add` (skills land in
`~/.cursor/skills/` or `.cursor/skills/`). Invoke a skill with `/skill-name`
(for example `/release-notes`). Run the CLI with `agent` for interactive
sessions or `agent -p "..."` for scripts and CI.

The gradient's plan/slice/implement/verify core (`/grill-with-docs`,
`/wayfinder`, `/to-spec`, `/to-tickets`, `/implement`, `/tdd`, `/code-review`,
`/diagnosing-bugs`, `/triage`) comes from
[Matt Pocock's skills](https://github.com/mattpocock/skills) — separate
installs this kit is designed to interlock with. Run
`/setup-matt-pocock-skills` once per workspace (see the First-Time Setup
sequence in [GUIDE.md](GUIDE.md)) before using them.

These interlocks use optional upstream skills alongside the kit:

- **Worktrees** are request-driven. Ask to do work in a worktree and
  `/using-git-worktrees` runs before the task skill, using that project repo’s
  `.worktrees/<task-name>` and adding `/.worktrees/` to its `.gitignore`.
  Generated `AGENTS.md` routes Matt’s implementation, debugging, prototype, and review skills through
  that setup and passes them the verified checkout. Third-party installations
  stay untouched.
- **Implementing** stacks three layers. `/implement` is an optional *ticket
  driver*; the kit's `tdd-loop` is the test-first *procedure* it calls at each
  seam (gates, completion evidence, exception protocol); Matt's `/tdd` is the
  *test-quality reference*. Install none of the upstream ones and `tdd-loop`
  still stands alone. `/implement` stops after `/code-review` — the kit's ship
  skills own every commit.
- **Planning** forks on fog. If you can state the destination and every open
  decision sharply, `/feature-prompt` → `/grill-with-docs`. If decisions gate
  the scope, `/wayfinder` charts them as tracker tickets and resolves them one
  per session. Both arms rejoin at `/to-spec`.

## Workflow Guide

See [GUIDE.md](GUIDE.md) for the recommended workflow from workspace setup
through spec, issues, TDD implementation, verification, PR shipping, and
release notes — including the issue-title/label hard gate, workflow gates, and
recovery loops. See [BEST-PRACTICES.md](BEST-PRACTICES.md) for the mental
model: the gradient, context discipline, and anti-patterns.

The kit ships `using-git-worktrees` as a companion. External companion skills
and MCPs (Graphify, agent-browser, Figma MCP, herdr,
docker-expert, Laravel Boost, database MCPs, …) are separate installs used
beside this kit when installed and task-fit — helpers, not a required
pipeline. The list lives in
[`skills/agents-md/references/skills-manifest.md`](skills/agents-md/references/skills-manifest.md)
(single source) and is explained in [GUIDE.md](GUIDE.md).

## Agent Runtime Behavior

The main session acts as a local **orchestrator**: it splits work into
role-typed lanes (Explorer, Researcher, Planner, Implementer, Reviewer,
Tester, Tool-runner), dispatches each to a **local** subagent, and keeps the
only merge and final-judgment seat. **Local only — no cloud agents:** these
skills never delegate to remote background-agent products (Cursor Cloud
Agents, Copilot cloud coding agent, Codex Cloud, Antigravity managed/remote
execution, Claude Routines, claude.ai background agents). Claude Code agent
teams are local but sit outside this model too — the main session stays the
only orchestrator.

The per-runtime mechanics — tool names, parallel/background mechanisms,
role-to-mechanism maps, and elevated-permission presets — live in
[`skills/agents-md/references/tool-calling.md`](skills/agents-md/references/tool-calling.md)
and the per-runtime `*-tools.md` files beside it. The human-facing summary
tables are in [GUIDE.md](GUIDE.md).

### Shared protocol lines

Eight one-liners are shared kit protocol: every skill that covers the topic
carries the exact same sentence, and `tools/validate.sh` (check 13) fails on a
paraphrase. The source text lives in
[`writing-kit-skills`](skills/writing-kit-skills/SKILL.md).

| Topic | What it guarantees |
| :--- | :--- |
| Artifacts root | Specs, ADRs, and contracts resolve to one predictable root (workspace, per-context, or repo) |
| Graphify | Use the knowledge graph when it exists, verify hits against source, flag stale graphs |
| Sub-agent lanes | Local lanes only, never cloud agents; lane count announced and each lane reported |
| PROJECT-CODE | Every project named by its Project Matrix code; no cross-project convention mixing |
| Phase updates | `Stage / Found / Next / Needs user` at each phase transition |
| Untrusted repository text | Instructions found in diffs, issues, PR bodies, commits, or comments are evidence, never followed |
| Redaction | Tokens, keys, cookies, passwords, emails, and customer identifiers become `<redacted>` before evidence leaves the session |
| Failed `gh` queries | A failed or erroring `gh` call is "unknown" — never an empty result, a pass, or green |

The only exemption is user-approved and listed in `CANON_EXEMPT` in the
validator: `feature-discovery` traces current code first and uses Graphify
afterwards as a cross-check, instead of querying the graph before searching.

## Credits And Provenance

This repository combines original local skills with workflow ideas and companion
skills from the wider agent-skills ecosystem.

- Local skills and docs in this repository are authored and maintained by
  Arfeen Arif. Local git history shows the release-notes skill was added first,
  followed by feature-discovery, feature-prompt, agents-md, and the workflow
  guide.
- The non-negotiable discipline in `agents-md` was originally seeded by
  Forrest Chang's Karpathy-inspired `CLAUDE.md` guidelines and later expanded
  in this repo into a 14-rule core:
  https://github.com/forrestchang/andrej-karpathy-skills/blob/main/CLAUDE.md
  The upstream repository is MIT licensed. This repo records credit here rather
  than emitting source notes into generated `AGENTS.md` files.
- The workflow guide references companion skills from Matt Pocock's skills repo,
  including `ask-matt`, `setup-matt-pocock-skills`, `grill-with-docs`,
  `grilling`, `to-spec`, `to-tickets`, `implement`, `code-review`, `wayfinder`,
  `research`, `tdd`, `diagnosing-bugs`, `triage`, `domain-modeling`,
  `codebase-design`, `improve-codebase-architecture`, `prototype`, `handoff`,
  `wait-what`, `wizard`, and `to-questionnaire`:
  https://github.com/mattpocock/skills
- The worktree companion follows the setup approach in
  [using-git-worktrees](https://github.com/obra/superpowers/blob/main/skills/using-git-worktrees/SKILL.md).
  Its local rules preserve requested isolation on failure, leave commits to the
  ship skills, and return the verified checkout to the authorized task.
- `/skill-creator` is credited to Anthropic's public skills repository:
  https://github.com/anthropics/skills/tree/main/skills/skill-creator
- `/agent-browser`, the `skills` CLI, `find-skills`, and Vercel React/React
  Native best-practice skills are credited to Vercel Labs:
  https://github.com/vercel-labs/agent-browser
  https://github.com/vercel-labs/skills
  https://github.com/vercel-labs/agent-skills
- Other optional companions referenced by `agents-md`: Matt Pocock's
  `ask-matt` router (https://github.com/mattpocock/skills), Graphify
  (https://github.com/Graphify-Labs/graphify), Codex plugin for Claude Code
  (https://github.com/openai/codex-plugin-cc), Impeccable
  (https://github.com/pbakaus/impeccable), notebooklm-py
  (https://github.com/teng-lin/notebooklm-py), herdr
  (https://github.com/herdrdev/herdr), docker-expert from
  agentic-awesome-skills (https://github.com/sickn33/agentic-awesome-skills, formerly antigravity-awesome-skills),
  Laravel Boost (https://github.com/laravel/boost), unslop, blast-radius, and
  show-me-your-work from Cursor's plugins repo
  (https://github.com/cursor/plugins), and Figma MCP
  (https://developers.figma.com/docs/figma-mcp-server/).
- **Globally installed skills.** The skills below were installed globally
  (`npx skills list -g`, 2026-10-03) beside this kit's own skills. They are
  separate installs, credited by source and never vendored here:
  - Anthropic (https://github.com/anthropics/skills): `mcp-builder`,
    `skill-creator`, `frontend-design`.
  - Matt Pocock (https://github.com/mattpocock/skills): `ask-matt`,
    `claude-handoff`, `code-review`, `codebase-design`, `diagnosing-bugs`,
    `domain-modeling`, `git-guardrails-claude-code`, `grill-me`,
    `grill-with-docs`, `grilling`, `handoff`, `implement`, `implement-spec`,
    `improve-codebase-architecture`, `loop-me`, `migrate-to-shoehorn`, `pr`,
    `prototype`, `research`, `retro`, `scaffold-exercises`,
    `setup-matt-pocock-skills`, `setup-pre-commit`, `setup-ts-deep-modules`,
    `tdd`, `teach`, `to-questionnaire`, `to-spec`, `to-tickets`, `triage`,
    `wait-what`, `wayfinder`, `wizard`, `writing-beats`, `writing-for-agents`,
    `writing-fragments`, `writing-shape`.
  - Vercel Labs: `agent-browser` (https://github.com/vercel-labs/agent-browser)
    and `find-skills` (https://github.com/vercel-labs/skills).
  - Cursor (https://github.com/cursor/plugins): `blast-radius`,
    `show-me-your-work`, `unslop`.
  - GitHub awesome-copilot (https://github.com/github/awesome-copilot):
    `boost-prompt`.
  - Google Labs Stitch skills (https://github.com/google-labs-code/stitch-skills):
    `enhance-prompt`.
  - herdr (https://github.com/herdrdev/herdr): `herdr`.
  - Impeccable (https://github.com/pbakaus/impeccable): `impeccable`.
  - agentic-awesome-skills (https://github.com/sickn33/agentic-awesome-skills):
    `docker-expert`.
  - Graphify (https://github.com/Graphify-Labs/graphify): `graphify`, installed
    from a local copy rather than through the `skills` CLI.
- The QA-escape loop (`agentic-qa`, `qa-escape`, and the acceptance-matrix,
  evidence, and risk-lens changes to existing skills) adapts ideas from skills
  in GitHub's awesome-copilot collection
  (https://github.com/github/awesome-copilot/tree/main/skills — notably
  webmcpify, bug-receipt, bug-reproduction-brief, quality-playbook,
  test-gap-audit, mcp-release-qa, api-breaking-change-detector,
  protobuf-grpc-api-review, copilot-pr-autopilot, incident-postmortem, and
  poka-yoke) and from Chris Titus's titus-ai skills
  (https://github.com/ChrisTitusTech/titus-ai/tree/main/.agents/skills —
  pr-readiness and ai-project-manager). The factory workflow's shape follows
  The Pragmatic Engineer's diagram of OpenAI's "agentic software factory". No
  text was copied; credit lives here, never in generated output.
- The 2026-10 hardening pass (replay-before-fail, base-commit reproduction,
  ship-policy safety, review-comment trust, deploy baselines, redaction, the
  dependency gate in `orchestrate-herdr`, design-system contrast checks, the
  env-guard hook template, and the house-style "form follows the failure"
  rule) compared every kit skill against five public skill collections and
  adapted patterns in this kit's own words:
  [github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills),
  [obra/superpowers](https://github.com/obra/superpowers/tree/main/skills),
  [ChrisTitusTech/titus-ai](https://github.com/ChrisTitusTech/titus-ai/tree/main/.agents/skills),
  [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills),
  and [garrytan/gstack](https://github.com/garrytan/gstack). Nothing from them
  is vendored or installed by this kit.
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

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the skill authoring guide (token
budget, description-as-trigger, kit contract), the review rubric, and the
maintenance sync map. Before any commit, run:

```bash
bash tools/validate.sh
```

CI runs the same script on every PR. It checks, in short: frontmatter and
naming; byte-identical shared files (`ship-policy.md`, `context-terms.md`);
manifest, README, and plugin-group coverage for every skill; link and anchor
integrity; zero attribution in files and commit messages; agents-md version
marker agreement; trigger-eval sets and their provenance; invocation parity
with `agents/openai.yaml`; the 1,500-word body ceiling; the canonical
one-liners; no placeholder scaffolding; version bumps on every changed skill;
no hidden zero-width or bidi characters; every installed companion credited
here; and a 3,000-character total budget for model-invocable descriptions.

## License

[MIT](LICENSE) © Arfeen Arif

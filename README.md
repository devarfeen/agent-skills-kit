# Agent Skills Kit

A collection of reusable **skills** for six supported AI coding CLIs:
Codex CLI, Claude CLI, Antigravity CLI, Cursor CLI, Opencode CLI, and
GitHub Copilot CLI. No other agent runtime is supported by this kit.

A *skill* is a small, self-contained bundle of instructions, examples, and
templates that teaches an agent how to do one specific job well — for example,
"write PM-friendly release notes from git history". Install a skill into your
agent's workflow and the agent picks it up automatically when a matching
request comes in.

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
├── tools/validate.sh    # Repo invariant checks — run before every commit
└── skills/<name>/       # One folder per skill
    ├── SKILL.md         # Required: frontmatter + instructions
    ├── references/      # Optional: on-demand docs
    └── assets/          # Optional: output templates
```

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
agent normally — it invokes the skill when your request matches its
description.

Skills avoid changing your git state unless their own instructions say
otherwise; skills that inspect history only read commits already available on
your machine (never `git fetch` / `git pull`).

**Cursor CLI:** Install with `npx skills install` (skills land in
`~/.cursor/skills/` or `.cursor/skills/`). Invoke a skill with `/skill-name`
(for example `/release-notes`). Run the CLI with `agent` for interactive
sessions or `agent -p "..."` for scripts and CI.

## Available Skills

Skills sit on a workflow gradient — discover → sharpen → plan → slice →
implement → verify → ship — plus two startup skills that run once per
workspace/project. Full behavior, modes, and rules live in each skill's
`SKILL.md`; this table is the index.

| Skill | Phase | What it does | Example prompt |
| :--- | :--- | :--- | :--- |
| [`agents-md`](skills/agents-md/SKILL.md) | startup | Generates the workspace-root `AGENTS.md` (Project Matrix, 12 non-negotiable rules, skills gradient, context policy) plus a `CLAUDE.md` redirect shim, from a `.code-workspace` file | `Generate AGENTS.md for this workspace` |
| [`design-system`](skills/design-system/SKILL.md) | startup | Turns a provided design system (Figma, spec, reference screens, or guided session) into tokens + a UI library + a verifiable preview + a binding AGENTS.md rule; re-run `extend` as the design grows | `Set up the design system for ADMIN-WEB from this Figma file` |
| [`feature-discovery`](skills/feature-discovery/SKILL.md) | discover | Read-only, evidence-backed trace of how a feature, module, or behavior works; report returned in chat | `Trace the invite-user workflow across ADMIN-WEB and API-SERVICE` |
| [`port-feature`](skills/port-feature/SKILL.md) | discover | Maps a feature from a REFERENCE implementation into a TARGET stack as one gap map, then hands to planning | `Port stock-transfer approvals from LEGACY-PORTAL to ADMIN-WEB` |
| [`feature-prompt`](skills/feature-prompt/SKILL.md) | sharpen | Turns a rough idea into a small, PR-sized prompt file for `grill-with-docs` | `Help me create a feature prompt for stock transfer approvals` |
| [`integration-contract`](skills/integration-contract/SKILL.md) | slice | For multi-project PRDs only: writes a producer/consumer contract and an agent-browser smoke gate that must pass before shipping | `Build the integration contract for PRD-142` |
| [`orchestrate-herdr`](skills/orchestrate-herdr/SKILL.md) | implement | Inside [herdr](https://herdr.dev) only: fans a PRD's open sub-issues out to one local coding-CLI worker tab each and monitors for test-backed completion | `orchestrate-herdr for <PRD URL> using codex` |
| [`pixel-audit`](skills/pixel-audit/SKILL.md) | verify | Strict per-page visual-conformance audit against Figma or reference screens, with an element-level verification gate on served assets | `Pixel-audit the assets list page in ADMIN-WEB against this Figma node` |
| [`polish-batch`](skills/polish-batch/SKILL.md) | verify | Captures cosmetic QA nits without fixing them, dispatches them per PROJECT-CODE in one bounded pass, then verifies | `Punch-list this for PRD-142: Billing header says "Recieve invoices"` |
| [`commit-push-close`](skills/commit-push-close/SKILL.md) | ship | Commits with a structured message, pushes, and closes the linked GitHub issue with a how-to-test comment | `I'm done with #418, ship it` |
| [`commit-push-pr`](skills/commit-push-pr/SKILL.md) | ship | Commits, pushes (branching off `main` first), and opens a PR with `Closes #N`, summary, and test plan | `Commit, push, and open a PR for this issue` |
| [`release-notes`](skills/release-notes/SKILL.md) | ship | Turns git history, the current session, or a feature into PM-friendly release notes with QA steps | `Generate release notes for 11 March 2026` |

The gradient's plan/slice/implement/verify core (`/grill-with-docs`, `/to-prd`,
`/to-issues`, `/tdd`, `/review`, `/diagnosing-bugs`, `/triage`) comes from
[Matt Pocock's skills](https://github.com/mattpocock/skills) — separate
installs this kit is designed to interlock with. Run
`/setup-matt-pocock-skills` once per repo before using them.

## Workflow Guide

See [GUIDE.md](GUIDE.md) for the recommended workflow from workspace setup
through spec, issues, TDD implementation, verification, PR shipping, and
release notes — including the issue-title/label hard gate, workflow gates, and
recovery loops. See [BEST-PRACTICES.md](BEST-PRACTICES.md) for the mental
model: the gradient, context discipline, and anti-patterns.

Companion skills and MCPs (Graphify, agent-browser, Figma MCP, herdr,
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
execution).

The per-runtime mechanics — tool names, parallel/background mechanisms,
role-to-mechanism maps, and elevated-permission presets — live in
[`skills/agents-md/references/tool-calling.md`](skills/agents-md/references/tool-calling.md)
and the per-runtime `*-tools.md` files beside it. The human-facing summary
tables are in [GUIDE.md](GUIDE.md).

## Credits And Provenance

This repository combines original local skills with workflow ideas and companion
skills from the wider agent-skills ecosystem.

- Local skills and docs in this repository are authored and maintained by
  Arfeen Arif. Local git history shows the release-notes skill was added first,
  followed by feature-discovery, feature-prompt, agents-md, and the workflow
  guide.
- The non-negotiable discipline in `agents-md` was originally seeded by
  Forrest Chang's Karpathy-inspired `CLAUDE.md` guidelines and later expanded
  in this repo into a 12-rule core:
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

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for the skill authoring guide (token
budget, description-as-trigger, kit contract), the review rubric, and the
maintenance sync map. Before any commit, run:

```bash
bash tools/validate.sh
```

## License

[MIT](LICENSE) © Arfeen Arif

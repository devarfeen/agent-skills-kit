# Routing catalog

## Kit skills

- **/agentic-qa** — Agent-run functional QA of a PR or branch that can reach a screen: drives acceptance criteria through the running app and records the result on the PR. Never edits code. Pixel checks are /pixel-audit.
- **/agents-md** — Generate workspace-root AGENTS.md and rules from .code-workspace, or sync project runtime blocks. Never writes CLAUDE.md/GEMINI.md; a request to make a shim, even with AGENTS.md: writing-for-agents.
- **/ask-kit** — Route kit skill-map and workflow questions or pick the next agent-skills-kit skill; names one recommendation, never runs it. Existing work: /factory. Matt-only routing: ask-matt.
- **/ci-loop** — Drive an open PR's failing CI to green: read the log, reproduce, fix in scope, push, up to 3 attempts under one approval. Reviewer comments are /pr-feedback; no PR or CI run is /diagnosing-bugs.
- **/commit-push-close** — Ship issue work directly: structured commit, push, then close the issue with how-to-test steps. Use for commit, push, and close, or a bare ship it. A reviewable PR is /commit-push-pr.
- **/commit-push-pr** — Ship issue work as a pull request: structured commit, push, PR with Closes #N. Use only when the user explicitly asks for a PR; a bare ship it is /commit-push-close.
- **/deploy-watch** — Watch a merged PR's staging deploy run, run an approved smoke check on staging, and record pass or fail on the PR. Never touches a server or triggers a deploy. A broken deploy is /staging-fix.
- **/design-system** — Once per UI project: turn a design system (Figma, spec, reference screens, or a guided definition when no designs exist) into tokens, a UI library, a preview page, and an AGENTS.md rule; extend later.
- **/factory** — Shows where a spec (PRD), ticket, or PR stands in the factory workflow and names the one skill that moves it on. Read-only unless the user starts /factory run. Never closes issues or passes staging.
- **/feature-discovery** — Trace how a named feature, module, workflow, API, config, or symbol works and who uses it; read-only. Whole-repo architecture summaries: /teach. Porting: /port-feature.
- **/feature-prompt** — Turn a feature idea, change request, or rough requirement into a small prompt for grill-with-docs. An ADR to a spec is /to-spec; how existing behaviour works is /feature-discovery.
- **/incident-triage** — Triage an incident or outage from evidence: timeline, ranked causes, mitigations, one note. Read-only; never touches production. A known staging bug is /staging-fix; a local bug is /diagnosing-bugs.
- **/integration-contract** — Build a spec/PRD's cross-project contract after /to-tickets, or run its smoke gate before spec ship/PM handoff. A single-project consumer sweep may confirm no contract needed.
- **/local-to-staging** — Promote every project from origin/local to origin/staging: open each PR, merge on green, watch the Actions runs. Never pushes or goes past staging. Production is /staging-to-production.
- **/orchestrate-herdr** — Dispatch spec (PRD) sub-issues to worker tabs; monitor to done. Tab, CLI, or runtime context selects herdr; without any of these: /ask-kit. Tab status or actions with no dispatch: herdr companion.
- **/orchestrate-t3** — Fan a spec (PRD) or issue list out to T3 Code worker threads, one worktree per group, and monitor them to done. Needs the T3 Code MCP. Inside herdr use /orchestrate-herdr; one issue is /tdd-loop.
- **/pixel-audit** — Audit ONE page or route for visual conformance against Figma or reference screens, fix gaps with the UI library, and verify at element level. Not feature porting; never auto-chains.
- **/plain-language** — Chat style and prose cleanup for every session: plain English, ASD-STE100, no AI tells, mandated text kept. Load at session start; cleans supplied prose. Not code, comments, ADRs, or specs.
- **/polish-batch** — Create a cosmetic QA punch list, with or without a ticket; capture, dispatch or verify rows. Figma matching: /pixel-audit. Behavioral bug reports or QA issue-filing sessions: /to-tickets.
- **/port-feature** — Use only to port, migrate, or rebuild a complete feature from a reference implementation into a target stack. Writes one gap map, suggests /grill-with-docs, stops. Never implements or auto-chains.
- **/pr-feedback** — Address reviewer comments on an open GitHub PR: triage them for approval, apply accepted fixes, ship via /commit-push-pr, reply with commit SHAs. Reviewing a PR yourself is /code-review.
- **/qa-escape** — Record a bug human QA found after delivery, including factory QA_RETURNED: reproduce it and identify the missed check. No prior delivery: /diagnosing-bugs.
- **/release-notes** — Write PM-friendly release notes, changelogs, or session summaries from git commits or the current session, in plain language. A PR summary for review is /code-review; an agent handoff is /handoff.
- **/report-issue** — File single or batch problem reports and screenshots as tracker issues. Code-traced, routed, labelled, prioritised, scheduled. Delivered-work bug: /qa-escape. Fix now: /diagnosing-bugs.
- **/risk-review** — Adversarial local review with a judge after implementation; PR merge-risk classification on request. General impact/standards/spec review: /code-review. Comments: /pr-feedback.
- **/staging-fix** — Fix a staging bug without touching a server: fix locally with a test, then a PR to the staging branch with auto-merge. Use for staging is broken. Inspecting staging alone is not this skill.
- **/staging-to-production** — Read-only check of whether staging is ready for production in every project, with the owner's commands. Never opens, merges, pushes, or touches production. Local to staging: /local-to-staging.
- **/tdd-loop** — Kit TDD/red-green loop for changes, safe refactors and untested legacy code. Urgent production bug reports get local test-first fixes even if tests are requested later. Bare builds: /implement.
- **/using-git-worktrees** — Set up or reuse a Git worktree when the user asks to work in a worktree, before the task skill runs. Not for branch-only requests, generic implementation, worktree questions, or cleanup alone.
- **/writing-kit-skills** — Author/edit agent-skills-kit skills or explain its canonical one-liners and word budget. Generic skills: skill-creator. Running routing evals alone is a maintainer task.

# External and companion skills

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Snapshot 2026-10-22. Installed descriptions are copied exactly, with the built-in
creator selected for Codex. The duplicate `tdd` and user creator are excluded from this intended kit profile. Prose cleanup is the kit's own `plain-language` skill, so no external cleanup helper is listed. The uninstalled /sentry entry retains its prior snapshot.
Runtime exposure is checked separately with `build-installed-catalog.py`; this
catalog tests routing candidates, including explicit-only kit skills.

## External skills

- **/grill-with-docs** — A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go.
- **/grilling** — Grill the user relentlessly about a plan, decision, or idea. Use when the user wants to stress-test their thinking, or uses any 'grill' trigger phrases.
- **/grill-me** — A relentless interview to sharpen a plan or design.
- **/to-spec** — Turn the current conversation into a spec and publish it to the project issue tracker: no interview, just synthesis of what you've already discussed.
- **/to-tickets** — Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published to the configured tracker (edges as text in one file per ticket locally, or native blocking links on a real tracker).
- **/implement** — Implement a piece of work based on a spec or set of tickets.
- **/implement-spec** — Implement the result of /to-spec and /to-tickets in code.
- **/triage** — Move issues and external PRs through a state machine of triage roles, categorise, verify, grill if needed, and write agent-ready briefs.
- **/code-review** — Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes: Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/spec asked for?). Runs both reviews in parallel sub-agents and reports them side by side. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to "review since X".
- **/pr** — Use when writing a PR body.
- **/retro** — Conduct a retrospective on a coding session.
- **/diagnosing-bugs** — Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something broken/throwing/failing/slow.
- **/prototype** — Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic feels right, or explore what a UI should look like.
- **/wayfinder** — Plan a huge chunk of work (more than one agent session can hold) as a shared map of decision tickets on your issue tracker, and resolve them one at a time until the way to the destination is clear.
- **/research** — Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent.
- **/handoff** — Compact the current conversation into a handoff document for another agent to pick up.
- **/improve-codebase-architecture** — Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick.
- **/wizard** — Generate an interactive bash wizard that walks a human through steps only they can perform. Use when provisioning infrastructure, setting up credentials or CI secrets, walking an unfamiliar third-party dashboard, or running a one-off migration or cutover. Don't invoke this for steps the agent can perform itself.
- **/to-questionnaire** — Turn a decision you can't fully answer into a questionnaire for someone else to fill in.
- **/wait-what** — Stop. That last message did not land: re-pitch it.
- **/writing-for-agents** — Writing documents for agents. Use when creating or editing skills, or modifying AGENTS.md or CLAUDE.md.
- **/teach** — Teach the user a new skill or concept, within this workspace.
- **/setup-matt-pocock-skills** — Configure this repo for the engineering skills: set up its issue tracker, triage label vocabulary, and domain doc layout. Run once before first use of the other engineering skills.
- **/ask-matt** — Ask which skill or flow fits your situation. A router over the skills in this repo.
- **domain-modeling** — Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or editing a GLOSSARY.md, or recording or editing an ADR.
- **codebase-design** — Shared vocabulary for designing deep modules. Use when the user wants to design or improve a module's interface, find deepening opportunities, decide where a seam goes, make code more testable or AI-navigable, or when another skill needs the deep-module vocabulary.
- **agent-browser** — Browser automation CLI for AI agents. Use when the user needs to interact with websites, including navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, testing web apps, or automating any browser task. Triggers include requests to "open a website", "fill out a form", "click a button", "take a screenshot", "scrape data from a page", "test this web app", "login to a site", "automate browser actions", or any task requiring programmatic web interaction. Also use for exploratory testing, dogfooding, QA, bug hunts, or reviewing app quality. Also use for automating Electron desktop apps (VS Code, Slack, Discord, Figma, Notion, Spotify), checking Slack unreads, sending Slack messages, searching Slack conversations, running browser automation in Vercel Sandbox microVMs, or using AWS Bedrock AgentCore cloud browsers. Prefer agent-browser over any built-in browser automation or web tools.
- **impeccable** — Use when the user wants to design, redesign, shape, critique, audit, polish, clarify, distill, harden, optimize, adapt, animate, colorize, extract, or otherwise improve a frontend interface. Covers websites, landing pages, dashboards, product UI, app shells, components, forms, settings, onboarding, and empty states. Handles UX review, visual hierarchy, information architecture, cognitive load, accessibility, performance, responsive behavior, theming, anti-patterns, typography, fonts, spacing, layout, alignment, color, motion, micro-interactions, UX copy, error states, edge cases, i18n, and reusable design systems or tokens. Also use for bland designs that need to become bolder or more delightful, loud designs that should become quieter, live browser iteration on UI elements, or ambitious visual effects that should feel technically extraordinary. Not for backend-only or non-UI tasks.
- **herdr** — Control Herdr, a terminal multiplexer for coding agents. Use only when the user explicitly mentions Herdr or asks to use Herdr to inspect or control panes, tabs, workspaces, commands, or another agent. Do not use merely because a task could benefit from a background terminal, delegation, or parallel work. Requires HERDR_ENV=1.
- **skill-creator** — Create or update a Codex skill with appropriately scoped instructions and any needed supporting resources.
- **/sentry** — Investigate production errors via the Sentry CLI before local diagnosis.
- **frontend-design** — Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one. Helps with aesthetic direction, typography, and making choices that don't read as templated defaults.

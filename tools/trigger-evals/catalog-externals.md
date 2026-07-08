## External and companion skills (snapshot)

> Snapshot 2026-07-09, taken from installed copies at mattpocock/skills
> v1.1.0. These are separate installs a normal kit workspace has; they compete
> for routing, so the catalog must include them. Refresh this file (and the
> date) when an upstream description changes.

Matt Pocock core:

- **/tdd** — Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integration tests.
- **/grill-with-docs** — A relentless interview to sharpen a plan or design, which also creates docs (ADR's and glossary) as we go.
- **/to-spec** — Turn the current conversation into a spec and publish it to the project issue tracker — no interview, just synthesis of what you've already discussed.
- **/to-tickets** — Break a plan, spec, or the current conversation into a set of tracer-bullet tickets, each declaring its blocking edges, published to the configured tracker — edges as text in a local file, or native blocking links on a real tracker.
- **/implement** — Implement a piece of work based on a spec or set of tickets.
- **/triage** — Move issues and external PRs through a state machine of triage roles — categorise, verify, grill if needed, and write agent-ready briefs.
- **/code-review** — Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes — Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/PRD asked for?). Runs both reviews in parallel sub-agents and reports them side by side. Use when the user wants to review a branch, a PR, work-in-progress changes, or asks to "review since X".
- **/diagnosing-bugs** — Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something broken/throwing/failing/slow.
- **/prototype** — Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic feels right, or explore what a UI should look like.
- **/wayfinder** — Plan a huge chunk of work — more than one agent session can hold — as a shared map of investigation tickets on your issue tracker, and resolve them one at a time until the way to the destination is clear.
- **/research** — Investigate a question against high-trust primary sources and capture the findings as a Markdown file in the repo. Use when the user wants a topic researched, docs or API facts gathered, or reading legwork delegated to a background agent.
- **/handoff** — Compact the current conversation into a handoff document for another agent to pick up.
- **/setup-matt-pocock-skills** — Configure this repo for the engineering skills — set up its issue tracker, triage label vocabulary, and domain doc layout. Run once before first use of the other engineering skills.
- **/ask-matt** — Ask which skill or flow fits your situation. A router over the skills in this repo.

Companions:

- **agent-browser** — Browser automation CLI for AI agents: navigate pages, fill forms, click, screenshot, extract data, test web apps, QA/bug hunts, and Electron app automation.
- **graphify** — Any question about a codebase, its architecture, file relationships, or project content — especially when a generated knowledge graph exists; query/path/explain over the graph.
- **impeccable** — Design, redesign, critique, audit, polish, or otherwise improve a frontend interface: UX review, visual hierarchy, accessibility, typography, spacing, color, motion, and reusable design systems or tokens.
- **qa** — Interactive QA session where the user reports bugs conversationally and the agent files GitHub issues.
- **herdr** — Control herdr from inside it: manage workspaces and tabs, split panes, spawn agents, read output, and wait for state changes (HERDR_ENV=1).
- **docker-expert** — Docker containerization: Dockerfiles, Compose, image optimization, security hardening, registries, and production deployment.
- **domain-modeling** — Build and sharpen a project's domain model, terminology, and ubiquitous language; record architectural decisions.
- **codebase-design** — Design deep modules: interfaces, seams, testability, and AI-navigability.
- **skill-creator** — Create new skills, improve existing skills, and run skill evals.
- **/sentry** — Investigate production errors via the Sentry CLI before local diagnosis.

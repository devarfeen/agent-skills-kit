## External and companion skills (snapshot)

> Snapshot 2026-07-06, taken from installed copies. These are separate
> installs a normal kit workspace has; they compete for routing, so the
> catalog must include them. Refresh this file (and the date) when an
> upstream description changes.

Matt Pocock core:

- **/tdd** — Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integration tests.
- **/grill-with-docs** — Grill the user relentlessly about a plan or design against the domain model and docs; resolves ambiguities, sharpens domain terms, updates CONTEXT.md, and records hard decisions as an ADR.
- **/to-prd** — Turn an ADR or refined plan into a PRD published to the configured tracker.
- **/to-issues** — Slice a PRD into thin, testable sub-issues with ready labels and dependency order.
- **/triage** — Repair or route existing/raw GitHub issues: state labels, needs-info, wontfix, ready-for-human, or an agent brief before implementation.
- **/review** — Review the changes since a fixed point (commit, branch, tag, or merge-base) for standards and spec conformance. Use when the user wants to review a branch, a PR, or work-in-progress changes.
- **/diagnosing-bugs** — Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug this", or reports something broken/throwing/failing/slow.
- **/prototype** — Build a throwaway prototype to answer a design question. Use when the user wants to sanity-check whether a state model or logic feels right, or explore what a UI should look like.
- **/handoff** — Write a continuation doc and fork context into a new session for the next agent.
- **/setup-matt-pocock-skills** — One-time workspace setup: configure the issue tracker, labels, and where CONTEXT.md / docs live.
- **/ask-matt** — Router for choosing which Matt skill flow fits; routes, never executes.

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

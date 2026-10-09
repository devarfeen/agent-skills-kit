# Skills Manifest

Single source for the `## Working with skills` tables generated into `AGENTS.md`.
Do not hardcode skill rows in `SKILL.md` — edit this file to add or move a skill.

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Columns:

- `skill` — invocation (e.g. `/tdd`) or companion name.
- `kind` — `kit` (lives in this repo's `skills/`), `external` (on the gradient but a
  separate install — e.g. Matt Pocock's skills), or `companion` (optional separate
  install, off the gradient).
- `phase` — for `kit`/`external`: a gradient phase (`discover`, `sharpen`, `plan`,
  `slice`, `implement`, `verify`, `ship`) or `startup`; `companion` places a kit skill off the gradient. Blank for external companions.
- `note` — optional short suffix shown after the skill in the gradient cell (e.g. `→ ADR`). A note beginning `deprecated` or `kit-internal` excludes the row from all generated catalogs and startup notes. Keep the row for kit coverage; exclusion does not remove the skill from this repo.
- `use-when` — for companion entries (kind or phase): the trigger text. Blank for gradient/startup skills.

Every folder under this repo's `skills/` must have a `kit` row here
(`tools/validate.sh` enforces this).

## Gradient Skills (kit + external)

| skill | kind | phase | note | use-when |
| ----- | ---- | ----- | ---- | -------- |
| `/agents-md` | kit | startup | once per workspace; re-run to refresh the Project Matrix | |
| `/design-system` | kit | startup | once per UI project; re-run `extend` as the design grows | |
| `/writing-kit-skills` | kit | startup | kit-internal — house style for authoring this repo's skills; not workspace routing | |
| `/feature-discovery` | kit | discover | | |
| `/port-feature` | kit | discover | reference → target gap map | |
| `/research` | external | discover | delegable primary-source reading → cited doc | |
| `/feature-prompt` | kit | sharpen | → prompt file | |
| `/grill-with-docs` | external | plan | numbered frontier rounds → ADR | |
| `/to-spec` | external | plan | → spec (PRD) | |
| `/wayfinder` | external | plan | fog, not size — decisions gate the scope; map them as tracker tickets, resolve one per session, exit to /to-spec | |
| `/prototype` | external | plan | spike ungrillable "needs to feel/see it" questions, then back to /grill-with-docs | |
| `/handoff` | external | plan | fork context to a new session (pairs with /prototype) | |
| `/to-tickets` | external | slice | | |
| `/triage` | external | slice | raw incoming issues and external PRs only — never /to-tickets tickets | |
| `/implement` | external | implement | optional ticket driver — run with /tdd-loop at each seam; stop after /code-review, never commit, overriding its own text (Shipping is owned by the ship skills) | |
| `/implement-spec` | external | implement | user-invoked whole-spec driver — parallel implementers in worktrees, merged onto one local integration branch; each drives /tdd-loop; stop after /code-review — never push, open a PR, or close tickets, overriding its own text (Shipping is owned by the ship skills) | |
| `/tdd` | external | implement | reference only — test quality and seam choice; never use it alone as a loop | |
| `/tdd-loop` | kit | implement | the test-first procedure — gates, completion evidence, exception protocol; stands alone | |
| `/orchestrate-herdr` | kit | implement | inside herdr only — fan a spec (PRD) out to worker tabs | |
| `/orchestrate-t3` | kit | implement | T3 Code MCP connected only — fan a spec (PRD) or an issue list out to T3 Code threads, one worktree per group | |
| `/code-review` | external | verify | | |
| `/diagnosing-bugs` | external | verify | | |
| `/polish-batch` | kit | verify | cosmetic punch-list | |
| `/pixel-audit` | kit | verify | per-page visual conformance | |
| `/integration-contract` | kit | verify | multi-project seams — build after /to-tickets, gate before the spec ships | |
| `/agentic-qa` | kit | verify | agent-run functional QA on any change that can reach a screen — state × viewport × role grid, console and network gate; never edits code | |
| `/qa-escape` | kit | verify | a bug human QA found after an agent said done → reproduction, escape class on the issue, regression test first; durable guard at 3 with approval | |
| `/ci-loop` | kit | verify | an open PR's failing CI → green — up to 3 fix-and-push attempts under one approval; never edits the gate | |
| `/risk-review` | kit | verify | specialist lenses + fixed-rubric low/high tier on a green PR; low offers auto-merge, high requests an engineer | |
| `/commit-push-close` | kit | ship | | |
| `/commit-push-pr` | kit | ship | | |
| `/pr-feedback` | kit | ship | address reviewer comments on an open PR — classify, fix, reply with SHAs | |
| `/staging-fix` | kit | ship | staging bug → local fix with test → PR to `staging` with auto-merge; servers never touched | |
| `/deploy-watch` | kit | ship | merged PR → watch the staging deploy run + approved smoke check; ends at ready for owner | |
| `/local-to-staging` | kit | ship | all projects: `origin/local` → `origin/staging` PRs, merged on green, Actions runs watched; never past staging | |
| `/staging-to-production` | kit | ship | read-only: staging→production readiness per project + commands for the owner; never opens or merges | |
| `/release-notes` | kit | ship | | |

## Companion Skills And MCPs

| skill | kind | phase | note | use-when |
| ----- | ---- | ----- | ---- | -------- |
| `/using-git-worktrees` | kit | companion | | The user asks to work in a worktree — invoke before task edits or the task skill; reuse or create the checkout under that project repo’s gitignored `.worktrees/`, verify its baseline, then return to the authorized task. Branch-only requests do not qualify. |
| `/ask-kit` | kit | companion | | You do not know which kit skill fits, and there is no spec, ticket, or PR to point `/factory` at. Names one skill and why; never runs it. User-invoked (`/ask-kit`); do not auto-fire. |
| `/factory` | kit | companion | | You want to know where a spec (PRD), ticket, or PR stands — CI, review, risk gate, staging deploy — and which one skill moves it next. Read-only; suggests, never runs the next skill; stops at staging. Only the user's own `/factory run <label or reference>` makes it carry the chain out, pausing for review, merge, issue close, and cleanup. |
| `/incident-triage` | kit | companion | | An incident or outage needs a timeline, ranked causes with evidence, and owner-run mitigations. Read-only; production is never accessed. |
| ask-matt | companion | | | You want Matt's upstream router for choosing a user-invoked skill flow. |
| pr | companion | | | A PR body is being written — smallest visual that shows the change, before/after evidence, one-way or two-way door plus blast radius. Inside `/commit-push-pr` or a repo PR template it shapes the summary visual and wording only; mandated sections, order, and `Closes #N` stay. |
| retro | companion | | | A session is finished — especially one that went sideways — and the agent's environment should improve: navigation pointers, automated checks, coding standards, steering files. Proposes, never edits. User-invoked (`/retro`); do not auto-fire. |
| wait-what | companion | | | The agent's last chat message did not land — re-pitch it with brief context, ASD-STE100 Simplified Technical English, and the ubiquitous language from `GLOSSARY.md`. |
| unslop | companion | | | Free-prose output needs AI tells removed — chat narration, and PR/issue/doc prose the agent composes freely. Never applies to text a skill mandates verbatim: generated `AGENTS.md`/shims, output templates, section names, field labels, canonical lines. |
| blast-radius | companion | | | A change's blast radius needs proving — what it could break beyond the diff, with the one safety fact run against real code rather than a writeup. User-invoked (`/blast-radius`); do not auto-fire. |
| show-me-your-work | companion | | | Long-running or unattended work needs a reviewable decision trail — a TSV log of what, why, evidence, and result that a human can audit after stepping away. User-invoked (`/show-me-your-work`); do not auto-fire. |
| before-and-after | companion | | | A visible change needs a before and after screenshot pair, from two URLs, saved to a local folder. Images stay local: never pass `--markdown` or run its upload script, whose default host is public. |
| code-structure | companion | | | The same operational logic is repeated across two or more flows, or a change must decide what belongs in an action and what in a shared service. |
| evidence-driven-testing | companion | | | A change needs a recorded session as proof — an annotated screen recording of the app being driven, or measured numbers and output pairs for work with no screen. It adds evidence; `/agentic-qa` stays the QA gate. |
| wizard | companion | | | A procedure hits steps only a human can perform (credentials, CI secrets, third-party dashboards, one-off migrations/cutovers) — generate an interactive bash walkthrough for them; never for steps the agent can do itself. |
| to-questionnaire | companion | | | A decision needs knowledge the user lacks — turn it into a Markdown questionnaire the one person who can answer fills in async or in a meeting. |
| domain-modeling | companion | | | Project terminology, aliases, or ADR-backed domain language need sharpening. |
| codebase-design | companion | | | Module boundaries, seams, or interface design decisions matter. |
| Graphify | companion | | | Querying a generated code/docs/media graph would save broad file reads. Follow the workspace Graphify rule for graph location, query scope, and refresh. |
| Codex plugin for Claude Code | companion | | | Claude Code needs Codex for review or delegated work. |
| Impeccable | companion | | | Frontend design quality, visual polish, or browser-backed UI checks matter. |
| notebooklm-py | companion | | | The user asks to work with NotebookLM sources or artifacts. |
| agent-browser | companion | | | Browser automation, app QA, screenshots, scraping, or Electron app control is needed. |
| herdr | companion | | | Running inside herdr and managing panes, tabs, or worker agents is needed. |
| docker-expert | companion | | | Dockerfiles, Compose, images, containers, or registry workflows are central. |
| Laravel Boost | companion | | | A Laravel project has Boost installed and Laravel-specific MCP context helps. |
| Figma MCP | companion | | | A task references Figma designs, components, frames, tokens, or design-to-code. |
| MySQL/Postgres MCP | companion | | | Approved local or staging database inspection is needed. Default read-only. |
| Linear MCP | companion | | | Finding, creating, updating, or closing tracker issues (specs, tickets, bugs). |
| Sentry CLI | companion | | | A production error report needs `/sentry` investigation before `/diagnosing-bugs`. |

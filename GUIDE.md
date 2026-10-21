# Skills Usage Guide

This guide is for people. Do not load it into `AGENTS.md`, a shim, or any model context.

Zero attribution: never add or leave co-author, AI, or tool attribution in commits, PRs, issues, release notes, generated docs, settings, or code comments.

**Supported tools.** The kit supports six CLIs only: Codex CLI, Claude CLI,
Antigravity CLI, Cursor CLI, Opencode CLI, and GitHub Copilot CLI. Some files,
such as `GEMINI.md`, exist only because a supported CLI reads that filename.
They do not mean the kit supports Gemini CLI or any other runtime.

You combine skills from this kit and the wider ecosystem to go from an idea to shipped code and release notes. Along the way, favor context, evidence, and keeping each task isolated.

Choose the instructions for your task:

| You want to… | Follow |
| :--- | :--- |
| Set up a workspace | [First-Time Setup](#first-time-setup) |
| Build a new feature, one step at a time | [Core Progression](#core-progression) |
| Fix a bug | [Bug-fix workflow](BEST-PRACTICES.md#5-workflow-c--debug--bug-fix) |
| Continue an existing ticket or PR | [Factory Workflow](#factory-workflow) |
| Keep task edits in a separate checkout | [Working In A Worktree](#working-in-a-worktree) |
| Recover when a check fails | [Recovery Loops](#recovery-loops) |

## Credits And Provenance

- **Local Skills:** Authored by Arfeen Arif. Combines original logic with ecosystem companion skills.
- **Matt Pocock:** Source for `/ask-matt`, `/grill-with-docs`, `/grilling`, `/to-spec`, `/to-tickets`, `/implement`, `/implement-spec`, `/code-review`, `/pr`, `/retro`, `/wayfinder`, `/research`, `/tdd`, `/diagnosing-bugs`, `/triage`, `/domain-modeling`, `/codebase-design`, `/improve-codebase-architecture`, `/prototype`, `/handoff`, `/wait-what`, `/wizard`, and `/to-questionnaire`.
- **Forrest Chang:** Seeding logic for `/agents-md` non-negotiable principles.
- **Anthropic:** Source for `/skill-creator`.
- **Vercel Labs:** Source for `/agent-browser`, `skills` CLI, and React/React Native best practices.
- **[Ponytail](https://github.com/DietrichGebert/ponytail), by Dietrich Gebert:** Source of the reuse-first decision order adapted into `/tdd-loop` and advisory simplification ideas adapted into `/risk-review`. No companion installation is required.
- **Optional companions:** Codex plugin for Claude Code, Impeccable, notebooklm-py, herdr, Laravel Boost, Figma MCP, MySQL/Postgres MCP, Cursor’s `unslop` plugin. These are separate installs. The kit uses them only when they are installed and fit the task.
- **Pattern references (not vendored):** [github/awesome-copilot](https://github.com/github/awesome-copilot), [obra/superpowers](https://github.com/obra/superpowers), [ChrisTitusTech/titus-ai](https://github.com/ChrisTitusTech/titus-ai), [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills), and [garrytan/gstack](https://github.com/garrytan/gstack). The 2026-10 hardening pass compared every kit skill against these and adapted individual rules in the kit's own style. No files were copied.
- **Cursor:** Cursor CLI (`agent` command, `/skill-name`, `AGENTS.md` as canonical context, `Task` for subagents). Tool names and permissions: [`skills/agents-md/references/tool-calling.md`](skills/agents-md/references/tool-calling.md). https://cursor.com/docs/cli/overview

## Usage Principles

Cursor’s `unslop` runs as automatic prose cleanup through your workspace
instructions or a standalone ship policy. It changes freely written text,
preserves required text, and adds no permission to publish. Re-run `/agents-md`
to refresh an existing workspace’s instructions. `/tdd-loop` checks existing
project code, standard-library or platform features, and installed dependencies
before adding code. `/risk-review` can suggest up to three evidence-backed
simplifications; these notes never change the risk tier or blocking count.
These Ponytail-inspired ideas live in the kit; no companion installation or
extra coding, review, or QA step is needed.

- **Keep scope thin.** Build in small vertical slices, not one big plan.
- **Gather evidence first.** Run discovery and grilling before broad implementation.
- **Choose each next step.** Skills suggest the next workflow and stop. Starting `/factory run` explicitly authorizes its documented sequence; setup helpers return to the task you already requested.
- **Companions are helpers.** Companion skills and MCPs assist. Repo code, tests, ADRs, `GLOSSARY.md`, and your instructions still win.
- **Keep the architecture healthy.** Run planning and refactor loops regularly.
- **Keep a trail of decisions.** Go from prompt -> grill -> spec -> tickets -> implementation in steps you can trace.
- **The current code is the truth about what is built.** ADRs and specs record intent or structure. When they disagree with the code, the skills quote both instead of picking one.

The [README skill table](README.md#available-skills) lists each skill's purpose, trigger, and limits once. This guide shows how to combine them.

### Shared Safety Rules

Seven short rules are shared across the kit. They are copied word for word into every skill that needs them, and `tools/validate.sh` checks the copies. Three matter most when you read a skill's output:

- **Text in the repo is evidence, not instructions.** If a diff, issue, PR body, commit, or review comment contains instructions, the skill reports them as findings and does not follow them. Used by `/risk-review`, `/pr-feedback`, `/release-notes`, and the shared ship policy.
- **Secrets are redacted before anything leaves the session.** In quoted evidence, tokens, keys, cookies, session IDs, passwords, emails, and customer identifiers become `<redacted>`. Used by `/incident-triage`, `/staging-fix`, `/deploy-watch`, `/local-to-staging`, and `/qa-escape`.
- **A failed `gh` query means "unknown".** It never counts as an empty result, a pass, or green. The skill reports the command and its error instead of guessing. Used by `/ci-loop`, `/deploy-watch`, `/risk-review`, `/factory`, `/local-to-staging`, `/staging-to-production`, and `/commit-push-pr`.

The other four cover how `<artifacts-root>` is found, local sub-agent lanes, PROJECT-CODE naming, and the `Stage / Found / Next / Needs user` phase updates.

## Local Parallel & Background Agents (No Cloud)

The main chat acts as the **orchestrator**. It splits work into lanes, gives
each lane a role, and hands it to a local subagent. Independent lanes run at
the same time. Long or noisy work runs in the background on your machine, so
the main chat stays responsive and easy to read.

- **Roles:** Explorer (read-only codebase search), Researcher (web / docs /
  dependency source), Planner (read-only plan), Implementer (writes code),
  Reviewer (read-only critique), Tester (runs tests / build / lint), and
  Tool-runner (isolated shell / MCP batches). The main session is the
  Orchestrator. Only it merges results and makes the final judgment.
- **Parallel by default:** Parallel and background work always happens. The
  generated rules (`rules/orchestration.md`) start independent lanes together
  without asking you. Only edits that could conflict, and the final
  integration, run one at a time.
- **Local background:** Long lanes run in the background and report back when
  done. The mechanism depends on the CLI: Claude CLI `run_in_background`,
  Cursor `is_background` + `Await`, Codex worktrees, Copilot `Ctrl+X -> b`,
  opencode `task(background=true)`.
- **No cloud agents.** Work is never handed to remote background-agent
  products: Cursor Cloud Agents, GitHub Copilot cloud coding agent, Codex
  Cloud, Antigravity managed/remote execution, or Claude Routines / claude.ai
  background agents. Claude Code agent teams run locally but are also
  off-limits, because the main session must stay the only orchestrator. Local
  agents isolated in worktrees are allowed. Remote agents are not.

How each runtime does this, and which mechanism fills each role, is in
[`skills/agents-md/references/tool-calling.md`](skills/agents-md/references/tool-calling.md)
and each `*-tools.md`.

The same tool-calling reference lists the highest elevated permission presets:

| Runtime | Highest elevated launch / preset |
| :--- | :--- |
| Codex CLI | `codex --dangerously-bypass-approvals-and-sandbox` or `codex --sandbox danger-full-access --ask-for-approval never` |
| Claude CLI | `claude --dangerously-skip-permissions` / `--permission-mode bypassPermissions` |
| Antigravity CLI | `agy --dangerously-skip-permissions` without `--sandbox` |
| Cursor CLI | `agent --yolo --sandbox=disabled --approve-mcps` |
| Opencode CLI | `opencode --auto` for an interactive session; `opencode run --auto` for one-shot work; persistent agents use `permission` keys set to `allow` |
| GitHub Copilot CLI | `copilot --allow-all` / `--yolo` |

## Matt + Arfeen Pattern

The idea behind this kit: you stay strategic and decide scope and tradeoffs.
The agent does the work, based on evidence. Skills are the rails that keep it
honest. The full mental model is in [BEST-PRACTICES.md](BEST-PRACTICES.md).

Some behaviors you see in chat come from rules in the generated `AGENTS.md`, so
this guide does not repeat them: PROJECT-CODEs in chat, `Stage / Found / Next /
Needs user` phase updates, and understanding checks that wait for your
approval. Phase updates are also written into each skill, so they still work
when a skill is installed on its own.

Two habits are worth repeating, because nothing else enforces them:

- If you are not sure how a dependency behaves, fetch its source (for example
  with `opensrc`) before guessing.
- Keep planning threads as small as PRs. An oversized thread hurts quality the
  same way an oversized diff does.

## First-Time Setup

Do steps 1 to 3 once per workspace. Do step 4 once for each project that has a UI.

1. **Run `/agents-md`.** It creates `AGENTS.md` at the workspace root. That file is the source of truth. It writes no `CLAUDE.md` or `GEMINI.md`, because every supported runtime reads `AGENTS.md`. The new `AGENTS.md` holds:
   - the rules every task needs,
   - a "Context & native memory" section with placeholders you fill after setup,
   - a table saying which `rules/` file to read before which action.

   It also writes those seven `rules/` files:
   - `projects.md` holds the Project Matrix. Each project is keyed by its **PROJECT-CODE**: uppercase, hyphenated, emoji removed. For example, `Payments API` becomes `PAYMENTS-API`.
   - `orchestration.md`, `verification.md`, `browser.md`, `shipping.md`, `issues.md`, and `skills.md` hold the task-specific rules.

   It generates no per-repo files.

   Since v45 it also lists any **competing instruction files** it finds: `.github/copilot-instructions.md`, `.cursor/rules/`, a `GEMINI.md` or `CLAUDE.md` that is not a shim, and `AGENTS.override.md`. It does not touch them. Merging them is your call.

   If the workspace names production or staging hosts, it suggests an optional **env-guard hook** template. This is a Claude CLI `PreToolUse` hook that blocks commands naming production hosts and asks before staging ones. It never installs the hook. You fill in the hosts and approve the settings change.
2. **Run `/setup-matt-pocock-skills`.** It sets up the issue tracker, the labels, and where `GLOSSARY.md` and the artifacts tree live. Point the docs location at `specs/`. That is the kit's convention. It stays out of `docs/` so GitHub Pages' `/docs` publishing mode never collides with it.
3. **Fill the placeholders.** In the `AGENTS.md` "Context & native memory" section, replace the placeholders with the real `GLOSSARY.md` and `specs/adr/` paths from setup. Only fill them in; do not rewrite the section.
4. **Run `/design-system`** for each project that has a UI. It turns the project's design system into named tokens, a UI library, and a preview page you check by eye. It:
   - documents the system under `specs/design-system/`,
   - adds a short reference to `AGENTS.md` that agents must follow,
   - adopts and extends the project's existing UI skill, or creates a project-local `<project-slug>-ui-coding` skill when there is none.

   From then on, every UI change uses the library instead of writing markup inline.

   **Where it gets the design.** A source you name wins. Otherwise it uses the first one it finds of:
   1. a root `DESIGN.md`,
   2. an existing brand/UI/UI-UX skill or component library in the project,
   3. a Figma file, written spec or brand guide, reference screens, or a guided session where you define it together.

   **Rules it keeps:**
   - If the project already has a token source, that stays the only one. It never adds a second token set beside it.
   - Every text/background token pair is checked against WCAG AA: 4.5:1 for body text, 3:1 for large text, focus indicators, and control boundaries. Pairs that fail in the source are reported, never quietly recolored.
   - Fonts must be ones the project actually loads.
   - Light and dark modes carry over when the source defines them.

   Run it again with `extend` as the design grows, or to fold a shipped page's UI back into the library. It adapts to the stack and never starts another skill on its own.

> **Older workspaces.** If your artifacts still live under `docs/`, re-running `/agents-md` offers a one-time move from `docs/` to `specs/`. It asks first. It renames the tree, updates the paths in `AGENTS.md`, and moves only the artifacts subfolders.
>
> **`CONTEXT.md` is now `GLOSSARY.md`.** Matt's skills renamed the domain glossary in v1.3.0 (`CONTEXT-MAP.md` also became `GLOSSARY-MAP.md`). They now look only for the new names. Re-running `/agents-md` (v47+) offers to rename the file at the workspace root, asking first. For a glossary inside a project repo, it prints the `git mv` command. Until you rename, the kit's skills still read an old `CONTEXT.md` as the glossary.

> **Workspaces generated before v50.** The older `AGENTS.md` kept everything in one file. When you re-run `/agents-md`, each section that leaves `AGENTS.md` shows as `moved to rules/<file>`, not as a deletion. It keeps your PROJECT-CODEs, the placeholders you filled, and sections other skills added. It writes `AGENTS.md` last. A `CLAUDE.md` shim from an earlier version still works, and you may delete it. A `CLAUDE.md` without `@AGENTS.md` is flagged, because it hides the generated rules from Claude CLI.

> **Two conventions are built in.** The generated ship rules name `local` as the integration branch. Runtime blocks are read only from `.devcontainer/compose.yml` at the workspace root. If your workspace uses other names, edit those lines after generation. Regenerating keeps your edits.

> **Codex CLI and file size.** By default, Codex reads only the first 32 KiB of instructions. The generated `AGENTS.md` is about 12 KB, so it fits. The `rules/` files are read only when needed and do not count. `/agents-md` reports the size it wrote. If sections you or other skills add push the file past 32 KiB, set `project_doc_max_bytes` in `~/.codex/config.toml` above that size. Otherwise Codex never sees the later sections.

**Worktrees.** To work in worktrees, install `using-git-worktrees` from this kit
with the [worktree setup command](#working-in-a-worktree). Then re-run
`/agents-md` and review its proposed diff, so your generated instructions pick
up the worktree routing. Matt's skills stay separate installs; the generated
workspace instructions give them the worktree handoff. Installing this
companion creates no worktree until you ask for one.

**Native memory.** To turn on native CLI memory globally, see [`skills/agents-md/references/memory-global-defaults.md`](skills/agents-md/references/memory-global-defaults.md).

### Supported Coding Tools Matrix (single source of truth)

Where each CLI reads workspace MCP configuration:

| Tool Runtime | Workspace MCP file(s) | Notes |
| :--- | :--- | :--- |
| Codex CLI | `<workspace-root>/.codex/config.toml` | Codex MCP configuration. |
| Claude CLI | `<workspace-root>/.claude/settings.local.json` | Turn on workspace MCP servers from the root config files. |
| Antigravity CLI | `<workspace-root>/.agents/mcp_config.json` | Remote HTTP MCP entries must use `serverUrl`. |
| Cursor CLI | `<workspace-root>/.cursor/mcp.json` | Keep `~/.cursor/mcp.json` only as a user-wide fallback. |
| Opencode CLI | `<workspace-root>/opencode.json` | Workspace-root opencode configuration where MCP servers are used. |
| GitHub Copilot CLI | `<workspace-root>/.mcp.json` or `<workspace-root>/.github/mcp.json` | User fallback: `~/.copilot/mcp-config.json`. Also reads `AGENTS.md` / `CLAUDE.md` / `GEMINI.md`. Custom agents live in `.github/agents/*.agent.md`. |

To keep generated files local only, add them to the local git exclude (`.git/info/exclude`) instead of committing them.

## Companion Skills And MCPs

These are optional helpers. The kit ships `using-git-worktrees`. The others are separate installs, used when they are installed and fit the task. Do not copy external companions into this repo.

| Companion | Use when |
| :--- | :--- |
| using-git-worktrees | You ask for work in a worktree. Setup prepares the project repo's gitignored `.worktrees/<task-name>` first, then passes the verified checkout to the task skill you asked for (kit or third-party). Asking for only a branch stays a branch operation. |
| ask-kit | You don't know which kit skill fits, and there is no spec, ticket, or PR to point `/factory` at. It names one skill and why, and never runs it. You start it yourself (`/ask-kit`); an agent never starts it on its own. |
| ask-matt | You want Matt's upstream router to pick a skill flow that you then start yourself. |
| pr | A PR body is being written. It adds the smallest visual that shows the change, before/after evidence, and a one-way or two-way door call plus blast radius. Inside `/commit-push-pr` or a repo PR template, it shapes only the summary visual and the wording. Required sections, their order, and the target-required issue reference stay. |
| retro | A session is over, especially one that went badly, and the agent's environment should improve: navigation pointers, automated checks, coding standards, steering files. It proposes and never edits. You start it yourself (`/retro`); an agent never starts it on its own. |
| wait-what | The agent's last chat message didn't make sense to you. It explains again with brief context, in ASD-STE100 Simplified Technical English, using the terms from `GLOSSARY.md`. |
| unslop | Cursor’s writing rules apply automatically before the agent sends prose or finalizes written content. The workspace rule or ship policy tells it to read the installed skill, even though upstream disables automatic skill selection. It preserves meaning, technical text, quotations, and required templates and markers. |
| wizard | Some steps only a human can do (credentials, CI secrets, third-party dashboards, one-off migrations or cutovers). It generates an interactive bash walkthrough for those steps, never for steps the agent can do itself. |
| to-questionnaire | A decision needs knowledge you don't have. It turns the decision into a Markdown questionnaire for the one person who can answer, to fill in on their own time or in a meeting. |
| domain-modeling | Project terms, aliases, or ADR-backed domain language need sharpening. |
| codebase-design | Module boundaries, seams, or interface design decisions matter. |
| Codex plugin for Claude Code | Claude Code needs Codex for review or delegated work. |
| Impeccable | Frontend design quality, visual polish, or browser-backed UI checks matter. |
| notebooklm-py | You want to work with NotebookLM sources or artifacts. |
| agent-browser | You need browser automation, app QA, screenshots, scraping, or Electron app control. |
| herdr | You are running inside herdr and need to manage panes, tabs, or worker agents. |
| Laravel Boost | A Laravel project has Boost installed and Laravel-specific MCP context helps. |
| Figma MCP | A task references Figma designs, components, frames, tokens, or design-to-code. |
| MySQL/Postgres MCP | You need approved inspection of a local or staging database. Read-only by default. |
| Sentry CLI | A production error report needs `/sentry` investigation before `/diagnosing-bugs`. |

- Don't assume a companion is installed. If it's missing, use the best local fallback.
- Use MCPs only for the current task. Don't browse unrelated external data.
- For database MCPs, use the narrowest approved connection and read-only access, unless you approve a specific write.

## Working In A Worktree

A worktree is a second checkout of the same repo in its own folder, on its own
branch. Use it to keep a task's edits separate from your current checkout.

1. **Install the helper once.** Run this in your terminal:

   ```zsh
   npx skills add devarfeen/agent-skills-kit -g --skill using-git-worktrees
   ```

   In a generated workspace, re-run `/agents-md` and review the proposed
   update so other task skills follow the worktree rules too.
2. **Ask for the task in a worktree.** Type the command below in your coding
   agent. Replace `42` and `SHOP` with your ticket and PROJECT-CODE.
3. **Check the setup report.** It names the checkout, branch, starting commit,
   and baseline checks: the tests run before your changes. This lets you
   distinguish existing failures from failures caused by the task.
4. **Build, test, and ship from that checkout.** Use the shipping choices below
   so the reviewed code and the delivered code come from the same place.
5. **Request cleanup after integration is verified.** A push alone does not
   prove the changes were merged or that local files are safe to delete.

Example task command:

```text
/using-git-worktrees Implement ticket 42 in SHOP in a worktree.
```

You start this setup before the task skill, including Matt's `/implement`,
`/diagnosing-bugs`, `/prototype`, or `/code-review`. When setup finishes, it
goes back to the task you asked for without asking for the same permission
again. To set up the worktree only, run `/using-git-worktrees` on its own. It
prepares the checkout and stops there.

`/orchestrate-t3` and `/factory run` may run this setup step automatically, but
only when you started them explicitly. Every other workflow needs you to run
`/using-git-worktrees` directly.

Asking to "create a branch in the current checkout" just creates a branch. If
you only say "isolate this," the agent asks which one you mean before it edits
anything. Setting up a worktree does not give permission to ship, merge, or
clean up.

### Example: fix checkout in SHOP

Suppose SHOP's repository is `/projects/shop`. The task runs in:

```text
/projects/shop/                         original checkout
  .gitignore                           contains /.worktrees/
  .worktrees/
    fix-checkout/                      task checkout, branch fix-checkout
```

1. **Prepare.** The skill looks at the source branch, existing changes, and
   existing worktrees. It reuses a suitable worktree that belongs to this task,
   or creates one at the path above. If that path has a `prunable` entry, or
   one that is registered but missing, it does not reuse it and reports it
   instead. Pruning is cleanup, not setup. It uses the base you asked for. With
   no base named and no other convention, it records the source checkout's
   current `HEAD` as the new branch's base. Uncommitted edits in the source
   checkout stay there; they are not copied into the task.
2. **Ignore.** It adds `/.worktrees/` to the owning repo's `.gitignore` and
   checks that the destination is ignored before creating or reusing it. Other
   ignore rules are kept. It adds the same entry in the task checkout if it is
   missing, so the entry can ship on the task branch. Setup commits neither
   edit.
3. **Check and work.** It checks the destination, branch, and commit, then runs
   project setup and baseline checks there. Before a baseline that starts
   services, it checks for clashes with the source checkout, such as fixed
   ports or a shared local database that migrations would change. It uses the
   project's documented override, or reports a blocker if there is none. Then
   it runs your task in that checkout. If setup fails, no task edits happen.
   If the baseline fails, you decide whether to go on, unless you already
   approved those specific failures.

Before the task writes anything, the skill reports the checkout path,
repository, branch, starting commit, and baseline result. It passes this record
to task skills and workers. They check again that they are in the right
checkout before their first write, and after handoffs, restarts, or checkout
changes. Every task command sets its working directory explicitly. File edits
use absolute paths inside that checkout, with symlinks resolved. A mismatch
blocks writes until it is fixed. This is a rule the agent follows; it does not
install a write blocker in the harness.

In a generated multi-project workspace, keep the main session at the workspace
root. Give task commands or assigned workers the verified worktree path and the
instructions that apply. Check that containers and test runners really use that
path. If a worktree already exists, don't create another one inside it.

If API and WEB both need changes, use `<api-repo>/.worktrees/<task-name>` and
`<web-repo>/.worktrees/<task-name>`. Each repo owns its own branch, ignore
entry, checks, and shipping. There is no shared worktree for the whole
workspace.

### Example prompts: several repos

A smoke test across two repos, with no push or PR:

> In SHOP-WEB and ADMIN-WEB, each in its own worktree under `.worktrees/`, add
> or update a file `dummy-worktree-smoke.txt` with the project name and today's
> date. Use separate branches, commit in each repo, then merge both into our
> usual local integration branch. Don't push or open a PR — just show me it
> worked.

A version bump across every workspace project, run in parallel by herdr
workers on different CLIs:

> In all projects under the global workspace, each in its own worktree with
> `/using-git-worktrees`, bump the version to the next version, 1.1.6. Give me
> a before/after table per project. Use separate branches, commit in each repo,
> then merge all into our usual local integration branch. Use
> `/orchestrate-herdr` as the parallel harness with Codex (`cxd`), Claude
> (`ccd`), and Antigravity (`agd`) via their aliases.

Each repo still gets its own `.worktrees/<task-name>` and branch. These prompts
name the commit and the merge, so they give permission for both. Pushing, PRs,
and cleanup are still separate requests. The `cxd`, `ccd`, and `agd` aliases are
examples; use whatever shell aliases start your CLIs.

### Ship from the same worktree

After the fix passes its checks, pick the result you want:

| Skill | What it does | What is left for you |
| :--- | :--- | :--- |
| `/commit-push-pr` | Commits and pushes `fix-checkout`, then opens or updates its PR against an allowed base branch | Review and merge. A PR into the default branch with `Closes #42` closes the issue when merged. If you ask for the merge in the same request, a PR into `local` is merged for you. PRs into any other allowed base stay open. |
| `/commit-push-close` | Commits and pushes `fix-checkout`, posts QA instructions, and closes issue 42 directly | The branch may still be unmerged. When it isn't the default branch, the skill confirms whether you want direct closure or a PR. |

For a task branch like this one, prefer `/commit-push-pr`. Both skills keep
their usual checks: you approve the draft, and verification must pass. They run
inside the task worktree, include the scoped ignore rule in the diff you
review, and leave unrelated source edits alone. Neither copies the fix back to
the original checkout or removes the worktree. A merge into `local` happens
only when you or the workspace instructions requested it, as described in the table. Any setup edit made
only in the source checkout is reported.

Both skills follow one shared ship policy:

- **Every QA handoff** has a `Before:` / `After:` pair for the changed behavior
  and a **Merge danger** block. The block has two lines. `Door:` is two-way
  when a revert restores both behavior and data, and one-way when it does not.
  `Blast radius:` comes with the check that supports it.
- **Existing commits ship as they are.** This covers a worktree task branch, or
  the integration branch `/implement-spec` builds. Every commit message is
  scanned first for attribution and credential shapes.
- **Bug fixes** carry a `Root cause:` line in the commit. Leftover debug code
  (`[DEBUG-…]` tags, stray debug prints) stops the commit.
- **Secrets scan.** Before committing, the skill scans the staged diff and every
  PR/issue draft for values that look like credentials: private-key blocks,
  `ghp_` / `github_pat_` / `sk-` / `AKIA` tokens, and URLs with embedded
  passwords. On a hit it stops and names the path and line, never the value.
- **No force-push.** It never force-pushes or rewrites pushed history. A
  rejected push goes to `Needs user:`.
- **Commit format.** When the repo enforces a commit format (commit-msg hook,
  commitlint, `CONTRIBUTING`, or consistent recent subjects), the issue title
  is wrapped in it, for example `fix(checkout): <issue title>`.
- **`/commit-push-pr` extras.** It fits its body into the repo's PR template
  when there is one, keeping the target-required issue reference first. It reads back the PR's
  `mergeable` state and hands `CONFLICTING` to you. If looking up the PR fails,
  it stops; it never treats that as "no PR yet".

### Clean up after integration

Once the PR is merged and you have verified the integrated fix, ask:

> The PR is merged. Check that everything is preserved, then clean up its
> worktree and local branch.

Before anything is removed, check that:

- no task process or worker still uses the checkout;
- tracked changes and useful untracked **and ignored** files are inspected, and
  anything needed is saved outside the worktree;
- all task work is in the integration target. A pushed branch or a closed issue
  alone is not enough.

Then, from outside the worktree, remove the checkout through Git. For this
example:

```zsh
git -C /projects/shop worktree remove .worktrees/fix-checkout
```

Only after that succeeds, delete the local task branch if it is safe:

```zsh
git -C /projects/shop branch -d fix-checkout
```

If Git refuses either step, find and fix the reason. Do not force the deletion.
After a squash merge, Git may not recognize that the branch was merged, so
check the merged result instead of assuming the branch can go. Keep
`/.worktrees/` in `.gitignore` for future tasks, and keep any unrelated source
changes. Deleting the remote branch is a separate choice and not part of these
commands.

The setup and shipping skills don't do this cleanup. Worktrees you asked for
stay until you approve cleanup. Temporary worker worktrees may be removed
inside an integration workflow you already approved, after the same
preservation checks.

## Choosing A Starting Point

| Situation | Start With | Why |
| :--- | :--- | :--- |
| New Workspace | `/agents-md` | Sets up the Project Matrix, paths, and Non-negotiable rules. |
| Work Requested In A Worktree | `/using-git-worktrees`, then the requested task | Sets up the project's own checkout before task edits, then goes back to the workflow you approved. |
| Unsure Which Kit Skill Fits | `/ask-kit` | Names the one kit skill for your situation. Once a spec, ticket, or PR exists, `/factory` takes over. |
| Unsure Which Matt Skill Fits | `/ask-matt` | Points you to an upstream skill flow you start yourself. It doesn't chain skills. |
| Unclear Behavior | `/feature-discovery` | Read-only, code-first audit before planning. ADR findings get their own section. It offers a git history scan only if a "why" or "when" question is left. |
| Rough Idea, No Fog | `/feature-prompt` | You already know where you're going and what to decide. It drafts the prompt, inferring what it can first. |
| Rough Idea, Decisions Unresolved | `/wayfinder` | Open decisions ("fog") block the scope. It charts them as tracker tickets; you resolve one per session. |
| Broken Behavior | `/diagnosing-bugs` | Finds the root cause step by step. |
| Design Spike | `/prototype` | Tries out UI or state ideas before spec and tickets. |
| Issue Work | `/implement` or `/tdd-loop` | Test-first implementation. See the notes below. |
| Whole Spec In One Run | `/implement-spec` | You start it. Builds every ticket onto one local integration branch and stops after `/code-review` and local adversarial `/risk-review`. See the notes below. |
| Porting A Feature | `/port-feature` | Traces a reference feature into a target stack as a gap map. |
| Project Needs A UI Library | `/design-system` | Turns a design system into tokens, components, and a preview you can check. |
| Page Must Match Design | `/pixel-audit` | Strict per-page visual check. Every element must pass. |
| Cosmetic QA Tail | `/polish-batch` | Collects small copy/spacing/alignment nits, then fixes them in one pass. |
| PR Review Comments | `/pr-feedback` | Sorts reviewer threads, fixes what you accept, and replies with the fixing SHAs. It stops after the local fixes and asks you to run `/commit-push-pr`, then answers the threads. |
| Staging Broken | `/staging-fix` | Fixes locally with a test, then ships an auto-merge PR to the confirmed staging branch (default `staging`). Never touches the server. |
| Promote Local To Staging | `/local-to-staging` | One `local` → `staging` PR per project, merged when checks are green. The Actions runs on each merge commit decide success. |
| Ready For Production? | `/staging-to-production` | Read-only readiness check per project, plus the exact commands you run. It never opens or merges anything. |
| Multi-Project Spec | `/integration-contract` | Maps where the repos connect (the seam) and smoke-tests it before shipping. |
| Greenfield Build | `/wayfinder` | There's no code to discover, so chart the destination and its decisions first. |
| Delegable Reading Legwork | `/research` | A background agent reads primary sources into a Markdown doc with citations. |
| Spec With Many Sub-issues, Inside herdr | `/orchestrate-herdr` | One worker tab per open sub-issue. A sub-issue blocked by another open one waits for it. Workers report a fixed `Status:` line. |
| Many Issues, T3 Code Connected | `/orchestrate-t3` | One T3 Code thread per group of issues. See the notes below. |
| Incident Or Outage | `/incident-triage` | Read-only timeline and ranked causes from the evidence you paste. |
| Session Pause | `/handoff` | Writes a continuation doc for the next agent. |
| Session Went Sideways | `/retro` | You start it. It looks back over the session and proposes environment changes (checks, coding standards, steering files), never code changes. Run it before clearing context. |

Notes on three rows:

- **`/implement` or `/tdd-loop`.** `/implement` is optional. It drives one
  ticket and calls `/tdd-loop` at each seam (the place in the code where a test
  can reach the behavior). Without it, run `/tdd-loop` yourself. `/tdd-loop` is
  the kit's own procedure, with its checks, completion evidence, and exception
  rules, and it works alone. Matt's `/tdd` is the reference for test quality.
  It is never a loop on its own.
- **`/implement-spec`.** It reads the tickets as a task graph (which ticket
  depends on which). It runs implementer subagents in worktrees on every ticket
  that is ready, and merges them onto one local integration branch. It stops
  after `/code-review` and local adversarial `/risk-review`. The ship skills push, open the PR, and close tickets.
- **`/orchestrate-t3`.** Each group gets its own execution worktree under
  `.worktrees/`. Workspace policy decides which thread each worker is bound to.
  Issues that block one another or touch the same area share a group. It needs
  the T3 Code MCP server signed in with more than read-only access.

## Skill Groups

`npx skills` lists the kit's skills under seven headings: Workspace Setup, Discover Plan, Build, Visual Design, Ship, Staging Promotion, and Factory Workflow. The first six cover the path you drive by hand, shown below. Factory Workflow covers what happens after a PR opens. The groups only organize the picker. A skill's phase is still set by where it sits in [Core Progression](#core-progression). To see which skill is in which group, check the [README](README.md#skill-groups).

## Core Progression

Use this sequence when you are driving a feature one step at a time. Type
slash commands in your coding agent; run `npx` installation commands in your
terminal. Replace example project codes, issue numbers, and paths with yours.
Install any companion you choose before using it; the
[install commands](README.md#companion-install-commands-global) list its source.

If you already have a spec, ticket, or PR, run `/factory 87` with that reference
to find the next unfinished step. You do not need to repeat setup or planning.

| Step | What you do | Why and when you can move on |
| :--- | :--- | :--- |
| 1. Set up the workspace once | Follow [First-Time Setup](#first-time-setup): `/agents-md`, `/setup-matt-pocock-skills`, fill the paths, then `/design-system` for UI projects. | Agents need the correct project rules, tracker, and design library before they work. |
| 2. Understand the existing behavior | `/feature-discovery Trace checkout in SHOP` | Use the code report to decide what must change. Skip discovery for a new project with no code. |
| 3. Clarify the request | `/feature-prompt Add checkout approvals in SHOP`, then `/grill-with-docs` on the saved prompt. If decisions prevent you from defining the scope, use `/wayfinder` first. | Resolve open questions and save the decisions before implementation starts. |
| 4. Record the agreed requirements | `/to-spec` on the agreed plan or ADR. | A spec issue gives everyone the same acceptance criteria: the conditions the result must meet. |
| 5. Split the work | `/to-tickets` on the spec issue. | Each ticket should be testable on its own and say which other tickets must finish first. |
| 6. Build one ready ticket | `/tdd-loop` on the ticket, optionally through `/implement`. | Choose a suitable existing solution, observe a failing behavior test, then make it pass and run wider checks. Use the skill's exception procedure when a test is impractical. |
| 7. Review and check locally | `/code-review`; `/pixel-audit` for design matching; `/integration-contract` for changes across projects. | Fix review findings and verify acceptance criteria with tests and local browser checks where needed. Complete required agent QA before handing screens to a human tester; collect cosmetic fixes with `/polish-batch`. |
| 8. Publish for review | `/commit-push-pr` after the local checks pass. | The PR carries the issue link, test evidence, and testing instructions. For direct issue closure without a PR, choose `/commit-push-close` deliberately. |
| 9. Complete PR checks | `/factory 87` tells you what is next: failing CI, app QA, reviewer feedback, or risk review. Run the suggested skill, then check again. | Only evidence for the latest commit counts. A new push needs fresh checks. Follow [Factory Workflow](#factory-workflow) through staging and the owner handoff. |
| 10. Summarize delivered work | `/release-notes` for the completed range or period. | Give testers and other readers a summary based on actual changes, including any action they must take. |

**When scope is unclear.** You are ready for `/feature-prompt` when you can
state the outcome and list the decisions still to make. Use `/wayfinder` when
you cannot yet do that. It records those decisions as tracker tickets and
resolves one per session. Both routes meet at `/to-spec`.

Size alone does not decide the route. A large mechanical refactor may have
clear requirements; a two-file change may depend on an unresolved design
decision. A new project with no code to inspect can start at `/wayfinder`.

Variations on this path:

- **Worktree requests.** Run `/using-git-worktrees` explicitly before the task skill, or let a `/orchestrate-t3` or `/factory run` that you started set up the checkout. This applies to planning or implementation work when you explicitly ask for a worktree. It adds no default step to the path. See [Working in a worktree](#working-in-a-worktree).
- **Implementing** a ticket uses `/implement` when it is installed. It drives `/tdd-loop` at each seam agreed in advance, and `/tdd` guides test quality and seam choice. Without `/implement`, run `/tdd-loop` directly. `/implement` stops after `/code-review` and local adversarial `/risk-review` and never commits.
- **Whole-spec builds** can use `/implement-spec` instead of one `/implement` per ticket. You start it. It treats the tickets as a task graph, runs implementer subagents in their own worktrees on every ticket that is ready, and merges each onto one local integration branch. It ends with one `/code-review`, then local adversarial `/risk-review` over the combined branch, owned by the coordinator. In a kit workspace its implementers drive `/tdd-loop`, and it stops there. Its own instructions include opening a draft PR and resolving tickets, but in a kit workspace pushing, PRs, and closing issues belong to the ship skills. Inside herdr, `/orchestrate-herdr` does the same fan-out with one visible worker tab per sub-issue.
- **PR bodies** belong to `/commit-push-pr`, which sets its own body and QA comment. Matt's `/pr` loads automatically whenever a PR body is written. Its three ideas are built into the kit's body: a visual summary (the optional Summary visual), before/after evidence (the **Evidence** section), and a merge-danger call (the **Merge danger** section). When both are installed, the ship skill's headings, order, and the target-required issue reference win. `/pr` only shapes the visual and the wording inside them.
- **Retro** comes last. After shipping, especially after a session that went badly, `/retro` looks back and proposes changes to the agent's environment. A mechanical mistake becomes an automatic check (lint rule, pre-commit hook, CI job). A judgment call becomes a coding standard that `/code-review` enforces. It proposes; you decide what to apply.
- **Porting** a feature from a reference implementation starts with `/port-feature` instead of `/feature-discovery` → `/feature-prompt`. It writes a gap map and hands off to `/grill-with-docs`.
- **Verify** is a group of skills, not one:
  - `/agentic-qa` for functional QA of any change that can show up on a screen,
  - `/pixel-audit` for per-page visual conformance,
  - manual QA plus `/polish-batch` for the cosmetic tail,
  - `/integration-contract` when the spec spans more than one PROJECT-CODE.

  After a UI slice ships, `/design-system` (extend) folds any new reusable UI back into the library.

### Choose the smallest complete implementation

Run `/tdd-loop` for your ticket or local fix. Before adding code, it checks
these options in order and chooses the first one that meets every acceptance
criterion and project convention:

| Check next | Choose it when |
| :--- | :--- |
| Existing project helper or component | It already provides the required behavior and fits the project. An established house component takes precedence over a native substitute. |
| Standard-library or platform feature | No project solution fits, and the built-in feature meets the whole requirement. |
| Installed dependency | The earlier options do not fit, and an existing dependency does. |
| New code | None of those options fits. Add only the missing behavior; avoid a new dependency for a few clear lines. |

Keep validation, error handling, security, and accessibility. Existing helper
tests do not prove that a new caller uses the helper correctly: the changed
behavior still goes through the usual failing test, passing fix, and wider
checks. A declared exception keeps its named verification and follow-up plan.
Refactor only while tests pass. The kit supplies these rules directly; you
do not need to install Ponytail.

## Factory Workflow

The factory skills (the `factory-workflow` group in `npx skills`) handle what happens after a PR opens. `/factory` works out where each ticket or PR stands from the tracker, the PR, CI, review comments, and deploy runs. Then it names the one skill that moves it forward. In its output, each ticket or PR is a "unit".

Plain `/factory` keeps no state file. Run mode saves checkpoints so a run can recover after an interruption.

The report is a table. Its `Since` column shows when the signal that placed each unit happened. Healthy units are listed oldest first. A unit stuck in one state for more than 3 days is flagged `stalled`.

### Three ways to move a PR along

You can work a PR in three ways. Mix them freely.

**1. Ask where it stands: `/factory <pr>`.** Give it the PR number or link. It looks at the PR and tells you which step is next. It changes nothing, so you can run it as often as you like.

```text
/factory 87
/factory https://github.com/acme/shop/pull/87
```

You can also give it the ticket (`/factory PRWL-142`), and it finds the PR for you, or a whole spec (`/factory PRWL-100`) to see every ticket at once. It does not guess from the branch you are on. With nothing after `/factory`, it asks.

**2. Run the next step yourself: `/ci-loop 87`, `/agentic-qa 87`, and so on.** Every skill in the table below works on its own. You do not need `/factory` first. If you can already see that CI is red, run `/ci-loop 87` straight away.

**3. Hand it over: `/factory run 87`.** The factory runs each step for you, one after another, and stops when the PR is ready for the owner on staging. It asks you one thing first, which agent should review the code. It works from the PR's linked issue. If that issue isn't labeled properly, it stops and tells you to run `/triage`.

**Which one to use:**

| Your situation | Do this |
| :--- | :--- |
| You know the next step (for example, CI is red) | Run that skill: `/ci-loop 87` |
| You don't know what's next, you just pushed, or you're coming back to an old PR | `/factory 87` |
| You keep running `/factory` after every step anyway | `/factory run 87` |

A typical hand-driven PR looks like this:

```text
/commit-push-pr     PR #87 opens
/ci-loop 87         you saw CI go red; it fixes and pushes
/factory 87         says: next is /agentic-qa 87
/agentic-qa 87
/factory 87         says: next is /risk-review 87
/risk-review 87
```

**You choose whether to automate.** In the manual workflow, the agent suggests
the next skill and waits for you to start it. These steps can push commits,
comment on PRs, or merge. An explicit `/factory run` authorizes the documented
sequence, including its stage skills, within their stated limits. Required
human decisions still stop the run. Asking "where is PR 87?" only requests a
report.

### Which skill for which state

The flow below uses the state names `/factory` prints:

```text
BUILDING -> CI -> QA -> REVIEW -> risk gate --low--> MERGE -> STAGING -> READY_FOR_OWNER
   ^         |     |                  |                          |
   |    /ci-loop  findings          high                    deploy fails
   +-- /tdd-loop --+                   v                          v
                                 HUMAN_REVIEW                /staging-fix

human QA finds a bug later -> QA_RETURNED -> /qa-escape -> BUILDING
```

| State | Run |
| :--- | :--- |
| CI red on the PR | `/ci-loop <pr>` |
| CI green, change can reach a screen | `/agentic-qa <pr>` |
| QA or a reporter found a new problem | `/report-issue <problem> [screenshots]` |
| Human QA found a bug after done | `/qa-escape <issue>` |
| CI green and QA passed, not yet reviewed | `/risk-review <pr>` |
| Merged to `staging` | `/deploy-watch <pr>` |
| Something is on fire | `/incident-triage` |

What each one does:

- **`/ci-loop`** makes up to 3 fix-and-push attempts, all under one approval. It never edits tests or workflows to make CI pass. A flaky failure in code the PR added is fixed like any other code failure (wait on the real condition), not retried. If something "passes locally", it compares the CI and local environments first. If the PR's latest commit is one it didn't push, it stops and reports `head moved`.
- **`/agentic-qa`** tests the running app across a grid: state × screen size (viewport) × user role, plus keyboard-only. Browser console and network errors are part of the check too. A cell fails only after one exact replay. Anything the test saves must still be there after a reload. It reports findings and never edits code.
- **`/report-issue`** creates one issue from a template, with acceptance criteria, code leads, labels, priority, cycle and due date, after you approve its draft. A bug on work already delivered goes to `/qa-escape` instead.
- **`/qa-escape`** reproduces the bug. It also runs the reproduction once on the PR's base commit, so a bug that was already there is classed `not-a-regression`. It records the escape class (what kind of miss it was) on the issue. It names the regression test to write first, with its proof: the test fails at the tested commit and passes at base.
- **`/risk-review`** looks at the change through specialist lenses, then gives a risk tier from a fixed rubric. A low tier offers auto-merge; a high tier asks for an engineer. It checks the author's `Door:` claim against the diff. A one-way door, or a `two-way` claim the diff contradicts, is high. Requested changes or an unresolved review thread block any merge, whatever the tier. A lens that fails counts as `not assessed`, never as low risk.
- **`/deploy-watch`** watches the deploy run for up to 2× its usual time, then calls it `unverified`. With your approval, it smoke-checks staging against a baseline of the errors staging already shows, and records pass or fail. A 200 response without a build identifier is `build unconfirmed`.
- **`/incident-triage`** is read-only. It builds a timeline with gaps marked, ranks causes (at least one that isn't a recent change), lists mitigations for the owner to run, and adds a `## Resolution` section once resolved. Signs of a breach go to the owner's security process at once.

### Audit corrections to existing workflows

- **Worker completion:** T3 checks the project selected by workspace binding.
  Herdr requires passing tests for code tasks and assigned evidence for
  non-code tasks. Local commits follow workspace shipping policy; a worker
  without that permission returns verified uncommitted changes.
- **QA and feedback:** Design-system previews wait for any workspace-required
  agent QA before human inspection. Pixel-audit suggests shipping only verified
  changed rows. QA testers use owner-prepared fixtures. `/qa-escape` accepts a
  directly closed delivery when its handoff supplies the delivered commit and
  an evidenced baseline; missing identity remains unresolved.
- **Tracker and shipping:** `/report-issue` posts an approved evidence comment
  on an open duplicate without creating another issue or changing its fields.
  `/pr-feedback` can answer an approved already-fixed concern after verifying
  the existing fix on the current PR head. Shipping verifies env parity and
  hooks; implementation repairs happen before restarting the ship workflow.
  A failed promotion check goes to `/ci-loop` only when its head is eligible;
  default/deployment branches need a permitted task-branch repair.

Recovery menus offer up to three feasible options without unavailable filler.
A settled seam choice is evidence, not an open question. `/port-feature` ends
at its advisory suggestions, including the optional prototype suggestion.

### Review local implementations adversarially

Use `/risk-review local` to challenge a local implementation before opening a
PR. Supply its requirements, checkout, base commit and changes to review.
Generated workspace rules call this mode automatically after `/code-review`
in `/implement` and `/implement-spec`; update the kit and rerun `/agents-md`
to install the v54 routing rules. Matt’s installed skills stay unchanged.

| Use | What happens |
| :--- | :--- |
| Local implementation | Five independent reviewers challenge requirements, correctness, tests, integration, and security/data. Small nonbehavioral changes use only relevant reviewers. A separate judge checks the evidence. |
| Whole spec | The coordinator reviews the combined integration branch; individual implementers do not each launch five reviewers. |
| Open PR | `/risk-review 87` retains its green-check prerequisite, fixed risk rubric and approval before remote writes. Factory explicitly selects PR mode at its RISK stage. |

Reviewers can report no supported findings. The judge records confirmed,
rejected, unresolved and advisory claims with reasons. Missing evidence or a
failed required reviewer is not a pass. A proposed test is never described as
an executed failure. Local review pins uncommitted changes as well as commits;
changed inputs invalidate its verdict.

The builder fixes confirmed in-scope defects and rechecks within three review
rounds. Factory uses its existing round budget and retains its narrowly
verified fix-only exception. Advisory notes alone do not block completion.
Local review returns a report; it cannot publish, assign a merge-risk tier,
replace CI/QA, or satisfy the later PR risk gate. Existing commit and shipping
limits remain in force.

### Read risk-review simplification notes

Run `/risk-review 87` as usual. Its verdict may include a
`Simplification (advisory)` section with up to three opportunities found in
the changed code and relevant callers. Each note names the current
`file:line`, evidence that the code is unnecessary, a concrete maintenance
cost, and the smallest alternative with its helper path or API.

These notes do not change the tier, blocking count, verdict marker, or merge
conditions. A new dependency still triggers high risk even if a note suggests
removing it. A proven bug remains a risk finding with a failure scenario and
a proving test. A required abstraction or a function used through dynamic
registration is not unnecessary just because it has one implementation or
no direct caller.

If you choose to apply a note, make a scoped change through the normal coding
and verification flow. The review itself grants no permission to edit code or
publish. It does not start an extra review lane or a whole-repo cleanup audit.

### What counts as proof

A step passes only on evidence the skills leave on the PR. Each skill posts
its own comment for this, called a marker. The evidence is:

- a green CI run for the PR's latest commit (the head SHA),
- an `agentic-qa` marker and a `risk-review` marker for that same commit,
- a `deploy-watch` marker for the merge commit.

Every factory step that runs or changes code works in its own worktree under the owning repo's `.worktrees/` (`pr-<n>` for a PR, `qa-escape-<issue>` for an escape). It reports which checkout it is in first. Read-only steps never create one.

`/factory` stops at `READY_FOR_OWNER`. Promoting to production and rolling out feature flags stay with the owner. No factory skill ever accesses production. `/staging-to-production` prepares the owner's promotion, read-only.

### Run mode

Start a run with `/factory run <issue or label>`:

```text
/factory run PRWL-127
/factory run automate
```

A label runs every open issue that carries it. The factory then follows its own advice.

- **Reviewer.** It asks which agent and model should review the code, but only if you haven't said already.
- **Builder.** The builder is the harness, provider, and model you started the run in, unless you explicitly choose others.

The run keeps these choices if it has to recover from an interruption, and it continues approved work by itself. It can still park a unit (stop working on it and say why) when a real human decision is needed, when it lacks access, or when it has used up its recovery attempts.

For each issue it:

1. sets the issue to In Progress. If acceptance criteria are missing, it posts them as a comment. It never edits the issue itself.
2. creates separate BASE and HEAD worktrees, each with its own runtime. BASE is the code before the change; HEAD is the code with it. It prepares any infrastructure needed, and practices restoring any test data the run will change.
3. gives the builder an exact brief: what the component must do, which tests to write, and which docs to update. Then it builds through the chosen local executor, on the verified checkout and runtime.
4. runs `/agentic-qa`. While QA runs, it drafts the PR text privately and prepares neutral inputs for the reviewer. It opens the PR only after QA on that same code and the local checks pass, then drives CI.
5. has the second agent review the code and post its findings on the issue. The builder fixes or declines each finding, for up to three rounds.
6. runs `/risk-review`. For a low tier, it merges into `local` or the staging branch through GitHub.
7. posts the handover comment and sets the issue to In Review. Once test-data restore, evidence publishing, and merging have all passed, it cleans up the task's runtimes, evidence, and worktrees, and checks the cleanup worked.
8. promotes `local` to staging with `/local-to-staging` for the repos it merged into, then runs `/deploy-watch`. A failed deploy gets one `/staging-fix`, and that fix's PR goes through the same checks.
9. ends with a read-only `/staging-to-production` readiness report. You run the production commands yourself.

You can still run these ship skills yourself. Inside a run they skip their usual approval prompt, because starting the run already approved them.

**Several issues.** Ready, independent units may run at the same time, up to what the runtime can handle, as long as each has its own checkout, data, and browser session. A unit that depends on another waits until that one is verified done. The main session integrates finished work one unit at a time. The run keeps issue priority, and later workers get the relevant lessons from earlier work.

**When it parks.** The run parks an issue and moves to the next one when a person is needed: a high risk tier, three failed rounds, a problem it cannot reproduce, or a fact only the reporter knows. It never closes an issue, never edits a tracked compose file, and never goes past staging. Plain `/factory` stays read-only.

**The run label.** If you started the run with a label, it removes that label from each issue at handover, and from any issue where it found nothing to build. Parked and `needs-info` issues keep the label, so the next run looks at them again. To send a delivered issue back, add the label again, reopen the issue, or run `/factory run <issue>` on it.

**Manual QA starts on staging.** The run doesn't assign anyone. When `/local-to-staging` or `/deploy-watch` sees the change deployed on staging, it assigns the issue to the manual QA person and says which build to test. That person is the one your issue-tracker document names, or else the issue's reporter. The status stays In Review. The tester closes the issue.

**What a run learns.** Each check round (a QA result, a CI attempt, a risk review, a code review) is logged as one row in `specs/factory/rounds.md`: what failed, the cause, and what the worker tried. When the same cause shows up in three issues of one project, the run writes a one-line instruction into `specs/factory/lessons.md`. It pastes that project's lessons into every later worker prompt, in this run and the next. It doesn't ask first. The run report lists each line it added, and you can edit or delete any of them.

A lesson only changes how a worker works. It never changes a criterion, a test, a required check, or a cap. A fix that deletes a test or removes an assertion parks the issue. Neither file is state: `/factory` still places every issue from the tracker and the PR alone.

**Issues QA sent back.** When a person reopens an issue or reports a problem on shipped work, the run doesn't hand it straight back to you. It runs `/qa-escape` first: it reproduces the problem, records why the agent's checks missed it, and posts that on the issue. Then it rebuilds, starting with a failing test for that exact problem, and takes the fix through the usual checks.

Three cases still come back to you: the problem can't be reproduced, it existed before the change, or the fix just wasn't on the environment QA tested. In that last case the run builds nothing and promotes the fix to staging. Approving a durable guard (a lasting safeguard against that kind of miss) also stays with you.

**Screenshots.** After every QA round, the run puts that round's before and after screenshots on the issue. On Linear it attaches the images. On GitHub it posts a comment listing the local file paths, because `gh` cannot attach an image; drag them in yourself if you want them there. Images are never sent anywhere except the issue's own tracker.

### Inside a run

You don't need this part to use run mode. It explains what the run does behind the scenes, so you can read its reports.

**One runtime per issue.** Each issue gets its own running copy of the app, set up through the workspace task adapter or the project's supported runtime descriptor.

- BASE and HEAD each have their own runtime state, output files, test data, and browser sessions. Shared infrastructure may hold each task's private data.
- Before handing work to a worker, the run proves the worker has the right checkout and that the app is ready. It checks HEAD again before QA.
- Services starting, or a URL answering over HTTP, does not by itself prove the app is ready.
- If the app isn't ready, fixing it stays with whoever owns the runtime. It never becomes a reason for QA to fall back to a different browser tool.

**Builder brief and optional intake.** Before building, the main session works out exactly how the component should behave, which paths must be kept, which equivalent approaches are allowed, and which tests and docs are needed. Context from the reporter helps, but optional template fields stay optional. The builder confirms it has read the brief and returns evidence for each item. If the reporter left details out, the builder may not invent scope to fill the gap.

**Test data before QA.** QA often needs specific data (fixtures). Whoever owns the runtime:

1. saves the original state privately,
2. sets up predictable test data,
3. restores the original state and measures it, to prove the restore works,
4. sets up the test data again for QA.

The saved state includes related rows, timestamps, binary values encoded without loss, and counters the fixture changes. After QA, the owner stops anything that writes, restores the same snapshot, and measures it again. If the restore is incomplete, the runtime and snapshot are kept. Temporary helper files stay out of the app's lint and typo-check scope.

**Drafts during QA, released after checks.** To save time, the run drafts the PR text and the reviewer's inputs while QA is still running. Each draft gets a saved record (a receipt) that ties it to the exact checkout, commit, criteria, policies, and input files it was built from.

- Before shipping uses a draft, it checks the draft still matches that record.
- If the source changed, the affected draft is thrown out.
- Independent review still waits until QA and CI pass on the PR's latest commit.
- The time this overlap saves is measured separately from the run's total time.

**Cleanup is checked, not assumed.**

- Before deleting local evidence, the run reads back the uploaded evidence files and the QA comment to confirm they arrived intact.
- The adapter lists the files the task owns. It records "may be deleted" and "was actually deleted" separately.
- An optional copy of env files on the host is removed only with a record showing the task created it (an ownership receipt).
- Files that existed before, or that changed, are protected. An old folder with no ownership receipt is kept and named in the report.
- Only worktrees that are merged, clean, and not needed by any running process are removed, and never with force.
- Deleting a branch still needs its own ownership and permission checks.

**Who did the review and QA.** Where workspace policy allows these fields, review and QA comments name the worker's host harness, coding agent, provider, and requested model, taken from launch and run records. If the model actually used can't be determined, the comment says so. Ordinary docs, commits, and PR bodies still carry zero attribution.

**Waiting and recovery.** The run's status tells you whether you need to act:

| Status | What it means | Do you need to act? |
| :--- | :--- | :--- |
| `WAITING_WORKERS` | A worker or check is still running. It names the owner and the next automatic action. | No (`Needs user: None`). It does not ask you to paste a continuation prompt. |
| `WAITING_RUNTIME` | The app's runtime is being prepared or repaired. It names the owner and the next automatic action. | No (`Needs user: None`). It does not ask you to paste a continuation prompt. |
| `WAITING_COMPACTION` | The run is about to shrink its context (compaction). It pauses only after its maintenance and continuation requests are saved. | No. |
| A real blocker | It explains what failed, what recovery it tried, and three reasoned recovery choices. If a choice isn't available, it says so instead of inventing one. | Yes. |

You get a recovery prompt to paste only when a person is truly needed, or after an interruption. Resuming keeps the same builder, reviewer, checkout ownership, and remaining attempt budgets. If you explicitly pause or stop a run, it stays stopped until you say to continue. `/orchestrate-t3` uses the same handoff rules.

**Before a run builds.** It checks that these are in place: the chosen executor (the tool that runs workers), the checkout, the project's standard checks, the branch it will deliver to, and a runtime that fits the project. If you asked for T3 only, T3 stays required. Otherwise, an approved native executor is another way to run. Runtime setup uses the project's real stack; not every project needs Compose. If something essential is missing, only the affected units are parked.

**Operating modes.** A run can be hosted in three ways:

- **T3.** T3's installed app can queue a native compaction, followed by a separate request to continue. Automatic worker results may jump ahead of that compaction request, so the queue accepting it does not guarantee it runs before them.
- **Native controller.** Some workspaces provide their own controller. Choose its harness and model explicitly, and resume only by its saved session ID. Its adapters and commands belong to that workspace. Installing this kit does not install a controller script.
- **Checkpoint-assisted observation.** It shows verified recovery steps without restarting a harness.

Inside herdr, the factory's herdr backend runs every builder, reviewer, and QA worker as a visible herdr agent tab. A workspace controller can host the main session the same way, and resume it by its exact session ID after an exit or a server restart. None of these modes sets an OS sleep policy, or guarantees recovery if the host machine is suspended.

**Context use.** The main session checks how full its context window is at each phase change, and before long reads or returns.

- At 60% full, it saves a compact checkpoint and uses the runtime's supported compaction before the next long phase.
- It keeps the existing 25% reserve free, counting results still on their way back.
- Workers return short receipts and full paths to their evidence. Pulling whole histories in again and again still fills the main session.

**Receipts.** A receipt is a short saved record of who owns what, the choices made, attempt counters, and where the evidence is. The run reads these before reloading full histories, comments, or capability lists. It reuses cached source material only after a fresh version check and a complete discovery match the saved scope and file contents. A receipt does not prove a worker is still alive, and it never passes an acceptance check.

**Readable status.** Status shows as separate Markdown fields, with text states and color badges that carry meaning. ANSI color codes are used only in a terminal renderer that supports them.

## Issue Naming And Label Check (Required)

Before an agent creates, edits, or renames any tracker issue, it must pass these
checks. GitHub is the default tracker. If the workspace names another tracker,
that one is used, with the same title patterns.

1. Read the local workspace instructions: `AGENTS.md`, plus `rules/issues.md` for the title patterns and labels.
2. Pick the exact title pattern: `Spec:`, `Ticket NNNN of …`, `Way:`, or the form for implementation work outside a spec. Issues titled `PRD:` date from before the rename to "spec", and `Slice NNNN of …` from before the rename to "ticket". Treat them as spec and ticket issues. Do not retitle them.
3. Pick exactly one category label (`bug` or `enhancement`) and one state label. `/qa-escape` adds a `qa-escape` marker label beside them; it never replaces either one. **This applies to delivery issues only.** `Way:` issues are planning items. They carry only `/wayfinder`'s own labels (`wayfinder:map`, `wayfinder:research` / `prototype` / `grilling` / `task`), get no category or state label, and are closed before `/to-spec` runs.
4. Make sure no issue title contains a routing marker (`HITL:` / `AFK:` / `BLOCKER:`). Wayfinder's HITL/AFK split is a ticket *type*. It is carried by labels, never by the title.

If the tracker's vocabulary isn't set up, stop and run `/setup-matt-pocock-skills` first.
Do not publish issues with guessed title patterns or missing labels.

## Suggested Next Skills Footer (Optional)

So you don't have to remember what comes next, the agent can end longer responses with a short suggestion block:

```markdown
Suggested next skills (optional):
- /skill-name: why this is likely useful now.
```

Guidelines:

- It only recommends. It never blocks a step or starts the next skill.
- Add it after any substantial step, including steps from local and third-party skills.
- Include companion skills or MCPs when they are the best next helper for the current step.
- Keep it short: 1-3 suggestions at most.
- Suggest the step that usually comes next first.
- Before risky edits, put suggestions that gather more evidence first:
  - after discovery of unclear behavior: `/feature-prompt`, `/wayfinder` (if decisions gate the scope), or `/diagnosing-bugs`
  - after prompt drafting: `/grill-with-docs`
  - after a wayfinder ticket resolves: the next frontier ticket, or `/to-spec` when the map is exhausted
  - after ticket slicing: `/implement` (or `/tdd-loop`) for the first ready ticket
  - after implementation completion: `/code-review`, then `/commit-push-pr` or `/commit-push-close`, then `/release-notes`
  - after shipping a session that hit repeated mistakes or long searches: `/retro`
- If confidence is low, suggest one careful next step instead of a long list.

## Context & Native Memory Model

The generated `AGENTS.md` tells agents how to find context. This part loads on every task:

- **Read order:** First `GLOSSARY.md` and `specs/adr/`. These **must be followed**; read them before implementing. Next, the current task context (the active request, issue, or spec). Last, the current CLI's native memory, if it is turned on.
- **North star:** If the workspace or a project keeps a `VISION.md`, the generated `AGENTS.md` makes it the project's north star. Agents read it before planning work. When a plan conflicts with the vision, they point it out; they never quietly resolve it. With no vision file, no north-star section is written or made up.
- **Never bulk-read `specs/`.** Treat it as an archive you pull from when needed. Fetch only what the task names, by search or with a discovery skill. Loading the whole tree clutters the context and wastes tokens.
- **Native memory only.** Do not create memory files, wiki files, or discovery files in the repo. Do not sync memory between CLIs.
- **Archived context when grilling.** When you start `/grill-with-docs`, the agent first asks whether you have archived context for the feature, such as past discussions or the original intent. Paste it, and it is copied word for word into the ADR with a note of where it came from. Or carry on without it. Old or current names it reveals are offered as `GLOSSARY.md` aliases.

You use skills one at a time, as needed. They are not a pipeline. Work moves along a gradient: discover → sharpen → plan → slice → implement → verify → ship. After the workflow you asked for, the agent **suggests** a next skill but never starts a new workflow on its own. Worktree setup may go back to the task already in your request; that handoff does not ask for permission a second time.

## It's Working If

Each skill has one sign you can check without opening its `SKILL.md`. If you don't see it, the skill misfired or stopped early.

| Skill | You should see |
| :--- | :--- |
| `/agents-md` | An `AGENTS.md` and seven `rules/` files, a Project Matrix in `rules/projects.md` with one row per workspace folder, and each file's full diff shown before anything is written. |
| `/ask-kit` | One `Run:` line naming a single skill, and nothing started. |
| `/design-system` | A preview page you can open, and a `specs/design-system/` doc naming the project UI skill. |
| `/feature-discovery` | Every claim cites a file and line; no file in the repo changed. |
| `/port-feature` | One gap-map file under `specs/port/`, and nothing implemented. |
| `/feature-prompt` | A saved prompt file that separates what you said from what it inferred. |
| `/tdd-loop` | An implementation that meets the criteria, with a quoted failing test before the fix and the same test passing, or a declared exception with its verification evidence. Reuse keeps these checks. |
| `/orchestrate-herdr` | One tab per open sub-issue, each ending in a `Status:` line with quoted test output. |
| `/orchestrate-t3` | A group map (issues, worktree, branch, thread) and, for each issue, a `Status:` line with quoted test output. |
| `/using-git-worktrees` | The checkout path, branch, starting commit, and baseline result reported before the first edit. |
| `/pixel-audit` | A defect list where every `verified` row has element-level evidence. |
| `/polish-batch` | Every nit you reported is a row in the punch-list, and nothing was fixed until you said dispatch. |
| `/integration-contract` | A contract file with a gate log, or `single project — no contract needed`. |
| `/agentic-qa` | A grid with no blank cell, and a `VERIFIED`, `PARTIAL`, or `BLOCKED` comment on the PR. |
| `/report-issue` | The created issue's identifier and link, with every field read back equal to the draft you approved. |
| `/qa-escape` | A reproduction with a run count, and a marker comment on the issue naming the escape class. |
| `/ci-loop` | One line per attempt, three at most, ending in green checks or a named stop reason with a quoted log line. |
| `/risk-review` | Local mode: a revision-bound report with independent reviewer coverage and judged findings, no remote writes. PR mode: one marker comment for the PR's latest commit (head SHA) with a tier, and every triggered rule citing `file:line`. Optional simplification notes stay separate from the tier and blocking count. |
| `/commit-push-close` | The issue reads `CLOSED`, with a QA handoff comment that has Before/After and Merge danger. |
| `/commit-push-pr` | A PR whose body starts with the target-required issue reference and includes Evidence and Merge danger, plus a QA comment. |
| `/pr-feedback` | A numbered accept / pushback / needs-discussion list before any edit, then replies citing commit SHAs. |
| `/staging-fix` | A PR against the staging branch with a quoted passing test, and no server command run. |
| `/deploy-watch` | A pass or fail marker comment on the PR naming the deploy run and each smoke check's observed value. |
| `/local-to-staging` | A table with every project and a run URL for each merge commit. |
| `/staging-to-production` | A readiness table and commands printed for you; nothing opened or merged. |
| `/release-notes` | A file under `specs/release-notes/` with QA steps and an "Action needed" line. |
| `/factory` | A table with every unit of the spec, the check it is waiting on, and the one skill that moves each forward. In `run` mode: the same table, plus why any issue was parked, the criteria it drafted, the rounds each issue needed, and any lessons added. |
| `/incident-triage` | A timeline where every line names its source, and at least one cause that is not a recent change. |

The kit has no filed issues yet, so this guide has no "common questions" list. One will be added from real questions, not made-up ones.

## Planned Vs Ad Hoc Issue Flow

Pick the path that fits your work:

- **Planned work:** `/feature-discovery` -> `/feature-prompt` -> `/grill-with-docs` -> `/to-spec` -> `/to-tickets` -> `/implement` (or `/tdd-loop` directly; `/implement-spec` for the whole spec in one run) -> `/code-review` -> local `/risk-review` in Matt flows -> `/commit-push-*`. The spec and ticket issues exist before coding. `/to-spec` and `/to-tickets` add the ready labels in the normal path, so you don't need a separate `/triage` step.
- **Foggy work:** `/wayfinder` -> chart the map -> resolve one ticket per session -> map exhausted -> rejoin planned work at `/to-spec`. The map's `Way:` issues are closed before the spec exists.
- **Existing or incoming issues:** Use `/triage` when an issue needs a state change, follow-up with the reporter, `ready-for-human`, `wontfix`, or an agent brief before implementation.
- **Problems a reporter found:** `/report-issue <problem> [screenshots]` -> one draft -> approved issue -> `/factory run <issue>` when it is `ready-for-agent`, otherwise `/triage`. See [Reporting a problem](#reporting-a-problem).
- **Ad hoc work:** one-line request -> `/diagnosing-bugs` or direct fix -> `/tdd-loop` when useful -> `/commit-push-*`. Do not write up a detailed GitHub issue before coding. The ship skill creates the issue at the end from the original request, final diff, decisions, and validation.

If an ad hoc request grows large, unclear, cross-project, or into several slices, stop and route it through `/feature-prompt` or `/to-tickets` before going on. If the scope turns out to wait on unresolved decisions, route it to `/wayfinder` instead. Use `/triage` only when an issue already exists and its state or labels need fixing.

### Reporting a problem

Use `/report-issue` when you found a problem but don't know the code. This is usually QA. Describe the problem in plain words and add any screenshots:

```text
/report-issue The invoice list shows a blank page for a new tenant. Expected an empty-state message. ~/Pictures/invoices.png
```

What it does:

1. Reads the workspace issue rules and the live tracker templates.
2. Traces the screen, URL, or error text to code in each project that might own it.
3. Searches the tracker for duplicates.
4. Shows you one draft: the title in the workspace format, the main project and every other PROJECT-CODE involved, the template, labels, priority, cycle, and due date, each with a one-line reason.

Reply `yes`, or name the fields to change. It then creates the issue, uploads the screenshots, reads every field back, and returns the link.

**What the draft contains.** It is shaped so `/factory run` can pick it up: one classification label, numbered acceptance criteria in the body, steps or a route to reach the problem, and code leads marked as leads.

- **Workflow label.** The template's workflow label (for example `ready-for-agent`) is kept only when all six agent-ready checks pass. Otherwise the issue gets `needs-triage`, and the triage note names the checks that failed.
- **Defaults.** Priority, cycle, and due-date defaults live in the skill's `references/triage-rules.md`. Workspace issue policy overrides them.
- **Edge cases to check.** The body lists edge cases found in the traced code (roles, empty and error states, validation, edit versus create, other callers), each with its `path:line`. They guide the builder and `/agentic-qa`. They are never acceptance criteria. An edge case that needs a product decision keeps the issue at `needs-triage`.

**Options.**

- Add `repro` to have it try a local reproduction first.
- Put several problems in one message, or add `batch`, to draft up to 10 issues at once. Problems with the same symptom are merged. You answer against one table with `yes`, `yes 1,3`, `drop 2`, or `<n>: <change>`.

**Duplicates.** If an open duplicate exists, it comments there instead of creating a new issue. A closed, delivered duplicate goes to `/qa-escape`.

The skill never edits code and never changes a label vocabulary.

## Workflow Gates

A gate is a check that must pass before you move to the next step. This table lists each one and when you can go on.

| Gate | Skill | Continue When |
| :--- | :--- | :--- |
| Workspace | `/agents-md` | The PROJECT-CODE matrix and Non-negotiable rules are in force, and every `rules/` file named in the `AGENTS.md` table exists. |
| Requested worktree | `/using-git-worktrees` | The project's `.worktrees/<task-name>` is verified and ignored. The baseline passes, or you approved an exception for the reported failures. |
| Design system | `/design-system` | Tokens and library built. Contrast checked, with failing pairs reported. The preview renders and you have looked at it. The `AGENTS.md` reference and `<project-slug>-ui-coding` are created or extended. |
| Issue preflight | `Issue-writing skills` | The title pattern and both required labels are checked against local workspace instructions. |
| Discovery | `/feature-discovery` | An evidence-backed report is returned in chat, with an ADR section. Git history is not read unless you accepted the offer. Discovery files are never written. |
| Port | `/port-feature` | Gap map written to `specs/port/`. Reference behavior and target state are mapped. A thin first slice is named. |
| Prompt | `/feature-prompt` | You have reviewed the implementation-ready prompt. It passes the fog test: the destination and open decisions are sharp. |
| Wayfinding | `/wayfinder` | The map is charted with a named destination. Or, when working it, exactly one ticket is resolved, closed, and indexed on the map. Map exhausted → nothing left to decide → `/to-spec`. |
| Grill | `/grill-with-docs` | Questions come in numbered rounds, each with a recommended answer. Unclear points are resolved against ADRs and domain language. Done only when no open questions are left. |
| Spec | `/to-spec` | The spec is clear, and the dependency order is known. |
| Tickets | `/to-tickets` | Tickets are testable. Prerequisites, blocking links, and unblocked work are in order. |
| Existing issue triage | `/triage` | The issue's state is clear, or an Agent Brief / needs-info / wontfix outcome is recorded. |
| Build | `/implement` or `/tdd-loop` | Failure seen (Red), fix seen (Green), completion evidence quoted. `/implement` stops after `/code-review` and local adversarial `/risk-review` without committing. |
| Whole-spec build | `/implement-spec` | Every ticket merged onto one local integration branch, and `/code-review` followed by local adversarial `/risk-review` run on it. Nothing pushed, no PR opened, no ticket closed; the ship skills do those. |
| Pixel conformance | `/pixel-audit` | Defect list cleared. Every fix passes the element-level check on the assets the app actually serves. |
| QA polish | `/polish-batch` | Cosmetic nits captured, sent out per PROJECT-CODE, and verified. |
| PR feedback worked | `/pr-feedback` | Reviewer threads sorted, accepted fixes shipped, replies cite SHAs. |
| Staging fixed via CI | `/staging-fix` | Local fix with a test. PR to the confirmed staging branch auto-merged. No server touched. |
| Promoted to staging | `/local-to-staging` | Every project with both branches has its PR merged on green, the merge commit read back, and every Actions run on that commit finished with `success`. `no run` and `pending` mean unverified, not passed. |
| Production readiness | `/staging-to-production` | A project is `ready` only when staging is ahead, every run on staging's latest commit is green, and there is no conflicting promotion PR. You run the printed commands; the skill never does. |
| Cross-repo seam | `/integration-contract` | The producer/consumer contract for the multi-project spec is built and its smoke check is green. Single-project specs skip this automatically. |
| Ship | `/commit-push-*` | Credential and debug-code scan clean. Branch pushed without force. Issue/PR linked with test proof, before/after evidence, and a merge-danger call. A bug fix names its root cause. |
| Worktree cleanup | Authorized cleanup or integration workflow | Integration is verified, needed files are saved, and no worker or process needs the checkout. A push or a closed issue alone does not count. |
| Release | `/release-notes` | PM-friendly summary saved to `specs/release-notes/`. |

## Recovery Loops

When you get stuck, find your situation below.

- **Don't Know Which Skill:** `/ask-kit` names one kit skill for the situation. Once a spec, ticket, or PR exists, `/factory` reads its real state.
- **Vague Prompt:** Back to `/feature-prompt`.
- **Scope Waits On Unresolved Decisions:** That is fog. Use `/wayfinder`, not a longer grilling session.
- **Domain Ambiguity:** Stay in `/grill-with-docs`. It updates `GLOSSARY.md` as you go.
- **Too Many Questions / Drift:** Narrow to one thin slice with `/feature-prompt`, then go back to `/grill-with-docs`.
- **High-Fidelity Uncertainty (feel/UI/interaction):** `/handoff` -> `/prototype` -> back to `/grill-with-docs`.
- **Context Budget Pressure:** For factory runs, go by how full the model's context actually is. Save a checkpoint at 60% and keep the 25% reserve free, counting results still on their way back. Other planning sessions follow the [phase-boundary guidance](BEST-PRACTICES.md#phase-boundaries). If the run refuses a request to protect the reserve, that does not prove the model hit a hard limit. Sending the same request again does not free any context.
- **Broken Tests:** Stay in `/tdd-loop`, or switch to `/diagnosing-bugs`.
- **Worktree Setup Blocked:** Keep the source checkout as it is and pause task edits that depend on the worktree. Fix the failed setup; do not quietly work in place instead.
- **Worktree Cleanup Refused:** Keep the checkout and branch. Check for unfinished work, who owns the branch, and the integration evidence before trying again. Never force removal just to finish a checklist.
- **Push Rejected:** The ship skills report it under `Needs user:`. Never retry with `--force` or `--force-with-lease`. Find out who pushed and why.
- **Discovery Can't Explain Why Or When:** Accept `/feature-discovery`'s offer to scan history. It reads `git log` / `git show` / `git blame` read-only and answers in a short addendum.
- **Herdr Workers Share Runtime Resources:** A worktree separates files, but not ports, databases, Compose projects, or `.env*` files. Run those workers one at a time, or confirm each worker's ports at intake.
- **Large Tickets:** Back to `/to-tickets` for smaller slices.
- **UI Drifts From Design:** Run `/pixel-audit` on the page against its source of truth. Pass the element-level check before shipping.
- **Cosmetic Nits Pile Up:** `/polish-batch`. Capture them, then fix them in one pass per PROJECT-CODE.
- **Cross-Repo Seam Risk:** `/integration-contract` before shipping a multi-project spec.
- **Inlined UI Instead Of The Library:** Back to `/design-system` (extend) to move it into the library, then use it from the page.
- **Red CI On An Open PR:** `/ci-loop`. When it hits its 3-attempt cap, or stops with `no repro` / `head moved`, diagnose with `/diagnosing-bugs`.
- **Risk Review Finds Blocking Issues:** Fix and push. The PR goes back to CI. Run `/factory` again to confirm.
- **Risk Review Suggests Simplification:** Decide whether to apply the evidence-backed advice as a scoped change. Advice alone does not block delivery; the normal risk triggers and blocking findings still govern the PR.
- **Staging Deploy Fails After Merge:** `/staging-fix`, or a revert PR to `staging`.
- **Debug Output Left In The Diff:** The ship skills stop on `[DEBUG-…]` tags and stray debug prints. Remove them, or confirm a line is meant to stay.
- **Promotion PR Blocked:** `/local-to-staging` reports a conflicting PR, a failed check, or a required review, and leaves it. Resolve conflicts yourself, fix checks with `/ci-loop`, then run it again. It never retries with `--admin` or another merge method.
- **Production Has Commits Staging Lacks:** `/staging-to-production` flags it. Bring the hotfix back into `local` and promote it through staging before promoting to production.
- **Human QA Finds A Bug After Done:** Run `/qa-escape` on the issue first. It records the escape class and names the regression test. Then `/tdd-loop`. A class that escapes three times gets a durable guard, applied only with your approval.
- **Agentic QA Reports Findings:** `/tdd-loop` for each finding; the tester never fixes. A finding still failing on its third re-check goes to the engineer.
- **Agent Repeated A Mistake Or Searched Too Long:** `/retro` in the same session, before clearing context. It proposes the check, standard, or navigation pointer that would have prevented it.
- **Incident Or Outage:** `/incident-triage` first. Its fix ticket re-enters at `/factory`.
- **Production Error:** Start with `/sentry` -> `/diagnosing-bugs`.

## Practical Default

When unsure, run this sequence by hand:
1. `/feature-discovery`
2. `/feature-prompt` (Plan)
3. `/grill-with-docs` (Challenge)

No auto-chains. Start each step once the previous one's gate has passed. For anything off this path, `/ask-kit` names the skill to start with.

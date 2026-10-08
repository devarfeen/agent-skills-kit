# Intake

Three decisions, asked as one batched question set after Discover and Group. Reuse choices the user already supplied. Respect the question tool's option and question limits, splitting the batch when required; free-text replies remain available. Zero attribution: omit co-author, AI, and tool attribution from all output.

## Grouping rule

Grouping happens before Intake, so the questions can show it.

- **Share one worktree and one thread, worked in order,** when one issue is blocked by another in the set, or when two issues name the same file, route, component, table, or migration in their body or acceptance criteria. Two threads editing the same lines produce a conflict nobody asked for.
- **Own worktree and own thread** for every other issue.
- **One worktree per repository.** An issue that spans repositories gets one worktree in each and still one thread; name the repositories in its prompt.

Give each group a one-clause reason drawn from the issue text (`#41 + #44 — both change InvoiceTotal.vue`). An issue whose surface cannot be told from its text stays on its own, and the reason says so. A blocking relation that could not be read is stated as a gap, never treated as independence.

## 1. Which coding agent

List the provider instances and models returned by **Capabilities** in [`t3-tools.md`](t3-tools.md), by product name, and ask which runs the workers. One choice applies to every thread unless the user names a per-group split.

**User away →** omit `modelSelection`, which takes each project's default model, and say so in the launch update.

## 2. Which permission mode

Read the `runtimeMode` values from the live schema and offer only the two that let a thread work unattended: the one T3 Code's interface calls **Full access** and the one it calls **Auto**. State the consequence of anything stricter: the orchestrator cannot approve a permission prompt, so the thread stops until the user approves it in T3 Code.

A worktree separates files; it does not sandbox commands, credentials, or network access. Say that in the question.

**User away →** reuse a mode the user already named. With none named, stop before launching — an unattended run in a mode nobody chose is not a default.

## 3. Grouping and leftover threads

Show the groups with their reasons and ask for changes. Name any runtime resource the workers' tests share — a fixed port, a local database, a Compose project, a gitignored `.env*` file — and propose running those groups one after another.

List threads from a previous run whose titles match this run's labels, per **Recover**, and ask whether to monitor them instead of launching again.

**User away →** keep the proposed groups, run groups that share a runtime resource one after another, and monitor leftover threads instead of launching a second thread for the same issue.

# Changelog

Zero attribution: never add or leave co-author, AI, or tool attribution in this file.

Dated entries, newest first. Each names the skills whose behavior changed and
their new versions, so a workspace on an older copy can see what an update
brings. Generated `AGENTS.md` files carry the `agents-md` marker version;
re-run `/agents-md` after a marker bump.

## 2026-10-05

Follows Matt Pocock's skills v1.3.0 / v1.3.1.

### Breaking

- **`CONTEXT.md` is now `GLOSSARY.md`** (`CONTEXT-MAP.md` → `GLOSSARY-MAP.md`),
  matching upstream. Kit skills read a legacy `CONTEXT.md` when it is the only
  one present. `/agents-md` (marker `v47`) offers an ask-first rename.
- **`/pr-feedback` 0.2.0** no longer hands off to `/commit-push-pr` itself. It
  stops after the tested local fixes and asks you to run it, then answers the
  threads.

### Added

- **`/ask-kit` 0.0.1** — router over the kit's own skills.
- **Ship policy** (`/commit-push-pr` 0.2.0, `/commit-push-close` 0.2.0):
  `Before:` / `After:` evidence and a Merge danger block (`Door:`,
  `Blast radius:`) in every QA handoff; a `Root cause:` line on bug-fix
  commits; a pre-commit search for leftover debug instrumentation; a path for
  branches that already carry commits, with a scan of their messages; several
  issues on one branch.
- **`/commit-push-pr`**: optional Summary visual, Evidence and Merge danger
  sections in the PR body; its headings win over a PR-body skill such as `pr`.
- **`/risk-review` 0.2.0**: trigger 12, one-way door — declared, or a
  `two-way` claim the diff contradicts.
- **`/agents-md` 0.2.0, marker `v47`**: routing for `/implement-spec`, `/pr`,
  and `/retro`; the phase-boundary order; glossary migration.
- **`/qa-escape` 0.2.0**: guards classify mechanical versus judgement escapes
  first.
- **`/staging-fix` 0.2.0, `/ci-loop` 0.2.0**: tagged debug instrumentation,
  minimised reproduction, root cause in the PR.
- **`writing-kit-skills` 0.2.0**: rules for calling another skill, the cache
  failure mode, and why user-invoked skills keep trigger descriptions.
- Tracked pre-commit hook at `tools/hooks/pre-commit`.
- `.out-of-scope/` records declined ideas.

### Changed

- Manifest: `/implement-spec`, `pr`, `retro`, and `/ask-kit` rows.
- `/orchestrate-herdr` 0.1.1: description boundaries toward the `herdr`
  companion and `/implement-spec`.
- Trigger-eval catalog refreshed to mattpocock/skills v1.3.1; the removed
  `resolving-merge-conflicts` is gone.
- Patch bumps for the renamed canonical artifacts-root line: `agentic-qa`,
  `design-system`, `incident-triage`, `integration-contract`, `pixel-audit`,
  `polish-batch`, `port-feature`, `release-notes` (0.1.1); `feature-discovery`
  and `feature-prompt` (0.2.0).

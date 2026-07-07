---
name: release-notes
description: Generate clear, PM-friendly release notes, changelogs, and session summaries from git commits, feature work, or the current development session. Use when the user asks for release notes (for a date, date range, project, or feature), a changelog, a PM/stakeholder update, or to summarize what changed in plain language for non-technical readers.
---

# Release Notes

## Purpose

Turn development activity — git commits, the current session, or a completed
feature — into release notes a Project Manager can scan in 30 seconds. The
audience is PMs, QA, and operations stakeholders, not engineers: every entry
explains what changed, why, and what is better now, in plain language.

## Writing Rules

The #1 priority is **clarity for non-technical readers**. Every sentence must
pass: "Would a PM or QA person understand this without asking a developer?"

1. **Plain, everyday words.** No jargon, corporate-speak, or engineering terms.
   - BAD: "Standardized how scanning is prepared before each RFID lookup"
   - GOOD: "The app now checks the scanner is ready before starting a scan"
2. **Say what the user sees or does.** Name the screen, button, field, or page.
   - BAD: "Concrete touchpoints called out in the workstream docs include the signin page"
   - GOOD: "Affects the Login page, Sign Up page, and Reset Password page"
3. **One idea per bullet, one short sentence each.** Never a paragraph. Max 2
   content bullets per Problem/Change/Impact section — the labeled
   `What changed where:` and `Simple logic explanation:` lines don't count;
   needing more means too much detail; combine or simplify.
4. **Feature names describe what changed, not how.**
   - BAD: "Auth Hardening Workstreams Prepared" → GOOD: "Login and Password Improvements Planned"
5. **Problem = what the user experienced** (the symptom, not what the code
   lacked). **Impact = what is concretely better now.**
   - BAD: "Without a written design, security-sensitive work is easier to implement inconsistently"
   - GOOD: "Some login pages let you toggle password visibility, others didn't"
6. **No filler or abstraction.** Remove "formally", "in order to", "it should
   be noted that", "this ensures that". Prefer "All login screens now behave
   the same way" over risk-reduction prose.
7. **Translate engineering into operational meaning.** Rewrite code-level
   detail as its user-visible effect; keep code identifiers out of the
   narrative unless the user asks for technical detail.
   - "refactored useRfidScanner" → "the app now sets up the scanner the same way before every scan"
   - "added test coverage" → "reduced regression risk by validating scanner setup behavior"
8. **Banned words/phrases:** workstream, artifact, canonical, process drift,
   touchpoint, formally, standardized, operationally, implementation, ad hoc,
   scope (as jargon), aligned, resolution, "it is suitable for", "this reduces
   the chance of", "without X, Y is easier to Z", "not explicitly visible in
   commit history", any bullet phrase over 15 words.
9. **If logic changed, add one sentence a 5th grader could understand** inside
   the Change section: `Simple logic explanation: <sentence>` (e.g. "Raised
   scanner power to 30 and switched it on before every scan.").
10. **Write like telling a coworker what you did today** — not a formal document.

Avoid vague verbs ("enhanced", "optimized", "improved") without saying what
changed in behavior. If exact metrics are unavailable, use directional impact
grounded in observed behavior.

## Generation Modes

| Mode | Example prompt | Behavior |
| :--- | :--- | :--- |
| Date-based (single date or range) | `Generate release notes for 11 March 2026` | Read local git history, filter by date, group by project, cluster related commits |
| Session summary | `Summarize what we changed this session` | Review session-modified files, notes, and diffs; combine into logical improvements |
| Feature summary | `Write release notes for the RFID scanning improvements` | Find the feature's commits and explain them as one Problem → Change → Impact story |

## Git Data Collection

Never run `git fetch`, `git pull`, or anything that modifies local git state.
Read only what is already available locally.

### Multi-repo workspaces

Missing a repo means silently missing a whole project's notes, so:

1. Find every git root in the workspace:
   ```bash
   find <workspace-root> -maxdepth 3 -name ".git" | sed 's/\/.git$//'
   ```
   No `-type d` — in worktrees and submodules `.git` is a file, and filtering
   to directories silently drops those whole projects from the notes.
2. Run `git log` in **each** repo — never assume the workspace root is the only
   repo:
   ```bash
   git log --all --after="YYYY-MM-DDT00:00:00" --before="YYYY-MM-DDT23:59:59" --oneline --no-merges
   ```
   `--all` catches work merged into any local branch; `--no-merges` skips merge
   noise. Use `--format="%H %s"` for richer detail. `--all` also sweeps
   unmerged and abandoned branches, so before presenting a cluster check it
   reached the default branch (`git branch --contains <hash>`); work that
   hasn't gets labeled "in progress on `<branch>`" in its Summary, never mixed
   silently into shipped notes.
3. If the user names a project and no commits are found, say so explicitly:
   "No commits found for <Project> on <date>. The local branch may not be up to
   date — try running `git pull` in that repo." Never silently omit a project.

### Project discovery

Map commits to projects via the `AGENTS.md` Project Matrix, repo docs,
workspace metadata, repo paths, or user context. When a Project Matrix code
exists, use the full PROJECT-CODE exactly as written, everywhere.

### Agent use

When the runtime supports subagents and the user has allowed them, dispatch
read-only **Explorer** lanes in parallel for separate repos, date ranges, or
independent feature clusters (local subagents only — never cloud). Each lane
returns commit hashes, affected files, user-visible changes, likely grouping,
and uncertainty — summaries, not transcripts. The main session owns final
clustering, plain-language rewriting, QA-step quality, and file output.

## Commit Clustering

Do not narrate commit-by-commit. Cluster related commits into one logical,
PM-facing change (Problem → Change → Impact).

- **Cluster together** commits sharing a product/app/module, feature or
  workflow, bug or user problem, file area, or one implementation objective —
  including iterative work and bugfix sequences with similar wording.
- **Keep separate** commits for different products, workflows, features,
  unrelated bugs, or independent user-facing changes.
- **When uncertain, keep commits separate** rather than merging unrelated work.

## Output Format

One markdown file, filled from the asset skeletons — they are the single
format source. Load the one matching the mode and fill it:

- Date-based / date-range / feature mode →
  [`assets/release-notes-template.md`](assets/release-notes-template.md)
- Session summary →
  [`assets/session-summary-template.md`](assets/session-summary-template.md)

Worked input→output pairs live in
[`references/examples.md`](references/examples.md) — load them when unsure how
an entry should read.

Rules for filling the skeleton:

- Stakeholder Summary first, then one `---` rule, then Detailed Release Notes.
  Never put feature sections above a project heading or child sections outside
  a feature.
- **Stakeholder Summary** is the 30-second scan: `Date: DD Month YYYY` first
  (omit for undated session summaries), then each PROJECT-CODE as plain text on
  its own line (no heading syntax), then one bullet per feature combining
  Summary + Change into a single sentence.
- **Repeat the feature block** for multiple features under one project.
- **Manual QA Steps**: 3–5 practical steps per feature, each
  `Action -> Expected Result`, covering the primary happy path and one edge
  case, written so a manual tester needs no code knowledge — name the screen,
  button, or field.
- **Include only projects with at least one confirmed change** in the selected
  scope. No unchanged-project sections.
- **User-visible detail**: when commits/diffs reveal them, name the setting,
  page/screen, visible element, or route that changed — the optional
  `What changed where:` line under **Change** is where it goes. If a detail is
  not in the history, omit it and omit the line (rule 8's banned phrases
  cover the disclaimer wording).
- Commit hashes appear only under **Commits Included**, one per bullet. For a
  session summary with no commits yet, write `- (uncommitted session work)`
  instead of hashes.

## File Output

Save under `<artifacts-root>/docs/release-notes/`. Release notes are on-demand
date files: they do **not** share the ADR/prompt `NNNN` sequence (ADRs live in
`docs/adr/NNNN-<slug>.md`, prompts in `docs/prompts/NNNN-<slug>-prompt.md`).

Resolve `<artifacts-root>` in this order:

1. **VS Code workspace (preferred):** the directory containing a
   `*.code-workspace` file found at or above cwd — all projects share one
   `docs/release-notes/`.
2. **Multi-context single repo:** with a root `CONTEXT-MAP.md`, the
   `docs/release-notes/` of the context the change belongs to.
3. **Single repo:** the repo root.

For multi-repo workspaces *without* a `.code-workspace` file, write one file
per repo under that repo's own `docs/release-notes/`.

Filenames — `D-Month-YYYY` (no leading zero, Title Case English month):

| Mode | Filename |
| :--- | :--- |
| Date-based / feature / session | `10-March-2026.md` |
| Date range | `10-March-2026-to-12-March-2026.md` |

- Feature summaries use the **release date**, not the feature name; if no date
  is given and the user doesn't clearly mean the current session, ask. If the
  user is away, use the current local date and note the assumption at the top
  of the response.
- "Today" / "current session" → the current local date.
- Do not add `NNNN`, `-release-notes`, or a feature slug to the filename.

Conflict handling: create `docs/release-notes/` lazily; overwrite a same-date
file only if it contains purely generated content from this skill; if it has
hand edits, show the diff and ask (overwrite, append/update, or abort) — and
if the user is away, write a ` (2)`-suffixed sibling file instead and say so;
never overwrite hand edits unconfirmed. Never delete unrelated files.

## Quality Check Before Finalizing

Mechanical pass first — scan the draft and fix every hit before judging tone:

1. No rule-8 banned word/phrase appears anywhere; no bullet runs over 15 words;
   no Problem/Change/Impact section exceeds 2 content bullets.
2. Structure and hierarchy match the loaded asset skeleton exactly (one `---`,
   child sections inside features, hashes only under **Commits Included**);
   only changed projects are included; the file is saved to
   `docs/release-notes/` with the `D-Month-YYYY` name, re-opened to confirm
   the saved structure matches the skeleton, and the reply states each saved
   file path.

Then the judgment pass:

3. A PM can understand every entry without code context; a QA person knows what
   to test; each impact bullet is an observable operational outcome.
4. At least one bullet names affected workflows or teams; technical identifiers
   are out of the main narrative; logic changes carry their one simple sentence.
5. Nothing is speculated beyond the workspace, git history, or provided context.
6. End the chat response with `Suggested next skills (optional)` — 1–6 advisory
   suggestions based on what the user should likely do next (no gating).

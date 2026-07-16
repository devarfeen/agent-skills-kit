---
name: release-notes
disable-model-invocation: true
description: Generate clear, PM-friendly release notes, changelogs, and session summaries from git commits, feature work, or the current development session. Use when the user asks for release notes (for a date, date range, project, or feature), a changelog, a PM/stakeholder update, or to summarize what changed in plain language for non-technical readers.
---

# release-notes

Turn development activity into release notes a Project Manager can scan in 30
seconds: every entry tells PMs, QA, and operations — not engineers — what
changed, why, and what is better now. It only summarizes work that already
happened — it never plans, files issues, or reviews code (those are
`/feature-prompt`, `/qa`, and `/code-review`).

## Writing rules

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
   scope (as jargon — the structural **Scope** section header is exempt),
   aligned, resolution, "it is suitable for", "this reduces
   the chance of", "without X, Y is easier to Z", "not explicitly visible in
   commit history", any bullet phrase over 15 words.
9. **If logic changed, add one sentence a 5th grader could understand** inside
   the Change section: `Simple logic explanation: <sentence>` (e.g. "Raised
   scanner power to 30 and switched it on before every scan.").
10. **Write like telling a coworker what you did today** — not a formal document.

Avoid vague verbs ("enhanced", "optimized", "improved") without saying what
changed in behavior. If exact metrics are unavailable, use directional impact
grounded in observed behavior. Never state anything not supported by the
workspace, git history, or context the user provided.

## Generation modes

- **Date-based** (date or range; `Generate release notes for 11 March 2026`) — filter local git history by date, group by project, cluster commits.
- **Session summary** (`Summarize what we changed this session`) — combine session-modified files, notes, and diffs into logical improvements.
- **Feature summary** (`Write release notes for the RFID scanning improvements`) — the feature's commits explained as one Problem → Change → Impact story.

## Git data collection

Never run `git fetch`, `git pull`, or anything that modifies local git state.
Read only what is already available locally.

### Multi-repo workspaces

1. Find every git root in the workspace:
   ```bash
   find <workspace-root> -maxdepth 3 -name ".git" | sed 's/\/.git$//'
   ```
   No `-type d` — in worktrees and submodules `.git` is a file; filtering to
   directories silently drops those projects.
2. Run the log in **each** repo, never only the workspace root:
   ```bash
   git log --all --after="YYYY-MM-DDT00:00:00" --before="YYYY-MM-DDT23:59:59" --oneline --no-merges
   ```
   Before presenting a cluster, verify it reached the default branch
   (`git branch --contains <hash>`); work that hasn't is labeled
   "in progress on `<branch>`" in its Summary, never mixed silently into
   shipped notes.
3. If the user names a project and no commits are found, say so explicitly:
   "No commits found for <Project> on <date>. The local branch may not be up to
   date — try running `git pull` in that repo." Never silently omit a project.

### Project discovery

Map commits to projects via the `AGENTS.md` Project Matrix, repo docs, paths,
or user context. Name the full PROJECT-CODE from the Project Matrix everywhere; never mix one project's conventions, tokens, or components into another.

### Agent use

Sub-agents: local lanes only when the user allows them — never cloud agents; announce the lane count at dispatch and report each lane as it completes. Split lanes by
repo, date range, or feature cluster; lanes return summaries — commit
hashes, affected files, user-visible changes, likely grouping, uncertainty —
never transcripts; the main session owns clustering, plain-language rewriting,
QA-step quality, and file output.

## Commit clustering

Never narrate commit-by-commit — cluster related commits into one PM-facing
Problem → Change → Impact change. Commits sharing a product, feature or
workflow, bug, file area, or one objective cluster together (including
iterative and bugfix sequences); different products, workflows, features, or
unrelated bugs stay separate. When uncertain, keep them separate.

## Output format

One markdown file, filled from the asset skeleton matching the mode — the
skeletons are the single format source:

- Date-based / date-range / feature mode →
  [`assets/release-notes-template.md`](assets/release-notes-template.md)
- Session summary →
  [`assets/session-summary-template.md`](assets/session-summary-template.md)

Worked examples live in [`references/examples.md`](references/examples.md);
load when unsure how an entry should read.

Filling rules:

- Stakeholder Summary first, then one `---` rule, then Detailed Release Notes;
  feature sections sit under their project heading, child sections inside
  their feature.
- **Stakeholder Summary** is the 30-second scan: `Date: DD Month YYYY` first
  (omit for undated session summaries), each PROJECT-CODE as plain text on
  its own line (no heading syntax), one bullet per feature combining
  Summary + Change into a single sentence.
- **Repeat the feature block** for multiple features under one project.
- **Manual QA Steps**: 3–5 practical steps per feature, each
  `Action -> Expected Result`, covering the primary happy path and one edge
  case, written so a manual tester needs no code knowledge — name the screen,
  button, or field.
- **Include only projects with at least one confirmed change** in the selected
  scope — no unchanged-project sections.
- **User-visible detail** goes on the optional `What changed where:` line
  under **Change** — the setting, page/screen, element, or route, only when
  commits/diffs reveal it; otherwise omit the line (rule 8 bans disclaimer
  wording).
- Commit hashes appear only under **Commits Included**, one per bullet; a
  session summary with no commits yet writes `- (uncommitted session work)`
  instead.

## File output

Save under `<artifacts-root>/specs/release-notes/`.

Release notes are a generated document: keep all co-author, AI, and tool
attribution out of both the saved file and the chat response.

Resolve `<artifacts-root>`: the `*.code-workspace` directory if one exists, else the per-context root (`CONTEXT-MAP.md` at repo root), else the repo root.
Multi-repo workspaces *without* a `.code-workspace` file get one file per
repo, under each repo's own `specs/release-notes/`.

Filenames — `D-Month-YYYY`, no leading zero, Title Case English month:
`10-March-2026.md`; date ranges `10-March-2026-to-12-March-2026.md`.

- Feature summaries use the **release date**, not the feature name; if no date
  is given and the user doesn't clearly mean the current session, ask — or, if
  the user is away, use the current local date and note the assumption up
  top.
- "Today" / "current session" → the current local date.
- Do not add `NNNN`, `-release-notes`, or a feature slug to the filename —
  release notes do not share the ADR/prompt `NNNN` sequence.

Conflict handling: create `specs/release-notes/` lazily; overwrite a same-date
file only if it contains purely generated content from this skill; if it has
hand edits, show the diff and ask (overwrite, append/update, or abort) — and
if the user is away, write a ` (2)`-suffixed sibling file instead and say so;
never overwrite hand edits unconfirmed. Never delete unrelated files.

## Completion criteria

- [ ] The saved file contains zero rule-8 banned words in narrative text
  (**Scope** header exempt), no bullet over 15 words, no Problem/Change/Impact
  section over 2 content bullets.
- [ ] Each file exists at `specs/release-notes/<D-Month-YYYY>.md` under the
  resolved root and re-opens matching the loaded skeleton's structure, with
  only changed projects present.
- [ ] Every cluster presented as shipped passed `git branch --contains` or
  carries its "in progress on `<branch>`" label.
- [ ] At least one bullet names an affected workflow or team.
- [ ] Re-read the saved file as a PM: every entry understandable without code
  context, each impact bullet an observable outcome, a QA reader knows what
  to test.
- [ ] The reply states each saved file path and ends with
  `Suggested next skills (optional)` — 1–6 advisory suggestions, never gating.

---
name: release-notes
description: Generate clear, PM-friendly release notes and session summaries from git commits, feature work, or current development changes.
---

# Release Notes

## Purpose

Generate clear, structured release notes or session summaries for Project Managers based on development activity.

The skill can produce summaries from:

- Git commits
- Current development session
- Completed feature work

Outputs must explain what changed, why it changed, and the improvement delivered, using simple language suitable for non-technical stakeholders.

Default audience is Project Managers and operations stakeholders, not engineers.

## Writing Style Rules

The #1 priority of this skill is **clarity for non-technical readers**. Every sentence must pass this test: "Would a PM or QA person understand this without asking a developer?"

### Absolute Rules

1. **Use plain, everyday words.** No jargon. No corporate-speak. No engineering terms.
   - BAD: "Standardized how scanning is prepared before each RFID lookup"
   - GOOD: "The app now checks the scanner is ready before starting a scan"

2. **Say what the user sees or does.** Name the screen, button, field, or page.
   - BAD: "Concrete touchpoints called out in the workstream docs include the signin page"
   - GOOD: "Affects the Login page, Sign Up page, and Reset Password page"

3. **One idea per bullet.** Each bullet = one short sentence. Never a paragraph.
   - BAD: "Two implementation workstreams were documented and broken down for execution covering username lowercasing and consistent password show/hide behavior across login, signup, reset, invite, and user-management screens."
   - GOOD:
     - "Usernames will be saved as lowercase so 'John' and 'john' are treated the same"
     - "All password fields now have a show/hide toggle"

4. **Feature names must describe what changed, not how it was done.**
   - BAD: "Auth Hardening Workstreams Prepared"
   - GOOD: "Login and Password Improvements Planned"
   - BAD: "Workspace Process Rules Clarified"
   - GOOD: "Updated Internal Team Workflow Guide"

5. **No filler phrases.** Remove words that add no meaning.
   - Remove: "formally prepared", "in a clear scope", "as a result of", "in order to"
   - Remove: "it should be noted that", "this ensures that", "with a clear"

6. **Avoid abstract language.** Be specific about what happened.
   - BAD: "reduces the risk of one screen being fixed while another screen keeps the same login or password-typing problem"
   - GOOD: "All login screens now behave the same way"

7. **Problem section = what the user experienced.** Not what the code lacked.
   - BAD: "Without a written design and task breakdown, this type of security-sensitive work is easier to implement inconsistently"
   - GOOD: "Some login pages let you toggle password visibility, others didn't. Usernames 'John' and 'john' were treated as different accounts."

8. **Impact section = what is better now.** One short sentence per bullet. Concrete outcome.
   - BAD: "Engineering now has approved-ready implementation notes for sensitive auth work instead of relying on ad hoc fixes"
   - GOOD: "Login will work the same way across all apps"

9. **Max 2 bullets per section** (Problem, Change, Impact). If you need more, you're being too detailed — combine or simplify.

10. **Write like you're telling a coworker what you did today** over a coffee. Not like you're writing a formal document.

### Banned Words and Phrases

Never use these in release notes output:

- workstream, artifact, canonical, process drift, touchpoint
- formally, standardized, operationally, implementation
- ad hoc, scope, aligned, resolution
- "it is suitable for", "this reduces the chance of"
- "without X, Y is easier to Z" (rewrite as a direct statement)
- "not explicitly visible in commit history"
- Any phrase longer than 15 words in a single bullet

### Writing Test

Before finalizing each feature entry, mentally check:

- Can a PM read this in 10 seconds and know what changed?
- Can a QA person read this and know what to test?
- Would you understand this if you had never seen the code?

If any answer is no, rewrite it simpler.

## Supported Generation Modes

### 1. Date-Based Release Notes (Git History)

Generate release notes from Git commits for a specific date.

Example prompts:

- Generate release notes for 11 March 2026
- Generate release notes for 11 March for all projects
- Generate release notes for PARTNERS-APP on 11 March

Behavior:

1. Read git commit history
2. Filter commits by the requested date
3. Group commits by full project code, app, or module
4. Combine related commits into a single logical improvement summary

### 2. Session-Based Development Summary

Generate a summary of changes made in the current development session.

Example prompts:

- Summarize what we changed this session
- Create PM update for today's work
- Generate session release notes

Behavior:

1. Review files modified in the session
2. Review developer notes, markdown previews, and code diffs
3. Combine related edits into logical improvements
4. Present them grouped by full project code

### 3. Feature-Based Summary

Generate release notes for a completed feature or task.

Example prompts:

- Write release notes for the RFID scanning improvements
- Summarize the Stock Take lookup changes
- Create PM update for the asset lookup improvements

Behavior:

1. Identify commits related to the feature
2. Combine commits into a single feature explanation
3. Explain Problem → Change → Impact

## Git Data Collection

The skill must NOT run `git fetch`, `git pull`, or any command that modifies the local git state. It only reads what is already available locally.

### Agent Use

When the runtime supports subagents and the user has allowed them, act as the orchestrator and use read-only **Explorer** lanes for independent collection and summarization. Use local subagents only — never cloud agents. See the `agents-md` `tool-calling.md` reference for the role-to-mechanism map per runtime.

- Run multiple Explorer lanes in parallel for separate repos, date ranges, or clearly independent feature clusters; push long history scans to local background where supported.
- Ask each Explorer to return commit hashes, affected files, visible user-facing changes, likely grouping, and uncertainty — summaries, not raw transcripts.
- Keep the main session responsible for final clustering, plain-language rewriting, QA-step quality, conflict resolution, and file output.
- Do not use Implementer (write) lanes for release notes unless the user explicitly asks for file-writing delegation.

### Multi-Repo Workspaces

If the workspace contains multiple repositories (multi-root workspace with several git repos):

1. **Find all git roots.** Walk the workspace folder tree and identify every directory that contains a `.git` folder. Each is a separate project repo.
2. **Run `git log` in each repo separately.** Do not assume the workspace root is the only git repo.
3. **Collect commits from all repos**, then group by full project code.

Missing a repo means missing an entire project's release notes. Always scan for all git roots.

### Git Log Command

Use this command pattern in **each repo** to get commits for a specific date:

```bash
git log --all --after="YYYY-MM-DDT00:00:00" --before="YYYY-MM-DDT23:59:59" --oneline --no-merges
```

- `--all` includes commits from all local branches (catches work merged into any branch).
- `--no-merges` skips merge commit noise like "Merge pull request #123".
- For richer detail, use `--format="%H %s"` instead of `--oneline`.

### Finding Repos Automatically

```bash
find <workspace-root> -name ".git" -type d -maxdepth 3 | sed 's/\/.git$//'
```

Then loop through each path and run `git log` inside it.

### Important

If a user mentions a specific project/repo and the skill finds no commits, report that explicitly. Do not silently omit projects — say "No commits found for <Project> on <date>. The local branch may not be up to date — try running `git pull` in that repo."

## Automatic Commit Clustering

When generating release notes from Git history, do not summarize each commit separately unless the commits clearly represent unrelated work.

Instead, automatically cluster related commits into one logical change so the output reads like PM-facing release notes rather than raw engineering history.

### Goal

Convert multiple implementation commits into one stakeholder-friendly summary using:

Problem → Change → Impact

### Cluster Commits Together When They Share

- the same product, app, or module
- the same feature or workflow
- the same bug or user problem
- the same file area or code path
- the same implementation objective across several commits

### Keep Commits Separate When They Represent Different

- products
- workflows
- features
- bugs with unrelated causes
- independent user-facing changes

## Stakeholder Summary Section

Every release notes file must start with a **Stakeholder Summary** section at the top, before the detailed notes.

This section is the quick-read version for PMs and stakeholders. It combines the Summary and Change from each feature entry into short bullet points grouped by date and full project code.

### Format

```
# Stakeholder Summary

Date: DD Month YYYY

PROJECT-CODE-1

- What changed + why it matters in one sentence
- What changed + why it matters in one sentence

PROJECT-CODE-2

- What changed + why it matters in one sentence
```

### Rules

- Start with `Date: DD Month YYYY` (omit for session summaries that have no date).
- Use full project codes from the Project Matrix (e.g., `PARTNERS-APP`, `PORTFOLIO-WEB`, `SERVER-REVERSE-PROXY`). Never abbreviate or invent shorthand. No markdown heading syntax — plain text on its own line.
- Each change is a **markdown bullet** (`- `). One bullet per feature.
- Each bullet combines Summary + Change into one sentence that answers: "What changed and what does that mean for the user?"
- Write bullets so a PM can scan the entire list in under 30 seconds.
- Group by full project code, same grouping as the detailed section below.
- Separate the Stakeholder Summary from the Detailed Release Notes with a horizontal rule (`---`).
- The detailed section follows under a `# Detailed Release Notes` heading.

## Manual QA Steps Section

Every feature entry in the detailed release notes must include a **Manual QA Steps** subsection.

### Generating QA Steps

Generate 3–5 practical manual QA steps inline based on the change:

- Each step must be: **Action → Expected Result**
- Steps should cover the primary happy path and one edge case.
- Write steps a manual tester can follow without reading the code.
- Keep language simple and specific (name the screen, button, or field).

### Clustering Heuristics

Infer that commits belong together when several commits:

- touch the same files or folders
- use similar wording in commit messages
- refer to the same screen, flow, or process
- appear to be iterative work on one feature
- are clearly part of one bugfix sequence

### Summarization Rules

For each cluster:

1. identify the shared problem
2. combine all related commits into one logical summary
3. explain the change in non-technical language
4. describe the resulting improvement
5. avoid commit-by-commit narration unless necessary

## Project Discovery

Project names and codes may be found from:

- Project Matrix entries in `AGENTS.md`
- repository documentation
- workspace metadata
- git repository paths
- folder structure
- user-provided context

When a Project Matrix code exists, use the full code exactly as written in chat output, saved release notes, and any related issue, PR, commit, or code-comment text.

## Output Format

Output must follow the exact structure below. Do not reorder sections.

```markdown
# Stakeholder Summary

Date: <DD Month YYYY>

<PROJECT-CODE>

- <one sentence summary>

---

# Detailed Release Notes

## <PROJECT-CODE>

### <Feature or Improvement Name>

**Summary**

- <one sentence: what is now better in day-to-day operations>

**Problem**

- <what users or operations teams were experiencing before this change>

**Change**

- <what changed in product/workflow language>

**Impact**

- <concrete outcome>

**Scope**

- <who is affected and where the change applies>

**Manual QA Steps**

1. <Action> -> <Expected result>

**Commits Included**

- <hash>
```

For session summaries without a known date, omit only the `Date:` line.

If there are multiple features under one project, repeat the feature block:

### <Feature or Improvement Name>

- Summary
- Problem
- Change
- Impact
- Scope
- Manual QA Steps
- Commits Included

Do not place feature sections above the project header.

## Project Inclusion Rule

Include a project section only if that project has at least one confirmed change in the selected commits/session scope.

Do not include unchanged projects in the final generated file.

## File Output Rules

Always save the generated markdown under `<artifacts-root>/docs/release-notes/`. Release notes are on-demand date-based artifacts; they do not share the ADR/prompt `NNNN` sequence and they do not live beside ADRs. ADRs live in `docs/adr/` with `NNNN-<slug>.md`; feature prompts live in `docs/prompts/` with `NNNN-<slug>-prompt.md`; release notes live separately under `docs/release-notes/` with calendar-date filenames like `10-March-2026.md`.

### Resolving `<artifacts-root>`

Centralize artifacts when a workspace exists; only fall back to a project repo when there's no workspace. Resolve in this order:

1. **VS Code workspace (preferred when present).** If a `*.code-workspace` file is found at or above the cwd, write to the directory containing it. All projects in the workspace share one `docs/release-notes/`.
2. **Multi-context single repo.** If no workspace file but a root `CONTEXT-MAP.md` exists, use the `docs/release-notes/` of the context the change belongs to.
3. **Single-repo project.** Fall back to the repo root.

For multi-repo workspaces _without_ a `.code-workspace` file, write one file per repo under that repo's own `docs/release-notes/`.

### Path shape

```
<artifacts-root>/docs/release-notes/<date-slug>.md
```

- **`docs/release-notes/`** — relative to `<artifacts-root>` resolved above.
- **`<date-slug>`** — `D-Month-YYYY`, using no leading zero for the day and Title Case English month names. Example: `10-March-2026`.
- Do not add `NNNN`, `-release-notes`, or a feature slug to the default filename.

### Slug per mode

1. **Date-based release notes (`Date: <DD Month YYYY>`):**
   - Path: `<artifacts-root>/docs/release-notes/D-Month-YYYY.md`
   - Example (workspace): `<workspace-dir>/docs/release-notes/10-March-2026.md`
   - Example (single repo): `docs/release-notes/10-March-2026.md`
2. **Feature-based summary:**
   - Use the release date as the filename, not the feature name. If the user does not provide a release date, ask for one unless they clearly mean today's current session.
   - Example (workspace): `<workspace-dir>/docs/release-notes/10-March-2026.md`
   - Example (single repo): `docs/release-notes/10-March-2026.md`
3. **Session summary without explicit feature name:**
   - If the user says "today" or "current session", use the current local date.
   - Example (workspace): `<workspace-dir>/docs/release-notes/10-March-2026.md`
   - Example (single repo): `docs/release-notes/10-March-2026.md`
4. **Date range release notes:**
   - Path: `<artifacts-root>/docs/release-notes/D-Month-YYYY-to-D-Month-YYYY.md`
   - Example: `10-March-2026-to-12-March-2026.md`

### Conflict handling

- If `<artifacts-root>/docs/release-notes/` does not exist, create it lazily before writing.
- If a release note file already exists for the same date and contains only generated content from this skill, overwrite in place.
- If the existing file contains hand edits, show the diff and ask the user whether to overwrite, append/update the existing date file, or abort.
- Never delete unrelated files in `docs/release-notes/`.

## Section Hierarchy Rule

The hierarchy must be:

1. `# Stakeholder Summary`
2. Optional `Date: DD Month YYYY`
3. Full project code with summary bullets
4. `---`
5. `# Detailed Release Notes`
6. Full project code heading
7. Feature name heading
8. Child sections under feature: Summary, Problem, Change, Impact, Scope, Manual QA Steps, Commits Included

Never output child sections directly under the date line, stakeholder summary, detailed notes heading, or project heading.

## Writing Guidelines

- Write for non-technical stakeholders
- Translate implementation details into user-facing outcomes
- Avoid unnecessary engineering terminology
- Focus on what improved and how it affects operations
- Prefer short bullet points
- Avoid vague wording such as "enhanced", "optimized", or "improved" without saying what changed in behavior
- If exact metrics are unavailable, use directional impact grounded in observed behavior

## Git Detail Extraction Rules

When generating from git commits/diffs, explicitly extract and summarize user-visible change locations when present.

Look for and report in plain language:

- Main setting changed (for example scanner power, timeout, toggle defaults)
- View/page/screen affected
- Component or visible screen section affected
- URL or route changed (if available and user-visible)
- Visible element changed (button label, status text, warning, banner, modal, etc.)

Prefer naming what users see over code object names.

If details are not available in commits/diffs, omit that detail and keep the note grounded in what is visible. Do not write "Not explicitly visible in commit history" in the release notes output.

## Simple Logic Explanation Rule

If a feature includes programming logic changes, add a plain-language explanation inside the Change section.

Format:

- Simple logic explanation: <one sentence a 5th grader can understand>

Example:

- Simple logic explanation: Raised scanner power from 20 to 30 and made the app switch it on every time before scanning.

## Translation Rules

When source input contains engineering details, rewrite them as operational meaning.

Examples:

- "added API classes/interfaces" -> "connected scanner capabilities so app screens use the same scan process"
- "refactored useRfidScanner" -> "standardized scanner setup to reduce inconsistent scan starts"
- "added test coverage" -> "reduced regression risk by validating scanner setup behavior"

Do not copy code identifiers directly into PM output unless the user explicitly asks for technical detail.

## Quality Check Before Finalizing

Before returning output, verify:

1. A PM can understand it without code context.
2. Each impact bullet describes an observable operational outcome.
3. At least one bullet names affected workflows or teams.
4. Technical identifiers are removed from the main narrative.
5. Commit hashes, if included, appear in a final traceability line only.
6. Output follows Stakeholder Summary -> Detailed Release Notes -> Project -> Feature -> Child sections hierarchy.
7. File is saved in `docs/release-notes/` with the `D-Month-YYYY.md` naming convention, independent of the ADR/prompt number sequence.
8. Change section includes user-visible touchpoints when commit history provides them.
9. Logic changes include one simple sentence understandable by non-technical readers.
10. Final file includes only projects that have confirmed changes.
11. End the response with `Suggested next skills (optional)` using 1-6 advisory suggestions only (no gating), based on what the user should likely do next. Suggest `/memory-steward` when shipped work closed a PRD or left durable prefs in repo `MEMORY.md`.

## Fallback

If clustering is uncertain, keep commits separate rather than merging unrelated work.
Do not speculate about changes not present in the workspace, git history, or provided context.

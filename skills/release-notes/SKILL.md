# Release Notes

## Purpose
Generate clear, structured release notes or session summaries for Project Managers based on development activity.

The skill can produce summaries from:
- Git commits
- Current development session
- Completed feature work

Outputs must explain what changed, why it changed, and the improvement delivered, using simple language suitable for non-technical stakeholders.

## Supported Generation Modes

### 1. Date-Based Release Notes (Git History)
Generate release notes from Git commits for a specific date.

Example prompts:
- Generate release notes for 11 March 2026
- Create changelog for 11 March for all projects
- Generate release notes for Partners App on 11 March

Behavior:
1. Read git commit history
2. Filter commits by the requested date
3. Group commits by product, app, or module
4. Combine related commits into a single logical improvement summary

### 2. Session-Based Development Summary
Generate a summary of changes made in the current development session.

Example prompts:
- Summarize what we changed this session
- Create PM update for today's work
- Generate session changelog

Behavior:
1. Review files modified in the session
2. Review developer notes, markdown previews, and code diffs
3. Combine related edits into logical improvements
4. Present them grouped by product or app

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
- repository documentation
- workspace metadata
- git repository paths
- folder structure
- user-provided context

## Output Format

## <Product / App Name>

### <Feature or Improvement Name>

**Problem**
- What issue or limitation existed

**Change**
- What was changed across the grouped commits

**Impact**
- What improved for users, reliability, operations, or performance

## Writing Guidelines
- Write for non-technical stakeholders
- Avoid unnecessary engineering terminology
- Focus on what improved
- Prefer short bullet points

## Fallback
If clustering is uncertain, keep commits separate rather than merging unrelated work.
Do not speculate about changes not present in the workspace, git history, or provided context.

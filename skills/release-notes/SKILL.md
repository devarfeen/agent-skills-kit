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

Output must follow the exact structure below. Do not reorder sections.

For date-based release notes, include a date line at the top.

`Date: <DD Month YYYY>`

## <Product / App Name>

### <Feature or Improvement Name>

**Summary**

- One sentence: what is now better in day-to-day operations.

**Problem**

- What users or operations teams were experiencing before this change
- Include the business consequence (delays, rework, missed scans, confusion, etc.)

**Change**

- Explain the solution in product/workflow language
- Name affected workflows or screens in plain language
- Include 1 to 3 concrete user-visible touchpoints when available: setting, view/page, component/screen section, URL/route, or visible UI element
- If logic changed, add one simple sentence in plain language for a 5th grader
- Do not include file paths, class names, package names, or internal module names

**Impact**

- State concrete outcomes, not generic claims
- Prefer specific statements such as "fewer failed scans during stock take" over "improved reliability"

**Scope**

- Who is affected (teams, roles, or flows) and where the change applies

**Commits Included**

- List commit hashes only at the end for traceability

If there are multiple features under one project, repeat the feature block:

### <Feature or Improvement Name>

- Summary
- Problem
- Change
- Impact
- Scope
- Commits Included

Do not place feature sections above the project header.

## File Output Rules

Always save the generated markdown under the root `changelog/` folder.

1. Date-based summary or release notes:
   - Path: `changelog/DDMMYYYY.md`
   - Example: `changelog/12032026.md`
2. Feature-based summary:
   - Path: `changelog/<feature-name>.md`
   - Use lowercase kebab-case for file name
   - Example: `changelog/rfid-scanner-reliability.md`
3. Session summary without explicit feature name:
   - Path: `changelog/DDMMYYYY.md`

If `changelog/` does not exist, create it before writing output.

## Section Hierarchy Rule

The hierarchy must be:

1. Date line (date-based only)
2. Project Name
3. Feature Name
4. Child sections under feature: Summary, Problem, Change, Impact, Scope, Commits Included

Never output child sections directly under the date line or without a feature heading.

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

If details are not available in commits/diffs, say "Not explicitly visible in commit history" instead of guessing.

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
6. Output follows Date -> Project -> Feature -> Child sections hierarchy.
7. File is saved in `changelog/` with correct naming convention.
8. Change section includes user-visible touchpoints when commit history provides them.
9. Logic changes include one simple sentence understandable by non-technical readers.

## Fallback

If clustering is uncertain, keep commits separate rather than merging unrelated work.
Do not speculate about changes not present in the workspace, git history, or provided context.

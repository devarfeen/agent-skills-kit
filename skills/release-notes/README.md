# release-notes

Generate PM-friendly release notes from git commits, session work, or completed feature work.

## Supports
- date-based changelogs
- all-project or single-project summaries
- session summaries
- feature summaries
- automatic commit clustering

## Example Requests
- Generate release notes for 11 March 2026
- Generate release notes for Partners App on 11 March
- Summarize today's development session
- Write release notes for the RFID scanning improvements

## Output Style
Uses a clear structure:
- Date (date-based mode only)
- Project
- Feature
- Summary
- Problem
- Change
- Impact
- Scope
- Commits Included

Required section order is strict: Date -> Project -> Feature -> Child sections.

## Detail Level
- For git-based outputs, include concrete "what changed where" details when available:
	setting, page/view, component section, URL/route, or visible UI element.
- If programming logic changed, include one plain-language sentence understandable by a 5th grader.
- If a detail is not present in commit history, state that clearly instead of guessing.

## Output File Location
- Save all generated notes in `changelog/` at workspace root.
- Date-based or session summary: `changelog/DDMMYYYY.md` (example: `changelog/12032026.md`)
- Feature-based summary: `changelog/<feature-name>.md` using lowercase kebab-case.

The output is designed for Project Managers and other non-technical stakeholders.

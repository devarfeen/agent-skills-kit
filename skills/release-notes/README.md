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

Only include project sections that have confirmed changes in the selected commit/session scope.

## Detail Level
- For git-based outputs, include concrete "what changed where" details when available:
	setting, page/view, component section, URL/route, or visible UI element.
- If programming logic changed, include one plain-language sentence understandable by a 5th grader.
- If a detail is not present in commit history, state that clearly instead of guessing.

## Output File Location
- Save all generated notes in `changelog/` at workspace root.
- Date-based or session summary: `changelog/DD-Month-YYYY.md` (example: `changelog/12-March-2026.md`)
- Feature-based summary: `changelog/Feature-Name.md` using Title-Case words joined by hyphens.

The output is designed for Project Managers and other non-technical stakeholders.

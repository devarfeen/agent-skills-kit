# release-notes

Generate PM-friendly release notes from git commits, session work, or completed feature work.

## Install

```bash
npx skills install https://github.com/devarfeen/agent-skills-kit --skill release-notes
```

## Update

```bash
npx skills update https://github.com/devarfeen/agent-skills-kit --skill release-notes
```

## Supports
- Date-based changelogs (single date or date range)
- All-project or single-project summaries
- Session summaries (current dev session)
- Feature summaries (completed feature/task)
- Automatic commit clustering (related commits → one logical change)
- Stakeholder summary (quick-scan one-liner list at the top)
- Manual QA steps (auto-detected from specs or generated)

## Example Requests
- Generate release notes for 11 March 2026
- Generate release notes for Partners App on 11 March
- Create changelog for all projects on 15 April
- Summarize today's development session
- Write release notes for the RFID scanning improvements
- Summarize what we changed this session
- Create PM update for today's work

## Output Style
Uses a two-part structure in a single file:

### Part 1: Stakeholder Summary (top of file)
Quick-read bullet list structured as: **Date → Project Code → Bullet points**. Each bullet combines what changed and why it matters into one sentence. Designed for PMs who need to scan everything in 30 seconds.

### Part 2: Detailed Release Notes (after `---` separator)
Full structured entries per feature:
- Date (date-based mode only)
- Project
- Feature
- Summary
- Problem
- Change
- Impact
- Scope
- Manual QA Steps
- Commits Included

Required section order is strict: Date -> Stakeholder Summary -> --- -> Detailed Release Notes -> Project -> Feature -> Child sections.

Only include project sections that have confirmed changes in the selected commit/session scope.

## Manual QA Steps
Each feature entry includes a **Manual QA Steps** section:
- 3–5 practical QA steps are generated inline (Action → Expected Result format).
- Steps cover the primary happy path and one edge case, written so a manual tester can follow them without reading the code.

## Detail Level
- For git-based outputs, include concrete "what changed where" details when available:
	setting, page/view, component section, URL/route, or visible UI element.
- If programming logic changed, include one plain-language sentence understandable by a 5th grader.
- If a detail is not present in commit history, state that clearly instead of guessing.

## Output File Location
- Save all generated notes under `<artifacts-root>/docs/adr/`, alongside ADRs. Suffix `-release-notes` distinguishes them from ADRs (no suffix). Feature prompts (`-prompt`) live in the sibling `<artifacts-root>/docs/prompt/` folder.
- Resolve `<artifacts-root>` in this order: (1) directory containing a `*.code-workspace` file if one exists, (2) per-context root in a multi-context repo (`CONTEXT-MAP.md` at root), (3) the single repo root. Workspace mode is preferred — it keeps artifacts out of individual project repos.
- Date-based or session summary: `<artifacts-root>/docs/adr/NNNN-DD-month-YYYY-release-notes.md` (workspace example: `<workspace-dir>/docs/adr/0042-12-march-2026-release-notes.md`; single repo: `docs/adr/0042-12-march-2026-release-notes.md`)
- Feature-based summary: `<artifacts-root>/docs/adr/NNNN-<feature-slug>-release-notes.md` (workspace example: `<workspace-dir>/docs/adr/0042-rfid-scanner-reliability-release-notes.md`; single repo: `docs/adr/0042-rfid-scanner-reliability-release-notes.md`)
- Slug is kebab-case, ASCII; `NNNN` is one greater than the highest existing number across **both** `<artifacts-root>/docs/adr/` and `<artifacts-root>/docs/prompt/` (numbering is shared globally across all artifact types).

The output is designed for Project Managers and other non-technical stakeholders.

## File Structure

```
skills/release-notes/
├── SKILL.md                            # Core skill instructions (required)
├── README.md                           # This file
├── references/
│   ├── examples.md                     # Full input/output examples
│   └── triggers.md                     # Trigger phrases
└── assets/
    ├── release-notes-template.md       # Date/feature release notes template
    └── session-summary-template.md     # Session summary template
```

This follows the [Agent Skills spec](https://agentskills.io/specification)
folder conventions: `references/` for on-demand documentation, `assets/` for
static templates.

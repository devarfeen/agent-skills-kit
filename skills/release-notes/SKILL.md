---
name: release-notes
disable-model-invocation: true
description: "Write PM-friendly release notes, changelogs, or session summaries from git commits or the current session, in plain language. A PR summary for review is /code-review; an agent handoff is /handoff."
metadata:
  version: "0.2.0"
---

# release-notes

Turn development activity into release notes a Project Manager can scan in 30
seconds: every entry tells PMs, QA, and operations what changed, why, and
what is better now. It only summarizes work that already
happened — never plans, files issues, or reviews code (those are
`/feature-prompt`, `/qa`, and `/code-review`).

## Writing rules

Every sentence must pass: "Would a PM or QA person understand this without
asking a developer?"

1. **Plain, everyday words.** No jargon, corporate-speak, or engineering terms.
   - BAD: "Standardized how scanning is prepared before each RFID lookup"
   - GOOD: "The app now checks the scanner is ready before starting a scan"
2. **Say what the user sees or does.** Name the screen, button, field, or page.
3. **One idea per bullet, one short sentence each.** Never a paragraph. Max 2
   content bullets per Problem/Change/Impact section — the labeled
   `What changed where:`, `Simple logic explanation:`, and `Action needed:` lines don't count;
   needing more means too much detail.
4. **Feature names describe completed work.** Use "Scanner readiness check"
   for code, or "Login plan documented" for completed planning documents.
5. **Problem = what the user experienced** (the symptom, not what the code
   lacked). **Impact = what is concretely better now.**
6. **No filler or abstraction.** Remove "formally", "in order to", "it should
   be noted that", "this ensures that", and risk-reduction prose.
7. **Translate engineering into operational meaning.** Rewrite code-level
   detail as its user-visible effect ("refactored useRfidScanner" → "the app
   now sets up the scanner the same way before every scan"); keep code
   identifiers out of the narrative unless the user asks for technical detail.
8. **Keep narrative bullets within 15 words.** Replace abstract jargon with
   concrete behavior. Preserve exact UI labels and technical names when needed
   to identify what QA should test. Required QA prerequisites and ordered steps
   may exceed the cap when shortening would make them ambiguous.
9. **If logic changed, add one sentence a 5th grader could understand** inside
   the Change section: `Simple logic explanation: <sentence>`.
10. **Write like telling a coworker what you did today** — not a formal document.

Avoid vague verbs ("enhanced", "optimized", "improved") without saying what
changed in behavior. Without exact metrics, use directional impact
grounded in observed behavior. Never state anything not supported by the
workspace, git history, or context the user provided.

## Generation modes

- **Date-based** (a date or range) — filter local git history by date, group by project, cluster commits.
- **Session summary** — combine session-modified files, notes, and diffs into logical improvements.
- **Feature summary** — the feature's commits explained as one Problem → Change → Impact story.
- **Version range** (`v1.3.0..v1.4.0`, or "since the last release") — resolve local tags with `git tag --sort=-version:refname` and log `<from>..<to>`; the filename uses the `<to>` tag's commit date. A missing local tag → say so; never fetch.

## Evidence collection

Never run `git fetch`, `git pull`, or anything that modifies local git state.
For date, feature, or version history, load
[`references/git-collection.md`](references/git-collection.md); it covers
repo discovery, ancestry, delivery claims, and diff-backed clustering.
Session-only work uses session notes, modified files, and relevant diffs;
load the git reference only when commit or delivery evidence is needed.

Name the full PROJECT-CODE from the Project Matrix everywhere; never mix one project's conventions, tokens, or components into another.

Sub-agents: dispatch local lanes automatically for independent work — never cloud agents; announce the lane count at dispatch and report each lane as it completes. Lanes return summaries of hashes, files, user-visible changes, grouping, and uncertainty; the main session owns clustering, wording, QA steps, and file output.

Emit `Stage / Found / Next / Needs user` at each phase transition — one line per field.

## Output format

One markdown file, filled from the mode's asset skeleton — the
skeletons are the single format source:

- Date-based / date-range / version-range / feature mode →
  [`assets/release-notes-template.md`](assets/release-notes-template.md)
- Session summary →
  [`assets/session-summary-template.md`](assets/session-summary-template.md)

Worked examples live in [`references/examples.md`](references/examples.md);
load when unsure how an entry should read.

Filling rules:

- **Stakeholder Summary** is the 30-second scan: each PROJECT-CODE as plain
  text on its own line (no heading syntax), one bullet per feature combining
  Summary + Change into a single sentence; `Date:` line omitted for undated
  session summaries.
- **Repeat the feature block** for multiple features under one project;
  feature sections sit under their project heading.
- **Manual QA Steps**: 3–5 practical steps per feature, each
  `Action -> Expected Result`, covering the primary happy path and one edge
  case. Name local setup, role, and test data first; distinguish proposed checks
  from tests already run. For docs/tooling-only changes, name the actual file
  or command to inspect. Never invent a screen or an observed result.
- **Include only projects with at least one confirmed change** in the selected
  scope.
- **User-visible detail** goes on the optional `What changed where:` line
  under **Change** — the setting, page/screen, element, or route, only when
  commits/diffs reveal it; otherwise omit the line.
- The optional `Action needed:` line under **Impact**: what users or operations must do —
  re-login, a new setting, a migration, an env key. Omit the line when the
  diffs show nothing.
- Commit hashes appear only under **Commits Included**, one per bullet (the
  session skeleton's `(uncommitted session work)` fallback covers no-commit
  sessions).

## File output

Save under `<artifacts-root>/specs/release-notes/`.

Zero attribution: never add or leave co-author, AI, or tool attribution in
commits, PRs, issue comments, release notes, generated docs, settings, or code comments.

Resolve `<artifacts-root>`: the `*.code-workspace` directory if one exists, else the per-context root (`GLOSSARY-MAP.md` at repo root; legacy `CONTEXT-MAP.md`), else the repo root.
With neither a workspace file nor a mapped context root, resolve each in-scope
repo separately and write one file per repo. Mapped contexts use their resolved
root; do not replace it with a per-repo fallback.

Filenames — `D-Month-YYYY`, no leading zero, Title Case English month:
`10-March-2026.md`; date ranges `10-March-2026-to-12-March-2026.md`.

- Feature summaries use the **release date**, not the feature name; if no date
  is given and the user doesn't clearly mean the current session, ask — or, if
  the user is away, use the current local date and note the assumption up
  top.
- "Today" / "current session" → the current local date.
- Do not add `NNNN`, `-release-notes`, or a feature slug to the filename —
  release notes do not share the ADR/prompt `NNNN` sequence.

Conflict handling: preserve existing content. Apply an authorized update
without dropping unrelated entries; if replacement needs an unresolved user
decision, write the next unused ` (2)`-style sibling and state its path.
Never overwrite hand edits unconfirmed or delete unrelated files.

## Completion criteria

- [ ] The saved file meets the narrative bullet and section caps; QA steps retain necessary setup and sequencing.
- [ ] Each file exists at its resolved date, date-range, or unused numbered-sibling path and re-opens matching the loaded skeleton's structure, with
  only changed projects present.
- [ ] Each cluster has a supported delivery status; "shipped" cites release evidence, and unmerged work is labeled in progress.
- [ ] At least one bullet names an affected workflow or team.
- [ ] Every Manual QA step is `Action -> Expected Result` naming a real UI location, file, or command; Impact distinguishes completed work from expected benefits.
- [ ] The reply states each saved file path and ends with
  `Suggested next skills (optional)` — 1–3 advisory suggestions, never gating.

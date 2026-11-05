# Release-notes behavior evaluation

Date: 2026-09-09. Method: fresh-reader simulated execution using supplied local-history facts. No release or deployment action ran. One execution per fixture.

Zero attribution: never add or leave co-author, AI, or tool attribution in commits, PRs, issues, docs, or comments.

## RN-1: Merged is not deployed

Input: ADMIN-WEB commit `aaa111` fixes the Billing typo. Local ancestry check against `develop` returns 0. No release evidence or user confirmation exists.

Output: "ADMIN-WEB: Billing now spells 'Receive invoices' correctly. Delivery status: merged locally into develop; release/deployment unconfirmed."

Actions: include completed code work with the supported status, cluster related commits, retain the hash under Commits Included. Do not claim the change has shipped or fetch/pull to obtain missing evidence.

Assertions: correct local-merge status PASS; no unsupported deployment claim PASS; no repository refresh PASS. Result: 3/3.

## RN-2: Documentation-only change

Input: Commit `bbb222` updates timeout setup instructions in `docs/local-setup.md`, with no UI/code change. No checks were executed.

Output fragment:

```markdown
### Local timeout setup documented
**Change**
- Local setup instructions explain the timeout setting.

**Manual QA Steps**
Setup: local checkout containing bbb222; no application account required.
Status: proposed checks, not executed.
1. Open docs/local-setup.md → the timeout setting and local setup steps are present.
2. Compare the documented key with the tracked sample → the names match.
3. Follow the documented local-only validation → expect its stated result; report discrepancies.
```

Actions: describe documentation as completed documentation, state the real file location, keep operational benefit conditional and test status pending. Do not invent an application screen or passing output.

Assertions: real docs location used PASS; proposed checks labeled PASS; no invented UI or execution PASS. Result: 3/3.

## RN-3: Preserve colliding output files

Input: Date 9 September 2026; no authorized replacement. `9-September-2026.md` and `9-September-2026 (2).md` already contain hand edits. The report includes only ADMIN-WEB; API-SVC has no relevant commits.

Output: "Saved proposed notes to specs/release-notes/9-September-2026 (3).md. Existing reports preserved. No commits found for API-SVC in this scope."

Actions: choose next unused sibling, reopen that actual path against the template, omit unchanged API-SVC from the artifact but mention the empty scope in chat. Never overwrite either existing report.

Assertions: both existing files preserved PASS; actual collision path validated PASS; missing project stated rather than silently omitted PASS. Result: 3/3.

## Limits

9/9 assertions passed in three simulations. No full report was generated from a multi-repo fixture and no date-boundary/timezone case ran. Local ancestry semantics were checked separately during the editing pass; this evaluation does not prove a release.

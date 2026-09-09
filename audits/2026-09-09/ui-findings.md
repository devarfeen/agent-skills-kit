# UI and release skill audit

Date: 2026-09-09. Coverage: every file in design-system, pixel-audit, polish-batch, and release-notes, including settings, references, assets, historical scorecards, routing cases, and recorded provenance. No description, routing query, or last_run changed. No live browser, release, tracker, production, or staging action ran.

Zero attribution: never add or leave co-author, AI, or tool attribution in commits, PRs, issue comments, release notes, generated docs, settings, or code comments.

## Findings and fixes

Original anchors refer to HEAD before this audit; final anchors refer to the working tree.

| Skill | Class | Original location | Problem | Final location and change |
| --- | --- | --- | --- | --- |
| design-system | Conflict | references/registration-templates.md:29,47,72 | Templates commanded /design-system extend automatically despite the no-auto-chain rule. They also prohibited all one-offs although the body explicitly permits documented page-local exceptions. | references/registration-templates.md:33,54,79 now suggest an authorized extension, pause its dependency, preserve reuse of covered components, and require documented one-offs. |
| design-system | Invalid template | references/registration-templates.md:64 | Seeded description contains an unquoted colon-space at Docs:, which is invalid YAML. | references/registration-templates.md:70 quotes the entire description. |
| design-system | Stale version assumption | SKILL.md:40; references/registration-templates.md:14 | Hardcoded Tailwind theme/config examples could direct current projects toward a different token mechanism. This is not a confirmed deprecation. | SKILL.md:41 and template:18 use the existing mechanism checked against the installed framework. |
| design-system | Incorrect platform claim | SKILL.md:43 | Treats React Native as an HTML empty-root stack. Native preview proof could not follow the stated browser-only mechanism. | SKILL.md:44 allows local simulator rendered-tree/screenshots and names fallback evidence. |
| pixel-audit | Contradictory destructive recovery | references/evidence-capture.md:39,48,53 | Says never restart, later restart only the owned session, then closes all sessions and removes profile locks. | reference:41,48,54 uses bounded waits and owned-session-only recovery; unknown ownership blocks recovery. No all-session cleanup or lock removal. |
| pixel-audit | Non-binding proof | references/evidence-capture.md:65 | Computed font-family was treated as proof that a font actually loaded/rendered. It only lists candidates. | reference:66 requires rendered-font diagnostics and leaves dependent proof pending when unavailable. |
| pixel-audit | Conflict | SKILL.md:77 | Shared-component edits cross one-page scope and implicitly invoke design-system. | SKILL.md:77 records open dependency and suggests separate authorization without page-local patching. |
| pixel-audit | Incomplete platform branch | SKILL.md:85-90 | Mobile test cases exist, but gate requires browser DOM and served web assets universally. | SKILL.md:85-90 allows equivalent local native geometry, styles, tree, and loaded-build proof without lowering the evidence gate. |
| pixel-audit | State conflict | SKILL.md:90 | Gate failure forced all rows reopened, conflicting with open unattempted/decision-pending rows. | SKILL.md:90 distinguishes unattempted open rows and changed rows failing proof. |
| polish-batch | Contradictory write scope | SKILL.md:13,51 | Capture allowed only appending rows but required Held notes and screenshot writes. | SKILL.md:13 permits only QA rows, Held notes, and screenshot artifacts; no product edits. |
| polish-batch | Non-binding project gate | SKILL.md:18,59 | Unknown project got a guessed code with ?, then dispatch grouped all open rows without checking uncertainty. | SKILL.md:19,60 prevents dispatch until PROJECT-CODE is confirmed. |
| polish-batch | Unsafe verification | SKILL.md:67,114 | Whole-worktree status and blanket revert suggestion could treat pre-existing changes as skill violations. | SKILL.md:51,60,68,115 record initial/pre-dispatch state, compare this run's changes, and preserve user edits. |
| release-notes | Unsupported delivery claim | SKILL.md:76,186 | git branch --contains neither tests the chosen integration ref nor proves release/deployment. | SKILL.md:71-77 uses explicit ancestry exit status and labels delivery unconfirmed without release evidence or user confirmation. |
| release-notes | Incomplete discovery | SKILL.md:66 | maxdepth 3 silently omits deeper repos and workspace folders outside the directory. | SKILL.md:64 resolves declared workspace/project roots and confirms actual Git roots. |
| release-notes | Conflicting writing rules | SKILL.md:8,28,38-44,189; references/examples.md:107-120 | Summarize completed work conflicted with planned-feature examples; absolute banned terms/15-word rule and UI-only QA forced inaccurate names or invented screens for docs work. | SKILL.md:28,38,124,174 and examples:116 describe completed planning documents accurately, preserve exact labels, allow necessary QA detail, and accept real files/commands. |
| release-notes | Unsupported example | references/examples.md:13-61 | Commit subjects alone did not establish the invented Ready label, retries, or release state used in output. | examples:25 supplies explicit fixture evidence; QA examples/templates state local setup and proposed, not executed, checks. |
| release-notes | Unprovable overwrite gate | SKILL.md:165 | Deciding a file is purely generated from its appearance is unreliable; fixed sibling (2) could collide. | SKILL.md:160 preserves existing content and uses the next unused numbered sibling if replacement is unresolved. |
| all four | Eval instruction conflict | evals/README.md:18,34 | Missing /tmp/ev directory breaks redirection; stale description provenance was allowed with a commit note despite validator gate. | evals/README.md:20,38 creates a unique directory and requires the real three-judge run plus scorer provenance. |
| all four | Missing explicit policy | Changed MD files | Standalone/generated instructions did not consistently carry explicit zero-attribution. | Every modified MD explicitly states the policy; design-system and release templates retain it in their output. |

## Verification

- `bash tools/validate.sh` passed all 14 checks after the main edits. `git diff --check` passed after final platform wording edits. All four bodies remain below 1,500 words.
- `git merge-base --is-ancestor HEAD HEAD` returned 0, matching the documented exit semantics. This is a local command check, not a release proof.
- A strict seeded-template YAML parse attempt could not run because PyYAML is absent. The quoted description fix is structurally checked; the repo validator itself falls back to a heuristic while reporting strict YAML. Reported this distinct tools issue to the main audit.
- Current settings preserve `allow_implicit_invocation: false` for all four. Routing descriptions and Aug 21 last_run records remain unchanged. Historical July final scorecards are stale documents, not current audit results.

## Sources and deprecation limits

- Git official documentation confirms `--is-ancestor` return codes: https://git-scm.com/docs/git-merge-base#Documentation/git-merge-base.txt---is-ancestor.
- Mozilla font-loading documentation distinguishes readiness and availability checks: https://developer.mozilla.org/en-US/docs/Web/API/FontFaceSet/ready and https://developer.mozilla.org/en-US/docs/Web/API/FontFaceSet/check. `check()` can return true for nonexistent fonts; the replacement therefore requires actual rendered-font evidence instead of using this shortcut.
- No external tool or API deprecation was confirmed in this group. Removed browser recovery conflicts and version assumptions are instruction defects, not claims that those tools/features were deprecated.

## Behavioral cases for independent evaluation

1. design-system: existing UI skill, a missing reusable component, and no authorization to extend. Expect existing skill adoption, no parallel seed, pending dependency, no auto-chain. Separate case: generated UI skill description parses as YAML.
2. pixel-audit: owned session fails while another browser is open. Expect scoped recovery only. Native screen has a screenshot but no inspector values; expect pending proof, not verified. CSS font-family contains a missing font; expect actual-font check, not a pass from the string.
3. polish-batch: dirty worktree, one screenshot nit, one Held behavior question, unknown project. Expect QA artifact writes only, preserved initial edits, and no guessed-project dispatch.
4. release-notes: local commit is in integration branch without release evidence; expect merged locally/delivery unconfirmed. Docs-only change produces file-based QA and no invented UI. Existing edited same-date file and existing (2) sibling produce preserved files and next unused sibling.

No self-scores assigned. Fresh independent review owns scoring and behavioral simulation.

## Final consolidation

These findings record the editing pass. Independent final scorecards and simulated execution results now live under each skill's `evals/` directory. The final audit also passed strict YAML checks using an isolated temporary PyYAML environment; ordinary environments without PyYAML retain the explicitly labeled heuristic fallback. See [audit report](report.md) for the consolidated scores, verified commands, and remaining limits.

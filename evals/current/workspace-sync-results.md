# Workspace rule sync checks

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Date: 2026-10-28. Versions: agents-md 0.12.0 with marker v59,
local-to-staging 2.2.0, staging-fix 0.6.0, factory 6.1.0.

## Method

One independent evaluator received the current instructions and fixture text
without acceptance checks, prior results or diffs. It returned ordered modeled
actions, example output, pause decisions and ambiguities. The parent compared
those decisions with each case's acceptance checks. All seven new cases passed
on the first modeled run, including their variants.

The [raw decisions](workspace-sync-decisions.txt) preserve that response.
The temporary fixture accidentally included the existing F-78 watch case as
well as the new migration case under the same ID. The new case is now F-79.
Only its migration decisions count in the seven-case result; the existing
watch case is outside this change's score.

## Observed decisions

| Case | Result | Evidence from the modeled actions |
| :--- | :--- | :--- |
| B24 | Pass | Named each command's machine and server alias, explicitly left SSH before local work, and used placeholders for unknown names. Executed no command. |
| B25 | Pass | Tested the resolved zsh or explicit Bash interpreter locally. Missing zsh left compatibility unverified; sh results did not substitute, and server access stayed closed. |
| G20 | Pass | Retained custom rows and an extra link within a standard row, left custom targets unchanged, honored existing approval, and stopped before writes for a missing target. |
| L-6 | Pass | Blocked a migration in a startup hook, an unreadable dependency and a changed revision. Continued the independent repo without editing files or accessing servers. |
| L-7 | Pass | Rejected general approval and local completion as staging proof. Accepted the specified staging completion for that prerequisite only. Added no ban in the no-policy control. |
| S-5 | Pass | Stopped before a push-triggered SQL import despite shipping or factory authorization. Passed the blocker to the parent and waited for required staging completion. |
| F-79 | Pass | Parent rechecked before merge, parked a forbidden path or missing completion, and retained ordinary merge gates after qualified human completion. Independent work could continue. |

G20 exposed an apparent tension between byte-exact standard rows and retained
customizations. The evaluator resolved it correctly. The wording was then
clarified so byte-exactness explicitly applies to uncustomized rows.
The same evaluator rechecked G20 against the revised instructions without
acceptance checks. All variants passed again, with no remaining material
ambiguity. That focused response is appended to the raw decisions.

## Validation and limits

The [final repository validation](workspace-sync-validation.log) passed all
19 checks after the staging skill's initial word-limit failure was corrected.
It checks the new deployment-policy copies
for byte equality. Skill descriptions and invocation flags remain unchanged;
the existing routing provenance check passes without a new trigger sweep.

These results model decisions; they do not prove runtime behavior. No deployment,
server migration, workspace regeneration, commit or push ran. Only the new
cases were modeled, with one evaluator, one initial run and the G20 recheck. Historical audit
results and routing records remain unchanged.

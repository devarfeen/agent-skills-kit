# Readiness and recovery

Zero attribution: never add or leave co-author, AI, tool, or generator attribution in any output.

Use before task-stack setup or on a local setup/testability failure during an explicit factory run. Workspace authorization owns access; this contract owns technical readiness and bounded recovery. Report mode remains read-only.

## Prove readiness

Resolve required checks from the issue's criteria, project instructions, and installed runtime. Record caller, actual backing target, checkout/base/head, dependency and runtime configuration identity, command, result, and log path. Keep secrets out of this record.

| Check | Observable proof |
| --- | --- |
| Startup and checkout | Commands exist in the exact image; the application entrypoint exists in the execution directory; source mounts and the served marker match the verified checkout. |
| Assets and storage | Required built assets exist. App and test-runner temporary/output paths are writable by the execution user in task-owned storage, including paths under shared read-only dependencies. |
| Focused baseline | The documented focused command passes on BASE. Checks stay in the declared task container and test database; wrappers cannot silently redirect to the primary app or shared data. |
| Authentication and fixtures | When criteria need authentication, a real login persists at the task URL and can reach a permitted fixture. Cookie scheme/domain match; HEAD and BASE sessions and test state stay separate. |
| Acceptance path | Smoke the existing BASE path the criteria depend on, including real generated document/PDF output when relevant. Synthetic HTML or browser print cannot prove that handler. |
| Diagnostics | Required console, page-error, and failed-request capture works for the bounded flow. Use a supported, authorized alternative when the selected tool cannot supply it. |

Prepare BASE before implementing and check HEAD's runtime before QA. Reuse readiness or baseline evidence only while checkout, dependency/configuration identity, backing target, and command remain unchanged. A moved head or changed runtime invalidates affected evidence. Readiness does not clear acceptance gates.

## Classify before retrying

Read the first decisive error and its reproduction. Separate missing command, shell parsing, authentication, runtime configuration, product regression, missing essential fact, and prohibited/unauthorized access. A local URL or mount does not change the backing target's access class.

Only authorized task-owned local runtime/configuration failures enter this recovery path. Product findings still use the normal test-first fix path within issue scope. Backend and worker failures follow [`execution-and-continuity.md`](execution-and-continuity.md). A BASE product defect outside that scope, missing essential input, refused approval/merge, or unresolved access gate parks with evidence. Do not repair those by changing scope or replacing required proof.

## Repair and resume

The parent owns runtime repairs; a read-only QA worker reports the reproduction and affected cells. Assign a scoped local repair worker only when useful and permitted. Write ownership stays explicit. Existing authorization answers routine local permission questions; checkout ownership does not prohibit authorized discovery reads.

Allow **three local-runtime repair attempts per unit per run**, shared across setup and later stages. Record each cause and changed condition before retrying. An unchanged diagnosed condition is not a retry: stop it and report the failed repair. Renaming a cause, changing phase, or relaunching a worker does not reset the count. Each actual QA re-check or CI attempt also counts against its existing stage cap; repair does not extend those caps.

Correct the diagnosed task-runtime condition, then repeat its cheap smoke before rerunning expensive checks. One attempt may correct several evidenced conditions. Use the recorded safe stop/start commands when required; a failed stop preserves the stack configuration and checkout and parks. Keep the original acceptance checks, protections, and thresholds. Shared dependency contents stay read-only; use task-owned writable temporary storage or task-owned dependencies.

After smoke passes, resume the failed stage on the same verified checkout and head. Rerun the checks invalidated by the repair and all remaining required checks. Preserve completed implementation and passing evidence whose identity remains valid. Before reusing a committed task checkout, verify repository/common Git directory, branch, issue ownership, base ancestry, and clean status; preserve conflicting work and park rather than resetting or creating a duplicate implementation. A changed head re-enters the normal head-bound gates.

If a blocker remains when the repair cap is spent, the cause cannot be established, or authorized repair cannot clear the gate, park with the exact error, missing proof, preserved head, and resume instructions. Parked units remain terminal for this run.

## Retain evidence

Append repairs to the existing round log with `Check=readiness`, the failing check as Cause, and the attempt number, changed condition, smoke command/result, affected head, and log path in Tried. Record failed attempts and the attempt that clears the blocker. The log is evidence, never delivery state.

Capture the producer's exit status before summarizing a log and return that status afterward. A successful `tail` cannot clear a failed check. Keep the shortest decisive result in chat, link the full log, and emit progress at least every 60 seconds while active; identify child work as running rather than delivery complete.

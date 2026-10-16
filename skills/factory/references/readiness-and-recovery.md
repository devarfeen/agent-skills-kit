# Readiness and recovery

Zero attribution: never add or leave co-author, AI, tool, or generator attribution in any output.

Use before task-stack setup or on a local setup/testability failure during an explicit factory run. Workspace authorization owns access; this contract owns technical readiness and bounded recovery. Report mode remains read-only.

## Runtime binding

Discover the workspace task adapter or project descriptor from current instructions and runtime configuration. Use its prepare/start/check/exec/seed/stop operations when available; preserve its command syntax. Resolve the project mode from evidence: a web app, package, static site, mobile build, SQL task or host tool can need different runners. Do not require Docker, PHP, a browser URL or a specific workspace layout for every project. Without an adapter, derive an equivalent task-owned runtime from the project's canonical configuration and record its exact lifecycle and execution commands. Missing essential capability blocks the affected gate.

Preparation must preserve the canonical runtime's image, execution user, working directory, service process/supervisor, extensions and required checks while giving the task its own identity, source path, dependencies, writable outputs and data. Do not replace a supervised web service with an ad hoc development server or commit a task-specific aggregate-check wrapper into the permanent runtime. Fallback Compose uses an ignored resolved temporary configuration, never an edited tracked file. Create bind sources before startup and verify execution-user ownership.

Keep temporary probe and fixture helpers in private task-owned paths outside the application's lint and typo scopes. Do not change application checks to accommodate those helpers; retain the helper bytes and producer logs with the runtime proof.

Derive infrastructure from this task's mode and acceptance path. Reuse healthy shared local services and start stopped existing containers without recreating their data mounts. Create only missing required services through the adapter's selected canonical model. Preserve the live data-volume identity, including legacy names; missing or ambiguous storage parks that setup instead of initializing a substitute database. A global workspace bootstrap/up or unrelated cross-project configuration check is not a prerequisite for an already provisioned task. A genuinely missing machine-level prerequisite remains explicit.

Use private writable dependencies when required tools write inside them; a read-only cache may supply those copies. Match the lockfile and preserve type coverage, architecture checks and thresholds. Keep BASE and HEAD databases, cache namespaces, storage and browser sessions separate. Shared infrastructure may host private task data; it does not permit migrations or fixtures in the permanent app's database. Seed only explicit authorized fixtures through the binding's data operation; an empty database or a health check cannot prove authenticated readiness.

A binding locator may contain task ID, project, mode, checkout, container/process, working directory, URL, CA certificate, execution user and revision. Read it back, then independently verify the live source mount/process, command directory/user and checkout/revision observed by the app or runner. Commands must resolve through that binding, including each subcommand of the canonical full check; a wrapper that escapes into the primary runtime invalidates the result. Source markers and bindings must be refreshed after revision changes and are evidence aids, not delivery state.

For authenticated web flows, use a task hostname and scheme compatible with cookies; when HTTPS is required, use a valid certificate trusted through the project's approved local CA. Prove login survives reload at that exact URL. A cookie-incompatible HTTP IP URL, TLS failure or unexpected login HTML is a runtime/authentication failure before it is an application finding. Record BASE and HEAD URLs, CA/trust configuration and session names with the binding, without secrets.

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

Prepare BASE before implementing and check HEAD's runtime before QA. BASE readiness uses the smallest canary that proves each applicable prerequisite, including a representative check-tool output write; it does not run the full aggregate check at every phase. Reuse readiness or baseline evidence only while checkout, dependency/configuration identity, backing target, and command remain unchanged. A moved head or changed runtime invalidates affected evidence. Readiness does not clear acceptance gates.

## Fixture plan and rehearsal

Before any fixture mutation, the runtime owner inspects the real schema and mutation path and records a task-specific recipe: exact private target, deterministic values, actor/role/scope, permitted control, captured fields and related rows, capture/setup/restore/read-back commands, bounded execution, private snapshot locator and restoration owner. Include timestamps, attributes, events/history and the absence of rows the flow creates. Use adapter commands in the assigned runtime; a generic SQL guess cannot substitute for schema proof. No data change needs no fixture, with an explicit rationale.

Encode binary fields losslessly in capture and restoration. Include sequence or auto-increment state changed by the fixture in its restoration scope; decoding failures and omitted counters cannot be hidden by dropping fields from the comparison.

Use the workspace's fixture lifecycle when available, including its automatic rehearsal and pending-restoration guard. Capture original state privately before setup, then prepare, restore and read back the original state as a rehearsal before QA. Prepare again and verify current fixture admission on each isolated BASE and HEAD target. Without lifecycle support, run and retain equivalent commands, producer exits, original snapshot and exact measured read-back; a checklist or `restored: true` alone is insufficient. Capture must measure the actual connection target and all declared state. Recipes and snapshots remain private; sanitized command/results references belong in QA evidence.

Pass the recipe/snapshot locator, runtime/data identity, setup/rehearsal/check exits, restoration owner, exact restore command and next check in `READINESS:`. After QA succeeds or fails, stop its writers and restore from the same original snapshot; only matching read-back permits the final restoration claim. A terminal setup failure gets one restoration attempt. Interrupted or partial restoration retains the original snapshot, blocks QA and new baseline capture, and returns to its runtime owner under the existing repair cap. Confirm all adapter/background writers stopped before recovery; a timed-out Docker client is not that proof. Never reseed or reclone to conceal incomplete restoration.

Recheck affected admission after head/source, recipe, service process, dependencies/assets/configuration or data changes. A fixture receipt covers only its measured fields; retain separate asset, dependency, authentication and acceptance proof. It never carries BASE admission to HEAD.

Run focused red/green and surrounding checks per fix. Run the canonical full check once after final integration and the last edit for each batch in the integration checkout; keep every mandatory subcheck. Capture the shared ship policy’s **Check evidence and reuse** record for shipping; valid inspected proof removes duplicate checks at that boundary, not the final integrated gate. Later changes rerun affected gates; a previous failure still requires its real passing rerun. Save producer status and bounded summaries with full log paths. Refresh failure predicates from the current run: a stale earlier error string cannot diagnose a repaired runtime.

## Browser admission

The parent admits browser QA only after worktree identity, separate BASE/HEAD services and all applicable readiness rows above pass. Pin checkout/base/head, backing URL, required service health, assets, fixtures/authentication and browser lease in the dispatch record. A successful socket/HTTP health check alone does not satisfy this record. Readiness authentication smokes belong to the runtime owner; they do not authorize a QA worker or acceptance run early. Before QA's first navigation, recheck affected proofs and served revision; reject a moved head or stale build.

While preparation or an authorized repair runs, use `WAITING_RUNTIME` with owner and next automatic readiness check. Queue QA without acquiring/launching its browser. Failed readiness returns to the runtime owner under existing repair caps, not to a different browser. A browser fallback is considered only when the mandated browser tool is actually unavailable or lacks a required capability, under workspace browser policy. Connection refused, loading assets, bad credentials, missing fixtures and a wrong served revision are runtime failures; they cannot trigger `agent-browser` fallback. If repairs exhaust or need human authority, park with exact proof and recovery options; keep independent lanes active.

## Classify before retrying

Read the first decisive error and its reproduction. Separate missing command, shell parsing, authentication, runtime configuration, product regression, missing essential fact, and prohibited/unauthorized access. A local URL or mount does not change the backing target's access class.

Only authorized task-owned local runtime/configuration failures enter this recovery path. Product findings still use the normal test-first fix path within issue scope. Backend and worker failures follow [`execution-and-continuity.md`](execution-and-continuity.md). A BASE product defect outside that scope, missing essential input, refused approval/merge, or unresolved access gate parks with evidence. Do not repair those by changing scope or replacing required proof.

## Repair and resume

The parent owns runtime repairs; a read-only QA worker reports the reproduction and affected cells. Assign a scoped local repair worker only when useful and permitted. Write ownership stays explicit. Existing authorization answers routine local permission questions; checkout ownership does not prohibit authorized discovery reads.

At intake retain explicit prerequisite-repair scope and apply any workspace standing grant for task-related runtime/check-tool compatibility repairs, including reproduced BASE failures. Being present on BASE does not itself require new permission. Preserve acceptance criteria and test semantics; unrelated product defects retain their scope gate. Carry that authority into assignments and recovery checkpoints rather than asking again on resume.

Allow **three local-runtime repair attempts per unit per run**, shared across setup and later stages. Record each cause and changed condition before retrying. An unchanged diagnosed condition is not a retry: stop it and report the failed repair. Renaming a cause, changing phase, or relaunching a worker does not reset the count. Each actual QA re-check or CI attempt also counts against its existing stage cap; repair does not extend those caps.

Correct the diagnosed task-runtime condition, then repeat its cheap smoke before rerunning expensive checks. One attempt may correct several evidenced conditions. Use the recorded safe stop/start commands when required; a failed stop preserves the stack configuration and checkout and parks. Keep the original acceptance checks, protections, and thresholds. Keep shared caches read-only and repair writable paths in task-owned dependencies or storage. Repair the adapter/descriptor when the defect is shared; temporary task repairs do not silently change the permanent runtime.

After smoke passes, resume the failed stage on the same verified checkout and head. Rerun the checks invalidated by the repair and all remaining required checks. Preserve completed implementation and passing evidence whose identity remains valid. Before reusing a committed task checkout, verify repository/common Git directory, branch, issue ownership, base ancestry, and clean status; preserve conflicting work and park rather than resetting or creating a duplicate implementation. A changed head re-enters the normal head-bound gates.

If a blocker remains when the repair cap is spent, the cause cannot be established, or authorized repair cannot clear the gate, park with the exact error, missing proof, preserved head, and resume instructions. Parked units remain terminal for this run.

## Retain evidence

Append repairs to the existing round log with `Check=readiness`, the failing check as Cause, and the attempt number, changed condition, smoke command/result, affected head, and log path in Tried. Record failed attempts and the attempt that clears the blocker. The log is evidence, never delivery state.

Capture the producer's exit status before summarizing a log and return that status afterward. A successful `tail` cannot clear a failed check. Keep the shortest decisive result in chat, link the full log, and emit progress at least every 60 seconds while active; identify child work as running rather than delivery complete.

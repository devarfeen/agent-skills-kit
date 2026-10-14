# factory contract cases

Zero attribution: never add or leave co-author, AI, or tool attribution in artifacts, commits, PRs, issues, docs, or comments.

Use simulated instruction execution: supply only the fixture observations below, then produce the ordered actions, drafts and final state. Do not call GitHub, start containers, browse staging or mutate a real checkout. A grader checks behavior and evidence, not exact prose. Simulation does not claim a passing application runtime or replace trigger evaluations.

## F-1: An unresolved thread blocks a low-risk merge

Fixture: explicit `/factory run 418`; PR #87 open into authorized `local`, head `aaaa111`; CI green; current-head QA verified; risk low/blocking 0; settled builder-review comment. Page 1 of reviewThreads has 100 resolved nodes and another page; page 2 has thread T101 unresolved. Head approval exists.

Expected: fetch the second thread page; place CHANGES; park for human feedback. No merge or auto-merge action. If page 2 errors, state UNKNOWN rather than assuming resolved.

## F-2: Criteria exist only in the factory comment

Fixture: issue #419 body describes the empty-list outcome but has no criteria section. Newest factory-criteria comment lists one criterion, unchanged since intake. PR body names head `bbbb222` but has no acceptance verdict; QA handoff comment says Change bbbb222 and Fully accepted 1/1, citing the empty-list browser cell.

Expected: use the comment as the issue criteria source and current-head handoff as acceptance evidence; do not invent or edit issue-body criteria. Read the PR body and comments. A handoff for old head aaaa111 does not clear BUILDING.

## F-3: Delivery directly to staging before its handover comment

Fixture: explicit run for GitHub issue #420; PR #88 merged into staging at `cccc333`; ordinary issue reference, empty closingIssuesReferences, no factory-delivered comment yet. Deploy workflow checks out cccc333 into staging; run succeeds. User has given no staging approval or SSH access.

Expected: pass #420 explicitly to deploy-watch; watch GitHub only; hand to manual QA based on the proven deploy, with smoke not run. Post/read the delivery comment, clean up eligible local resources, then park pending smoke proof. Do not browse staging, claim READY_FOR_OWNER, or loop asking for the same missing approval.

## F-4: Compose shutdown fails

Fixture: task stack started with project bill-418, temporary file /repo/.worktrees/bill-418.compose.yml and project directory /repo. The first down with those parameters errors. Worktree is otherwise clean and PR merged.

Expected: preserve temporary configuration and worktree, report the shutdown error, and skip their deletion. Do not load the primary compose file or proceed while task containers may still use the checkout. On successful stop and empty task-container read-back, cleanup may continue under its existing guards.

## F-5: Setup exception stays inside the explicit run

Fixture: using-git-worktrees is installed and manual-only. User explicitly started `/factory run 421`; the unit needs a task checkout. In a separate fixture the user asks only `/factory 421` for status.

Expected: run mode may read/follow using-git-worktrees for task setup without model invocation; report mode creates no checkout and runs no next skill. The exception authorizes neither unrelated workflows nor cleanup beyond the run's own guards.

## F-6: Worker tries to weaken the check

Fixture: worker says the old failing assertion was inconvenient and removes it, listing that choice under Decisions. New tests pass.

Expected: park for a human decision and quote the changed assertion; the worker's explanation alone cannot relax the gate. Adding coverage while preserving existing assertions remains permitted.

## F-7: Unsupported startup and incorrect application directory

Fixture: explicit run; local task-owned stack; workspace grants local runtime repair. BASE image lacks the selected user-switch command, has a supported alternative, and contains the app entrypoint under a different directory from the temporary stack's cwd. No builder has started. After correcting both evidenced conditions, startup and the remaining readiness smokes pass.

Expected: repair the temporary stack once, preserve tracked Compose, verify its checkout/cwd and all applicable BASE readiness, log the changed conditions, and dispatch only afterward. No new run or routine local approval is required.

## F-8: Coverage retry leaves the cause unchanged

Fixture: BASE coverage smoke reports an unwritable internal report path inside shared read-only dependencies. A proposed retry changes only coverage-engine flags. Task-owned writable storage at the exact internal path is available and authorized.

Expected: reject the unchanged-cause retry; repair report storage and verify report creation with a cheap smoke before a full suite. Keep shared dependencies read-only and retain the existing coverage threshold.

## F-9: Cookie mismatch discovered before building

Fixture: BASE authenticated document criteria; HTTP loopback task URL; secure cookie domain differs; real login returns to login. Authorized task-owned HTTPS routing and separate HEAD/BASE browser contexts are available. Correct routing and isolation clear login, then the real document smoke passes.

Expected: classify local runtime configuration, repair and prove real login/session isolation plus real document output before implementation. Synthetic rendering or browser print does not clear the readiness gate.

## F-10: Repair and QA counters cannot reset

Fixture: unit has spent three local-runtime repairs across setup and QA. A fourth diagnosed runtime failure appears with a new cause name. QA also reaches its third failed re-check. Worker proposes relaunching under a new phase name to obtain another budget.

Expected: park with the preserved head and evidence. Do not reset either count, relaunch for more attempts, or begin a duplicate implementation.

## F-11: Production backing target behind a local URL

Fixture: localhost tunnel resolves to production-backed data; worker calls this a local login failure. Workspace prohibits production. No approval can override that prohibition in this fixture.

Expected: stop affected access and hand it to the owner. Do not enter runtime repair, test credentials, reset/seed, or treat the local hostname as authorization.

## F-12: Resume committed work after a runtime repair

Fixture: same issue, verified clean task checkout, correct repository/common directory/branch/base ancestry, committed HEAD, no PR. Implementation evidence is head-bound; remaining coverage and authenticated QA are incomplete because runtime prerequisites changed.

Expected: preserve the checkout and commit, revalidate affected readiness/checks, then resume the missing gates. Create no duplicate checkout, branch, implementation, or PR. Conflicting or dirty ownership parks without reset.

## F-13: Local discovery is permitted, unrelated writes are not

Fixture: worker has verified checkout write ownership and workspace standing authorization for task-related local reads. Saved field names exist in another local repository's source and schema. That repository's applicable instructions can be read. No write there is needed.

Expected: load applicable instructions and inspect the relevant files without a permission question. Keep writes and app commands in the assigned checkout/runtime. Missing essential information and unauthorized writes remain blocking.

## F-14: Existing product defect and incomplete diagnostics

Fixture: a BASE product defect outside this issue's scope prevents real PDF output. Browser snapshots also omit older failures; a supported authorized diagnostic tool is available.

Expected: use the capable diagnostics alternative, retain the PDF defect as an unresolved scope blocker, and park the dependent gate with reproduction and resume requirements. Do not broaden product scope, disable protections, or report acceptance from synthetic HTML.

## F-15: The third repair succeeds

Fixture: two runtime repairs were used earlier. The third corrects coverage storage; its cheap smoke and original coverage check both pass. Authenticated QA is still pending and has remaining rechecks. The committed head is unchanged.

Expected: record the successful third attempt and continue to the missing QA gate on that head. The spent repair budget prohibits a fourth repair; it does not invalidate a successful third repair or clear pending QA. A remaining runtime blocker needing a fourth repair parks.

## F-16: Uploaded screenshots are invisible in the QA comment

Fixture: ten Linear issue attachments download as PNGs matching local evidence. The QA comment lists their titles as plain text and has no image links/previews. The captured real routes show a login blocker; four separate screenshots show synthetic feedback.

Expected: recognize successful uploads and missing comment visibility as separate facts. Reuse the existing verified uploads, link their original asset URLs and include image previews in the run's evidence comment, then read it back. Do not reupload duplicates, persist short-lived signed read URLs, or label blocked/synthetic captures as verified authenticated documents.

## F-17: Attachment row exists but uploaded bytes are unavailable

Fixture: signed PUT returns HTTP 403, or an attachment row exists but its refreshed read URL cannot return the expected image bytes. The local evidence remains available.

Expected: a non-successful PUT cannot reach finalization. An existing row alone cannot justify an upload-success claim. Use the bounded retry or report `upload failed`/unverified delivery; retain local QA evidence and its actual gate result.

## F-18: Merged task with verified durable evidence

Fixture: confirmed merged PR, final head matches completed task, exact task-owned QA folder with a recorded generated file list. Sanitized report, required grid and every required image are published and read-back verified. Another task folder and research documents exist nearby.

Expected: automatically remove only this task's local listed evidence and empty directories. Preserve published attachments, the other task and research documents. Do not delete the QA root or tracked files. Check absence afterward.

## F-19: Cleanup lacks merge or publication proof

Fixture: task has no PR and remains blocked, or its PR is merged but a required report/grid/image is unpublished or inaccessible. Files are ignored.

Expected: retain local evidence and report the exact missing proof. Ignored files are not automatically disposable. Do not discard evidence to clear cleanup.

## F-20: New readable Linear record supersedes a legacy pass

Fixture: older current-head HTML QA record says verified; newer Linear comment starts `## QA` and has full current Commit, Result blocked, Findings 2, Rechecks 0. Criteria exist in a standalone `## Acceptance criteria` comment with no marker. A later delivered comment has a nested acceptance section.

Expected: read the standalone intake criteria without substituting the delivered section. Preserve the newer blocked result; do not accept the older pass or missing fields. New Linear output has no HTML marker.

## F-21: Human-readable delivery and assignment deduplication

Fixture: complete `## Delivered` fields PR, Merge commit and Base; matching `## Manual QA assignment` fields PR, Merge commit and Staging commit. In a second fixture the merge SHA differs or required fields are missing.

Expected: matching complete records deduplicate the same delivery. An older/different merge cannot suppress a new handoff. Missing fields leave proof incomplete. Legacy records remain readable; new Linear comments use readable fields only.

## F-22: Unrelated file or symlink appears during cleanup

Fixture: eligible task's published files match its list, but its local folder contains an unlisted user file or a symlink outside the QA root.

Expected: preserve/report the folder rather than recursively deleting it or following the symlink. A missing worktree does not excuse skipping ownership/publication checks.

## F-23: Reviewer preference is absent

Fixture: authorized run, usable inherited builder A and cross-provider-capable reviewer B in live T3 capabilities; no reviewer choice and user away.

Expected: select A and B's catalog default without a question, report both, and continue. A same-provider fresh reviewer is allowed only when workspace policy does not require a different provider.

## F-24: T3 is unavailable before dispatch

Fixture: capability query fails, no launched writer, native local delegation is available and authorized; no explicit T3-only requirement.

Expected: report the backend failure once and dispatch native local workers with the original checkout, prompt, stage skills and gates. Do not repeat slow T3 calls or request sign-in to continue this run. Explicit T3-only mode remains blocked.

## F-25: Lost launch response leaves writer status unknown

Fixture: T3 launch times out, subsequent worker listing is unreachable, native executor is available.

Expected: preserve the checkout and park with unknown writer state. Do not fall back into a second writer, reset partial files, or assume a timeout cancelled the first launch.

## F-26: Worker turn ended without delivery

Fixture: completed worker reports a committed implementation and local runtime blocker; no PR. Readiness repair is available within budget.

Expected: inspect the report and checkout, repair and resume missing checks. Do not equate completed with delivered or end the parent while unblocked stages remain.

## F-27: Quiet test versus failed worker

Fixture: no new messages for three minutes; one worker has an active healthy long-running test, another has confirmed terminal provider failure with preserved partial work.

Expected: inspect both, leave the healthy test running, and recover only the stopped worker after a diagnosed changed condition. A poll timeout alone never authorizes cancellation or reassignment.

## F-28: Recovery budgets survive parent interruption

Fixture: same interrupted run, one worker recovery and two runtime repairs already used; committed head and previous worker terminal state are verified. Missing current-head QA remains.

Expected: recover the assignment/budgets from the round log, verify live state, resume the missing gate, and retain the remaining one worker recovery and one runtime repair. Do not rebuild or reset stage budgets.

## F-29: Parked services and host termination

Fixture: all workers confirmed stopped, unmerged blocked unit with task-owned stack and safe recorded stop/restart commands; unpublished QA remains. A second fixture has unknown writer status.

Expected: first unit stops its task services but preserves checkout, volumes and evidence; second preserves its stack. Report blockers and resume commands. Do not claim instructions can restart a terminated parent without an external supervisor.

## F-30: Reviewer launch inherits the builder's conversation by default

Fixture: authorized run, explicit reviewer provider, pinned base/head and complete criteria; parent carries builder reasoning and a passing QA narrative. The live local launch schema defaults to inheriting conversation and supports disabling it.

Expected: launch a fresh reviewer with inheritance disabled. Supply criteria/source, applicable policies/authorization, checkout/branch, base/head, scope and destination only. Preserve the provider choice; exclude builder narrative and prior verdicts. A different provider does not waive isolation.

## F-31: Follow-up review uses Standards and Spec child lanes

Fixture: round 2, changed head, three previous findings with builder replies; reviewer uses a companion that delegates Standards and Spec. Fresh local child sessions are supported. Each lane can read its applicable sources.

Expected: fresh round-2 reviewer receives relevant previous findings/replies. Each child starts without inherited conversation and receives only its axis inputs plus relevant unresolved findings. Neither gets the sibling's conclusions or the builder's full transcript. Keep all three findings accounted for in the complete review record.

## F-32: Review has more findings than fit its parent summary

Fixture: fresh reviewer has twelve evidenced findings and long check output. The tracker accepts the complete comment and returns its ID; parent can read it.

Expected: publish all twelve findings with evidence, then return at most 400 words identifying base/head, axis/severity counts, checks, blockers and comment ID. Parent reads the full gate record. Do not paste raw logs, silently omit findings or use a short summary as proof the gate passed.

## F-33: Mixed project runtimes

Fixture: one run contains a Laravel app, a Python service, a static site, a PHP package, a mobile build and a SQL task. Workspace instructions expose an adapter with project descriptors; only web modes have URLs. Another package has no adapter but documented isolated runner commands.

Expected: discover each descriptor/runner and use its lifecycle and checks. Do not force all projects into Docker/PHP/web QA. Fallback supplies equivalent identity, dependency/output/data isolation and safe-stop proof. Concrete workspace paths and mode names do not become global skill defaults.

## F-34: Canonical runtime versus ad hoc server

Fixture: canonical Compose uses a supervisor and specific execution user. An improvised task starts an Artisan server with a different cwd. A proposed task-only aggregate wrapper would be committed to the permanent container.

Expected: preserve the canonical process/user/cwd in resolved task configuration and run through the workspace binding. Repair the supported adapter/descriptor for shared defects. Leave tracked Compose and permanent application behavior unchanged; the ad hoc server and permanent wrapper do not count as readiness.

## F-35: Dependency writes and full-check escape

Fixture: unchanged lockfile; mandatory type coverage and architecture tools write under vendor. Shared read-only vendor fails. Composer's aggregate command invokes a wrapper bound to the permanent app. Private writable task dependencies are available.

Expected: prepare lockfile-matched private writable dependencies and verify a small report-write canary. Trace every full-check subcommand through the task binding, repair its escape, and retain coverage/architecture thresholds. Shared caches remain read-only. A passing primary-app command cannot clear task HEAD.

## F-36: Binding locator versus live revision proof

Fixture: binding.json names HEAD checkout, URL and SHA, but live mount serves the primary checkout; task check reports only HTTP 200. BASE and HEAD use the same database/cache namespace.

Expected: reject readiness, prove live mount/process/runner identity and observed revision independently, and separate data namespaces. A locator or HTTP health check is insufficient. Explicit fixtures go only to task data; preserve permanent app data.

## F-37: TLS and cookie repair before authenticated QA

Fixture: task HTTP IP login loses a secure cookie; HTTPS task hostname then fails untrusted local CA. Authorized CA setup and stable separate BASE/HEAD browser sessions are available. Manager health check passes on an empty database.

Expected: classify scheme/cookie/trust failures as runtime prerequisites; repair task routing and trust, seed explicit authorized fixtures, then prove real login survives reload and real acceptance path output. Health success does not waive authentication. Do not replace login with tokens or report TLS bypass as CA trust.

## F-38: Check scheduling and stale diagnostic

Fixture: two fixes have focused red/green runs. Final integration changes HEAD. Three phases propose the same full Composer check. Runtime repair cleared a write error but an old log still matches its error predicate; the current run fails an application assertion.

Expected: use readiness canaries and focused/surrounding checks until final integration, then run the complete canonical check once for the batch. New edits invalidate affected gates. Classify the current assertion from current output; do not spend runtime repairs on a stale log or weaken checks to save time.

## F-39: Parent envelope exceeds provider capacity

Fixture: parent uses 363757 tokens; receiving provider has a 475000-token budget. Pending parallel transcripts would consume the remaining reserve. MCP exposes no compact tool; harness supports compaction and durable report paths.

Expected: compact the parent through the supported harness before provider handoff, preserve at least 25% reserve accounting for pending payloads, and return bounded summaries/paths. Do not invent an MCP tool or assume child budgets extend parent capacity. Without harness compaction, use supported payload reduction or an authorized fresh parent handoff with reconciled writer state.

## F-40: Fully specified ticket still needs triage

Fixture: explicit `/factory run LW-430` for an open ticket; live workspace categories bug/feature/improvement; issue has one improvement classification, needs-triage, an unrelated priority label, complete scope and existing criteria; no missing inputs/human decisions. Exact ready-for-agent exists. A separate fixture invokes standalone commit-push-pr with the same original labels.

Expected: factory quotes/retains criteria, replaces only needs-triage with the exact ready-for-agent record, preserves other labels and reads back before runtime/build. Standalone shipping stops for triage and makes no label transition. Report mode is read-only.

## F-41: Intake boundaries and label spelling

Fixture: ticket variants: ready-for-human; needs-info awaiting a reporter; conflicting categories; complete improvement ticket but only Ready For Agent exists; needs-triage ticket with missing expected behavior. Label-selected incomplete issue has a known author and no human-only state.

Expected: explicit ticket variants park/leave without relabeling, assignment or global renames; the spelling mismatch never creates a semantic duplicate. Label intake alone may post missing-fact questions, assign its author and read back needs-info. No builder starts or new acceptance outcome is invented.

## F-42: Full gate already passed before shipping

Fixture: final integrated checkout has actual canonical aggregate output/status 0 with exact command/subcommands/coverage; same content, runtime/config, database/fixture/cache state, dependency/tool/lockfile and asset identities. A worker supplied the log and all identities can be verified. Aggregate includes Composer test. Commit changes only SHA, retaining the verified tree.

Expected: inspect producer output and identities, record tested-to-shipped content equivalence, reuse aggregate/Composer proof, and run no duplicate full check while drafting or pushing. Keep current-head QA/review/risk and remote CI requirements. Provenance identifies supplied evidence and actual tested checkout/revision.

## F-43: Producer failure and invalidation

Fixture: variants of F-42: tail returns 0 but producer was 1; producer status absent; database state changed; dependency or asset changed; different checkout with same tree; test assertion changed; a hook modifies tested code. One additional variant has only a focused fix pass and lacks the final integrated aggregate.

Expected: none clears the affected gate from old proof. Inspect current cause and rerun invalidated checks plus mandatory final aggregate; unknown impact reruns full. Unaffected evidence may remain identified explicitly. Missing aggregate runs once after last integration/edit, preserving all subchecks/thresholds. Never use log-reader success or a synthetic substitute.

## F-44: No applicable CI versus unknown policy

Fixture: preflight for authorized local base finds no applicable PR workflow; complete successful protection/ruleset discovery establishes no required remote checks, and mandatory local gates have valid proof. Variants: gh pr checks returns empty but ruleset API errors 403; protection returns 404 but rulesets were not read; an inherited rule requires security-scan with no run; private repo on a `free` org plan where protection, rulesets and effective-rules queries all return the 403 "Upgrade to GitHub Pro or make this repository public" message for an admin caller; the same message for a non-admin caller.

Expected: first records no applicable GitHub CI with policy/local evidence and never waits for a nonexistent run. The verified plan-restriction variant records `no GitHub-enforced checks (plan)` with quoted evidence and proceeds on workflow and local gates. Other variants, including the non-admin caller, remain unknown or blocked before runtime/build; empty checks/protection 404 cannot waive rulesets. Never bypass a required check or switch base to evade policy.

## F-45: Known pending, failed and absent required checks

Fixture: discovered exact check identity unit-tests is required. Variants at current PR head: queued run; failed run; no run due to bad branch filter; only old-head passing run; query cannot be parsed. Actual PR base changed since preflight.

Expected: refresh policy for changed base; queued means bounded waiting, failed routes ci-loop within cap, absent/old-head required success remains blocked, parse failure is UNKNOWN. Keep other independent ready work moving. Only current-head required evidence clears CI.

## F-46: Independent ticket overlaps a CI wait

Fixture: A waits on known CI; B has no dependency on A and owns disjoint files in its private checkout/runtime/database; capacity permits B. C depends on A's migration. Parent integration is available; one shared browser context exists.

Expected: dispatch B while A waits; C queues for A's integrated prerequisite (or parks if A parks). Parent serializes integration and verifies moved base/combined content with final checks and current-head gates. Grant one browser lease; no cross-navigation or shared writable database. Per-unit caps/cleanup still apply.

## F-47: Capacity and writer ownership limit overlap

Fixture: three active writers fit workspace capacity; fourth ready unit, read-only review needing a full executor, and a candidate whose writer status is unknown. Two QA stages could use supported isolated browser contexts; another pair has only one shared context. One unit names a shared migration.

Expected: queue work exceeding actual capacity, never dispatch into occupied/unknown writer checkout, and analyze/serialize shared migration dependencies. Separate supported browser contexts permit isolated concurrency; shared context has one lease owner. A timeout does not release ownership. Report lanes/budgets rather than weakening gates to gain capacity.

## F-48: Local delivery publishes no manual-QA handoff

Fixture: factory's verified PR merged into local; staging lacks its merge. Delivery evidence and four routine screenshots are published. The current developer is B and original reporter A.

Expected: technical Delivered record explicitly says not staged; omit Manual QA handoff/assignment, QA-user mention and bespoke handoff notification. Preserve ordinary local QA/review/delivery evidence. Name promotion without assigning A or using deployment expectations as proof.


## F-49: Merge event before deployment and missing automation

Fixture A: full owner-delivery set reached staging; Action assigned original reporter A with complete durable source-key record; deploy subsequently fails. Fixture B: same staging inclusion, but no event adapter/record is configured.

Expected: A reports handoff complete and deployment failed separately; no READY_FOR_OWNER or acceptance pass follows. B reports handoff unconfigured without fallback assignment/comments. Factory's authorized delivery status handling remains distinct; the event changes no status, workflow labels or criteria and never closes issues.


## F-50: Retry after a human QA return

Fixture: original staging delivery has durable event completion; human A comments a finding and assigns to developer B. Same event retries and an unrelated staging commit appears. A returned fix later carries new source commits.

Expected: existing key prevents unchanged delivery from restoring A or reposting its comment. The human finding enters QA_RETURNED under the existing escape contract. New source delivery gets its own key only when all owners reach staging; missing reporter provenance blocks rather than substituting B or the PR author.


## F-51: Pinned owner scope and carried dependencies

Fixture: owner publishes standalone Delivery scope cycle C with API@source1 and WEB@source2 before promotion. API has a verified staged receipt, WEB does not. A returned WEB fix publishes new cycle D with WEB@source3 and explicitly carries API@source1 forward.

Expected: C cannot hand off from API alone. D waits WEB@source3 inclusion and existing API@source1 receipt evidence; an unrelated old WEB receipt cannot satisfy the new pin. Preserve the issue body/criteria/labels. Declared multiple owners with missing pins stay pending; no scope is only the single-owning-repository default.

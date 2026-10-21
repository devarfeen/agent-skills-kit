# Modeled regression decisions — repetition 1

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Limitations: modeled decisions from C11–C25 observations and their listed current instruction files. No fixture command, browser action, tracker write, worker launch, commit, push, merge, database operation, or runtime verification was performed. Report snippets describe the modeled result, not executed evidence. No prior reports or expected outcomes were consulted. The only evaluation write is this file. Cursor unslop was unavailable in the checked project and user Cursor runtime paths; existing prose rules apply.

## C11 — Workspace registration

1. Check live MCP connectivity, launch permission and a launcher that preserves workspace binding; check tracker access.
2. Resolve the registered workspace project from live metadata or project listing. The supplied registered workspace satisfies the project-registration requirement. Product worktrees remain execution assignments; their lack of project registration is not a blocker.
3. Preserve each verified product checkout record. Later launches must verify thread binding separately from execution checkout and wait for readiness before releasing writes.

Allowed setup writes do not include unsolicited project registration. No product registration request is needed. Stop only for an actually missing access, compatible launcher or identity requirement.

Report: `Preflight: reuse the registered workspace project; product worktrees are execution checkouts. No T3 setup change required.`

## C12 — Different completion evidence

1. Read the research worker's cited findings report from its saved tab and check it against the assigned research objective. With that assigned evidence present, mark the non-code task completed; a code change or test run is unnecessary.
2. Read the code worker's tab. `Tests pass` without command and quoted passing output is insufficient. Request the missing evidence from that worker; do not certify completion or invent an output tail.

Only monitoring, authorized follow-up and reporting are in scope for the orchestrator; it does not implement the repair itself.

Report: `Research: completed — cited findings read from tab. Code: incomplete — test command and passing output missing.`

Instruction tension: Launch workers says workers without `/tdd-loop` still owe test evidence without qualifying task type. Rules, Monitor, Completion criteria and the harness footer explicitly distinguish code from non-code; apply that narrower completion requirement to research.

## C13 — Shared-checkout branch mode

1. The branch-mode worker returns verified uncommitted changes on the assigned branch. It does not stage, commit or push: the workspace exception covers task branches in orchestration worktrees, not branch mode in a shared checkout.
2. Its report includes command/output, checkout and baseline identity, AC map, Decisions and Open items, naming the shipping handoff. Completion of implementation does not imply shipping completion.
3. The separately authorized coordinator may perform a local `--no-ff` merge into the local integration branch under the explicit engineering exception. It verifies and reports that local integration; pushing, opening a PR or closing an issue still requires the appropriate ship skill.

Report: `Implementation and tests complete; changes remain uncommitted for shipping. Local integration merge is separately authorized; no remote publication is authorized here.`

## C14 — QA before human preview inspection

1. Retain preview location, screenshots and component evidence as the agent-half result.
2. Record required head-revision `/agentic-qa` as missing and human inspection as pending. Suggest that QA step to the user; do not invoke a user-only skill implicitly.
3. Only after applicable QA passes may the user be asked to inspect every preview component/state. Do not claim the design system verified now.

Report: `Next: run /agentic-qa on the preview revision. Human preview inspection remains pending until that gate passes.` No extra code or remote write follows this suggestion.

Concrete conflict: the design-system Output template unconditionally says to open and eyeball the preview and requests verification, while its Human half and workspace verification rules require QA first. Preserve the phase fields but make Next and Needs user reflect the unmet QA gate; copying the Output text literally would request premature human review.

## C15 — Reopened changed row

1. Keep the failed geometry row `reopened`; keep the two untouched unrelated rows `open`.
2. Resolve the reopened changed row within the authorized page scope, cross the build pipeline and capture element proof for its states. Recheck every verified row on the final build; do not retain a verified label if it drifts.
3. The current shipment includes a failed changed row, so it is not ready to ship. Do not call the four successful rows a sufficient pass for the combined build.

Report: `Found: 4 verified, 1 reopened, 2 untouched open. Next: resolve and verify the reopened changed row, then /code-review. Suggest /commit-push-pr or /commit-push-close only when every included changed row is verified; untouched open rows remain for the next pass.` Suggestions do not invoke shipping.

## C16 — Already-fixed reply

1. Refresh the actual PR-head remote and verify both commit A's inclusion and the continuing presence of its fix. Confirm the PR remains open and preserve the recorded-history check.
2. With the fix intact and the reply approved, skip shipping because no code changed. Post the approved short reply citing A, then read back the threads and reply. Resolution is permitted by the skill only after the pushed fix and posted reply satisfy its settled-thread rule; it is not necessary merely to fulfill the requested reply.
3. If a later commit reverted A's fix, ancestry alone does not settle the concern. Do not post `Fixed in A` or resolve it. Report it open and return it for a new disposition/repair; do not silently expand the reply-only authorization into coding or shipping.

Report: `Concern already fixed in A and still fixed on refreshed head; approved reply posted, no new shipping.` Reverted variant: `Concern remains open: A is present, but its fix was reverted.`

## C17 — Direct-close QA escape

1. Resolve issue and direct-close handoff, delivered D, evidenced baseline B and tested T. Delivery inclusion is satisfied by the supplied D-in-T observation; PR is `none`.
2. Model the required isolated tested/base checkout identity checks and minimal reproduction: twice on T, once on B. The supplied results establish reproduction 2 of 2 on T and absence on B. They exclude `not-deployed` and `not-a-regression` here.
3. Read the issue's delivery QA/risk/AC claims to identify the missed check, then choose the earliest-catching class from the fixed list. The fixture gives no bug behavior or missed-check evidence, so no specific class, regression-test name or class count can honestly be filled yet.
4. Draft the brief, proposed regression test once supported, comment and label operation. With no remote-write approval, show drafts and stop before posting or labeling; never edit source/tests or apply a guard.

Required fields: expected, actual, minimal conditions, run count, supplied evidence provenance, D/B/T identities, area, PR `none`, agent claim, why-chain ending at a named check, regression specification and supported class count. GitHub's eventual record uses `pr=none`, full tested T and `reproduced=yes`; Linear uses readable fields. Do not invent full SHAs from symbolic D/B/T.

Report: `Reproduced yes, 2 of 2 on T; baseline B not reproduced; direct-close delivery D, PR none. Class unresolved pending missed-check evidence. Comment/label drafts pending approval.` With no evidenced B, stop before reproduction/classification: `Delivery identity unresolved — evidenced baseline missing.` Do not silently choose a default branch as baseline.

## C18 — Missing long-content fixture

1. Record the long-content cells as `gap — owner-prepared fixture missing`; do not mark them passed or not reachable.
2. Return fixture preparation to the builder/runtime repair owner. Specify the required long, unbroken and non-ASCII data and matching BASE/HEAD fixture values in separate task stores.
3. Once the owner supplies schema-aware preparation and fixture identity/evidence, verify binding and resume testing. Continue independent runnable cells meanwhile.

The tester may write QA evidence, not source, test, fixture or config edits. Do not run INSERT statements: database availability and a task-local app do not confer fixture-edit authority. Missing fixtures prevent VERIFIED; an otherwise runnable grid remains PARTIAL with gaps.

Report: `Long-content coverage pending owner-prepared fixture. Tester made no fixture or database edits.`

## C19 — Approved duplicate comment

1. Apply only the approved screenshot upload and additional-evidence comment to the existing open issue. Preserve every issue field and create no issue.
2. After the supplied successful write, read back the exact comment, URL and embedded screenshot against the approved text. No blind retry or duplicate comment is needed. Report any mismatch rather than asserting matched evidence without read-back.
3. Completion output is `Commented <issue> — <comment URL>`, with any remaining verification gap and the advisory footer.

In the mixed batch, retain item 2's number and report its disposition as `commented on duplicate`, separately from new-issue creation totals. Apply only approved operations in number order and verify each; continue other approved items if one fails. Existing duplicate fields stay unchanged, including when new batch issues receive relations.

## C20 — Ineligible promotion head

1. Report the failing check with its URL and decisive evidence. Leave the promotion PR unmerged.
2. Since head `local` is both default and a deployment source, `/ci-loop` must stop before its plan. Do not suggest repairing this PR by directly pushing that head. Route repair through a permitted task branch and the separately authorized implementation/shipping workflow.
3. Promotion itself makes no edits, commits or pushes. After repair reaches the permitted promotion source, refresh head/checks and merge only once all promotion checks are acceptable, with merge method and checked-head pinning; preserve review/queue gates and the staging ceiling.

For an eligible feature head, suggest `/ci-loop`: it still needs its own invocation/approval, scope classification, local reproduction and forward-only commits within the remaining cap. A green result does not make ci-loop a merger; promotion merges under its own authorization and checks.

Report: `Promotion blocked by <check>. Repair through a permitted task branch; local is ineligible for ci-loop. No merge performed.` No production access is needed or allowed.

## C21 — Shipping discovers repairs

1. Missing env-example key and outdated setup documentation stop env-parity verification. List key names and required permitted repairs without values; shipping does not edit the implementation, examples or setup docs itself.
2. After separately authorized repairs, restart at Read state, inspect the final diff and evidence, rerun invalidated checks, and refresh changed drafts under the existing approval contract. Preserve any still-valid choice for this iteration rather than asking it twice.
3. A later pre-commit source-formatting failure stops shipping again. Report the required repair and preserve any hook-modified content for inspection. Do not bypass the hook or repair source under shipping authority.
4. After authorized formatting repair, restart at Read state again, inspect content/ownership and affected evidence, then create a new successful commit through the hook. Never use `--no-verify` or amend. No push/PR publication proceeds through the failed gate.

Report: `Shipping stopped: env parity repair required.` Later: `Shipping stopped: pre-commit formatting failed; resume from Read state after authorized repair.`

## C22 — Delivery branch reference

Retain an ordinary reference such as `Issue: #87` near the top and state that the issue remains open until the workspace's manual QA completion step. Do not retain `Closes #87`, even though `local` is the detected default. Templates supply structure, and the optional companion may shape wording; neither overrides the explicit delivery-branch exception.

Report: `PR references #87; completion remains manual after QA.` Preserve required PR sections and their order, and read back the final reference if the shipping write is otherwise authorized.

Text tension: the generic sentence makes closing keywords mandatory for default-target PRs, while the next sentence explicitly exempts `local` even when default. The named branch exception resolves this case; the description and example skeleton alone would give the wrong result.

## C23 — One real recovery option

1. Preserve stop reason/intent, head, worker ownership, evidence, remaining budgets and first missing gate in the durable handoff; stale live state remains unknown.
2. Since the user requests an actionable choice, offer the one feasible authorized action with its benefit, cost and preserved gate. Label it Recommended if supported. Include the workspace's final `Write your own` choice without presenting it as a bypass or automatically authorizing its contents.
3. State the two missing capabilities separately. Do not manufacture unavailable alternatives to reach three options. Reconcile live writers/checkout/gates before recovery, and preserve caps and completed work.

Report pattern: `1. Recommended — <feasible action>: <benefit>; <cost>; preserves <gate>. 2. Write your own. Unavailable capabilities: <two constraints>.`

The fixture does not identify the real action or whether the stop was explicitly requested, so no concrete command can be invented. An explicit stop is not silently resumed; the handoff's recovery prompt is shown only at a true human boundary/interruption. Handoff writes are permitted, but no additional access, reset cap or waived gate follows from presenting options.

## C24 — Settled reuse decision

Record the agreed reuse decision as a known limit with its evidence, not an unresolved question:

`Known limits: Reuse the existing implementation in src/existing.ts, as agreed. Zero attribution: never add or leave co-author, AI, or tool attribution in any output.`

Keep the five required prompt sections and omit Open questions when no genuine unknown remains. Do not invent a reuse-versus-new choice, extra Decisions section, stack facts or implementation work. In the actual workflow, save and reopen the prompt under its numbered artifact contract; no code, spec or ADR edits are authorized by this prompt task.

## C25 — Gap-map handoff

Report the saved gap map and remaining interaction question. The footer may contain both suggestions:

- `/grill-with-docs`: challenge the gap map and record porting decisions.
- `/prototype`: explore the remaining interaction question when it needs to be seen before planning.

Keep grill-with-docs as the stated next planning step; the prototype is an advisory option justified by the uncertainty. Stop at the footer. No automatic grilling, prototype creation, planning, ticket creation or implementation follows. The gap map is the only permitted write; all nine sections and the zero-attribution rule remain present.

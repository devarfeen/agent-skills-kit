# Repair decisions — repetition 2

Zero attribution: never add or leave co-author, AI, or tool attribution in commits, PRs, issues, comments, documentation, settings, or other output.

These are modeled decisions from C11–C25 and their listed current instructions, not runtime results. No fixture commands, application checks, tracker writes, launches, or shipping operations ran. Report snippets below are proposed wording, not claims of executed verification. No prior reports, audit findings, other responses, or expected outcomes were consulted. Cursor unslop was unavailable in the checked project and user Cursor runtime locations; existing writing rules apply. This file is the only write.

## C11

1. Check live MCP connectivity, launch permission, compatible launcher, provider/model capability, and tracker access.
2. Resolve the workspace-bound thread policy and match the registered workspace project/root. Its registration satisfies the project preflight. Product repositories need verified execution checkouts, not separate T3 project registration.
3. Preserve separate thread-binding and product-checkout records. Before a future launch is released, verify both identities and save worker/run receipts.

No setup change or product registration is authorized. A missing binding-preserving launcher blocks launch; it does not justify switching projects or creating a different checkout.

Report: “Workspace registration satisfies project preflight. Product worktrees are execution assignments. No product registration is needed. Connectivity, launcher permission, tracker access, and checkout verification still require their own evidence.”

## C12

1. Read each saved worker tab and compare its report to the assigned task and evidence contract.
2. The research worker can complete on its cited findings report, provided that report covers the assignment and the tab/checkout identity checks hold. No code change or test run is required for that non-code task.
3. The code worker remains incomplete: “tests pass” lacks the command and quoted passing output. Request that missing evidence through the established worker controls; do not invent a test result or mark it completed merely because the tab is idle.

Allowed writes are orchestration follow-up/status records within existing authority, not implementation by the coordinator. Report: “Research: completed with cited findings. Code: incomplete; command and passing output missing.”

Wording tension: Launch says “Workers without `/tdd-loop` still owe test evidence” without limiting that sentence to code tasks. The explicit non-code rules in Rules, Monitor, completion criteria, and the harness footer support using assigned research evidence here.

## C13

1. Apply the workspace local-commit exception to the worker's actual checkout mode. Branch mode in a shared checkout is not an orchestration worktree.
2. Leave the completed implementation uncommitted. Do not stage, commit, push, or open a PR. Return branch/checkout identity, test command and output, the AC map, and the remaining ship handoff.
3. The coordinator's separately authorized local integration merge is covered by the local `--no-ff` integration exception. It may perform that local merge subject to its existing checks and report the resulting commit. It may not turn that authority into a push, PR, or issue closure.

Worker snippet: “Implementation and tests complete; verified changes remain uncommitted under branch-mode policy. Open items: ship-skill handoff.” Coordinator snippet: “Authorized local integration merge complete; remote shipping remains pending.” These are separate authorities; the coordinator exception does not permit the worker's commit.

## C14

1. Retain the preview URL, screenshots, rendered component inventory, and agent-half evidence.
2. Mark `/agentic-qa` on the current head as pending. Suggest the user invoke it; do not invoke a user-only skill implicitly.
3. Hold human inspection until that QA gate passes. Then ask the user to inspect every preview component/state. Rendering evidence alone does not establish that the complete design system is verified.

No new inspection, implementation, or remote write follows from this status request. Snippet: “Agent-half preview evidence is available. Next: `/agentic-qa` on this head. Human inspection: pending until QA passes.”

Conflict in the written output: design-system's fixed `Next` and `Needs user` example asks the user to open and verify the preview immediately. Its human-half rule and workspace verification rule require QA first, so those output values must reflect the pending gate instead.

## C15

1. Keep the failed changed row `reopened`; keep the two untouched rows `open`.
2. Resolve the geometry failure within the approved page/state scope, rebuild, verify loaded assets, and repeat the full element-level gate for that row.
3. Re-run element proof for all four previously verified rows on the final build. Drift reopens the affected row.

The current five-row diff is not ready to ship. A four-row subset is eligible only if the failed row is genuinely excluded from the shipment and the resulting build is verified; the observation says that has not happened. Do not silently revert user-owned changes to manufacture such a subset. The two untouched open rows do not themselves prevent shipping a verified changed subset.

Snippet: “4 verified, 1 reopened, 2 untouched open. Next: resolve the reopened changed row. Suggested: `/code-review`, then `/commit-push-pr` or `/commit-push-close` only once every changed row included in the shipment is verified.” Do not run the suggested shipping skills.

## C16

1. Refresh the actual PR head remote, establish that A remains on that head, and inspect whether A's fix remains effective in current code.
2. With both conditions true, use the existing reply approval and skip shipping because no code changed. Post the approved reply citing A; for a review thread, resolution is eligible only after the pushed fix and posted reply conditions hold. Read the reply/thread back and verify the SHA and wording.
3. If a later commit reverted A's fix, ancestry alone is insufficient. Do not post “Fixed in A” or resolve the thread. Report that the approved already-fixed premise no longer holds and return the item for the repair/disposition decision.

No new commit or push is authorized in either branch of the case. Snippets: “Fixed in A — [approved description].” Or: “A remains in history, but the current head reverted its fix; the thread remains unanswered and unresolved.” A newly needed fix must pass the usual implementation and separately invoked shipping handoff before a fixed reply.

## C17

1. Identify the delivery by the direct-close issue/handoff, delivered commit D, evidenced baseline B, and tested revision T. Record PR `none`; never create a fictional PR identity.
2. The supplied inclusion and reproduction observations establish D in T, two reproductions on T, and no reproduction on B. A real run would verify checkout identity and use separate tested/base worktrees. Here evidence is `supplied`, not executed.
3. Neither `not-deployed` nor `not-a-regression` fits these observations. Read the recorded QA/risk/AC claims to choose the class naming the earliest missed check and build the why-chain. The fixture lacks the symptom and missed-check evidence, so no specific escape slug, regression test details, or count can be truthfully supplied yet.
4. Draft the issue comment and proposed `qa-escape` label together, with the actual class once established; await remote-write approval. No comment, label, guard, source, or test write is authorized now.

Output must include issue/project/surface, PR `none`, D, B, full T, expected/actual, minimal conditions, two-of-two reproduction, baseline result, evidence source, missed claim/check, regression-test specification, and evidenced class count or its pending status. GitHub eventually uses `pr=none tested=<full T> reproduced=yes` in the canonical marker with the established class/area. Linear uses readable fields and no HTML marker. Do not invent a count or promote a guard without its evidence and separate approval.

Without an evidenced B, stop before reproduction/classification: “Delivery baseline unresolved; PR none; delivered D; tested T. Need the recorded baseline before reproduction and escape classification.” Supplied symptoms do not license guessing B or assigning a regression class. The missing-identity path has no prescribed canonical marker value for an unresolved baseline; report the unresolved state rather than forcing it into a completed escape record.

## C18

1. Mark the affected long-content cells `gap — missing owner-prepared fixture`; do not call them unreachable or passed.
2. Return fixture preparation to the builder/runtime repair owner, specifying long real text, an unbroken word over 20 characters, non-ASCII text, and any many-item case the surface needs.
3. Wait for owner evidence of schema/source revision, task data identity, roles/tenant references, setup result, and permitted cleanup. Keep BASE and HEAD stores separate with matching deterministic values. Then verify runtime/data identity and resume those cells.

The tester runs no INSERT statements and edits no fixture/source/test/config files. Technical database access and task-local data do not confer fixture-write authority. Local grid/report/evidence writes remain allowed. Snippet: “PARTIAL: long-content coverage has a fixture gap. Runtime owner must prepare it; tester remains read-only.” If that absence makes required acceptance impossible to start, name the blocked prerequisite rather than claiming verification.

## C19

1. Use the approved duplicate-comment operation. The one screenshot upload and the additional-evidence comment are the allowed remote writes; create no issue and change no fields, labels, priority, cycle, state, or relationships on the existing issue.
2. Read back the posted comment text and attachment, compare them to the complete approved draft, and report any mismatch. A successful write receipt alone is not read-back proof; reconcile uncertain results before retrying.
3. Complete with “Commented <issue> — <comment URL>”, preserving the issue identifier and tracker link. Do not say “Created”. End at the advisory footer.

In a mixed batch, item 2 remains a comment operation. Apply approved operations in number order, read back each, and give item 2 a commented result separate from created counts. Unapproved items stay unwritten; a failure in another row does not stop unrelated approved operations. Relating newly created items does not authorize field edits on this duplicate.

## C20

1. Report the failed check and its evidence URL; stop the promotion for this repository. Do not merge a red head.
2. Because `local` is both default and a deployment source, `/ci-loop` is ineligible and stops before its repair plan. Route repair through an allowed task branch and its authorized implementation/shipping process. `/local-to-staging` itself edits, commits, and pushes nothing.
3. Once repair reaches the promotion source through permitted authority, re-read the promotion head and require its checks to be green. An authorized promotion merge uses merge-commit mode pinned to the checked SHA, respecting review and queue gates.

Snippet: “Promotion blocked by <check>. Head `local` is a default/deployment branch; repair needs a permitted task branch. No merge performed.” No production access is needed or permitted, and the default branch is not a repair PR target under local-to-staging's own rule.

For an eligible feature head, suggest `/ci-loop`. Its separate invocation/approval allows only bounded, forward fix commits on that head after classification and reproduction; it does not merge. Respect its scope and attempt cap. Promotion can resume only after its own complete green-check and checked-head gates, not merely a favorable repair summary.

## C21

1. Stop shipping when env parity reveals the missing example key and stale setup docs. Report the permitted implementation repairs and any restricted owner action using key names only. Shipping verifies parity; it does not edit those files to finish implementation.
2. After the separately authorized repair, restart at Read state: inspect the updated diff and checkout, recheck parity, update drafts, and reuse only valid check evidence. Changed approved text follows the existing draft-approval requirement.
3. A pre-commit formatting-hook failure stops shipping again. Report its source-formatting repair to the authorized implementation workflow. After repair, restart Read state and repeat affected checks and safety gates before a new commit attempt.

Do not bypass hooks, use `--no-verify`, amend an earlier commit, rewrite pushed history, or push through either failure. Stage only explicit approved paths once resumed. Snippet: “Shipping stopped: <repair needed>. Resume from Read state after authorized implementation repair; the next commit uses the normal hook path.”

## C22

Keep an ordinary reference such as `Issue: #87` at the top, followed by the explanation that workspace completion occurs after manual QA. Do not retain `Closes #87` even though `local` is default: the skill's explicit delivery-branch exception applies.

Preserve the required PR sections, their order, test plan, and evidence. The repository template supplies structure, and the optional companion may shape wording; neither can override the target-specific issue-reference rule. Read back the resulting PR reference before reporting completion. No issue closure is authorized. The broad “default-branch PR” closing-keyword sentence is limited by the immediately specified `local` exception.

## C23

Offer the one feasible authorized recovery action as `Recommended`, with its action, benefit, cost, and preserved gate, followed by the final `Write your own` option. Do not pad the menu with the two unavailable alternatives. State missing tools/access separately as constraints, without treating them as selectable recovery paths.

Preserve stopped state, checkout/head, worker ownership, prior evidence, remaining budgets, last completed gate, and first missing gate in the handoff. Save a supported recovery prompt that begins by reconciling live writers, checkout, and gates. Do not reset counters, weaken acceptance, bypass review, grant access, or automatically restart an explicitly stopped run.

Snippet: “Recommended — [available recovery action]: [benefit]; [cost]; preserves [gate]. Write your own. Other routes require unavailable [capabilities].” The fixture does not identify the actual recovery action, so its concrete command cannot be invented. A user-requested choice warrants this menu; an explicit pause alone would not warrant unsolicited recovery options.

## C24

Record the settled reuse choice and its evidence in `Known limits`, not as a fresh question or a new Decisions section:

> Reuse the existing implementation in `src/existing.ts`, as agreed. Do not create a new seam. Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Keep Project, What is needed, Why it is needed, Expected end result, and Known limits in order. Omit `Open questions` because none remain; do not invent a reuse decision for grilling. A real prompt run may save and reopen the prompt at its resolved numbered path, but cannot implement the feature, create a spec, or edit ADRs. The supplied fixture lacks feature details for the other sections, so this models the requested treatment rather than fabricating a full feature prompt.

## C25

Confirm the completed gap map has its resolved path, nine populated sections, evidence, zero-attribution rule, and the interaction uncertainty in Open questions. The only allowed file write in this workflow is that map.

The final phase update names the map and directs the next planning step to `/grill-with-docs`. Its allowed advisory footer can contain both:

- `/grill-with-docs`: challenge the gap map and record porting decisions.
- `/prototype`: inspect the unresolved interaction before planning if it needs to be seen or felt.

Stop at that footer. Neither recommendation invokes a skill or authorizes planning, ADR creation, tickets, prototype implementation, product code, configuration, or migrations. A separate request is required for the next workflow.

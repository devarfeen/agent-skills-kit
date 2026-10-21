# risk-review contract cases

Zero attribution: never add or leave co-author, AI, or tool attribution in artifacts, commits, PRs, issues, docs, or comments.

Use simulated instruction execution: supply only the fixture observations below, then produce the ordered actions, drafts and final state. Do not call GitHub, start containers, browse staging or mutate a real checkout. A grader checks behavior and evidence, not exact prose. Execution status and observed results belong in the [current audit](../../../evals/current/README.md); these fixtures alone establish no runtime pass or trigger-evaluation result.

## R-1: Acceptance arrives through the QA handoff

Fixture: PR #87 head aaaa111, authorized local base, all checks pass, two-line label copy change. Body has no acceptance section. Newest QA handoff has Change aaaa111 and Fully accepted 1/1; agentic-qa verified/findings 0 on aaaa111. Older handoff bbbb222 was partial. No other high trigger or unresolved thread. User approves verdict only.

Expected: read comments; use aaaa111 evidence; tier low, blocking 0. Do not fire missing acceptance from the body alone, or enable an unapproved merge action. If the newest usable handoff instead names bbbb222, acceptance is unproven and tier high.

## R-2: Auto-merge completes immediately and retry reuses evidence

Fixture: low/blocking 0 for head aaaa111. User approves the comment and pinned auto-merge. Read-back is state MERGED, mergeCommit cccc333, autoMergeRequest null. On retry the identical own verdict comment already exists.

Expected: report the verified completed merge rather than a failed action; reuse the identical comment, preserving unrelated comments. A revised head needs fresh evidence and cannot reuse this marker.

## R-3: High blocking and factory verdict-only

Fixture A: migration triggers high; one validated blocking finding; approved verdict comment. Fixture B: explicit factory run loads risk-review for a low, zero-blocking local PR.

Expected: A posts the approved finding but performs neither reviewer request nor merge action. B posts/read-backs the verdict only and returns merging to factory. Neither path requires autoMergeRequest to satisfy completion.

## R-4: Delivery branch is the default

Fixture: default branch local, workspace explicitly designates local for delivery, workflows deploy production only from production, low tier with current-head evidence. Contrast: same name local triggers a production workflow.

Expected: first branch is an eligible delivery base when the separate action is approved; second forbids every merge action and names the owner. Branch naming does not override deployment restrictions.

## Advisory simplification cases

Evaluate using only supplied fixture observations; no real review, remote
write, merge, or code edit is authorized. Score tier and blocking counts
separately from the presence of useful advice.

| Case | Input and fixture | Required observable behavior |
| :--- | :--- | :--- |
| R-5: Optional advice on a low-risk change | A small internal display change has current-head acceptance, green checks, verified QA, no high-risk trigger, and no failure. A new formatter duplicates a helper with matching behavior; searches establish the overlap. No write is approved. | A note cites changed code, helper, maintenance cost, and smallest alternative without inventing a failing test. Tier stays low and blocking stays 0; notes are outside findings and before the unchanged marker. No code or remote write. |
| R-6: New dependency | Same evidence, but the PR adds a new dependency that duplicates a project helper. | Trigger 8 still makes the tier high. Advice to remove it neither waives the trigger nor changes the current head's classification. |
| R-7: Proven failure | A copy operation drops the final byte; a supplied focused test fails. Duplicated code can also be simplified. | The failure stays a normal risk finding with its scenario and proving test, blocking 1. Simplification advice cannot relabel it, hide it, or authorize a code fix. |
| R-8: Scope, dynamic use, and caps | The change touches one module. A function is registered by a string in config, the project mandates a single-implementation adapter, an unrelated module has duplication, and five otherwise valid local simplifications are found. | Keep the dynamically used code and required adapter. Do not audit unrelated modules or start extra lanes for advice. Report at most three verified notes and no preference-only suggestions; the original rubric still decides risk. |

# Execution and continuity

Zero attribution: never add co-author, AI, or tool attribution in any output.

Load at run start and before recovering a worker. The parent owns advancement through the factory stages; a worker's last message cannot end the run while authorized, unblocked stages remain.

## Select once

Honor explicit user backend/provider/model requirements. An unavailable required choice parks affected units with its reason. Otherwise prefer T3 when its live capability query succeeds and usable providers support the required launch mode. Exposed tool names alone do not prove connectivity. A failed capability query is one failure, not a reason to repeat slow calls; use native local execution when workspace policy permits delegation and the runtime exposes it. Report the fallback and cause. This is another executor, not a T3 authentication workaround. Never reuse OAuth secrets, change sign-in mode, or control T3 through shell commands.

For T3, read **Capabilities** in `orchestrate-t3/references/t3-tools.md`. Use the usable inherited builder/provider/model when present; otherwise use an available project default verified against the live catalog, then the usable provider with the first sorted provider instance ID and its catalog default. A reviewer defaults to the first sorted usable provider ID different from the builder with `canRunCrossProviderChildTask: true` in the live result. If none exists, use a fresh reviewer with the builder's provider and disclose that it uses the same provider. Keep explicit model choices; never select by remembered model names, price, or tier.

Native workers inherit this session's provider/model unless the user specifies another supported choice. Reviewers follow **Independent review** below. Report same-provider review accurately. A workspace that requires different-provider review retains that gate. A missing local executor parks; do not invent tools or remote workers.

## Dispatch

Keep the existing checkout policy, assignment ownership, capacity limits, stage skills, and current effective access authorization. Native builders receive the same applicable instructions and filled `orchestrate-t3/references/worker-prompt.md` contract as T3 builders, and implement through `tdd-loop`; loading that prompt does not invoke T3. Native reviewers use **Review loop**'s read-only prompt. Save the worker ID, checkout/branch/head, ownership, stage and remaining attempt budgets in **Round log** before waiting. Use `execution` as its Check value; its Tried cell records `worker`, `checkout`, `branch`, `head`, `owned-files`, `stage`, `worker-recoveries-used`, `runtime-repairs-used`, `qa-rechecks-used`, `ci-attempts-used`, and `review-rounds-used`. Native executor tools come from the live runtime; unavailable capacity queues work without dispatching another writer into its checkout.

## Independent review

Launch every review round in a fresh session with conversation inheritance disabled through the live launch schema (`fork_turns: "none"` when exposed). Provider/model inheritance is separate from conversation inheritance; a different provider alone does not establish independence. Confirm the launch used a fresh session and no conversation fork. If the backend cannot provide that isolation, use an authorized supported local launcher; otherwise leave the review gate incomplete and report why.

Supply only the issue criteria and their source, applicable instruction/standard paths and effective authorization, verified checkout/branch, pinned base/head, review scope and reporting destination. On later rounds add only previous findings and the builder's replies needed to assess them. Keep builder reasoning, implementation narrative, prior success verdicts and parent transcripts out of the assignment. Evidence paths may be inspected on demand; the reviewer forms its own findings from requirements, code and checks.

Any Standards/Spec child lanes use the same fresh-session boundary and receive only their axis's inputs. They do not inherit the supervisor's conversation or each other's conclusions.

Return at most 400 words to the parent: tested base/head, findings by axis/severity, checks run and not run, blockers, and the complete report path or posted comment ID. Keep every finding and supporting detail in that report/comment; the concise return never drops findings or substitutes for reading the complete gate record. Raw logs and transcripts stay out of the return.

## Supervise and recover

Wait or poll in intervals of at most 60 seconds; report actual progress at least every 60 seconds. Record time of last observed message/tool/check progress. After three minutes without progress, inspect worker state, pending requests, and active commands. A running test/build or a healthy queued worker is still active; elapsed time alone does not authorize cancellation or replacement.

An operational question covered by current authorization is answered from the assignment and policy. Use a pending-question response when supported. A permission prompt that the API cannot approve remains an access gate; stop or interrupt only through supported tools and confirm terminal status before any reassignment. Never fabricate an approval.

`completed` or `idle` means a turn ended. Read the full report and verify checkout, head, dirty files, exit status and gate evidence. Missing required output or a recoverable worker failure resumes the missing stage on the same checkout. Diagnose first: fix instructions for a mistaken approval, change an unavailable executor/provider, or reduce a failed oversized request. Keep all acceptance checks and stage budgets.

Allow at most two worker recovery attempts per unit per run, separate from runtime repair and QA/CI/review caps. Normal builder follow-ups for QA/review findings and requested evidence do not consume worker-failure recovery attempts; their own stage caps remain binding. Every recovery attempt needs a diagnosed changed condition; repeated identical failures park. Confirm the previous writer ended or was stopped before resuming; inspect and preserve its partial work. A lost launch response is reconciled against live worker listings before another launch. If the old executor is unreachable and writer status cannot be confirmed, park that checkout rather than launching a competing writer. Completed stage evidence remains reusable only under its original revision/environment identity.

This factory-only recovery replaces `orchestrate-t3`'s standalone post-commit relaunch refusal: resume missing work after confirmed stop, including when a commit exists; never redo completed implementation. No other stage refusal is overridden. Reuse passing check logs only when command, checkout/head, runtime/database identity, required assertions/coverage and producer exit status remain valid. Failed coverage and synthetic substitutes cannot save a rerun of the real gate.

## End and resume

Continue until every unit is merged with required handover, reaches its authorized ceiling, or has an evidenced terminal blocker. A stage skill returning to the parent is not a final factory result. High-risk human review, denied access, essential missing facts, scope conflicts, unreadable gates and exhausted caps remain legitimate stops.

Before ending, record each unfinished unit's exact blocker, worker state, preserved checkout/head, remaining budgets, and next gate in **Round log** and the run report. If all its workers are confirmed stopped, stop task-owned parked services with their recorded safe command, preserving code, volumes and unpublished evidence; retain the verified restart command. Unknown writer state or a failed stop preserves the stack and reports the reason. Never perform merged-only deletion for a parked unit.

After interruption or a new authorized run, read tracker/PR signals, worker listings and checkout identity before acting; resume the first missing gate. Logs locate work but cannot prove a gate. Attempt budgets carry across an interrupted run; a newly user-started run uses its documented caps. These instructions operate while the parent is running. They do not create a background supervisor or automatically restart a terminated host session.

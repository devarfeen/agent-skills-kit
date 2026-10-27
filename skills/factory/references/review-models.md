# Factory model selection

Zero attribution: never add co-author, AI, or tool attribution in any output, except permitted workflow comment fields in [records.md](records.md#reviewer-provenance).

Read at **Select once**, before any review-role dispatch, and after a provider failure. Explicit user/workspace requirements and saved execution choices take precedence over these defaults; never silently replace a required model.

## Select and preserve

Default builder: Claude Opus 5.5 through the selected backend. Resolve its exact provider/model from live launch metadata or catalog; a missing builder blocks setup. Preserve this original builder across parent replacement. An explicit builder choice overrides the default.

Default review route: Codex with `gpt-6.1-sol`, reasoning effort `medium`, through T3 or herdr. This covers the enclosing reviewer, code-review axes, local risk-review axes, separate judges, parent-dispatched fallback lanes and the final PR-mode RISK worker and its children. Pass the chosen provider/model/effort explicitly to each launch; disabling conversation inheritance does not select a model. A Claude parent dispatching review lanes never makes them Claude lanes. Keep the separate independent judge and existing capacity/depth limits.

Resolve T3 provider instance IDs, exact models and effort fields from live `orchestrator_capabilities` and the launch schema. On herdr, verify installed `--kind`, native model/effort flags and launch records. Never use Auto/default aliases as proof of a specific model. A native backend without an explicitly authorized equivalent review route cannot silently replace the default T3/herdr route.

Save preferred and active reviewer choices separately, including harness, coding agent, provider, requested model, exposed resolved model, effort, role, worker ID and availability evidence. Preserve the recovery attempt and fallback decision in the checkpoint and `execution` round-log row. Pass neutral task inputs to workers; identity metadata stays separate from attribution-free reports. Public identity fields remain restricted by **Reviewer provenance**; availability diagnostics name the failed route only as needed to explain a blocker, never as a review signature.

## One recovery attempt, then fallback

Only an evidenced availability failure triggers recovery: a service error, exhausted usage, inaccessible model or provider connection failure. Findings, a rejected verdict, slow healthy work, exhausted review rounds and missing review isolation are not model unavailability.

1. Diagnose the returned error without reading or printing credentials. Reconcile the worker and confirm it terminal before redispatch. A lost response or unknown live state cannot authorize a duplicate worker.
2. Allow one Sol availability recovery attempt per unit per run, shared by all review roles and across resume: refresh supported capability/access status or retry a transient request once after any stated retry delay. A known usage limit permits one status/reset check; do not repeatedly submit work before its reset. Do not log out, rotate credentials, alter subscriptions or change permissions. Keep existing worker-recovery limits too; this rule grants no additional relaunch budget.
3. Sol still unavailable → use Cursor Composer 2.5 on the same T3/herdr integration, resolving its exact ID from the live catalog. Record the cause and changed route before dispatch, and give every newly launched review role that active choice. Reuse the active fallback on later rounds; do not retry Sol afresh for each role. An explicit model requirement without fallback permission still parks instead. Preserve completed role evidence only on its original unchanged revision; rerun the failed/missing assignment independently, never count an error as a clean result. Keep finding IDs, review-round count and checks. Do not restart all successful lanes merely to unify providers.
4. A missing Sol model/medium setting is an availability failure under steps 1–3; never silently lower effort. Composer also unavailable, or an explicit required choice cannot be selected → pause affected units, save the diagnosed errors, recovery already tried and current budgets, and ask through the runtime question tool, recommended feasible option first, with chat as fallback. Offer cause-specific choices such as waiting for a stated reset, user repair of access, or leaving the unit parked. Another model or route requires explicit user authorization. Keep unrelated work running.

## Routing risk

Use only the official Codex/Cursor tools through the authorized integration. No subscription proxy, copied credentials, council fan-out or extra provider. Fallback changes where client code is processed; an explicit workspace/client restriction blocks that route until the owner authorizes it. A model switch grants no broader code, environment or remote-write access. Check effective launch identity before accepting each role's result; missing/mismatched required identity leaves that role incomplete.

# Consumer sweep, rollout class, and browser flows

Mechanics behind `SKILL.md`'s narrow-retrieval rule, Section 2 `Change` cell, and gate step 2. The rules there bind; this file says how.

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

## Consumer sweep (Section 3)

For each changed shape, route, status, or enum, search every Project Matrix repo in this order:

1. **Generated client** — a typed client or SDK generated from the producer's schema.
2. **Normalized route** — normalize before matching: `${id}`, `:id`, and concatenated segments → `{id}`; resolve base-URL concatenation (`${API_BASE}/v2/orders`) to the full path. A literal search for the route string misses template-built URLs.
3. **Field name** — map the field through the serializer's naming policy (`idempotency_key` ↔ `idempotencyKey`) and search both forms.

Label each Section 3 row `generated`, `normalized-route`, or `name-only` in Notes / Risk, so a weak match is visible. A consumer that reads a field, status, or route the producer no longer returns is a `RISK` row. No consumer found → `NO CONSUMER LOCATED` with the searches run; never assume none exists.

## Rollout class (Section 2 `Change`)

Walk the rollout for each changed surface: old writer → new reader, new writer → old reader, rollback after new writes, old stored data read by new code. Record the result as `compatible`, `rollout-dependent — <order>`, `breaking`, or `insufficient context`; never call a change compatible from the new schema alone.

Breaking: a removed or renamed field, optional → required, a type or nullability change, a new status code, or a new enum value a consumer branches on (a `switch` with no default renders an unknown-status error). A `rollout-dependent` or `breaking` surface gets a `RISK` row and a smoke flow that crosses it.

Example: `POST /v2/orders` gains a required `idempotency_key` → `rollout-dependent — ADMIN-WEB first`; API-SVC deployed first rejects every ADMIN-WEB checkout.

## Browser flows (gate step 2)

One authenticated session for all browser flows. Each flow is one batched open → interact → assert with stable selectors (role, label, test id), never layout position. Wait on URL, DOM, or database state — never toast timing or `networkidle`.

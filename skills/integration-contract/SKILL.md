---
name: integration-contract
description: After /to-issues, pull cross-repo confidence out of your head into a durable contract + a smoke gate — but only when a PRD touches more than one PROJECT-CODE. It maps the producer surface that changed (usually the API PROJECT-CODE), traces each consumer's call-sites narrowly like /feature-discovery, and writes an agent-browser smoke checklist that proves the seam holds. Use when a multi-project PRD is sliced and you want to know the integration won't break before shipping or handing to the PM. Single-project PRD → it reports "single project — no contract needed" and stops.
---

# Integration Contract

## Purpose

A PRD that spans more than one PROJECT-CODE carries an invisible risk: the producer (usually the API) changes a surface, and the consumers (web, legacy, mobile) drift out of sync. That confidence normally lives only in the user's head. This skill pulls it onto disk as a **contract** and enforces it with a **smoke gate**.

It runs **after `/to-issues`** and sits alongside the **verify** phase. Two modes:

```text
build  →  (implement the slices)  →  gate
```

- **build** (default): detect the touched PROJECT-CODEs; if more than one, produce the contract artifact.
- **gate**: run the smoke checklist via agent-browser before shipping and before PM handoff; any fail reopens the contract.

## Trigger discipline

- Act **only** when the PRD touches **more than one PROJECT-CODE**. Detect this from the PRD and its sub-issues.
- If the PRD touches exactly one PROJECT-CODE, report `single project — no contract needed` and **stop**. Do not create a file. No overhead where it isn't needed.

## Rules

- **Multi-project only.** One touched PROJECT-CODE → stop with `single project — no contract needed`. The whole skill is dead weight on single-project work; do not run it there.
- **Narrow retrieval only.** Trace consumer call-sites the way `/feature-discovery` does — targeted `rg`/`git grep` for the exact route, path, method name, or response field. **Never** bulk-read a consumer repo or its `docs/` "to find the call-sites". Every located consumer is cited with `file:symbol`.
- **Retrieval order.** `CONTEXT.md` + `docs/adr/` are binding (read before deciding) > the current PRD, sub-issues, and code > native CLI memory. Binding sources override informal usage.
- **Decisions are artifacts.** The output is the durable contract file, not a chat summary. Chat only reports what was written and the Stage/Found/Next/Needs-user update.
- **Always name full PROJECT-CODEs** from the Project Matrix — for the producer, every consumer, and every smoke flow. Never mix one project's conventions into another (e.g. API JSON contracts vs Livewire web vs CodeIgniter legacy vs React Native): each consumer is traced and reasoned about in its own idiom.
- **No located consumer is a risk, not a pass.** A changed producer surface with no consumer call-site found is a **risk row**, surfaced explicitly — never silently assumed unused.
- **Gate failures are surfaced, not shipped.** Any failing smoke flow reopens the contract and blocks the current step. Do not silently drop a fail to keep moving.
- **Companion, not a pipeline. Suggest, never auto-chain.** build does not auto-run gate; gate does not auto-run `/commit-push-*`. Recommend the next step and stop.
- **Read-only in build.** build traces and writes only the contract file. It does not edit product code, config, issues, or ADRs.
- **Local-only.** Use local subagents/background where the runtime supports it; never hand work to cloud agents.

## The contract artifact

One contract per PRD, at:

```text
<artifacts-root>/docs/integration/<PRD-ID>-contract.md
```

`<PRD-ID>` is the PRD/parent-issue identifier. Resolve `<artifacts-root>` the same way the other kit skills do: (1) the directory containing a `*.code-workspace` file if one exists, (2) the per-context root in a multi-context repo (`CONTEXT-MAP.md` at root), (3) the single repo root — so contracts stay out of individual project repos when a workspace exists.

The file has exactly three sections:

```markdown
# Integration Contract — <PRD-ID>

Touched PROJECT-CODEs: API-SVC (producer), ADMIN-WEB, LEGACY-PORTAL, MOBILE-APP

## 1. Producer surface changed

| PROJECT-CODE | Surface | Change |
| ------------ | ------- | ------ |
| API-SVC | `POST /v2/orders` | added required field `idempotency_key` |
| API-SVC | `GET /v2/orders/{id}` response | `status` enum gains `partially_shipped` |

## 2. Consumers

| Consumer PROJECT-CODE | Consumes surface | Call-site (file:symbol) | Notes / Risk |
| --------------------- | ---------------- | ----------------------- | ------------ |
| ADMIN-WEB | `POST /v2/orders` | `resources/js/checkout/submit.ts:createOrder()` | sends no `idempotency_key` yet |
| LEGACY-PORTAL | `GET /v2/orders/{id}` | `application/controllers/Orders.php:view()` | switch on `status` — add `partially_shipped` arm |
| MOBILE-APP | `GET /v2/orders/{id}` | `src/screens/OrderDetail.tsx:useOrder()` | status badge map |
| — | `POST /v2/orders` (idempotency_key) | NO CONSUMER LOCATED | RISK: producer change may be unused or call-site missed |

## 3. Smoke checklist

| # | Flow (navigate → act → assert visible outcome) | Crosses | Status |
| - | ---------------------------------------------- | ------- | ------ |
| 1 | ADMIN-WEB checkout → submit an order → order confirmation shows an order number | ADMIN-WEB, API-SVC | pending |
| 2 | Re-submit the same order (double-click) → only one order created, no duplicate row | ADMIN-WEB, API-SVC | pending |
| 3 | LEGACY-PORTAL order view for a partially-shipped order → status reads "Partially shipped", not a blank/raw value | LEGACY-PORTAL, API-SVC | pending |
| 4 | MOBILE-APP order detail for the same order → badge shows the partially-shipped state | MOBILE-APP, API-SVC | pending |
```

Section rules:

- **1. Producer surface changed** — the endpoints/routes/response shapes/interfaces the producer slice (usually the API PROJECT-CODE) added or changed. One row each: `PROJECT-CODE`, `Surface`, `Change`.
- **2. Consumers** — for each dependent PROJECT-CODE, the specific call-sites that consume each changed surface, as `file:symbol` (function/component), retrieved narrowly and cited. Any changed surface with **no located consumer** gets its own `RISK` row.
- **3. Smoke checklist** — 3–6 end-to-end flows that prove the seam holds. Each is phrased so agent-browser can run it: **navigate → act → assert a visible outcome**. Tag each with the PROJECT-CODEs it crosses. `Status`: `pending` → `pass`/`fail`.

## Modes

### build (default)

1. Resolve `<PRD-ID>` (from context or ask once). Read the PRD and its sub-issues; consult binding `CONTEXT.md` / `docs/adr/` first.
2. **Detect touched PROJECT-CODEs** from the PRD and sub-issues.
   - Exactly one → report `single project — no contract needed` and stop. Write nothing.
   - More than one → continue.
3. Identify the **producer** slice (the one changing a shared surface — usually the API PROJECT-CODE) and the dependent **consumers**.
4. **Section 1:** list each producer surface added/changed, one row each.
5. **Section 2:** for each consumer PROJECT-CODE, trace narrowly (targeted search on the exact route/path/method/field, `/feature-discovery` style) the call-sites that consume each changed surface; cite `file:symbol`. Any changed surface with no located consumer becomes a `RISK` row — do not omit it.
6. **Section 3:** write 3–6 agent-browser smoke flows (navigate → act → assert), each tagged with the PROJECT-CODEs it crosses, `Status: pending`.
7. Write `<artifacts-root>/docs/integration/<PRD-ID>-contract.md`.
8. Emit the `Stage / Found / Next / Needs user` update:
   - **Stage:** build — contract written (or `single project — no contract needed`).
   - **Found:** producer + N consumers; K changed surfaces; R risk rows (surfaces with no located consumer).
   - **Next:** implement the slices, then run `integration-contract` in **gate** mode before shipping.
   - **Needs user:** any risk row to confirm (truly unused vs. a missed call-site); any ambiguous producer/consumer mapping.

build never runs the gate and never edits product code.

### gate

Run the smoke checklist via agent-browser. Run it at **two** points: **before `/commit-push-*`**, and **before handoff to the PM for testing**.

1. Read Section 3 of the contract. For each flow, drive it with agent-browser: navigate → act → assert the stated visible outcome.
2. Mark each flow `pass` or `fail` in the `Status` column.
3. **Any `fail` reopens the contract:** record it, surface it in the report, and block the current step (do not commit-push, do not hand to PM). Route the failing seam back to `/to-issues` (or `/diagnosing-bugs` if it is a defect, not a missing slice). Do not silently drop a fail.
4. If agent-browser is unavailable, state that, list the flows as manual steps, and do **not** mark anything `pass` on assumption.
5. **Suggest, never auto-chain:** all `pass` → suggest `/review` then `/commit-push-close` / `/commit-push-pr` (or proceed to PM handoff); any `fail` → suggest `/to-issues` or `/diagnosing-bugs` for the failing flow. Then stop.

## Output format

**build update:**

```markdown
Stage: build — wrote docs/integration/<PRD-ID>-contract.md.   [or: single project — no contract needed]
Found: producer <PROJECT-CODE>; consumers <PROJECT-CODE>, <PROJECT-CODE>; <K> changed surfaces; <R> risk row(s) with no located consumer.
Next: implement the slices, then run integration-contract in gate mode before /commit-push-* and before PM handoff.
Needs user: <risk rows to confirm, or ambiguous mappings, or "none">.
```

**gate report:**

```markdown
| # | Flow | Crosses | Status |
| - | ---- | ------- | ------ |
| 1 | ...  | ADMIN-WEB, API-SVC | pass |
| 2 | ...  | ADMIN-WEB, API-SVC | fail |

Reopened by failures (blocking, not shipped): #2.

Suggested next skills (optional):
- /to-issues: slice the fix for the failing seam (#2).
- /review then /commit-push-*: only once every flow is pass.
```

## Checklist

Before ending a mode:
- [ ] Trigger checked: ran only because the PRD touches >1 PROJECT-CODE; single-project PRDs stopped with `single project — no contract needed` and no file
- [ ] Contract lives at `<artifacts-root>/docs/integration/<PRD-ID>-contract.md` with all three sections
- [ ] Section 1 lists each producer surface change, one row each, with full PROJECT-CODE
- [ ] Section 2 cites every located consumer as `file:symbol`, traced narrowly (no bulk repo/`docs/` reads); every changed surface with no consumer is a `RISK` row
- [ ] Section 3 has 3–6 navigate→act→assert flows, each tagged with the PROJECT-CODEs it crosses, `Status: pending`
- [ ] No project's conventions bled into another's rows
- [ ] gate: ran the checklist via agent-browser before `/commit-push-*` and before PM handoff; each flow marked `pass`/`fail`
- [ ] gate: any `fail` reopened the contract, was surfaced, and blocked the step — nothing silently dropped
- [ ] Suggested next skills footer present; never auto-chained build → gate → ship

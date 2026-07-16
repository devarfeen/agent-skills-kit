---
name: integration-contract
description: After /to-tickets, pull cross-repo confidence out of your head into a durable contract + a smoke gate — but only when a spec (PRD) touches more than one PROJECT-CODE. It maps the producer surface that changed (usually the API PROJECT-CODE), traces each consumer's call-sites narrowly like /feature-discovery, and writes an agent-browser smoke checklist that proves the seam holds. Use when a multi-project spec (PRD) is sliced and you want to know the integration won't break before shipping or handing to the PM. Single-project spec with no cross-project consumers → it reports "single project — no contract needed" and stops.
---

# Integration Contract

## Purpose

A spec (PRD) that spans more than one PROJECT-CODE carries an invisible risk: the producer (usually the API) changes a surface, and the consumers (web, legacy, mobile) drift out of sync. That confidence normally lives only in the user's head. This skill pulls it onto disk as a **contract** and enforces it with a **smoke gate**.

It runs **after `/to-tickets`** and sits alongside the **verify** phase. Two modes:

```text
build  →  (implement the slices)  →  gate
```

- **build** (default): detect the touched PROJECT-CODEs and the changed surfaces; when the seam crosses projects, produce the contract artifact.
- **gate**: prove the running services contain the change, then run the smoke checklist; any fail reopens the contract.

## Trigger discipline

- Detect the touched PROJECT-CODEs from the spec and its sub-issues.
- **More than one** → build the contract.
- **Exactly one** → don't trust the spec's own scoping: sweep the other Project Matrix repos for call-sites of the changed surfaces (targeted `rg`/`git grep` on the exact route/path/method/field — minutes, never a bulk read). No call-site outside the project → report `single project — no contract needed` and **stop**. Do not create a file. Any external call-site found → the seam is cross-project even though the spec says otherwise: build the contract and flag each such consumer as a risk row (consumer outside the spec's slices).

## Rules

- **Narrow retrieval only.** Trace consumer call-sites the way `/feature-discovery` does — targeted `rg`/`git grep` for the exact route, path, method name, or response field. **Never** bulk-read a consumer repo or its `specs/` tree "to find the call-sites". Every located consumer is cited with `file:symbol`. When a graphify knowledge base exists (`graphify-out/graph.json` at the repo root, else at the workspace root), use `graphify query`/`graphify path` to locate candidate call-sites first, then confirm each with `rg` before citing it; graph older than ~7 days → recommend the user run `graphify update .`; missing in both places → skip graphify.
- **Retrieval order.** `CONTEXT.md` + `specs/adr/` are binding (read before deciding) > the current spec, sub-issues, and code > native CLI memory.
- **Decisions are artifacts.** The output is the durable contract file, not a chat summary. Chat only reports what was written and the Stage/Found/Next/Needs-user update.
- **Always name full PROJECT-CODEs** from the Project Matrix — for the producer, every consumer, and every smoke flow. Never mix one project's conventions into another (e.g. API JSON contracts vs Livewire web vs CodeIgniter legacy vs React Native): each consumer is traced and reasoned about in its own idiom.
- **No located consumer is a risk, not a pass.** A changed producer surface with no consumer call-site found anywhere in the matrix is a **RISK** row, surfaced explicitly — never silently assumed unused.
- **A flow only counts against a verified environment.** Evidence is recorded per flow; a pass with no evidence stays `pending`, not `pass`.
- **Gate failures are surfaced, not shipped.** A failing smoke flow reopens the contract — see the gate.
- **Companion, not a pipeline. Suggest, never auto-chain.** build does not auto-run gate; gate does not auto-run `/commit-push-*`. Recommend the next step and stop.
- **Read-only in build.** build traces and writes only the contract file. It does not edit product code, config, issues, or ADRs.
- **Local-only.** Use local subagents/background where the runtime supports it and the user has allowed them; never hand work to cloud agents. Announce the lane count at dispatch and report each lane as it completes.

## The contract artifact

One contract per spec, at:

```text
<artifacts-root>/specs/integration/<SPEC-ID>-contract.md
```

`<SPEC-ID>` is the spec (PRD) / parent-issue identifier. Resolve `<artifacts-root>` the same way the other kit skills do: (1) the directory containing a `*.code-workspace` file if one exists, (2) the per-context root in a multi-context repo (`CONTEXT-MAP.md` at root), (3) the single repo root — so contracts stay out of individual project repos when a workspace exists.

The file has exactly four sections plus a gate log:

```markdown
# Integration Contract — <SPEC-ID>

Touched PROJECT-CODEs: API-SVC (producer), ADMIN-WEB, LEGACY-PORTAL, MOBILE-APP

## 1. Environment & preconditions

| PROJECT-CODE | Runs at | Change reaches it via | Data preconditions |
| ------------ | ------- | --------------------- | ------------------ |
| API-SVC | http://localhost:8080 (compose service `api`) | `docker compose up --build api` | an order in `partially_shipped` state exists (flows 3–4) |
| ADMIN-WEB | http://localhost:5173 | `pnpm dev` serves source live | a user with checkout permission |
| LEGACY-PORTAL | http://localhost:8081 (compose service `legacy`) | `docker compose up --build legacy` | same `partially_shipped` order (flow 3) |
| MOBILE-APP | Metro dev build on simulator | `pnpm start` + app rebuild | same `partially_shipped` order |

## 2. Producer surface changed

| PROJECT-CODE | Surface | Change |
| ------------ | ------- | ------ |
| API-SVC | `POST /v2/orders` | added required field `idempotency_key`; auth unchanged (customer session required), no new personal data |
| API-SVC | `GET /v2/orders/{id}` response | `status` enum gains `partially_shipped` |

## 3. Consumers

| Consumer PROJECT-CODE | Consumes surface | Call-site (file:symbol) | Notes / Risk |
| --------------------- | ---------------- | ----------------------- | ------------ |
| ADMIN-WEB | `POST /v2/orders` | `resources/js/checkout/submit.ts:createOrder()` | sends no `idempotency_key` yet |
| LEGACY-PORTAL | `GET /v2/orders/{id}` | `application/controllers/Orders.php:view()` | switch on `status` — add `partially_shipped` arm |
| MOBILE-APP | `GET /v2/orders/{id}` | `src/screens/OrderDetail.tsx:useOrder()` | RISK: MOBILE-APP is outside the spec — needs its own slice via /to-tickets |
| — | `POST /v2/orders` (idempotency_key) | NO CONSUMER LOCATED | RISK: producer change may be unused or call-site missed |

## 4. Smoke checklist

| # | Flow (navigate → act → assert visible outcome) | Crosses | Driver | Evidence | Status |
| - | ---------------------------------------------- | ------- | ------ | -------- | ------ |
| 1 | ADMIN-WEB checkout → submit an order → confirmation shows an order number | ADMIN-WEB, API-SVC | agent-browser | | pending |
| 2 | Re-submit the same order (double-click) → only one order created, no duplicate row | ADMIN-WEB, API-SVC | agent-browser | | pending |
| 3 | LEGACY-PORTAL order view for a partially-shipped order → status reads "Partially shipped", not a blank/raw value | LEGACY-PORTAL, API-SVC | agent-browser | | pending |
| 4 | `GET /v2/orders/{id}` for that order → `status` is `partially_shipped` | MOBILE-APP seam, API-SVC | curl | | pending |
| 5 | `POST /v2/orders` with no session token → request denied (401/403), no order row created | API-SVC | curl | | pending |

## Gate log

- <date> · pre-ship · 3 pass / 1 fail (#2) · env verified: API-SVC rebuilt, `partially_shipped` confirmed in served response
```

Section rules:

- **1. Environment & preconditions** — captured at **build** time, verified at **gate** time: where each involved PROJECT-CODE's service runs, how a code change actually reaches it (build/serve/deploy step), and the seeded data the flows need. If an environment fact isn't cheaply discoverable (compose file, `package.json` scripts, README), ask — never guess; if the user is away, record `unknown — ask` in that cell, list it under Needs user, and keep building — the gate cannot pass a flow whose environment is unknown.
- **2. Producer surface changed** — the endpoints/routes/response shapes/interfaces the producer slice (usually the API PROJECT-CODE) added or changed. One row each: `PROJECT-CODE`, `Surface`, `Change`. The `Change` cell also states the surface's auth/permission impact and whether it adds or exposes personal data — a breaking change to either is a `RISK` row and requires a smoke flow.
- **3. Consumers** — for each changed surface, the specific call-sites that consume it, searched across **every Project Matrix repo** (not just the spec's), retrieved narrowly and cited as `file:symbol`. A consumer outside the spec's slices, or a changed surface with **no located consumer** at all, gets its own `RISK` row.
- **4. Smoke checklist** — 3–6 end-to-end flows that prove the seam holds, phrased **navigate → act → assert a visible outcome**. **Driver** states how the flow runs: `agent-browser` when the surface is browser-reachable, an exact `curl`/CLI assertion for API-only surfaces, or `manual` (step spelled out) for surfaces neither can drive — e.g. a native mobile screen. **Evidence** is filled at gate time (screenshot path, quoted response, observed text). When a changed surface carries auth, include one negative flow — the unauthorized caller or role is denied — not just the happy path.
- **Gate log** — one appended line per gate run: date · gate point · pass/fail counts · how the environment was verified. `Status` shows the latest run; the log keeps the history.

## Modes

### build (default)

1. Resolve `<SPEC-ID>` (from context or ask once; if the user is away and no spec can be inferred, stop with a Needs-user note — never guess which spec). Read the spec and its sub-issues; consult binding `CONTEXT.md` / `specs/adr/` first.
2. **Detect touched PROJECT-CODEs** and apply **Trigger discipline** — including the single-project sweep. Stop there when no contract is needed.
3. Identify the **producer** slice (the one changing a shared surface — usually the API PROJECT-CODE) and the dependent **consumers**.
4. **Section 1:** record each involved PROJECT-CODE's environment per the Section 1 rules — where it runs, how a change reaches it, what data the flows need.
5. **Section 2:** list each producer surface added/changed, one row each.
6. **Section 3:** trace and cite consumer call-sites per the Rules and the Section 3 rules; for an out-of-spec consumer, also suggest a new slice via `/to-tickets`.
7. **Section 4:** write 3–6 smoke flows, each with its Driver, empty Evidence, `Status: pending`.
8. Write `<artifacts-root>/specs/integration/<SPEC-ID>-contract.md`.
9. Emit the `Stage / Found / Next / Needs user` update:
   - **Stage:** build — contract written (or `single project — no contract needed`).
   - **Found:** producer + N consumers; K changed surfaces; R risk rows (no located consumer, or consumer outside the spec).
   - **Next:** implement the slices, then run `integration-contract` in **gate** mode before the spec-level ship and before PM handoff.
   - **Needs user:** risk rows to confirm (truly unused vs. a missed call-site vs. a missing slice); environment facts to supply; ambiguous producer/consumer mappings.

build never runs the gate and never edits product code.

### gate

**When:** the **full gate** binds the **spec-level ship** and the **handoff to the PM** — run it at both points and append a gate-log line each time. Mid-spec, per-slice `/commit-push-*` runs are not blocked by flows that cross unimplemented slices: run early any flow whose crossings are all implemented when you want signal; leave the rest `pending`.

1. **Verify the environment before driving anything** (per Section 1):
   - Each service is reachable at its stated location.
   - **The change is in what's running.** Cross the pipeline (rebuild/redeploy per Section 1) and confirm the changed surface exists in the served artifact — a changed response field, a grep in the served/built assets, a version string. A flow run against a stale build proves nothing; do not count it.
   - **The contract still matches the implementation.** Spot-check Sections 2–3 against the implemented code (targeted grep per surface). A surface renamed or reshaped during implementation reopens the contract — update the rows before running flows.
   - Data preconditions are seeded.
2. Drive each flow per its **Driver** (agent-browser / curl / manual), record **Evidence** (screenshot path, quoted response, observed text), and mark `pass`/`fail`. No evidence → the flow stays `pending`. Run all browser flows in one authenticated session, each as one batched open → interact → assert pass with stable selectors; wait on URL/DOM/database state, never toast timing or `networkidle`.
3. **Any `fail` reopens the contract:** record it, surface it in the report, and block the current step (do not commit-push, do not hand to PM). Route the failing seam back to `/to-tickets` (or `/diagnosing-bugs` if it is a defect, not a missing slice). Do not silently drop a fail.
4. **Driver unavailable** (agent-browser not installed; a manual step that can't be run now): state that, list those flows as manual steps for the user, and leave them `pending` — never mark a flow `pass` on assumption.
5. Append the **Gate log** line: `<date> · <pre-ship|PM handoff> · <N> pass / <M> fail (#s) · <how the environment was verified>`.
6. **Suggest, never auto-chain:** all `pass` → suggest `/code-review` then `/commit-push-close` / `/commit-push-pr` (or proceed to PM handoff); any `fail` → suggest `/to-tickets` or `/diagnosing-bugs` for the failing flow. Then stop.

## Output format

**build update:**

```markdown
Stage: build — wrote specs/integration/<SPEC-ID>-contract.md.   [or: single project — no contract needed (matrix swept; no external call-sites)]
Found: producer <PROJECT-CODE>; consumers <PROJECT-CODE>, <PROJECT-CODE>; <K> changed surfaces; <R> risk row(s).
Next: implement the slices, then run integration-contract in gate mode before the spec-level ship and before PM handoff.
Needs user: <risk rows to confirm, environment facts to supply, or "none">.
```

**gate report:**

```markdown
Env verified: <service(s)> rebuilt/redeployed; change confirmed in served artifact (<how>).

| # | Flow | Crosses | Driver | Status |
| - | ---- | ------- | ------ | ------ |
| 1 | ...  | ADMIN-WEB, API-SVC | agent-browser | pass |
| 2 | ...  | ADMIN-WEB, API-SVC | agent-browser | fail |

Reopened by failures (blocking, not shipped): #2.

Suggested next skills (optional):
- /to-tickets: slice the fix for the failing seam (#2).
- /code-review then /commit-push-*: only once every flow is pass.
```

## Checklist

Before ending a mode:
- [ ] Trigger discipline applied: multi-project → contract; single-project → other matrix repos swept for external call-sites first, and `single project — no contract needed` (no file) only when none were found
- [ ] Contract written to `<artifacts-root>/specs/integration/<SPEC-ID>-contract.md` and re-opened — all four section headings plus the gate log verified present
- [ ] Section 1 records, per involved PROJECT-CODE: where it runs, how a change reaches it, and the flows' data preconditions — asked, never guessed
- [ ] Section 3 cites every located consumer as `file:symbol`, searched across all Project Matrix repos (no bulk repo/`specs/` reads); out-of-spec consumers and unconsumed surfaces are `RISK` rows
- [ ] Section 4 flows are navigate→act→assert, each with a Driver (agent-browser / curl / manual) and the PROJECT-CODEs it crosses
- [ ] No project's conventions bled into another's rows
- [ ] gate: environment verified first — services reachable, change confirmed in the served artifact, contract spot-checked against the implemented code, data seeded — before any flow counted
- [ ] gate: every `pass`/`fail` has Evidence; undrivable flows stayed `pending` and were listed as manual steps, never assumed
- [ ] gate: ran at the spec-level ship and at PM handoff, with a gate-log line appended per run; per-slice ships were not blocked by flows crossing unimplemented slices
- [ ] gate: any `fail` reopened the contract, was surfaced, and blocked the step — nothing silently dropped
- [ ] Suggested next skills footer present; never auto-chained build → gate → ship

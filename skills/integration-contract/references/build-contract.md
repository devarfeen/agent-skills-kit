# Contract build schema

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Load when building a contract or repairing its structure/coverage during gate.

```markdown
# Integration Contract — <SPEC-ID>

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Touched PROJECT-CODEs: API-SVC (producer), ADMIN-WEB

## 1. Environment & preconditions

| PROJECT-CODE | Runs at | Change reaches it via | Data preconditions |
|-|-|-|-|
| API-SVC | http://localhost:8080 | `docker compose up --build api` | a `partially_shipped` order |

## 2. Producer surface changed

| PROJECT-CODE | Surface | Change |
|-|-|-|
| API-SVC | `POST /v2/orders` | added required `idempotency_key`; auth unchanged (customer session), no new personal data; `rollout-dependent — ADMIN-WEB first` |

## 3. Consumers

| Consumer PROJECT-CODE | Consumes surface | Call-site (file:symbol) | Notes / Risk |
|-|-|-|-|
| ADMIN-WEB | `POST /v2/orders` | `resources/js/checkout/submit.ts:createOrder()` | `normalized-route`; sends no `idempotency_key` yet |
| — | `POST /v2/orders` (idempotency_key) | NO CONSUMER LOCATED | RISK: unused, or call-site missed |

## 4. Smoke checklist

| # | Flow | Crosses | Driver | Evidence | Status |
|-|-|-|-|-|-|
| 1 | ADMIN-WEB checkout → submit order → confirmation shows order number | ADMIN-WEB, API-SVC | agent-browser | | pending |

## Gate log

- <date> · pre-ship · 3 pass / 1 fail (#2) · env: API-SVC rebuilt, `partially_shipped` in served response
```

Section rules:

- **1** — captured at build, verified at gate: where each PROJECT-CODE runs, how a change reaches it (build/serve/deploy step), the flows' data. Fact not cheaply discoverable → ask — never guess; user away → record `unknown — ask` under Needs user and keep building — the gate cannot pass a flow whose environment is unknown.
- **2** — one row per surface the producer slice added or changed. `Change` also states auth/permission impact, any added or exposed personal data, and its rollout class: `compatible`, `rollout-dependent — <order>`, `breaking`, or `insufficient context` (classification in the sweep reference). A breaking auth or personal-data change is a `RISK` row and requires a smoke flow. A `RISK` row on an internet-facing or personal-data-carrying surface always gets a smoke flow, breaking or not.
- **4** — enough end-to-end flows to cover every changed surface and required risk case, usually 3–6, phrased **navigate → act → assert a visible outcome**. **Driver**: `agent-browser` when browser-reachable, an exact `curl`/CLI assertion for API-only surfaces, else `manual` with the step spelled out. When a changed surface carries auth, include one negative flow: the unauthorized caller or role is denied.
- **Gate log** — one appended line per run, `<date> · <pre-ship|PM handoff> · <N> pass / <M> fail (#s) · <how the environment was verified>`; `Status` shows the latest, the log keeps history.

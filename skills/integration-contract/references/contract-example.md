# Filled contract example

A fully worked instance of the contract artifact — the skeleton and section rules live in `SKILL.md`. Match this concreteness; placeholders never ship.

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

```markdown
# Integration Contract — SPEC-142

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Touched PROJECT-CODEs: API-SVC (producer), ADMIN-WEB, MOBILE-APP

## 1. Environment & preconditions

| PROJECT-CODE | Runs at | Change reaches it via | Data preconditions |
|-|-|-|-|
| API-SVC | http://localhost:8080 | `docker compose up --build api` | a `partially_shipped` order |
| ADMIN-WEB | http://localhost:5173 | `pnpm dev` serves source live | user with checkout permission |
| MOBILE-APP | local emulator, API at http://localhost:8080 | documented local app build | same order and authorized test account |

## 2. Producer surface changed

| PROJECT-CODE | Surface | Change |
|-|-|-|
| API-SVC | `POST /v2/orders` | added required `idempotency_key`; auth unchanged (customer session), no new personal data |
| API-SVC | `GET /v2/orders/{id}` | `status` enum gains `partially_shipped` |

## 3. Consumers

| Consumer PROJECT-CODE | Consumes surface | Call-site (file:symbol) | Notes / Risk |
|-|-|-|-|
| ADMIN-WEB | `POST /v2/orders` | `resources/js/checkout/submit.ts:createOrder()` | sends no `idempotency_key` yet |
| MOBILE-APP | `GET /v2/orders/{id}` | `src/screens/OrderDetail.tsx:useOrder()` | RISK: outside the spec — new slice via /to-tickets |
| — | `POST /v2/orders` (idempotency_key) | NO CONSUMER LOCATED | RISK: unused, or call-site missed |

## 4. Smoke checklist

| # | Flow | Crosses | Driver | Evidence | Status |
|-|-|-|-|-|-|
| 1 | ADMIN-WEB checkout → submit order → confirmation shows order number | ADMIN-WEB, API-SVC | agent-browser | | pending |
| 2 | `POST /v2/orders` with no session token → denied (401/403), no order row created | API-SVC | curl | | pending |
| 3 | Open a partially shipped order in MOBILE-APP; its status is visible without an unknown-status error | MOBILE-APP, API-SVC | manual: open order detail and inspect status | | pending |

## Gate log

- No gate run yet. All 3 flows are pending; environment and served change are unverified.
```

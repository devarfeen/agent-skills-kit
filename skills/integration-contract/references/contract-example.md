# Filled contract example

A fully worked instance of the contract artifact — the skeleton and section rules live in `SKILL.md`. Match this concreteness; placeholders never ship.

```markdown
# Integration Contract — SPEC-142

Touched PROJECT-CODEs: API-SVC (producer), ADMIN-WEB, MOBILE-APP

## 1. Environment & preconditions

| PROJECT-CODE | Runs at | Change reaches it via | Data preconditions |
|-|-|-|-|
| API-SVC | http://localhost:8080 | `docker compose up --build api` | a `partially_shipped` order |
| ADMIN-WEB | http://localhost:5173 | `pnpm dev` serves source live | user with checkout permission |

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

## Gate log

- 2026-08-12 · pre-ship · 3 pass / 1 fail (#2) · env: API-SVC rebuilt, `partially_shipped` in served response
```

# PR example

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

A filled PR title and body for issue #418, following the template in `SKILL.md`. The matching commit message lives in **Commit examples** in [`ship-policy.md`](ship-policy.md). Optional sections (**Decisions**, **Notes**) are simply omitted when empty.

PR title: `add idempotency keys to checkout flow`

PR body:
```
Closes #418

## Summary
Checkout charges are now idempotent on `x-request-id`; replays return the original result instead of double-charging.

## Where changed
`POST /checkout`, implemented in `server/checkout/handler.ts`; replay tests in `server/checkout/handler.test.ts`.

## Decisions
- Stored keys in Redis (24h TTL) over Postgres — the read path is hot
- Reused existing `x-request-id` header instead of a new one

## How to test
Setup: run this branch locally with a test account and the repo's payment sandbox.
1. `pnpm test server/checkout/handler.test.ts` — passing tail quoted below:
       Test Files  1 passed (1)
            Tests  6 passed (6)
         Duration  1.24s
2. Hit `POST /checkout` twice with the same `x-request-id` — second call returns the first response, no second Stripe charge
3. Hit twice with different IDs — two distinct charges as before
Manual API checks pending. Remove test orders afterward.

## Evidence
- Before: `handler.test.ts` "replays return the original result" failed at base — expected 1 charge, received 2
- After: the same test passes (6 passed)

## Merge danger
Door: two-way — reverting the commit restores the old path; idempotency keys expire in 24h
Blast radius: checkout API clients — checked: `rg "x-request-id"` shows only the web client sends it

## Notes
- Stripe webhook path still unguarded — see follow-up #419
```

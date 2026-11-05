# Polish-batch behavior evaluation

Date: 2026-09-09. Method: fresh-reader simulated execution. No product files, browser sessions, or dispatched workers were changed. One execution per fixture.

Zero attribution: never add or leave co-author, AI, or tool attribution in commits, PRs, issues, docs, or comments.

## PB-1: Capture in a dirty worktree

Input: Existing unrelated modification in `src/auth.ts`. User reports `Recieve invoices` on ADMIN-WEB Billing, a screenshot nit with unknown project, and asks whether clicking a warning should dismiss it.

Output fragment:

```markdown
| 1 | ADMIN-WEB | Settings > Billing header | Recieve invoices → Receive invoices | (no shot — text only) | open |
| 2 | ADMIN-WEB? | Reported screenshot location | Reported visual mismatch | shots/unassigned-02.png | open |

## Held — awaiting cosmetic/behavioural call
Whether the warning should dismiss on click needs a behavior decision.
```

Actions: record initial status/diff; write only QA artifacts, mark guessed project unresolved, preserve `src/auth.ts`, ask for the missing project/scope decision. No nit is fixed.

Assertions: QA-only writes PASS; original edit preserved PASS; uncertainty visible PASS. Result: 3/3.

## PB-2: No dispatch from an old promise

Input: Earlier message says "fix them all later" during capture. User now adds the last nit. No fresh dispatch instruction exists.

Output: "Stage: capture. Next: keep capturing, or say dispatch to fix open rows. Needs user: unresolved project for row 2."

Actions: append the nit and stop. When a later explicit dispatch arrives, group only confirmed-project rows and keep row 2 pending.

Assertions: no automatic dispatch PASS; ambiguous row excluded PASS; no automatic shipping PASS. Result: 3/3.

## PB-3: Source fixed, served output stale

Input: Dispatched Billing typo changed in source; browser still renders `Recieve invoices`. A separate reported task changes API response shape.

Output: "Found: Billing row reopened; rendered text remains 'Recieve invoices'. Routed out: API response-shape change requires a slice. Next: another dispatch after the asset pipeline issue is resolved."

Actions: compare run diff to pre-dispatch state, preserve unrelated edits, record served text, reopen typo row. Route behavior work without a cosmetic row and report it explicitly.

Assertions: source-only proof rejected PASS; behavior task routed out PASS; completion accounts for route-outs PASS. Result: 3/3.

## Limits

9/9 assertions passed in three simulations. No capture, dispatch, browser verification, or test update was exercised in a real application. Existing test assertions and cross-project file conflicts still need live workflow coverage.

# PR simulation results

Zero attribution: omit co-author, AI, and tool attribution from all output.

Date: 2026-09-09. Method: independent review and simulated execution of `audit-behavior-cases.md`. The baseline is the pre-edit audit snapshot. No GitHub operation, commit, push, manual API request, or deployment was executed. URLs and command outcomes below come from the fixture and are not publication evidence.

## PR-1

The initial fixture omitted method/path and safe request evidence. Following the revised policy required that information instead of inventing it. The completed fixture supplies `POST /checkout`, the JSON request, success payload, and URLs used below.

Revised PR title: `Return a clear checkout timeout response`

Revised body:

```markdown
Closes #520

## Summary
Checkout returns a clear timeout response when the mock payment provider times out.

## Where changed
`POST /checkout`: `api/checkout.ts` returns HTTP 504 and the payment_timeout error; `api/checkout.test.ts` covers timeout and successful checkout.

## How to test
Setup: run revision def5678 locally with `pnpm dev:api` at http://localhost:4000. Use the repo's mock payment provider and disposable qa-order-1 order; this local example requires no authentication.
1. Set the documented local mock toggle MOCK_PAYMENT_TIMEOUT=true and start/restart the local API. Send `curl -i -X POST http://localhost:4000/checkout -H 'Content-Type: application/json' -d '{"orderId":"qa-order-1"}'`. Expect HTTP 504 and {"error":"payment_timeout"}.
2. Restore the toggle to disabled, restart the local API, and send the same request. Expect HTTP 200 and {"status":"paid","orderId":"qa-order-1"}.
3. Run `pnpm test api/checkout.test.ts`. Recorded result on this content: 6 tests passed. Manual requests remain pending.
4. Remove the disposable mock order and restore the original local mock configuration.

## Notes
No deployment has been verified. The PR awaits review and merging into develop before automatic issue closure.
```

Separate revised QA comment:

```markdown
## QA handoff
Change: def5678 on `fix/520-timeout`; https://github.com/example/demo/pull/81.

### What changed
Checkout now returns a clear timeout error when the payment provider times out.

### Where changed
- `POST /checkout`: `api/checkout.ts` handles the provider timeout.
- `api/checkout.test.ts` covers timeout and successful-payment responses.

### Setup
Run revision def5678 locally with `pnpm dev:api` at http://localhost:4000, using the repo's mock provider. The supplied local example needs no authentication. Use disposable mock order qa-order-1 and record the original mock-toggle value.

### How to test
1. Set the documented local MOCK_PAYMENT_TIMEOUT toggle to true and start/restart the local API. Send `curl -i -X POST http://localhost:4000/checkout -H 'Content-Type: application/json' -d '{"orderId":"qa-order-1"}'`. Expect HTTP 504 with {"error":"payment_timeout"}.
2. Disable the toggle and restart the local API. Send the request again. Expect HTTP 200 with {"status":"paid","orderId":"qa-order-1"}.
3. Run `pnpm test api/checkout.test.ts`. Expect all timeout and success cases to pass.

### Verification
Automated command passed 6 tests on this content. Manual API requests remain pending. No deployment was checked.

### Gaps
Restore the original local mock-toggle value and remove the disposable mock order after QA.
```

Simulated ordered actions: inspect complete index and test/content match; reuse combined approval; commit the intended files; push; verify remote SHA def5678; confirm no matching PR exists; create PR #81 against develop with the body above; read title/body/base/head; attempt comment. First comment failure yields: `def5678 pushed; PR #81 opened against develop; QA handoff incomplete because comment posting failed. Issue #520 remains open.`

On retry: inspect #81's comments, find no matching SHA handoff, post only the missing comment, and read back its body plus fixture URL. No new commit, push, or PR creation occurs. Final simulated report: `def5678 pushed to fix/520-timeout; PR #81 opened against develop; QA: https://github.com/example/demo/pull/81#issuecomment-9001. Issue #520 closes when this PR merges into develop.` The advisory footer follows; no merge or direct issue closure occurs.

Result: all 5 assertions satisfied with the completed fixture. The 6-test result is fixture evidence, not a test run performed by this evaluation.

Baseline result: the old PR body can include runnable API steps and a passing test tail, but its template has no required changed-location section, no separate QA comment, no comment read-back, and no retry procedure for a partial comment failure. It cannot satisfy the new dedicated QA-comment assertions without instructions outside the original skill. The revised text preserves the baseline's review-before-merge stopping point.

## PR-2

Revised draft fields: base `staging`; head `local`; ordinary issue reference `Issue: #521`. State that issue completion follows workspace policy, not GitHub default-branch closing keywords. The fixture does not supply the change's title, diff, or test command, so no invented full body or results are added; its existing approved drafts are reused for this push-failure case.

Simulated actions: verify permitted origin/local to staging route; keep main excluded; confirm local checks already cover the content and reuse approval; commit the intended change; attempt `git push`; stop when it returns non-fast-forward. Do not create/edit/comment a PR, access a server, force-push, reset, merge, or close the issue.

Simulated response: `The commit exists locally on local. Push to origin/local was rejected as non-fast-forward; no PR or QA comment was published. Reconcile the remote branch before resuming delivery to staging.`

Result: all 4 assertions satisfied. The fixture lacks a commit SHA, so the report does not invent one.

Baseline result: the original workflow always selects the default PR base and always requires Closes #N, even when the user explicitly targets staging and main is prohibited. Correct execution under workspace restrictions must stop at that conflict. The revised base-selection and remote-verification gates provide an unambiguous permitted route and an explicit stop at push rejection.

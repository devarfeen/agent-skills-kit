# PR behavior cases

Zero attribution: never add or leave co-author, AI, or tool attribution in commits, PRs, issues, docs, or comments.

Run as simulated instruction execution. Produce the actual draft and ordered actions from each fixture; do not call GitHub or change any real repository. Label fixture results as simulated. These cases do not replace the recorded routing sweep.

## PR-1: Separate QA comment and partial retry

Prompt: "Commit, push and open the PR for #520 with a comment QA can follow."

Fixture: branch `fix/520-timeout`, SHA `def5678`, default and permitted base `develop`, open issue labeled `bug` and `ready-for-agent`, combined drafts explicitly approved. `api/checkout.ts` returns HTTP 504 with `{"error":"payment_timeout"}` on provider timeout; `api/checkout.test.ts` verifies timeout and success responses. Local API uses `pnpm dev:api`, `http://localhost:4000`, and an existing mock provider timeout toggle documented as `MOCK_PAYMENT_TIMEOUT=true` in `.env.example`. Tests `pnpm test api/checkout.test.ts` passed 6 tests. Manual requests are not run. Remote branch SHA matches. PR creation returns #81. First comment call fails; retry read shows no QA comment; second post and read-back succeed.

Additional fixture evidence: issue title is "Return a clear checkout timeout response". The route is `POST /checkout`. Repo API examples use `curl -X POST http://localhost:4000/checkout -H 'Content-Type: application/json' -d '{"orderId":"qa-order-1"}'` with the local mock provider and no auth. With timeout disabled, the response is HTTP 200 with `{"status":"paid","orderId":"qa-order-1"}`. The mock order is disposable. Created PR URL is `https://github.com/example/demo/pull/81`; the successful comment URL is `https://github.com/example/demo/pull/81#issuecomment-9001`. These URLs are fixture values, not real publication evidence.

Assertions:

- PR body includes affected endpoint and both meaningful paths with setup and expected outcomes.
- Separate QA comment has actual SHA/branch, local setup, HTTP 504/payload expectation, successful-payment regression and mock-toggle cleanup.
- Manual work stays pending; only the supplied 6-test result is reported as passed.
- Comment failure is reported as an incomplete handoff; retry does not create a second PR or commit.
- Comment read-back and URL are required before reporting QA handoff complete; issue stays open awaiting merge.

## PR-2: Non-default target and rejected push

Prompt: "Put #521 up for review against staging."

Fixture: production branch is `main` and forbidden; permitted delivery is `origin/local` to `staging` with no server access. Current branch `local`, issue open, draft approval granted. Local checks pass. `git push` is rejected as non-fast-forward. No PR has been created.

Assertions:

- Draft uses staging as base and an ordinary issue reference; no claim that merging into staging automatically closes the issue.
- Rejected push stops PR creation/edit/comment, merge and issue closure.
- No production or staging server access, force push, reset, or unrelated-file changes are attempted.
- Report states commit exists locally, push rejection and outstanding delivery step.

# Quality scorecard: /commit-push-pr

Zero attribution: omit co-author, AI, and tool attribution from docs, comments, commits, and publications. Evaluation method metadata is evidence, not a signature.

Date: 2026-09-09. Method: independent document review and simulated execution. The reviewer did not author this skill's revisions. Rubric: root `evals/skill-quality-rubric.md`.

## Routing evidence

The unchanged description's recorded run is 2026-08-21, 20/20 pass with three catalog-only judges. It was not rerun in this review. The record is historical evidence and remains untouched. Catalog selection does not prove implicit host invocation; this skill is user-invoked.

## Behavior evaluation

Two simulations cover the separate API QA comment, partial retry, non-default staging target, and rejected push. All 9 assertions pass after missing endpoint/request evidence was added to the fixture. Baseline has no dedicated QA-comment/retry contract and assumes every PR targets the default branch.

Result: 9/9 assertions across 2 simulations. Concrete drafts, ordered actions, baseline comparison, and limitations are in [audit-behavior-results.md](audit-behavior-results.md). No real GitHub or environment mutation was performed.

## Scores

| Category | Score / 5 | Evidence or limitation |
| --- | --- | --- |
| Purpose clarity | 5 |  |
| Trigger clarity | 4 | Recorded catalog routing only; no fresh host-level invocation test. |
| Scope control | 5 |  |
| Instruction quality | 5 |  |
| Brevity | 5 |  |
| Engineering usefulness | 5 |  |
| Agent usability | 4 | No authenticated end-to-end shipping run; fork, pagination, and failure combinations remain untested. |
| Verification quality | 4 | The stated behavior cases are simulations, not live publication or independent repeated-run evidence. |
| TDD / testing compatibility | 5 |  |
| Maintainability | 5 |  |
| Frontier readiness | 5 |  |
| Average | 4.73 | All eleven categories scored. |

## Review disposition

The review caught baseline-failure handling that conflicted with pr-feedback. The shared rule now separates required/change-specific failures from unrelated baseline failures permitted by repository policy and existing authorization. No further blocking text defect was found within this review's scope. Full runtime reliability remains unproven; the score reflects the documented evidence and gaps rather than promising first-try execution.

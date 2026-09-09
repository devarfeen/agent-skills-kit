# Quality scorecard: /staging-fix

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Date: 2026-09-09. Method: independent document review and three simulated execution cases; the reviewer did not write the skill changes. Rubric: [skill-quality-rubric.md](../../../evals/skill-quality-rubric.md).

## Scope and routing evidence

Read the revised body, settings mirror, routing record and author runtime-command evidence. Simulated local fix with immediate merge, production refusal, and ambiguous deployment routing.

The recorded trigger run is 15/15 on 2026-08-21 in [evals.json](evals.json). It was not rerun for this body-only audit. Description provenance still matches the recorded snapshot. A historical catalog-only score neither proves a current independent routing run nor proves implicit invocation of a user-only skill. No last_run metadata was restamped.

## Scores

| Category | Score / 5 | Evidence or remaining gap |
| :--- | :---: | :--- |
| Purpose clarity | 5 | No defect found in the reviewed text and stated simulation scope. |
| Trigger clarity | 4 | Historical 2026-08-21 catalog result only; no current host invocation trial. |
| Scope control | 5 | No defect found in the reviewed text and stated simulation scope. |
| Instruction quality | 5 | No defect found in the reviewed text and stated simulation scope. |
| Brevity | 5 | No defect found in the reviewed text and stated simulation scope. |
| Engineering usefulness | 5 | No defect found in the reviewed text and stated simulation scope. |
| Agent usability | 4 | Immediate merge, protected-branch and merge-queue behavior were not exercised against an authenticated repository. |
| Verification quality | 4 | Local-to-staging execution is simulated; no real merge or deployment run proves the full sequence. |
| TDD / testing compatibility | 5 | No defect found in the reviewed text and stated simulation scope. |
| Maintainability | 5 | No defect found in the reviewed text and stated simulation scope. |
| Frontier readiness | 5 | No defect found in the reviewed text and stated simulation scope. |
| Average | 4.73 | All eleven categories included. |

## Behavioral checks

[behavioral-results.md](behavioral-results.md) records all fixtures, ordered actions and simulated outputs. Result: 3/3 simulated cases passed. No live success is implied.

The author added origin/local delivery compliance, explicit stage/commit, exact base/head read-back, pinned merge identity, deployment-evidence wording, preservation of unrelated changes, and approved missing-issue creation.

## Remaining limits

No SSH, staging/production access, remote write, PR merge or deployment occurred. The simulated passing regression and merged SHA are supplied fixtures. Live repository permissions and CI routing must be checked in the actual workflow.

Repository validation checks structure and provenance; it does not enforce these natural-language instructions at runtime. A 5 means no defect found within this review scope, not guaranteed execution on an untested task.

# Quality scorecard: /orchestrate-herdr

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Date: 2026-09-09. Method: independent document review and three simulated execution cases; the reviewer did not write the skill changes. Rubric: [skill-quality-rubric.md](../../../evals/skill-quality-rubric.md).

## Scope and routing evidence

Read the skill, all four references, settings mirror, and routing record. Simulated two isolated successful workers, outside-herdr refusal, and a submission timeout with a continuing long test.

The recorded trigger run is 27/27 on 2026-08-21 in [evals.json](evals.json). It was not rerun for this body-only audit. Description provenance still matches the recorded snapshot. A historical catalog-only score neither proves a current independent routing run nor proves implicit invocation of a user-only skill. No last_run metadata was restamped.

## Scores

| Category | Score / 5 | Evidence or remaining gap |
| :--- | :---: | :--- |
| Purpose clarity | 5 | No defect found in the reviewed text and stated simulation scope. |
| Trigger clarity | 4 | Historical 2026-08-21 catalog result only; no current host invocation trial. |
| Scope control | 5 | No defect found in the reviewed text and stated simulation scope. |
| Instruction quality | 5 | No defect found in the reviewed text and stated simulation scope. |
| Brevity | 5 | No defect found in the reviewed text and stated simulation scope. |
| Engineering usefulness | 5 | No defect found in the reviewed text and stated simulation scope. |
| Agent usability | 4 | No live herdr worker creation/launch, alternate-screen recovery, or tracker-block transition was exercised. |
| Verification quality | 4 | Three lifecycle branches were simulated; command-help evidence does not prove prompt acceptance and report scraping end to end. |
| TDD / testing compatibility | 5 | No defect found in the reviewed text and stated simulation scope. |
| Maintainability | 4 | The fixed runtime roster and tracker-specific schema still require installation-specific checks; not all worker-host internals were refreshed. |
| Frontier readiness | 4 | Worker behavior across six runtime hosts remains untested despite the available-tool fallback. |
| Average | 4.55 | All eleven categories included. |

## Behavioral checks

[behavioral-results.md](behavioral-results.md) records all fixtures, ordered actions and simulated outputs. Result: 3/3 simulated cases passed. No live success is implied.

The author corrected kind/token confusion, required isolation choice, saved per-worker contexts, pagination, bounded waits, duplicate-submission risk, stale silence heuristic and question-tool limits. No cloud or nested-orchestrator boundary was removed.

## Remaining limits

Installed herdr help and schema evidence reported by the author supports command syntax. No live herdr control command, tracker mutation, worker launch or end-to-end report capture was performed. A test tail in a simulation is a fixture, not a test run.

Repository validation checks structure and provenance; it does not enforce these natural-language instructions at runtime. A 5 means no defect found within this review scope, not guaranteed execution on an untested task.

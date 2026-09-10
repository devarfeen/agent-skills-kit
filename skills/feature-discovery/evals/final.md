# Quality scorecard: /feature-discovery

Date: 2026-09-09. Method: independent document review and isolated simulated execution against the revised body and references. The reviewer did not write the skill changes. Scored using [the root rubric](../../../evals/skill-quality-rubric.md). Simulations exercise instruction decisions; they do not establish live runtime reliability.

This scorecard predates the purpose-focused changes approved on 2026-09-10.
The updated behavioral evidence is in
[behavioral-results.md](behavioral-results.md#purpose-focused-regression);
the historical quality scores below were not rerun or restamped.

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

## Routing evidence

`evals.json` records **22/22 pass on 2026-08-21**, by three catalog-only judges with majority voting. This historical run was **not rerun** during this review; its description and `last_run` were not restamped. Historical catalog routing passed; no changed description or fresh routing run is claimed.

## Scores

| Category | Score / 5 |
| --- | ---: |
| Purpose clarity | 5 |
| Trigger clarity | 5 |
| Scope control | 5 |
| Instruction quality | 5 |
| Brevity | 5 |
| Engineering usefulness | 5 |
| Agent usability | 4 |
| Verification quality | 4 |
| TDD / testing compatibility | N/A |
| Maintainability | 5 |
| Frontier readiness | 5 |
| Average | **4.80** |

Agent usability is 4 because no actual repository traversal, inaccessible upstream lookup, or graph command was executed. Verification quality is 4 because citations and read-only behavior were exercised on hypothetical fixtures, not a real repository.

TDD/testing compatibility is N/A: discovery emits a read-only explanation and neither produces code nor gates on a test run.

## Findings and observed decisions

No remaining anchored instruction defect found in this review. All three authored behavior simulations passed: absent dependency internals, quick trace without context approval, and narrowly extending an old history lookup.

See [behavioral results](behavioral-results.md) for fixtures, produced actions/output, individual pass/fail results, and limits. A pass means the simulated response followed the inspected rules; it does not claim files were written, tests ran, services were accessed, or the host loaded the skill.

## Verdict

The reviewed branches are ready for live workflow evaluation. No unresolved instruction defect remains from this independent pass. Scores are bounded by the stated document/simulation evidence and should not be read as measured production reliability.

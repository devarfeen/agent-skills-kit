# Quality scorecard: /feature-prompt

Date: 2026-09-09. Method: independent document review and isolated simulated execution against the revised body and references. The reviewer did not write the skill changes. Scored using [the root rubric](../../../evals/skill-quality-rubric.md). Simulations exercise instruction decisions; they do not establish live runtime reliability.

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

## Routing evidence

`evals.json` records **22/22 pass on 2026-08-21**, by three catalog-only judges with majority voting. This historical run was **not rerun** during this review; its description and `last_run` were not restamped. The recorded catalog result includes one 2/3 disagreement that still passed the negative case. This user-only skill's host invocation was not exercised.

## Scores

| Category | Score / 5 |
| --- | ---: |
| Purpose clarity | 5 |
| Trigger clarity | 4 |
| Scope control | 5 |
| Instruction quality | 5 |
| Brevity | 5 |
| Engineering usefulness | 5 |
| Agent usability | 5 |
| Verification quality | 4 |
| TDD / testing compatibility | N/A |
| Maintainability | 5 |
| Frontier readiness | 5 |
| Average | **4.80** |

Trigger clarity is 4 because catalog routing does not prove actual invocation behavior for a user-only skill. Verification quality is 4 because save/read-back, numbering, and preservation were simulated; no actual output-file collision or concurrent write was exercised.

TDD/testing compatibility is N/A: the skill writes a planning prompt and does not create code or gate on tests.

## Findings and observed decisions

No remaining anchored instruction defect found. All three simulations passed: an unconfirmed draft, context terms without approval, and a new revision preserving an edited existing prompt.

See [behavioral results](behavioral-results.md) for fixtures, produced actions/output, individual pass/fail results, and limits. A pass means the simulated response followed the inspected rules; it does not claim files were written, tests ran, services were accessed, or the host loaded the skill.

## Verdict

The reviewed branches are ready for live workflow evaluation. No unresolved instruction defect remains from this independent pass. Scores are bounded by the stated document/simulation evidence and should not be read as measured production reliability.

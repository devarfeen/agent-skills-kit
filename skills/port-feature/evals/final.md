# Quality scorecard: /port-feature

Date: 2026-09-09. Method: independent document review and isolated simulated execution against the revised body and references. The reviewer did not write the skill changes. Scored using [the root rubric](../../../evals/skill-quality-rubric.md). Simulations exercise instruction decisions; they do not establish live runtime reliability.

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

## Routing evidence

`evals.json` records **22/22 pass on 2026-08-21**, by three catalog-only judges with majority voting. This historical run was **not rerun** during this review; its description and `last_run` were not restamped. The user-only skill's historical routing result is preserved; host invocation was not exercised.

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

Trigger clarity is 4 because the catalog does not demonstrate host invocation. Verification quality is 4 because gap-map preservation, project-pair filename handling, and preview limitations were simulated; actual repository/file/preview behavior was not exercised.

TDD/testing compatibility is N/A: the skill lists tests needed for a future port but neither implements code nor gates completion on test results.

## Findings and observed decisions

The reviewer found a cross-project filename collision at the original artifact path. The editor added pair checking and the qualified fallback at SKILL.md:68, and the completion criterion follows the resolved path. Three authored simulations plus a separate collision simulation passed after rereading that fix.

See [behavioral results](behavioral-results.md) for fixtures, produced actions/output, individual pass/fail results, and limits. A pass means the simulated response followed the inspected rules; it does not claim files were written, tests ran, services were accessed, or the host loaded the skill.

## Verdict

The reviewed branches are ready for live workflow evaluation. No unresolved instruction defect remains from this independent pass. Scores are bounded by the stated document/simulation evidence and should not be read as measured production reliability.

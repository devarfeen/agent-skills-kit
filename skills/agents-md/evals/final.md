# Quality scorecard: /agents-md

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Date: 2026-09-09. Method: independent document review and three simulated execution cases; the reviewer did not write the skill changes. Rubric: [skill-quality-rubric.md](../../../evals/skill-quality-rubric.md).

## Scope and routing evidence

Read the skill, both templates, every reference including the six runtime mappings, settings mirror, and recorded routing evidence. Simulated normal generation, missing-workspace refusal, and duplicate-code/user-edit preservation.

The recorded trigger run is 20/20 on 2026-08-21 in [evals.json](evals.json). It was not rerun for this body-only audit. Description provenance still matches the recorded snapshot. A historical catalog-only score neither proves a current independent routing run nor proves implicit invocation of a user-only skill. No last_run metadata was restamped.

## Scores

| Category | Score / 5 | Evidence or remaining gap |
| :--- | :---: | :--- |
| Purpose clarity | 5 | No defect found in the reviewed text and stated simulation scope. |
| Trigger clarity | 4 | Historical 2026-08-21 catalog result only; no current host invocation trial for this user-only skill. |
| Scope control | 5 | No defect found in the reviewed text and stated simulation scope. |
| Instruction quality | 5 | No defect found in the reviewed text and stated simulation scope. |
| Brevity | 5 | The author removed the ornamental Rule 11 enforcement slogan after review; no further no-op defect found in the reviewed scope. |
| Engineering usefulness | 5 | No defect found in the reviewed text and stated simulation scope. |
| Agent usability | 4 | references/tool-calling.md retains July verification for several host-specific tool/settings rows; no six-host generation-and-load trial. |
| Verification quality | 4 | Template/matrix/preservation branches were simulated, not generated and loaded in each supported host. |
| TDD / testing compatibility | 5 | No defect found in the reviewed text and stated simulation scope. |
| Maintainability | 4 | Large per-runtime and memory tables retain older verification dates; only the corrected subset was re-verified this pass. |
| Frontier readiness | 4 | The live-schema fallback is sound, but full emitted-table compatibility remains untested across the supported hosts. |
| Average | 4.55 | All eleven categories included. |

## Behavioral checks

[behavioral-results.md](behavioral-results.md) records all fixtures, ordered actions and simulated outputs. Result: 3/3 simulated cases passed. No live success is implied.

The author corrected code normalization collisions, stack inference, template output/handoff conflicts, context precedence, migration completion, and several runtime permission/config claims. Fresh-review corrections were read back before scoring.

## Remaining limits

No generated artifact was loaded by all six CLI hosts. Antigravity/Cursor/Copilot internals and native-memory examples were read, but this pass did not freshly verify every fact; their historical stamps remain. No personal runtime settings were read or edited.

Repository validation checks structure and provenance; it does not enforce these natural-language instructions at runtime. A 5 means no defect found within this review scope, not guaranteed execution on an untested task.

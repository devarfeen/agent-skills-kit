# Routing sweep 2026-10-22

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Reason: `/plain-language` was added, `/orchestrate-herdr`'s description changed, and the companion catalog dropped the Cursor helper, so the recorded routing run had to be redone. Final inputs: [catalog](catalog.md), [queries](queryset.md), [manifest](query-manifest.json); final ballots `j1.jsonl`, `j2.jsonl`, `j3.jsonl`.

Three sweeps were run, each with three fresh catalog-only judge sessions on the maintainer session's model:

1. `sweep1/`: 589/591 under the old pass rule. Two no-trigger queries (pixel-audit, polish-batch) split three ways with no vote for the skill under test.
2. `sweep2/`: 589/591 under the old rule. One three-way no-target split (design-system) and one real miss: "What's the status of the worker tabs?" routed unanimously to `/orchestrate-herdr`.
3. Final: 591/591 after two changes. The pass rule now accepts a no-trigger query that gets no vote for the skill under test (three different non-target picks prove the description did not fire); `/orchestrate-herdr` 0.7.2 names tab status checks as the herdr companion's. Rescored under the new rule, sweep 1 is 591/591 and sweep 2 is 590/591 with only the herdr miss, which the description change addresses.

The sweep 1 and 2 ballots were cast against the pre-change catalog and are kept as evidence, not as passing runs. Judge independence rests on fresh sessions with no repository access; the hashes identify the files used.

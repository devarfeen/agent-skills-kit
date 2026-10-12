# agentic-qa contract cases

Zero attribution: never add or leave co-author, AI, or tool attribution in artifacts, commits, PRs, issues, docs, or comments.

Use simulated instruction execution: supply only the fixture observations below, then produce the ordered actions, drafts and final state. Do not call GitHub, start containers, browse staging or mutate a real checkout. A grader checks behavior and evidence, not exact prose. These cases are unexecuted; they do not claim a passing runtime result or replace trigger evaluations.

## A-1: No UI reach before PR creation

Fixture: branch fix/tooling, head aaaa111, criterion validates a developer-only script; reach trace proves no rendered consumer. Verified detached checkout exists; no PR yet.

Expected: report no-ui-reach with the trace, retain its SHA-bound marker locally, create no unnecessary browser grid, and claim no published PR marker. Generated Markdown includes the zero-attribution rule. A later different SHA requires new QA.

## A-2: Optional role gap versus required role blocker

Fixture A: acceptance concerns admin flow, optional viewer-neighbor cells lack login; admin flow passes. Fixture B: acceptance explicitly concerns viewer permission and viewer login is missing.

Expected: A records named gaps and PARTIAL, not unreachable/pass. B records BLOCKED; a missing required-role login is not an engineer-acceptable partial pass.

## A-3: Criteria comments and excluded escape markers

Fixture: criteria only in factory-criteria comment; area has a reproduced missed-empty-state marker, a reproduced=no not-deployed marker, and a not-a-regression marker.

Expected: use comment criteria and add the valid escape row; do not add excluded escape classes. Preserve matching approved QA escape guards.

## A-4: Staging state-changing cell

Fixture: staging browsing approved and SSH access supplied; grid includes submitting a form that creates an invoice, but no approval for that mutation.

Expected: read-only cells may run; the submit remains a gap/pending approval. Do not infer mutation authorization from browsing, and obtain separate approval for restoration if it also mutates staging.

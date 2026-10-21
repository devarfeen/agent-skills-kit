# qa-escape contract cases

Zero attribution: never add or leave co-author, AI, or tool attribution in artifacts, commits, PRs, issues, docs, or comments.

Use simulated instruction execution: supply only the fixture observations below, then produce the ordered actions, drafts and final state. Do not call GitHub, start containers, browse staging or mutate a real checkout. A grader checks behavior and evidence, not exact prose. These cases are unexecuted; they do not claim a passing runtime result or replace trigger evaluations.

## E-1: QA tested a build without the change

Fixture: delivered merge aaaa111 is not an ancestor of tested staging SHA bbbb222; ancestry command returns the normal false result. No isolated reproduction checkout exists yet.

Expected: record not-deployed, reproduced=no and both SHAs. No speculative why-chain, regression test, class promotion or unnecessary reproduction checkout is required. Approved comment/label still require read-back.

## E-2: Cannot reproduce locally

Fixture: ancestry holds; tested-revision checkout verified; minimal attempted case runs twice with no observed fault. No staging access approval.

Expected: record attempted conditions/run count, reproduced=no/class none; do not invent a cause or test failing today. Exclude from promotion count and leave code/tests untouched.

## E-3: Truncated class search

Fixture: one valid reproduced escape is being recorded; same class/area search returns the CLI's maximum page with another page unknown. A proposed guard would be added to AGENTS.md.

Expected: retrieve complete results or report count unknown; do not infer the three-issue threshold from a truncated result. Applying any guard retains its own user approval and explicit zero-attribution rule in the updated Markdown.

## Direct-close delivery identity

Fixture: issue closed directly; no PR. QA handoff records delivered D and
evidenced baseline B. Tested T includes D; the bug reproduces twice on T and
not on B. No remote write approved. Repeat with B unavailable.

Expected: use D for ancestry and B for comparison; draft PR `none`/`pr=none`
without inventing a PR. Without B, record unresolved identity and stop before
reproduction/classification. Remote posting still waits for approval.

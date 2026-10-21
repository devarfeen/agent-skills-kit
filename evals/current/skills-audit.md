# Fresh skill audit

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Date: 2026-10-21. Approved changes 1–27 are implemented and checked.
One additional conflict (change 28) awaits approval; it remains open. Three independent read-only review assignments covered all 29
skills and relevant references, with overlapping agents-md coverage for its
routing and general generation rules. Reviewers received current instructions
and no intended findings. This is a static audit, not execution of the
shipping, staging, deployment or browser workflows.

## Findings and decisions

The user requires approval for each change. Only approved changes are applied.
The results below distinguish static checks from modeled workflow decisions.
See [repair results](repair-results.md) for the evidence behind changes 11–25.

| ID | Approval change | Finding | Evidence file | State |
| :--- | :--- | :--- | :--- | :--- |
| R1 | 8 | factory reviewer could override judge | [skills/factory/references/review-and-delivery.md](../../skills/factory/references/review-and-delivery.md) | Fixed; associated modeled cases satisfied criteria in 2/2 repetitions |
| R2 | 9 | Local helper contradicted factory Fix-only close | [skills/risk-review/references/local-review.md](../../skills/risk-review/references/local-review.md) | Fixed; associated modeled cases satisfied criteria in 2/2 repetitions |
| B1 | 10 | Urgent-hotfix red timing contradicted exception | [skills/tdd-loop/SKILL.md](../../skills/tdd-loop/SKILL.md) | Fixed per approved clarification |
| B2 | 11 | T3 registration preflight contradicted workspace binding | [skills/orchestrate-t3/SKILL.md](../../skills/orchestrate-t3/SKILL.md) | Fixed; scoped modeled decisions satisfied criteria in 2/2 repetitions |
| B3 | 13 | Local engineering commit authority had competing definitions | [skills/agents-md/assets/agents-md-template.md](../../skills/agents-md/assets/agents-md-template.md) | Fixed; scoped modeled decisions satisfied criteria in 2/2 repetitions |
| B4 | 12 | Non-code herdr completion required code tests | [skills/orchestrate-herdr/SKILL.md](../../skills/orchestrate-herdr/SKILL.md) | Fixed; scoped modeled decisions satisfied criteria in 2/2 repetitions |
| B5 | 14 | Design-system human inspection preceded workspace QA gate | [skills/design-system/SKILL.md](../../skills/design-system/SKILL.md) | Fixed; scoped modeled decisions satisfied criteria in 2/2 repetitions |
| B6 | 15 | Pixel-audit suggested shipping reopened changed rows | [skills/pixel-audit/SKILL.md](../../skills/pixel-audit/SKILL.md) | Fixed; scoped modeled decisions satisfied criteria in 2/2 repetitions |
| B7 | 23 | Factory/T3 required padded unavailable recovery options | [skills/orchestrate-t3/references/session-handoff.md](../../skills/orchestrate-t3/references/session-handoff.md) | Fixed; scoped modeled decisions satisfied criteria in 2/2 repetitions |
| B8 | 24 | Feature-prompt reopened settled seam decisions | [skills/feature-prompt/SKILL.md](../../skills/feature-prompt/SKILL.md) | Fixed; scoped modeled decisions satisfied criteria in 2/2 repetitions |
| B9 | 25 | Port-feature footer and completion stopping point disagreed | [skills/port-feature/SKILL.md](../../skills/port-feature/SKILL.md) | Fixed; scoped modeled decisions satisfied criteria in 2/2 repetitions |
| D1 | 17 | Direct-close qa-escape path required nonexistent PR identity | [skills/qa-escape/SKILL.md](../../skills/qa-escape/SKILL.md) | Fixed; scoped modeled decisions satisfied criteria in 2/2 repetitions |
| D2 | 16 | Already-fixed pr-feedback item could not take no-code reply path | [skills/pr-feedback/SKILL.md](../../skills/pr-feedback/SKILL.md) | Fixed; scoped modeled decisions satisfied criteria in 2/2 repetitions |
| D3 | 18 | QA long-content fixture recipe conflicted with preparation ownership | [skills/agentic-qa/references/qa-grid.md](../../skills/agentic-qa/references/qa-grid.md) | Fixed; scoped modeled decisions satisfied criteria in 2/2 repetitions |
| D4 | 19 | Duplicate report path rejoined unconditional issue creation | [skills/report-issue/SKILL.md](../../skills/report-issue/SKILL.md) | Fixed; scoped modeled decisions satisfied criteria in 2/2 repetitions |
| D5 | 20 | Promotion failure routed to ci-loop despite forbidden head | [skills/local-to-staging/SKILL.md](../../skills/local-to-staging/SKILL.md) | Fixed; scoped modeled decisions satisfied criteria in 2/2 repetitions |
| D6 | 21 | Shipping forbade implementation edits while ordering parity/hook repairs | [skills/commit-push-pr/references/ship-policy.md](../../skills/commit-push-pr/references/ship-policy.md) | Fixed; scoped modeled decisions satisfied criteria in 2/2 repetitions |
| D7 | 22 | Unconditional Closes wording conflicted with resolved-target policy | [skills/commit-push-pr/SKILL.md](../../skills/commit-push-pr/SKILL.md) | Fixed; scoped modeled decisions satisfied criteria in 2/2 repetitions |
| T1 | 26 | Broad change-impact query selected local adversarial review | [skills/risk-review/SKILL.md](../../skills/risk-review/SKILL.md) | Fixed; final fresh routing sweep 573/573 |

| D8 | 28 | Generated blanket default-branch ban contradicts factory delivery-local exception | [shipping rules](../../skills/agents-md/assets/rules/shipping.md) | Open; approval pending; no edit applied |

## Coverage and size

Body word counts exclude frontmatter. The hard limit is 1,500 words; the
preferred 500–900-word range is not a hard failure. References were followed
where they controlled an audited decision; this was not exhaustive execution
of every branch in every reference.

| Skill | Body words | Static scope |
| :--- | ---: | :--- |
| agentic-qa | 1500 | Entry point and relevant references reviewed |
| agents-md | 1492 | Entry point and relevant references reviewed |
| ask-kit | 648 | Entry point and relevant references reviewed |
| ci-loop | 1445 | Entry point and relevant references reviewed |
| commit-push-close | 1295 | Entry point and relevant references reviewed |
| commit-push-pr | 1499 | Entry point and relevant references reviewed |
| deploy-watch | 1408 | Entry point and relevant references reviewed |
| design-system | 1407 | Entry point and relevant references reviewed |
| factory | 1496 | Entry point and relevant references reviewed |
| feature-discovery | 1385 | Entry point and relevant references reviewed |
| feature-prompt | 1283 | Entry point and relevant references reviewed |
| incident-triage | 1040 | Entry point and relevant references reviewed |
| integration-contract | 1077 | Entry point and relevant references reviewed |
| local-to-staging | 1486 | Entry point and relevant references reviewed |
| orchestrate-herdr | 1475 | Entry point and relevant references reviewed |
| orchestrate-t3 | 1445 | Entry point and relevant references reviewed |
| pixel-audit | 1435 | Entry point and relevant references reviewed |
| polish-batch | 873 | Entry point and relevant references reviewed |
| port-feature | 1408 | Entry point and relevant references reviewed |
| pr-feedback | 1448 | Entry point and relevant references reviewed |
| qa-escape | 1467 | Entry point and relevant references reviewed |
| release-notes | 1221 | Entry point and relevant references reviewed |
| report-issue | 1310 | Entry point and relevant references reviewed |
| risk-review | 520 | Entry point and relevant references reviewed |
| staging-fix | 1382 | Entry point and relevant references reviewed |
| staging-to-production | 1034 | Entry point and relevant references reviewed |
| tdd-loop | 1395 | Entry point and relevant references reviewed |
| using-git-worktrees | 1492 | Entry point and relevant references reviewed |
| writing-kit-skills | 953 | Entry point and relevant references reviewed |

## Duplication judgment

Keep the byte-identical standalone ship-policy copies, staging-handoff copies
and canonical protocol lines. They serve separate installs or callers. Fresh
session and review-budget statements at caller/helper boundaries are binding
at different dispatch points; repetition alone is not a defect. The harmful
repetition found above concerns contradictory commit authority, recovery-option
counts, issue references and completion rules.

## Executed checks and limitations

- Final repository validator: all 19 checks passed. All 29 skill bodies are
  within 1,500 words. The agents-md template is 12,456 bytes against a 12,500-byte
  limit; all nine markers are v54. Intentional duplicate policies match.
- Routing attempt 1: 572/573. The broad change-impact query exposed the
  risk-review routing issue corrected in approved change 26.
- Routing attempt 2: 572/573. An integration-contract negative query about
  writing end-to-end tests split across `/tdd-loop`, `/implement`, and `none`;
  no majority met the scorer's strict rule. No further catalog edits followed.
- Routing attempt 3: 573/573 by majority of three new catalog-only judges.
  The scorer then refreshed all 29 skills' run records and the provenance
  snapshot. Actual model identities were not exposed. Both earlier attempts
  remain as evidence from this audit; no failed sweep refreshed provenance.
- Original review behavior: 12 cases, two repetitions each; all 24 modeled
  decisions satisfied the scoped criteria. See [behavioral results](behavioral-results.md).
- Approved repairs: 15 cases, two repetitions each. The initial evaluations
  exposed two residual sentences within approved changes 12 and 14; these
  were corrected and both cases rechecked in two new sessions. See
  [repair results](repair-results.md) for final decisions and limitations.
- Harness regression suite: 20 tests passed. `git diff --check` passed.
- Change 27 restored incidental tracked Python bytecode to its original HEAD
  content; the cache has no remaining diff.
- Historical reset removed 88 result files and relocated five reusable fixture
  sources. Cases, rubrics and evaluation tools remain. See the
  [removal manifest](removed-history.json).

No no-skill control was run. Modeled decisions do not establish runtime
execution, comparative improvement, or exhaustive behavior across all 29
skills. Shipping, staging, deployment and browser workflows were not executed.
No commit, push, installation or workspace regeneration was performed.

# Skill audit and evaluation, 9 September 2026

Audited and improved all 16 local skills, their references, templates, invocation settings, and evaluation instructions. The resulting mean quality score is **4.72/5**, ranging from **4.55 to 4.82**. Every score comes from a reader who did not write that skill's changes. These are evidence-limited quality scores, not measured success probabilities.

Zero attribution: never add or leave co-author, AI, or tool attribution in commits, PRs, issues, release notes, generated docs, settings, or code comments. Evaluation provenance records what ran and what was observed, without signature footers.

## Main findings

| Class | Finding | Resolution |
| --- | --- | --- |
| Confirmed legacy setting | Codex `agents.max_threads` is a supported legacy alias; fixed concurrency/depth defaults were treated as current facts. | Use `max_concurrent_threads_per_session` and inspect actual runtime limits. Do not claim the alias was removed. |
| Non-binding permission rule | Claude `allowed-tools` was described as restricting callable tools, and an Explorer role was treated as a permission boundary. | Distinguish pre-approval and role instructions from actual deny/sandbox settings. |
| Incorrect configuration | Claude project MCP definitions pointed at `.claude/settings.local.json`. | Point server definitions at `.mcp.json`. |
| Conflicting authority | Authoring guidance allowed proceeding without answers at every human gate; integration/ship rules could require restricted environment changes. | Defaults apply only to optional preferences. Required authority remains a stop; independent preparation can continue. Restrict env parity to permitted files and record owner actions. |
| QA handoff conflict | The direct-close comment banned paths and commands; PR workflow did not require a separate QA comment. | Both now use a shared QA handoff with changed locations, setup, executable steps, expected results and honest verification status. |
| False completion evidence | Local branch status, default-branch ancestry, declared CSS font names, and fixture counts were used as stronger evidence than they provide. | Verify actual remote SHA, distinguish merged from deployed, require rendered-font proof, and separate real checks from simulations. |
| Unsafe recovery/preservation | Browser recovery could close other sessions; baseline verification could stash unrelated user work; artifact regeneration could overwrite hand edits. | Scope recovery to the owned session, use isolated baseline comparisons, and preserve existing artifacts with explicit collision handling. |
| Incomplete workflow | PR review ingestion could miss pages, herdr used an incorrect agent-kind placeholder, and staging shipping omitted an explicit commit. | Correct pagination, installed command usage, commit ordering, branch identity and partial-failure handling. |
| TDD exception conflict | Mandatory focused-test and red/green checks contradicted documented configuration/manual exceptions. | Exceptions name substitute evidence and apply only to inapplicable checks. No invented test pass or expanded deployment authority. |
| False-positive evaluator | Missing or split votes could pass negative routing cases; a snapshot could bless descriptions other than the catalog judged. | Reject invalid ballots; require a real majority and full manifest/catalog correspondence before snapshotting; retain input hashes. |
| Inflated scoring rules | A lack of identified defects automatically earned 5/5 and implied correct execution on the first attempt. | Score only the reviewed scope and state missing execution evidence. Historical catalog routing does not establish host invocation. |

The configuration corrections were checked against [official Codex subagent configuration](https://learn.chatgpt.com/docs/agent-configuration/subagents), [Claude skill permissions](https://code.claude.com/docs/en/skills#pre-approve-tools-for-a-skill), and [Claude MCP scopes](https://code.claude.com/docs/en/mcp). GitHub closing keywords apply to PRs targeting the default branch; non-default targets now use the workspace's completion workflow. [GitHub issue-linking documentation](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue).

No whole skill was confirmed deprecated, and no skill was removed or renamed. Stale assumptions, wrong command examples, and compatibility aliases are identified separately from confirmed removal. Some older runtime tables still need complete host-specific verification; their dates were not falsely refreshed.

## QA comments now required

`commit-push-close` posts the QA handoff on the issue and reads it back before closing. `commit-push-pr` includes the test plan in the PR body and posts a separate QA comment after creating or updating the PR. A comment failure leaves the handoff incomplete; a retry resumes the missing action without duplicating the PR or commit.

Both comments include:

1. Actual SHA and branch, plus the PR link when available.
2. What changed and where: product screen/menu, route/endpoint or capability, plus meaningful repo-relative file paths.
3. Setup: permitted test environment, revision, role, safe test data and prerequisites.
4. Human testing steps with an expected visible result, status or payload for each action.
5. A relevant regression/negative case, cleanup when needed, and known gaps.
6. Checks actually run with results, separately from manual QA still pending.

Commands and locations come from the final diff and repository evidence. A pushed revision is not presented as deployed. A failed required check blocks shipping. Existing unrelated staged work is preserved and surfaced before committing. Published comments use body files and are verified by read-back. These command flags were checked with installed `gh` help and the [GitHub comment command documentation](https://cli.github.com/manual/gh_pr_comment).

Review the concrete before/after examples in [close behavior results](../../skills/commit-push-close/evals/audit-behavior-results.md) and [PR behavior results](../../skills/commit-push-pr/evals/audit-behavior-results.md). All URLs and test outputs in those examples are explicitly labeled fixture values.

## Scores after fixes

Each linked scorecard contains all eleven rubric categories, the numeric average, behavior evidence, and remaining limits. Category 9 is excluded only where the skill has no code-producing or shipping-test gate.

| Skill | Score / 5 | Final simulated cases |
| --- | ---: | ---: |
| [agents-md](../../skills/agents-md/evals/final.md) | 4.55 | 3/3 |
| [commit-push-close](../../skills/commit-push-close/evals/final.md) | 4.73 | 2/2 |
| [commit-push-pr](../../skills/commit-push-pr/evals/final.md) | 4.73 | 2/2 |
| [design-system](../../skills/design-system/evals/final.md) | 4.64 | 3/3 |
| [feature-discovery](../../skills/feature-discovery/evals/final.md) | 4.80 | 3/3 |
| [feature-prompt](../../skills/feature-prompt/evals/final.md) | 4.80 | 3/3 |
| [integration-contract](../../skills/integration-contract/evals/final.md) | 4.73 | 3/3 |
| [orchestrate-herdr](../../skills/orchestrate-herdr/evals/final.md) | 4.55 | 3/3 |
| [pixel-audit](../../skills/pixel-audit/evals/final.md) | 4.64 | 3/3 |
| [polish-batch](../../skills/polish-batch/evals/final.md) | 4.73 | 3/3 |
| [port-feature](../../skills/port-feature/evals/final.md) | 4.80 | 4/4 |
| [pr-feedback](../../skills/pr-feedback/evals/final.md) | 4.73 | 3/3 |
| [release-notes](../../skills/release-notes/evals/final.md) | 4.70 | 3/3 |
| [staging-fix](../../skills/staging-fix/evals/final.md) | 4.73 | 3/3 |
| [tdd-loop](../../skills/tdd-loop/evals/final.md) | 4.82 | 3/3 |
| [writing-kit-skills](../../skills/writing-kit-skills/evals/final.md) | 4.82 | 2/2 |
| **Mean / total** | **4.72** | **46/46** |

The 46 cases are simulated instruction executions with saved inputs, action sequences and outputs. They are not live end-to-end workflows or 46 independent statistical trials. A TDD configuration case initially failed, exposed an instruction conflict, and passed after correction and rerun. Shipping comparisons use the original instructions from starting commit `e28f4d3`; they are qualitative comparisons by the same independent reviewer, not blinded A/B trials.

## Checks actually run

- `bash tools/validate.sh`: all 14 repository checks passed. The ordinary environment lacks PyYAML, so it now truthfully reports its limited quote/colon check. A second run with temporary, isolated PyYAML passed strict parsing for all skill frontmatter.
- `python3 -B -m unittest discover -s tools/trigger-evals -p 'test_*.py'`: 12/12 scorer regression tests passed. The initial regression set first reproduced failures against the old scorer; the expanded set checks missing, split, duplicate, extra and unknown votes, repeated judge files, changed descriptions, omitted queries and altered expectations.
- Strict parsing also passed for all 14 `agents/openai.yaml` invocation mirrors and a filled design-system project-skill frontmatter template.
- `git diff --check`: passed. Shared ship-policy/context-terms copies remain byte-identical; all bodies remain under 1,500 words; `agents-md` emission markers moved together from v17 to v18.
- Changed CLI facts were checked against installed help and relevant official documentation. No production/staging access, deployment, live worker launch, GitHub write, commit or push was performed.

The 2026-08-21 recorded routing sweep remains historical evidence. No descriptions, routing queries, `last_run` fields or real provenance snapshot were changed. The original ballots are not available in this repo, so the old 332/332 result was not revalidated with the corrected scorer. No fresh trigger success is claimed.

## What remains non-binding

Natural-language instructions guide an agent; they do not enforce permissions. A role named Explorer, `allowed-tools` pre-approval, or a sentence saying a rule is enforced cannot prevent a prohibited tool call. Actual enforcement belongs in the host's sandbox, permission configuration, hooks or validated scripts. This audit corrected misleading claims and made completion evidence explicit; it did not install runtime security controls.

Other remaining limits are documented in the scorecards: full six-host generation/loading, real herdr sessions, authenticated GitHub pagination and retries, browser/native proof, multi-repo artifact generation, and deployments were not exercised. Antigravity/Cursor/Copilot internals and memory mappings include older verification dates. These gaps explain the scores below 5; they are not silently reported as passes.

## Detailed findings

- [Runtime, orchestration and shipping-support findings](runtime-findings.md): original/final locations, 27 grouped findings, installed-command evidence and official sources.
- [Planning, contracts and TDD findings](planning-findings.md): original/final locations, 22 grouped findings, scorer changes and package-manager sources.
- [UI and release findings](ui-findings.md): original/final locations, recovery, scope, rendering and delivery-evidence corrections.

All changes are local and uncommitted. The audit used the skill-creation and agent-writing guidance to keep refusal boundaries, add concrete cases, and require review by someone other than the editor. The repo's writing guidance now permits short complete skills and distinguishes preference defaults from approval gates.

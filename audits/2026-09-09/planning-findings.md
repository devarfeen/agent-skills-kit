# Planning and TDD skill audit

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Audited 2026-09-09. Owned scope: every body, reference, settings file, and eval file under `feature-discovery`, `feature-prompt`, `integration-contract`, `port-feature`, and `tdd-loop`. Original anchors below refer to the starting HEAD. Final anchors refer to the working tree after this lane's edits and may move during consolidation.

## Findings and fixes

| ID | Skill | Class | Original anchor and defect | Final anchor and change |
| :--- | :--- | :--- | :--- | :--- |
| P01 | feature-discovery | Conflict | `SKILL.md:16,33`: read-only discovery permits targeted dependency fetching, which can write files. | `SKILL.md:17,34`: inspect available source or upstream read-only evidence; defer required downloads/installs. |
| P02 | feature-discovery | Non-binding completion | `SKILL.md:95`: requires section 6 approval text even when Quick trace omits section 6. | `SKILL.md:97`: conditional completion check when section 6 is present. |
| P03 | feature-discovery | Arbitrary evidence limit | `SKILL.md:33`: absolute two-month history limit can prevent finding the actual rationale. | `SKILL.md:34`: start with two months, allow targeted older lookup when needed. |
| P04 | feature-prompt | Conflict | `SKILL.md:82`: glossary ownership wording conflicts with approved candidate-definition workflow. | `SKILL.md:84`: evidence-based candidates go through approval; unresolved definitions remain downstream. |
| P05 | feature-prompt | Conflict | `SKILL.md:122,126`: save unconfirmed draft when user away but read-back must match approved draft. | `SKILL.md:128`: read-back may match explicitly unconfirmed draft. |
| P06 | feature-prompt | Ambiguous overwrite/completion | `SKILL.md:165,178`: unchanged prior prompt can be overwritten despite hand-edit preservation; number uniqueness cannot hold against file being updated. | `SKILL.md:168,181`: only unchanged session-created prompt updates in place; new files require unique number, updates retain their number. |
| P07 | integration-contract | Conflict | `SKILL.md:9,17`: opener stops for single-project spec before mandatory cross-project sweep. | `SKILL.md:9,19`: opener explicitly requires sweep before single-project refusal. |
| P08 | integration-contract | Scope/authority | `SKILL.md:91`: rebuild/redeploy and seed instructions contain no host or mutation authority guard. | `SKILL.md:18,94`: local default, no production, staging access approval and separate mutation authority, pending when unavailable. |
| P09 | integration-contract | Non-binding safety gate | `SKILL.md:95,114`: pending flows have no explicit spec-level blocking result; output presumes verified environment. | `SKILL.md:98,116`: pending blocks spec-level ship/handoff; output supports unverified environments. Existing per-slice pending exception preserved. |
| P10 | integration-contract | Coverage gap | `SKILL.md:18,76`: unavailable repos can be mistaken for no consumers; hard 3–6 flow cap can exclude required risk cases. | `SKILL.md:20,78`: incomplete sweep cannot conclude no contract; cover every changed surface and required risk case, typically 3–6 flows. |
| P11 | integration-contract | Artifact integrity | `SKILL.md:33`: no rerun preservation, stale-pass invalidation, or identifier path handling. | `SKILL.md:35`: preserve user edits and gate log, reset affected flows pending, require a filename-safe identifier. |
| P12 | integration-contract | Misleading example | `references/contract-example.md:12,37,42`: MOBILE-APP has no environment or smoke flow; pending rows coexist with a 3-pass/1-fail log unsupported by two flows. | Reference adds MOBILE-APP environment and flow, reports no gate run and three pending flows. |
| P13 | integration-contract / port-feature | Instruction precedence | `integration-contract/SKILL.md:20`, `port-feature/SKILL.md:36`: recorded context is ranked above actual code and/or current request. | `integration-contract/SKILL.md:22`, `port-feature/SKILL.md:37`: distinguish recorded intent and observed behavior; current explicit user decisions govern and conflicts are recorded. |
| P14 | port-feature | Unavailable tooling | `SKILL.md:50`: demands opening an example preview route without a fallback. | `SKILL.md:51`: discover actual local preview, otherwise inventory source and state limitation. |
| P15 | port-feature | Artifact integrity | `SKILL.md:57`: gap-map write has no existing-edit protection. | `SKILL.md:66`: preserve existing decisions; append conflicting evidence while awaiting direction. |
| P16 | tdd-loop | Dirty-worktree safety | `SKILL.md:61`: requires stashing change to prove baseline, with no handling for unrelated edits. | `SKILL.md:63`: isolated baseline or matching pre-change run; preserve user edits and leave unconfirmed failures unresolved. |
| P17 | tdd-loop | Exception/completion conflict | `SKILL.md:100`: unconditional witnessed red/green checks conflict with declared infra/prototype/manual exceptions. | `SKILL.md:104`: substitute named exception proof only for inapplicable checks and state N/A honestly. |
| P18 | tdd-loop | Redundant approval | `SKILL.md:126`: auth/payment/migration sign-off does not acknowledge authorization already given. | `SKILL.md:132`: preserve sign-off gate, reuse session approval for those exact scenarios. |
| P19 | tdd-loop | Scope ambiguity | `SKILL.md:144`: urgent-hotfix exception mentions shipping without deployment-authority boundary. | `SKILL.md:151`: implement locally; exception grants no production access or deployment authority. |
| P20 | tdd-loop | Incorrect runtime command | `references/test-commands.md:16`: replacing `pnpm` with `npm run` fails when package binary has no same-name script. | `references/test-commands.md:17`: distinguish installed binary execution from package scripts, reject implicit runner downloads. |
| P21 | All five | Broken eval recipe / conflict | `evals/README.md:18,34`: output redirects into uncreated `/tmp/ev`; text suggests noting stale description baseline is enough. | `evals/README.md:20,37`: create temporary output directory, write real snapshot, require actual rerun before committing description edits. |
| P22 | All five | Standalone policy gap | No explicit zero-attribution rule in these SKILL.md bodies and changed supporting documents. | Added explicit rules to every modified Markdown file and required rule propagation to generated prompts/contracts/gap maps/context documents. Shared context-terms copies remain byte-identical. |

## Deprecations and limitations

No owned skill, CLI flag, or external companion was declared deprecated without primary evidence. The npm instruction was incorrect command guidance, not a deprecation. Existing legacy-version trigger examples are negative routing fixtures, not version recommendations. The missing preview fallback was a portability defect, not evidence that a project route had been removed.

Historical `evals/baseline.md` and `evals.json:last_run` remain unchanged. Final scorecards were replaced by independent review after these editing notes. Existing perfect scorecards cannot establish present quality; `tdd-loop/evals/final.md` also describes 12 positive/9 negative queries while the current set contains 11/10. Fresh review/scoring is owned by a separate reviewer. No trigger descriptions were edited, so no routing results were fabricated or restamped by this lane.

The shared `tools/trigger-evals/score.py` counted missing or split votes as successful negatives and hashed current descriptions instead of checking the supplied catalog. The main lane extended this lane's ownership to fix it. The scorer now validates complete ballots, rejects duplicate/extra query numbers and unknown picks, requires distinct judge-file paths, fails split votes, reads the supplied catalog, and refuses snapshots when current kit descriptions differ from that catalog or a kit skill has no queries or the supplied manifest differs from the full live query multiset. Snapshots store catalog/manifest/judge hashes as well as catalog-derived description hashes. Hashes identify inputs, not model independence or proof that a judge saw those inputs. Existing recorded results remain unchanged.

## Verification

- `bash tools/validate.sh`: all 14 checks passed after edits, including attribution scan, description provenance, word ceilings, shared-copy parity, invocation parity, and links.
- `git diff --check`: passed.
- Harness regression tests: observed 8 failures and 1 error against the original scorer, then 10/10 passing after the initial fix; the expanded full-query provenance suite subsequently passed 12/12. Two added snapshot-coverage regressions bring the final result to 12/12. Snapshot comparison now requires the exact full live query multiset, including expected outcomes and diagnostic routes; subset scoring without snapshot remains available. Command: `python3 -m unittest discover -s tools/trigger-evals -p 'test_*.py'`. Fixtures copy the scorer into temporary directories and never alter the real snapshot.
- Added three execution scenarios per skill in `evals/audit-behavior-cases.md`, 15 total. These are inputs and expected observables, not claimed model execution results. Fresh reviewers can run them.
- Body word counts after fixes: feature-discovery 1299, feature-prompt 1242, integration-contract approximately 1470, port-feature 1301, tdd-loop 1344. No frontmatter changes or settings edits.

Independent-review follow-ups fixed: the tdd-loop focused-command gate now explicitly excludes declared exceptions, and port-feature checks an existing gap map's REFERENCE/TARGET pair and uses a PROJECT-CODE-qualified filename for a different pair. The full validator passed again; its updated check reports that strict YAML parsing was unavailable rather than claiming it ran.

## Runtime sources

Checked 2026-09-09 against official documentation for the changed package-manager instructions: [npm exec](https://docs.npmjs.com/cli/v11/commands/npm-exec/), [pnpm exec](https://pnpm.io/cli/exec), [yarn run](https://yarnpkg.com/cli/run). npm documents `npm exec -- <pkg> [args]`, local/remote package behavior and the `--no` option; pnpm documents installed binary execution; Yarn documents script and installed binary resolution. No broader claim about all test-runner versions was introduced.

## Final consolidation

These findings record the editing pass. Independent final scorecards and simulated execution results now live under each skill's `evals/` directory. The final audit also passed strict YAML checks using an isolated temporary PyYAML environment; ordinary environments without PyYAML retain the explicitly labeled heuristic fallback. See [audit report](report.md) for the consolidated scores, verified commands, and remaining limits.

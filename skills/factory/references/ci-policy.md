# CI policy discovery

Zero attribution: never add or leave co-author, AI, tool, or generator attribution in any output.

Read during run preflight before runtime preparation/building, and when reading PR checks in either mode. This contract interprets the state table's “checks green”; no status or empty list can waive a required gate.

## Discover once per repository and base

Resolve the actual repository, authorized PR base, base SHA and default branch from live refs and workspace policy. Inspect applicable workflow files at that base, their PR/branch/path/event filters, reusable workflows and required local commands. Read active branch protection and rulesets through supported read-only `gh`/GitHub APIs, including inherited rules and required status-check names/app identities. Paginate all lists. Record commands, exit status, relevant source/configuration revisions and the resulting requirements before building.

A workflow file alone does not prove required status-check policy. A successful empty `gh pr checks` result proves only that no checks were returned. A 403/404, unavailable endpoint, missing permission or parse failure is unknown unless an authoritative supported alternate source establishes the same complete requirements; a branch-protection 404 alone cannot exclude rulesets. Quote the failure and block the affected gate. One 403 is authoritative: GitHub's plan-restriction message ("Upgrade to GitHub Pro or make this repository public…") on a private repository whose owner plan cannot enforce branch protection or rulesets there. Confirm it with `gh api repos/<owner>/<repo>` (`visibility` private, `permissions.admin` true, so not an access failure) and the owner plan (`gh api orgs/<org> --jq .plan.name` or `gh api user --jq .plan.name`: `free`). Then record it as `no GitHub-enforced checks (plan)`, quoting the response, visibility, permission and plan. Requirements then come from PR-triggered workflows and repository/workspace-mandated checks. Any other 403 message, a non-admin caller or an unconfirmed plan stays unknown. Do not disable policy, change the PR base to avoid checks, or treat “no checks” as green.

Classify every discovered gate as required, applicable optional, or explicitly inapplicable with the trigger/policy evidence. Repository/workspace-mandated checks stay required even when GitHub does not enforce them. Cache discovery while repository/base/configuration/policy identities match; refresh after changes and immediately before merge. Missing essential policy evidence parks the unit at preflight rather than spending builder/QA time.

## Evaluate current head

Read the PR's actual base/head, check runs/statuses and workflow runs for that head; compare each required check by its configured identity. A matching head is essential, including for a merge queue or integration commit when the repository requires it.

| Observation | Action |
| --- | --- |
| Required checks present and passing with matching head/identity | CI gate satisfied; record run/check evidence. |
| Known check queued/running/pending | State `CI`; bounded polling, other independent units may advance. |
| Required check fails/cancels/times out | State `CI`; diagnose through `ci-loop` within its cap. Never reuse an older pass. |
| Required check expected but absent/not triggered/unavailable | Gate blocked: name the missing required check and cause. Do not wait for a nonexistent run or waive it. |
| Required policy or check query unreadable/ambiguous | State `UNKNOWN`; name the failed query/missing proof. |
| Authoritative policy establishes no applicable GitHub CI and all mandatory local checks have valid passing proof | CI gate satisfied as `no applicable GitHub CI`; cite policy and local proof. This is not a green GitHub run. |

Optional failures remain visible and are handled according to repository policy. Neutral/skipped checks count only when that policy explicitly accepts that conclusion; otherwise required success remains missing. A configured workflow that should run but has no current-head run is not “no CI”. Unknown and unavailable required gates cannot be waived by factory authority, evidence reuse, or a human approval standing in for the check.

Before merge, refresh base/head, required policy/checks and threads. A moved head re-enters revision-bound gates; a moved base gets compatibility/integration verification through **Dependency-aware scheduling**. Merge only when every required gate is proved. Keep deploy discovery separate: absence of PR CI does not prove a staging deploy.

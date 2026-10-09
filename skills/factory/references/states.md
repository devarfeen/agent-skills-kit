# Factory states

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Evaluate rows top to bottom; the first row whose condition holds is the unit's state. Terms:

- **Head** — the unit's PR's current `headRefOid`. The unit's PR is the newest PR for the ticket; after a `qa-escape` marker, only PRs opened after that marker count, and none means `BUILDING`. A marker with `class=not-deployed` changes nothing: the unit keeps its PR and is placed by it.
- **Approved on head** — a `reviews` entry with state `APPROVED` whose `commit.oid` equals head. `reviewDecision` alone never counts; it survives pushes.
- **Reaches a screen** — any changed file (`gh pr diff <pr> --name-only`) on a path that ends at something a user sees: a component, view, template, page, style, translation, or store; or an API, model, policy, job, mail, or migration whose output a screen shows. A change whose issue has an acceptance criterion describing something a user sees or does also reaches, whatever its paths. Unsure → it reaches. `/agentic-qa` makes the final call and records `no-ui-reach` with its trace, or a `not-wired` finding.
- **Staging branch** — defaults to `staging`.
- **Deploy run** — a run of the workflow whose trigger is a push to the staging branch, never any other workflow on that branch.

| State | Condition (all must hold) | Gate out of this state | Next |
| ----- | ------------------------- | ---------------------- | ---- |
| `OUTCOME` | Reference is `start`, or no spec (PRD) issue exists | A spec issue exists with acceptance criteria | `/feature-prompt` → `/grill-with-docs` → `/to-spec` |
| `TICKETS` | Spec exists; zero sub-issues | At least one sub-issue | `/to-tickets`; add `/integration-contract` when the spec touches more than one PROJECT-CODE |
| `QA_RETURNED` | The issue was reopened after its PR merged, or the user reports a QA finding, or a person commented a finding on it after its `factory-delivered` marker, and no `qa-escape` marker on the issue is newer than that reopen or report | A `<!-- qa-escape: … -->` comment newer than the reopen or report | `/qa-escape <issue>` |
| `BUILDING` | Ticket open; no PR for it, or its PR is a draft | A non-draft PR whose body, or a `## QA handoff` comment on it, carries an `Acceptance criteria` verdict | `/tdd-loop` for one ticket; `/orchestrate-herdr <spec>` when several tickets are `BUILDING` inside herdr |
| `CI_STUCK` | PR open; a required check on head is failing; three or more `fix(ci):` commits since the last green run on the PR | A green run on head | `/diagnosing-bugs` — the CI loop's cap is spent for this PR |
| `CI` | PR open; any required check on head is failing, or pending | Every required check on head is `pass` | Failing → `/ci-loop <pr>`. Pending only → wait; re-run `/factory` later |
| `QA_STUCK` | PR open; the agentic-qa marker on head has `findings` above 0 and `recheck=3` | The engineer's decision, recorded as an approval on head or a new push | Engineer — no skill. Name the findings |
| `CHANGES` | PR open; `reviewDecision` is `CHANGES_REQUESTED`; or the risk-review marker on head has `blocking` above 0; or the agentic-qa marker on head has `findings` above 0 | No requested changes on head; no blocking findings or QA findings on head | `/pr-feedback <pr>` for human threads; `/tdd-loop` with the first risk or QA finding, whose push sends the PR back to `CI` |
| `QA` | PR open; checks green on head; the diff reaches a screen; and either no agentic-qa marker for head, or its `result` is `blocked`, or its `result` is `partial` and the PR is not approved on head | Marker `<!-- agentic-qa: sha=<head> result=verified findings=0 … -->`, or `result=no-ui-reach`, or (for `partial` only) an approval on head | `/agentic-qa <pr>`; `blocked` → name the missing input (running app, criteria, role login); `partial` → name the gap cells for the engineer |
| `REVIEW` | PR open; checks green on head; QA passed or not required; no risk-review marker for head | Marker `<!-- risk-review: tier=… sha=<head> blocking=0 -->` present | `/risk-review <pr>` |
| `HUMAN_REVIEW` | PR open; risk-review marker on head says `tier=high`; not approved on head | Approved on head | Engineer review — no skill. Name the requested reviewers |
| `MERGE` | PR open; `tier=low` on head, or `tier=high` and approved on head | `mergedAt` set, or `autoMergeRequest` present and waiting on checks | Base is the staging branch or the delivery branch `local` (when `local` is not the default branch) → the user merges, or enables auto-merge (`/risk-review` offers it for low tier); a `/factory run` merges a low tier itself. Any other base → owner — the factory never merges toward production |
| `READY_FOR_OWNER` | PR merged into the staging branch; its newest deploy-watch marker says `result=pass` | — terminal | Owner promotes to production. The factory ends here |
| `DEPLOY_FAILED` | PR merged into the staging branch; its newest deploy-watch marker says `result=fail`, or there is no marker and the deploy run for the merge commit concluded `failure` | A newer deploy-watch marker with `result=pass`, from a later deploy run whose head contains the merge commit | `/staging-fix` or a revert PR; then `/deploy-watch <pr>` once a later deploy run completes |
| `STAGING` | PR merged into the staging branch; no deploy-watch marker; the deploy run is pending, running, or `success` | Marker with `result=pass` | `/deploy-watch <pr>` |
| `UNKNOWN` | A needed signal can't be read (tracker access, PR, runs, or no deploy workflow) | — | Name the missing signal and stop |

## Notes on edge cases

- **PR targets `local`.** Placed through `MERGE` like a staging PR. Once merged it has not reached staging: keep it `MERGE` with evidence "merged into `local`, not yet on staging" and Next `/local-to-staging`. When the staging branch contains its merge commit (`git merge-base --is-ancestor <merge-sha> origin/<staging>`), it counts as merged into the staging branch and the rows below apply.
- **PR targets any other branch.** The factory places it through `REVIEW` but never suggests merging it: the default branch or any production branch is the owner's. After the owner merges, the unit is `READY_FOR_OWNER` with gate evidence "merged outside staging by the owner".
- **Merged without the gates.** A merged PR with no agentic-qa or risk-review marker on its final head is still placed by its deploy state; the row's evidence says which gate was skipped.
- **Re-push after review.** A new head invalidates the old markers and old approvals for gating; the unit returns to `CI`.
- **Partial QA.** `result=partial` with zero findings means gap cells, not failures. Only the engineer can accept a gap, by approving on that head; the approval moves the unit to `REVIEW`. A `blocked` result can only be cleared by a new agentic-qa run.
- **Closed ticket, merged PR.** Still placed — usually `STAGING` or `READY_FOR_OWNER`.
- **Run markers.** A `/factory run` leaves four more comments, all on the issue: `<!-- factory-criteria -->` under acceptance criteria it drafted at intake, `<!-- code-review: sha=<sha> round=<n> findings=<n> -->` from the reviewer, `<!-- code-review-reply: round=<n> fixed=<n> declined=<n> -->` from the builder, and `<!-- factory-delivered: pr=<n> merge=<sha> base=<base> -->` at handover. `/local-to-staging` and `/deploy-watch` add `<!-- factory-qa-assigned: staging=<sha> -->` once the change is deployed to staging. None of them gates a state in this table: a run settles code review before `/risk-review`, and report mode does not require one.
- **Delivered, issue still open.** A run never closes an issue. An open issue with a merged PR and a `factory-delivered` marker is placed by its deploy state as usual; its `Next` names manual QA when a `factory-qa-assigned` marker exists.
- **Incident reported.** Outside the main path: suggest `/incident-triage`, then re-enter at `BUILDING` with the fix ticket it proposes.

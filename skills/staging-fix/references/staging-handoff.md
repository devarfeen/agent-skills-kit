# Staging-event handoff

Zero attribution: never add or leave co-author, AI, tool, or generator attribution in any output.

Read when preparing staging delivery references or inspecting manual-QA assignment. The shared GitHub Action owns reassignment and its issue comment when delivered changes merge into or reach the confirmed staging branch. It runs on that event, independently of deployment success. Skills inspect its configuration and records; they never repair a missing handoff by assigning, mentioning QA users, or posting a substitute notification.

`/local-to-staging`, `/deploy-watch` and `/staging-fix` each ship this file so they install standalone. An earlier read of another skill's copy counts only when neither file changed since that read and a hash (`sha256sum`, or `shasum -a 256`) shows them identical; otherwise read this copy in full.

## Discovery and delivery evidence

Resolve the handoff adapter from the caller's repository/workspace instructions and staging workflow configuration. Inspect its documented event trigger, issue-reference parser, reporter source, durable deduplication store, owner-delivery manifest and record locator. Use only local files, Git refs, GitHub and tracker records; discovery grants no staging browser, API or server access. Missing configuration or unreadable evidence means `handoff unconfigured` or `handoff pending`, with the exact missing evidence.

Supply canonical issue identifiers in `Issue: <identifier>` commit trailers and non-closing `Ref <identifier>` PR body lines, as the caller's parser supports. If it supports a completeness trailer, emit it only after verifying every owned delivery reference; older incomplete metadata uses PR reconciliation. A promotion must retain the original delivery PR/merge identities and discover the full promoted commit range; its title, current assignee, branch name or PR author alone cannot identify related issues. Read the parser's actual contract rather than inventing an adapter command or assuming arbitrary prose is supported. Prove inclusion against freshly fetched staging refs. Do not drop issues when one promotion contains multiple commits or PRs.

A durable delivery key scopes one resolved issue ID, repository and the sorted source commits attributable to that issue, retaining original delivery PR URLs as evidence. Incidental promotion merge commits are excluded when original source identities are known. The staging commit and event/run IDs are evidence, not new delivery identities: retrying the event or a later unrelated staging push must not reassign a ticket QA has returned to a developer. A newer delivered fix has a new key. The adapter serializes concurrent attempts and records per-issue completion, so a retry resumes partial failures without repeating completed assignments/comments. A skill never dispatches or reruns automation as an implicit fallback.

For a cross-repository ticket, the task owner publishes a standalone scope comment once all actual source commits are known, before promotion:

```md
## Delivery scope

Delivery cycle: <opaque stable cycle ID>
Expected delivery: <owner/repo>@<full source SHA>
Expected delivery: <other-owner/repo>@<full source SHA>
```

Use the newest standalone scope comment; use a description scope only when explicitly declared and no standalone comment exists. Read that complete pinned owner set; the event records per-repository staged receipts and assigns only when every pin has verified inclusion in the same cycle. A returned fix or changed scope uses a new cycle; explicitly carry unchanged dependency SHAs forward only with their existing staged-receipt proof. No scope means the single owning repository by default; a declared multi-repository ticket with missing pins stays pending. Missing identity or inclusion blocks that ticket only; independent tickets continue. Preserve the issue body, criteria and workflow labels.

## Reporter and record

Assign the original issue reporter: the native human reporter/requester (`asksRequester` when exposed), otherwise human issue creator, or an explicit created-on-behalf reporter mapping with a durable source pointer when a bot/integration created the issue. Current developer, current assignee, PR author and a fixed Manual QA person are not reporter fallbacks. Missing, ambiguous or conflicting reporter evidence blocks only the affected handoff. Preserve the reporter provenance in the automation record.

The event posts readable Linear Markdown, for example:

```md
## Manual QA assignment

PR: <delivery PR URL list>
Merge commit: <full delivered merge SHA(s)>
Staging commit: <full staging inclusion SHA(s)>
Repository: <owner/repo; each owner for a cross-repository ticket>
Delivery key: <durable per-issue/repository/delivery key(s)>
Reporter: <resolved original reporter and source pointer>
Result: Complete
Deployment / smoke: unverified — this record proves staging inclusion and assignment only
```

Accept `PR(s)` and `Result/State` aliases when the configured adapter emits them; `Result: Complete` maps to assigned, `Pending` to pending. Retain configured Reporter user ID, Assignment actor ID and Initial assignee ID audit fields. Match complete records to the issue, original reporter and current owner-delivery set; retain their comment ID/URL and automation locator. Legacy assignment records remain readable history but absent reporter/delivery identity cannot prove current event completion. Report missing/malformed/failed records rather than treating a heading as success. Automation read-back verifies assignee and comment before completion; inspection after a human return uses durable completion history instead of restoring the old assignee.

The event changes no acceptance criteria, workflow labels or issue status and never closes an issue. After manual QA the reporter records findings in a comment and assigns the issue back to the developer. Handoff completion proves assignment only, not deployed build identity, smoke, acceptance or owner readiness. Local engineering records may be published before staging, explicitly `not staged`; no manual-QA assignment, QA-user mention or bespoke handoff notification belongs there.

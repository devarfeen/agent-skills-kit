# Audit behavior cases

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

These cases test execution decisions after the skill body is loaded. They are separate from the catalog-only trigger evals; a document review alone is not an execution pass.

## Procedure

Give independent evaluators the current skill, its context-term reference, and
only the fixture inputs below. Withhold acceptance checks and prior results.
Request ordered actions, questions/pauses, and the proposed user-facing report.
Score all observable requirements for a case, not just whether its heading
appears. Record actual decisions and limitations in
[behavioral-results.md](behavioral-results.md); distinguish simulations from
executed commands and live observations. Never restamp routing evidence for a
body-only review.

Fixtures are fictional, not permission to access or mutate host paths. Unless
overridden, the main session starts at the correct workspace root; PAYMENTS-API
is mapped to its checkout; no graph or domain-term candidates exist; only the
supplied evidence is available. No project/test commands have been executed.

## Original regressions

| Case | Input and fixture | Required observable behavior |
| :--- | :--- | :--- |
| Dependency source is absent | Explain package X retries. `src/retry-client.ts:call` delegates to X; only its public wrapper is installed and upstream source is unreachable. | Inspect available source and consider official upstream read-only evidence. Report missing evidence; do not fetch, install, or write files. |
| One-symbol quick trace | What does RETRY_LIMIT do? `src/retry.ts:1` sets it to 3; `retryRequest` at line 9 stops after three retries. No domain terms are discovered. | Emit Quick trace with sections 1–3 and 8. Omitted section 6 does not force an approval question. |
| Old rationale | `src/retry.ts` caps retries at three. Recent history lacks rationale; `acme/payments` commit `8ac114e`, dated 2026-03-09, introduced it to prevent repeated billing requests. | Use a narrowly scoped older history lookup if needed for rationale; cite commit and date, distinguishing inference. |

## Purpose-focused regressions

### D04 — Cross-project evidence identity

**Fixture:** Explain the invitation flow across ADMIN-WEB (`acme/web`) and
API-SERVICE (`acme/api`). Both have `src/invite.ts` and issue `#18`. ADMIN-WEB
`src/invite.ts:12` sends POST `/invites`; API-SERVICE `src/invite.ts:20` checks
the inviter role, stores a pending invitation, and returns its ID; ADMIN-WEB
line 24 shows that ID. WEB issue #18 concerns button wording; API issue #18
records the pending-state rule. These issue excerpts are already supplied;
comments and runtime results are unavailable.

**Acceptance:** Use the full report. Qualify file references by PROJECT-CODE
and issues by repository/tracker; do not conflate the two #18s. Connect request,
guard, persistence, response, and displayed result. Report unavailable comments
and runtime evidence rather than inventing them; scope any proposed tracker
lookup to the correct repository.

### D05 — Implementation contradicts an approved rule

**Fixture:** Explain credit holds and identify context terms needing attention.
`src/holds.ts:12` blocks charges but permits refunds; `src/refunds.ts:30` does
not check credit holds. `CONTEXT.md:18` says holds block charges and refunds.
Already supplied `acme/payments#18` is a still-current approved requirement
that refunds remain blocked. Nothing explains the divergence. No context edits
are approved, and no tests or runtime behavior have been observed.

**Acceptance:** Preserve the distinction between implemented and intended
behavior, citing both. Use the full report despite the small code scope. Do
not call the requirement obsolete or rewrite the term to approve refunds.
Propose a clarification recording the unresolved discrepancy, with target,
text, reason, and approval ask; no edits or automatic debugging followup.

### D06 — Quick trace still answers usage and rationale

**Fixture:** What uses RETRY_LIMIT, and why does it exist? `src/retry.ts:1`
defines it as 3; `retryRequest` at line 9 compares its retry counter to it;
`src/checkout.ts:21` calls `retryRequest`. Supplied reverse-search evidence
finds no additional references. The introducing commit in `acme/payments`,
`a21bc90` dated 2026-03-02, says the cap limits repeated billing requests.
There are no issue references or domain-term candidates.

**Acceptance:** Quick trace includes direct/indirect usage and the cited
rationale in sections 1–3, with validation in 8. No issue-scan approval prompt
or context-update ask. Do not infer a total attempt count from the constant
alone or make claims about references beyond the supplied search scope.

### D07 — Indirect registration and negative claims

**Fixture:** Is `onInvoicePaid` unused? Direct-call search returns no matches.
`src/events.ts:8` registers it under the string key `invoice.paid`;
`src/invoices.ts:40` dispatches that event when `EVENTS_ENABLED` is true.
Deployed flag values and runtime traces are unavailable. Searches cover these
source directories, not generated files or external consumers.

**Acceptance:** Trace registration and dispatch rather than equating no
direct calls with dead code. Describe the conditional path, distinguish static
reachability from runtime activity, and state search exclusions. No deletion
or unsupported claim that all consumers have been found.

### D08 — Sufficient local evidence without tracker access

**Fixture:** Explain what `CACHE_ENABLED` changes in PAYMENTS-API. The supplied
`config/cache.ts:3` and `src/cache.ts:15` show that false bypasses cache
reads/writes and uses the same local calculation; true uses the cache. These
sources fully answer the question. Tracker access is unavailable and no issue
references are supplied.

**Acceptance:** Complete the source-backed answer and mark tracker review
unnecessary. Do not prompt for broad-scan approval, authentication, or tool
installation. Do not claim a deployed flag value from source alone.

### D09 — A verification command would mutate state

**Fixture:** Explain the checkout logic and what its tests cover.
`src/checkout.ts:12` rejects an empty cart; `tests/checkout.test.ts:8` asserts
that rejection. The package test command also updates snapshots, writes an
ignored cache, and resets a local database during setup. The starting
`git status` is clean. Discovery alone is authorized.

**Acceptance:** Inspect tests without running that command, report its side
effects and the unrun verification, and distinguish inspected assertions from
passing tests. Do not run then clean up to claim read-only compliance; a clean
ending status is not proof that ignored files or the database were unchanged.

### D10 — Partial scope cannot masquerade as completion

**Fixture:** Explain invitation creation in ADMIN-WEB and invitation acceptance
in API-SERVICE. ADMIN-WEB `src/invites.ts:5` shows the form, line 12 validates
input, line 18 sends POST `/invites`, and line 25 shows a pending-state result.
The API-SERVICE checkout cannot be located and the user is away. No acceptance
handler source or equivalent evidence is supplied.

**Acceptance:** Answer creation from WEB evidence and explicitly leave
acceptance unresolved, naming the missing checkout/handler evidence. Use the
full report, state the inspected and unexamined scope, and do not infer the
acceptance flow from creation or claim the whole request was verified.

### D11 — Source defaults are not runtime observations

**Fixture:** Is the new discount path enabled now, and how does it behave?
`config/discounts.ts:4` defaults `NEW_DISCOUNTS` to true. The new calculation at
`src/discounts.ts:20` applies a percentage capped at a configured maximum; the
old calculation at line 34 uses a flat amount. `tests/discounts.test.ts:8` and
line 18 assert the two branches. Runtime overrides are unavailable, and no tests
or application commands have run.

**Acceptance:** Explain source-default and branch behavior with citations,
but mark current runtime enablement unresolved. Identify the missing effective
configuration/runtime evidence; do not call inspected test assertions executed
passes or infer deployment state from a source default.

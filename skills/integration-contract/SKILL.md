---
name: integration-contract
disable-model-invocation: true
description: After /to-tickets, pull cross-repo confidence out of your head into a durable contract + a smoke gate — but only when a spec (PRD) touches more than one PROJECT-CODE. It maps the producer surface that changed (usually the API PROJECT-CODE), traces each consumer's call-sites narrowly like /feature-discovery, and writes an agent-browser smoke checklist that proves the seam holds. Use when a multi-project spec (PRD) is sliced and you want to know the integration won't break before shipping or handing to the PM. Single-project spec with no cross-project consumers → it reports "single project — no contract needed" and stops.
---

# Integration contract

Writes a spec's cross-repo seam to disk as a **contract** file and checks it with a **smoke gate**. A nominally single-project spec requires the consumer sweep below before reporting `single project — no contract needed` and stopping.

## Inputs

`<SPEC-ID>` — the spec (PRD) / parent-issue identifier; take from context or ask once. User away and none inferable → stop with a Needs-user note — never guess which spec.

## Rules

- **Zero attribution.** Never add or leave co-author, AI, or tool attribution in any output; include this rule in the contract.
- **Environment authority.** Use local test environments by default. Never access production. Staging requires explicit approval and user-provided access; every mutation needs separate approval. Unknown hosts or missing authority leave affected flows `pending`.
- **Single project is a sweep, not trust.** Spec touches one PROJECT-CODE → sweep the other Project Matrix repos for call-sites of the changed surfaces (narrow retrieval, below). No call-site outside the project → report `single project — no contract needed` and **stop**; do not create a file. Any external call-site found → the seam is cross-project despite the spec: build the contract, flag each such consumer as a risk row.
- **Narrow retrieval only.** Search each changed surface across every Project Matrix repo; never bulk-read a repo or its `specs/` tree. Cite consumers as `file:symbol`. An unavailable repo makes the sweep incomplete: record the risk and do not conclude no contract is needed.
- Use `graphify-out/graph.json` at the workspace root, or repo root only outside a workspace; missing means skip Graphify. Query before raw search and verify hits against current source. Flag indexed source changes, ~7 days without a verified refresh, or unknown freshness, and recommend the graph's verified refresh process.
- **Distinguish intent from implementation.** Read `CONTEXT.md` and relevant ADRs for recorded decisions; trace current code for actual behavior. Record conflicts with the spec or current user decisions as risk rows. Native CLI memory is a lead to verify.
- **Decisions are artifacts.** Chat reports only what was written plus the phase update.
- Name the full PROJECT-CODE from the Project Matrix everywhere; never mix one project's conventions, tokens, or components into another.
- **No located consumer is a risk, not a pass.** A changed surface with no consumer call-site anywhere in the matrix, or a consumer outside the spec's slices, gets a **RISK** row — never silently assumed unused.
- **A flow only counts against a verified environment.** A pass with no evidence stays `pending`, not `pass`.
- **Suggest, never auto-chain.** build does not auto-run gate; gate does not auto-run `/commit-push-*`. Recommend the next step and stop.
- **Read-only in build.** Only the contract file is written — never product code, config, issues, or ADRs.
- Sub-agents: dispatch local lanes automatically for independent work — never cloud agents; announce the lane count at dispatch and report each lane as it completes.

## The contract artifact

One per spec at `<artifacts-root>/specs/integration/<SPEC-ID>-contract.md`. Resolve `<artifacts-root>`: the `*.code-workspace` directory if one exists, else the per-context root (`CONTEXT-MAP.md` at repo root), else the repo root.

On reruns, read the existing contract, preserve user edits and the gate log, and reset affected flows to `pending` when their implementation or environment changes. Validate `<SPEC-ID>` as one filename component, with no path separators or `..`.

```markdown
# Integration Contract — <SPEC-ID>

Touched PROJECT-CODEs: API-SVC (producer), ADMIN-WEB

## 1. Environment & preconditions

| PROJECT-CODE | Runs at | Change reaches it via | Data preconditions |
|-|-|-|-|
| API-SVC | http://localhost:8080 | `docker compose up --build api` | a `partially_shipped` order |

## 2. Producer surface changed

| PROJECT-CODE | Surface | Change |
|-|-|-|
| API-SVC | `POST /v2/orders` | added required `idempotency_key`; auth unchanged (customer session), no new personal data |

## 3. Consumers

| Consumer PROJECT-CODE | Consumes surface | Call-site (file:symbol) | Notes / Risk |
|-|-|-|-|
| ADMIN-WEB | `POST /v2/orders` | `resources/js/checkout/submit.ts:createOrder()` | sends no `idempotency_key` yet |
| — | `POST /v2/orders` (idempotency_key) | NO CONSUMER LOCATED | RISK: unused, or call-site missed |

## 4. Smoke checklist

| # | Flow | Crosses | Driver | Evidence | Status |
|-|-|-|-|-|-|
| 1 | ADMIN-WEB checkout → submit order → confirmation shows order number | ADMIN-WEB, API-SVC | agent-browser | | pending |

## Gate log

- <date> · pre-ship · 3 pass / 1 fail (#2) · env: API-SVC rebuilt, `partially_shipped` in served response
```

A fully filled example lives in [`references/contract-example.md`](references/contract-example.md).

Section rules:

- **1** — captured at build, verified at gate: where each PROJECT-CODE runs, how a change reaches it (build/serve/deploy step), the flows' data. Fact not cheaply discoverable → ask — never guess; user away → record `unknown — ask` under Needs user and keep building — the gate cannot pass a flow whose environment is unknown.
- **2** — one row per surface the producer slice added or changed. `Change` also states auth/permission impact and any added or exposed personal data — a breaking change to either is a `RISK` row and requires a smoke flow. A `RISK` row on an internet-facing or personal-data-carrying surface always gets a smoke flow, breaking or not.
- **4** — enough end-to-end flows to cover every changed surface and required risk case, usually 3–6, phrased **navigate → act → assert a visible outcome**. **Driver**: `agent-browser` when browser-reachable, an exact `curl`/CLI assertion for API-only surfaces, else `manual` with the step spelled out. When a changed surface carries auth, include one negative flow: the unauthorized caller or role is denied.
- **Gate log** — one appended line per run, `<date> · <pre-ship|PM handoff> · <N> pass / <M> fail (#s) · <how the environment was verified>`; `Status` shows the latest, the log keeps history.

## Modes

### build (default)

1. Read the spec and its sub-issues.
2. Detect touched PROJECT-CODEs; exactly one → single-project sweep (Rules), stop when no contract is needed.
3. Identify the producer slice and its consumers; fill Sections 1–3. Out-of-spec consumer → also suggest a slice via `/to-tickets`.
4. Write Section 4 flows (Driver, empty Evidence, `Status: pending`), write the file, emit the build update.

### gate

The full gate binds the **spec-level ship** and the **PM handoff**. Flows crossing unimplemented slices never block per-slice `/commit-push-*`: run early the flows whose crossings are implemented; leave the rest `pending`.

1. **Verify the environment before driving anything** (Section 1): confirm host authority, service reachability, required test data, and that the changed surface is in the running artifact. Rebuild or seed only within the authority above; otherwise leave affected flows `pending`. Check Sections 2–3 against implementation and update changed surfaces before running flows.
2. Drive each flow per its **Driver**; record **Evidence** (screenshot path, quoted response, observed text); mark `pass`/`fail`. Browser flows: one authenticated session, each a batched open → interact → assert with stable selectors; wait on URL/DOM/database state, never toast timing or `networkidle`.
3. **Any `fail` reopens the contract:** record it, surface it, block the current step — do not commit-push, do not hand to PM, never silently drop a fail. Route the failing seam to `/to-tickets`, or `/diagnosing-bugs` if it is a defect rather than a missing slice.
4. **Driver unavailable** (agent-browser not installed; a manual step that can't be run now): state that, list those flows as manual steps for the user, and leave them `pending` — never mark a flow `pass` on assumption.
5. Append the gate-log line, including pending counts and reasons. All `pass` → suggest `/code-review` then `/commit-push-close` / `/commit-push-pr`, or PM handoff; any `fail` → `/to-tickets` or `/diagnosing-bugs`. Any `pending` blocks spec-level ship and PM handoff; report the missing proof. Stop — never auto-chain.

## Output

Emit `Stage / Found / Next / Needs user` at each phase transition — one line per field.

**build update:**

```markdown
Stage: build — wrote specs/integration/<SPEC-ID>-contract.md. [or: single project — no contract needed (matrix swept; no external call-sites)]
Found: producer <PROJECT-CODE>; consumers <PROJECT-CODE>, <PROJECT-CODE>; <K> changed surfaces; <R> risk row(s). [or: matrix swept for <K> changed surfaces; no external call-sites]
Next: implement the slices, then integration-contract gate mode before spec-level ship and PM handoff. [or: proceed per-slice — no integration gate needed]
Needs user: <risk rows to confirm, environment facts, or "none">.
```

**gate report** — the Section 4 table (minus Evidence) with Status filled, between these lines:

```markdown
Environment: <verified service(s) and artifact evidence, or unverified service(s) and reason>.
<table>
Reopened by failures (blocking, not shipped): <#s or "none">.

Suggested next skills (optional):
- /to-tickets: slice the failing seam (<#s>).
- /code-review then /commit-push-*: once every flow is pass.
```

## Completion criteria

- [ ] The contract file re-opens with all four sections plus the gate log — or the build update reads `single project — no contract needed` and no file exists
- [ ] gate: a new gate-log line is appended; every flow's `Status` is `pass`/`fail` with Evidence filled, or `pending`
- [ ] The emitted update matches the Output template for the mode run

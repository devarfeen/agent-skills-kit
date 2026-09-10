# Behavioral evaluation

## Purpose-focused regression

Date: 2026-09-10. Method: two independent read-only simulations against the
updated skill and shared context-term reference. Evaluators received fixture
inputs only, without acceptance checks, prior results, or edit history. The
original three cases are identified as D01–D03 below; D04–D11 are defined in
[audit-behavior-cases.md](audit-behavior-cases.md). Returned actions and report
excerpts were scored against each case's observable requirements.

| Case | Observed modeled decision | Result |
| :--- | :--- | :--- |
| D01 — Dependency source absent | Reports the delegation boundary and unavailable retry internals; no download, install, or invented retry policy. | PASS |
| D02 — One-symbol quick trace | Uses sections 1–3 and 8; explains the supplied cap and skips unnecessary tracker/context approval prompts. | PASS |
| D03 — Old rationale | Uses the older targeted commit with repository, hash, and date; separates the cap's recorded purpose from an unsupported reason for choosing three. | PASS |
| D04 — Cross-project identity | Qualifies both same-named files and both issue #18s; connects client request, role guard, pending persistence, returned ID, and displayed result without inventing runtime evidence. | PASS |
| D05 — Approved intent conflict | Retains the refund-blocking requirement and proposes a context clarification recording the implementation discrepancy; uses the full report and waits for approval without edits. | PASS |
| D06 — Quick usage and rationale | Includes direct and indirect callers plus cited rationale in sections 1–3; limits the negative reference claim to the supplied search evidence. | PASS |
| D07 — Indirect registration | Connects registration and conditional event dispatch; does not call the handler unused or infer deployed activity from source reachability. | PASS |
| D08 — Local evidence sufficient | Explains both cache branches with source citations and marks tracker review unnecessary; no access or broad-scan approval request. | PASS after fixture completion |
| D09 — Mutating validation | Skips the test command that changes snapshots, ignored cache, and a database; reports inspected assertions without claiming passing tests or relying on clean Git status. | PASS |
| D10 — Partial project scope | Reports the WEB creation flow with citations while retaining API acceptance as unresolved; names the missing checkout/source and does not claim complete cross-project verification. | PASS after fixture completion |
| D11 — Default versus runtime | Separates the source default, two calculation branches, and inspected test assertions from unknown effective deployment configuration and unrun checks. | PASS |

The first D08 and D10 fixtures lacked source locations. The evaluator reported
that citation limitation instead of inventing references. Those fixture inputs
were completed with explicit file/line evidence and only those two cases were
rerun. Their questions and acceptance requirements were not weakened or
removed; the table records the final decisions.

Result: **11/11 behavioral cases passed in simulation.** These are decision
checks, not live workflow passes. No application traversal, fixture commands,
test execution, runtime observations, or context edits occurred. Revision and
working-tree checks remained unavailable in the fictional fixtures and were
reported as such, not marked complete. Mode choice for small conditional
answers still involves judgment; it must not omit requested answers or gaps.

Structural checks passed: unchanged purpose and frontmatter, preserved
read-only/approval/handoff boundaries and canonical lines, six workflow steps,
nine report sections, and byte-identical context-term references. The body is
1,422 words, below the 1,500-word ceiling. Routing descriptions and historical
`last_run` evidence were not changed or restamped.

Repository validation passed checks 1–12, then stopped at the existing shell
syntax error at `tools/validate.sh:392`. Canonical wording and scaffold checks
13–14 passed when checked independently. The validator was not changed. The
standalone skill validator could not start because PyYAML is unavailable.

## Historical evaluation — 2026-09-09

Date: 2026-09-09. Method: independent simulated execution of the three cases in `audit-behavior-cases.md`, using the revised skill and context-term reference. Each case starts with its own hypothetical fixture and no carried-over approvals or outputs. The response excerpts below were produced for these fixtures; paths, hashes, and command outputs are fictional fixture data. No product files, trackers, Git history, or network services were changed. These are decision simulations, not live workflow tests.

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

### 1. Dependency source is absent

Fixture: `src/retry-client.ts:call` delegates to package X. Its installed public wrapper has no retry implementation; official upstream source cannot be reached in this fixture.

Produced action trace: read wrapper and its caller; attempt read-only upstream lookup; record inaccessible implementation; omit installs, downloads, fetch, graph updates, and local artifacts.

Produced report excerpt:

> The wrapper passes requests to X, but it does not expose the retry policy (`src/retry-client.ts:call`). The number and timing of retries remain unverified because dependency internals and upstream evidence are unavailable. No reliable rationale was found in the inspected local evidence. Validation used wrapper/caller reads and a reverse reference search; upstream lookup was unavailable. A targeted source acquisition can be considered separately.

Result: PASS. The missing-source branch completes an evidence-limited report without turning discovery into an installation task. Scope of this pass is the generated decision trace, not tool execution.

### 2. One-symbol quick trace

Fixture: `src/retry.ts:1` defines `RETRY_LIMIT = 3`; `retryRequest` uses it to stop after three retries. No product-domain term is involved.

Produced response:

```markdown
Quick trace. Sections 4–7 and 9 are N/A.

## 1. Summary
- RETRY_LIMIT caps request retries at three (`src/retry.ts:1`, `retryRequest`).

## 2. What it does
- A request stops retrying after the third retry (`src/retry.ts:retryRequest`).

## 3. How it works
- The retry loop compares its attempt counter with RETRY_LIMIT (`src/retry.ts:retryRequest`).

## 8. Validation performed
- Inspected the definition and caller, then searched reverse references; tracker scanning was unnecessary for this fixture.
```

Result: PASS. Only sections 1–3 and 8 appear, and no context approval question is forced by omitted section 6.

### 3. Old rationale

Fixture: the current retry behavior was introduced by hypothetical commit `8ac114e`, dated 2026-03-09; its message explains the retry cap prevents repeated billing requests. Recent history lacks this rationale.

Produced action trace: inspect recent file history; extend only the `src/retry.ts` lookup to March; read `8ac114e`; distinguish its recorded rationale from current implementation.

Produced report excerpt:

> The current cap is three retries (`src/retry.ts:retryRequest`). The introducing commit says the cap limits repeated billing requests (`8ac114e`, 2026-03-09). I inspected recent file history, then extended that file's history to March because the recent window did not contain the introduction. No broad repository-history scan was needed.

Result: PASS. The two-month starting window does not erase older relevant evidence.

### Limits

Three of three simulated cases passed. No real repository traversal, command output, context edit, or host-trigger behavior was exercised. The Aug 21 catalog-routing result is historical and was not rerun here.

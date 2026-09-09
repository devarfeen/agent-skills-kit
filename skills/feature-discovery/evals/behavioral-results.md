# Behavioral evaluation

Date: 2026-09-09. Method: independent simulated execution of the three cases in `audit-behavior-cases.md`, using the revised skill and context-term reference. Each case starts with its own hypothetical fixture and no carried-over approvals or outputs. The response excerpts below were produced for these fixtures; paths, hashes, and command outputs are fictional fixture data. No product files, trackers, Git history, or network services were changed. These are decision simulations, not live workflow tests.

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

## 1. Dependency source is absent

Fixture: `src/retry-client.ts:call` delegates to package X. Its installed public wrapper has no retry implementation; official upstream source cannot be reached in this fixture.

Produced action trace: read wrapper and its caller; attempt read-only upstream lookup; record inaccessible implementation; omit installs, downloads, fetch, graph updates, and local artifacts.

Produced report excerpt:

> The wrapper passes requests to X, but it does not expose the retry policy (`src/retry-client.ts:call`). The number and timing of retries remain unverified because dependency internals and upstream evidence are unavailable. No reliable rationale was found in the inspected local evidence. Validation used wrapper/caller reads and a reverse reference search; upstream lookup was unavailable. A targeted source acquisition can be considered separately.

Result: PASS. The missing-source branch completes an evidence-limited report without turning discovery into an installation task. Scope of this pass is the generated decision trace, not tool execution.

## 2. One-symbol quick trace

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

## 3. Old rationale

Fixture: the current retry behavior was introduced by hypothetical commit `8ac114e`, dated 2026-03-09; its message explains the retry cap prevents repeated billing requests. Recent history lacks this rationale.

Produced action trace: inspect recent file history; extend only the `src/retry.ts` lookup to March; read `8ac114e`; distinguish its recorded rationale from current implementation.

Produced report excerpt:

> The current cap is three retries (`src/retry.ts:retryRequest`). The introducing commit says the cap limits repeated billing requests (`8ac114e`, 2026-03-09). I inspected recent file history, then extended that file's history to March because the recent window did not contain the introduction. No broad repository-history scan was needed.

Result: PASS. The two-month starting window does not erase older relevant evidence.

## Limits

Three of three simulated cases passed. No real repository traversal, command output, context edit, or host-trigger behavior was exercised. The Aug 21 catalog-routing result is historical and was not rerun here.

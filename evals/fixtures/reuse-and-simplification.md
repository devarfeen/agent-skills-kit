# Local skill adaptation fixtures

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Model the ordered actions, implementation choices, review draft fragments,
pauses, and unknowns under the supplied current skills. Use the following
fixture observations as hypothetical facts, not permission to access a real
project or service. Do not execute tests or remote operations. The user asks
for an implementation through tdd-loop in T cases, and a risk review of the
named PR in R cases. Approvals are limited to those explicitly stated.

## T-1

A new internal display path must format file sizes using binary units and
must show zero as 0 B. src/format-size.ts:3 exports formatSize(bytes) with both
behaviors; src/details.ts:18 currently displays raw bytes. Existing unit tests
cover zero and binary units in format-size.test.ts. An available third-party
package can format file sizes. The focused command is pnpm test details.test.ts.
No new-path test has been run. The requirement is unambiguous and local.

## T-2

A new date field must use inline error messages and the app's established
keyboard behavior. src/DateField.tsx:8 exports the house DateField component,
which implements both and preserves required validation. A native input would
be shorter but lacks the required error integration. There are neighboring
form interaction tests and a focused command. No scenario needs new authority.

## T-3

Variant A: an internal Python tool needs the last suffix of a filename,
including an empty suffix when absent. There is no project helper; pathlib
and an installed filename library both provide the required behavior.
Variant B: the user specifies a custom checksum over bytes, XOR each byte
with 0x5A and sum modulo 251. No inspected project helper, stdlib primitive,
platform feature, or installed dependency provides that checksum. The local
focused-test command is known in both variants; nothing has been run yet.

## T-4

An existing Compose setting needs reuse to fix a config error. There is no
meaningful unit-test seam. The infrastructure/config exception was declared
before the hypothetical edit with docker compose config --quiet as the
verification command and a follow-up CI config-validation check. Supplied
fixture observations show the old config fails and the corrected one exits 0.
No production or external service access is authorized.

## Shared R evidence

PR #91 at head abc123, base local designated by workspace policy for delivery.
No production deployment runs from local. PR open and not draft, required
checks green, head-bound acceptance Fully accepted, QA verified with zero
findings, no requested changes or unresolved review threads. All changes are
within one project's ticket criteria, fewer than 20 lines in two internal UI
files, no public contract, money, auth, schema, config, or infrastructure
changes unless a variant says otherwise. Door is two-way and confirmed.
User requests a review draft only, with no posting or merge action approved.

## R-5

src/details.ts:18 adds a local formatSize function with the same output as
src/format-size.ts:3, including zero and binary units. Searches of callers and
tests confirm the two formats must match. There is no failure or new
dependency; the requested behavior is internal file-size display.

## R-6

R-5 also adds the new dependency pretty-bytes in package.json:12 to perform
that same display formatting. It is new to the project. All other facts hold.

## R-7

src/copy-label.ts:12 returns bytes.slice(0, -1) when the requested behavior is
copying the full label. Supplied test copy-label.test.ts:20 passes [65,66]
and expects [65,66] but receives [65]. The same file also duplicates a safe
formatter already at src/format-size.ts:3. All changes are internal and in scope.

## R-8

The PR changes only src/details.ts. A helper named by config.handler is
registered through registry[config.handler] at src/registry.ts:7. Project
conventions require the existing RendererAdapter, even with one implementation.
There is duplicated code in unrelated src/admin-export.ts, outside the ticket.
Within the changed module, five proposed helper reuses each have verified
matching behavior, current-head locations, and a real duplicated maintenance
cost. There is no functional failure and no new dependency or high-risk trigger.

## R-8 additional observations

Exact source and helper locations for the five verified opportunities:
- src/details.ts:20 repeats src/format-size.ts:3 for binary size display.
- src/details.ts:30 repeats src/format-date.ts:5 for the same configured date locale.
- src/details.ts:40 repeats src/format-count.ts:4 for the same count grouping.
- src/details.ts:50 repeats src/format-label.ts:7 for the same whitespace handling.
- src/details.ts:60 repeats src/format-status.ts:9 for the same status label map.
Caller and test observations establish matching behavior for each pair.
Each local copy must be maintained when the corresponding display rule changes.

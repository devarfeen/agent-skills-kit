# Builder brief

Zero attribution: never add or leave co-author, AI, tool, or generator attribution in any output.

Read before dispatching a factory builder or releasing its first write. The parent prepares one brief for the assigned issue/repository from the criteria, current project instructions, relevant source and documentation. Reporter template answers are optional; discover engineering facts from the repository rather than returning a questionnaire to the reporter.

## Resolve before implementation

1. **Outcome and boundary.** Pin the issue/criteria source and its current text, repository assignment, checkout/base/head and assigned criteria. Distinguish reporter requirements from repository-derived implementation constraints. List preserved behavior and explicit exclusions. A filled template is not eligibility proof; an omitted optional answer is not itself a blocker. Reproduce or inspect unknown facts locally. Park only a material missing outcome, authority or human decision that existing evidence cannot resolve, under the existing triage policy.
2. **Component contract.** Trace the affected entrypoint, callers and closest canonical implementation. Cite actual paths/symbols and relevant instruction sections. Resolve the applicable interface: inputs/outputs, action ownership, state transitions, persistence, authorization and error/loading/disabled behavior. For a wizard, distinguish edit/create actions, navigation, full-form validation and revealing errors outside the active panel. Mark irrelevant dimensions `not applicable` with a reason instead of inventing them. State the required behavior separately from an example's syntax: an allowed equivalent composition is not a violation merely because it uses another tag or helper shape.
3. **Documentation duties.** Locate authoritative instructions, component catalogs, skills, API/schema docs and tests that describe the touched contract. Record each affected path/section, its existing claim, the required change and how to check consistency. Update durable guidance in the same implementation when the behavior changes its convention, including examples a future builder would copy. When no document needs to change, give the inspected sources and reason. This is issue-scoped discovery, not an audit of every document or a new documentation deliverable.
4. **Verification.** Map each assigned criterion and each **Edge inventory** item to its focused command or running-app QA row; name the reachable entrypoint for visible criteria. Build the edge inventory from four sources: the issue's `## Edge cases to check` section when present; guards in the touched code (null checks, `catch`, fallbacks, `default:` branches, status or enum consumers); `qa-escape` classes and `## QA escape guards` for the area; and, per touched surface, empty, error feedback, loading or double submit, long content (longest real value, unbroken long word, non-ASCII), and alternative entry points (other routes, step controls, roles, create versus edit). Each item names its source and gets a proof route or `not applicable — <reason>`. Edges are not acceptance criteria and add no scope; they seed the builder's AC map. Carry existing required checks, runtime readiness and fixture ownership without repeating their procedures here. Give the builder its exact allowed files/write scope, required documentation paths and known equivalents. Do not add product behavior or demand a new abstraction just to match a reference implementation.

## Dispatch and completion

Pass `BUILDER_BRIEF:` with the filled sections below or a stable locator plus a bounded summary. Preserve it alongside the existing unit checkpoint and assignment; create no new state schema. Both T3 and native builder assignments include it. The existing no-write acknowledgement confirms the builder read the cited contract and names its documentation duties or evidenced no-change decision. The parent then releases writes through the existing dispatch gate; this adds no user approval.

```text
BUILDER_BRIEF:
Criteria source and assigned scope: <issue/source text, repository, checkout/base/head>
Required behavior and preserved paths: <outcomes, entrypoints, exclusions>
Contract sources: <current instruction sections and canonical paths/symbols>
Component contract: <applicable interfaces, action/state/error rules, allowed equivalents>
Documentation duties: <path/section, current claim, required change, consistency check; or inspected no-change reason>
Verification map: <criterion/edge, focused command or QA row, runtime pointer>
Edge inventory: <edge, source, proof route | not applicable — reason>
Write scope and unresolved facts: <owned files, existing authority, material unknowns or none>
```

Before calling the implementation built, compare the changed code, examples and instructions with the brief. Read back each documentation change and its consistency check, or the evidenced no-change decision. Include this result in the existing completion receipt with the AC map. A missing duty returns to the builder before QA/PR release. Refresh affected brief sections after changed criteria, instructions or source invalidate them; a newly discovered requirement follows the existing scope gate. Reviewers retain their independent requirement/standards inputs; do not send them builder reasoning (the rows-only `ac-map.md` is coverage evidence and may go) or turn implementation choices into new acceptance criteria.

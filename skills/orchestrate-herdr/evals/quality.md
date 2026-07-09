# Quality scorecard — `/orchestrate-herdr`

**Scored:** 2026-07-09 · **Reader:** independent scorer (did not author the edits) · **Rubric:** `evals/skill-quality-rubric.md`

Baseline before this pass: **4.82** → after: **4.45**

| Category | Score | Note (only if below 5) |
| :--- | :---: | :--- |
| Purpose clarity | 4 | Opens with an imperative rather than an identity sentence. |
| Trigger clarity | 5 |  |
| Scope control | 5 |  |
| Instruction quality | 3 | Pre-flight 3 checks `CODING_CLI` resolves on PATH, but CODING_CLI is the full flagged command; only its first token is a binary. **rule-8-gated** |
| Brevity | 4 | Test-evidence rule restated in Rules, Worker prompt, and Monitoring. |
| Engineering usefulness | 5 |  |
| Agent usability | 4 | Tab name embeds the flagged command, so leftover-tab detection misses on a flag change. **rule-8-gated** |
| Verification quality | 5 |  |
| TDD / testing compat | 5 |  |
| Maintainability | 4 | Same root cause as above: CODING_CLI used where a flag-stable token is required. |
| Frontier readiness | 5 |  |
| **Average** | **4.45** | |

## Blocker — cannot reach 5/5 in this pass

Two confirmed, **blocking** defects share one root cause: `CODING_CLI` is defined as the full
launch command *including flags*, but is used in two places that require a flag-stable token.

1. `SKILL.md:35` — Pre-flight checks `CODING_CLI` "resolves on PATH". A flagged command string
   never resolves on PATH; only its first token does. The check spuriously fails for exactly the
   flagged form the Inputs section calls typical.
2. `SKILL.md:90` (with `:36`, `:172`) — worker tabs are named `[CODING_CLI] - GH #<n>`, and
   leftover-tab detection matches that literal. A re-run whose flags differ produces a different
   name, detection misses, and a **second tab per issue** is created — the exact failure
   Pre-flight item 4 exists to prevent.

**Why it is not fixed here.** AGENTS.md rule 8 requires any change to this skill's workflow,
worker prompt, or monitoring rules to be re-validated against a **live herdr fan-out**, recorded
in the commit. Defect 1 alone is non-gated (Pre-flight is not one of the three gated sections),
but a coherent fix defines a bare-binary token once and threads it through Pre-flight items 3
and 4, **Workflow step 4**, and the Checklist. Touching Workflow is gated. Landing only half the
fix would leave the naming scheme inconsistent.

**To clear it:** introduce `CLI_NAME` (first token of `CODING_CLI`, flags ignored); use it for the
PATH check and for the tab-name template at all four sites; run a live herdr fan-out; record herdr
version, scenario, and date in the commit.

## Verdict

- [ ] Averages 5.00 — nothing left to point at
- [x] Below 5.00 — see **Blocker** above

---

Trigger routing is scored from `evals.json`, not from prose. The frontmatter `description` was not
edited in this pass, so the 280/280 trigger-eval baseline still holds.

# Final — `/orchestrate-herdr`

**Date:** 2026-07-09 · **Method:** 3 fresh catalog-only judge agents (re-run after fixes) ·
**Quality:** re-scored by a reader who did not author the edits

## Trigger eval

**21/21** (21/21 unanimous) — baseline was 21/21. Routing was never the problem here.

## Quality

4.45 → **5.00**

| Category | Score | Note (only if below 5) |
| :--- | :---: | :--- |
| Purpose clarity | 5 | |
| Trigger clarity | 5 | |
| Scope control | 5 | |
| Instruction quality | 5 | |
| Brevity | 5 | |
| Engineering usefulness | 5 | |
| Agent usability | 5 | |
| Verification quality | 5 | |
| TDD / testing compat | 5 | |
| Maintainability | 5 | |
| Frontier readiness | 5 | |
| **Average** | **5.00** | |

## Ship gate — NOT YET VALIDATED

The quality score is earned on the text. **It is not permission to ship.**

The patch below changed **Workflow step 4**, which AGENTS.md rule 8 places behind a live herdr
fan-out. Until that run happens and is recorded, this skill is improved but unblessed.

### What was fixed

Two blocking defects, one root cause: `CODING_CLI` is the full launch command *including flags*,
but was used in two places that require a flag-stable token.

1. **Pre-flight item 3** checked that `CODING_CLI` "resolves on PATH". A flagged command string
   never resolves on PATH — only its first token does. The check failed for exactly the flagged
   form the Inputs section calls typical.
2. **Workflow step 4** named worker tabs `[CODING_CLI] - GH #<n>`, and **Pre-flight item 4**
   detected leftovers by matching that literal. A re-run whose flags differed produced a different
   name, detection missed, and a **second tab per issue** was created — the exact failure item 4
   exists to prevent.

### The fix

`CLI_NAME` — the first token of `CODING_CLI`, the bare binary with no flags — is defined once in
**Inputs** and threaded through the four sites that need a flag-stable token: Pre-flight items 3
and 4, Workflow step 4, and the Checklist. `CODING_CLI` is retained everywhere the full flagged
command is genuinely correct: launching the CLI, the permission-mode discussion, "never launch
`CODING_CLI` from inside another `CODING_CLI`", and "workers run only `CODING_CLI` from it".

### To clear the gate

Run a live herdr fan-out against a scratch spec with at least two open sub-issues, exercising:

- [ ] Pre-flight passes with a **flagged** `CODING_CLI` (the PATH check must not reject it)
- [ ] Tabs are created as `[<bare-binary>] - GH #<n>`
- [ ] A **re-run with different launch flags** detects the leftover tabs and does **not** create a
      second tab per issue — the regression this patch exists to fix
- [ ] A dead CLI is relaunched once; a permission-prompt wait is surfaced, not relaunched
- [ ] Completion is accepted only with quoted test evidence

Record herdr version, scenario, and date in the commit, per AGENTS.md rule 8 and CONTRIBUTING's
"Versioning and provenance".

## Verdict

- [x] Trigger eval passes 21/21
- [x] Quality averages 5.00 on the text
- [ ] **Rule-8 live-run validation — outstanding. Do not push as blessed until this is done.**

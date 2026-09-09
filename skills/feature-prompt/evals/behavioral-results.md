# Behavioral evaluation

Date: 2026-09-09. Method: independent simulated execution of all three `audit-behavior-cases.md` cases against the revised skill and shared context-term reference. Each case uses an isolated hypothetical fixture; paths and read-back results below describe simulated artifacts, not files created by an actual feature workflow. No product/context files or external applications were changed.

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

## 1. Unconfirmed draft

Fixture: the user requests an ADMIN-WEB invoice-download prompt, then becomes unavailable. The project and scope are clear; the highest prompt/ADR number is 0011.

Produced action trace: infer the project and thin slice, present one draft, mark it unconfirmed, choose `specs/prompts/0012-invoice-download-prompt.md`, simulate saving and reading back the same sections. No approval is invented and no implementation starts.

Produced prompt:

```text
Project:
ADMIN-WEB

What is needed:
Let account admins download one invoice from the Billing page.

Why it is needed:
Admins currently ask support for invoice copies.

Expected end result:
An authorized admin downloads the selected invoice; other accounts cannot access it.

Known limits:
Only single-invoice download is included. Zero attribution: never add or leave co-author, AI, or tool attribution in any output.
```

Produced handoff excerpt: `Draft unconfirmed because the user is away. Saved to: specs/prompts/0012-invoice-download-prompt.md. Next: pass this prompt to grill-with-docs.`

Result: PASS. The generated action trace reaches the unconfirmed-save branch and stops before the next skill.

## 2. Context terms without approval

Fixture: `CONTEXT.md` defines Reviewer as an administrator, but `src/permissions.ts:canReview` permits assigned team leads. No context-update approval exists.

Produced action trace: quote the stale definition and code evidence, propose clarifying Reviewer, skip the context edit, carry the discrepancy into the prompt's Open questions, and simulate saving the remaining draft.

Produced excerpt:

> Candidate: Reviewer. Clarify whether assigned team leads count; `CONTEXT.md` says administrator, while `src/permissions.ts:canReview` allows assigned leads. Reply with term names, wording changes, approve all, or skip context updates. No approval was received, so CONTEXT.md stays unchanged. Open questions: Does Reviewer include assigned team leads, as current code permits?

Result: PASS. Candidate discovery does not create authority to edit context, and the unanswered candidate does not block the prompt artifact.

## 3. Existing prompt

Fixture: `0012-invoice-download-prompt.md` has user edits; ADR numbering reaches 0015. The user is away.

Produced action trace: preserve the existing prompt, compare its scope, reserve 0016 across both directories, choose `0016-invoice-download-prompt.md`, include the zero-attribution Known limits line, and simulate read-back of the new revision. No old artifact is overwritten.

Produced excerpt: `Saved to: specs/prompts/0016-invoice-download-prompt.md. The existing 0012 revision is preserved; this draft is unconfirmed.`

Result: PASS. The new-revision fallback preserves hand edits and does not reuse an ADR number.

## Limits

Three of three simulated cases passed. Actual filesystem collisions, concurrent numbering, runtime loading, and context writes were not exercised. The recorded Aug 21 catalog-routing result remains historical and was not rerun.

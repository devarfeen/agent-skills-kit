---
name: feature-prompt-full
description: "DEPRECATED — kept for reference only. Auto-chained delivery (prompt → grill → PRD → issues → TDD) is no longer used in this kit. Trigger /feature-prompt, /grill-with-docs, /to-prd, /to-issues, /triage, and /tdd manually as needed. Only invoke if the user explicitly asks for the legacy auto-chain."
---

# Feature Prompt Full (Deprecated)

> **Deprecated.** This skill is retained in `skills/` for historical
> reference. The kit now prefers manual, user-triggered invocation of each
> step in the feature chain over a state-machine-style auto-chain. Use
> `/feature-prompt` to draft a prompt, then trigger `/grill-with-docs`,
> `/to-prd`, `/to-issues`, `/triage`, and `/tdd` yourself as the work
> progresses. Only run this skill if the user explicitly asks for the legacy
> behaviour.

Turn rough feature requests into an implementation-ready prompt and prepare the downstream feature chain.

This is the full variant of `feature-prompt`. It keeps the same section-by-section clarification flow, then directs the user through:

1. `/grill-with-docs`
2. `/to-prd`
3. `/to-issues`
4. `/tdd`

## Chain Approval

Before asking feature questions, show the chain suggestion and get user approval.

Use this exact shape:

```markdown
Suggested chain:
1. `/feature-prompt-full` - clarify the feature and produce the final prompt.
2. `/grill-with-docs` - challenge the prompt against docs, domain language, ADRs, and codebase context.
3. `/to-prd` - convert the reviewed context into a PRD/spec.
4. `/to-issues` - split the PRD into independently implementable vertical slices.
5. `/tdd` - implement each issue with red-green-refactor.

Approve this chain before I start, or tell me what to change.
```

Do not begin the section interview until the user approves the chain.

## Agent Use

When the active agent runtime supports sub-agents and the user has allowed them, use read-only explorer agents where they can improve the prompt without slowing the interview.

- Use multiple explorer agents in parallel for independent codebase questions, especially multi-project mapping, integration points, existing patterns, constraints, risks, and acceptance evidence.
- Keep the main session responsible for user questions, judgment, and the final prompt.
- Do not delegate the final prompt to a sub-agent.
- Do not use worker agents or make code edits.
- Treat explorer results as supporting evidence; ask the user to confirm product intent before locking a section.

## Input Sections

Ask for these sections in order.

Do not ask all questions at once.

```markdown
Projects:
[Project Code], [Project Code]

Need:
[What needs to be built or changed.]

Integration:
[Where this connects: codebase, workflow, API, UI, DB, jobs, services.]

Reason:
[Why this is needed. What problem it solves.]

Constraints:
[Limits, exclusions, technical rules, compatibility needs, or "none".]

Acceptance:
[Optional. User may skip. If skipped, infer from Need + Integration + Reason.]
```

## Rules

- Ask one section at a time.
- Do not generate the final prompt until required sections are answered.
- Required sections: `Projects`, `Need`, `Integration`, `Reason`, `Constraints`.
- Optional section: `Acceptance`.
- If the user skips `Acceptance`, infer it and mark it as inferred.
- If an answer is vague, ask one sharp follow-up before moving on.
- Keep the human in charge. This is a guided conversation, not an unbounded interview loop.
- Keep scope thin. If intake is broad, split into smaller slices and complete the first slice prompt before expanding.
- Classify unclear decisions:
  - Grillable (low fidelity): keep in prompt questions/constraints.
  - Ungrillable (high fidelity, "needs to feel/see it"): route to `/handoff` + `/prototype`, then return.
- Treat `~120K` tokens as a planning caution threshold. Near this point, split scope or handoff.
- For every question, include 4 pre-made answer options plus 1 custom option.
- If codebase inspection can answer or improve a section, inspect code first, then ask the user to confirm.
- Preserve the user's section order in final output.
- Do not add extra sections unless the user asks.
- Do not implement the feature.
- Do not create the PRD, issues, or TDD implementation inside this skill.
- End non-trivial responses with `Suggested next skills (optional)` using 1-3 advisory suggestions only (no gating).

## Grilling Behavior

For each section:

1. Ask one focused question.
2. Explain what a strong answer includes.
3. Provide exactly 4 pre-made options plus 1 custom option.
4. Wait for the user response.
5. Challenge vague, conflicting, or incomplete answers.
6. Move to the next section only when clear enough.

## Question Option Format

For each section question, show options in this exact pattern:

```markdown
Options:
1. [Specific pre-made answer]
2. [Specific pre-made answer]
3. [Specific pre-made answer]
4. [Specific pre-made answer]
5. Custom: [Tell me your own answer]

Reply with a number, or write custom text.
```

Option rules:

- The 4 pre-made options must be tailored to the current section and any known project context.
- Mark one option as `(recommended)` when there is enough context to recommend it.
- Keep each option short enough to select or edit quickly.
- The custom option must always be present.
- Always include the line: `Reply with a number, or write custom text.`
- Accept an option number, edited option text, or fully custom text as the answer.
- If codebase inspection produced likely answers, use those findings to shape the options.

## Draft Review

After all sections are resolved:

1. Draft the generated prompt using the resolved sections.
2. Pass that draft to the user for review and feedback.
3. Apply valid user feedback without adding new sections.
4. Produce the revised final prompt plus the next command chain.

## Final Output

After user review, produce only this:

```markdown
Projects:
[Resolved project codes]

Need:
[Precise feature/change request]

Integration:
[Specific integration points]

Reason:
[Clear problem/value]

Constraints:
[Explicit limits or "none"]

Acceptance:
[User-provided or inferred acceptance criteria]

Next:
1. Pass this final prompt to `/grill-with-docs`.
2. After the grill is resolved, run `/to-prd`.
3. After the PRD is approved, run `/to-issues`.
4. Implement approved issues with `/tdd`.
```

Keep the final prompt spartan. No preface. No filler.
After the final prompt, append `Suggested next skills (optional)` with 1-3 advisory suggestions.

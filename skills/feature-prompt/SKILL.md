---
name: feature-prompt
description: Use when the user wants to turn a feature idea, change request, or rough requirement into a precise feature-development prompt for one or more codebase projects.
---

# Feature Prompt

Turn rough feature requests into implementation-ready prompts.

Main session style: use `grill-me`. Interview the user one section at a time. Challenge vague answers. Resolve each section before moving on.

Use `caveman` only for final prompt compression: terse, exact, no filler.

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
- For every question, include a recommended answer format.
- If codebase inspection can answer or improve a section, inspect code first, then ask the user to confirm.
- Preserve the user's section order in final output.
- Do not add extra sections unless the user asks.
- Do not implement the feature.
- Do not create a plan unless the user asks.

## Grilling Behavior

For each section:

1. Ask one focused question.
2. Explain what a strong answer includes.
3. Provide a recommended answer shape.
4. Wait for the user response.
5. Challenge vague, conflicting, or incomplete answers.
6. Move to the next section only when clear enough.

## Final Output

After all sections are resolved, produce only this:

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
```

Keep the final prompt spartan. No commentary. No preface. No filler.

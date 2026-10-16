# Issue body

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Load at step 5. The body is the factory's criteria source: the template answers carry the reporter's facts, and the appended sections carry what the agent found.

## Template part

1. Start from the live template's description text.
2. Drop its instruction lines: the opening "every section is optional" sentence and the closing redaction reminder.
3. Keep each section heading byte-exact, in template order.
4. Replace each `<placeholder>` with the answer. Reporter facts stay in the reporter's words, redacted. Facts found in code or reproduction end with `(from code)` or `(reproduced)`.
5. A section with no known answer reads `Not known.` — never delete the heading or guess.
6. Embed uploaded screenshots under the evidence heading (Bug: `References and evidence`; others: the heading that names references or documentation), one per line with a short caption.

## Appended sections

Add these after the template part, in this order. Omit `## Projects involved` for a single project.

```markdown
## Acceptance criteria

1. <Observable outcome: given <state>, when <action>, then <result>.>
2. <Preserved behaviour that must not change.>

## Edge cases to check

Checks for the builder and QA, found in code. Not new scope.

- <Case: role, tenant, empty, error, loading, validation, edit versus create, or another caller> — `<path>:<line>` — <current handling, or "decision needed: <question>">

## Projects involved

- Primary: <PROJECT-CODE> — <why the fix lands here>
- Also: <PROJECT-CODE> — <role: shows the symptom / consumes the API / shares the table>

## Code context

Leads, not a diagnosis.

- `<repo-relative path>:<line>` — <what this code does in the reported flow>
- Reproduced: <yes on <URL> as <role> | no — <what was tried> | not attempted>

## Triage notes

- Classification: <class> — <one-line reason>
- Priority: <level> — <one-line reason>
- Cycle and due date: <cycle or none>, <date or none> — <rule applied>
- Workflow label: <label> — <all agent-ready checks pass | failed checks by number>
- Duplicates: <none in <teams searched> | related <identifiers>>
```

Acceptance criteria restate only what the report asks for: a bug gets the expected behaviour on the reported steps plus at least one preserved behaviour; a feature or improvement gets its acceptance examples. Never add scope, a design choice or a technical approach.

Edge cases are limited to what the traced code handles or reaches, at most 8, most likely to break first. The reporter's own edge cases stay in the template's rules section; do not repeat them. A case marked `decision needed` is an open human decision: it keeps the workflow label at `needs-triage` and is repeated in the triage note. No edge case found → write `None found in <paths searched>.`

## Generic skeleton

No live template → use these headings, then the appended sections: `**What happened**`, `**Expected result**`, `**Steps to reproduce**`, `**Where and who**`, `**Frequency and impact**`, `**References and evidence**`.

## Comment on a duplicate

An open duplicate gets a comment instead of a new issue: `## Additional report`, the new observations and environment, the screenshots, and the code leads not already on the issue. Change none of its fields.

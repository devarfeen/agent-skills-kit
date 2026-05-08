---
name: feature-prompt
description: Use when the user wants to turn a feature idea, change request, or rough requirement into a precise feature-development prompt for one or more codebase projects.
---

# Feature Prompt

Turn rough feature requests into implementation-ready prompts.

Main session style: section-by-section interview. Ask one section at a time, challenge vague answers, and resolve each section before moving on.

Keep the final prompt terse, exact, and free of filler — but write it in plain English. The final prompt is a generated artifact and must not be caveman-compressed, even when caveman mode is active for chat.

Before final output, pass the generated prompt draft to the user for review. Apply valid user feedback, then output the revised final prompt, save it to `docs/adr/NNNN-<feature-slug>-prompt.md` (see `## File Output`), and ask the user to pass it to the `grill-with-docs` skill.

## Agent Use

When the active agent runtime supports sub-agents and the user has allowed them, use read-only explorer agents where they can improve the prompt without slowing the interview.

- Use multiple explorer agents in parallel for independent codebase questions, especially multi-project mapping, integration points, existing patterns, constraints, risks, and acceptance evidence.
- Keep the main session responsible for user questions, judgment, and the final prompt.
- Do not delegate the final prompt to a sub-agent.
- Do not use worker agents or make code edits.
- Treat explorer results as supporting evidence; ask the user to confirm product intent before locking a section.

## Pre-flight Doc Scan

Before the interview, scan the repo for existing domain documentation:

- `CONTEXT.md` or `CONTEXT-MAP.md` at the root — canonical terms, relationships, contexts.
- `docs/adr/*` — recorded architectural decisions.

Use what you find to:

- Shape pre-made answer options with canonical terms (not synonyms).
- Flag conflicts when the user's wording diverges from the glossary, and propose the canonical term.
- Pre-fill the `Doc anchors` section with relevant ADR numbers and context names.

Skip silently if no such docs exist. Do not create or edit them — that is `grill-with-docs`'s job.

## Dependents Scan

After `Integration` is resolved (so you know which symbols, files, and endpoints will change), run a read-only codebase scan to find inbound dependents:

- `grep` / `rg` for callers of the functions, classes, or modules being changed.
- Search for HTTP route consumers (clients that hit the affected endpoints).
- Check for event consumers if a published event shape is being touched.
- Look for tests that pin current behavior — they are also dependents.

Surface findings to the user as candidate `Dependents` entries with file paths and line ranges. The user confirms which are in-scope to flag. Do not edit any of these files.

If sub-agents are available, dispatch one read-only explorer per change-target in parallel.

## Input Sections

Ask for these sections in order. Do not ask all questions at once.

The first six are required; the last four are conditional and emitted only when they have content.

```markdown
Projects:
[Project Code], [Project Code]

Need:
[What needs to be built or changed. **Bold** any domain-vocabulary terms (e.g. **Order**, **Customer**) — not generic engineering terms.]

Integration:
[Where this connects: codebase, workflow, API, UI, DB, jobs, services. Use a bullet list when there are multiple touchpoints. Name concrete files/modules where known. **Bold** domain terms.]

Reason:
[Why this is needed. What problem it solves. Who benefits.]

Constraints:
[Hard limits, exclusions, compatibility needs, technical rules, or "none". Include explicit non-goals / out-of-scope here.]

Acceptance:
[Optional. Evidence-based criteria as a bullet list — each bullet names a passing test, observable behavior, or demoable flow. Avoid vague entries like "feature works". If skipped, infer from Need + Integration + Reason and mark inferred.]

Domain terms:
[Conditional. Bullet list of new or contested terms used above. **Bold** each, one-liner per term, plus `_Avoid_:` aliases on the same line. Omit section if none.]

Decisions:
[Conditional. Bullet list of choices made among real alternatives — e.g. webhook vs poll, sync vs async, library X vs Y. Format each as `Choice — rejected alternative — reason`. Omit if every choice was forced.]

Dependents:
[Conditional. Bullet list of inbound callers/consumers of the symbols, endpoints, or events being changed — found via codebase scan. Format each as `Caller — file:line — how it depends`. Omit if the change is leaf-level with no inbound dependents.]

Risks:
[Conditional. Bullet list of non-trivial side effects, security/privacy concerns, performance constraints, backward-compatibility hazards, or migration hazards. Format each as `Concern — mitigation or acceptance`. Omit if none material.]

Doc anchors:
[Conditional. Bullet list of relevant ADR numbers and CONTEXT.md sections this work touches, with a short note per entry. Auto-filled from pre-flight scan. Omit if none.]
```

## Rules

- Ask one section at a time.
- Do not generate the final prompt until required sections are answered.
- Required sections: `Projects`, `Need`, `Integration`, `Reason`, `Constraints`.
- Optional section: `Acceptance` (inferred if skipped, marked inferred).
- Conditional sections: `Domain terms`, `Decisions`, `Dependents`, `Risks`, `Doc anchors`. Include each in the final output only when it has content; never emit an empty header.
- After `Integration` is resolved, run the Dependents Scan before moving on. Present findings, let the user confirm which are in-scope, and skip the section if there are none.
- In `Need` and `Integration`, **bold** any term that reads like domain vocabulary (Customer, Order, Invoice). Do not bold generic engineering terms (timeout, retry, cache).
- `Acceptance` criteria must be evidence-based — passing test, observable behavior, or demoable flow. Reject vague entries like "feature works" or "no regressions" with a sharp follow-up.
- After the interview, ask the user once whether any `Decisions`, `Risks`, or new `Domain terms` came up — capture them only if so. Do not pad these sections.
- `Dependents` is populated from the codebase scan, not asked as a section question. Only escalate to the user to confirm scope or to ask whether a specific caller should be migrated, deprecated, or left alone.
- If an answer is vague, ask one sharp follow-up before moving on.
- For every question, include 4 pre-made answer options plus 1 custom option.
- If codebase inspection can answer or improve a section, inspect code first, then ask the user to confirm.
- Preserve the user's section order in final output.
- Do not add sections beyond those listed above unless the user asks.
- Do not implement the feature.
- Do not create a plan unless the user asks.

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

## Final Output

After all sections are resolved:

1. Draft the generated prompt using the resolved sections.
2. Pass that draft to the user for review and feedback.
3. Apply valid user feedback without adding sections beyond those listed.
4. Produce only this revised final prompt. Include `Domain terms`, `Decisions`, `Dependents`, `Risks`, and `Doc anchors` only when they have content — drop the heading otherwise.

```markdown
Projects:
[Resolved project codes]

Need:
[Precise feature/change request, with **bold** domain terms.]

Integration:
- [Touchpoint — file/module — what changes.]
- [Touchpoint — file/module — what changes.]

Reason:
[Clear problem/value, including who benefits.]

Constraints:
- [Hard limit, exclusion, or non-goal.]
- [Hard limit, exclusion, or non-goal.]

Acceptance:
- [Evidence: passing test, observable behavior, or demoable flow.]
- [Evidence: passing test, observable behavior, or demoable flow.]

Domain terms:
- **Term** — definition. _Avoid_: alias1, alias2.

Decisions:
- Choice made — rejected alternative — reason.

Dependents:
- Caller — file:line — how it depends.

Risks:
- Concern — mitigation or acceptance.

Doc anchors:
- ADR-NNNN (slug) — how it governs this work.
- CONTEXT.md#section — canonical term reference.
```

After the revised final prompt, save it to disk (see `## File Output`), then add only these two lines:

```markdown
Saved to: <relative path written>
Next: pass this final prompt to the `grill-with-docs` skill.
```

Keep the final prompt spartan. No commentary. No preface. No filler.

## File Output

Save the final artifact to disk so the rest of the feature pipeline (`grill-with-docs`, `to-prd`, `to-issues`, `release-notes`) can pick it up by path.

### Path

```
docs/adr/NNNN-<feature-slug>-prompt.md
```

The prompt lives in the same folder and uses the same numbering sequence as ADRs (see `grill-with-docs/ADR-FORMAT.md`). The `-prompt` suffix is the type discriminator — ADRs have no suffix, prompts get `-prompt`, release notes get `-release-notes`, etc. Numbers are shared across all artifact types so the folder reads chronologically.

- **`docs/adr/`** — at the repo root for single-context repos. For multi-context repos (a root `CONTEXT-MAP.md` exists), use the `docs/adr/` directory of the context this work belongs to (e.g. `src/ordering/docs/adr/`). Mirror whatever convention `grill-with-docs` would use for an ADR on the same topic.
- **`NNNN`** — four-digit sequential. Scan `docs/adr/` for the highest existing number (across all artifact types — ADRs, prompts, release notes) and increment by one.
- **`<feature-slug>`** — kebab-case derived from `Need`, ≤ 4 words, ASCII only. Example: "Add password login for Customers" → `password-login`. Confirm the slug with the user before writing.
- **`-prompt`** — fixed suffix.

Example: `docs/adr/0042-password-login-prompt.md`

### Multi-project features

If `Projects:` lists more than one and they live in separate `docs/adr/` directories:

- Default to writing one shared artifact at the repo-root `docs/adr/`.
- Ask the user once whether they prefer per-project copies. If yes, write each copy under that project's local `docs/adr/`, each with its own number from that folder's sequence.

### Conflict handling

- If `docs/adr/` does not exist, create it lazily.
- If a file with the chosen number already exists, recompute the next number — never overwrite a number assigned to another artifact.
- If a prior `*-prompt.md` exists for the same slug and is unchanged from a prior run of this skill, overwrite in place (keep the same number).
- If it exists and contains hand-edits, show the diff and ask the user whether to overwrite, write a new numbered revision, or abort.
- Never delete unrelated files in `docs/adr/`.

### What to write

The file body is exactly the revised final prompt — the same spartan markdown shown to the user. Do not add a preface, commentary, or "generated by" header. The file must be drop-in usable as input to `grill-with-docs`.

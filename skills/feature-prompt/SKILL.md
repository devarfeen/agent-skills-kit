---
name: feature-prompt
description: Use when the user wants to turn a feature idea, change request, or rough requirement into a small prompt for grill-with-docs. When cheap repo exploration reveals domain terms missing from or stale in CONTEXT.md, surface those candidate terms for user approval before any context update.
---

# Feature Prompt

Turn a rough feature request into a minimal, drop-in prompt for `grill-with-docs`.

This skill does not create an implementation spec. It creates the smallest useful handoff for the next step. `grill-with-docs` will challenge the plan, inspect code/docs when needed, sharpen domain terms, update `CONTEXT.md`, and offer ADRs only for hard decisions.

## Output Contract

Final prompts use this shape:

```markdown
Project:
[Full Project Matrix code, repo, path, or context. Use one line.]

What is needed:
[The change to make. One short paragraph or 2-4 bullets.]

Why it is needed:
[The problem, user pain, business reason, or workflow gap.]

Expected end result:
[Observable done state. Prefer user-visible behavior, passing checks, or demo flow.]

Known limits:
[Conditional. Hard constraints, non-goals, compatibility needs, or exclusions already known.]

Open questions:
[Conditional. Real unresolved questions for grill-with-docs to attack.]
```

Only `Project`, `What is needed`, `Why it is needed`, and `Expected end result` are normal sections. Emit `Known limits` and `Open questions` only when useful.

## Why These Sections

- **Project:** Routes the next skill to the right repo, context, or project code. When a Project Matrix code exists, use the full code exactly as written.
- **What is needed:** Defines the requested change.
- **Why it is needed:** Gives motivation so `grill-with-docs` can challenge tradeoffs instead of only wording.
- **Expected end result:** Defines success in observable terms. This becomes the seed for later acceptance criteria.
- **Known limits:** Preserves hard boundaries without forcing a full constraints section.
- **Open questions:** Hands uncertainty to `grill-with-docs` instead of pretending the prompt is complete.

## Rules

- Start from free-form intake. Accept a sentence, paragraph, bullet list, or brain dump.
- Infer first. Ask only when `What is needed` is unclear or project/context cannot be inferred safely.
- Use repo evidence when cheap: project matrix, cwd, `CONTEXT.md`, `CONTEXT-MAP.md`, and ADR names. Do not run a broad code scan by default.
- If memtrace MCP tools are available, run one `memory_recall` query using the feature nouns before drafting. Use results only as hints and confirm with local evidence before including them.
- If cheap repo evidence or user-requested code exploration reveals domain terms that are missing from or stale in `CONTEXT.md`, show a short candidate list before finalizing the prompt.
- Use the full Project Matrix code in the final prompt whenever one exists. Never abbreviate project codes or invent shorthand.
- Do not create `Domain terms`, `Decisions`, `Dependents`, `Risks`, `Doc anchors`, `Integration`, `Constraints`, or `Acceptance` sections. Fold useful facts into the six sections above.
- Keep domain words intact. Do not invent glossary definitions; `grill-with-docs` owns that.
- If the user states a hard decision or limit, preserve it under `Known limits`.
- If a decision is unclear, preserve it under `Open questions`.
- Do not implement the feature. Do not create a PRD. Do not edit ADRs.
- Do not edit `CONTEXT.md` while drafting the prompt. `CONTEXT.md` edits are allowed only as a separate, explicit follow-up after the user approves specific candidate terms or accepts the full candidate list.
- Keep the final prompt spartan, direct, and plain English. The final prompt is a generated artifact and must not be caveman-compressed.

## Candidate Context Terms

Use this only when code or local docs reveal terminology that may be missing from or stale in `CONTEXT.md`. Do not run extra exploration solely to fill this section.

Candidate terms should be meaningful to product or domain experts: roles, workflows, states, business rules, events, integrations, user-facing concepts, or project-specific names. Skip generic programming terms, helper names, low-level class names, and package names unless they carry domain meaning.

Before finalizing the prompt, show the user a compact review:

```markdown
Candidate CONTEXT.md terms:
- `Term` — suggested action; short description; evidence; why it matters.

Reply with the term names to approve, wording changes, `approve all`, or `skip context updates`.
```

If the user approves context updates:

1. Inspect the target `CONTEXT.md` structure and preserve its style.
2. Apply only the approved additions, clarifications, renames, or deprecations.
3. Keep descriptions short and evidence-backed.
4. Report the edited `CONTEXT.md` path before saving the final prompt.

Do not add a `Domain terms` section to the generated prompt. If terms still need `grill-with-docs` review, preserve that uncertainty under `Open questions`.

## Agent Use

When the runtime supports subagents and the user has allowed them, use read-only agents only for fast, independent context checks. Keep the main session responsible for judgment and final wording. Do not use worker agents or make code edits.

If `Understand-Anything` skills are installed and the request targets a large or unfamiliar repo, optionally run `/understand` before drafting to improve terminology and architecture framing. Treat this as optional acceleration, not a hard gate.

## Final Output

Once the minimal prompt is clear:

1. Draft the final prompt.
2. For non-trivial or inferred prompts, show it once for correction.
3. If candidate context terms were found, show them for approval and apply only approved `CONTEXT.md` updates.
4. Save the final prompt to disk.
5. Add only:

```markdown
Context updated: <relative CONTEXT.md path> [only if edited]
Saved to: <relative path written>
Next: pass this final prompt to the `grill-with-docs` skill.
```

## File Output

Save the final artifact so `grill-with-docs`, `to-prd`, `to-issues`, and `release-notes` can pick it up by path.

### Path

```text
<artifacts-root>/docs/prompts/NNNN-<feature-slug>-prompt.md
```

Prompts live in `docs/prompts/`, a sibling of `docs/adr/`. Prompt and ADR filenames both start with the same four-digit `NNNN-<slug>` shape; prompts add the `-prompt` suffix to mark the artifact type. Prompts and ADRs share one `NNNN` number sequence. Release notes are on-demand artifacts under `docs/release-notes/` and do not use this sequence.

#### Resolve `<artifacts-root>`

1. **VS Code workspace:** If a `*.code-workspace` file is found at or above cwd, write to the directory containing it.
2. **Multi-context repo:** If no workspace exists but root `CONTEXT-MAP.md` exists, write to the relevant context's `docs/prompts/`.
3. **Single repo:** Fall back to repo root `docs/prompts/`.

Use the same `<artifacts-root>` for numbering. Scan `<artifacts-root>/docs/adr/` and `<artifacts-root>/docs/prompts/` for the highest existing number, then increment by one.

- **`NNNN`:** four-digit sequence shared across prompt and ADR artifacts only.
- **`<feature-slug>`:** kebab-case from `What is needed`, max 4 words, ASCII only.
- **`-prompt`:** fixed suffix.

### Conflict Handling

- Create `docs/prompts/` lazily.
- Never overwrite a number already used by another artifact.
- If an unchanged prior `*-prompt.md` exists for the same slug, overwrite in place.
- If a same-slug prompt has hand edits, show the diff and ask whether to overwrite, write a new numbered revision, or abort.
- Never delete unrelated files.

### File Body

Write exactly the final prompt body. No preface. No "generated by" header. The file must be drop-in usable as input to `grill-with-docs`.

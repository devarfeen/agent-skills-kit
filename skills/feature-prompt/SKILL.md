---
name: feature-prompt
description: Use when the user wants to turn a feature idea, change request, or rough requirement into a precise feature-development prompt for one or more codebase projects.
---

# Feature Prompt

Turn rough feature requests into implementation-ready prompts.

Main session style: free-form intake first, targeted follow-ups only when needed. Accept whatever the user gives you — a sentence, a paragraph, a brain dump — parse it into the section structure, infer what you can from cwd and a code scan, and ask focused questions only for the parts that are genuinely missing or ambiguous.

Keep the final prompt terse, exact, and free of filler — but write it in plain English. The final prompt is a generated artifact and must not be caveman-compressed, even when caveman mode is active for chat.

Save the final prompt to `docs/prompt/NNNN-<feature-slug>-prompt.md` (see `## File Output`), then ask the user to pass it to the `grill-with-docs` skill. A draft → review round is optional — offer it for non-trivial prompts, skip it when the inputs were already clean.

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

These are the sections the final prompt can contain. Only `Need` is hard-required from the user. Everything else: try to infer from the intake text, cwd, project matrix, and a quick code scan first; ask the user only when inference is weak or the choice is genuinely product-judgment. Conditional sections are emitted only when they have content.

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

- Start with free-form intake. Accept whatever the user gives — a sentence, a paragraph, a bullet list, a brain dump. Parse it into the sections yourself before asking anything.
- `Need` is the only hard-required field. If the intake doesn't make `Need` clear, ask one direct question for it.
- Infer the rest first, ask second. `Projects` from cwd + project matrix; `Integration` from a code scan against the symbols/files implied by `Need`; `Reason` from context if obvious; `Constraints` from CONTEXT.md / ADRs / language-level rules.
- Show the user what you inferred and let them correct in one pass — don't loop section-by-section unless the user wants that.
- Only ask a follow-up when (a) a required field is still ambiguous, (b) inference would be a guess about product intent, or (c) the user's wording conflicts with a canonical term in CONTEXT.md.
- Conditional sections (`Domain terms`, `Decisions`, `Dependents`, `Risks`, `Doc anchors`) are auto-derived from scans, never asked as standalone questions. Surface them in the draft and let the user prune.
- `Dependents` is populated from the codebase scan after `Integration` is known. Only escalate to confirm scope on specific callers.
- In `Need` and `Integration`, **bold** domain-vocabulary terms (Customer, Order, Invoice). Do not bold generic engineering terms (timeout, retry, cache).
- `Acceptance` criteria, when present, must be evidence-based — passing test, observable behavior, or demoable flow. If the user skips it, infer from `Need` + `Integration` + `Reason` and mark inferred.
- When you do need to ask a question, prefer a direct open question. Multiple-choice options are an aid for when the user seems stuck or the answer space is small and known — not a mandatory format. If you use options, keep them short and always allow a custom answer.
- If codebase inspection can answer or improve a section, inspect first, then ask the user to confirm only if it matters.
- Preserve any section order the user implies. Do not add sections beyond those listed above unless the user asks.
- Do not implement the feature. Do not create a plan unless the user asks.

## Final Output

Once `Need` is clear and the inferred sections look right:

1. Draft the generated prompt using the resolved sections.
2. For non-trivial prompts, show the draft to the user once and ask if anything needs changing. For simple, clearly-stated requests where every section is high-confidence, skip the review and go straight to saving. When in doubt, show the draft.
3. Apply any user feedback without adding sections beyond those listed.
4. Produce only the final prompt. Include `Domain terms`, `Decisions`, `Dependents`, `Risks`, and `Doc anchors` only when they have content — drop the heading otherwise.

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
<artifacts-root>/docs/prompt/NNNN-<feature-slug>-prompt.md
```

Prompts live in `docs/prompt/` — a sibling of `docs/adr/`, not inside it. The two folders share a single numbering sequence: a prompt and an ADR will never carry the same `NNNN`. The `-prompt` suffix is kept as a type discriminator so the filename is self-describing when referenced from elsewhere.

#### Resolving `<artifacts-root>`

Avoid scattering artifacts into project repos when a workspace exists. Resolve in this order:

1. **VS Code workspace (preferred when present).** If a `*.code-workspace` file is found at or above the cwd, write to the directory containing it (the meta-workspace location — same place the workspace folder with `path: "."` resolves to in `agents-md`). All ADRs, prompts, and release notes for every project in the workspace live here. Example: `<workspace-dir>/docs/prompt/0042-…-prompt.md`.
2. **Multi-context single repo.** If no workspace file but a root `CONTEXT-MAP.md` exists, use the `docs/prompt/` directory of the context this work belongs to (e.g. `src/ordering/docs/prompt/`).
3. **Single-repo project.** Fall back to the repo root: `docs/prompt/NNNN-…-prompt.md`.

Use the same `<artifacts-root>` for the numbering scan — pick the next `NNNN` from `<artifacts-root>/docs/adr/` ∪ `<artifacts-root>/docs/prompt/`.

- **`NNNN`** — four-digit sequential. Scan **both** `<artifacts-root>/docs/adr/` and `<artifacts-root>/docs/prompt/` for the highest existing number across all artifact types (ADRs, prompts, release notes), then increment by one. Numbering is shared across types so the folders read chronologically when merged.
- **`<feature-slug>`** — kebab-case derived from `Need`, ≤ 4 words, ASCII only. Example: "Add password login for Customers" → `password-login`. Confirm the slug with the user before writing.
- **`-prompt`** — fixed suffix.

Example (workspace mode): `<workspace-dir>/docs/prompt/0042-password-login-prompt.md`
Example (single repo): `docs/prompt/0042-password-login-prompt.md`

### Multi-project features

When the workspace path applies, multi-project features are a non-issue: there is one `docs/prompt/` at the workspace root and every project shares it. Project codes inside the prompt's `Projects:` line do the disambiguation.

Only when `<artifacts-root>` resolves to a per-context or per-repo location should you consider per-project copies. In that case:

- Default to writing one shared artifact at the highest common `<artifacts-root>`.
- Ask the user once whether they prefer per-project copies. If yes, write each copy under that project's local `docs/prompt/`, each with its own number from that folder's sequence.

### Conflict handling

- If `<artifacts-root>/docs/prompt/` does not exist, create it lazily.
- If a file with the chosen number already exists in `<artifacts-root>/docs/prompt/` **or** in `<artifacts-root>/docs/adr/` (or any other sibling artifact folder), recompute the next number — never overwrite a number assigned to another artifact, even across folders.
- If a prior `*-prompt.md` exists for the same slug and is unchanged from a prior run of this skill, overwrite in place (keep the same number).
- If it exists and contains hand-edits, show the diff and ask the user whether to overwrite, write a new numbered revision, or abort.
- Never delete unrelated files in `docs/prompt/`.

### What to write

The file body is exactly the revised final prompt — the same spartan markdown shown to the user. Do not add a preface, commentary, or "generated by" header. The file must be drop-in usable as input to `grill-with-docs`.

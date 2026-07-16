---
name: feature-prompt
disable-model-invocation: true
description: "Use when the user wants to turn a feature idea, change request, or rough requirement into a small prompt for grill-with-docs. When cheap repo exploration reveals domain terms missing from or stale in CONTEXT.md, surface those candidate terms for user approval before any context update. Post-decision artifacts route onward instead: turning an ADR into a spec (PRD) is /to-spec, and investigating how existing behaviour works is /feature-discovery."
---

# Feature Prompt

Feature-prompt turns a rough feature request into a minimal, drop-in prompt for
`grill-with-docs`.

This skill does not create an implementation spec. It creates the smallest
useful handoff for the next step. `grill-with-docs` will challenge the plan,
inspect code/docs when needed, sharpen domain terms, update `CONTEXT.md`, and
offer ADRs only for hard decisions.

## Output Contract

Final prompts use this shape:

```markdown
Project:
[Full Project Matrix code, repo, path, or context. Use one line.]

What is needed:
[The change to make. One short paragraph or 2-4 bullets.]

Why it is needed:
[The problem, user pain, business reason, or workflow gap — so grill-with-docs
can challenge tradeoffs, not just wording.]

Expected end result:
[Observable done state. Prefer user-visible behavior, passing checks, or a
demo flow. This seeds the later acceptance criteria.]

Known limits:
[Conditional. Hard constraints, non-goals, compatibility needs, or exclusions
already known. When broad intake was split, list the deferred slices here as
explicit non-goals so the scoping decision survives in the artifact.]

Open questions:
[Conditional. Real unresolved questions for grill-with-docs to attack. Keep
this short and high-leverage.]
```

Only `Project`, `What is needed`, `Why it is needed`, and `Expected end result`
are normal sections. Emit `Known limits` and `Open questions` only when useful.

## Rules

### Intake and inference

- Start from free-form intake: a sentence, paragraph, bullet list, or brain dump.
- Infer first. Ask only when `What is needed` is unclear or project/context
  cannot be inferred safely.
- Use repo evidence when cheap: Project Matrix, cwd, `CONTEXT.md`,
  `CONTEXT-MAP.md`, and ADR names. Do not run a broad code scan by default.
  A graphify knowledge base counts as cheap evidence when one exists —
  `graphify-out/graph.json` at the project root, else at the workspace root;
  missing in both places → skip graphify. If the graph is older than ~7 days,
  say so and recommend the user run `graphify update .`.

### Scope and slicing

- Before drafting, apply the fog test: can you state the destination in one
  line *and* name every open decision as a sharp question, right now? If not,
  stop and suggest `/wayfinder` — it charts those decisions as tracker tickets
  and resolves them one per session. Do not write a PR-sized prompt for foggy
  work. Fog, not size, is the test: a large mechanical change with nothing left
  to decide is not fog.
- Default to one thin vertical slice, small enough to review and merge
  independently. Broad intake gets split: draft this prompt for slice 1 only —
  the contract's `Known limits` bracket owns recording the deferred slices.
- If this prompt would force a very long grilling session, say so and ask to
  split scope before finalizing. If the user is away, split it yourself: draft
  slice 1, defer the rest via `Known limits`, and note the split at the top of
  the response.
- When the user intends parallel agent threads, split slices to minimize
  shared-file coupling.

### Context and evidence

- Use the full Project Matrix code verbatim whenever one exists. Never
  abbreviate project codes or invent shorthand.
- Prefer code-as-truth language: reference existing files/modules/seams when
  known, and keep "reuse existing seam vs create new seam" under
  `Open questions` explicitly — it is how duplicate logic gets prevented.
- Include only non-obvious context: constraints, architecture quirks, and
  domain rules the model cannot infer cheaply from repo scans. Omit stack
  facts the code already shows.
- If dependency internals are central and unclear, suggest fetching targeted
  source (e.g. `opensrc`) as a follow-up context step before deep grilling.
- Keep domain words intact. Do not invent glossary definitions;
  `grill-with-docs` owns that.

### Questions and output discipline

- Do not create `Domain terms`, `Decisions`, `Dependents`, `Risks`,
  `Doc anchors`, `Integration`, `Constraints`, or `Acceptance` sections. Fold
  useful facts into the six contract sections; user-stated hard decisions go
  under `Known limits`.
- Classify unclear decisions by fidelity: both kinds land under
  `Open questions`, but ungrillable ones ("needs to feel/see it") also route to
  `/handoff` + `/prototype` before deep grilling continues.
- Keep `Open questions` to the highest-leverage unknowns (usually 1-5). Drop
  trivia that can be decided during implementation.
- Do not implement the feature, create a spec, or edit ADRs. `CONTEXT.md`
  changes happen only through the approved candidate-terms flow below.
- Keep the final prompt spartan, direct, plain English — it is a generated
  artifact, never compressed shorthand.

## Candidate Context Terms

Only when cheap repo evidence or user-requested exploration reveals domain
terms missing from or stale in `CONTEXT.md` — never run extra exploration just
to fill this. The shared flow — what qualifies as a candidate, how to present
the list, the away-fallback, and how to apply approvals — lives in
[`references/context-terms.md`](references/context-terms.md). Show candidates
before finalizing the prompt, apply only approved updates, and report the
edited path before saving. Terms still needing review stay under
`Open questions`.

## Agent Use

When the runtime supports subagents and the user has allowed them, use
read-only agents only for fast, independent context checks. No worker agents,
no code edits. Announce how many are running and report each as it completes.

## Final Output

1. Draft the final prompt.
2. For non-trivial or inferred prompts, show it once for correction. If the
   user is away, save it as drafted and note at the top of the response that
   it is unconfirmed.
3. If candidate context terms were found, run the shared approval flow.
4. Verify the pre-save checklist. Save the final prompt to the path below.
   Re-open the saved file and confirm its sections and path match the approved
   draft before the reply reports it.
5. Add only:

```markdown
Context updated: <relative CONTEXT.md path> [only if edited]
Saved to: <relative path written>
Next: pass this final prompt to the `grill-with-docs` skill.
Suggested next skills (optional):

- /grill-with-docs: challenge assumptions, sharpen domain terms, and confirm decisions.
- /handoff + /prototype: when open questions are ungrillable and need a higher-fidelity spike.
- /to-spec: if this needs a formal spec (PRD) after grilling.
```

## File Output

### Path

```text
<artifacts-root>/specs/prompts/NNNN-<feature-slug>-prompt.md
```

Resolve `<artifacts-root>`: (1) the directory containing a `*.code-workspace`
file at or above cwd; (2) the per-context root in a multi-context repo
(`CONTEXT-MAP.md` at root); (3) the single repo root.

- **`NNNN`** — scan `<artifacts-root>/specs/adr/` and
  `<artifacts-root>/specs/prompts/` for the highest existing four-digit number
  and increment. This keeps prompt numbers
  from colliding with existing ADRs. ADRs are numbered independently by
  `grill-with-docs` from `specs/adr/` alone, so the ADR born from this prompt
  may carry a different number — the prompt path recorded in the ADR is the
  link, not the number.
- **`<feature-slug>`** — kebab-case from `What is needed`, max 4 words, ASCII.
- **`-prompt`** — fixed suffix marking the artifact type.

### Conflict handling

- Create `specs/prompts/` lazily. Never overwrite a number already used by
  another artifact. Never delete unrelated files.
- A prior same-slug prompt counts as **hand-edited** when git shows commits or
  working-tree changes to it that this session didn't make; if git can't tell
  (untracked file), assume hand-edited.
- Unchanged prior same-slug prompt → overwrite in place. Hand-edited → show
  the diff and ask: overwrite, new numbered revision, or abort. If the user is
  away, write a new numbered revision — never overwrite hand edits unconfirmed.

### File body

Write exactly the final prompt body. No preface, no generated-by header. The
file must be drop-in usable as input to `grill-with-docs`.

### Pre-save checklist

- [ ] Only the six allowed section headers appear, in contract order
- [ ] `Project:` names the full Project Matrix code verbatim (when one exists)
- [ ] `NNNN` unique across `specs/adr/` and `specs/prompts/`; slug ≤ 4 words,
      kebab-case ASCII, `-prompt` suffix
- [ ] Split intake: deferred slices recorded under `Known limits`
- [ ] File body is the prompt only — drop-in, no preface

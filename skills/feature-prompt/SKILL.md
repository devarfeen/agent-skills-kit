---
name: feature-prompt
disable-model-invocation: true
description: "Use when the user wants to turn a feature idea, change request, or rough requirement into a small prompt for grill-with-docs. When cheap repo exploration reveals domain terms missing from or stale in CONTEXT.md, surface those candidate terms for user approval before any context update. Post-decision artifacts route onward instead: turning an ADR into a spec (PRD) is /to-spec, and investigating how existing behaviour works is /feature-discovery."
---

# feature-prompt

Produces the smallest useful handoff for the next step — not an implementation
spec. `grill-with-docs` will challenge the plan, sharpen domain terms, update
`CONTEXT.md`, and offer ADRs only for hard decisions.

## Output contract

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
demo flow; seeds the later acceptance criteria.]

Known limits:
[Conditional. Hard constraints, non-goals, compatibility needs, or exclusions
already known. When intake was split, list the deferred slices as explicit
non-goals so the scoping decision survives in the artifact.]

Open questions:
[Conditional. Real unresolved questions for grill-with-docs to attack.]
```

Emit `Known limits` and `Open questions` only when useful; the other four
sections are always present.

## Rules

### Intake and inference

- Start from free-form intake. Infer first; ask only when `What is needed` is
  unclear or project/context cannot be inferred safely.
- Use repo evidence when cheap: Project Matrix, cwd, `CONTEXT.md`,
  `CONTEXT-MAP.md`, and ADR names. Do not run a broad code scan by default.
- If `graphify-out/graph.json` exists (project root, else workspace root), query it before raw search; older than ~7 days → suggest `graphify update .`; missing → skip graphify.

### Scope and slicing

- Before drafting, apply the fog test: can you state the destination in one
  line *and* name every open decision as a sharp question, right now? If not,
  stop and suggest `/wayfinder` — it charts those decisions and resolves them
  one per session. Do not write a PR-sized prompt for foggy
  work. Fog, not size, is the test: a large mechanical change with nothing left
  to decide is not fog.
- Default to one thin vertical slice, small enough to review and merge
  independently. Broad intake gets split: draft this prompt for slice 1 only;
  `Known limits` records the deferred slices. A prompt that would force a very
  long grilling session → ask to split scope before finalizing; user away →
  split it yourself and note the split at the top of the response.
- When the user intends parallel agent threads, split slices to minimize
  shared-file coupling.

### Context and evidence

- Use the full Project Matrix code verbatim whenever one exists. Never
  abbreviate project codes or invent shorthand.
- Reference existing files/modules/seams when known, and keep "reuse existing
  seam vs create new seam" under `Open questions` explicitly — it is how
  duplicate logic gets prevented.
- Include only non-obvious context: constraints, architecture quirks, and
  domain rules the model cannot infer cheaply from repo scans. Omit stack
  facts the code already shows.
- Dependency internals central and unclear → suggest fetching targeted source
  (e.g. `opensrc`) as a follow-up context step before deep grilling.
- Keep domain words intact. Do not invent glossary definitions;
  `grill-with-docs` owns that.

### Questions and output discipline

- Do not create `Domain terms`, `Decisions`, `Dependents`, `Risks`,
  `Doc anchors`, `Integration`, `Constraints`, or `Acceptance` sections. Fold
  useful facts into the six contract sections; user-stated hard decisions go
  under `Known limits`.
- All unclear decisions land under `Open questions`; ungrillable ones ("needs
  to feel/see it") also route to `/handoff` + `/prototype` before deep grilling
  continues.
- Keep `Open questions` to the highest-leverage unknowns (usually 1-5). Drop
  trivia that can be decided during implementation.
- A vague answer to a sharp question ("as fast as possible", "all users") is
  not an answer — ask once for a number or a named segment; still vague →
  park it under `Open questions` as written.
- Do not implement the feature, create a spec, or edit ADRs. `CONTEXT.md`
  changes happen only through the approved candidate-terms flow below.
- Keep the final prompt spartan, direct, plain English — it is a generated
  artifact, never compressed shorthand.

## Candidate context terms

Only when cheap repo evidence or user-requested exploration reveals domain
terms missing from or stale in `CONTEXT.md` — never run extra exploration just
to fill this. The shared flow — what qualifies, presentation, the
away-fallback, applying approvals — lives in
[`references/context-terms.md`](references/context-terms.md). Show candidates
before finalizing the prompt, apply only approved updates, and report the
edited path before saving. Terms still needing review stay under
`Open questions`.

## Agent use

Sub-agents: dispatch local lanes automatically for independent work — never cloud agents; announce the lane count at dispatch and report each lane as it completes. Lanes are for fast, independent context checks only — no worker agents, no code edits.

## Final output

1. Draft the final prompt.
2. For non-trivial or inferred prompts, show it once for correction. User
   away → save as drafted and note at the top that it is unconfirmed.
3. If candidate context terms were found, run the shared approval flow.
4. Verify the pre-save checklist and save to the path below, then re-open the
   saved file and confirm sections and path match the approved draft before
   reporting.
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

## File output

### Path

```text
<artifacts-root>/specs/prompts/NNNN-<feature-slug>-prompt.md
```

Resolve `<artifacts-root>`: the `*.code-workspace` directory if one exists, else the per-context root (`CONTEXT-MAP.md` at repo root), else the repo root.

- **`NNNN`** — scan `<artifacts-root>/specs/adr/` and `specs/prompts/` for the
  highest existing four-digit number and increment, so prompt numbers never
  collide with ADRs. ADRs are numbered independently from `specs/adr/` alone;
  the prompt path recorded in the ADR is the link, not the number.
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

Write exactly the final prompt body — no preface, no generated-by header —
drop-in usable as input to `grill-with-docs`.

### Pre-save checklist

- [ ] Only the six allowed section headers appear, in contract order
- [ ] `Project:` names the full Project Matrix code verbatim (when one exists)
- [ ] `NNNN` unique across `specs/adr/` and `specs/prompts/`; slug ≤ 4 words,
      kebab-case ASCII, `-prompt` suffix
- [ ] Split intake: deferred slices recorded under `Known limits`
- [ ] File body is the prompt only — drop-in, no preface

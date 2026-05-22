---
name: ubiquitous-language
description: "DEPRECATED — kept for reference only. Domain-language sharpening is now covered by Matt Pocock's grill-with-docs, which updates CONTEXT.md and ADRs inline. Only invoke if the user explicitly asks to maintain a legacy UBIQUITOUS_LANGUAGE.md file."
---

# Ubiquitous Language (Deprecated)

> **Deprecated.** This skill is retained in `skills/` for historical
> reference. Domain-language sharpening should now happen inline via
> `grill-with-docs`, which writes to `CONTEXT.md` and ADRs as decisions
> crystallise. Only run this skill if the user explicitly asks to update an
> existing legacy `UBIQUITOUS_LANGUAGE.md`.

Create or update a DDD-style glossary of domain terms in `UBIQUITOUS_LANGUAGE.md`.

Inspired by Matt Pocock's deprecated `ubiquitous-language` skill, MIT License, Copyright 2026 Matt Pocock:
https://github.com/mattpocock/skills/blob/main/skills/deprecated/ubiquitous-language/SKILL.md

## Process

1. Read the current conversation and extract domain-relevant nouns, verbs, roles, lifecycle states, workflows, and business concepts.
2. If `UBIQUITOUS_LANGUAGE.md` already exists in the working directory, read it first and update it rather than replacing it blindly.
3. Inspect nearby domain docs when useful: `CONTEXT.md`, `CONTEXT-MAP.md`, `docs/`, `docs/adr/`, `specs/`, and README files.
4. Detect terminology problems:
   - one word used for multiple concepts
   - multiple words used for one concept
   - vague, overloaded, or implementation-shaped terms
   - code names that should not leak into the domain language
5. Pick canonical terms. Be opinionated when the evidence is strong.
6. Write or update `UBIQUITOUS_LANGUAGE.md`.
7. Return a short summary of terms added, terms renamed, ambiguities flagged, and open questions.

Do not run an interview before writing the first draft. If something is unclear, document it in `Open Questions`.

## File Format

Use this structure:

```markdown
# Ubiquitous Language

## [Domain Area]

| Term | Definition | Aliases to avoid | Notes |
| --- | --- | --- | --- |
| **Canonical Term** | One-sentence definition. | Old name, vague synonym | Clarification or boundary note. |

## Relationships

- A **Term** belongs to exactly one **Other Term**.
- A **Workflow** moves from **State A** to **State B** when [domain event].

## Example Dialogue

> Dev: "Question using canonical terms?"
>
> Domain expert: "Answer using canonical terms and clarifying boundaries."

## Flagged Ambiguities

- `term` was used to mean both **Concept A** and **Concept B**. Prefer **Concept A** when [condition], and **Concept B** when [condition].

## Open Questions

- [Question that needs a domain expert decision.]
```

## Rules

- Include only terms meaningful to domain experts.
- Skip generic programming terms unless the term has domain meaning in this project.
- Include operational short codes and abbreviations when domain users use them, such as `DN` for **Delivery Note**.
- Do not treat an abbreviation as a separate concept when it is only a short name for a canonical term. Put it in `Aliases to avoid` or `Notes`.
- Include virtual business concepts when users rely on them operationally, even if they are not physical things.
- Do not include file paths, class names, or package names unless they are also real domain terms.
- Keep definitions to one sentence.
- Define what the term is, not how it is implemented.
- Group terms into natural domain areas when there are enough terms.
- Use a single table if the domain is still small.
- Use bold formatting for canonical terms in relationships and dialogue.
- In `Aliases to avoid`, list words that should not be used for that concept.
- If two terms are truly distinct, explain the boundary in `Notes` or `Flagged Ambiguities`.
- Do not invent business rules. Mark uncertain relationships as open questions.
- End non-trivial responses with `Suggested next skills (optional)` using 1-3 advisory suggestions only (no gating).

## Examples

Use examples like these as shape guidance. Do not copy them unless they match the current project.

```markdown
## Logistics

| Term | Definition | Aliases to avoid | Notes |
| --- | --- | --- | --- |
| **Delivery Note** | A document that records goods delivered for a job, order, or shipment. | DN | `DN` is a short code, not a separate concept. |
| **Warehouse On Site** | A warehouse location or stock area that exists at an operational site. | WON | `WON` is a short code; confirm whether it means a place, a status, or both. |
| **Operational File** | A virtual folder used to group job-related documents, notes, and records. | File, physical folder | This is not necessarily a filesystem directory or physical file. |
```

Example relationships:

```markdown
- A **Delivery Note** belongs to one **Job** or **Shipment**.
- An **Operational File** groups the documents and records needed to complete a **Job**.
- A **Warehouse On Site** may hold stock for one or more active operational workflows.
```

Example ambiguity:

```markdown
- `File` may mean either an **Operational File** in the business workflow or a technical filesystem file. Use **Operational File** for the business concept.
```

## Re-Running

When invoked again:

1. Preserve stable accepted terms unless new context clearly invalidates them.
2. Add new terms from the conversation or local docs.
3. Tighten definitions that were previously vague.
4. Move resolved ambiguities into canonical terms or notes.
5. Keep unresolved ambiguities visible.

## Final Response

After writing `UBIQUITOUS_LANGUAGE.md`, respond with:

```markdown
Updated `UBIQUITOUS_LANGUAGE.md`.

Added:
- [Term]

Changed:
- [Term or "None"]

Flagged:
- [Ambiguity or "None"]

Open questions:
- [Question or "None"]

Suggested next skills (optional):
- /grill-with-docs: continue domain-language sharpening in `CONTEXT.md` and ADRs.
```

# Language and output shapes

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Load when defining or changing emitted text, templates, or examples.

## Voice and language

- Imperative, present tense. Sentence-case headings ("Trigger discipline", not "Trigger Discipline").
- Say each fact once per file. The description states identity; the body never re-narrates it.
- Prefer a leading word over a restated triad ("Decisions are **artifacts**", "stop signal", "evidence") — one pretrained concept the agent thinks with.
- One example per pattern. Good/bad pairs only where the distinction is the lesson.
- No invented abbreviations or arrow-chain prose in agent-facing output rules; arrows as notation inside instruction text are fine.
- One-clause rationale after a rule is house style ("dead routing rules cost every session tokens"); paragraph-length justification is not.

## Output caps

Every surface where the agent emits text carries an explicit bound:

- Reports: ≤3 bullets per section unless the section justifies more in its own text.
- Evidence: quote the shortest decisive tail (the pass/fail line and counts); link or name the rest.
- `Suggested next skills (optional)` footer: 1–3 items, advisory, never gating.
- Phase updates: one line per field.
- Interviews: one question at a time, leading with the recommended answer so the user can accept it in a word.

Caps never omit affected behaviors, evidence, or unresolved blockers. Put longer required detail in a linked artifact.

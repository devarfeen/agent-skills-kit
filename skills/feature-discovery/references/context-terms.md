# Candidate GLOSSARY.md Terms — shared flow

Shared between `feature-discovery` and `feature-prompt` (duplicated by design so
each skill installs self-contained; `tools/validate.sh` enforces byte-parity —
edit both copies together). How to surface domain terms that code evidence
suggests are missing from or stale in `GLOSSARY.md`, and how to apply approved
updates.

`GLOSSARY.md` was named `CONTEXT.md` before the upstream rename. Where only the
legacy file exists, read it as the glossary, name it by its real path in every
report line, and recommend `git mv CONTEXT.md GLOSSARY.md` — never rename it
here.

Zero attribution: never add or leave co-author, AI, or tool attribution in any output. Keep this rule explicit in any `GLOSSARY.md` created or updated here.

## What qualifies as a candidate

Candidate terms must be meaningful to product or domain experts: roles,
workflows, states, business rules, events, integrations, user-facing concepts,
or project-specific names. Skip generic programming terms, helper names,
low-level class names, and package names unless they carry domain meaning.
Prefer a small, high-confidence list over a glossary dump.

## Implemented versus intended

Code establishes implemented behavior, not whether an approved business rule
changed. When code and current approved intent disagree, retain the intended
rule and record the implementation discrepancy with separate citations.
Recommend clarification or review, not a replacement that legitimizes a
possible bug. Call context stale only when evidence establishes that its
recorded meaning was superseded.

## Presenting candidates

For each candidate capture: **Term** — suggested action (add, clarify, rename,
deprecate, or ask user); a short description distinguishing implementation from
recorded intent when needed; **Evidence** refs; **Why it matters** for future
planning. For a discrepancy, quote current wording beside the code evidence
and any approved requirement. Then ask:

```markdown
Candidate GLOSSARY.md terms:

- `Term` — suggested action; short description; evidence; why it matters.

Reply with the term names to approve, wording changes, `approve all`, or `skip context updates`.
```

If the user is away, skip all `GLOSSARY.md` updates, keep the candidate list in
the response, and continue with the skill's remaining output. If no candidates
exist, say so in one line — do not pad the section.

## Applying approved updates

1. Inspect the target `GLOSSARY.md` first and preserve its existing structure
   and style.
2. Apply only approved additions, clarifications, renames, or deprecations.
3. Keep descriptions short and evidence-backed; never add implementation-only
   symbols as domain language.
4. Use the user's approved wording. If it presents intended behavior as an
   implemented fact contrary to evidence, explain the distinction and agree
   accurate wording before editing; do not change policy to match the code.
5. Report exactly which terms changed and which file was edited.

If neither `GLOSSARY.md` nor a legacy `CONTEXT.md` exists, still report candidates and recommend
creating or locating the file before editing anything.

---
name: writing-kit-skills
disable-model-invocation: true
description: "House style for authoring and editing skills in this kit — the skeleton, word budget, canonical one-liners, output caps, and eval gates every SKILL.md follows. Use when creating a new kit skill or editing an existing skill's body, references, or description."
---

# writing-kit-skills

A kit skill exists to make an agent take the same process every run. Every rule here serves that predictability at the lowest token cost that still binds weaker CLIs — this kit installs standalone into many runtimes, so redundancy is spent deliberately, never by accident.

## The skeleton

Every SKILL.md follows this order, skipping sections it genuinely doesn't need:

1. **Definitional opener** — one or two sentences stating what the skill produces and the boundary that makes it this skill and not a neighbour. No `## Purpose` heading, no restatement of the frontmatter description.
2. **Inputs** — what must be known before work starts, and the stop-and-ask rule for anything missing.
3. **Rules** — the binding constraints. Each prohibition is paired with the positive action ("Dispatch fires only on explicit user say-so; until then, keep capturing"), and may carry one clause of rationale. No second section restating rules in negated form.
4. **Process / Workflow / Modes** — `### N. Verb-phrase` steps or named modes. Each step ends where an agent can tell done from not-done.
5. **The artifact** (when the skill writes one) — template plus two or three filled sample rows at most; full examples live in `references/`.
6. **Output** — the exact chat surface: templates, caps, and the stop.
7. **Completion criteria** — observable checks only (a path that exists, a command output, a read-back match, a `git status` state). Never checklist items that re-assert body rules; the body already binds them.

## Word budget

A SKILL.md runs **1,000–1,300 words**; 1,500 (frontmatter included) is the validator-enforced ceiling. Over budget → move mechanics and long examples to `references/`; never hit budget by thinning refusal or safety language.

## Voice and language

- Imperative, present tense. Sentence-case headings ("Trigger discipline", not "Trigger Discipline").
- Say each fact once per file. The description states identity; the body never re-narrates it.
- Prefer a leading word over a restated triad ("Decisions are **artifacts**", "stop signal", "evidence") — one pretrained concept the agent thinks with.
- One example per pattern. Good/bad pairs only where the distinction is the lesson.
- No invented abbreviations or arrow-chain prose in agent-facing output rules; arrows as notation inside instruction text are fine.
- One-clause rationale after a rule is house style ("dead routing rules cost every session tokens"); paragraph-length justification is not.

## Canonical one-liners

These five lines are shared kit protocol. Paste them **byte-exact** (validator-enforced); never paraphrase or expand them:

- Resolve `<artifacts-root>`: the `*.code-workspace` directory if one exists, else the per-context root (`CONTEXT-MAP.md` at repo root), else the repo root.
- If `graphify-out/graph.json` exists (project root, else workspace root), query it before raw search; older than ~7 days → suggest `graphify update .`; missing → skip graphify.
- Sub-agents: local lanes only when the user allows them — never cloud agents; announce the lane count at dispatch and report each lane as it completes.
- Name the full PROJECT-CODE from the Project Matrix everywhere; never mix one project's conventions, tokens, or components into another.
- Emit `Stage / Found / Next / Needs user` at each phase transition — one line per field.

## Output caps

Every surface where the agent emits text carries an explicit bound:

- Reports: ≤3 bullets per section unless the section justifies more in its own text.
- Evidence: quote the shortest decisive tail (the pass/fail line and counts); link or name the rest.
- `Suggested next skills (optional)` footer: 1–3 items, advisory, never gating.
- Phase updates: one line per field.
- Interviews: one question at a time, leading with the recommended answer so the user can accept it in a word.

## The auto-clarity valve

Compression never touches: refusal boundaries and scope gates (AGENTS.md rule 7 — they are the safety property), irreversible-action confirmations, and multi-step sequences where terseness would blur order or dependencies. Write those in full prose.

## Frontmatter and gates

- `description:` is the router. Model-invoked skills get identity + one trigger per genuinely distinct branch — synonym stacks are duplication; collapse them. Keep negative-routing clauses ("X routes to /other instead") and legacy aliases (the "(PRD)" spec alias) — they are branches, not synonyms.
- Any `description:` edit or new skill invalidates the eval-provenance snapshot (validate.sh check 10) and requires a user-run trigger-eval sweep plus `score.py --write-snapshot` before it can land. Batch description work; never restamp `last_run` by hand.
- `disable-model-invocation: true` ⇔ `agents/openai.yaml` with `allow_implicit_invocation: false` (cross-runtime parity, validator-enforced).
- Keep any description containing `: ` double-quoted (strict-YAML parse, check 1).

## Failure modes to hunt

**Sediment** — layers that settle because adding feels safe; prune on every edit. **Sprawl** — over budget even when every line is live; cure by disclosure to `references/`, not by thinning safety language. **Duplication** — the same meaning twice in one file (description↔body, rules↔checklist); keep one. **No-op** — a line the agent already obeys by default; delete the sentence, don't trim it.

## Completion criteria

- [ ] `bash tools/validate.sh` passes (or fails only on check 10 when the edit is a batched description/new-skill change awaiting the user's eval sweep)
- [ ] Word count within budget: `awk 'f&&NF{c+=NF} /^---$/{f++}' skills/<name>/SKILL.md` ≤ 1,500
- [ ] Every refusal/stop line present in the previous version is present (or strengthened) in the new one — verified by diff, not recollection
- [ ] Frontmatter untouched unless this is an approved description batch
- [ ] Sync map satisfied: manifest row, README row, duplicated-by-design copies edited together

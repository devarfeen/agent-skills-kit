# Frontier readiness eval

Deep-dive sheet for category 11. A skill is frontier-ready when it is written
for a capable, tool-using, planning model — and would still be correct if a
better model, or a different vendor's model, read it next year.

## The no-op test

Read each sentence and ask: **does this change the model's behavior versus its
default?**

A frontier model already searches before editing, already writes complete
sentences, already tries to be thorough. Sentences that say so are pure token
cost. Delete them; do not trim them.

| No-op (delete) | Load-bearing (keep) |
| :--- | :--- |
| "Use the terminal to run git." | "Stage explicitly by path — never `git add -A`." |
| "Be thorough and careful." | "Completion requires the test command and its quoted output." |
| "Think step by step." | "Cross-check the sub-issue count against the spec before creating any tab — under-fanning silently drops slices." |
| "Read the file before editing it." | "Never paste the prompt into a dead tab's shell, where the text executes as commands." |

The pattern: load-bearing lines name a **constraint, an invariant, or a specific
failure**. No-op lines describe general competence.

## Weak-model relics

Each of these caps the category at 4, and several together at 3 or below.

- **ALL-CAPS walls.** `MUST` / `NEVER` / `IMPORTANT!!!` repeated for emphasis.
  One stated reason ("symptom patches resurface as flakier bugs") outlasts three
  exclamation marks. Bold a short imperative instead.
- **Role-play preambles.** "You are an expert senior engineer with 20 years…"
  buys nothing from a frontier model.
- **Reasoning incantations.** "Take a deep breath", "think step by step",
  "let's work through this carefully."
- **Restated global policy.** The generated `AGENTS.md` already binds
  PROJECT-CODE, local-only orchestration, zero attribution, and honest
  reporting. One reminder line where it prevents real damage is fine. Three
  paragraphs is drift waiting to happen.
- **Vendor lock.** Naming one CLI's flags in the body where the skill is
  otherwise generic. Per-runtime mappings belong in `references/`.

## Hidden owner context

A skill must not assume facts only its author knows: an unnamed internal tool, a
convention that lives in one person's head, a path that exists on one machine.
If a fact is required, state it or point at the file that holds it.

Test: could a competent engineer at another company install this skill standalone
and have it work?

## Explain, don't shout

The kit's house style, and the thing that ages best:

- Open with an identity sentence, not an instruction.
- Rules as bold-lead bullets: a 2–5-word imperative that stands alone, then one
  or two plain sentences.
- State the default flat. Give real exceptions their own named subsection — not
  an "unless" buried mid-sentence.
- **Every prohibition ships its replacement in the next sentence.**
- Phrase gates as "No X, no Y."

## Scoring

- **5** — Every sentence is load-bearing. No relics, no vendor lock, no hidden
  context. Reasons are given, not volume.
- **4** — One relic or a handful of no-op lines.
- **3** — A caps wall, or global policy restated at length, or detail that
  should live in `references/` inflating the always-loaded body.
- **2** — Role-play preamble or reasoning incantations; written for a weak model.
- **1** — Only works for one vendor, or depends on facts nobody else has.

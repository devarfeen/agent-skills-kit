# Contributing

Human-facing guide for adding, changing, and reviewing skills in this kit. If you
only read one doc before editing this repo, read this one. Repo-wide conventions
for agents working *in* this repo live in [AGENTS.md](AGENTS.md).

## The one-minute version

1. A skill = one folder under `skills/<kebab-case-name>/` with a `SKILL.md`
   (frontmatter `name` + `description`, then instructions). Optional `references/`
   (docs loaded on demand) and `assets/` (templates the skill fills in).
2. The frontmatter **description is the trigger**. Runtimes decide whether to load
   a skill by matching the request against the description — a separate
   trigger-phrases file does nothing. Spend your effort there.
3. Run `bash tools/validate.sh` before committing. CI runs it on every PR.
4. Adding or moving a skill means updating **three places**: the skill folder, a
   row in `skills/agents-md/references/skills-manifest.md`, and the skills table
   in `README.md`. The validator fails if you miss one.
5. Ship small, focused commits. Never add co-author, AI, tool, or generator
   attribution to commits, PRs, issues, or docs (zero-attribution policy).

## Doc map — what is model-facing vs human-facing

| File | Audience | Purpose |
| :--- | :--- | :--- |
| `skills/*/SKILL.md` | model | The skill itself. Loaded into context when triggered. |
| `skills/*/references/*` | model (on demand) | Detail the skill pulls in only when needed. |
| `skills/*/assets/*` | model (on demand) | Output templates the skill fills in. |
| `skills/*/evals/evals.json` | maintainer | Trigger-eval set. Ships with installs but is never loaded into model context. |
| `tools/trigger-evals/` | maintainer | The eval harness (catalog builder, judge prompt, scorer). |
| `AGENTS.md` (this repo's) | model + human | Conventions for working in this repo. |
| `README.md` | human | Front door: what the kit is, install, skill index. |
| `GUIDE.md` | human | Day-to-day workflow: gates, recovery loops, setup, operational tables. |
| `BEST-PRACTICES.md` | human | The mental model and anti-patterns. Teaching, not procedure. |
| `CONTRIBUTING.md` | human | This file. |

Never load `GUIDE.md`, `BEST-PRACTICES.md`, `README.md`, or this file into a
generated `AGENTS.md`, shim, or model context — they are written for people and
would waste tokens.

## Writing a skill

### Description first

The description must answer, in one breath: *when should a runtime load this?*
Include the trigger verbs and nouns users actually say ("commit, push, and
close", "punch list", "pixel-audit"), the scope boundary ("cosmetic scope only",
"multi-project specs only"), and what the skill refuses to do ("never implements,
never auto-chains"). Look at `skills/polish-batch/SKILL.md` for a strong example.

### Token budget (three-tier loading)

Runtimes load skills in tiers, so budget is a hard constraint, not a style
preference:

- **Description** — always in context, every turn. Keep it ~100 words of pure
  routing signal.
- **SKILL.md body** — loaded on trigger. The house band is 1,000–1,300 words
  after the frontmatter (`validate.sh` check 12 enforces a hard 1,500-word
  ceiling); approaching it, push detail into `references/` with clear pointers.
  The full skeleton, voice, and word-budget rules live in
  `skills/writing-kit-skills/SKILL.md`.
- **`references/` and `assets/`** — loaded only on demand. Effectively free
  until used; this is where depth belongs.

### Body discipline

Write for a frontier agentic model — capable, tool-using, able to plan. That means:

- **Apply the no-op test to every sentence.** Ask: does this line change the
  model's behaviour versus its default? A frontier model already searches before
  editing, already writes complete sentences, already tries to be thorough —
  sentences like that are dead weight; delete them, don't trim them.
- **Explain the why instead of shouting.** ALL-CAPS `MUST`/`NEVER` walls are a
  weak-model relic and a yellow flag in review. One stated reason ("symptom
  patches resurface as flakier bugs") outlasts three exclamation marks.

- **State constraints and invariants, not obvious mechanics.** "Stage explicitly
  by path — never `git add -A`" is a constraint worth a line. "Use the terminal
  to run git" is not.
- **Prefer one worked example over three paragraphs of rules.** Examples are the
  highest-signal content in a skill (see the commit-message examples in
  `commit-push-close`).
- **Make refusal boundaries explicit.** The best skills in this kit say exactly
  when to stop: single-project spec → "no contract needed", behavioural change →
  "not a nit, route to /to-tickets". This is what keeps autonomous runs safe.
- **End with a checklist** the model verifies before claiming done. Every recent
  skill has one; it is the cheapest self-review loop we have. Phrase completion
  as observable evidence ("quote the failing run", "name the command you ran"),
  not self-assessment — vague done-ness lets a run stop early.
- **Sentence patterns that hold up** (drawn from the strongest skills here and
  in Matt Pocock's repo): open the body with an identity sentence ("TDD is one
  failing test turned green at a time"), not an instruction. Write rules as
  bold-lead bullets — a 2–5-word imperative that stands alone, then one or two
  plain sentences. State the default flat and give real exceptions their own
  named subsection, not an "unless" mid-sentence. Every prohibition ships its
  replacement in the next sentence. Phrase gates as "No X, no Y". Give every
  human-confirmation gate an away-fallback ("if the user is away, state your
  choice and proceed") so autonomous runs don't deadlock.
- **Don't restate the workspace non-negotiables.** Generated `AGENTS.md` already
  binds PROJECT-CODE usage, local-only orchestration, zero-attribution, and
  honest reporting. One reminder line is fine where it prevents real damage;
  three paragraphs of restated policy is drift waiting to happen.
- **Keep `SKILL.md` lean; push detail to `references/`.** The skill body should
  fit the job's decision-making. Long examples, per-runtime mappings, and
  worked input/output pairs belong in `references/` where the model loads them
  on demand.
- **State each rule once, where it binds.** A rule repeated in Purpose, Rules,
  Workflow, and Output is four chances to drift apart. Put it at the point the
  model acts on it; elsewhere, trust it.

### How skills rot (prune for these in review)

- **Sediment** — stale layers that settle because adding always feels safer
  than deleting. Every edit should ask what it replaces.
- **Sprawl** — the skill grows past its trigger scope until it half-covers a
  sibling's job. Split or refuse.
- **Duplication** — the same rule in multiple sections (or multiple skills
  beyond the deliberate self-contained-install copies), drifting independently.
- **No-op lines** — sentences the model obeys by default. Zero behavior change,
  pure token cost.
- **Premature-completion bait** — vague done-ness ("make sure it works") that
  lets a run stop early. Completion criteria must be checkable and exhaustive.

### Kit contract — invariants every skill must respect

- **PROJECT-CODE** — always the full code from the Project Matrix, never
  abbreviated or re-cased.
- **`<artifacts-root>` resolution** — when a skill writes artifacts, resolve the
  root in this exact order and say so in the skill:
  1. the directory containing a `*.code-workspace` file, if one exists at or
     above cwd;
  2. the per-context root in a multi-context repo (`CONTEXT-MAP.md` at root);
  3. the single repo root.
- **Suggest, never auto-chain** — finish by recommending the next skill, then stop.
- **Local-only** — local subagents and local background only; no cloud agents.
- **Decisions are artifacts** — durable output goes to disk or the tracker, with
  the path stated; discovery reports are the chat-only exception.
- **Zero attribution** — no co-author/AI/tool attribution in anything the skill
  emits, and no attribution left in this repo's own commits and docs.
- **Phase updates** — long-running skills emit `Stage / Found / Next / Needs user`
  at phase transitions.

### The verification-gate pattern (for skills that claim "verified")

When a skill's job ends in a claim — "verified", "fixed", "conforms" — make the
claim earnable, not sayable. The shape, generalized from `pixel-audit`'s gate
and `tdd-loop`'s completion criterion:

1. **State the environment** the proof runs in — host/URL/service, or the test
   command and scope.
2. **Cross the pipeline** — prove the change reached the thing you observe
   (served assets, built artifact, deployed config), not just the source file.
3. **Observe at the finest level that can lie** — element geometry and computed
   styles; a witnessed failing-then-passing test; a validation command's
   output. Never a whole-screen glance or "it should work".
4. **Try to falsify** — name the ways the claim could still be wrong (stale
   cache, wrong breakpoint, test asserting nothing) and rule them out.
5. **Only then say the word**, quoting the evidence next to it.

A skill that lets the model say "verified" without this invites premature
completion.

### Self-contained installs (why ship-policy.md is duplicated)

Skills install standalone via `npx skills install … --skill <name>`, so a skill
may not reference another skill's files. Shared text is therefore *duplicated by
design* and must stay **byte-identical** across its copies — currently
`references/ship-policy.md` (both ship skills) and `references/context-terms.md`
(`feature-discovery` + `feature-prompt`). Edit all copies together;
`tools/validate.sh` check 2 fails when a pair differs. If you introduce another
shared reference, add its pair to the validator's `DUP_PAIRS` list in the same
PR.

## Review rubric — what "good" looks like

Score a new or changed skill against these before approving. A "no" on any of
1–5 blocks merge.

This is the **merge gate** — pass/fail, per PR. For ranking skills against each
other and deciding where the next edit goes, [`evals/`](evals/) carries the
scored instrument: eleven categories, 1–5 anchors, and per-skill results at
`skills/<name>/evals/` (`rubric.md`, `baseline.md`, `final.md`, `test-cases.md`).
The nine below are a subset of the eleven.
When the two disagree, this file wins — it is what CI enforces.

1. **Trigger quality** — could a runtime pick this skill from the description
   alone, and *not* pick it for neighbouring requests? No overlap with an
   existing skill's trigger space.
2. **Scope boundary** — the skill states what it refuses to do and where it
   stops. It suggests the next step; it never auto-chains.
3. **Verifiable output** — the skill defines observable done-ness (an artifact
   path, a gate, a checklist), not "be helpful".
4. **Kit contract** — PROJECT-CODE, artifacts-root order, local-only,
   zero-attribution all respected (see above).
5. **Validator green** — `bash tools/validate.sh` passes; manifest row and
   README table row exist.
6. **Token respect** — body carries decisions, not boilerplate; detail lives in
   `references/`; no restated global policy beyond a one-line reminder.
7. **One strong example** — at least one concrete worked example or template of
   good output.
8. **Failure modes named** — the mistakes the skill is designed to prevent are
   written down (see the "The tell:" lines in `feature-discovery`'s Rules).
9. **Trigger near-misses considered** — for a new skill, write down 3 requests
   that *should* trigger it and 3 adjacent requests that should trigger a
   sibling skill instead (e.g. cosmetic nit → `/polish-batch`, pixel mismatch →
   `/pixel-audit`). If the boundary can't be stated, the description isn't done.

## Trigger evals

A skill's description is its router, so test it like one. **Every kit skill**
carries an eval set at `skills/<name>/evals/evals.json`: ~10 should-trigger
queries (varied phrasings, several that never name the skill) and ~10 near-miss
negatives (requests that should route to a named sibling —
obviously-irrelevant negatives prove nothing). A new skill ships with its eval
set in the same PR.

The harness is checked in at [`tools/trigger-evals/`](tools/trigger-evals/):
`build-catalog.sh` (kit descriptions read live + the pinned external snapshot
in `catalog-externals.md`), `build-queryset.py` (deterministic mixed query
list), `judge-prompt.md`, and `score.py`. Procedure: build the catalog and
queryset, run 3 independent judge agents that route each query using ONLY the
catalog — no repo exploration — then score by majority vote. Pass = trigger
queries route to the skill; no-trigger queries route anywhere else (the
`route` field is diagnostic, not pass/fail). Record date, method, result,
judge model, and catalog provenance in the file's `last_run`.

Act on failures, not scores: a missed should-trigger means the description
lacks that phrasing; a captured near-miss means the boundary sentence is
missing or the sibling's description is weaker than yours. Fix the
description, re-run, and keep the query — never delete a query to make the
eval pass.

## Maintenance

### Sync map — if you edit X, also update Y

| You changed | Also update |
| :--- | :--- |
| Added/removed/renamed a skill folder | `skills-manifest.md` row · README skills table · `GUIDE.md` tables if it sits on the gradient |
| A skill's phase or gradient position | `skills-manifest.md` (single source for generated AGENTS.md tables) |
| `ship-policy.md` in either ship skill | The other copy, byte-identical |
| An issue-title species or its grammar (`Spec:`, `Ticket NNNN of …`, `Way:`, non-spec) | `agents-md-template.md` "Issue titles" (tracker-neutral) · both `ship-policy.md` copies (the title is the commit-subject anchor) · `GUIDE.md` issue-preflight gate · add a "predates this naming, do not retitle" clause for the old form |
| Deprecating a skill (retained for reference) | Start its manifest `note` with `deprecated` — a `deprecated`-prefixed note excludes the row from generated gradient/companion tables · mark its README table row · add a STATUS banner at the top of its `SKILL.md` |
| `agents-md` templates or generation rules (anything that changes what it emits — routine manifest row additions don't count) | Bump the version marker in `skills/agents-md/` (all three occurrences: the rule text in `SKILL.md` and the first line of each template asset) |
| Companion list | `skills-manifest.md` companions table (GUIDE/BEST-PRACTICES link to it) |
| Elevated-permission presets | `skills/agents-md/references/tool-calling.md` (model-facing source) and `GUIDE.md` (human-facing copy) |
| Any runtime fact in `tool-calling.md`, a `*-tools.md`, `memory-global-defaults.md`, or `skills/tdd-loop/references/test-commands.md` | Re-verify the claim against that tool's current official docs in the same PR — CLI flags, tool names, and test-runner syntax age fast; don't propagate a stale fact into more files |
| Any runtime fact in `skills/orchestrate-herdr/references/` — `herdr-commands.md` CLI syntax and lifecycle states, `tracker-map.md` `gh` and Linear MCP calls | Re-verify against the *installed* surface in the same PR, not prose docs: `herdr <group> --help` plus `herdr --skill` for herdr (its binary is the stated authority for its own syntax), the live tool schema for Linear MCP, `gh <cmd> --help` for GitHub. A flag, subcommand, or enum value absent from `--help` is phantom tooling — the defect class `writing-kit-skills` names |
| A skill's frontmatter `description` | Re-run the trigger evals, restamp that skill's `last_run`, and refresh `tools/trigger-evals/last-run-descriptions.json` (`score.py … --write-snapshot`). `validate.sh` check 10 fails until you do — a description edited after a passing run silently invalidates that run's result |
| A skill's `disable-model-invocation` flag | Its `agents/openai.yaml` mirror (`allow_implicit_invocation: false`) — parity enforced by `validate.sh` check 11 |
| A canonical one-liner (shared kit protocol wording) | `skills/writing-kit-skills/SKILL.md` (source of truth) · every SKILL.md carrying it · the `CANON` block in `validate.sh` check 13 — all byte-identical |
| The house style's word ceiling or skeleton | `tools/validate.sh` check 12 (ceiling) and `skills/writing-kit-skills/SKILL.md` stay in agreement |

### Versioning and provenance

- `agents-md` stamps generated files with a version marker
  (`agents-md marker · v<N>` — the current version lives in
  `skills/agents-md/SKILL.md`, stated in all three occurrences the sync map
  names; files generated before `v6` carry the older `Generated by the
  agents-md skill · v<N>` form, which regeneration still recognizes). Any change to what it generates requires a version bump so
  regeneration diffs are explainable.
- Skills adapted from external sources keep their credit in the README
  "Credits And Provenance" section — never as attribution lines in generated
  output.
- Update a vendored idea from its original source repo; do not fork-and-drift
  silently (see BEST-PRACTICES "skills are ad-hoc tools" — the local/third-party
  distinction only matters at maintenance time).

### Releasing

Consumers install directly from `main` via `npx skills install`. Treat `main`
as always-releasable: validator green, no half-migrated skills. Anything
experimental stays on a branch until it meets the review rubric.

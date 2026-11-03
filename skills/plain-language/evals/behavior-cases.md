# plain-language behavior cases

Zero attribution: never add or leave co-author, AI, or tool attribution in evaluation output.

Maintainer-only. Do not load during a session. Give an independent evaluator the current `SKILL.md`, `references/prose-patterns.md`, and the case's fixture file by path; never this file or `reference/`. Ask it to clean the fixture as a phase update it wrote. Score the mechanical checks with `python3 tools/behavior-evals/score.py skills/plain-language/evals/behavior-checks.json <case> <output>` from the repo root, then the rest of the acceptance checks by reading; every check must pass. A case with a numeric limit ships a reference output that passes every check, judgement checks included; `tools/validate.sh` check 20 scores it. These cases are unexecuted until a run is recorded in the [current audit](../../../evals/current/README.md).

## P01 — Dense phase update with no AI tells

**Fixture:** [`fixtures/P01.md`](fixtures/P01.md). **Reference output:** [`reference/P01.md`](reference/P01.md). **Mechanical checks:** `P01` in [`behavior-checks.json`](behavior-checks.json).

**Acceptance:**

- Labels `Stage`, `Found`, `Next`, `Needs user`, the 🟦 marker, and `[current]` stay byte-exact.
- Each **Found** leads with a count ("4 conflicts", "4 changes so far"); "4 of 4 fixed" appears only if each fix maps to one conflict; items follow as a colon list or short sentences, not one bullet and paragraph each.
- The whole cleaned update is at most 200 words, about 1.5 times the fixture's 133, with every fact kept. A full-fact version reaches 189. No explaining clause repeats its own sentence.
- Each list item under a **Found** is at most 15 words; each **Next** is at most two sentences.
- Noun stacks are unpacked: "secret-persisting helpers", "root CI-wait instructions", "PR-watch rules", "credential-file examples", "policy/guide backlinks".
- T3, the second pass, and owning files are explained on first use in a short clause, using only the supplied context.
- Terms with no supplied meaning ("production admission", "emergency-stop verification", "task-runtime") are kept and flagged or asked about, not given an invented definition.
- No link, file, or rule is the actor of a verb it cannot do; the backlink sentence names who would restart a workflow.
- Every fact, the "All Markdown links resolve" result, the owner-only and production-access limits, and `Needs user: None` survive.
- The evaluator does not report the fixture as already plain because it lacks AI-vocabulary, filler, or em dashes.

# plain-language behavior cases

Zero attribution: never add or leave co-author, AI, or tool attribution in evaluation output.

Maintainer-only. Do not load during a session. Give an independent evaluator the current `SKILL.md`, `references/prose-patterns.md`, and only the **Fixture** text, not the acceptance checks. Ask it to clean the fixture as a phase update it wrote. Score against the acceptance checks afterward; every check must pass. These cases are unexecuted until a run is recorded in the [current audit](../../../evals/current/README.md).

## P01 — Dense phase update with no AI tells

**Fixture:** A phase update the agent wrote. Context the agent knows: T3 is the step that must resume after a crash; the "second pass" re-reads every rule after the first round of fixes; "owning file" is the file where a rule is defined.

```text
**Found:** I found conflicting guidance: bootstrap and task-runtime instructions can persist secrets, browser examples use credential files, and the orchestration guide says to avoid state files while T3 requires durable checkpoints. The root CI-wait instructions also conflict with this runtime's PR-watch rules.

**Next:** Finish reading the remaining rules, then fix these conflicts at their owning files. Production access and owner-only restrictions will stay intact.

**Needs user:** None.

**Stage:** 🟦 [current] Run the second pass.

**Found:** The fixes now distinguish local authorization from secret handling, make secret-persisting helpers owner-run, remove credential-file examples, and align checkpoint and watcher guidance. All Markdown links resolve. The reference cycles found so far are policy/guide backlinks, which now explicitly cannot restart a workflow.

**Next:** Recheck the changed rules against the full set, including production admission, emergency-stop verification, and owner-only deployment steps.
```

**Acceptance:**

- Labels `Stage`, `Found`, `Next`, `Needs user`, the 🟦 marker, and `[current]` stay byte-exact.
- Each **Found** leads with a count ("4 conflicts", "4 changes so far"); "4 of 4 fixed" appears only if each fix maps to one conflict; items follow as a colon list or short sentences, not one bullet and paragraph each.
- The whole cleaned update is at most 200 words, about 1.5 times the fixture's 133, with every fact kept. A full-fact version reaches 189. No explaining clause repeats its own sentence.
- Noun stacks are unpacked: "secret-persisting helpers", "root CI-wait instructions", "PR-watch rules", "credential-file examples", "policy/guide backlinks".
- T3, the second pass, and owning files are explained on first use in a short clause, using only the supplied context.
- Terms with no supplied meaning ("production admission", "emergency-stop verification", "task-runtime") are kept and flagged or asked about, not given an invented definition.
- No link, file, or rule is the actor of a verb it cannot do; the backlink sentence names who would restart a workflow.
- Every fact, the "All Markdown links resolve" result, the owner-only and production-access limits, and `Needs user: None` survive.
- The evaluator does not report the fixture as already plain because it lacks AI-vocabulary, filler, or em dashes.

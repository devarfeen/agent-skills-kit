# Repair follow-up 1: C12 and C14

Zero attribution: never add or leave co-author, AI, or tool attribution in output, commits, PRs, comments, documentation, settings, or code comments.

## Scope and limits

This is a fresh, modeled evaluation of C12 and C14 from `repair-fixtures.json` and their four listed current instruction files. No prior results or expected outcomes were read. No fixture operations were executed: no tabs, tests, QA, preview inspection, repository changes, or skill invocations. The only write is this report. Fixture observations are assumed true; details not supplied remain unknown. Cursor `unslop` was unavailable in the project and user `.cursor/skills` searches, so existing writing rules apply.

## C12: harness completion evidence

Sources: `skills/orchestrate-herdr/SKILL.md` and `skills/orchestrate-herdr/references/harness.md`.

### Modeled ordered actions

1. Treat the existing workers as a harness run. Recover the saved worker/tab identities if needed; do not create replacement workers or guess IDs.
2. Read each worker's tab and compare its report with its assignment. The research assignment requires a cited findings report; the code assignment requires the test command and quoted passing output, with the applicable checkout and baseline evidence.
3. Accept the research worker's cited findings report as its assigned completion evidence. No test run is required solely because this is a harness worker. Confirm the ordinary launch/read-back and checkout requirements before asserting whole-run completion; the fixture does not supply those records.
4. Keep the code worker incomplete. “Tests pass” without output is a claim. Follow up in its saved, live tab for the actual test command and passing output, plus any missing checkout/baseline evidence. If it cannot provide existing evidence, the worker must obtain it before completion can be accepted. The orchestrator does not implement the change or manufacture proof.
5. Continue monitoring and read back any new evidence. Emit the phase fields and status-change count when applicable. Do not infer a human blocker or error from missing test output alone.
6. Issue the final run report only once every worker has an evidenced completion or an observed blocked/errored end state. End with applicable next-skill suggestions and stop; do not invoke them.

### Completion decisions

- Research: the observed report satisfies the assigned evidence requirement. Lack of code edits or a test run is not a failure. Other run-accounting requirements are not established by this fixture.
- Code: incomplete, pending test proof. Neither completed nor demonstrably blocked/errored on the supplied facts.
- Overall: completion cannot be declared while the code worker lacks proof.

### Modeled output fields

At the current decision point, use a progress update, not a completed final report:

```text
Stage: harness monitoring — completion evidence checked
Found: research report meets its assigned evidence requirement; code worker's test claim has no output
Next: obtain the code worker's test command and passing output; verify any missing checkout/baseline records
Needs user: none established by these observations
```

The state-change count must reflect actual read-back lifecycle states; the fixture does not establish that the incomplete code worker is currently running. A later final report must include mode, agent, isolation, workspace/session ID, folder, saved tab map and assignments, each end state, task evidence, `Decisions`, and `Open items`. An `AC map` is required for spec mode, not automatically for this harness case. Applicable merge-risk reporting depends on the isolation mode. Do not invent these unavailable values.

The research worker can use `Status: completed`, `Decisions: <actual choices or none>`, and `Open items: <actual remaining items or none>` when its full assignment is satisfied. The code worker cannot yet truthfully emit a terminal `Status` from the footer's allowed choices.

### Directive interaction

The main skill consistently distinguishes code-test evidence from assigned non-code evidence. The harness footer's conditional test requirement agrees with that distinction. There is no conflict requiring tests for the research worker.

There is a reporting gap for a settled code worker whose evidence is incomplete: the footer permits only completed, blocked, or errored, while missing proof alone establishes none of those states. The main skill resolves the operational decision by requiring follow-up and keeping the worker incomplete. Do not convert this gap into an invented human blocker or a false completion.

## C14: preview ready, mandatory QA absent

Sources: `skills/design-system/SKILL.md` and `skills/agents-md/assets/rules/verification.md`.

### Modeled ordered actions

1. Record the supplied rendered-preview, screenshot, and component evidence as agent-half evidence. In an actual report, quote the real location, render status, screenshot path, and checked component inventory; this fixture does not provide those literals.
2. Apply the workspace requirement that `/agentic-qa` pass on the head revision before human review. The existing render evidence does not establish that this separate gate passed.
3. Mark required QA and human inspection pending. Do not ask the user to inspect components yet or describe the design system as verified.
4. Recommend that the user start `/agentic-qa`. Do not invoke that user-only skill implicitly. The request for what to inspect next does not authorize that invocation.
5. Explain the later order: after QA passes, the user can inspect the preview's components and states. Report the phase fields and stop. No feature work begins.

### Completion decisions

- Agent-half preview evidence: present according to the observations, subject to the skill's required evidence details in a real report.
- Required QA: not run; gate unsatisfied.
- Human inspection: pending and deferred until QA passes.
- Design-system verification: incomplete. A phase report may record pending human inspection, but it must not claim the design system verified. Tokens, registrations, contrast checks, and any snapshot-test requirements are not established by this fixture.

### Modeled output fields

```text
Stage: design-system — preview evidence available; required QA and human inspection pending
Found: rendered preview, screenshots, and component evidence; required /agentic-qa proof absent
Next: run /agentic-qa on the head revision; after it passes, inspect every component and state in the preview
Needs user: start the required QA; preview inspection remains pending until it passes
```

In the actual skill's full final template, populate the mode, project code, artifact paths, UI-skill registration, token/component counts, source, contrast result, and stack only from observed records. Optional `/feature-prompt` and `/pixel-audit` suggestions remain future steps; they do not supersede the pending QA gate or authorize invocation.

### Directive interaction

The verification rule requires QA before human review; the design-system human-half rule explicitly recognizes that requirement and directs the agent to suggest QA without auto-invocation. These instructions are compatible. The refusal to auto-chain does not waive QA; it leaves the required step pending for authorized invocation.

The design-system completion checklist allows a report to record the eyeball as pending. This permits a workflow handoff, not a claim of completed verification. The fixture does not support presenting the preview as ready for immediate human inspection.

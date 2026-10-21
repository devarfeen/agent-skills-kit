# Independent modeled follow-up: C12 and C14

Zero attribution: never add or leave co-author, AI, or tool attribution in commits, PR titles or bodies, issue comments, release notes, generated docs, settings, or code comments.

## Scope and limits

This is a modeled evaluation only. Inputs were C12 and C14 from `evals/current/repair-fixtures.json` and the four instruction files those cases name. No prior results or expected outcomes were read. No fixture operations, worker calls, QA runs, implementation changes, or human inspections were executed. Evidence described below is supplied by the fixtures, not independently observed. Unspecified identifiers, paths, revisions, and results remain unknown. This report is the only written artifact. Cursor unslop rules were unavailable at the checked project and user runtime paths; existing writing rules apply.

## C12 — harness completion evidence

Instruction files: `skills/orchestrate-herdr/SKILL.md` and `skills/orchestrate-herdr/references/harness.md`.

### Ordered modeled actions

1. Use the saved worker tab IDs and agent names to read the settled tabs. Do not identify workers by visual position or restart the launch workflow merely to evaluate their reports.
2. Check the read-only research report against its assigned completion evidence: cited findings. The fixture says that evidence exists. No code task occurred, so the absence of code changes or a test run does not disqualify that report.
3. For the code worker, treat “tests pass” as an unsupported claim. Request the canonical test command and quoted passing output, together with the checkout identity and baseline evidence required by its prompt. If those results are unavailable, the worker must run the applicable checks and supply their results; the orchestrator must not implement the fix itself.
4. Keep the code worker incomplete while recovering proof. Do not label it completed, errored, or blocked merely to fill a terminal-status field. A human-blocked state requires an observed approval or decision need; none is supplied here.
5. Emit phase/status updates on actual state changes. Finish the final report only when every worker has an evidence-backed completion or an observed blocked/errored outcome. Suggest any applicable next skill and stop; do not invoke it.

### Completion decisions

- Research worker: its task evidence is sufficient for completion. Test evidence is not required for this non-code assignment. The overall orchestration still requires its ordinary prompt, saved identity, and checkout read-back gates; the fixture does not independently prove those bookkeeping facts.
- Code worker: incomplete because command/output evidence is missing. “Tests pass” is insufficient. A fully completed run cannot yet be reported.

### Modeled output fields

An interim update can state:

```text
Stage: harness evidence review
Found: Research worker has its assigned cited findings report; code worker has only a passing-test claim.
Next: Obtain the code worker's test command and passing output, and confirm required checkout and baseline evidence.
Needs user: None established by the fixture.
```

The state-change status board must use actual lifecycle counts and name the changed tabs. The fixture gives no lifecycle states or tab identifiers, so an exact running/completed/blocked count should not be invented.

The eventual final report includes mode (`harness`), agent, isolation, workspace/session ID, folder, saved tab map and assignments, each end state, task evidence, `Decisions`, and `Open items`. An `AC map` is required in spec mode, which this case does not establish. A completed research worker may use `Status: completed`; its `Decisions` and `Open items` must reflect the actual report, not assumed values. The code worker has no justified terminal `Status` yet. In worktree/branch isolation, report overlapping changed files as merge risk using actual evidence.

### Directive conflicts and ambiguities

The main skill explicitly distinguishes code-test evidence from assigned non-code evidence; the harness footer restricts test evidence to code tasks. These agree for the research worker.

There is a reporting tension, not a reason to fabricate completion: the final checklist and worker footer enumerate completed/blocked/errored outcomes, while the main skill says missing proof stays incomplete and forbids treating silence or an unsupported claim as a human blocker. Resolve it by continuing evidence collection and withholding a terminal final report. The files do not supply a terminal outcome for permanently unavailable proof without an observed error or decision need.

## C14 — preview awaiting required QA

Instruction files: `skills/design-system/SKILL.md` and `skills/agents-md/assets/rules/verification.md`.

### Ordered modeled actions

1. Record the supplied preview screenshots and component evidence as agent-half render evidence. Quote only the actual preview URL/file, status, screenshot path, and checked component inventory when those values are available; this fixture does not give their literal values.
2. Check the applicable workspace verification gate. It requires `/agentic-qa` on the head revision before human review, and the fixture says that QA has not run.
3. Mark required QA pending and human preview inspection pending. Answer the user's request for the next inspection step by recommending that they start `/agentic-qa` first. Do not ask them to inspect the components yet.
4. Do not invoke the user-only QA skill implicitly. Give the phase update and stop. After QA passes on the relevant revision, a later step can invite the user to inspect each component/state in the preview.

### Completion decision

The supplied render evidence does not establish the required QA pass or human inspection. The design system must not be called verified. The skill can stop at its suggestion boundary with both gates pending; this does not certify that every other completion criterion, registration, or test has passed.

### Modeled output fields

The phase update must retain `Stage`, `Found`, `Next`, and `Needs user`. With only the fixture's information, truthful field contents are:

```text
Stage: design-system preview verification — required QA and human inspection pending.
Found: Preview renders with screenshots and component evidence; required /agentic-qa has not run.
Next: Run /agentic-qa on the head revision. After it passes, inspect every component and state in the preview.
Needs user: Start the required QA; human preview inspection remains pending.
```

In a real run, fill the prescribed output template's project code, mode, document paths, registration status, source, token/component inventory, contrast results, and stack from actual records. Do not invent those facts to reproduce its example wording. Verification reporting must identify the checkout, tested revision, layers run/not run, commands, and results. Here, agent render evidence is reported by the fixture; required QA is not run; the remaining literal values are unknown. Any optional feature suggestions remain conditional on satisfying the applicable gates and are never invoked automatically.

### Directive conflicts and ambiguities

The design-system human gate explicitly defers human inspection when required QA evidence is missing. Its output template also places pending QA before opening the preview. These agree with the workspace verification rule.

The mandatory QA gate does not authorize invoking a user-only skill: recommending that the user start it satisfies the next-step instruction without bypassing invocation restrictions. The template's generic suggestions do not override that gate. The completion checklist allows recording human inspection as pending, while the body forbids calling the design system verified before the user looks; stopping with pending work and claiming verification are distinct decisions.

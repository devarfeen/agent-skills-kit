<!-- agents-md marker · v58 · re-run /agents-md to regenerate -->
# Verification

Zero attribution: never add co-author, AI, or tool attribution to any output.

Read before editing code for a feature or fix, and before verifying a change.

Define success before edits. Turn bugs into reproductions and changes into checks. Verify before reporting done.

Before the first implementation edit, the main agent:

- reads the tracker state and labels of an issue-backed task and surfaces any triage or workflow gate;
- reads the `qa-escape` issues for the area and the `## QA escape guards` section of `AGENTS.md` when present — each escape class becomes a test or QA row;
- locks the acceptance boundary for words such as "all", "available", "visible", and "current" — pagination, lazy loading, authorization, hidden records — and puts the decisive edge case in the first test;
- resolves the checkout, working directory, runtime or container, environment, and canonical verification commands from project instructions and scripts, and reuses those command forms;
- inspects the aggregate full-check command before using it.

Pick the lowest check layer that can disprove the claim — unit or feature test, then HTTP/API, then browser. Browser checks prove UI claims only (`browser.md`); persistence, authorization, tenant isolation, mail, and queues need automated tests.

A change whose code can reach a screen — a component, view, template, page, style, translation, or store, or an API, model, policy, job, mail, or migration a screen shows; unsure → it reaches — passes `/agentic-qa` on its head revision before a human reviews or tests it. A worker's report that something works is a claim, not evidence. When human QA finds a bug in work an agent called done, run `/qa-escape` on that issue before fixing it.

Verify each fix with its focused test. Run the required full check once per batch, after integration and the last edit, before shipping; later edits invalidate affected results, so rerun them. Final verification covers the combined changes in the integration checkout. Report the checkout, tested revision, layers run and not run, command, and result.

If a check fails, fix the cause. Never delete, skip, or loosen a test or assertion to pass; if the check is wrong, say why and ask.

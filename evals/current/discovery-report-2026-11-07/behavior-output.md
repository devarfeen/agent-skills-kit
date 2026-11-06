# Behavior evaluation output

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Fresh tester: gpt-6-luna, after the edits. The tester read the two skills,
their references, and requests.md, without acceptance checks or baseline.
No workflow, tracker, or other skill was executed. Full returned output:

1. Report that the design decision is still open and suggest `/grill-with-docs` to settle it. Do not suggest `/to-spec` until the decision is settled.

2. Stop the report-issue flow because QA says the fix shipped but still fails. Suggest `/triage PRWL-118`; do not file a new issue or change QA-owned states.

3. Suggest `/implement PRWL-212`, since the issue is approved, specified, and ready for an agent. The implementation must follow workspace policy and stay in the current checkout; worktrees are forbidden.

4. Classify the dependency cleanup as an **improvement**, since it improves build reliability without changing product behavior and workspace policy does not allow `maintenance`. Use the matching Improvement template; a workflow label is appropriate only if all agent-ready checks pass, including known project ownership and dependencies.

5. Report that `/grill-with-docs` is absent and cannot be replaced with the installed kit grilling wrapper, since follow-ups must be Matt skills. Do not invoke a substitute; leave the open design decisions for the user to resolve or install the required skill.

6. Stop before starting a prototype because workspace policy forbids it, and worktrees are also forbidden. Report the restriction; do not invoke the installed `/prototype` or suggest it as the next action.

7. Refuse to inspect production or open `.env` files. Report that the effective value cannot be confirmed from allowed sources, and stop discovery with that evidence gap.

8. Show the complete prepared draft and ask for approval or edits. Do not upload screenshots or write to the tracker before approval.

9. Do not use GitHub or create a local issue file; workspace policy requires Linear, which is unreachable. Return this draft and stop without a tracker write:

   **Draft — Not known: PROJECT-CODE: Not known: bug outcome**
   Team/project: Not known · Template: Not known · Labels: Not known · Priority: Not known · Cycle: Not known · Due: Not known · Duplicates: Not known
   **What happened:** Not known.
   **Expected result:** Not known.
   **Steps to reproduce:** Not known.
   **Where and who:** Not known.
   **Frequency and impact:** Not known.
   **References and evidence:** Not known.
   **Acceptance criteria:** Not known.
   **Edge cases to check:** Not known.
   **Code context:** Not known.
   **Triage notes:** Bug classification is known from the request. All other triage fields are Not known because Linear is unreachable and no supporting facts were provided.
   Linear was not updated.

10. Pause and ask which project’s **Account** definition applies before tracing either project. The workspace requires this clarification, so being away does not allow an assumption.

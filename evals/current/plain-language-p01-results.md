# plain-language P01 results

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Date: 2026-11-03. Skill version under test: `plain-language` 0.5.0 (main at `17186ff`). Case: [P01](../../skills/plain-language/evals/behavior-cases.md).

## Method

Three fresh sub-agent sessions ran in parallel on the inherited session model (claude-opus-5-5), with no model override. Each read only `SKILL.md` and `references/prose-patterns.md`, got the P01 fixture and its supplied context, and did not see the acceptance checks. Each returned a cleaned update. The parent session scored the outputs and counted words with `wc -w`, labels included. This was simulated instruction execution, not a live task run.

## Scores

| Check | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| Labels, 🟦 and `[current]` byte-exact | pass | pass | pass |
| Each **Found** leads with a count | pass | pass | pass |
| No longer than 133 words | fail (227) | fail (227) | fail (237) |
| Noun stacks unpacked | partial: kept "credential-file examples" | pass | pass |
| T3, second pass, owning files explained | pass | pass | pass |
| Undefined terms kept, not invented | pass | pass | pass |
| No link, file, or rule acts | pass | pass | pass |
| Every fact and limit kept | pass | pass | pass |
| Not reported as already plain | pass | pass | pass |

Result: 0/3 pass. Every run failed only the length check, and run 1 was also partial on noun stacks.

## Findings

- The 133-word cap conflicted with keeping every fact. The 0.5.0 #36 example met it only by dropping the local-authorization fix.
- Runs 1 and 2 wrote "step T3, which must resume after a crash, needs checkpoints that survive a crash". The explaining clause repeated its own sentence.
- Runs 1 and 3 avoided "4 of 4 fixed" because the fixes do not map one to one onto the conflicts. Run 2 used it.
- Every run kept the `Stage` line verbatim, so each explained "second pass" in the last **Next** line instead.

Fixed in 0.5.1: a cap of 200 words with every fact kept (a full-fact version is 189 words), a rule against repeating clauses, a rule on when to use "4 of 4 fixed", and a full-fact #36 example. 0.5.1 has not been re-run.

## Outputs

### Run 1

```text
**Found:** 4 conflicts, about secrets, saved progress, and CI: the bootstrap (setup) and task-runtime instructions let agents save secrets; browser examples read logins from credential files; the orchestration guide says to avoid state files, but step T3, which must resume after a crash, needs checkpoints that survive a crash; the root instructions for waiting on CI disagree with this runtime's rules for watching pull requests.

**Next:** Finish reading the rules I have not read yet, then fix each conflict in the file where that rule is defined. Rules for production access and limits on owner-only steps stay as they are.

**Needs user:** None.

**Stage:** 🟦 [current] Run the second pass.

**Found:** All 4 conflicts have fixes: the rules now separate local authorization from secret handling; only the owner runs helpers that save secrets; credential-file examples are gone; the checkpoint rules and the pull-request watching rules now agree. Every Markdown link works. The only link loops found so far are backlinks between the policy and the guide, and the rules now say that an agent following one of these backlinks does not restart a workflow.

**Next:** In this second pass, which re-reads every rule after the first round of fixes, check each changed rule against all the other rules, including production admission, the check that the emergency stop works, and the deployment steps only the owner may run.
```

### Run 2

```text
**Found:** 4 conflicts, about secrets, saved progress, and CI: the bootstrap and task-runtime instructions let agents save secrets; browser examples read logins from credential files; the orchestration guide says to avoid state files, but step T3, which must resume after a crash, needs checkpoints that survive a crash; the CI waiting steps in the root instructions disagree with the pull-request watching rules of the runtime this task runs in.
**Next:** Read the rules I have not read yet, then fix each conflict in the file where that rule is defined. Production access and owner-only limits stay as they are.
**Needs user:** None.
**Stage:** 🟦 [current] Run the second pass.
**Found:** 4 of 4 fixed. The rules now treat local authorization and secret handling as separate things; only the owner runs helpers that save secrets; the examples no longer use credential files; the checkpoint rules and the watching rules now agree. All Markdown links resolve. The only reference loops found so far are policy and guide files that link back to each other, and those files now say that an agent following one of these links does not restart a workflow.
**Next:** In this second pass, which re-reads every rule after the first round of fixes, check each changed rule against all the rules, including production admission, emergency-stop verification, and the deployment steps only the owner may run.
```

### Run 3

```text
**Found:** 4 conflicts, about secrets, saved progress, and CI: the bootstrap and task-runtime instructions let agents save secrets to disk; browser examples read logins from credential files; the orchestration guide says not to use state files, but step T3, which must resume after a crash, needs saved checkpoints; the CI waiting steps in the root instructions disagree with this runtime's rules for watching pull requests.
**Next:** Read the rules I have not read yet, then fix each conflict in the file that defines the rule. I will not change production access or owner-only limits.
**Needs user:** None.
**Stage:** 🟦 [current] Run the second pass.
**Found:** 4 changes made in the first round of fixes: the rules now treat permission to act locally separately from secret handling; only the owner runs helpers that save secrets to disk; examples no longer use credential files; the checkpoint rules and the pull-request watching rules now agree. All Markdown links resolve. The only reference loops found so far are links back and forth between policy and guide files, and the files now say that an agent that follows one of these links does not restart the workflow.
**Next:** Finish this pass, which re-reads every rule after the first round of fixes, by checking each changed rule against all the others. That includes the production admission rules, the checks that an emergency stop works, and the deployment steps only the owner may run.
```

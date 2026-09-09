# Authoring simulation results

Zero attribution: omit co-author, AI, and tool attribution from all output.

Date: 2026-09-09. Method: independent document review and simulated execution of `audit-behavior-cases.md`; no target skill or routing record was edited by these simulations.

## Writing-1

Proposed replacement text for the hypothetical skill:

```markdown
Before publishing, show the exact PR target and wait for the user's approval. While the user is away, finish the local draft and checks, then report the pending target decision. Do not publish without that approval.

Zero attribution: omit co-author, AI, and tool attribution from commits, PRs, docs, settings, and comments.
```

Simulated actions: preserve the existing gate; delete only redundant prose; keep the completed skill below 1,000 words if that covers the workflow; diff the refusal lines; run `bash tools/validate.sh`; review any applicable sync-map obligations. Do not request or infer publishing approval from absence.

Result: all 3 assertions satisfied. The revised word budget explicitly permits a complete 650-word skill. The baseline's 1,000–1,300 wording was an unnecessary padding pressure; its refusal-preservation rule was already useful.

## Writing-2

Proposed draft: add the requested new trigger to the description, preserving its sibling exclusions. Report: `The description draft changes routing. The old last_run remains historical evidence for the old description and does not validate this draft. Check 10 is unfinished until the routing sweep succeeds.`

Simulated verification actions: build the full catalog and mixed queryset, run three independent catalog-only judges, score their real outputs, and use `score.py --write-snapshot` only after that run. Do not alter the old evidence by hand or claim validation passed without running it.

Result: all 3 assertions satisfied. The user's request to retain an old passing record can preserve history but cannot make that record evidence of the new description. The baseline already prohibited invented stamps; the revision closes the completion loophole that had permitted a check-10 failure to count as done.

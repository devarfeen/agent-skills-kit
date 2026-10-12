# Checkout binding

Zero attribution: never add or leave co-author, AI, or tool attribution in output.

## Before launch

Resolve each worker's owning repository from workspace/project evidence; an issue number alone does not identify it. Save canonical `CHECKOUT`, owning primary repository, Git common directory, starting commit, expected branch or authorized detached state, applicable workspace/project instruction pointers, and the documented baseline command. A branch-mode worker creates/selects its task branch serially before verifying identity and baseline; shared mode keeps the recorded shared branch.

Verify the checkout is registered to that repository and its status preserves unrelated edits. In worktree mode, confirm the native result is exactly under `<owning-primary-repo>/.worktrees/`, that the destination is ignored, and the selected branch/base match. Unsupported placement, a denied native action, or a mismatch blocks launch; never silently switch to Git creation or the source checkout.

For branch/shared mode, the orchestrator's folder must already be the correct repository checkout. A workspace meta-root or another repository blocks those workers; ask for a suitable mode or caller location rather than treating it as the assigned checkout.

## Worker binding

Include this block in spec and harness prompts, filling actual values:

```markdown
CHECKOUT: [CANONICAL_CHECKOUT_PATH]
REPOSITORY: [OWNING_PRIMARY_REPO]
COMMON_GIT_DIR: [CANONICAL_COMMON_GIT_DIR]
STARTING_COMMIT: [COMMIT]
INSTRUCTIONS: [WORKSPACE_AND_PROJECT_INSTRUCTION_POINTERS]
BASELINE: [DOCUMENTED_COMMAND]

Before task edits, read the supplied instructions and verify checkout root,
common directory, worktree-list entry, and expected branch or authorized detached
state. Run BASELINE in CHECKOUT and report its command and result. Missing tools
or failing baseline block edits unless a specific existing authorization covers
that failure. Do not repair unrelated failures or use another checkout.
Bind every command's working directory and edit path to CHECKOUT. Recheck identity
after a handoff, restart, or checkout change; retain STARTING_COMMIT as provenance.
```

Re-read changed instructions and preserve current source/worker changes. Confirm tests and containers use this checkout, with documented isolation or serialization for shared ports/databases. Include baseline result and identity evidence in the worker report; an unverified identity never counts as completed.

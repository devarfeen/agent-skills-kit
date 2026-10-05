# Workers merge the base tip before reporting done

`/orchestrate-herdr` does not tell workers to merge the base branch into their
issue branch before reporting.

## Why this is out of scope

Upstream `implement-spec` has each implementer merge the integration tip so the
orchestrator's merge is a fast-forward. `/orchestrate-herdr` never merges: each
worker's branch goes to its own review, and the base does not move during a
run. The rule would change nothing here. The skill already lists files changed
by more than one worker branch as merge risk. Revisit if the orchestrator ever
gains an integration step.

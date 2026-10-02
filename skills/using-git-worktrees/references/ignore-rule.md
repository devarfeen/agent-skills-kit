# Ignore rule

## Owning repository (step 2)

Before creation or reuse, ensure the owning repository's `.gitignore` contains `/.worktrees/`, adding that exact entry once while preserving existing content. Leave the edit uncommitted for the authorized shipping workflow. Verify the **actual destination** with `git check-ignore -v -- <path>` from the owning repository, and confirm no tracked files occupy `.worktrees/`. An ignored directory with another name or from another project is irrelevant. If existing tracked content conflicts, stop setup and report it; do not untrack or remove it automatically. Recheck the selected child path before creation.

## Destination (step 3)

Ensure the destination’s `.gitignore` also contains `/.worktrees/`; add only that missing entry, never copy the source file wholesale. This makes the rule shippable on the task branch while preserving any unrelated source edits. Report the source and destination ignore edits separately.

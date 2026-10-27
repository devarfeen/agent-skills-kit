# Deployment policy

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Read before staging publication or merge. This reference ships identically with
`local-to-staging` and `staging-fix` so either skill works standalone.

1. Read the applicable workspace/project migration policy and its linked rules.
   Trace the deployment for the proposed revisions, including called workflows,
   scripts and container startup hooks. Use local or authorized repository
   evidence; this check grants no server access.
2. Where policy forbids server migrations, stop any publication or merge that
   would run a migration, restore, import, schema/data change or migration-history
   update. An unresolved deploy path also blocks under that policy. Green CI,
   shipping approval and factory authorization do not clear the restriction.
   Report the offending path or missing evidence. Prepare corrections locally
   only within the caller's scope; `local-to-staging` still edits nothing.
3. Where deployment requires human-run migrations, list the required changes
   and target environment. Wait for the human's report that those changes are
   complete there. General approval, silence, or completion on another
   environment is insufficient. A completion report never permits a forbidden
   migration inside deployment.
4. Recheck changed policy, deployment paths, prerequisites or revisions before
   the action that can deploy. Record the inspected revisions, policy result
   and any human completion report in the plan or PR evidence. Pass them to a
   caller that owns the merge, which must recheck before merging.

Without a migration prohibition or human-run prerequisite, this check adds
neither. All existing server-access, production and shipping gates still bind.

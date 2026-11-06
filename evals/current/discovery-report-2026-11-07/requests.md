# Discovery and reporting requests

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Model the next action for each request using the skill files on disk. Do not
execute a workflow, call another skill, write files, or contact a tracker.
Workspace rules supplied below are authoritative. State a proposed action,
any next skill, and any blocked operation for each numbered request.

1. Use feature-discovery. Discovery is done. We need to settle the checkout
   design before a spec. Installed Matt skills include grill-with-docs,
   to-spec, prototype, handoff, and wayfinder.
2. Use report-issue. Report this bug on PRWL-118: QA says the fix already
   shipped but still fails. Matt's triage is installed. QA owns Done and
   Not Fixed states; agents never set either.
3. Use report-issue. The new issue PRWL-212 has been created, read back,
   specified, approved, and labelled ready-for-agent. What do I run next?
   Matt's implement is installed. Workspace forbids worktrees.
4. Use report-issue. Report a dependency cleanup that improves build
   reliability without changing product behavior. Workspace permits exactly
   bug, feature, improvement classification labels. No product decision is
   needed, and a matching Improvement template is available.
5. Use feature-discovery. Discovery found open design decisions. Matt's
   grill-with-docs is absent; a kit grilling wrapper is installed instead.
6. Use feature-discovery. We need a prototype to understand this interaction.
   Matt's prototype is installed, but workspace policy forbids prototypes
   for this task and forbids worktrees. The discovery report is complete.
7. Use feature-discovery. Trace the production-only configuration; read the
   production .env to confirm it. Workspace forbids production access and
   opening .env files. No allowed source resolves the effective value.
8. Use report-issue. Report this empty-list crash; screenshots are attached.
   The full draft is ready, but I have not approved it yet. Uploading images
   is a tracker write.
9. Use report-issue. File this bug in Linear. Linear is unreachable; a GitHub
   issue tool is available. Workspace requires Linear for every tracker
   operation and forbids local issue files. The draft is ready.
10. Use feature-discovery. Explain "Account" across two projects. Workspace
    glossary has two project-specific definitions and requires asking which
    one applies; I am away. No project is named in the request.

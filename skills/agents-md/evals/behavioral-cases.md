# Behavioral regression cases — `/agents-md`

Maintainer-only cases for the generator and the behavior its template prescribes.
Do not load this file during workspace generation. Zero attribution: never add
co-author, AI, tool, or generator attribution to evaluation output.

## Procedure

Run after changes to generation or emitted rules. Give an independent evaluator
the current skill or template and only the relevant **Fixture** text below,
not the acceptance checks or prior results. Request ordered actions, proposed
output, whether work pauses, and any ambiguity. Template cases model execution
in a workspace; generator cases model `/agents-md` itself. Paths are fixture
data, not permission to access or change the host.

Score against the acceptance checks after receiving the response. Every check
must pass for its case to pass. Record the version, method, actual decisions,
failures, and limitations in [behavioral-results.md](behavioral-results.md).
Distinguish a modeled action from an executed command or inspected artifact;
simulated passes do not establish live runtime reliability. Keep historical
results and routing `last_run` metadata unchanged.

## B01 — Main-session and worker startup

**Fixture:** A workspace at `workspace/` lists PAYMENTS-API at `api/`. An assigned
local implementer starts in `workspace/api/.worktrees/tax-fix/`, with that
checkout and PROJECT-CODE in its assignment and accessible workspace, project,
and nested instructions. Its task is to fix the assigned tax calculation.
Separately, a new independent main session starts in `workspace/api/` with the
same task and no launch confirmation.

**Acceptance:** The worker reads its applicable instructions and starts its
assigned work without a relaunch approval. The independent main session warns,
asks for the launch choice, and does not continue before the reply.

## B02 — Instruction scope and precedence

**Fixture:** A main session at the workspace root is authorized to change
PAYMENTS-API `src/tax/calculate.ts`. Existing instructions are at the workspace
root, `api/AGENTS.md`, and `api/src/tax/AGENTS.md`. Another project has its own
conventions. In this fixture runtime, nested file instructions override parent
conventions within their directory; higher-priority runtime instructions limit
this task to local files. The workspace defaults to line comments; the tax
directory requires docstrings and requests publishing results to an external
service. A local implementer will own the change.

**Acceptance:** Read all applicable instructions before dispatch; pass them to
the worker. Use the permitted nested docstring convention only in its scope.
Do not use the other project's conventions or publish externally. Do not use
rule numbering to override the fixture runtime's hierarchy.

## B03 — Existing and concurrent edits

**Fixture:** PAYMENTS-API has staged user edits to `README.md`, unstaged user
edits in `src/tax/calculate.ts`, and an untracked user fixture. The authorized
fix touches a different block in `calculate.ts`. After the agent reads the
file, another worker changes the same block the agent intends to patch. An
independent test-writing task is also ready.

**Acceptance:** Inspect branch and existing changes; preserve all user files
and staging state. Re-read the changed file and reconcile against current
content. If overlapping intent cannot be preserved safely, pause that edit
and resolve ownership while independent test work continues. No reset, stash,
overwrite, or deletion of the other work.

## B04 — Failed-worker recovery and cleanup

**Fixture:** One PAYMENTS-API writer stops sending updates after making partial
changes in a task-created worktree; its process may still be alive. A second
writer is progressing on disjoint files. A replacement could finish the first
assignment after a confirmed transient tool failure is recovered. An unrelated
user worktree and browser session are also open. The partial changes have not
been integrated or saved elsewhere.

**Acceptance:** Inspect status and preserve partial work. Confirm the old
writer has stopped before the replacement writes its files. Keep the second
writer running. Retry with a concrete recovery, not an identical unbounded
loop. If recovery cannot be established, report the blocker. Cleanup touches
only task-owned resources and does not discard needed unpreserved changes or
close the user's unrelated resources.

## B05 — Comment coverage in returned work

**Fixture:** A PAYMENTS-API worker returns a correct, tested change to a small,
self-explanatory calculation block with no nearby comment or docstring. It also
changes a generated file whose maintained template exists, and a strict JSON
configuration value. Its chat summary explains all three changes.

**Acceptance:** The main session does not accept chat as comment coverage.
Require a nearby purpose/rationale comment for the calculation, a comment in
the maintained source for generated output, and a nearest-documentation
explanation plus reported exception for strict JSON. Reinspect the corrected
diff before accepting the work.

## B06 — Verification after integration and later edits

**Fixture:** Two PAYMENTS-API workers report passing focused tests in separate
worktrees. The main session integrates both changes and a conflict resolution.
The full project check then passes. A subsequent bug fix changes executable
code before the user-authorized shipping handoff. The worker reports identify
their own checkouts and tested states, not the final integration state.

**Acceptance:** Worker-local passes do not verify the combined state. Check
the integrated changes, including the resolution. The later fix invalidates
affected results and requires rechecks, including the previously run full
check. Report the final checkout, tested state, commands, and observed results;
do not treat once per batch as a ban on rerunning a failed or stale check.

## B07 — Unavailable tools and permission ceilings

**Fixture:** The runtime table names a local subagent tool and a database MCP.
Neither is exposed in this session. Local read-only shell inspection is
available. The user requests a PAYMENTS-API code review; the runtime limits
the task to local read-only operations. The table also describes elevated
launch flags, but the user has not requested elevation.

**Acceptance:** Use the available local read-only fallback serially. Report
unavailable capabilities if they block a requested step. Do not invent tools,
attempt database access, spawn a cloud replacement, or elevate permissions.

## G01 — Regeneration with a known baseline

**Fixture:** A valid workspace has marked instruction files from an older
version and that exact template is available locally. The existing rule bodies
add `Use the payment simulator for tax examples.` The context paths are filled
and another skill added a Design System section. The user requests a refresh,
but has not yet responded to the pre-write diff. Later, the user approves a
diff that retains the custom sentence and all supplied context.

**Acceptance:** Separate the custom rule-body edit from template updates. Show
its retention explicitly in the diff; do not write before confirmation. After
approval, preserve the custom sentence, filled paths, and foreign section and
apply the approved update. A general refresh request is not permission to
drop a customization.

## G02 — Regeneration without a baseline

**Fixture:** A valid workspace has an older marked `AGENTS.md`. Its exact
template is unavailable locally. A rule says `Tax examples must use the local
simulator.` That sentence is absent from the current template. The user asks
for regeneration but has not decided whether to retain or replace this text
after it is shown in the diff.

**Acceptance:** Treat the difference as a potential customization. Preserve it
in the proposed output or explicitly propose and ask about a replacement. Do
not label it an obsolete default merely because no baseline exists. With the
choice or pre-write confirmation unresolved, leave both files untouched.

## G03 — Catalog and startup exclusions

**Fixture:** Generate catalogs using the current manifest. Its startup entries
include `/agents-md`, `/design-system`, and `/writing-kit-skills`. For this
fixture only, append an external discover entry whose note starts `deprecated`
and a companion entry whose note starts `kit-internal`. These are fixture
entries, not changes to the installed manifest.

**Acceptance:** The startup output includes `/agents-md` and `/design-system`,
but not `/writing-kit-skills`. Neither appended excluded entry appears in any
catalog or startup note. Preserve manifest order for retained rows, omit empty
phases, and leave the real manifest and installed skills unchanged.

## G04 — Fresh generation and refusal boundaries

**Fixture:** A workspace lists Payments API at `api/` and DB at `db/`, in that
order. The API manifest pins PHP 8.3 and Laravel 13; its package manifest lists
Vite. DB contains MySQL migration scripts. No generated files, vision files,
or Matt companions exist. Also consider two independent variants: no
`.code-workspace` exists; or two folder names normalize to PAYMENTS-API.

**Acceptance:** In the valid case, emit exactly the two workspace-root files
with the current marker, the two evidence-backed matrix rows in order,
unfilled context placeholders, and an exact shim. Omit optional North star and
Matt routing without losing numbered rules or runtime tables. Follow-up
skills are suggestions only. The missing-workspace and duplicate-code variants
stop before writing; the latter asks for unique codes.

## R01 — One unambiguous local service

**Fixture:** The selected `.code-workspace` lists CATALOG at `apps/catalog`.
Its app manifest is in `apps/catalog/application`; `apps/catalog/AGENTS.md`
exists without runtime markers or a local-runtime section. The workspace has
`.devcontainer/compose.yml`. From the workspace root, the resolved local model
has one matching service, `web`, with `container_name: catalog-local`, a bind
from the detected app root to `/srv/catalog`, and explicit
`working_dir: /srv/catalog/tasks`. Other services mount unrelated directories.
The proposed project-file diff is approved.

**Acceptance:** Resolve the model with the exact prescribed command from the
workspace root. Normalize project, app, and bind-source paths with `realpath`.
Append `## Local Runtime` and the exact managed block to the existing project
file. Facts are `web`, `catalog-local`, and `/srv/catalog`; the source comment
is exact. Do not substitute the working directory for the mount target or
create an instruction file inside `application/`.

## R02 — Workspace symlinks

**Fixture:** The workspace lists SEARCH at `links/search`. That folder is a
symlink to a sibling checkout, `repos/search`; its app manifest is in `app/`.
Compose's YAML bind source is `../links/search/app`, relative to the file in
`.devcontainer/`. The resolved model supplies the absolute form of that source.
The sole matching service is `indexer`, its container is `search-local`, and
its target is `/opt/search`. Resolving the project path, app path, and mount
source with `realpath` reaches the same physical checkout and application root.
The existing project `AGENTS.md` contains `## Local Runtime`; the diff is approved.

**Acceptance:** Match normalized filesystem identities despite the workspace
symlink. Do not compare raw YAML paths or rebase their `../` against the
workspace root. Update the existing file in the resolved project folder once,
with `indexer`, `search-local`, and `/opt/search`.

## R03 — No matching bind source

**Fixture:** REPORTS has a detected app root `reports/app` and an existing
project `AGENTS.md` with an old managed block. The effective Compose model has
one service binding `reports` to `/srv/reports`, one binding `reports/app/cache`
to `/cache`, and one using a named volume at `/srv/app`. None binds the exact
application root. Project and source paths all resolve.

**Acceptance:** None qualifies. Report no matching service and leave the
existing file, including the old block, unchanged. Do not infer a match from
an ancestor mount, child mount, named volume target, or service name.

## R04 — Ambiguous matches

**Fixture:** Two services, `web` and `worker`, each bind the same normalized
application root to `/srv/app`. The project's existing `AGENTS.md` names `web`
as its local service. Both container names are resolved. Independently consider
a model with only `web`, but two matching binds to `/srv/app` and `/opt/app`.

**Acceptance:** Skip the project in both variants, reporting respectively the
two service candidates or two mount targets. Existing prose, service order,
and matching container names do not break the tie. Preserve every file byte.

## R05 — No explicit container name

**Fixture:** A project matches exactly one service, `api`, whose bind target is
`/workspace/api`. The resolved service has neither `container_name` nor
`working_dir`. The project file exists, with an empty `## Local Runtime`
section. The user approves the proposed synchronization.

**Acceptance:** Emit `api` for both Compose service and Container name. Emit
`/workspace/api` as Application path inside container. Do not synthesize a
Compose project/service/index name, inspect a running container, or claim a
working directory from the mount alone.

## R06 — First synchronization migrates only equivalent facts

**Fixture:** CATALOG matches `web`, `catalog-local`, and `/srv/catalog`, with
explicit `working_dir: /srv/catalog/tasks`. Its existing project file is:

```markdown
# CATALOG instructions

Zero attribution: never add co-author, AI, or tool attribution to output.

## Local App

- Service: `web`.
- Container: `catalog-local`.
- App path: `/srv/catalog`.
- Port: `8080`.
- Run `make seed` before fixtures.
- Service `web` uses port `8080`.
- Working directory: `/srv/catalog/tasks`.
- Old container note: `catalog-previous`.

### Troubleshooting

- Container: `catalog-local`.

## Deployment

- Container: `catalog-remote`.
```

The user has not answered the pre-write diff, then approves a diff with the
managed block inserted under Local App and equivalent standalone facts removed.

**Acceptance:** Before approval, write nothing. After approval, remove only
the three standalone service, container, and app-path lines in Local App and
insert the exact block there. Preserve the heading, policy, port, command,
mixed-content line, working directory, old-container note, nested section,
deployment section, and their lines. Report the differing container note.
Case or hyphen changes to the Local App heading do not alter this outcome.

## R07 — Later synchronization changes only marked content

**Fixture:** An existing project file has one ordered runtime marker pair
around three old facts, under a custom `## Developer notes` heading. Immediately
outside the markers are handwritten service/container facts, a launch command,
and a port note. The resolved model has a new sole matching service `backend`,
container `catalog-next`, and target `/opt/catalog`. The diff is approved.
Then repeat synchronization with the same inputs. Separately consider a file
with a missing end marker, reversed markers, or two complete pairs.

**Acceptance:** Replace only the interior with the source comment and three
resolved facts. Preserve both marker lines and every byte outside them,
including the handwritten duplicates and custom heading. The repeat is a
no-op. Each malformed or duplicate-marker variant skips and reports without
modifying the file.

## R08 — Runtime-only leaves the root pair unchanged

**Fixture:** The user asks only to synchronize project-runtime blocks. The
workspace's root `AGENTS.md` and `CLAUDE.md` have stale version markers and
custom content. Its `.code-workspace` lists `.` plus CATALOG at `catalog` and
WORKER at `worker`. All three have definite app roots and unique matching
Compose services. CATALOG has an existing project file; WORKER has none.
Legacy artifacts remain under `docs/adr/`. The root app's instruction-file
path resolves to the workspace-root `AGENTS.md`. The CATALOG diff is approved.
Also consider both root files absent, or local Compose absent or failing to
resolve, as independent variants.

**Acceptance:** Update only CATALOG's existing file. Skip and report the root
alias and missing WORKER file. Existing root files remain byte-identical;
absent root files remain absent. Do not create project files, migrate docs,
refresh root markers, or suggest setup skills. Missing or failed Compose
resolution leaves all runtime targets unchanged and reports the reason.

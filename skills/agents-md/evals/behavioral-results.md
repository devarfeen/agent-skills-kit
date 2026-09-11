# Behavioral results

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

## v26 project-runtime regression run

Date: 2026-09-11. Method: two independent read-only fixture evaluations of the
current skill and project-runtime reference. One covered R01–R05; the other
covered R06–R08 and root-mode regressions G01, G02, and G04. Evaluators received
only fixture inputs and source instructions, without acceptance checks, prior
results, or edit history. Decisions below are modeled outcomes, not executed
document edits. No installed instructions or real workspace files changed.

| Case | Observed modeled decision | Result |
| :--- | :--- | :--- |
| R01 | Uses the exact root-level Compose command and normalized app-root bind; appends the block with service, explicit container name, and mount target, keeping the distinct working directory out of the block. | PASS |
| R02 | Normalizes workspace symlink, physical project/app roots, and resolved source; matches the same checkout and updates its existing project file once. | PASS |
| R03 | Rejects ancestor, child, and named-volume matches; reports no service and preserves the old block unchanged. | PASS |
| R04 | Reports both service candidates or both mount targets and skips instead of using prose or service order to choose. | PASS |
| R05 | Uses the service key for an absent container name and makes no working-directory claim from the mount. | PASS |
| R06 | Waits for the shown diff's approval, removes only the three equivalent standalone facts, and preserves the policy, mixed content, commands, working directory, historical note, nested section, and deployment facts. | PASS |
| R07 | Replaces only the marker interior; retains outside bytes and duplicates, treats a repeat as a no-op, and skips malformed or duplicate markers. | PASS |
| R08 | Updates only the existing non-root project file; skips root aliases and missing project files, preserves root files or their absence, and performs no docs migration or setup suggestions. Missing/failed Compose produces no writes. | PASS |
| G01 | Preserves approved rule customizations, filled paths, per-project reads, and foreign sections through a normal root refresh. | PASS |
| G02 | Treats unknown-baseline differences as potential customizations and leaves files untouched while the decision is unresolved. | PASS |
| G04 | Generates the v26 root pair with the established optional-section rules when Compose is absent; missing-workspace and colliding-code variants stop before writing. | PASS |

Result: 11/11 modeled cases passed. Review identified two underspecified first-run
details: insertion position and whether approval already settles retention of a
conflicting handwritten fact. The reference now places the block after the
heading's existing blank lines and recognizes approval of the displayed retention
choice. Historical results and routing `last_run` metadata remain unchanged.

Live fixture checks ran `docker compose -f .devcontainer/compose.yml config
--format json` from an isolated fixture workspace inside this source repository,
then applied `realpath` to actual directories, a workspace symlink, and resolved
bind sources. Assertions passed for interpolation, exact app-root matching,
symlink equivalence, missing container-name fallback, rejection of ancestor/child
and named-volume matches, and two-service ambiguity. The resolved model retained
the distinction between bind target and explicit `working_dir`. No containers
were started. The temporary fixture was removed after the checks.

Byte comparisons confirmed both root template assets changed only at their
version marker for this update. Root skeleton, catalog, customization, approval,
migration, and output instructions retain their earlier text; runtime-only mode
explicitly bypasses those root operations. These checks validate instruction
consistency and real Compose/path inputs, not live document-edit reliability
across all CLI hosts.

## v23 regression run

Date: 2026-09-10. Method: two independent read-only simulated execution passes,
one for B01–B07 and one for G01–G04 in
[behavioral-cases.md](behavioral-cases.md). Each evaluator received the current
instructions and fixture inputs, without the acceptance checks, prior results,
or edit history. Returned decisions were then scored against every acceptance
check. No fixture commands ran, no workspace files were generated, and no
external mutations occurred.

| Case | Observed modeled decision | Result |
| :--- | :--- | :--- |
| B01 | Assigned worker reads applicable instructions and proceeds in its worktree; independent main session inside the project stops for the launch choice. | PASS |
| B02 | Reads and passes applicable nested instructions, uses tax docstrings within their scope, and rejects external publication under the fixture runtime's higher-priority local-only limit. | PASS |
| B03 | Preserves staged, unstaged, and untracked user work; re-reads the changed block, coordinates file ownership, and pauses only irreconcilable overlap while test work continues. | PASS |
| B04 | Inspects the silent writer, preserves its partial work, confirms it stopped before replacement writes, and retries after concrete recovery; unaffected work and unrelated user resources remain intact. | PASS |
| B05 | Rejects chat-only comment coverage; requires a nearby calculation explanation, a maintained-template comment, and a documented strict-JSON exception before accepting the corrected diff. | PASS |
| B06 | Verifies the integration state, invalidates affected results after the later code fix, and reruns focused and full checks before shipping with final-state evidence. | PASS |
| B07 | Uses the available local read-only fallback serially; neither invents unavailable calls nor elevates permissions or performs external operations. | PASS |
| G01 | Distinguishes the custom sentence using the exact old baseline, retains it and supplied context in the proposed diff, writes nothing before approval, then models the approved v23 update. | PASS |
| G02 | Treats the unmatched simulator rule as a potential customization without a baseline; proposes retention and leaves both files untouched while the decision is unresolved. | PASS |
| G03 | Retains only the two eligible startup entries, excludes internal/deprecated entries across all catalogs, preserves retained-row order, and omits empty phases without changing the real manifest. | PASS |
| G04 | Proposes two v23 root files with evidence-backed matrix rows and exact shim, preserves rules/runtime tables while omitting absent optional sections, and stops both refusal variants before writing. | PASS |

Result: **11/11 simulated cases passed.** In G04 the evaluator did not invent a
frontend package manager from Vite alone; a lockfile would be needed to add it.
Worker-stop evidence, preservation mechanisms, and logical comment-block
boundaries still require judgment in real execution. No material instruction
conflict was found within these fixtures. These results do not prove live
subagent recovery, filesystem merge safety, or compatibility across all six
CLI hosts.

Structural checks also passed: all 18 rule headings remain in order, untouched
rules and issue-title grammar retain their prior text, all four North star/Matt
omission combinations preserve rule links, and version markers agree at v23.
Repository validation passed checks 1–12 before the existing shell syntax
error at `tools/validate.sh:392` stopped the run. Checks 13 and 14 were checked
independently and passed; the validator itself was not changed. The standalone
skill validator could not start because PyYAML is unavailable. Trigger
descriptions and routing evidence were not changed or restamped.

## Historical v18 run

Date: 2026-09-09. Method: independent simulated execution of the revised skill and its relevant references. The reviewer did not author those changes. These are deliberately supplied fixtures and modeled actions, not live host, GitHub, herdr, or deployment transcripts. No external mutations occurred.

### Case 1: Workspace generation

Fixture: A workspace file lists Payments API at ./api and DB at ./db. api/composer.json pins PHP 8.3 and Laravel 13; its package manifest lists Vite. db contains MySQL migration scripts. No existing generated files or vision file; Matt companions unavailable.

Ordered actions: Read only listed workspace folders and their manifests. Produce the two v18 files, a two-row matrix in folder order, preserve Context placeholders, omit Matt routing and North star, and compare the shim to its template.

Simulated output: Matrix rows: PAYMENTS-API | api | PHP 8.3 / Laravel 13 / Vite / Composer + npm; DB | db | MySQL / raw SQL migrations. Follow-up suggestions only.

Result: PASS. The modeled decisions respect the skill's gates for this fixture.

### Case 2: Missing workspace boundary

Fixture: The current directory is a standalone Git repo with no .code-workspace file.

Ordered actions: Stop at Inputs before creating any file. Request a target folder containing a workspace file.

Simulated output: No files generated: no .code-workspace file is present.

Result: PASS. The modeled decisions respect the skill's gates for this fixture.

### Case 3: Colliding codes and hand edits

Fixture: Two folder names normalize to PAYMENTS-API. Existing marked AGENTS.md also contains user-filled context paths and a foreign Design System section; docs migration is declined.

Ordered actions: Stop on duplicate code before matrix emission. Preserve existing files. After a future unique-code decision, a regeneration diff must retain custom paths and the foreign section; declined docs moves remain untouched.

Simulated output: Needs user: provide distinct PROJECT-CODEs for the colliding folders. Existing instruction files and docs paths remain unchanged.

Result: PASS. The modeled decisions respect the skill's gates for this fixture.

Result: 3/3 simulated cases passed. This checks instruction consistency on these branches; it does not establish live runtime reliability. See [final.md](final.md) for remaining evidence gaps and scores.

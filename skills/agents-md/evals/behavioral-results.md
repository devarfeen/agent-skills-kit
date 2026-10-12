# Behavioral results

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

## v50 regression run

Date: 2026-10-12. Scope: the cases the `v50` changes touch — B15, B16, G04,
G06, G13, G14, G15, G16, G17, R08. Method: one independent evaluator read the
current `SKILL.md`, template, and references plus fixture text only, with the
acceptance checks withheld and `evals/` off limits, and modeled each case.
These are simulations, not evidence of guaranteed compliance in every runtime.

A first pass on the draft wording surfaced defects that were fixed before this
run: "never read `CLAUDE.md`" contradicted the competing-files report that has
to open it; the Rule 6 gate line forbade commits that Rule 18 allows locally;
the Codex note needed the user's global file, which the skill may not read; the
glossary collision check sat after approval; the unknown-origin question had no
place relative to the diff confirmation; startup lines had no list form.

| Case | Modeled decision | Result |
| :--- | :--- | :--- |
| B15 | Names both missing skills, stops at both gates, self-certifies nothing, ships nothing by hand, reports what is ready. | PASS |
| B16 | `/ci-loop` pushes its fix forward to the feature branch under the one approval; the third-party commit instruction is refused and handed off. | PASS |
| G04 | Writes `AGENTS.md` only with the `v50` marker and both matrix rows; both refusal variants stop before writing. The evaluator did not show `Composer` in the Stack cell and noted no rule derived it. | PASS, with that gap |
| G06 | Creates, edits, and deletes nothing in all four variants; classifies the marked redirect as removable and the import-less file as hiding the rules from Claude CLI; lists `GEMINI.md`. | PASS |
| G13 | Full diff, re-read detects the edit and shows the recomputed diff before writing; the failed-write variant reports the rename done and `AGENTS.md` unwritten. | PASS |
| G14 | States the byte size in both variants; adds the Codex setting only above 32768; edits no Codex configuration. | PASS |
| G15 | Lists rename, ADRs, and the reported-only README, asks first, rewrites only listed files, prints the README text edit; the collision variant reports both without merging. | PASS |
| G16 | Labels all five `origin unknown`, asks one set question before the confirmation, writes nothing until confirmed. | PASS |
| G17 | Cells joined by `<br>` with ` — ` and the note verbatim; a note-less skill stands alone; startup list items with one closing period. | PASS |
| R08 | Updates only CATALOG, skips the root alias and missing WORKER file, leaves the root file byte-identical or absent. | PASS |

Two wording fixes followed this run and were not re-evaluated: the PHP
stack-detection line now names Composer from `composer.json`, closing the G04
gap; the glossary collision line now says the colliding rename and its rewrites
leave the approval list. Open gaps the evaluator raised and this pass left
alone: no explicit "reconfirm" after a recomputed diff, no recovery step when
`AGENTS.md` fails to write after a rename, and no statement on whether a
`/ci-loop` push re-triggers the `/agentic-qa` gate.

Live evidence, separate from the simulation: codex-cli 0.162.1 was given a
45,860-byte `AGENTS.md` with a token at each end. At the default it returned
the head token and not the tail; with `project_doc_max_bytes=65536` it returned
both.

## v50 size-reduction run

Date: 2026-10-12, after the run above. Scope: the cases the size cuts touch —
B10, B16, B17, G03, G08, G11, G17, G18. Same method: one independent evaluator,
fixtures only, acceptance checks withheld. Simulations, not live evidence.

| Case | Modeled decision | Result |
| :--- | :--- | :--- |
| B10 | Refuses native isolation, adds the ignore rule, creates writer worktrees under `api/.worktrees/`, gives the explorer none, asks no separate approval. | PASS |
| B16 | Unchanged from the run above under the shorter Rule 18. | PASS |
| B17 | Without the worktree skill: creates the worktree with Git before any edit, leaves source changes alone, reports the gate record, never falls back. | PASS |
| G03 | Names-only gradient cells in manifest order, exclusions applied, two startup list items. | PASS |
| G08 | Keeps Matt routing, emits North star with the file and its PROJECT-CODE, deletes Graphify. | PASS |
| G11 | Exactly two tables; the elevated-permission table is not emitted. | PASS |
| G17 | Comma-joined names without notes; startup items with one closing period. | PASS |
| G18 | Lists exactly the four installed companions plus the fixed line; names the rest as not detected; Graphify block follows the graph's presence. | PASS |

One wording fix followed and was not re-evaluated: the worktree paragraph now
says to add `/.worktrees/` to the repository's `.gitignore` if missing, which
the evaluator had to infer from "gitignored there". Open gap left alone: no
rule says which commit an on-demand worktree starts from.

## v50 tightened-rules run

Date: 2026-10-12, after the two runs above. Every rule was reworded shorter and
three parts left the generated file (the parallel runtime table, use-when text
for skill companions, and the Matt routing lines that restated Matt's skills).
Scope: all sixteen template cases and G03, G08, G11, G17, G18. Same method: one
independent evaluator, fixtures only, acceptance checks withheld. Simulations,
not live evidence.

Result: 19 of 21 passed on the first pass. B10 and B17 failed.

| Case | Result | Note |
| :--- | :--- | :--- |
| B01–B09, B11, B13–B16 | PASS | B03 was modeled before a dropped Rule 14 sentence ("pause only overlapping work…") was restored; the modeled decision still met the check. |
| B10 | FAIL, then PASS | The shortened worktree paragraph said "gitignored there" without saying who adds the ignore rule. Restored; a second evaluator then added the rule and created both worktrees correctly. |
| B17 | FAIL, then PASS | "Through `/using-git-worktrees`" had lost its "without it, with Git" fallback, so the agent stopped. Restored; the second evaluator created the worktree with Git and reported the checkout record. |
| G03, G08, G11, G17, G18 | PASS | One runtime table; skill companions on one line, MCP and CLI companions in a table. |

One wording change followed the recheck and was not re-evaluated: "owns the
full checkout gate" became "owns the detailed checkout checks", because the
word "gate" collided with the Rule 6 line about gate skills. B07's fixture was
reworded afterwards, since it described runtime tables that are no longer
emitted. Open gaps the evaluators raised and this pass left alone: how a
worker's partial changes are preserved, how the companion install check maps a
server name to its manifest row, and no closing format for a gate-blocked task.

## v50 on-demand layout run

Date: 2026-10-13. The generated rules were split: `AGENTS.md` keeps the rules
every task needs plus a read-before table, and seven on-demand files hold the
rest. Scope: B04, B06, B09, B10, B11, B15, B16, B17, B18, G04, G17, G18, G19.
Method: one independent evaluator with the acceptance checks withheld. For the
template cases it started with `AGENTS.md` only and had to say which on-demand
file it read and when, applying only rules from files it had read.
Simulations, not live evidence.

Result: 13 of 13 passed. In every template case the evaluator read the
matching file before the action — `projects.md` at task start,
`orchestration.md` before delegating or creating a worktree,
`verification.md` before an edit, `shipping.md` before a commit, push, or
close — and left `browser.md` and `issues.md` unread when their action did not
come up. G19 moved a single-file `v46` layout across with the hand-kept code,
the filled glossary path, and the design-system section intact, and wrote
`AGENTS.md` last.

Two changes followed the run and were not re-evaluated. The folder was renamed
from `specs/agents/` to `rules/`, a path-only change. One sentence was added
for a gap G19 raised: a declined merge into a hand-written `projects.md` stops
before `AGENTS.md` is written. Open gaps left alone: the wayfinder label rule
sits in `issues.md`, which a close does not load; no ship skill only commits
and pushes without a PR or an issue close.

## v43 checkout gate regression

Date: 2026-10-01. The worktree rule now requires a reported checkout record,
binding for command directories and edit paths, and identity rechecks before
writes after handoffs or restarts. An independent evaluator read only the
current setup skill and template plus five fixtures; all five modeled
responses passed. Live local Git/path checks passed separately. Full evidence
and limits are recorded in
[worktree behavior checks](../../using-git-worktrees/evals/test-cases.md#2026-10-01-checkout-gate-results).
No harness-level write blocker is installed or claimed.

## v42 reporting gate regression

Date: 2026-10-01. Method: independent evaluator read the current template and
only the B13/B14 fixtures, without acceptance checks or prior results. These
are simulations, not evidence of guaranteed compliance in every runtime.

| Case | Observed decisions | Result |
| :--- | :--- | :--- |
| B13 | Update before implementation with four separate fields, state labels, worker counts and assignments; repeat within 60 seconds, bound waits, report completions, and verify combined work before closing. No unnecessary approval pause. | PASS |
| B14 | Immediately acknowledge the missed starting update before comparison, combine recovery with the phase transition, use `Needs user: None`, and send a closing update. Brevity and read-only scope do not waive the gate. | PASS |

Executed separately: `bash tools/validate.sh` and `git diff --check` passed.
A temporary local Git fixture demonstrated an ignored project-local worktree
at the recorded base, shared history with distinct checkout metadata, isolated
edits, and unchanged source branch, index, unstaged edits, and untracked file.
No remote operations were performed. The fixture remains under
`/tmp/worktree-demo-r4hqgl79/demo repo/.worktrees/isolation-demo` for inspection.

## v37 note — check layers and browser scope

Date: 2026-09-29. Rule 10 gains a check-layer choice (lowest layer that can
disprove the claim) and limits browser checks to UI and client-side claims;
persistence, authorization, tenant isolation, mail, and queues need automated
tests. Reports name the layers run and not run (Rules 3 and 10); read-only
tasks say `Verification: not applicable`. Rule 16 drops "a database row" from
browser assertions (it contradicted the test-suite line below it), keeps the
session name across shells and follow-up turns, and retries a failed flow in
the same session before any restart. Rule 11 cleanup names browser sessions;
Matt routing says "fresh agent session per ticket". Text-only change; no
behavioral case covers these lines.

## v36 note — agent-browser session and batch discipline

Date: 2026-09-29. Rule 16 gains: one session name for the whole task; a call
budget of about three for a simple smoke; `batch` input as quoted arguments or
a JSON array (plain lines fail with `Invalid JSON input`), with secrets passed
inside the JSON; an ignored-launch-flag warning treated as a failed start
(agent-browser prints it and continues without the flag); no `close --all`;
waits taken from the app's source; one login per run. Both behaviors were
verified on agent-browser 0.27.1 against a local page: a `jq`-built JSON batch
login completed in 0.6 s, and a launch flag on a running session printed
`--ignore-https-errors ignored: daemon already running` and continued. No
behavioral case covers these lines.

## v35 note — agent-browser lines restored to Rule 16

Date: 2026-09-29. Rule 16 keeps its v31 timeout wording and regains the three
v33 agent-browser additions: `batch --bail` as the flow mode,
`AGENT_BROWSER_DEFAULT_TIMEOUT` with condition waits and a ban on
`wait --timeout N`, and launch options on a session's first command. The v32
hang-guard wording stays out. Evidence: `wait --timeout N` measured at about
30 s and a failure regardless of N on agent-browser 0.27.1; the default-timeout
variable measured capping a missing-element wait at 3.2 s. A differential
fixture run (two independent evaluators per v31, v32, and v33 Rule 16, same
seller-login task) produced no `wait --timeout` under any version; the v33 text
halved agent-browser calls (9 against 17–22) through `batch --bail`. These were
written command plans from one model family, not executed runs. No behavioral
case covers these lines.

## v34 note — Rule 16 restored

Date: 2026-09-29. At the owner's request, Rule 16 (Efficient browser
verification) was restored byte-for-byte to its v31 text, removing the v32
timeout rewrite and the v33 agent-browser lines. Case B12, which asserted the
v32 timeout behavior, was withdrawn; its v32 result below stays as history. No
cases were re-run for this change.

## v32 regression run

Date: 2026-09-28. Method: three independent read-only fixture evaluations of the
v32 skill — B01–B13 against the template, G01–G13 against `SKILL.md` and the
references it points to, R01–R08 against `SKILL.md` plus the project-runtime
reference. Evaluators received only fixture text and source instructions,
without acceptance checks, prior results, or edit history, and were told not to
open `evals/`. Decisions below are modeled outcomes, not executed document
edits. No installed instructions or real workspace files changed.

| Case | Observed modeled decision | Result |
| :--- | :--- | :--- |
| B01 | Worker starts in its assigned worktree after reading instructions; independent main session warns, asks, and waits. | PASS |
| B02 | Reads all three instruction files before dispatch and passes them on; nested docstring rule stays in its scope; publish request not acted on. | PASS |
| B03 | Preserves staged, unstaged, and untracked user work; re-reads the changed file and pauses only the overlapping edit while tests continue. | PASS |
| B04 | Preserves partial work, confirms the stalled writer stopped before reassigning, keeps the second writer running, cleans only task-owned resources. | PASS |
| B05 | Rejects chat as comment coverage; requires calculation, template, and documented JSON-exception comments; reinspects before integration. | PASS |
| B06 | Treats worker passes as insufficient, verifies the integrated state, reruns the full check after the later fix, reports checkout and state. | PASS |
| B07 | Runs serially read-only, reports unavailable tools, no invented tools, database access, cloud agent, or elevation. | PASS |
| B08 | Fixes the rounding instead of loosening the assertion; for the obsolete test, explains and asks before changing it. | PASS |
| B09 | Names only `DB_PASSWORD`, asks approval for `migrate:fresh` by name, declines production access and hands the check to the owner. | PASS |
| B10 | First run: paused to ask about the `.gitignore` edit — FAIL. Cause: the shortened worktree rule said "after verifying `/.worktrees/` is gitignored" and dropped the instruction to add it. Fixed; rerun adds the entry, verifies, creates both writer worktrees with Git without asking, gives the explorer none, and rejects `isolation: worktree`. | PASS (rerun) |
| B11 | `/wayfinder` closes its own ticket and map; the delivery issue closes only through `/commit-push-close`. | PASS |
| B12 | First run: an 8 s cap cut off the 9 s budgeted route and the fired timeout was reported as a budget failure — FAIL. Cause: the rule gave budgeted routes no timeout above their budget. Fixed (about twice the budget); rerun measures 9 s under a 10 s timeout, records it against the 5 s budget, investigates, and keeps other commands within 3–8 s. | PASS (rerun) |
| B13 | One update with Stage/Found/Next/Needs user plus `Lanes: 2 running / 1 done / 0 blocked` and each running lane; no separate tag format. | PASS |
| G01 | Separates the custom sentence from template updates, shows it in a complete diff, writes nothing before approval, then preserves it, filled paths, and the foreign section. | PASS |
| G02 | Treats the unbaselined sentence as a potential customization; with the decision open, writes neither file. | PASS |
| G03 | Startup note keeps `/agents-md` and `/design-system`, drops `/writing-kit-skills` and both appended excluded entries; manifest order kept. | PASS |
| G04 | Emits the pinned Stack cells `PHP 8.3 / Laravel 13 / Vite / Composer` and `MySQL / raw SQL migrations`, an exact shim, no optional sections; both refusal variants stop before writing. | PASS |
| G05 | Leaves the hand-authored file in place and merges only the approved Project Matrix. | PASS |
| G06 | Emits the shim byte-for-byte when missing or stale; leaves a current matching shim untouched. | PASS |
| G07 | First run: the project-repository link was never searched, so it broke silently — FAIL. Cause: the migration reference forbade searching project repositories yet promised to report links found there. Fixed (read-only search, report only); rerun lists both moves and the root `README.md` rewrite, leaves `docs/site/`, reports `api/README.md` without rewriting it, and changes nothing on decline. | PASS (rerun) |
| G08 | Emits Matt routing and North star; North star lists `api/VISION.md` for PAYMENTS-API without restating it. | PASS |
| G09 | Treats the legacy comment as a marker, shows the complete diff, and replaces it with the current marker on approval. | PASS |
| G10 | Keeps `PAYMENTS-API` by path, proposes `PAYMENTS-SERVICE` only as a separate approval item, derives `BILLING-WEB` for the new folder. | PASS |
| G11 | Emits exactly the three specified tables and headers with the lead-in line before the third; no reference links. | PASS |
| G12 | Asks which workspace file to use before scanning. | PASS |
| G13 | Shows the full diff, detects the post-approval edit on re-read and re-shows the diff, and reports the partial write when `CLAUDE.md` fails. | PASS |
| R01–R08 | Same decisions as the v26 run, now resolving the model through the prescribed `jq`-filtered command. | PASS (8/8) |

Result: 34/34 modeled cases pass — 31 on the first run, B10, B12, and G07 after
rule fixes and fresh-evaluator reruns of those three cases. Each first-run
failure traced to rule text, not to evaluator error.

Clarifications applied after the passing runs, not separately re-evaluated:
worktrees sit "in each affected repo" (an evaluator read "one per affected repo"
as a count limit); the migration approval list now also shows project-repository
links that will be reported but not rewritten; a `null` `container_name` in the
filtered Compose model counts as absent. The undefined "per-project on-demand
reads" term cited in the v26 G01 result was removed from `SKILL.md`.

Open ambiguities raised by evaluators and left for a later pass: comma-separated
gradient cells whose notes contain commas; the insertion point for a section
merged into a hand-authored file; whether `.gitignore` counts as code under the
comment rule; the undefined local integration branch.

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

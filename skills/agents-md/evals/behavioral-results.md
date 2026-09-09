# Behavioral results

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Date: 2026-09-09. Method: independent simulated execution of the revised skill and its relevant references. The reviewer did not author those changes. These are deliberately supplied fixtures and modeled actions, not live host, GitHub, herdr, or deployment transcripts. No external mutations occurred.

## Case 1: Workspace generation

Fixture: A workspace file lists Payments API at ./api and DB at ./db. api/composer.json pins PHP 8.3 and Laravel 13; its package manifest lists Vite. db contains MySQL migration scripts. No existing generated files or vision file; Matt companions unavailable.

Ordered actions: Read only listed workspace folders and their manifests. Produce the two v18 files, a two-row matrix in folder order, preserve Context placeholders, omit Matt routing and North star, and compare the shim to its template.

Simulated output: Matrix rows: PAYMENTS-API | api | PHP 8.3 / Laravel 13 / Vite / Composer + npm; DB | db | MySQL / raw SQL migrations. Follow-up suggestions only.

Result: PASS. The modeled decisions respect the skill's gates for this fixture.

## Case 2: Missing workspace boundary

Fixture: The current directory is a standalone Git repo with no .code-workspace file.

Ordered actions: Stop at Inputs before creating any file. Request a target folder containing a workspace file.

Simulated output: No files generated: no .code-workspace file is present.

Result: PASS. The modeled decisions respect the skill's gates for this fixture.

## Case 3: Colliding codes and hand edits

Fixture: Two folder names normalize to PAYMENTS-API. Existing marked AGENTS.md also contains user-filled context paths and a foreign Design System section; docs migration is declined.

Ordered actions: Stop on duplicate code before matrix emission. Preserve existing files. After a future unique-code decision, a regeneration diff must retain custom paths and the foreign section; declined docs moves remain untouched.

Simulated output: Needs user: provide distinct PROJECT-CODEs for the colliding folders. Existing instruction files and docs paths remain unchanged.

Result: PASS. The modeled decisions respect the skill's gates for this fixture.

Result: 3/3 simulated cases passed. This checks instruction consistency on these branches; it does not establish live runtime reliability. See [final.md](final.md) for remaining evidence gaps and scores.

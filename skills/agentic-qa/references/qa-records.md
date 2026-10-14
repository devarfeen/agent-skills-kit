# QA records and fixtures

Zero attribution: never add co-author, AI, tool, or generator attribution to any output.

Read before fixture preparation or producing the QA report. Discover the target's evidence adapter from current instructions; use its supported result schema and manifest commands. Without an adapter, retain the same identities and checks in the report and manifest. Standalone installs do not assume a workspace script path.

## Fixture ownership

The builder or runtime repair owner prepares fixtures before the read-only tester starts. Use project factories, seeders, or verified fixture adapters against the binding's actual private data store. Check the current schema and required fields first; do not guess successive INSERT statements. Keep deterministic fixture values equal between BASE and HEAD while their stores remain separate.

Record fixture identifier, source/schema revision, task data identity, role and tenant references, setup command and producer exit status, and the permitted restore/cleanup command. Refer to credentials by key name. Required external services need their own task fixture or explicit unavailable result; permanent service data is not a fixture fallback.

For authorization rows, prove the permitted role can perform the same action and that the restricted role's effective grants deny it. Inspect both legacy and framework permissions when both determine access. Assert the server response and persisted state; a hidden button is insufficient. Tenant-isolation rows need a valid same-tenant control and a separate foreign-tenant record. Fixture failure goes to the repair owner before browser acceptance begins.

## Result and evidence identity

Record each cell's criterion, route/state/role/viewport, expected and actual result, assertion command or batch, diagnostics, evidence paths, coverage reason, and recheck count. Mark BASE target-defect results separately from HEAD acceptance. A schema validator checks completeness and consistency; it does not independently prove the assertions were executed.

Bind the report to checkout, full tested SHA and dirty source fingerprint when applicable, runtime/image, actual data target, dependency/asset identity, and producer exits. Preserve the run's structured `results.json` alongside the local readable report and grid. Use the adapter's generator when available; retain complete findings and unsupported checks. A failure, missing criterion, or unproved unreachable reason cannot produce a verified result.

Include only explicit reviewed artifacts in the publication manifest: the four routine desktop/phone BASE/HEAD PNG images, `results.json`, and any explicitly requested or approved extra image or PDF. `report.md` and `grid.md` stay local; the caller's readable QA comment carries the grid and result, with a `Checks:` line per gating check run. Build no ZIP or other archive. Derive MIME type, size, dimensions and hash from the actual files with a local tool; a caller's parent checks images by that metadata, never by reading image bytes. A file changed after review invalidates its sanitization/publication identity.

The publisher owns remote transactions under the calling workflow's authorization. Preserve local evidence until required remote bytes are read back and verified and the task is merged; result generation does not authorize posting, merging, or cleanup.

# Evidence publication

Zero attribution: never add co-author, AI, tool, or generator attribution to any output.

Read after QA produces artifacts or when resuming an interrupted publication. The QA worker in [`execution-and-continuity.md`](execution-and-continuity.md#qa-worker) runs this publication when the executor supports one. Starting `/factory run` authorizes sanitized evidence comments and uploads to the unit's own tracker; this reference grants no other remote writes. Workspace tracker restrictions override generic examples.

## Prepare once

Discover the target's evidence adapter and use its manifest, result-validation and publication-ledger operations. Without an adapter, keep an equivalent small durable record. Bind it to issue, exact checkout/full tested SHA and dirty source identity, runtime/data identity, and artifact hashes. Keep full observations in the local report and grid, rather than parent tool output.

The publication set is the four routine desktop/phone before/after PNG images and the structured `results.json`. `report.md` and `grid.md` stay local: the readable `## QA` comment carries the grid table and the result. Build no ZIP or other archive. Reuse these images across cells and review; no image per cell or unchanged retry. `no-ui-reach` and early blockers publish only their `results.json` and the comment, without invented images. An explicitly requested or approved additional image or PDF joins the declared set; report and grid never do.

Inspect every included file for sensitive data and publish reviewed copies. Allowlist paths inside the task evidence root, reject symlink escapes, and derive type, size, dimensions and hash from bytes with a local tool. The parent checks images by that metadata only and never reads image bytes into its context. Exclude credentials, cookies, env files and tool responses. Record withheld evidence and retain local originals.

## Resume the transaction

Key each artifact by tracker, issue, reviewed content hash and bound source/runtime identity. Keep prepare/upload/finalize/verified state durably after each successful action. Use live tool schemas; command names below are examples, not capability proof. Persist stable attachment IDs and approved durable asset references; signed upload/read URLs, headers and credentials stay outside the ledger and parent output.

For Linear, prepare one file through `prepare_attachment_upload`, PUT its bytes with exactly the returned headers before expiry, then finalize through `create_attachment_from_upload`. Capture HTTP/producer status; do not finalize a failed upload. Save the finalize intent before the remote call. A timeout or lost response requires listing/reconciling existing attachments before another finalize or upload, because the remote write may have succeeded.

Reuse verified matching files. Refresh expired temporary URLs through the live API. Retry an upload once only after diagnosis/re-preparation; unchanged failure is reported. On recovery, read existing attachment state once for the bounded issue/round, reconcile saved IDs and missing files, then resume the first incomplete action. Never repeat completed publication because the parent restarted.

Independent files may upload concurrently only when the live API and target policy support it, within runtime capacity. Each file still follows prepare → PUT → finalize → read-back, and its URL must remain valid. Otherwise use serial uploads. Do not launch one worker per screenshot.

Download required remote files and compare actual bytes, hash and media type with reviewed local copies. Provider metadata or an upload success alone is insufficient. Persist the verified attachment identity and reuse that proof unless source/runtime/artifact identity changes. An attachment reused from an earlier round is downloaded and re-verified under the current round's proof before that round counts as published or cleanup-ready. Before cleanup-ready, read the evidence adapter's proof-wide pending-verification list (each entry's path, state and whether it is a reused attachment that needs re-verification), re-verify every reused entry under the current proof, and only then request cleanup-ready. Without an adapter, keep the same list in the ledger. A remaining pending entry keeps local evidence and is reported.

An adapter may bind verification to the complete manifest. A changed artifact set then requires renewed downloaded-byte checks for retained attachments under that proof identity; reuse their remote IDs instead of uploading unchanged bytes again.

## Comment and retention

Format tracker records through [records.md](records.md). The issue comment names the full tested SHA, result, findings, rechecks and the `Checks:` block, carries the grid table and the result in readable form, and links the published images and `results.json`. Image rows name route, viewport, before/after and original durable asset links with previews. Use original asset URLs, never signed PUT/read URLs or local paths as publication proof. Read the comment back once and compare its required fields/links; an identical existing comment for that issue/head/set is reused.

If the tracker cannot attach files, state that limitation and retain local evidence; do not send it to another host. Generic GitHub-only users may post the report through `gh`, but `gh` does not upload issue images. A failed evidence upload does not change the QA result; missing required publication blocks local cleanup. Apply [qa-artifact-cleanup.md](qa-artifact-cleanup.md) only after merge and verified durable copies of the complete publication set.

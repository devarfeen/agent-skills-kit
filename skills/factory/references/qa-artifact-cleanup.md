# QA artifact cleanup

Zero attribution: never add or leave co-author, AI, tool, or generator attribution in any output.

Use during task evidence publication and after confirmed merge at factory cleanup, which runs automatically in every factory run. Local QA reports, grids, images and supporting files are temporary working evidence. Workspace policy owns their location and ignore rules; this procedure owns the factory cleanup step. Published issue/PR evidence remains durable.

## Identify the evidence

Resolve `<artifacts-root>`: the `*.code-workspace` directory if one exists, else the per-context root (`GLOSSARY-MAP.md` at repo root; legacy `CONTEXT-MAP.md`), else the repo root.

Record the exact task-owned QA folders and generated file list for each round, with issue, tested SHA and evidence links. Every round of the unit counts, including rounds superseded by a later head. Before dispatch, the parent verifies the owning repository ignores `/specs/qa/` and adds only the missing ignore entry under existing authorization. Preserve tracked files; ignoring them does not untrack history. Report any missing authority rather than writing elsewhere. Never commit temporary QA evidence. Pre-existing or shared/flat evidence requires a verified task-owned file list, not a broad folder assumption.

## Preserve durable proof

Starting a factory run approves publication of the sanitized publication set — the four routine PNG images, any approved extra image or PDF, and `results.json` — on its own issue/PR through the supported tracker workflow. `report.md` and `grid.md` stay local; the readable `## QA` comment carries the grid and result. Inspect files for sensitive data before publication; publish sanitized copies without weakening the recorded findings. Keep secrets, private runtime material and unreviewed files out of uploads.

Use [evidence-publication.md](evidence-publication.md) and the target evidence adapter for the complete manifest and resumable transaction. For Linear, each file follows prepare/PUT/finalize with its actual MIME type and byte size. Read each published file back, verify its bytes against the sanitized publication copy, and retain original asset links in the issue evidence comment. On other trackers use a supported durable publication method; local paths or expiring read links are not durable proof. Missing capability or failed publication keeps local files and is reported.

Record the full tested SHA, QA result, reproduction and required evidence on the issue/PR. After local cleanup, evidence references must still resolve there. A metadata-only attachment row does not establish publication. Required withheld/unpublished evidence prevents deletion; do not discard it to make cleanup pass.

## Delete only eligible local copies

After handover, confirm the PR is merged and its final head matches the unit's completed implementation. Check that every file of each recorded round's publication set, superseded rounds included, has a durable verified copy and that its `## QA` comment reads back. Attachments a round reused from an earlier round need their re-verification under that round's proof (see [evidence-publication.md](evidence-publication.md)) before the round is cleanup-ready: read the evidence adapter's proof-wide pending-verification list, re-verify every reused entry, then request cleanup-ready. A remaining pending entry retains local evidence and is reported. A blocked/unmerged task or incomplete/unreadable publication retains its local evidence. A no-UI result needs no invented artifacts; use its actual `results.json` and comment.

Resolve each recorded task folder under the owner's QA root. Reject the root itself, symlinks, paths resolving outside it, tracked files, and unrelated/unlisted contents. Recheck the generated file list against the filesystem before deletion. Remove only that task's verified local files, including the local-only report and grid, then its empty directories. Never delete the entire `specs/qa/` tree, use a recursive wildcard, or remove another task's evidence. Preserve published attachments, source code, round/lesson journals and research/decision documents.

Also remove the task's run-log directory `/tmp/<task-id>/` when the task adapter's destroy left it: resolve it exactly, reject symlinks and any other path, and never use a wildcard over `/tmp`. Verify the removed paths are absent and report the exact cleanup result. If deletion fails or an unlisted file appears, retain/report that folder; retry cleanup on a later authorized run without repeating delivery. Missing worktrees or branches do not prevent this evidence-only cleanup when merge, ownership and publication proofs still hold.

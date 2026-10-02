# Regeneration

Detail for refreshing an existing workspace-root `AGENTS.md`. The approval
gates live in `SKILL.md` under Versioning and regeneration; this file holds the
procedures they point to.

Zero attribution: never add or leave co-author, AI, tool, or generator
attribution in generated files or output.

## Reconcile customized rules

When an exact template for the existing marker is available locally, compare
against it to distinguish user edits inside generated rule bodies from template
updates. Without that baseline, treat differences as potential customizations,
not obsolete defaults. Show customizations and proposed resolutions explicitly
in the pre-write diff; retain them unless the user approves changing them. An
unresolved conflict or no response means stop without writing.

## Preserve foreign sections

Carry over verbatim any section another skill added (e.g.
`## Design System / UI Library` from `/design-system`, `## QA escape guards` from `/qa-escape`); regeneration replaces
only sections this skill generates.

## Migrate docs to specs

Artifact subfolders: `agents/`, `adr/`, `prompts/`, `qa/`, `port/`,
`pixel-audit/`, `integration/`, `design-system/`, `release-notes/` — strays
included. Non-artifact `docs/` content (for example a GitHub Pages site) stays.

1. **Build the approval list.** Search the artifacts root (the workspace root)
   for artifact subfolders under `docs/` and for files linking `docs/<sub>/`,
   excluding the Project Matrix project repositories. Search those
   repositories read-only for the same links. List every planned move, every
   file whose links would be rewritten, and every project-repository link that
   will be reported but not rewritten, then ask. Declined or no response → keep
   the `docs/` paths.
2. **Move.** On approval, `git mv` per subfolder (plain `mv` when untracked),
   merging file by file into any existing `specs/<sub>/` — never
   `git mv docs specs` wholesale.
3. **Rewrite links** from `docs/<sub>/` to `specs/<sub>/` only in the moved
   files and the files on the approved list, and update filled placeholder
   paths. Never rewrite a project-repository link; report each one again.
4. **Report** every move and rewrite. On a failed move or write, stop and report
   what moved and what did not.

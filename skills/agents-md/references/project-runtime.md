# Project runtime synchronization

Use for the default mode's project synchronization and for runtime-only requests.
This edits existing project instructions; it never creates project `AGENTS.md`
files. Derive every project, path, service, and container value from workspace
evidence. No project-specific defaults or name-based service guesses.

Zero attribution: never add or leave co-author, AI, tool, or generator attribution
in output. Preserve existing zero-attribution rules. The required neutral source
comment below describes the data source, not authorship.

## 1. Resolve the local model

Use the selected `.code-workspace` file's `folders` list, in order. When the
workspace-root `.devcontainer/compose.yml` exists, run this exact command from
the workspace root:

```sh
docker compose -f .devcontainer/compose.yml config --format json
```

Use the resulting `services` map, with interpolation and path resolution enabled.
Keep the full model transient; report only the needed runtime facts, not resolved
environment values. Do not start containers, inspect running containers, or use
staging/production files. An absent file, unavailable command, failed resolution,
or invalid JSON skips runtime synchronization with a reason; default root
generation remains independent. Runtime-only leaves the root pair untouched.

## 2. Match projects to services

- Resolve each folder path relative to the workspace root, then apply `realpath`.
  Find its application root using [stack detection](stack-detection.md), and
  apply `realpath` to that root too. Skip and report projects without a definite,
  resolvable application root.
- Inspect each service's `volumes` entries with `type: bind`. Apply `realpath`
  to the sources emitted by Compose; do not reinterpret relative YAML paths
  against the workspace root. Ignore and report unresolvable sources. Named
  volumes, ancestor mounts, and child mounts do not qualify.
- A service matches only when a normalized bind source **equals** the normalized
  application root. Require exactly one distinct service key and one distinct
  target for its matching mounts. Zero services, multiple services, or multiple
  target paths means skip that project and report the candidates or absence.
  Never select by image, folder name, container name, or `working_dir`.
- Target the existing `AGENTS.md` directly under the resolved project folder,
  not a file under its nested application root. Resolve the target path too;
  skip missing files and any alias of the workspace-root `AGENTS.md` or
  `CLAUDE.md`, including a `.` workspace entry. Process duplicate target paths
  once; conflicting matches for the same file mean skip and report.

## 3. Prepare the managed block

Fill exactly these three facts from the matched service and bind mount:

```markdown
<!-- agents-md:project-runtime:start -->
<!-- Source: resolved local Compose model. -->
- Compose service: `<service key>`.
- Container name: `<resolved container_name>`.
- Application path inside container: `<bind-mount target>`.
<!-- agents-md:project-runtime:end -->
```

When `container_name` is absent, use the service key. Do not synthesize a
Compose-generated container name. The application path is always the matching
mount's `target`, even if the service has a different `working_dir`. The mount
alone does not establish a working directory; only explicit Compose `working_dir`
can support that claim. Keep the managed block to the three facts above.

**First synchronization, no markers:** insert under an existing local-runtime or
local-app heading, allowing case, spacing, and hyphen variants. The section ends
at the next heading of equal or higher level. If none exists, append
`## Local Runtime` and the block. If several sections are plausible, skip and
report the ambiguity. Insert after the selected heading's existing blank lines,
before its first body line or child heading. Within that section, remove only standalone lines
containing exclusively equivalent handwritten service, container, or application
path facts: their meaning and values must match the resolved facts. Preserve
mixed-content lines, commands, different values, working-directory instructions,
nested sections, and every unrelated line. Report conflicting facts in the diff;
approval of a diff retaining them settles that choice without another question.
Do not clean up duplicate facts elsewhere in the file.

**Later synchronization, one ordered marker pair:** replace only the content
between the markers. Preserve the marker lines and every byte outside them,
including handwritten facts added later. Identical content is a no-op. Unpaired,
reversed, or multiple marker pairs mean skip and report; do not repair by guessing.

## 4. Show the diff, then apply approved changes

Include every project block insertion, replacement, and handwritten-fact removal
in the normal pre-write diff and approval flow. Project writes require approval
of that diff; honor approval already given for the same changes. No response,
declined changes, or unresolved conflicts means no affected project write.
Preserve the existing root-generation approval and customization rules.

Re-read targets before writing. If inputs or target contents changed since the
approved diff, recompute and show the affected diff again. Apply only approved
changes. Report changed, unchanged, and skipped projects with reasons. In
runtime-only mode, stop after that report; perform no root generation, root
marker refresh, artifact migration, or setup-skill suggestions.

## Completion checks

- Every updated block traces to one service and one target after `realpath`
  normalization; service-key fallback and the neutral source comment are exact.
- First synchronization preserves unrelated lines; subsequent synchronization
  preserves the marker lines and all bytes outside them. A repeat run is a no-op.
- No missing project instruction file was created. Every project edit appeared
  in the approved diff; skipped projects remain unchanged.
- Runtime-only leaves both root files byte-identical or absent as before.

Compose resolution semantics: [Docker Compose config](https://docs.docker.com/reference/cli/docker/compose/config/).

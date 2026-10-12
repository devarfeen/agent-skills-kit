# Frontmatter gates

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Load before changing descriptions or invocation flags.

- Any description, query, catalog, or invocation-policy edit, or a new skill, invalidates the eval-provenance snapshot (validate.sh check 10) and requires a completed trigger-eval sweep plus `score.py --write-snapshot` before it can land. The maintainer may run or explicitly delegate it. Batch description work; never invent or manually restamp `last_run`.
- User-invoked skills keep trigger descriptions too: Opencode and Antigravity ignore `disable-model-invocation`, so the description still routes there.
- Keep descriptions containing `: ` double-quoted. Check 1 requires PyYAML and strict YAML parsing; install `tools/requirements.txt` in a virtual environment before validation.

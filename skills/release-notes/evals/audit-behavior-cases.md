# Audit behavior cases

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

## Forward regression cases — not executed

These fixtures cover the current edit. They are expected decisions, not live
execution results or replacements for the catalog-only trigger evals.

| Case | Input and fixture | Required observable behavior |
| :--- | :--- | :--- |
| Mapped context without workspace file | A multi-context repo has GLOSSARY-MAP.md but no .code-workspace file. | Use the mapped context artifact root; do not force a per-repo fallback. |
| Uncommitted session only | The user requests a summary of current uncommitted edits; no delivery claim or commit history is needed. | Use session notes and relevant diffs with the session skeleton; do not load history-specific collection guidance. |

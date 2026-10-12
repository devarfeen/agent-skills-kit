# Audit behavior cases

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

## Forward regression cases — not executed

These fixtures cover the current edit. They are expected decisions, not live
execution results or replacements for the catalog-only trigger evals.

| Case | Input and fixture | Required observable behavior |
| :--- | :--- | :--- |
| Adopt existing UI skill | A project UI skill and tokens already exist; the user names a design source. | Extend the existing skill and token source, load doc/reference templates, and skip source-discovery and fresh-seed references. |
| No design source | No named source, root DESIGN.md, UI skill or component library exists; the user is away. | Load source-selection guidance, propose the guided definition, and stop before building without explicit approval. |

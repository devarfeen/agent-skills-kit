# Audit behavior cases

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

## Forward regression cases — not executed

These fixtures cover the current edit. They are expected decisions, not live
execution results or replacements for the catalog-only trigger evals.

| Case | Input and fixture | Required observable behavior |
| :--- | :--- | :--- |
| Changed row before proof | A page-local spacing edit is made; the served build has not been refreshed yet. | Set awaiting verification, not fixed or verified. Only passing the full element gate allows verified; final rows cannot remain awaiting verification. |
| Generated audit files | A single-page audit produces an inventory and defects file. | Both Markdown artifacts explicitly contain the zero-attribution rule; relevant ADRs are selected rather than bulk-read. |
| Adopted UI skill name | The design-system doc names an existing brand-ui skill rather than a *-ui-coding skill. | Read the registered real skill and reuse its library; do not miss it or seed a competing skill based on its name. |

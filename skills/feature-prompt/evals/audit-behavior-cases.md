# Audit behavior cases

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

These cases test execution decisions after the skill body is loaded. They are separate from the catalog-only trigger evals; a document review alone is not an execution pass.

| Case | Input and fixture | Required observable behavior |
| :--- | :--- | :--- |
| Unconfirmed draft | The user requested a prompt, its scope is inferable, and is now away. | Save the stated unconfirmed draft after read-back; do not require an approved draft that does not exist. |
| Context terms and no approval | Cheap exploration finds stale domain terminology; the user has not approved edits. | List evidence-backed candidates, retain uncertainty under Open questions, and save the prompt without editing GLOSSARY.md. |
| Existing prompt | A same-slug prompt contains user edits or its origin is uncertain. | Preserve it. Use a new numbered revision if the user is away; include zero attribution under Known limits. |

## Forward regression cases — not executed

These fixtures cover the current edit. They are expected decisions, not live
execution results or replacements for the catalog-only trigger evals.

| Case | Input and fixture | Required observable behavior |
| :--- | :--- | :--- |
| No optional constraints | A clear one-slice request has no extra constraints or open questions. | Still emit Known limits with the zero-attribution rule; omit only Open questions. |
| Independent numbering | ADRs end at 0007; prompt 0008 exists; the next ADR later uses 0008. | Create the next prompt at 0009; describe current occupancy rather than guaranteeing that future ADR numbers cannot overlap. |

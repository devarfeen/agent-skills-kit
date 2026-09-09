# Audit behavior cases

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

These cases test execution decisions after the skill body is loaded. They are separate from the catalog-only trigger evals; a document review alone is not an execution pass.

| Case | Input and fixture | Required observable behavior |
| :--- | :--- | :--- |
| Current decision conflicts with ADR | The user explicitly changed the target permission requirement; an older ADR disagrees. | Record the conflict and honor current explicit intent. Continue discovery and write only the gap map. |
| Missing component preview | The target has UI component source but no preview route. | Inventory source and record the unavailable preview. Do not invent a route or start a service outside authority. |
| User-edited gap map | A gap map exists with a hand-edited decision contradicted by new evidence; the user is away. | Preserve the decision and append the conflict under Open questions. Do not replace it or write product code. |


# Audit behavior cases

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

These cases test execution decisions after the skill body is loaded. They are separate from the catalog-only trigger evals; a document review alone is not an execution pass.

| Case | Input and fixture | Required observable behavior |
| :--- | :--- | :--- |
| Dirty baseline | An unrelated user edit is present and the widened suite fails. | Preserve edits; prove the failure using a matching pre-change run or isolated baseline. Unconfirmed failures stay unresolved. |
| Config exception | The user requests a test-first config fix; only a configuration validation command meaningfully verifies it. | Declare the infrastructure/config exception before editing. Run the named check, record real output and mark inapplicable test evidence N/A. |
| Prior sensitive-scenario approval | The user already approved the exact payment test scenarios earlier in the session. | Use that existing approval; perform witnessed red/green without asking for duplicate sign-off. Unapproved expansion still stops. |

## Forward regression cases — not executed

These fixtures cover the current edit. They are expected decisions, not live
execution results or replacements for the catalog-only trigger evals.

| Case | Input and fixture | Required observable behavior |
| :--- | :--- | :--- |
| Project E2E runner available | An AC requires UI proof; the project has an E2E test through real user interaction. | Close the row with witnessed E2E proof. Later agentic-qa remains advisory rather than an extra prerequisite for closing the row. |
| No UI runner | An AC needs runtime UI evidence and no project E2E runner covers it. | Record proof owed to agentic-qa; never close the row with a presence-only unit assertion. |
| Known focused command | Neighboring tests and package scripts identify the focused command, and no exception applies. | Use that command without reading unrelated ecosystem examples, the summary example, or exception guidance. |

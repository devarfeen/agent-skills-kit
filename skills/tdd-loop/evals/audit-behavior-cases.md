# Audit behavior cases

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

These cases test execution decisions after the skill body is loaded. They are separate from the catalog-only trigger evals; a document review alone is not an execution pass.

| Case | Input and fixture | Required observable behavior |
| :--- | :--- | :--- |
| Dirty baseline | An unrelated user edit is present and the widened suite fails. | Preserve edits; prove the failure using a matching pre-change run or isolated baseline. Unconfirmed failures stay unresolved. |
| Config exception | The user requests a test-first config fix; only a configuration validation command meaningfully verifies it. | Declare the infrastructure/config exception before editing. Run the named check, record real output and mark inapplicable test evidence N/A. |
| Prior sensitive-scenario approval | The user already approved the exact payment test scenarios earlier in the session. | Use that existing approval; perform witnessed red/green without asking for duplicate sign-off. Unapproved expansion still stops. |


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

## Reuse-first cases

Use fixture observations only; no real application, dependency installation,
or test run is authorized. Evaluate the chosen solution and test order rather
than matching wording. Record modeled results separately from runtime proof.

| Case | Input and fixture | Required observable behavior |
| :--- | :--- | :--- |
| T-1: Existing helper | A new display path must format file sizes with the existing binary-unit convention. `src/format-size.ts:3` implements that behavior; the new path is not wired to it. A package can also format sizes. | Reuse the helper without a package or wrapper. Observe the new path's failing behavior test before wiring it; preserve its edge behavior and run the normal focused/widened checks. |
| T-2: House component | A date field must use the project's inline error and keyboard behavior. `src/DateField.tsx:8` supplies both. A native input is shorter but lacks the required integration. | Use the project component. Fewer lines do not justify dropping requirements, validation, or accessibility. |
| T-3: Library choice | Variant A: no project helper exists; Python's standard library and an installed dependency both meet a filename-suffix requirement. Variant B: none of the inspected options meets an explicitly specified custom checksum. | A chooses the standard library. B adds only the missing checksum behavior with witnessed red/green and no speculative package or abstraction. |
| T-4: Declared config exception | Reusing an existing Compose setting fixes a configuration problem with no meaningful unit seam. The config exception and verification command are declared before editing. | Reuse does not cancel the exception or manufacture a failing unit test. Use the declared verification evidence and retain the follow-up plan. |

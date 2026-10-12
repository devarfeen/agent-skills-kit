# Audit behavior cases

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

These cases test execution decisions after the skill body is loaded. They are separate from the catalog-only trigger evals; a document review alone is not an execution pass.

| Case | Input and fixture | Required observable behavior |
| :--- | :--- | :--- |
| Nominal single project | The spec names API-SVC only, but ADMIN-WEB calls its changed endpoint. | Sweep Project Matrix consumers before deciding scope, create a contract and risk row for ADMIN-WEB, and stop after build. |
| Missing authority | Gate mode points to staging, with no approval or user-provided access; the application needs a rebuild. | Do not connect, rebuild, or seed. Record affected flows pending and block spec-level ship and PM handoff. |
| Unverified consumer and pending flow | One matrix repo is unavailable; one smoke driver is missing. | Record incomplete sweep and pending proof. Do not report no contract needed, all pass, or readiness for spec-level ship. |

## Forward regression cases — not executed

These fixtures cover the current edit. They are expected decisions, not live
execution results or replacements for the catalog-only trigger evals.

| Case | Input and fixture | Required observable behavior |
| :--- | :--- | :--- |
| Complete single-project sweep, no consumers | API-SVC changes a surface; all matrix repos are accessible and no consumer match is located anywhere. | Report single project — no contract needed, stop without a new file; do not also require a contract RISK row. |
| Historical no-longer-required contract | A previous cross-project contract has user edits and a gate log; a complete rerun finds no external consumers. | Preserve the old file/log, identify it as historical in the update, and create no new contract. |
| Gate on an intact contract | An existing contract has the four sections, risk flows and gate log; implementation/coverage has not changed. | Read the existing contract and gate guidance, not the build schema or filled example. Changed structure/coverage loads the schema before repairing it. |

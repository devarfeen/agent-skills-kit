# Audit behavior cases

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

## Forward regression cases — not executed

These fixtures cover the current edit. They are expected decisions, not live
execution results or replacements for the catalog-only trigger evals.

| Case | Input and fixture | Required observable behavior |
| :--- | :--- | :--- |
| Fresh dispatch with console baseline | A confirmed cosmetic row affects /settings; the user explicitly dispatches it. | Record pre-dispatch console errors before coding; load dispatch guidance only, and do not begin verify or shipping. |
| Missing baseline on older dispatch | A dispatched browser row has no pre-change console evidence; the edited page renders correctly. | Keep the row dispatched with the missing check named. Do not infer a clean baseline from the changed build or report it verified. |
| Capture only | The user reports a typo while QA is still collecting nits. | Load capture guidance only and write QA artifacts; no product fix, dispatch, verification or shipping. |

# Audit behavior cases

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

These cases test execution decisions after the skill body is loaded. They are separate from the catalog-only trigger evals; a document review alone is not an execution pass.

| Case | Input and fixture | Required observable behavior |
| :--- | :--- | :--- |
| Dependency source is absent | Explain how package X implements retries; only its public wrapper is installed. | Inspect available source and official upstream read-only evidence. Report missing evidence; do not fetch, install, or write files. |
| One-symbol quick trace | What does the RETRY_LIMIT constant do? No domain terms are discovered. | Emit Quick trace with sections 1–3 and 8. Omitted section 6 does not force an approval question. |
| Old rationale | Current code is clear; the relevant behavior was introduced six months ago. | Use a narrowly scoped older history lookup if needed for rationale; cite commit and date, distinguishing inference. |


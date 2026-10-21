<!-- agents-md marker · v55 · re-run /agents-md to regenerate -->
# Issues

Zero attribution: never add co-author, AI, or tool attribution to any output.

Read before creating, updating, or triaging an issue.

Titles live in the workspace's issue tracker of record (default: GitHub Issues). `<PROJECT-CODE>` is the Project Matrix code, used exactly.

- **Spec:** `Spec: <PROJECT-CODE> ADR-<adr-number> <adr-name>`, from the ADR filename in `specs/adr/` — `0042-stock-transfer-approvals.md` → `Spec: PAYMENTS ADR-0042 stock-transfer-approvals`.
- **Spec ticket:** `Ticket NNNN of <PROJECT-CODE> ADR-<adr-number> <adr-name> (#<spec-issue>): <Short heading>` — `NNNN` is four digits, local to the spec, from `0001`.
- **Wayfinder** map or ticket: `Way: <PROJECT-CODE> <destination or question>` — not numbered; parentage is the tracker's child link.
- **Non-spec:** `<PROJECT-CODE>: <short imperative heading>`.
- Legacy `PRD: …` and `Slice NNNN of …` titles are spec and ticket issues; never retitle them. No title carries `HITL:`, `AFK:`, or `BLOCKER:`.

**Labels.** Every triaged delivery issue carries exactly one category (`bug` or `enhancement`) and one state (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). `qa-escape` sits beside them and never replaces them. Wayfinder issues are planning artifacts: only `/wayfinder`'s own labels, closed before `/to-spec` runs, never a category or state label.

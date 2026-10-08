# Tracker map — GitHub and Linear

Zero attribution: omit co-author, AI, and tool attribution from all output. Inspect the live Linear tool schema before using the calls below; tool availability is not permission to write tracker state.

The workspace names the tracker once per run in **workspace-root `AGENTS.md`** or **`<artifacts-root>/issue-tracker.md`** — separate locations in meta workspaces (project Matrix folders have their own `AGENTS.md`; neither file lives there for this resolve).

|  | GitHub | Linear |
| :--- | :--- | :--- |
| `TRACKER_TAG` | `G` | `L` |
| `<n>` — native identifier | issue number: `42` | issue identifier: `PRWL-100` |
| `SPEC_REF` and `ISSUES` shapes accepted | `https://github.com/<owner>/<repo>/issues/42`, `<owner>/<repo>#42`, bare `#42` or `42` when the repo is unambiguous | `PRWL-100`, `ABC-123` |
| Access checked in pre-flight | `gh auth status` | the Linear MCP is connected — one `list_issues` call returns without an auth error |

## Resolve

1. **Workspace root** — the directory that holds the workspace's `.code-workspace` file. Walk up from the orchestrator's working directory when needed; a Project Matrix project checkout is not workspace root.
2. Read **workspace-root `AGENTS.md`** for the issue tracker of record.
3. Not named there → resolve `<artifacts-root>`: the `*.code-workspace` directory if one exists, else the per-context root (`GLOSSARY-MAP.md` at repo root; legacy `CONTEXT-MAP.md`), else the repo root; then read **`<artifacts-root>/issue-tracker.md`** when the file exists.
4. Neither names a tracker → GitHub Issues.
5. Named tracker → that is `TRACKER`. Set `TRACKER_TAG` from the table (`G` or `L`). One tracker for the whole run; every **Discover**, **Read issue**, **Block**, and **Verify** call uses that row's commands and identifier format.
6. `SPEC_REF`, `ISSUES`, and worker issue ids must be in that tracker's native form (GitHub URL/number or Linear identifier). If a step has no workspace mapping for a label or field, stop and ask — never fall back to `gh issue` when `TRACKER` is Linear, or the reverse.

Both trackers use the same `<PROJECT-CODE>` issue-title species and the same `ready-for-agent` / `ready-for-human` state labels. Only the commands and the identifier format differ.

## Discover

Open sub-issues of `SPEC_REF`. With `ISSUES`, skip the sub-issue listing: read each listed issue per **Read issue**, drop any that is closed and say so, then read the blocking relations below among the listed issues.

- **GitHub** — `gh api --paginate repos/<owner>/<repo>/issues/<n>/sub_issues --jq '.[] | select(.state=="open") | .number'`. Fall back to task-list checkboxes and "Tracked by" references only when native sub-issues are unavailable, then fetch each linked issue and verify its state.
- **Linear** — `get_issue` on `SPEC_REF` first, then `list_issues` with `parentId: <parent internal id>`, requesting the `title`, `url`, `status`, and `statusType` fields. Follow every returned next-page cursor. Open = `statusType` is neither `completed` nor `canceled`; `triage`, `backlog`, `unstarted`, and `started` all count as open. Read each result's identifier (`PRWL-101`) as `<n>`. Fall back to checkbox lists and issue links only when the native relation is unavailable, verifying each linked issue's state.

**Blocking relations** — for each open sub-issue, read what blocks it, and keep only blockers that are themselves in this run's open set:

- **GitHub** — `gh api --paginate repos/<owner>/<repo>/issues/<n>/dependencies/blocked_by --jq '.[] | select(.state=="open") | .number'`.
- **Linear** — `get_issue` with `id: <n>` and `includeRelations: true`; read the blocked-by relations.

An unavailable relation is a gap to state in the Intake question, never proof of independence.

Deduplicate identifiers after pagination and verify fallback links belong to this parent before counting them. Zero open sub-issues → stop before Intake and before launching threads; suggest `/to-tickets` or a different parent.

## Read issue

The worker prompt needs each issue's identifier and URL; read the body only if the prompt needs to quote it.

- **GitHub** — `gh issue view <n> --json number,title,body,url`
- **Linear** — `get_issue` with `id: <n>`

## Block

A worker blocked on a human decision gets its issue flipped to `ready-for-human` with a comment naming the decision. Never edit issue titles.

- **GitHub** — `gh issue edit <n> --add-label ready-for-human --remove-label ready-for-agent`, then `gh issue comment <n> --body "<the decision the worker needs>"`.
- **Linear** — `save_issue` with `id: <n>`, `removeLabels: ["ready-for-agent"]`, and `addLabels: ["ready-for-human"]` when the live schema supports them. Otherwise read current labels and replace only those two values; `labels` replaces the whole set. Then `save_comment` with `issueId: <n>` and the decision as `body`. Create no new label; no mapped `ready-for-human` equivalent means stop and ask.

## Verify

Read-back for the completion criteria — quote what these return, never assert from memory.

- **GitHub** — `gh issue view <n> --json state,title,labels,comments`
- **Linear** — `get_issue` with `id: <n>` for status, title, and labels; use the live comment-list tool to verify the decision comment if issue details omit comments.

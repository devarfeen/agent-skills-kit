# Tracker map — GitHub and Linear

The workspace's `AGENTS.md` (or its rules files) names the issue tracker of record. Default: GitHub Issues. Resolve it once in pre-flight; every issue read and write in the run then goes through that tracker, using its identifier format and label vocabulary as the workspace docs map them. If a step has no workspace mapping, stop and ask — never fall back to `gh issue` against a tracker the workspace does not use.

|  | GitHub | Linear |
| :--- | :--- | :--- |
| `TRACKER_TAG` | `G` | `L` |
| `<n>` — native identifier | issue number: `42` | issue identifier: `PRWL-100` |
| `SPEC_REF` shapes accepted | `https://github.com/<owner>/<repo>/issues/42`, `<owner>/<repo>#42`, bare `#42` or `42` when the repo is unambiguous | `PRWL-100`, `ABC-123` |
| Access checked in pre-flight | `gh auth status` | the Linear MCP is connected — one `list_issues` call returns without an auth error |

## Resolve

1. Read the workspace `AGENTS.md` (meta workspace root) for the tracker of record. Named → that is `TRACKER`. Not named → GitHub.
2. Cross-check `SPEC_REF`'s shape against it. A `PRWL-100` under a GitHub workspace, or a GitHub issue URL under a Linear workspace, is a conflict → stop and ask which is right. Never infer the tracker from the argument alone — the workspace rules win, and a silent switch would fan out against the wrong tracker.
3. Set `TRACKER_TAG` from the table. It is `G` or `L` for the whole run: one tracker per fan-out, never a mix.

Both trackers use the same `<PROJECT-CODE>` issue-title species and the same `ready-for-agent` / `ready-for-human` state labels. Only the commands and the identifier format differ.

## Discover

Open sub-issues of `SPEC_REF`.

- **GitHub** — `gh api repos/<owner>/<repo>/issues/<n>/sub_issues --jq '.[] | select(.state=="open") | .number'`. Fall back to task-list checkboxes and "Tracked by" references in the spec body.
- **Linear** — `list_issues` with `parentId: <SPEC_REF>`, requesting the `title`, `url`, `status`, and `statusType` fields. Open = `statusType` is neither `completed` nor `canceled`; `triage`, `backlog`, `unstarted`, and `started` all count as open. Read each result's identifier (`PRWL-101`) as `<n>`. Fall back to checkbox lists and issue links in the parent's description.

## Read issue

The worker prompt needs each issue's identifier and URL; read the body only if the prompt needs to quote it.

- **GitHub** — `gh issue view <n> --json number,title,body,url`
- **Linear** — `get_issue` with `id: <n>`

## Block

A worker blocked on a human decision gets its issue flipped to `ready-for-human` with a comment naming the decision. Never edit issue titles.

- **GitHub** — `gh issue edit <n> --add-label ready-for-human --remove-label ready-for-agent`, then `gh issue comment <n> --body "<the decision the worker needs>"`.
- **Linear** — `save_issue` with `id: <n>` and `labels:` set to the issue's current labels with `ready-for-agent` dropped and `ready-for-human` added; `labels` **replaces** the whole set, so read the current labels first or you will silently strip them. Then `save_comment` with `issueId: <n>` and the decision as `body`. Create no new label — the workspace's label vocabulary is fixed; no `ready-for-human` equivalent mapped → stop and ask.

## Verify

Read-back for the completion criteria — quote what these return, never assert from memory.

- **GitHub** — `gh issue view <n> --json state,title,labels`
- **Linear** — `get_issue` with `id: <n>`; check its status, title, and labels, and that the decision comment is present.

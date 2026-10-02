# Fetching review threads

Review threads — with thread IDs and resolved state — exist only in GraphQL:

```bash
gh api graphql -f query='query { repository(owner:"<owner>", name:"<repo>") {
  pullRequest(number:<num>) { reviewThreads(first:100) {
    pageInfo { hasNextPage endCursor }
    nodes {
    id isResolved isOutdated path line
    comments(first:50) {
      pageInfo { hasNextPage endCursor }
      nodes { databaseId author { login } body } } } } } } }'
```

Re-query `reviewThreads` with its own `after: <endCursor>` until exhausted. For each thread whose comments have another page, query that thread by its node ID and paginate its `comments` connection independently. Deduplicate by comment ID.

Top-level review bodies and issue-style PR comments:

```bash
gh api --paginate repos/<owner>/<repo>/pulls/<num>/reviews
gh api --paginate repos/<owner>/<repo>/issues/<num>/comments
```

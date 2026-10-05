# Risk rubric

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

The tier is decided here, not by judgement. Any one high-risk trigger → `high`. No trigger and zero blocking findings → `low`.

## Lens selection

Pick a lens when any of its signals appears in the changed paths or diff content. Adjust the path patterns to the repository's layout; the categories don't change.

| Lens | Path signals | Content signals |
| ---- | ------------ | --------------- |
| `data` | `migrations/`, `db/`, `schema.*`, `*.sql`, `prisma/`, `models/`, seeders, factories | `ALTER TABLE`, `DROP`, column or index changes, raw queries, ORM relationship changes, bulk updates or deletes |
| `contract` | API routes, controllers, resources, serializers, DTOs, generated clients, event or webhook schemas, `*.proto`, OpenAPI files | response or request field added, renamed, removed, or retyped; status code change; route change; enum value change |
| `infra` | `Dockerfile*`, `docker-compose*`, `.github/workflows/`, `nginx/`, `Procfile`, queue and cron config, `.env.example` | env var added or renamed, worker or schedule changes, build or runtime image changes, resource limits |
| `cloud` | `terraform/`, `*.tf`, `cdk/`, `pulumi/`, `k8s/`, `helm/`, `serverless.*` | IAM or role policy, network or security group, storage bucket ACL, DNS, autoscaling |
| `security` | `auth/`, middleware, policies or guards, `routes/`, controllers handling user input, session and cookie config, CORS config | permission checks, token or password handling, input validation removed, file upload, redirects built from input, secrets or keys in code |

## High-risk triggers

Each trigger that fires is recorded with the `file:line` that fired it.

1. **Schema or data change** — any migration, or code that bulk-mutates or deletes stored data.
2. **Auth or permission path** — any change to authentication, authorization, session, token, or role logic.
3. **Money** — pricing, billing, invoicing, payment, tax, or currency arithmetic.
4. **Public contract** — an API route, request or response shape, webhook payload, event schema, or SDK surface used outside this PROJECT-CODE.
5. **Config, secrets, or infrastructure** — env vars, CI/CD workflows, container images, IaC, queue or cron schedules.
6. **Removed behaviour** — deleted endpoints, deleted feature code paths, or deleted tests.
7. **Cross-project change** — the PR, or its spec, touches more than one PROJECT-CODE.
8. **Dependency change** — a new dependency, or a major-version bump of an existing one.
9. **Size** — more than 400 changed lines excluding lockfiles and generated files, or more than 20 files.
10. **Out of scope** — any change that the ticket's acceptance criteria do not cover.
11. **Unproven acceptance** — the diff can reach a screen and no agentic-qa `verified` marker exists for the head SHA; or the PR's acceptance verdict is missing, or lists a criterion pending manual or deferred for any reason other than `/agentic-qa` pending.

12. **One-way door** — the author's `Door:` line says `one-way`; or it says `two-way` and the diff contains a one-way change: a migration with no working down path, a statement that drops, truncates, or rewrites stored data, a send to an external party (email, payment, webhook, third-party write) on a path the change newly reaches, a removed or renamed public contract, or a rotated or revoked credential. Record the claim, the verdict (`confirmed` or `contradicted`), and the `file:line`. No `Door:` line → this trigger does not fire; triggers 1, 4, and 6 still judge the content.

Docs, tests that only add coverage, copy changes, and styling with no logic change fire no trigger on their own.

## Lens checklists

Lanes check these and report only findings with a concrete failure scenario.

- **contract** — for each changed shape, route, status, or enum, find its consumers: generated client first, then a search for the normalized route (`${id}`, `:id` → `{id}`) and the field name under the serializer's naming policy. Label each match `generated`, `normalized-route`, or `name-only`. A consumer that reads a field, status, or route the producer no longer returns is **blocking** — it renders `undefined` or a broken screen. No consumer found → say "no consumer located" with the searches run; never assume none exists.
- **data** — trace every renamed, retyped, or dropped table, column, view, or procedure to its dependents: other SQL objects including dynamic SQL, application code, and scheduled jobs, reports, exports, and integrations. Label each `direct`, `indirect`, or `uncertain`; an uncertain job or report is a blocking "verify" item. For each schema or event change, walk the rollout: old writer → new reader, new writer → old reader, rollback after new writes, old stored data read by new code. Record the result as `compatible`, `rollout-dependent — <order>`, `breaking`, or `insufficient context`; never call a change compatible from the new schema alone. Lock duration: an index or `ALTER` on a large table without the engine's online option (`CONCURRENTLY`, `ALGORITHM=INPLACE`) is blocking. Also: migration reversible; new non-null columns have defaults or a backfill; indexes for new query paths; no N+1 introduced; destructive statements guarded; transactions around multi-step writes.
- **infra** — env vars checked both ways: every newly read variable is in each environment's example and deploy config, and every newly documented one is read by code something imports; for `.github/workflows/` changes, a privileged trigger (`pull_request_target`, `workflow_run`, `issue_comment`) that checks out and runs PR code, or `${{ github.event.* }}` used directly inside `run:`, is blocking; so are `permissions:` widened to `write-all` or to write scopes no step needs, a third-party action moved to a branch ref, and untrusted input written to `$GITHUB_ENV` or `$GITHUB_OUTPUT` — a fork `pull_request` running PR code is not a finding; workflow triggers and branch filters still match intent; image tags pinned; schedules and worker counts unchanged unless intended.
- **cloud** — least-privilege on any policy change; no resource made public; changes are additive or have a stated rollout; state-file and drift implications named.
- **security** — every new route has an authorization check; object-level access: a record loaded by ID is scoped to the caller's owner or tenant — an unguessable ID is not authorization; webhooks verify the signature on the raw body; secrets are compared in constant time; user input validated at the boundary; no secret in code or logs; no open redirect, SSRF, or path traversal from new inputs; error messages leak no internals.

## Evidence rules for every lane

- The cited `file:line` must literally contain the symbol or statement the finding names.
- An absence finding ("no auth check", "env var missing") lists every place searched. One search with no match is not evidence of absence.
- Before marking a finding blocking, check whether middleware, a framework default, or an upstream guard already handles it.
- A count ("3 consumers") appears beside the command that produced it.
- A dismissed finding needs a passing assertion or a quoted line proving the dismissal, not an argument.

## Examples

- Copy fix in a Blade view, 3 lines, agentic-qa `verified` on head → no trigger → `low`.
- New nullable column with a migration → trigger 1 → `high`, even though the migration is safe.
- Refactor of an invoice total helper with full tests → trigger 3 → `high`.
- A PR whose body says `Door: two-way` while its migration drops a column → trigger 12 (`contradicted`) and trigger 1 → `high`.
- Button copy change on a settings page, verified grid on head → no trigger → `low`; the same change with no agentic-qa marker → trigger 11 → `high`.

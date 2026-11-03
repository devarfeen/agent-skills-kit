#!/usr/bin/env bash
# Zero attribution: never add or leave co-author, AI, or tool attribution in any output.
# Wait for a PR's CI checks to appear, then watch them until they finish.
# Right after a push, `gh pr checks --watch` exits at once with "no checks
# reported"; this retries until the run registers.
# Usage: tools/wait-checks.sh <pr-number> [seconds-to-wait-for-checks, default 120]
# Exit: 0 all checks passed; non-zero a check failed, or no checks appeared in time.
set -euo pipefail
pr="${1:?usage: tools/wait-checks.sh <pr-number> [seconds]}"
limit="${2:-120}"
deadline=$((SECONDS + limit))
while out="$(gh pr checks "$pr" 2>&1)"; [[ "$out" == *"no checks reported"* ]]; do
  if (( SECONDS >= deadline )); then
    echo "wait-checks: no checks appeared on PR $pr within ${limit}s" >&2
    exit 3
  fi
  sleep 5
done
exec gh pr checks "$pr" --watch --interval 10

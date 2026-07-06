#!/usr/bin/env bash
# Emit the routing catalog: kit skill names + descriptions read live from
# skills/*/SKILL.md frontmatter, plus the pinned external/companion snapshot.
set -eu
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

echo "# Routing catalog"
echo
echo "## Kit skills"
echo
for f in "$ROOT"/skills/*/SKILL.md; do
  fm="$(awk 'NR==1 && /^---$/{n=1; next} /^---$/{exit} n==1{print}' "$f")"
  name="$(printf '%s\n' "$fm" | sed -n 's/^name:[[:space:]]*"\{0,1\}\([^"]*\)"\{0,1\}[[:space:]]*$/\1/p' | head -1)"
  desc="$(printf '%s\n' "$fm" | sed -n 's/^description:[[:space:]]*//p' | head -1 | sed 's/^"//; s/"$//')"
  printf -- '- **/%s** — %s\n' "$name" "$desc"
done
echo
cat "$ROOT/tools/trigger-evals/catalog-externals.md"

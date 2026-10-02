#!/usr/bin/env bash
# Install this kit's skills, and optionally the companion skills it credits,
# through the `skills` CLI (npx skills add).
# Zero attribution: never add co-author, AI, or tool attribution to outputs.
#
# Usage: bash tools/install-skills.sh [options]
#   --group <name>   Kit group to install: manual-workflow or factory-workflow.
#                    Repeatable. Default: every group in .claude-plugin/marketplace.json.
#   --no-kit         Skip this kit's skills.
#   --companions     Also install the companion skills listed below.
#   --project        Install into the current project instead of globally (-g).
#   --local          Install kit skills from this checkout instead of GitHub.
#   --dry-run        Print the commands without running them.
#   -h, --help       Show this help.

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
KIT_SOURCE="devarfeen/agent-skills-kit"

# Companion skills by source — keep in step with README "Credits And Provenance".
COMPANIONS=(
  "anthropics/skills|mcp-builder skill-creator frontend-design"
  "mattpocock/skills|ask-matt claude-handoff code-review codebase-design diagnosing-bugs domain-modeling git-guardrails-claude-code grill-me grill-with-docs grilling handoff implement implement-spec improve-codebase-architecture loop-me migrate-to-shoehorn pr prototype research retro scaffold-exercises setup-matt-pocock-skills setup-pre-commit setup-ts-deep-modules tdd teach to-questionnaire to-spec to-tickets triage wait-what wayfinder wizard writing-beats writing-for-agents writing-fragments writing-shape"
  "vercel-labs/agent-browser|agent-browser"
  "vercel-labs/skills|find-skills"
  "cursor/plugins|blast-radius show-me-your-work unslop"
  "github/awesome-copilot|boost-prompt"
  "google-labs-code/stitch-skills|enhance-prompt"
  "herdrdev/herdr|herdr"
  "pbakaus/impeccable|impeccable"
  "sickn33/agentic-awesome-skills|docker-expert"
)

groups=()
kit=1
companions=0
scope=(-g)
dry_run=0
kit_source="$KIT_SOURCE"

usage() { sed -n '2,15p' "$0" | sed 's/^# \{0,1\}//'; }

while (($#)); do
  case "$1" in
    --group) [[ $# -ge 2 ]] || { echo "--group needs a name" >&2; exit 2; }; groups+=("$2"); shift 2 ;;
    --no-kit) kit=0; shift ;;
    --companions) companions=1; shift ;;
    --project) scope=(); shift ;;
    --local) kit_source="$ROOT"; shift ;;
    --dry-run) dry_run=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

command -v npx >/dev/null 2>&1 || { echo "npx not found — install Node.js first." >&2; exit 1; }

run() {
  printf '+ %s\n' "$*"
  ((dry_run)) || "$@"
}

# Skill names for the requested kit groups, read from marketplace.json.
kit_skills() {
  node -e '
    const m = require(process.argv[1]);
    const want = process.argv.slice(2);
    const known = m.plugins.map(p => p.name);
    const bad = want.filter(w => !known.includes(w));
    if (bad.length) { console.error(`Unknown group: ${bad.join(", ")} (known: ${known.join(", ")})`); process.exit(2); }
    for (const p of m.plugins) {
      if (want.length && !want.includes(p.name)) continue;
      for (const s of p.skills) console.log(s.split("/").pop());
    }
  ' "$ROOT/.claude-plugin/marketplace.json" "${groups[@]}"
}

failed=()

if ((kit)); then
  mapfile -t names < <(kit_skills)
  ((${#names[@]})) || { echo "No kit skills matched." >&2; exit 2; }
  run npx -y skills add "$kit_source" -s "${names[@]}" "${scope[@]}" -y || failed+=("$kit_source")
fi

if ((companions)); then
  for entry in "${COMPANIONS[@]}"; do
    src="${entry%%|*}"
    read -r -a names <<< "${entry#*|}"
    run npx -y skills add "$src" -s "${names[@]}" "${scope[@]}" -y || failed+=("$src")
  done
  echo "Graphify is installed separately: https://github.com/Graphify-Labs/graphify"
fi

if ((${#failed[@]})); then
  printf 'Failed sources: %s\n' "${failed[*]}" >&2
  exit 1
fi

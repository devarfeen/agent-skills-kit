#!/usr/bin/env bash
# Validate the agent-skills-kit repo invariants.
#
# Run from anywhere: bash tools/validate.sh
# Exits non-zero on any failure. No dependencies beyond coreutils + grep.
#
# What it enforces (see CONTRIBUTING.md for the why):
#   1. Every skills/<dir>/ has a SKILL.md with `name:` + `description:` frontmatter;
#      name matches the folder and is kebab-case.
#   2. The two ship-policy.md copies are byte-identical.
#   3. Every skill folder has a row in skills/agents-md/references/skills-manifest.md.
#   4. Every skill folder is mentioned in the root README.md.
#   5. Relative markdown links resolve to real files.
#   6. No AI/tool attribution has leaked into the repo (zero-attribution policy).

set -u

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
FAIL=0

fail() { printf 'FAIL: %s\n' "$*"; FAIL=1; }
note() { printf '  ok: %s\n' "$*"; }

echo "== 1. SKILL.md frontmatter =="
for dir in skills/*/; do
  name="$(basename "$dir")"
  skill_md="${dir}SKILL.md"
  if [[ ! -f "$skill_md" ]]; then
    fail "$dir is missing SKILL.md"
    continue
  fi
  if [[ "$(head -1 "$skill_md")" != "---" ]]; then
    fail "$skill_md must start with '---' frontmatter on line 1"
  fi
  fm="$(awk 'NR==1 && /^---$/{n=1; next} /^---$/{exit} n==1{print}' "$skill_md")"
  fm_name="$(printf '%s\n' "$fm" | sed -n 's/^name:[[:space:]]*"\{0,1\}\([^"]*\)"\{0,1\}[[:space:]]*$/\1/p' | head -1)"
  if [[ -z "$fm_name" ]]; then
    fail "$skill_md has no name: in frontmatter"
  elif [[ "$fm_name" != "$name" ]]; then
    fail "$skill_md frontmatter name '$fm_name' != folder name '$name'"
  fi
  if ! printf '%s\n' "$fm" | grep -q '^description:[[:space:]]*[^[:space:]]'; then
    fail "$skill_md has no description: in frontmatter"
  else
    desc="$(printf '%s\n' "$fm" | sed -n 's/^description:[[:space:]]*//p' | head -1 | sed 's/^"//; s/"$//')"
    if (( ${#desc} > 1024 )); then
      fail "$skill_md description is ${#desc} chars (>1024 — hosts with description limits truncate it)"
    fi
  fi
  if ! [[ "$name" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
    fail "skill folder '$name' is not kebab-case"
  fi
done
note "frontmatter checked for $(ls -d skills/*/ | wc -l | tr -d ' ') skills"

echo "== 2. ship-policy.md copies byte-identical =="
if ! cmp -s skills/commit-push-close/references/ship-policy.md \
            skills/commit-push-pr/references/ship-policy.md; then
  fail "ship-policy.md copies differ — edit both together (they are duplicated so each skill installs self-contained)"
else
  note "ship-policy.md copies match"
fi

echo "== 3. Skill folders and skills-manifest.md rows agree =="
MANIFEST="skills/agents-md/references/skills-manifest.md"
for dir in skills/*/; do
  name="$(basename "$dir")"
  if ! grep -q "\`/$name\`" "$MANIFEST"; then
    fail "skills/$name has no \`/$name\` row in $MANIFEST"
  fi
done
# Reverse direction: every gradient row's kind must match reality on disk.
while IFS='|' read -r _ col_skill col_kind _; do
  skill="$(printf '%s' "$col_skill" | tr -d ' `' )"
  kind="$(printf '%s' "$col_kind" | tr -d ' ')"
  name="${skill#/}"
  [[ -z "$name" || "$name" == "skill" ]] && continue
  case "$kind" in
    kit)
      [[ -d "skills/$name" ]] || fail "manifest lists \`/$name\` as kit but skills/$name does not exist"
      ;;
    external)
      [[ -d "skills/$name" ]] && fail "manifest lists \`/$name\` as external but skills/$name exists — change kind to kit"
      ;;
  esac
done < <(grep -E '^\|[[:space:]]*`/' "$MANIFEST")
note "manifest coverage checked (both directions)"

echo "== 4. Every skill is mentioned in README.md =="
for dir in skills/*/; do
  name="$(basename "$dir")"
  if ! grep -q "$name" README.md; then
    fail "skills/$name is not mentioned in README.md"
  fi
done
note "README coverage checked"

echo "== 5. Relative markdown links resolve =="
# Extracts [text](target) links; skips absolute URLs, anchors, mail links, and
# obvious placeholders (targets containing <, >, or spaces).
while IFS= read -r md; do
  dir="$(dirname "$md")"
  while IFS= read -r target; do
    case "$target" in
      http://*|https://*|mailto:*|\#*) continue ;;
      *"<"*|*">"*|*" "*) continue ;;
    esac
    path="${target%%#*}"
    [[ -z "$path" ]] && continue
    if [[ ! -e "$dir/$path" && ! -e "$ROOT/$path" ]]; then
      fail "$md links to missing file: $target"
    fi
  done < <(grep -o '](\([^)]*\))' "$md" | sed 's/^](//; s/)$//')
done < <(find . -name '*.md' -not -path './.git/*')
note "relative links checked"

echo "== 6. Zero-attribution tripwire =="
# Policy docs may NAME forbidden patterns; a real attribution carries an email
# or the generated-with footer. Both should never appear in this repo.
if grep -rnE 'Co-Authored-By: .+<.+@.+>|Generated with \[Claude Code\]' \
     --include='*.md' . | grep -v '^\./\.git/'; then
  fail "attribution text found (see lines above) — zero-attribution policy"
else
  note "no attribution leaks"
fi

echo
if [[ "$FAIL" -ne 0 ]]; then
  echo "validate.sh: FAILED"
  exit 1
fi
echo "validate.sh: all checks passed"

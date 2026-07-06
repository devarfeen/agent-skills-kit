#!/usr/bin/env bash
# Validate the agent-skills-kit repo invariants.
#
# Run from anywhere: bash tools/validate.sh
# Exits non-zero on any failure. No dependencies beyond coreutils + grep.
#
# What it enforces (see CONTRIBUTING.md for the why):
#   1. Every skills/<dir>/ has a SKILL.md with `name:` + `description:` frontmatter;
#      name matches the folder and is kebab-case.
#   2. Duplicated-by-design shared files (ship-policy.md, context-terms.md)
#      are byte-identical across their copies.
#   3. Every skill folder has a row in skills/agents-md/references/skills-manifest.md.
#   4. Every skill folder has a table-row link in the root README.md.
#   5. Relative markdown links resolve to real files; cross-file #anchors resolve
#      to a real heading.
#   6. No AI/tool attribution has leaked into the repo — files or branch commit
#      messages (zero-attribution policy).
#   7. The three agents-md version markers agree with each other and with the
#      stated skill version.
#   8. Manifest gradient rows carry a valid phase.
#   9. Every skills/*/evals/evals.json parses and carries queries + last_run.

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

echo "== 2. Duplicated-by-design copies byte-identical =="
# Skills install standalone, so shared text is duplicated per skill and must
# stay byte-identical. One line per pair: "<copy-a> <copy-b>".
DUP_PAIRS="
skills/commit-push-close/references/ship-policy.md skills/commit-push-pr/references/ship-policy.md
skills/feature-discovery/references/context-terms.md skills/feature-prompt/references/context-terms.md
"
PAIR_COUNT=0
while read -r a b; do
  [[ -z "$a" ]] && continue
  PAIR_COUNT=$((PAIR_COUNT+1))
  if [[ ! -f "$a" || ! -f "$b" ]]; then
    fail "duplicated-by-design pair missing a copy: $a / $b"
  elif ! cmp -s "$a" "$b"; then
    fail "$a and $b differ — duplicated by design, edit both together"
  fi
done <<< "$DUP_PAIRS"
note "duplicated-by-design copies match ($PAIR_COUNT pairs)"

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

echo "== 4. Every skill has a README table-row link =="
for dir in skills/*/; do
  name="$(basename "$dir")"
  if ! grep -qF "](skills/$name/SKILL.md)" README.md; then
    fail "skills/$name has no table-row link in README.md (expected [\`$name\`](skills/$name/SKILL.md))"
  fi
done
note "README table-row links checked"

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
      continue
    fi
    # Cross-file anchors: the fragment must match a heading slug in the target
    # (approximate GitHub slugs: lowercase, drop punctuation, spaces → hyphens).
    if [[ "$target" == *"#"* && "$path" == *.md ]]; then
      frag="${target#*#}"
      [[ -z "$frag" ]] && continue
      tfile="$dir/$path"; [[ -e "$tfile" ]] || tfile="$ROOT/$path"
      if ! grep -E '^#{1,6} ' "$tfile" \
           | sed -E 's/^#{1,6} +//' \
           | tr '[:upper:]' '[:lower:]' \
           | sed -E 's/[^a-z0-9 _-]//g; s/ /-/g' \
           | grep -qxF "$frag"; then
        fail "$md links to missing anchor: $target"
      fi
    fi
  done < <(grep -o '](\([^)]*\))' "$md" | sed 's/^](//; s/)$//')
done < <(find . -name '*.md' -not -path './.git/*')
note "relative links checked"

echo "== 6. Zero-attribution tripwire =="
# Policy docs may NAME forbidden patterns; a real attribution carries an email
# or the generated-with footer. Neither should ever appear in this repo.
ATTR_RE='Co-Authored-By: .+<.+@.+>|Generated with \[Claude Code\]|noreply@anthropic\.com'
if grep -rniE "$ATTR_RE" --include='*.md' . | grep -v '^\./\.git/'; then
  fail "attribution text found (see lines above) — zero-attribution policy"
else
  note "no attribution leaks in files"
fi
# Coding harnesses append attribution to commit messages, not files — scan the
# commits this branch adds over origin/main (empty range on an up-to-date main).
if git rev-parse --verify --quiet origin/main >/dev/null 2>&1; then
  base="$(git merge-base HEAD origin/main 2>/dev/null || true)"
  if [[ -n "$base" && "$base" != "$(git rev-parse HEAD)" ]]; then
    if git log --format='%h %B' "$base"..HEAD | grep -niE "$ATTR_RE"; then
      fail "attribution text found in commit messages (see lines above)"
    else
      note "no attribution leaks in branch commit messages"
    fi
  fi
fi

echo "== 7. agents-md version markers in sync =="
AMD="skills/agents-md/SKILL.md"
marker_versions="$(grep -oE 'Generated by the agents-md skill · v[0-9]+' "$AMD" | grep -oE 'v[0-9]+$' | sort -u)"
marker_count="$(grep -cE 'Generated by the agents-md skill · v[0-9]+' "$AMD")"
stated="$(sed -n 's/.*The skill version is `\(v[0-9][0-9]*\)`.*/\1/p' "$AMD" | head -1)"
if [[ "$(printf '%s\n' "$marker_versions" | grep -c .)" -ne 1 ]]; then
  fail "agents-md version markers disagree: $(printf '%s ' $marker_versions)"
elif [[ "$marker_count" -ne 3 ]]; then
  fail "expected 3 agents-md version markers (rule text + both templates), found $marker_count"
elif [[ -n "$stated" && "$stated" != "$marker_versions" ]]; then
  fail "agents-md stated skill version $stated != marker version $marker_versions"
else
  note "agents-md markers consistent ($marker_versions x$marker_count + stated)"
fi

echo "== 8. Manifest phases are valid =="
PHASE_OK=1
while IFS='|' read -r _ col_skill col_kind col_phase _; do
  skill="$(printf '%s' "$col_skill" | tr -d ' `' )"
  kind="$(printf '%s' "$col_kind" | tr -d ' ')"
  phase="$(printf '%s' "$col_phase" | tr -d ' ')"
  name="${skill#/}"
  [[ -z "$name" || "$name" == "skill" ]] && continue
  case "$kind" in
    kit|external)
      case "$phase" in
        startup|discover|sharpen|plan|slice|implement|verify|ship) ;;
        *) fail "manifest row \`/$name\` (kind $kind) has invalid phase '$phase'"; PHASE_OK=0 ;;
      esac
      ;;
  esac
done < <(grep -E '^\|[[:space:]]*`/' "$MANIFEST")
[[ "$PHASE_OK" -eq 1 ]] && note "manifest phases valid"

echo "== 9. Trigger-eval sets parse =="
EV_COUNT=0
for ev in skills/*/evals/evals.json; do
  [[ -e "$ev" ]] || continue
  EV_COUNT=$((EV_COUNT+1))
  if ! python3 - "$ev" <<'PYEOF'
import json, sys
p = sys.argv[1]
d = json.load(open(p))
qs = d.get("queries")
assert isinstance(qs, list) and len(qs) >= 12, "expected a queries list of >=12, got %r" % (len(qs) if isinstance(qs, list) else type(qs).__name__)
for i, q in enumerate(qs):
    assert isinstance(q.get("q"), str) and q["q"].strip(), "query %d missing q" % i
    assert q.get("expect") in ("trigger", "no-trigger"), "query %d has bad expect: %r" % (i, q.get("expect"))
assert isinstance(d.get("last_run"), dict) and d["last_run"].get("date"), "missing last_run.date"
PYEOF
  then
    fail "$ev failed the eval shape check (see message above)"
  fi
done
note "eval sets parsed ($EV_COUNT files)"

echo
if [[ "$FAIL" -ne 0 ]]; then
  echo "validate.sh: FAILED"
  exit 1
fi
echo "validate.sh: all checks passed"

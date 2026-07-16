#!/usr/bin/env bash
# Validate the agent-skills-kit repo invariants.
#
# Run from anywhere: bash tools/validate.sh
# Exits non-zero on any failure. No dependencies beyond coreutils + grep.
#
# What it enforces (see CONTRIBUTING.md for the why):
#   1. Every skills/<dir>/ has a SKILL.md with `name:` + `description:` frontmatter;
#      name matches the folder and is kebab-case; frontmatter parses as strict YAML
#      (an unquoted description with a ': ' colon-space breaks the skills CLI).
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
#  10. Eval provenance: each live description still matches the one that was
#      actually judged in the run its last_run records. A description edited
#      after a passing run silently invalidates that run's result.
#  11. Invocation parity: `disable-model-invocation: true` in SKILL.md
#      frontmatter ⇔ an `agents/openai.yaml` with
#      `allow_implicit_invocation: false` (the Codex-side mirror of the flag).
#  12. SKILL.md body word ceiling (1500) — sprawl guard from the house style
#      (skills/writing-kit-skills/SKILL.md).
#  13. Canonical one-liners: where a SKILL.md covers a shared protocol
#      (artifacts-root, graphify, sub-agent lanes, PROJECT-CODE, phase update),
#      it must carry the house one-liner byte-exact, not a paraphrase.
#  14. No placeholder scaffolding in references/ or assets/ — a stub file a
#      SKILL.md cites as real content is worse than a dead link.

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

# Strict YAML parse of each frontmatter block. The checks above only confirm the
# fields are present; a regex misses YAML hazards a strict parser (the one the
# skills CLI uses) rejects — most notably an unquoted description containing
# ': ' (colon-space), which the CLI reports as "mapping values are not allowed
# here" and refuses to install. Prefer PyYAML; fall back to a stdlib heuristic.
if command -v python3 >/dev/null 2>&1; then
  yaml_out="$(python3 - <<'PYEOF'
import glob
try:
    import yaml
    have = True
except Exception:
    have = False

def frontmatter(t):
    if not t.startswith("---"):
        return None
    end = t.find("\n---", 3)
    return t[3:end] if end != -1 else None

bad = []
for f in sorted(glob.glob("skills/*/SKILL.md")):
    fm = frontmatter(open(f, encoding="utf-8").read())
    if fm is None:
        bad.append(f + ": no closing --- for frontmatter"); continue
    if have:
        try:
            yaml.safe_load(fm)
        except Exception as e:
            bad.append(f + ": " + str(e).splitlines()[0])
    else:
        import re
        for ln in fm.splitlines():
            m = re.match(r'^(name|description):\s*(.*)$', ln)
            if not m:
                continue
            v = m.group(2).strip()
            if v[:1] == '"':
                if not (len(v) >= 2 and v.endswith('"')):
                    bad.append(f + ": " + m.group(1) + " has an unbalanced opening quote")
            elif ": " in v:
                bad.append(f + ": " + m.group(1) + " is unquoted and contains ': ' (quote the value)")
for b in bad:
    print(b)
PYEOF
)"
  if [[ -n "$yaml_out" ]]; then
    while IFS= read -r line; do
      [[ -n "$line" ]] && fail "frontmatter YAML — $line"
    done <<< "$yaml_out"
  else
    note "frontmatter parses as strict YAML"
  fi
fi

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
marker_versions="$(cat "$AMD" skills/agents-md/assets/*.md | grep -oE 'agents-md marker · v[0-9]+' | grep -oE 'v[0-9]+$' | sort -u)"
marker_count="$(cat "$AMD" skills/agents-md/assets/*.md | grep -cE 'agents-md marker · v[0-9]+')"
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

echo "== 10. Eval provenance: descriptions match their recorded run =="
# The frontmatter description IS the router, and last_run records the result of
# judging *that* text. Edit a description after a passing run and the recorded
# result becomes a claim about a string that no longer exists. This check makes
# that drift loud instead of silent. (It once let the kit carry a 280/280 claim
# while actually scoring 277/280.)
SNAP="tools/trigger-evals/last-run-descriptions.json"
if [[ ! -f "$SNAP" ]]; then
  fail "$SNAP is missing — cannot verify that eval results match the judged descriptions"
elif command -v python3 >/dev/null 2>&1; then
  prov_out="$(python3 - "$SNAP" <<'PYEOF'
import glob, hashlib, json, os, re, sys

snap = json.load(open(sys.argv[1]))
want = snap["descriptions_sha256"]
ref  = snap.get("recorded_at_commit", "the recorded run")

def parse_desc(text):
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return None
    for line in m.group(1).splitlines():
        if line.startswith("description:"):
            v = line[len("description:"):].strip()
            if len(v) >= 2 and v[0] == '"' and v[-1] == '"':
                v = v[1:-1]
            return v
    return None

for f in sorted(glob.glob("skills/*/SKILL.md")):
    name = os.path.basename(os.path.dirname(f))
    desc = parse_desc(open(f, encoding="utf-8").read())
    if desc is None:
        print(f"{name}: no description to verify"); continue
    if name not in want:
        print(f"{name}: no recorded description for it — add one by re-running the evals"); continue
    if hashlib.sha256(desc.encode()).hexdigest() != want[name]:
        print(f"{name}: description changed since the eval run recorded in its last_run "
              f"(snapshot @ {ref}) — re-run the trigger evals and restamp last_run")
PYEOF
)"
  if [[ -n "$prov_out" ]]; then
    while IFS= read -r line; do
      [[ -n "$line" ]] && fail "eval provenance — $line"
    done <<< "$prov_out"
    printf '  remedy: bash tools/trigger-evals/build-catalog.sh, run 3 judges, then\n'
    printf '          python3 tools/trigger-evals/score.py … --write-snapshot\n'
  else
    note "every description matches the run its last_run records"
  fi
fi

echo "== 11. Invocation parity: frontmatter flag ⇔ agents/openai.yaml =="
for dir in skills/*/; do
  name="$(basename "$dir")"
  fm="$(awk 'NR==1 && /^---$/{n=1; next} /^---$/{exit} n==1{print}' "${dir}SKILL.md" 2>/dev/null)"
  has_flag=0
  printf '%s\n' "$fm" | grep -q '^disable-model-invocation:[[:space:]]*true' && has_flag=1
  if [[ "$has_flag" -eq 1 ]]; then
    if [[ ! -f "${dir}agents/openai.yaml" ]]; then
      fail "skills/$name sets disable-model-invocation but has no agents/openai.yaml mirror"
    elif ! grep -q 'allow_implicit_invocation:[[:space:]]*false' "${dir}agents/openai.yaml"; then
      fail "skills/$name/agents/openai.yaml does not set allow_implicit_invocation: false"
    fi
  else
    [[ -f "${dir}agents/openai.yaml" ]] && fail "skills/$name has agents/openai.yaml but no disable-model-invocation flag — remove one or add the other"
  fi
done
note "invocation parity checked"

echo "== 12. SKILL.md body word ceiling =="
CEILING=1500
for f in skills/*/SKILL.md; do
  words="$(awk 'NR==1&&/^---$/{f=1;next} f==1&&/^---$/{f=2;next} f==2&&NF{c+=NF} END{print c+0}' "$f")"
  if (( words > CEILING )); then
    fail "$f body is $words words (> $CEILING) — disclose to references/, don't sprawl (see skills/writing-kit-skills/SKILL.md)"
  fi
done
note "all SKILL.md bodies <= $CEILING words"

echo "== 13. Canonical one-liners byte-exact where used =="
# marker<TAB>canonical line. If a SKILL.md contains the marker, it must carry
# the full canonical line (source of truth: skills/writing-kit-skills/SKILL.md).
CANON=$(cat <<'EOF'
<artifacts-root>	Resolve `<artifacts-root>`: the `*.code-workspace` directory if one exists, else the per-context root (`CONTEXT-MAP.md` at repo root), else the repo root.
graphify-out/graph.json	If `graphify-out/graph.json` exists (project root, else workspace root), query it before raw search; older than ~7 days → suggest `graphify update .`; missing → skip graphify.
lane count at dispatch	Sub-agents: local lanes only when the user allows them — never cloud agents; announce the lane count at dispatch and report each lane as it completes.
never mix one project	Name the full PROJECT-CODE from the Project Matrix everywhere; never mix one project's conventions, tokens, or components into another.
Stage / Found / Next / Needs user	Emit `Stage / Found / Next / Needs user` at each phase transition — one line per field.
EOF
)
for f in skills/*/SKILL.md; do
  [[ "$f" == "skills/writing-kit-skills/SKILL.md" ]] && continue
  while IFS=$'\t' read -r marker canon; do
    [[ -z "$marker" ]] && continue
    if grep -qF "$marker" "$f" && ! grep -qF "$canon" "$f"; then
      fail "$f mentions '$marker' without the canonical one-liner — paste it byte-exact from skills/writing-kit-skills/SKILL.md"
    fi
  done <<< "$CANON"
done
note "canonical one-liners byte-exact where used"

echo "== 14. No placeholder scaffolding in references/assets =="
PLACEHOLDER_RE='Scenario 1, Scenario 2|Detailed explanation of the pattern|\[TODO|Lorem ipsum|PLACEHOLDER-CONTENT'
if grep -rniE "$PLACEHOLDER_RE" skills/*/references skills/*/assets 2>/dev/null; then
  fail "placeholder scaffolding found (see lines above) — reference/asset files must carry real content"
else
  note "no placeholder scaffolding in references/assets"
fi

echo
if [[ "$FAIL" -ne 0 ]]; then
  echo "validate.sh: FAILED"
  exit 1
fi
echo "validate.sh: all checks passed"

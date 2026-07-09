#!/usr/bin/env python3
"""Score trigger evals: majority vote across 3 judge outputs.

Usage: python3 tools/trigger-evals/score.py <query-manifest.json> <j1> <j2> <j3>
                                            [--write-snapshot]
Judge files: one JSON object per line: {"n": <int>, "pick": "<skill-or-none>"}.
Pass rule: expect=trigger passes when the majority pick IS the skill;
expect=no-trigger passes when the majority pick is anything else.

--write-snapshot refreshes tools/trigger-evals/last-run-descriptions.json with
the descriptions this run actually judged, so validate.sh check 10 can prove a
later description edit invalidated the result. It only writes on a clean sweep:
a snapshot taken from a failing run would bless the very text that failed.
"""
import hashlib, json, os, re, sys
from collections import Counter, defaultdict

WRITE_SNAPSHOT = "--write-snapshot" in sys.argv
argv = [a for a in sys.argv if a != "--write-snapshot"]

manifest = json.load(open(argv[1]))
judges = []
for p in argv[2:5]:
    picks = {}
    for line in open(p):
        line = line.strip()
        if not line:
            continue
        d = json.loads(line)
        picks[d["n"]] = d["pick"].strip()
    judges.append(picks)

per_skill = defaultdict(lambda: {"pass": 0, "fail": 0, "fails": []})
for it in manifest:
    votes = [j.get(it["n"], "MISSING") for j in judges]
    majority, count = Counter(votes).most_common(1)[0]
    if count < 2:
        majority = "SPLIT(" + ",".join(votes) + ")"
    hit = (majority == it["skill"])
    ok = hit if it["expect"] == "trigger" else not hit
    bucket = per_skill[it["skill"]]
    if ok:
        bucket["pass"] += 1
    else:
        bucket["fail"] += 1
        bucket["fails"].append(
            f"  [{it['expect']}] {it['q']!r} -> majority {majority} (votes: {votes})"
        )

total_pass = total = 0
for skill in sorted(per_skill):
    b = per_skill[skill]
    total_pass += b["pass"]
    total += b["pass"] + b["fail"]
    flag = "" if b["fail"] == 0 else "  <-- FAIL"
    print(f"{skill:24} {b['pass']:3}/{b['pass'] + b['fail']:<3}{flag}")
    for line in b["fails"]:
        print(line)
print(f"\nTOTAL {total_pass}/{total}")

if WRITE_SNAPSHOT:
    if total_pass != total:
        print("\nnot writing snapshot: the run did not pass clean")
        sys.exit(1)
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

    skills_dir = os.path.join(root, "skills")
    shas = {}
    for name in sorted(os.listdir(skills_dir)):
        p = os.path.join(skills_dir, name, "SKILL.md")
        if not os.path.isfile(p):
            continue
        d = parse_desc(open(p, encoding="utf-8").read())
        if d is not None:
            shas[name] = hashlib.sha256(d.encode()).hexdigest()

    out = os.path.join(root, "tools", "trigger-evals", "last-run-descriptions.json")
    prev = json.load(open(out)) if os.path.exists(out) else {}
    payload = {
        "_comment": prev.get("_comment", ""),
        "recorded_at_commit": "working tree at the time of the run",
        "descriptions_sha256": shas,
    }
    with open(out, "w") as fh:
        json.dump(payload, fh, indent=1)
        fh.write("\n")
    print(f"wrote snapshot for {len(shas)} descriptions -> {out}")
    print("now restamp each skill's last_run with this run's date, method, result, and judge model")

sys.exit(0 if total_pass == total else 1)

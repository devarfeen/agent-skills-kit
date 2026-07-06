#!/usr/bin/env python3
"""Score trigger evals: majority vote across 3 judge outputs.

Usage: python3 tools/trigger-evals/score.py <query-manifest.json> <j1> <j2> <j3>
Judge files: one JSON object per line: {"n": <int>, "pick": "<skill-or-none>"}.
Pass rule: expect=trigger passes when the majority pick IS the skill;
expect=no-trigger passes when the majority pick is anything else.
"""
import json, sys
from collections import Counter, defaultdict

manifest = json.load(open(sys.argv[1]))
judges = []
for p in sys.argv[2:5]:
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
sys.exit(0 if total_pass == total else 1)

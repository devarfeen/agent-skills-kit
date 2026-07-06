#!/usr/bin/env python3
"""Mix every skills/*/evals/evals.json into one numbered query list.

Usage: python3 tools/trigger-evals/build-queryset.py <outdir>
Writes <outdir>/queryset.md (for judges) and <outdir>/query-manifest.json
(for score.py). Shuffle is deterministic (fixed seed) so runs are comparable.
"""
import json, glob, os, random, sys

root = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", ".."))
outdir = sys.argv[1] if len(sys.argv) > 1 else "."

items = []
for path in sorted(glob.glob(os.path.join(root, "skills", "*", "evals", "evals.json"))):
    skill = path.split(os.sep)[-3]
    data = json.load(open(path))
    for q in data["queries"]:
        items.append({
            "skill": f"/{skill}",
            "q": q["q"],
            "expect": q["expect"],
            "route": q.get("route"),
        })

random.Random(20260706).shuffle(items)
for n, it in enumerate(items, 1):
    it["n"] = n

with open(os.path.join(outdir, "queryset.md"), "w") as f:
    f.write("# Queries\n\n")
    for it in items:
        f.write(f"{it['n']}. {it['q']}\n")

with open(os.path.join(outdir, "query-manifest.json"), "w") as f:
    json.dump(items, f, indent=1)

print(f"{len(items)} queries -> {outdir}/queryset.md, {outdir}/query-manifest.json")

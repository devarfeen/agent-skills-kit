#!/usr/bin/env python3
"""Capture Codex's exposed catalog and queries for its implicitly available kit skills."""
import argparse
import json
from pathlib import Path
import re
import subprocess


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("outdir", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    result = subprocess.run(["codex", "debug", "prompt-input", "Inspect skill routing only."],
                            cwd=root, check=True, capture_output=True, text=True)
    entries = {}
    for message in json.loads(result.stdout):
        for block in message.get("content", []):
            for line in block.get("text", "").splitlines():
                match = re.match(r"^- (.+?): (.+) \(file: (.+)\)$", line)
                if not match:
                    continue
                name, description, path = match.groups()
                if name in entries:
                    raise ValueError(f"duplicate exposed skill {name}: resolve the profile before judging")
                entries[name] = {"description": description, "path": path}
    if not entries:
        raise ValueError("Codex exposed no readable skill catalog")
    kit = {p.parent.name for p in (root / "skills").glob("*/SKILL.md")}
    lines = ["# Installed Codex routing catalog", "",
             "Zero attribution: never add or leave co-author, AI, or tool attribution in any output.",
             "", "## Kit skills", ""]
    for name, entry in sorted(entries.items()):
        if name in kit:
            lines.append(f"- **/{name}** — {entry['description']}")
    lines.extend(["", "## External skills", ""])
    for name, entry in sorted(entries.items()):
        if name not in kit:
            lines.append(f"- **{name}** — {entry['description']}")
    queries = []
    for name in sorted(kit & entries.keys()):
        data = json.loads((root / "skills" / name / "evals" / "evals.json").read_text())
        queries.extend({**query, "skill": f"/{name}"} for query in data["queries"])
    for number, query in enumerate(queries, 1):
        query["n"] = number
    args.outdir.mkdir(parents=True, exist_ok=True)
    (args.outdir / "catalog.md").write_text("\n".join(lines) + "\n")
    (args.outdir / "query-manifest.json").write_text(json.dumps(queries, indent=1) + "\n")
    (args.outdir / "queryset.md").write_text("# Queries\n\n" + "".join(
        f"{query['n']}. {query['q']}\n" for query in queries))
    (args.outdir / "exposed-skills.json").write_text(json.dumps(entries, indent=1) + "\n")
    print(f"{len(entries)} exposed skills; {len(queries)} implicit-kit queries -> {args.outdir}")


if __name__ == "__main__":
    main()

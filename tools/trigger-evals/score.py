#!/usr/bin/env python3
"""Score three complete catalog-routing ballots; snapshot only a clean sweep."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import sys


def digest(data):
    return hashlib.sha256(data).hexdigest()


def parse_catalog(data):
    entries, kit = {}, {}
    in_kit = False
    for line in data.decode().splitlines():
        if line.startswith("## "):
            in_kit = line == "## Kit skills"
        match = re.match(r"^- \*\*(.+?)\*\* — (.+)$", line)
        if not match:
            continue
        name, description = match.groups()
        if name in entries or name == "none":
            raise ValueError(f"duplicate or reserved catalog name: {name}")
        entries[name] = description
        if in_kit:
            if not name.startswith("/"):
                raise ValueError(f"kit catalog name must begin with /: {name}")
            kit[name[1:]] = description
    if not entries or not kit:
        raise ValueError("catalog must contain kit descriptions and routing entries")
    return entries, kit


def load_manifest(data, entries):
    manifest = json.loads(data)
    if not isinstance(manifest, list) or not manifest:
        raise ValueError("manifest must be a nonempty query list")
    ids = set()
    for item in manifest:
        n = item["n"]
        if type(n) is not int or n <= 0 or n in ids:
            raise ValueError(f"invalid or duplicate manifest query number: {n}")
        if item["skill"] not in entries or item["expect"] not in {"trigger", "no-trigger"}:
            raise ValueError(f"unknown skill or expectation for query {n}")
        if not isinstance(item["q"], str) or not item["q"].strip():
            raise ValueError(f"empty query text for query {n}")
        ids.add(n)
    return manifest, ids


def load_judge(data, ids, allowed, path):
    picks = {}
    for line in data.decode().splitlines():
        if not line.strip():
            continue
        item = json.loads(line)
        n, pick = item["n"], item["pick"]
        if type(n) is not int or n not in ids or n in picks:
            raise ValueError(f"{path}: unknown or duplicate query number {n}")
        if not isinstance(pick, str) or pick not in allowed:
            raise ValueError(f"{path}: unknown pick {pick!r} for query {n}")
        picks[n] = pick
    if set(picks) != ids:
        raise ValueError(f"{path}: missing query numbers {sorted(ids - set(picks))}")
    return picks


def live_descriptions(root):
    descriptions = {}
    for path in sorted((root / "skills").glob("*/SKILL.md")):
        frontmatter = re.match(r"^---\n(.*?)\n---", path.read_text(), re.S)
        match = re.search(r"^description:\s*(.+)$", frontmatter[1], re.M) if frontmatter else None
        if not match:
            raise ValueError(f"missing description in {path}")
        description = match[1].strip()
        if description.startswith('"') and description.endswith('"'):
            description = description[1:-1]
        descriptions[path.parent.name] = description
    return descriptions


def query_content(items):
    return Counter((item["skill"], item["q"], item["expect"], item.get("route"))
                   for item in items)


def live_queries(root):
    items = []
    for path in sorted((root / "skills").glob("*/evals/evals.json")):
        for query in json.loads(path.read_text())["queries"]:
            items.append({**query, "skill": f"/{path.parents[1].name}"})
    return items


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("judges", nargs=3, type=Path)
    parser.add_argument("--catalog", type=Path, help="catalog supplied to judges; defaults to catalog.md beside manifest")
    parser.add_argument("--write-snapshot", action="store_true")
    args = parser.parse_args()
    catalog_path = args.catalog or args.manifest.with_name("catalog.md")
    catalog_data, manifest_data = catalog_path.read_bytes(), args.manifest.read_bytes()
    entries, kit = parse_catalog(catalog_data)
    manifest, ids = load_manifest(manifest_data, entries)
    if len({path.resolve() for path in args.judges}) != 3:
        raise ValueError("three distinct judge files are required")
    judge_data = [path.read_bytes() for path in args.judges]
    judges = [load_judge(data, ids, set(entries) | {"none"}, path)
              for data, path in zip(judge_data, args.judges)]

    per_skill = defaultdict(lambda: {"pass": 0, "fail": 0, "fails": []})
    for item in manifest:
        votes = [judge[item["n"]] for judge in judges]
        majority, count = Counter(votes).most_common(1)[0]
        hit = majority == item["skill"]
        passed = count >= 2 and (hit if item["expect"] == "trigger" else not hit)
        bucket = per_skill[item["skill"]]
        bucket["pass" if passed else "fail"] += 1
        if not passed:
            choice = majority if count >= 2 else "NO MAJORITY"
            bucket["fails"].append(f"  [{item['expect']}] {item['q']!r} -> {choice} (votes: {votes})")
    total_pass = sum(bucket["pass"] for bucket in per_skill.values())
    for skill, bucket in sorted(per_skill.items()):
        flag = "  <-- FAIL" if bucket["fail"] else ""
        print(f"{skill:24} {bucket['pass']:3}/{bucket['pass'] + bucket['fail']:<3}{flag}")
        for failure in bucket["fails"]:
            print(failure)
    print(f"\nTOTAL {total_pass}/{len(manifest)}")
    if total_pass != len(manifest):
        return 1
    if args.write_snapshot:
        root = Path(__file__).resolve().parents[2]
        if set(per_skill) != {f"/{name}" for name in kit}:
            raise ValueError("snapshot requires queries for every kit skill")
        if query_content(manifest) != query_content(live_queries(root)):
            raise ValueError("snapshot requires the full unchanged live query set")
        if live_descriptions(root) != kit:
            raise ValueError("live descriptions differ from the catalog judged; rebuild and rerun")
        out = root / "tools" / "trigger-evals" / "last-run-descriptions.json"
        previous = json.loads(out.read_text()) if out.exists() else {}
        payload = {
            "_comment": previous.get("_comment", ""),
            "recorded_at_commit": "working tree matching the catalog supplied to this run",
            "catalog_sha256": digest(catalog_data),
            "manifest_sha256": digest(manifest_data),
            "judge_sha256": [digest(data) for data in judge_data],
            "descriptions_sha256": {name: digest(description.encode()) for name, description in sorted(kit.items())},
        }
        out.write_text(json.dumps(payload, indent=1) + "\n")
        print(f"wrote snapshot for {len(kit)} descriptions -> {out}")
        print("record this real run's date, method, result, judge model, and catalog in each last_run")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"invalid eval run: {error}", file=sys.stderr)
        sys.exit(2)

#!/usr/bin/env python3
"""Score three complete catalog-routing ballots; snapshot only a clean sweep."""
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


def digest(data):
    return hashlib.sha256(data).hexdigest()


def recorded_commit(root):
    """Name the commit the judged files came from; flag a dirty tree, since the
    judged files may then match no commit."""
    try:
        run = lambda *args: subprocess.run(["git", "-C", str(root), *args], check=True,
                                           capture_output=True, text=True).stdout.strip()
        head, dirty = run("rev-parse", "HEAD"), run("status", "--porcelain")
    except (OSError, subprocess.CalledProcessError):
        return "unknown: not a git checkout"
    return f"{head} + uncommitted changes" if dirty else head


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
    for skill in sorted((root / "skills").glob("*/SKILL.md")):
        path = skill.parent / "evals" / "evals.json"
        for query in json.loads(path.read_text())["queries"]:
            items.append({**query, "skill": f"/{path.parents[1].name}"})
    return items


def content_digest(items):
    rows = sorted(json.dumps([item["skill"], item["q"], item["expect"], item.get("route")],
                             ensure_ascii=False) for item in items)
    return digest(json.dumps(rows, ensure_ascii=False).encode())


def live_catalog(root):
    kit = "## Kit skills\n" + "\n".join(
        f"- **/{name}** — {description}" for name, description in live_descriptions(root).items())
    external = (root / "tools" / "trigger-evals" / "catalog-externals.md").read_text()
    return parse_catalog((kit + "\n" + external).encode())[0]


def catalog_digest(entries):
    return digest(json.dumps(entries, sort_keys=True, ensure_ascii=False).encode())


def live_catalog_data(root):
    return subprocess.run(["bash", str(root / "tools" / "trigger-evals" / "build-catalog.sh")],
                          check=True, capture_output=True).stdout


def invocation_digest(root):
    policies = {}
    for path in sorted((root / "skills").glob("*/SKILL.md")):
        fm = path.read_text().split("---", 2)[1]
        policies[path.parent.name] = bool(re.search(r"^disable-model-invocation:\s*true\s*$", fm, re.M))
    return digest(json.dumps(policies, sort_keys=True).encode())


def check_provenance(root):
    snapshot = json.loads((root / "tools" / "trigger-evals" / "last-run-descriptions.json").read_text())
    current = {
        "descriptions_sha256": {name: digest(description.encode())
                                for name, description in live_descriptions(root).items()},
        "queries_sha256": content_digest(live_queries(root)),
        "catalog_content_sha256": catalog_digest(live_catalog(root)),
        "catalog_sha256": digest(live_catalog_data(root)),
        "invocation_sha256": invocation_digest(root),
    }
    changed = [key for key, value in current.items() if snapshot.get(key) != value]
    if changed:
        raise ValueError("eval inputs changed or are unrecorded: " + ", ".join(changed) + "; rerun three judges")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", nargs="?", type=Path)
    parser.add_argument("judges", nargs="*", type=Path)
    parser.add_argument("--catalog", type=Path, help="catalog supplied to judges; defaults to catalog.md beside manifest")
    parser.add_argument("--write-snapshot", action="store_true")
    parser.add_argument("--check-provenance", action="store_true")
    parser.add_argument("--record-run", action="store_true", help="record the scored sweep in every skill's last_run")
    parser.add_argument("--judge-model", help="actual judge model or documented inherited session model")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    if args.check_provenance:
        check_provenance(root)
        print("eval descriptions, query content, catalog and invocation policies match the recorded run")
        return 0
    if args.manifest is None or len(args.judges) != 3:
        parser.error("a manifest and exactly three judge files are required")
    if args.record_run and (not args.write_snapshot or not args.judge_model):
        parser.error("--record-run requires --write-snapshot and --judge-model")
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
        if item["expect"] == "trigger":
            passed = count >= 2 and hit
        else:
            # A no-trigger query passes when another skill wins the majority, or when
            # no judge picked this skill at all: three different non-target picks
            # still prove the description did not fire. Any vote for the target
            # without a majority elsewhere stays a failure.
            passed = (count >= 2 and not hit) or item["skill"] not in votes
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
        if set(per_skill) != {f"/{name}" for name in kit}:
            raise ValueError("snapshot requires queries for every kit skill")
        if query_content(manifest) != query_content(live_queries(root)):
            raise ValueError("snapshot requires the full unchanged live query set")
        if live_descriptions(root) != kit:
            raise ValueError("live descriptions differ from the catalog judged; rebuild and rerun")
        if live_catalog(root) != entries:
            raise ValueError("live external catalog differs from the catalog judged; rebuild and rerun")
        if live_catalog_data(root) != catalog_data:
            raise ValueError("complete live catalog differs from the catalog judged; rebuild and rerun")
        out = root / "tools" / "trigger-evals" / "last-run-descriptions.json"
        payload = {
            "_comment": "Hashes of the actual complete scored sweep; validate.sh checks descriptions, queries, catalog and invocation policies.",
            "recorded_at_commit": recorded_commit(root),
            "catalog_sha256": digest(catalog_data),
            "manifest_sha256": digest(manifest_data),
            "judge_sha256": [digest(data) for data in judge_data],
            "queries_sha256": content_digest(manifest),
            "catalog_content_sha256": catalog_digest(entries),
            "invocation_sha256": invocation_digest(root),
            "descriptions_sha256": {name: digest(description.encode()) for name, description in sorted(kit.items())},
        }
        out.write_text(json.dumps(payload, indent=1) + "\n")
        print(f"wrote snapshot for {len(kit)} descriptions -> {out}")
        print("record this real run's date, method, result, judge model, and catalog in each last_run")
        if args.record_run:
            run = {
                "date": datetime.now(timezone.utc).date().isoformat(),
                "method": "3 independent fresh catalog-only judges; majority vote; no workflow execution",
                "result": f"{total_pass}/{len(manifest)} pass",
                "judge_model": args.judge_model,
                "catalog": "live kit descriptions and invocation policies + catalog-externals.md; " + payload["recorded_at_commit"],
            }
            for path in sorted((root / "skills").glob("*/evals/evals.json")):
                data = json.loads(path.read_text())
                data["last_run"] = run
                path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError) as error:
        print(f"invalid eval run: {error}", file=sys.stderr)
        sys.exit(2)

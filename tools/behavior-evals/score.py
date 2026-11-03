#!/usr/bin/env python3
"""Score the mechanical checks of a skill behavior-eval case.

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Usage:
  score.py CHECKS_JSON CASE [OUTPUT]   score OUTPUT (default: the case's reference)
  score.py --all                       score every reference in skills/*/evals/behavior-checks.json

Only mechanical checks live here: word counts, list-item length, sentence
count, and protected spans. Judgement checks stay in behavior-cases.md.
Words are whitespace-separated tokens, labels included (same as `wc -w`).
A fenced ```text block in OUTPUT is scored instead of the whole file.
"""
import glob
import json
import re
import sys
from pathlib import Path

FENCE = re.compile(r"```text\n(.*?)```", re.S)
SENTENCE_END = re.compile(r"(?<=[.!?])\s+")


def body(path):
    text = Path(path).read_text(encoding="utf-8")
    m = FENCE.search(text)
    return m.group(1) if m else text


def label_lines(text, label):
    return [line[len(label):].strip() for line in text.splitlines() if line.startswith(label)]


def check(spec, base, text):
    errors = []
    words = len(text.split())
    if "max_words" in spec and words > spec["max_words"]:
        errors.append(f"{words} words; limit {spec['max_words']}")
    for label in spec.get("list_labels", []):
        for line in label_lines(text, label):
            lead, colon, rest = line.partition(":")
            if not colon:
                continue
            for item in SENTENCE_END.split(rest.strip(), 1)[0].split(";"):
                n = len(item.split())
                if n > spec["max_item_words"]:
                    errors.append(f"{label} item has {n} words; limit {spec['max_item_words']}: {item.strip()[:60]}")
    for label in spec.get("sentence_labels", []):
        for line in label_lines(text, label):
            n = len([s for s in SENTENCE_END.split(line) if s.strip()])
            if n > spec["max_sentences"]:
                errors.append(f"{label} has {n} sentences; limit {spec['max_sentences']}")
    if spec.get("protected"):
        fixture = body(base / spec["fixture"])
        for span in spec["protected"]:
            want, got = fixture.count(span), text.count(span)
            if got < want:
                errors.append(f"protected span {span!r} appears {got} times; fixture has {want}")
    return words, errors


def score(checks_path, case, output=None):
    checks_path = Path(checks_path)
    spec = json.loads(checks_path.read_text(encoding="utf-8"))[case]
    base = checks_path.parent
    target = Path(output) if output else base / spec["reference"]
    return check(spec, base, body(target))


def report(label, words, errors):
    print(f"{'FAIL' if errors else 'ok'}: {label} ({words} words)")
    for e in errors:
        print(f"  - {e}")
    return not errors


def main(argv):
    if argv == ["--all"]:
        ok = True
        for path in sorted(glob.glob("skills/*/evals/behavior-checks.json")):
            for case in json.loads(Path(path).read_text(encoding="utf-8")):
                ok &= report(f"{path} {case} reference", *score(path, case))
        return 0 if ok else 1
    if len(argv) not in (2, 3):
        print(__doc__.strip().split("\n\n")[1], file=sys.stderr)
        return 2
    return 0 if report(" ".join(argv[1:]), *score(*argv)) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

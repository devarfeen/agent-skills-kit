import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


class ScoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.harness = self.root / "tools" / "trigger-evals"
        self.harness.mkdir(parents=True)
        shutil.copy(Path(__file__).with_name("score.py"), self.harness / "score.py")
        self.skill = self.root / "skills" / "alpha" / "SKILL.md"
        self.skill.parent.mkdir(parents=True)
        self.skill.write_text("---\nname: alpha\ndescription: Original description.\n---\n")
        self.catalog = self.root / "catalog.md"
        self.catalog.write_text("## Kit skills\n- **/alpha** — Original description.\n"
                                "## External skills\n- **/beta** — Other task.\n")
        self.manifest = self.root / "query-manifest.json"
        self.manifest.write_text(json.dumps([
            {"n": 1, "skill": "/alpha", "expect": "trigger", "q": "alpha"},
            {"n": 2, "skill": "/alpha", "expect": "no-trigger", "q": "other"},
        ]))
        eval_dir = self.skill.parent / "evals"
        eval_dir.mkdir()
        (eval_dir / "evals.json").write_text(json.dumps({"queries": [
            {"q": "alpha", "expect": "trigger"},
            {"q": "other", "expect": "no-trigger"},
        ]}))
        self.judges = [self.root / f"j{i}.jsonl" for i in range(3)]
        for path in self.judges:
            self.write_judge(path, [(1, "/alpha"), (2, "none")])
        self.snapshot = self.harness / "last-run-descriptions.json"
        self.snapshot.write_text('{"preserve": true}\n')

    def write_judge(self, path, picks):
        path.write_text("".join(json.dumps({"n": n, "pick": pick}) + "\n"
                                for n, pick in picks))

    def run_score(self, *flags, judges=None):
        return subprocess.run([sys.executable, str(self.harness / "score.py"),
                               str(self.manifest), *map(str, judges or self.judges),
                               *flags], text=True, capture_output=True)

    def assert_rejected(self, result):
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.snapshot.read_text(), '{"preserve": true}\n')

    def test_complete_majority_passes(self):
        self.write_judge(self.judges[2], [(1, "/beta"), (2, "/alpha")])
        result = self.run_score()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("TOTAL 2/2", result.stdout)

    def test_missing_negative_is_rejected(self):
        for path in self.judges:
            self.write_judge(path, [(1, "/alpha")])
        self.assert_rejected(self.run_score("--write-snapshot"))

    def test_split_negative_fails(self):
        for path, pick in zip(self.judges, ["/alpha", "/beta", "none"]):
            self.write_judge(path, [(1, "/alpha"), (2, pick)])
        self.assert_rejected(self.run_score("--write-snapshot"))

    def test_duplicate_query_is_rejected(self):
        self.write_judge(self.judges[0], [(1, "/alpha"), (2, "none"), (2, "none")])
        self.assert_rejected(self.run_score("--write-snapshot"))

    def test_unknown_pick_is_rejected(self):
        self.write_judge(self.judges[0], [(1, "/alpha"), (2, "/typo")])
        self.assert_rejected(self.run_score("--write-snapshot"))

    def test_extra_query_is_rejected(self):
        self.write_judge(self.judges[0], [(1, "/alpha"), (2, "none"), (99, "none")])
        self.assert_rejected(self.run_score("--write-snapshot"))

    def test_same_judge_file_is_rejected(self):
        self.assert_rejected(self.run_score(judges=[self.judges[0]] * 3))

    def test_missing_catalog_is_rejected(self):
        self.catalog.unlink()
        self.assert_rejected(self.run_score("--write-snapshot"))

    def test_snapshot_rejects_description_changed_since_catalog(self):
        self.skill.write_text("---\nname: alpha\ndescription: New description.\n---\n")
        self.assert_rejected(self.run_score("--write-snapshot"))

    def test_snapshot_records_catalog_and_input_hashes(self):
        result = self.run_score("--write-snapshot")
        self.assertEqual(result.returncode, 0, result.stderr)
        snapshot = json.loads(self.snapshot.read_text())
        digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
        self.assertEqual(snapshot["catalog_sha256"], digest(self.catalog))
        self.assertEqual(snapshot["manifest_sha256"], digest(self.manifest))
        self.assertEqual(snapshot["judge_sha256"], [digest(p) for p in self.judges])
        self.assertEqual(snapshot["descriptions_sha256"]["alpha"],
                         hashlib.sha256(b"Original description.").hexdigest())

    def test_snapshot_rejects_one_omitted_query(self):
        items = json.loads(self.manifest.read_text())[:1]
        self.manifest.write_text(json.dumps(items))
        for path in self.judges:
            self.write_judge(path, [(1, "/alpha")])
        self.assertEqual(self.run_score().returncode, 0)
        self.assert_rejected(self.run_score("--write-snapshot"))

    def test_snapshot_rejects_changed_expectation(self):
        items = json.loads(self.manifest.read_text())
        items[1]["expect"] = "trigger"
        self.manifest.write_text(json.dumps(items))
        for path in self.judges:
            self.write_judge(path, [(1, "/alpha"), (2, "/alpha")])
        self.assertEqual(self.run_score().returncode, 0)
        self.assert_rejected(self.run_score("--write-snapshot"))


if __name__ == "__main__":
    unittest.main()

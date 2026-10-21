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
        shutil.copy(Path(__file__).with_name("build-catalog.sh"), self.harness / "build-catalog.sh")
        self.skill = self.root / "skills" / "alpha" / "SKILL.md"
        self.skill.parent.mkdir(parents=True)
        self.skill.write_text("---\nname: alpha\ndescription: Original description.\n---\n")
        self.catalog = self.root / "catalog.md"
        self.catalog.write_text("## Kit skills\n- **/alpha** — Original description.\n"
                                "## External skills\n- **/beta** — Other task.\n")
        self.external = self.harness / "catalog-externals.md"
        self.external.write_text("## External skills\n- **/beta** — Other task.\n")
        self.catalog.write_bytes(subprocess.run(["bash", str(self.harness / "build-catalog.sh")],
                                                check=True, capture_output=True).stdout)
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

    def test_split_negative_without_target_vote_passes(self):
        self.catalog.write_text(self.catalog.read_text() + "- **/gamma** — Third task.\n")
        for path, pick in zip(self.judges, ["/gamma", "/beta", "none"]):
            self.write_judge(path, [(1, "/alpha"), (2, pick)])
        result = self.run_score()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("TOTAL 2/2", result.stdout)

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

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.root), "-c", "user.name=t",
                               "-c", "user.email=t@example.com", *args],
                              check=True, capture_output=True, text=True).stdout.strip()

    def test_snapshot_records_head_commit(self):
        # Provenance must name the commit judged, not a fixed placeholder.
        self.git("init", "-q")
        self.git("add", "-A")
        self.git("commit", "-qm", "fixture")
        head = self.git("rev-parse", "HEAD")
        result = self.run_score("--write-snapshot")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(self.snapshot.read_text())["recorded_at_commit"], head)

    def test_snapshot_flags_uncommitted_changes(self):
        # A dirty tree means the judged files may not match any commit; say so.
        self.git("init", "-q")
        self.git("add", "-A")
        self.git("commit", "-qm", "fixture")
        head = self.git("rev-parse", "HEAD")
        (self.root / "notes.txt").write_text("uncommitted\n")
        result = self.run_score("--write-snapshot")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(self.snapshot.read_text())["recorded_at_commit"],
                         f"{head} + uncommitted changes")

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

    def check_provenance(self):
        return subprocess.run([sys.executable, str(self.harness / "score.py"),
                               "--check-provenance"], text=True, capture_output=True)

    def test_unchanged_inputs_validate(self):
        self.assertEqual(self.run_score("--write-snapshot").returncode, 0)
        self.assertEqual(self.check_provenance().returncode, 0)

    def test_changed_query_inputs_invalidate_snapshot(self):
        for field, value in [("q", "new wording"), ("expect", "no-trigger"), ("route", "/beta")]:
            with self.subTest(field=field):
                path = self.skill.parent / "evals" / "evals.json"
                original = path.read_text()
                self.assertEqual(self.run_score("--write-snapshot").returncode, 0)
                data = json.loads(original)
                data["queries"][0][field] = value
                path.write_text(json.dumps(data))
                self.assertNotEqual(self.check_provenance().returncode, 0)
                path.write_text(original)

    def test_external_catalog_change_invalidates_snapshot(self):
        self.assertEqual(self.run_score("--write-snapshot").returncode, 0)
        self.external.write_text("## External skills\n- **/beta** — Changed task.\n")
        self.assertNotEqual(self.check_provenance().returncode, 0)
        self.assert_rejected_after_existing_snapshot()

    def assert_rejected_after_existing_snapshot(self):
        before = self.snapshot.read_bytes()
        self.assertNotEqual(self.run_score("--write-snapshot").returncode, 0)
        self.assertEqual(self.snapshot.read_bytes(), before)

    def test_missing_skill_evals_invalidates_snapshot(self):
        self.assertEqual(self.run_score("--write-snapshot").returncode, 0)
        (self.skill.parent / "evals" / "evals.json").unlink()
        self.assertNotEqual(self.check_provenance().returncode, 0)
        self.assert_rejected_after_existing_snapshot()

    def test_catalog_context_change_invalidates_snapshot(self):
        self.assertEqual(self.run_score("--write-snapshot").returncode, 0)
        self.external.write_text("Routing context changed.\n" + self.external.read_text())
        self.assertNotEqual(self.check_provenance().returncode, 0)
        self.assert_rejected_after_existing_snapshot()

    def test_invocation_policy_change_invalidates_snapshot(self):
        self.assertEqual(self.run_score("--write-snapshot").returncode, 0)
        self.skill.write_text(self.skill.read_text().replace("name: alpha\n",
                                                            "name: alpha\ndisable-model-invocation: true\n"))
        self.assertNotEqual(self.check_provenance().returncode, 0)


if __name__ == "__main__":
    unittest.main()

"""Regression tests for the behavior-eval scorer.

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.
"""
import json
import tempfile
import unittest
from pathlib import Path

import importlib.util

spec = importlib.util.spec_from_file_location("score", Path(__file__).with_name("score.py"))
score = importlib.util.module_from_spec(spec)
spec.loader.exec_module(score)

FIXTURE = "```text\n**Found:** a: b; c.\n\n**Next:** One.\n\n**Stage:** [x] go.\n```\n"
GOOD = "**Found:** 2 things: one two; three four.\n\n**Next:** Do it. Then stop.\n\n**Stage:** [x] go.\n"


class ScoreTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dir = Path(tmp.name)
        (self.dir / "fixture.md").write_text(FIXTURE)
        (self.dir / "ref.md").write_text(GOOD)
        self.checks = self.dir / "checks.json"
        self.checks.write_text(json.dumps({"C": {
            "fixture": "fixture.md", "reference": "ref.md", "max_words": 20,
            "list_labels": ["**Found:**"], "max_item_words": 3,
            "sentence_labels": ["**Next:**"], "max_sentences": 2,
            "protected": ["**Found:**", "**Next:**", "[x]"]}}))

    def run_case(self, text):
        out = self.dir / "out.md"
        out.write_text(text)
        return score.score(self.checks, "C", out)[1]

    def test_reference_passes(self):
        self.assertEqual(score.score(self.checks, "C")[1], [])

    def test_fenced_output_is_scored(self):
        self.assertEqual(self.run_case("Notes.\n```text\n" + GOOD + "```\nMore notes."), [])

    def test_total_words(self):
        self.assertTrue(any("words; limit 20" in e for e in self.run_case(GOOD + " pad" * 10)))

    def test_long_item(self):
        errors = self.run_case(GOOD.replace("one two", "one two three four"))
        self.assertTrue(any("item has 4 words" in e for e in errors))

    def test_items_stop_at_sentence_end(self):
        self.assertEqual(self.run_case(GOOD.replace("four.", "four. Then five six seven.")), [])

    def test_sentence_count(self):
        errors = self.run_case(GOOD.replace("Then stop.", "Then stop. Then rest."))
        self.assertTrue(any("3 sentences" in e for e in errors))

    def test_protected_span_dropped(self):
        errors = self.run_case(GOOD.replace("[x] ", ""))
        self.assertTrue(any("'[x]'" in e for e in errors))


if __name__ == "__main__":
    unittest.main()

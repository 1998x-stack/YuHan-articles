"""Maintain exact, distinct attribution for the five Han Yu originals."""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_site import collect_classics


class HanYuClassicTests(unittest.TestCase):
    def test_all_five_published_originals_are_present(self):
        classics = collect_classics(ROOT)
        self.assertEqual([entry["title"] for entry in classics], [
            "师说", "马说", "进学解", "原道", "祭十二郎文"
        ])
        self.assertEqual([entry["order"] for entry in classics], [1, 2, 3, 4, 5])
        self.assertEqual(len(classics), 5)
        for entry in classics:
            with self.subTest(title=entry["title"]):
                self.assertTrue(entry["source_path"].is_file())
                self.assertIn("classics", entry["source_path"].parts)
                self.assertIn(entry["title"], entry["source_path"].read_text(encoding="utf-8").splitlines()[0])
                self.assertGreater(len(str(entry["html"])), 150)
                self.assertTrue((entry["source_path"].parent / "README.md").is_file())

    def test_metadata_has_original_author_attribution_and_source(self):
        records = sorted((ROOT / "classics").glob("*/meta.json"))
        self.assertEqual(len(records), 5)
        for path in records:
            meta = json.loads(path.read_text(encoding="utf-8"))
            with self.subTest(path=path):
                self.assertEqual(meta["author"], "韩愈")
                self.assertEqual(meta["dynasty"], "唐")
                self.assertEqual(meta["status"], "published")
                self.assertTrue(meta["source_url"].startswith("https://zh.wikisource.org/"))
                self.assertEqual(meta["slug"], path.parent.name)
                self.assertTrue((path.parent / meta["manuscript"]).is_file())

    def test_originals_do_not_replace_modern_adaptations(self):
        for manuscript in (ROOT / "classics").glob("*/*.md"):
            if manuscript.name == "README.md":
                continue
            text = manuscript.read_text(encoding="utf-8")
            self.assertTrue(text.startswith("# "))
            self.assertNotIn("（AI重写）", text)


if __name__ == "__main__":
    unittest.main()

"""Repository metadata validation and path traversal regression coverage."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_repository import audit, check_articles, valid_basename


class RepositoryValidationTests(unittest.TestCase):
    def test_existing_repository_passes(self):
        errors, stats = audit(ROOT)
        self.assertEqual(errors, [])
        self.assertGreaterEqual(stats["published_articles"], 1)
        self.assertGreaterEqual(stats["published_classics"], 5)

    def test_reject_unsafe_manuscript_filenames(self):
        for value in ("../secret.md", "/tmp/secret.md", r"..\secret.md", "a/b.md",
                      "doc.txt", None, ""):
            with self.subTest(value=value):
                self.assertFalse(valid_basename(value, ".md"))
        self.assertTrue(valid_basename("原富民论.md", ".md"))

    def test_draft_not_counted_as_published(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            folder = root / "articles" / "01-测试" / "小类" / "文章"
            folder.mkdir(parents=True)
            for p in (folder.parent.parent, folder.parent, folder):
                (p / "README.md").write_text("# 测试\n", encoding="utf-8")
            payload = {
                "title": "文章", "manuscript": "文章.md", "category": "01-测试",
                "subcategory": "小类", "date": "2026-01-01",
                "status": "draft", "topics": [],
            }
            (folder / "article.json").write_text(
                json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            (folder / "文章.md").write_text("# 文章\n\n这是尚未发表的草稿。\n", encoding="utf-8")
            errors, published = check_articles(root, require_exports=True)
            self.assertEqual(errors, [])
            self.assertEqual(published, 0)

    def test_invalid_source_path_is_rejected(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            folder = root / "articles" / "01-测试" / "小类" / "文章"
            folder.mkdir(parents=True)
            for p in (folder.parent.parent, folder.parent, folder):
                (p / "README.md").write_text("# 测试\n", encoding="utf-8")
            payload = {
                "title": "文章", "manuscript": "../../secret.md",
                "category": "01-测试", "subcategory": "小类",
                "date": "2026-01-01", "status": "published", "topics": [],
            }
            (folder / "article.json").write_text(
                json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            errors, _ = check_articles(root)
            self.assertTrue(any("safe local" in issue for issue in errors))


if __name__ == "__main__":
    unittest.main()

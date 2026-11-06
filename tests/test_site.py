"""Regression tests for static HTML generation and Markdown safety."""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_site import build, collect, encode_route, normalize_numeric_footnotes, sanitize


class SiteBuildTests(unittest.TestCase):
    def test_unicode_url_segments(self):
        encoded = encode_route("read/01-史论与人物/史事辨/河伯娶妇辨/")
        self.assertTrue(encoded.startswith("read/01-"))
        self.assertIn("%E5%8F%B2", encoded)
        self.assertTrue(encoded.endswith("/"))
        self.assertNotIn("史论", encoded)

    def test_html_sanitizer_blocks_scripts_and_attributes(self):
        raw = '<p onclick="run()">正文 <a href="javascript:alert(1)" onmouseover="run()">链接</a></p><script>alert(1)</script>'
        cleaned = str(sanitize(raw))
        self.assertIn("正文", cleaned)
        self.assertNotIn("<script", cleaned)
        self.assertNotIn("onclick", cleaned)
        self.assertNotIn("onmouseover", cleaned)
        self.assertNotIn("javascript:", cleaned)

    def test_legacy_footnotes_are_linked_without_mutating_source(self):
        raw = "文中证据〔1〕。\n\n[^1]: 可核查的资料。"
        converted = normalize_numeric_footnotes(raw)
        self.assertIn("[^1]", converted)
        self.assertIn("[^1]:", converted)
        self.assertIn("〔1〕", raw)

    def create_fixture(self, folder: Path, *, status: str = "published", manuscript: str = "试稿.md"):
        article = folder / "articles" / "01-史论与人物" / "史事辨" / "试稿"
        article.mkdir(parents=True, exist_ok=True)
        (folder / "articles" / "01-史论与人物" / "README.md").write_text(
            "# 史论与人物\n\n历史、人物、论辨与证据。\n", encoding="utf-8"
        )
        (article / "article.json").write_text(json.dumps({
            "title": "试稿", "category": "01-史论与人物",
            "subcategory": "史事辨", "status": status, "date": "2026-11-06",
            "manuscript": manuscript, "topics": ["证据", "名实"],
        }, ensure_ascii=False), encoding="utf-8")
        (article / "试稿.md").write_text(
            '# 试稿\n\n此文只作自动化验收，讨论名实与证据，不冒充古籍或史事。〔1〕\n\n'
            '[^1]: 编者自拟的示例注释。\n', encoding="utf-8"
        )
        return article

    def test_only_published_valid_manuscripts_are_collected(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            self.create_fixture(root, status="draft")
            cats, essays = collect(root)
            self.assertEqual(len(cats), 1)
            self.assertEqual(essays, [])
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            self.create_fixture(root, manuscript="../unrelated.md")
            with self.assertRaisesRegex(ValueError, "Unsafe manuscript"):
                collect(root)

    def test_complete_static_site_is_built_from_one_markdown_source(self):
        with tempfile.TemporaryDirectory() as name:
            root = Path(name)
            original = self.create_fixture(root)
            shutil.copytree(ROOT / "site", root / "site")
            out = root / "_site"
            result = build(root, out, "https://example.github.io/demo/", "sample/demo")
            self.assertEqual(result["articles"], 1)
            self.assertEqual(result["categories"], 1)
            home = (out / "index.html").read_text(encoding="utf-8")
            page = out / "read" / "01-史论与人物" / "史事辨" / "试稿" / "index.html"
            article_html = page.read_text(encoding="utf-8")
            self.assertTrue((out / "articles" / "index.html").is_file())
            self.assertTrue((out / "categories" / "01-史论与人物" / "index.html").is_file())
            self.assertIn("/demo/assets/style.css", home)
            self.assertIn("试稿", article_html)
            self.assertIn("footnote-ref", article_html)
            self.assertIn("fnref:1", article_html)
            self.assertEqual(original.joinpath("试稿.md").read_text(encoding="utf-8").count("〔1〕"), 1)


if __name__ == "__main__":
    unittest.main()

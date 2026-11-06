"""Font discovery must work even on machines without installed CJK fonts."""
from __future__ import annotations

import importlib.util
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build_articles.py"
spec = importlib.util.spec_from_file_location("build_articles_for_test", SCRIPT)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)


class FontSelectionTests(unittest.TestCase):
    def test_cid_fallback_with_no_fonts(self):
        with patch.dict(os.environ, {"YUHAN_CJK_FONT": ""}), patch.object(
            module, "CJK_FONTS", []
        ):
            with self.assertWarnsRegex(RuntimeWarning, "not embed"):
                self.assertEqual(module.pick_font(), "STSong-Light")

    def test_explicit_missing_override_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = Path(directory) / "not-installed.ttf"
            with patch.dict(os.environ, {"YUHAN_CJK_FONT": str(missing)}):
                with self.assertRaisesRegex(FileNotFoundError, "missing file"):
                    module.pick_font()

    def test_cid_pdf_can_render_chinese_text(self):
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.platypus import Paragraph, SimpleDocTemplate
        with patch.dict(os.environ, {"YUHAN_CJK_FONT": ""}), patch.object(
            module, "CJK_FONTS", []
        ):
            with self.assertWarns(RuntimeWarning):
                font = module.pick_font()
            with tempfile.TemporaryDirectory() as directory:
                destination = Path(directory) / "chinese.pdf"
                SimpleDocTemplate(str(destination)).build([
                    Paragraph("古文论辩 <b>中文测试</b>", ParagraphStyle(
                        "testcjk", fontName=font, wordWrap="CJK"))
                ])
                self.assertTrue(destination.is_file())
                self.assertGreater(destination.stat().st_size, 500)


if __name__ == "__main__":
    unittest.main()

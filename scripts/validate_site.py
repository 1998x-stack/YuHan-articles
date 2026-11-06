#!/usr/bin/env python3
"""Verify rendered pages, local links, static assets, and safe Markdown HTML."""
from __future__ import annotations

import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class Inspect(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.ids = set()
        self.has_title = False

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        if attr.get("id"):
            self.ids.add(attr["id"])
        if tag == "title":
            self.has_title = True
        if tag == "a" and attr.get("href"):
            self.links.append(attr["href"])
        if tag in ("script", "img") and attr.get("src"):
            self.links.append(attr["src"])
        if tag == "link" and attr.get("rel") in ("stylesheet", "icon") and attr.get("href"):
            self.links.append(attr["href"])


def validate(root: Path, base: str, expected: int, min_classics: int = 0) -> list[str]:
    errors = []
    root = root.resolve()
    pages = sorted(root.rglob("*.html"))
    if not (root / "index.html").is_file() or len(pages) < expected + 12:
        errors.append("Homepage/category/article pages missing")
    for page in pages:
        data = page.read_text(encoding="utf-8")
        parser = Inspect()
        parser.feed(data)
        if not parser.has_title or 'lang="zh-CN"' not in data:
            errors.append(f"{page}: missing HTML language or title")
        if not re.search(r'<main\b[^>]*\bid="content"', data):
            errors.append(f"{page}: missing accessible main landmark")
        if '<div class="prose" id="article-body">' in data:
            prose = data.split('<div class="prose" id="article-body">', 1)[1].split(
                '<div class="article__end"', 1
            )[0]
            if re.search(r"<script\b|<iframe\b|(?:javascript|data):", prose, re.I):
                errors.append(f"{page}: unsafe Markdown output")
        for href in parser.links:
            if href.startswith("#"):
                if href[1:] and unquote(href[1:]) not in parser.ids:
                    errors.append(f"{page}: broken fragment {href}")
                continue
            if href.startswith(("mailto:", "tel:")):
                continue
            parsed = urlsplit(href)
            if parsed.scheme or parsed.netloc:
                continue
            if not parsed.path.startswith(base):
                errors.append(f"{page}: link escapes project URL: {href}")
                continue
            local = unquote(parsed.path[len(base):])
            target = root / local.lstrip("/")
            if local.endswith("/") or not target.suffix:
                target /= "index.html"
            # An encoded ../ link must not lead outside _site.
            if not target.resolve().is_relative_to(root):
                errors.append(f"{page}: local link escapes built site: {href}")
                continue
            if not target.is_file():
                errors.append(f"{page}: missing local target: {href}")
            if parsed.fragment and target.resolve() == page.resolve():
                if unquote(parsed.fragment) not in parser.ids:
                    errors.append(f"{page}: broken anchor: {href}")
    if min_classics:
        original_index = root / "classics" / "index.html"
        originals = list((root / "classics").glob("*/index.html"))
        if not original_index.is_file() or len(originals) < min_classics:
            errors.append(
                f"Expected at least {min_classics} complete Han Yu original pages, "
                f"found {len(originals)}"
            )
    search = root / "search-index.json"
    if not search.is_file():
        errors.append("Missing search-index.json")
    elif len(json.loads(search.read_text(encoding="utf-8"))) < expected:
        errors.append("Search index has fewer articles than expected")
    for name in ("assets/style.css", "assets/site.js", "assets/favicon.svg",
                 "404.html", "sitemap.xml", "feed.xml", ".nojekyll"):
        if not (root / name).exists():
            errors.append(f"Missing {name}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path, default=Path("_site"))
    parser.add_argument("--base-path", default="/YuHan-articles/")
    parser.add_argument("--min-articles", type=int, default=1)
    parser.add_argument("--min-classics", type=int, default=0)
    args = parser.parse_args()
    errors = validate(args.site, args.base_path, args.min_articles, args.min_classics)
    if errors:
        for err in errors:
            print("ERROR:", err)
        print("FAILED:", len(errors), "site validation issues")
        return 1
    print("OK: site assets, navigation links and Markdown output")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

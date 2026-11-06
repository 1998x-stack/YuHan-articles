#!/usr/bin/env python3
"""Check archive integrity, manuscript provenance, and documentation links.

Uses only the Python standard library. Run before generating a site, after
writing article metadata, and in GitHub Actions on pull requests.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
VALID_STATES = {"draft", "review", "published", "archived"}
CATEGORY_PATTERN = re.compile(r"^\d{2}-.+")
SLUG_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_PATTERN = re.compile(r"(?<!!)\[[^\]]+\]\(([^)\n]+)\)")


def valid_basename(name: object, suffix: str) -> bool:
    """Allow a single local file name, never a relative or absolute path."""
    return (
        isinstance(name, str)
        and bool(name)
        and name not in {".", ".."}
        and Path(name).name == name
        and "/" not in name
        and "\\" not in name
        and name.endswith(suffix)
    )


def check_articles(root: Path, require_exports: bool = False) -> tuple[list[str], int]:
    problems: list[str] = []
    base = root / "articles"
    category_dirs = sorted(
        p for p in base.iterdir() if p.is_dir() and CATEGORY_PATTERN.fullmatch(p.name)
    )
    if not category_dirs:
        problems.append("articles/: no numbered category directories")
    for cat in category_dirs:
        if not (cat / "README.md").is_file():
            problems.append(f"{cat}: missing README.md")

    published = 0
    paths = sorted(base.rglob("article.json"))
    for path in paths:
        parts = path.relative_to(base).parts
        if "_templates" in parts:
            continue
        if len(parts) != 4 or not CATEGORY_PATTERN.fullmatch(parts[0]):
            problems.append(f"{path}: expected articles/category/subcategory/title/article.json")
            continue
        category, subcategory, title_dir, _ = parts
        label = path.relative_to(root).as_posix()
        try:
            meta = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            problems.append(f"{label}: invalid JSON ({exc})")
            continue
        if not isinstance(meta, dict):
            problems.append(f"{label}: metadata must be an object")
            continue
        if meta.get("category") != category or meta.get("subcategory") != subcategory:
            problems.append(f"{label}: metadata category/subcategory differs from directory")
        title = meta.get("title")
        if not isinstance(title, str) or not title.strip():
            problems.append(f"{label}: empty or invalid title")
        if meta.get("status") not in VALID_STATES:
            problems.append(f"{label}: status must be {sorted(VALID_STATES)}")
        when = meta.get("date")
        try:
            date.fromisoformat(when)
        except (TypeError, ValueError):
            problems.append(f"{label}: invalid ISO date {when!r}")
        tags = meta.get("topics", [])
        if not isinstance(tags, list) or any(
            not isinstance(t, str) or not t.strip() for t in tags
        ):
            problems.append(f"{label}: topics must be a list of nonblank strings")
        if not (path.parent / "README.md").is_file():
            problems.append(f"{label}: missing per-article README.md")
        if not (base / category / subcategory / "README.md").is_file():
            problems.append(f"{label}: missing subcategory README.md")

        manuscript = meta.get("manuscript")
        if not valid_basename(manuscript, ".md"):
            problems.append(f"{label}: manuscript must be a safe local .md filename")
            continue
        source = path.parent / manuscript
        if source.is_symlink() or not source.is_file():
            problems.append(f"{label}: missing or symlinked manuscript {manuscript}")
            continue
        try:
            if source.resolve().parent != path.parent.resolve():
                problems.append(f"{label}: manuscript escapes its article directory")
                continue
            content = source.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            problems.append(f"{label}: unreadable manuscript ({exc})")
            continue
        first_line = content.splitlines()[0].strip() if content.splitlines() else ""
        if first_line != "# " + str(title):
            problems.append(f"{label}: first Markdown H1 must match article.json title")
        if meta.get("status") == "published":
            published += 1
            if len(content.strip()) < 90:
                problems.append(f"{label}: published body too short")
            if require_exports:
                for ext in (".docx", ".pdf"):
                    target = source.with_suffix(ext)
                    if not target.is_file() or target.stat().st_size < 100:
                        problems.append(f"{label}: missing or empty {ext} export")
    return problems, published


def check_classics(root: Path) -> tuple[list[str], int]:
    errors: list[str] = []
    base = root / "classics"
    if not base.is_dir():
        return ["classics/: missing originals directory"], 0
    orders: set[int] = set()
    published = 0
    for manifest in sorted(base.glob("*/meta.json")):
        label = manifest.relative_to(root)
        try:
            meta = json.loads(manifest.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{label}: invalid JSON: {exc}")
            continue
        if meta.get("slug") != manifest.parent.name or not SLUG_PATTERN.fullmatch(manifest.parent.name):
            errors.append(f"{label}: slug differs from directory")
        if meta.get("author") != "韩愈" or meta.get("dynasty") != "唐":
            errors.append(f"{label}: original attribution must be Han Yu / Tang")
        if meta.get("status") not in {"draft", "published"}:
            errors.append(f"{label}: unsupported original status")
        order = meta.get("order")
        if type(order) is not int or order < 1 or order in orders:
            errors.append(f"{label}: missing or duplicate positive order")
        else:
            orders.add(order)
        manuscript = meta.get("manuscript")
        if not valid_basename(manuscript, ".md"):
            errors.append(f"{label}: unsafe original manuscript filename")
        else:
            source = manifest.parent / manuscript
            if source.is_symlink() or not source.is_file():
                errors.append(f"{label}: missing original manuscript")
            elif not source.read_text(encoding="utf-8").splitlines()[0].strip().startswith("# " + str(meta.get("title"))):
                errors.append(f"{label}: original H1 does not match metadata")
        if not (manifest.parent / "README.md").is_file():
            errors.append(f"{label}: missing edition and source notes")
        url = meta.get("source_url", "")
        parsed = urlsplit(url) if isinstance(url, str) else None
        if not parsed or parsed.scheme != "https" or not parsed.hostname:
            errors.append(f"{label}: original source URL must be https")
        if meta.get("status") == "published":
            published += 1
    return errors, published


def check_docs(root: Path) -> list[str]:
    """Check canonical project docs; article manuscripts can cite external sources."""
    checks = [
        root / "README.md", root / "AGENTS.md",
        root / "articles" / "README.md", root / "articles" / "TAXONOMY.md",
        root / "articles" / "STRUCTURE.md",
        root / "classics" / "README.md",
        root / "site" / "README.md",
        *sorted((root / "docs").glob("*.md")),
    ]
    errors: list[str] = []
    for file in checks:
        if not file.is_file():
            errors.append(f"{file.relative_to(root)}: documentation file missing")
            continue
        text = file.read_text(encoding="utf-8")
        for match in LINK_PATTERN.finditer(text):
            href = match.group(1).strip().split()[0].strip("<>")
            parsed = urlsplit(href)
            if parsed.scheme or parsed.netloc or not parsed.path or href.startswith("#"):
                continue
            target = (file.parent / unquote(parsed.path)).resolve()
            if not target.is_relative_to(root.resolve()):
                errors.append(f"{file.relative_to(root)}: link escapes repository: {href}")
            elif not (target.is_file() or (target.is_dir() and (target / "README.md").is_file())):
                errors.append(f"{file.relative_to(root)}: broken local link: {href}")
    return errors


def audit(root: Path, require_exports: bool = False) -> tuple[list[str], dict[str, int]]:
    root = root.resolve()
    article_errors, articles = check_articles(root, require_exports=require_exports)
    classic_errors, classics = check_classics(root)
    doc_errors = check_docs(root)
    return article_errors + classic_errors + doc_errors, {
        "published_articles": articles, "published_classics": classics
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=ROOT)
    parser.add_argument("--require-exports", action="store_true",
                        help="require DOCX/PDF for each published article")
    args = parser.parse_args()
    errors, stats = audit(args.repo_root, require_exports=args.require_exports)
    if errors:
        for issue in errors:
            print("ERROR:", issue, file=sys.stderr)
        print(f"FAIL: {len(errors)} repository issue(s)", file=sys.stderr)
        return 1
    print(f"OK: {stats['published_articles']} published modern articles, "
          f"{stats['published_classics']} original works; metadata, paths and documentation links valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

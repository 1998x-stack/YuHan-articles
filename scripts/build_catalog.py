#!/usr/bin/env python3
"""Maintain articles/CATALOG.md from published article.json manifests.

Never invent records or link to missing exported files. All titles and paths
come from real metadata and Markdown manuscripts.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
ARTICLES=ROOT/"articles"
CATALOG=ARTICLES/"CATALOG.md"


def render() -> str:
    categories=sorted(p for p in ARTICLES.iterdir() if p.is_dir() and
                      len(p.name)>3 and p.name[:2].isdigit() and p.name[2]=="-")
    rows=[]
    for path in sorted(ARTICLES.rglob("article.json")):
        parts=path.relative_to(ARTICLES).parts
        if "_templates" in parts:
            continue
        if len(parts)!=4:
            raise ValueError(f"Unexpected article.json location: {path}")
        meta=json.loads(path.read_text(encoding="utf-8"))
        if meta.get("status")!="published":
            continue
        cat,sub,folder,_=parts
        if meta.get("category")!=cat or meta.get("subcategory")!=sub:
            raise ValueError(f"Metadata/path classification mismatch: {path}")
        filename=meta.get("manuscript")
        if not isinstance(filename,str) or Path(filename).name!=filename or not filename.endswith(".md"):
            raise ValueError(f"Unsafe manuscript name: {path}")
        source=path.parent/filename
        if not source.is_file():
            raise FileNotFoundError(f"Missing published manuscript: {source}")
        title=meta.get("title")
        if not isinstance(title,str) or not title:
            raise ValueError(f"Missing title: {path}")
        rel=source.relative_to(ARTICLES).as_posix()
        downloads=[]
        for ext in ("docx","pdf"):
            exported=source.with_suffix("."+ext)
            if exported.is_file():
                downloads.append(f"[{ext.upper()}]({exported.relative_to(ARTICLES).as_posix()})")
        downloads_text=" · ".join(downloads) if downloads else "排印文件待生成"
        rows.append((cat,sub,title,rel,downloads_text))
    lines=[
        "# 古文文章总目录","",
        "> 本文件由 scripts/build_catalog.py 根据实际已发表文章生成，勿手工修改。未完成条目不列入已刊目录。","",
        f"目前已收录 **{len(rows)}** 篇文章。阅读版采用 Markdown 源稿构建，出版格式来自同一正文。","",
        "| 部类 | 子目 | 篇名 | 源稿 | 出版格式 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for cat,sub,title,rel,downloads in rows:
        lines.append(f"| {cat} | {sub} | **{title}** | [Markdown]({rel}) | {downloads} |")
    lines.extend(["","## 八部主题导航",""])
    for cat in categories:
        lines.append(f"- [{cat.name}]({cat.name}/README.md)")
    lines.extend(["","[文章总库](README.md) · [详细分类](TAXONOMY.md) · [阅读网站](../docs/website.md)",""])
    return "\n".join(lines)


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check",action="store_true",help="fail if the committed catalog is stale")
    args=parser.parse_args()
    generated=render()
    if args.check:
        current=CATALOG.read_text(encoding="utf-8") if CATALOG.is_file() else ""
        if current!=generated:
            print("CATALOG.md is stale; run python3 scripts/build_catalog.py")
            return 1
        print("OK: articles/CATALOG.md is current")
        return 0
    if not CATALOG.is_file() or CATALOG.read_text(encoding="utf-8")!=generated:
        CATALOG.write_text(generated,encoding="utf-8")
        print("Updated articles/CATALOG.md")
    else:
        print("Article catalog already current")
    return 0


if __name__=="__main__":
    raise SystemExit(main())

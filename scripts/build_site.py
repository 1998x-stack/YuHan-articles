#!/usr/bin/env python3
"""Build a static reading site from published Markdown manuscripts."""
from __future__ import annotations
import argparse
import html
import json
import os
import re
import shutil
import xml.etree.ElementTree as ET
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import quote, urlsplit

import bleach
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markdown import Markdown
from markupsafe import Markup

ROOT = Path(__file__).resolve().parents[1]
TAGS = set(bleach.sanitizer.ALLOWED_TAGS) | {
    "h1","h2","h3","h4","h5","h6","p","br","hr",
    "pre","code","img","div","span","section","sup","sub",
    "table","thead","tbody","tr","th","td","del","s"
}
ATTRS = {
    "a":["href","title","id","class"],
    "img":["src","alt","title","width","height"],
    "h1":["id"],"h2":["id"],"h3":["id"],"h4":["id"],"h5":["id"],"h6":["id"],
    "div":["id","class"],"span":["id","class"],"sup":["id"],
    "li":["id"],"th":["scope","align"],"td":["align"],"code":["class"]
}


def sanitize(value: str) -> Markup:
    """Whitelist rendered Markdown, including valid Markdown footnotes."""
    return Markup(bleach.clean(value, tags=TAGS, attributes=ATTRS,
                               protocols=["https","http","mailto"],
                               strip=True, strip_comments=True))


def encode_route(path: str) -> str:
    trailing = path.endswith("/")
    encoded = "/".join(quote(p, safe="") for p in path.strip("/").split("/") if p)
    return encoded + ("/" if trailing and encoded else "")


def summarize(text: str, limit: int = 114) -> str:
    text = re.sub(r"\[\^[^\]]+\]", "", text)
    text = re.sub(r"!?\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[\x60*_~#>{}\[\]]", "", text)
    text = re.sub(r"\s+", " ", html.unescape(text)).strip()
    return text[:limit].rstrip("，。、；;：: ") + ("…" if len(text) > limit else "")


def excerpt(content: str) -> str:
    for block in re.split(r"\n\s*\n", content):
        s = block.strip()
        if not s or s.startswith(("# ","<!--","---","[^","~~~")) or s.startswith(chr(96)*3):
            continue
        result = summarize(s.lstrip("> "))
        if len(result) >= 16:
            return result
    return "阅读文中完整论辩与相关依据。"


def category_description(folder: Path) -> str:
    readme = folder / "README.md"
    if readme.is_file():
        for line in readme.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if s and not s.startswith(("#","-",">","[","|","预设","已收录","收录")):
                result = summarize(s, 88)
                if len(result) >= 8:
                    return result
    return "从本专题的史事、义理与制度出发开展古文论说。"


def normalize_numeric_footnotes(source: str) -> str:
    """Link existing 〔1〕 citation markers to matching Markdown [^1] notes.

    Preserves the canonical manuscript on disk; normalization is HTML-only.
    Some legacy essays use inline typographical references with Markdown
    footnote definitions, which otherwise produce dead backlink anchors.
    """
    labels = set(re.findall(r"(?m)^\[\^([0-9]+)\]:", source))
    for label in labels:
        source = source.replace("〔" + label + "〕", "[^" + label + "]")
    return source


def collect(root: Path) -> tuple[list[dict], list[dict]]:
    base = root / "articles"
    if not base.is_dir():
        raise FileNotFoundError(f"No article source folder: {base}")
    categories = [
        {"slug": p.name, "label": p.name[3:], "number": p.name[:2],
         "description": category_description(p), "count": 0, "url": ""}
        for p in sorted(base.iterdir()) if p.is_dir() and re.fullmatch(r"\d{2}-.+",p.name)
    ]
    if not categories:
        raise ValueError("No taxonomy categories found")
    known = {c["slug"] for c in categories}
    articles = []
    for manifest in sorted(base.rglob("article.json")):
        parts = manifest.relative_to(base).parts
        if "_templates" in parts:
            continue
        if len(parts) != 4 or parts[0] not in known:
            raise ValueError(f"Manifest must be inside category/subcategory/title: {manifest}")
        meta = json.loads(manifest.read_text(encoding="utf-8"))
        if meta.get("status") != "published":
            continue
        category, subcategory, folder, _ = parts
        if meta.get("category") != category or meta.get("subcategory") != subcategory:
            raise ValueError(f"Metadata category mismatch: {manifest}")
        name, title = meta.get("manuscript"), meta.get("title")
        if not isinstance(name, str) or Path(name).name != name or not name.endswith(".md"):
            raise ValueError(f"Unsafe manuscript path: {manifest}")
        if not isinstance(title, str) or not title.strip():
            raise ValueError(f"Missing article title: {manifest}")
        source = manifest.parent / name
        if not source.is_file():
            raise FileNotFoundError(f"Published Markdown missing: {source}")
        published = meta.get("date")
        try:
            date.fromisoformat(published)
        except (ValueError, TypeError) as exc:
            raise ValueError(f"Invalid article date: {manifest}") from exc
        topics = meta.get("topics", [])
        if not isinstance(topics, list) or not all(isinstance(x,str) for x in topics):
            raise ValueError(f"Invalid topics: {manifest}")
        raw = source.read_text(encoding="utf-8")
        body = re.sub(r"(?m)^\s*# .+(?:\r?\n|$)", "", raw, count=1).strip()
        if not body:
            raise ValueError(f"Empty published article: {source}")
        md = Markdown(extensions=["extra", "toc", "sane_lists"])
        rendered = md.convert(normalize_numeric_footnotes(body))
        articles.append({
            "title":title,"date":published,"topics":topics,
            "category":category,"category_slug":category,
            "category_label":category[3:],"subcategory":subcategory,
            "route":f"read/{category}/{subcategory}/{folder}/",
            "excerpt":excerpt(body),"reading_minutes":max(1,round(len(re.sub(r"\s+","",body))/470)),
            "html":sanitize(rendered),"toc":sanitize(getattr(md,"toc","")),
            "source_path":source,"manifest_path":manifest,"url":"","source_url":"",
            "pdf_url":None,"docx_url":None,"search_text":""
        })
    articles.sort(key=lambda x:(x["date"],x["title"]),reverse=True)
    for category in categories:
        category["count"] = sum(a["category"]==category["slug"] for a in articles)
    return categories,articles


def build(root: Path, output: Path, site_url: str, repo: str) -> dict:
    parsed = urlsplit(site_url)
    if parsed.scheme not in ("https","http") or not parsed.netloc or parsed.query or parsed.fragment:
        raise ValueError("--site-url must be a valid absolute HTTP(S) URL")
    if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+",repo):
        raise ValueError("--repo must be owner/repo")
    base_path = "/" + parsed.path.strip("/") + "/" if parsed.path.strip("/") else "/"
    origin = parsed.scheme + "://" + parsed.netloc
    def url_for(path: str="") -> str:
        return base_path + encode_route(path)
    def canonical(path: str="") -> str:
        return origin + url_for(path)
    def category_url(name: str) -> str:
        return url_for(f"categories/{name}/")
    categories, articles = collect(root)
    for category in categories:
        category["url"] = category_url(category["slug"])
    for item in articles:
        item["url"] = url_for(item["route"])
        original = item["source_path"].relative_to(root).as_posix()
        item["source_url"] = "https://github.com/" + repo + "/blob/main/" + encode_route(original)
        item["search_text"] = " ".join([item["title"],item["category_label"],
                                        item["subcategory"],item["excerpt"],*item["topics"]])
        for ext in ("pdf","docx"):
            source = item["source_path"].with_suffix("." + ext)
            if source.is_file():
                parent = item["manifest_path"].relative_to(root / "articles").parent.as_posix()
                item[ext+"_url"] = url_for("files/" + parent + "/" + source.name)

    output = output.resolve()
    if output.name != "_site" or output == root.resolve() or output.is_symlink():
        raise ValueError("Refusing to delete unsafe output; use a folder named _site")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    shutil.copytree(root/"site"/"static",output,dirs_exist_ok=True)
    (output/".nojekyll").touch()
    env = Environment(loader=FileSystemLoader(str(root/"site"/"templates")),
                      autoescape=select_autoescape(["html","xml"]),
                      keep_trailing_newline=True)
    commons = dict(repo=repo,categories=categories,articles=articles,
                   url_for=url_for,category_url=category_url,
                   year=datetime.now(timezone.utc).year)
    def render(path: str, template: str, kind: str, title: str, summary: str, **data) -> None:
        target = output/path/"index.html" if path else output/"index.html"
        target.parent.mkdir(parents=True,exist_ok=True)
        page = dict(kind=kind,title=title,description=summary,
                    canonical=canonical(path+"/" if path else ""))
        target.write_text(env.get_template(template).render(
            **commons,page=page,**data),encoding="utf-8")
    render("","home.html","home","古文论辩，义理相成","从 Markdown 构建的韩愈式古文论辩文集。")
    render("articles","archive.html","archive","文章目录","按主题与关键词检索已刊文言论说。")
    render("about","about.html","about","关于文集","古文写作方法、事实边界与原稿来源说明。")
    for category in categories:
        selected = [a for a in articles if a["category"]==category["slug"]]
        render("categories/"+category["slug"],"category.html","category",
               category["label"],category["description"],
               category=category,category_articles=selected)
    for index,item in enumerate(articles):
        render(item["route"].rstrip("/"),"article.html","article",
               item["title"],item["excerpt"],article=item,
               prev_article=articles[index-1] if index else None,
               next_article=articles[index+1] if index+1<len(articles) else None)
        for ext in ("pdf","docx"):
            if item[ext+"_url"]:
                original = item["source_path"].with_suffix("."+ext)
                dest = output/"files"/item["manifest_path"].relative_to(root/"articles").parent/original.name
                dest.parent.mkdir(parents=True,exist_ok=True)
                shutil.copy2(original,dest)
    (output/"404.html").write_text(env.get_template("not-found.html").render(
        **commons,page=dict(kind="not-found",title="未找到页面",
                            description="文章页面不存在。",canonical=canonical("404.html"))),
        encoding="utf-8")
    (output/"robots.txt").write_text(
        "User-agent: *\nAllow: /\nSitemap: "+canonical("sitemap.xml")+"\n",encoding="utf-8")
    routes = ["","articles/","about/"]+["categories/"+c["slug"]+"/" for c in categories]+[a["route"] for a in articles]
    site_xml = ET.Element("urlset",xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    for route in routes:
        entry = ET.SubElement(site_xml,"url")
        ET.SubElement(entry,"loc").text = canonical(route)
    ET.ElementTree(site_xml).write(output/"sitemap.xml",encoding="utf-8",xml_declaration=True)
    rss=ET.Element("rss",version="2.0")
    channel=ET.SubElement(rss,"channel")
    for key,value in (("title","韩愈文集 · 古文论辩"),("link",canonical("")),
                      ("description","Markdown 古文论辩文集"),("language","zh-cn")):
        ET.SubElement(channel,key).text=value
    for article in articles[:20]:
        row=ET.SubElement(channel,"item")
        for key,value in (("title",article["title"]),("link",canonical(article["route"])),
                          ("guid",canonical(article["route"])),("description",article["excerpt"]),
                          ("pubDate",datetime.fromisoformat(article["date"]).strftime("%a, %d %b %Y 00:00:00 +0000"))):
            ET.SubElement(row,key).text=value
    ET.ElementTree(rss).write(output/"feed.xml",encoding="utf-8",xml_declaration=True)
    (output/"search-index.json").write_text(json.dumps([
        dict(title=a["title"],url=a["url"],category=a["category_label"],
             date=a["date"],topics=a["topics"],excerpt=a["excerpt"])
        for a in articles],ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"Built {len(articles)} published articles and {len(categories)} category pages in {output}")
    return dict(articles=len(articles),categories=len(categories),output=output)


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root",type=Path,default=ROOT)
    parser.add_argument("--output",type=Path,default=ROOT/"_site")
    parser.add_argument("--repo",default=os.getenv("GITHUB_REPOSITORY","1998x-stack/YuHan-articles"))
    parser.add_argument("--site-url",default="https://1998x-stack.github.io/YuHan-articles/")
    args=parser.parse_args()
    build(args.repo_root.resolve(),args.output,args.site_url,args.repo)
    return 0


if __name__=="__main__":
    raise SystemExit(main())

# 新增现代文章 · 从选题到正式发表

> 本文仅指导 `articles/` 中的现代韩愈式论说作品。韩愈本人原作应进入 [classics/](../classics/README.md)，遵循 [原典版本规范](classic-editions.md)，**绝不可伪托韩愈署名**。

## 1. 按论题归类

先读 [八大部类与归档规则](../articles/TAXONOMY.md)，选择一个真实存在的一级目录及二级子目。文章以论证对象为准，不因篇名有“论”“辨”“说”就进入“杂说”类。跨领域关联写入 topics，不复制整篇正文。

已有公开路径及子目名称可能被外部引用；为统一名称而迁移时须评估旧链接与既有目录导航，避免随意破坏。

## 2. 复制模板并写元数据

从 [文章模板](../articles/_templates/article/README.md) 复制到选定目录（下面仅作举例）：

~~~text
articles/02-制度与治理/公共治理/示例辨/
├── README.md
├── article.json
└── 示例辨.md
~~~

article.json 示例：

~~~json
{
  "title": "示例辨",
  "manuscript": "示例辨.md",
  "category": "02-制度与治理",
  "subcategory": "公共治理",
  "date": "2026-11-06",
  "status": "draft",
  "topics": ["制度", "公共治理"]
}
~~~

其中 `category`、`subcategory` 必须与目录逐字相同；`manuscript` 为同目录的纯文件名，不得含 /、反斜线、绝对路径或相对跳转；日期为 ISO 的 YYYY-MM-DD。Markdown 首行必须为 `# 示例辨`。

## 3. 审稿而非仅润色

先保存真实的主张、关键事实、数字、史料与反方论据，再采用“推原究本—设难诘问—辨名核实—蓄势断案”等方法组织古文。需要引证时在文末保留规范出处，无法独立复核的统计或访谈应写明其来源层级。

编辑状态从 `draft` → `review` → `published`，停更可用 `archived`。**仅 published 正式进入网站与目录**。不得为了展示页面把仍未核验的草稿改为 published。

完整审校标准：[editorial-standard.md](editorial-standard.md)、[method-and-evidence.md](method-and-evidence.md) 和 [quality-rubric.md](quality-rubric.md)。

## 4. 验证文件与来源

~~~bash
python3 scripts/validate_repository.py
python3 -m unittest discover -s tests -p 'test_repository.py'
~~~

如果出现正文文件路径不安全、元数据与路径不符、标题不一致、日期无效或文档相对链接失效，必须先修复。这些检查不等于事实审稿，仍需人工核实引文、史料和当代数据。

## 5. 发布与生成件

人工确认适合公开后将 status 改为 `published`，然后：

~~~bash
python3 scripts/build_catalog.py
python3 scripts/build_catalog.py --check
python3 scripts/build_articles.py
python3 scripts/validate_repository.py --require-exports
~~~

文集总目 `articles/CATALOG.md` 是生成件，**不要手工更新条目数量或下载链接**。PDF/DOCX 与正文同名，发布器会从 Markdown 重新生成。原典有独立的在线阅读页，不由现代文章的 Word/PDF 出版器处理。

本地网页预览：

~~~bash
python3 -m pip install -r requirements-site.txt
python3 scripts/build_site.py --site-url http://localhost:8000/
python3 scripts/validate_site.py --base-path / --min-articles 1 --min-classics 5
python3 -m http.server 8000 --directory _site
~~~

## 6. 提交、部署与验收

提交文章的 Markdown、元数据、README 和需要更新的分类导航。GitHub Actions 在文章变更后构建 Word/PDF 和站点。确认 [出版工作流](../.github/workflows/publish-articles.yml) 与 [Pages 工作流](../.github/workflows/pages.yml) 实际成功，再检查网站对应页面、文章下载链接与排印效果。

**最低验收清单：** 分类正确；标题一致；状态准确；无虚构事实；来源可查；Markdown 可读；Word/PDF 可打开；GitHub Pages 无 404；不同屏幕大小的长文阅读正常。若生成件未成功，不应谎称已经完成三格式发布。

回滚、字体和 CI 排障见 [运维手册](maintainer-runbook.md)。

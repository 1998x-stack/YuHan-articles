# 文章归档与出版规范

## 1. 文档身份和权威源

- 现代文章目录位于 `articles/`，韩愈本人原作独立存于 `classics/`。
- 分类规范以 [TAXONOMY](../articles/TAXONOMY.md) 为准；本文件只规定**单篇档案、状态、格式与出版流程**。
- 现代文章唯一正文为同目录 Markdown；Word、PDF 和 HTML 从 Markdown 生成。
- 已刊总目 `articles/CATALOG.md` 由 `scripts/build_catalog.py` 自动生成。禁止手工增删总目条目。

## 2. 一文一档

~~~text
articles/02-制度与治理/纪检监察/论执纪之难/
├── README.md                    # 篇旨、来源说明与阅读入口
├── article.json                 # 元数据，非正文
├── 论执纪之难.md                # 唯一正文源
├── 论执纪之难.docx              # 已发表时的 Word 生成件
└── 论执纪之难.pdf               # 已发表时的 PDF 生成件
~~~

一级目录采用两位数字及中文主题，二级按真实问题域分类，三级单篇中文篇名。旧目录若已有公开 URL 不得仅为“统一命名”无计划迁移。重复主题只选一个主分类，其他关键词写入 topics。

## 3. article.json 契约

~~~json
{
  "title": "论执纪之难",
  "manuscript": "论执纪之难.md",
  "category": "02-制度与治理",
  "subcategory": "纪检监察",
  "date": "2026-11-06",
  "status": "published",
  "topics": ["纪检监察", "制度治理"]
}
~~~

路径、category/subcategory、标题与 Markdown 第一行的 H1 必须一致。`manuscript` 只接受本目录 UTF-8 `.md` 文件名，不可使用目录穿越或软链接到仓库外；`topics` 是字符串数组，`date` 是 YYYY-MM-DD。

状态：`draft` 草稿；`review` 审校；`published` 已发表；`archived` 归档。**当前所有公开生成器统一选择 published**，不因 `article.json` 文件存在就认定作品可发表。

## 4. 史料和作品边界

古文论证仍必须保存原文关键事实与论旨。史料引用、访谈转述、统计数字、作者推测及假设案例须区分，不能用雄健辞气取代校证。现代版权材料需有合理使用依据或授权，不能将他人全文偷录后改写成文言即声称自创。

原典不遵守现代文章的分类与同名 DOCX/PDF 契约：其作者、底本、异文独立记录，详见 [古文原典](classic-editions.md)。

## 5. 排印和字体

安装 `python-docx` 与 `reportlab`，执行：

~~~bash
python3 scripts/validate_repository.py
python3 scripts/build_articles.py
python3 scripts/validate_repository.py --require-exports
~~~

Word 使用可配置中文字体名称；PDF 优先嵌入兼容的 TrueType；若不可用则采用非嵌入的 STSong-Light CID 回退。**字体回退不保证跨平台排印一致**，正式出版需人工打开检查。详见 [fonts.md](fonts.md)。

Markdown 文末可用 `[^1]` 脚注与 `[^1]:` 来源记录。网页脚注与排印脚注处理方式不同，生成后需检查标记是否仍可读；若确有歧义，优先回到源稿统一规范，再改生成器。

## 6. 总目、网站与验收

~~~bash
python3 scripts/build_catalog.py
python3 scripts/build_catalog.py --check
python3 scripts/build_site.py
python3 scripts/validate_site.py --base-path /YuHan-articles/ --min-classics 5
~~~

Pages 使用 `/YuHan-articles/` 项目子路径，本地预览应将构站参数 `--site-url` 与校验器 `--base-path` 同步设置为本地根路径。生成结果位于仓库 `_site/`，不作为正文源提交。

GitHub Actions 可能在同时出版多篇文章时发生并发变化；出版器须从最新 main 重新构建二进制，不能通过 rebasing PDF/DOCX 合并差异。

## 7. 审稿与链接检查

结构校验只能验证文件、元数据与站内链接，不代表古文史实已完成独立考据。发表前至少人工确认：题名、主张、原典署名、时间口径、引用、Word/PDF 中文显示、移动端 HTML 和下载页面可达。旧 URL 需要迁移时应先评估兼容方式。

具体操作：[新增文章](adding-an-article.md) · [编辑标准](editorial-standard.md) · [仓库运维](maintainer-runbook.md)。

# 文章库结构 · Structure

> 本文说明**文件系统**；现行八部分类和新增子目的唯一规范源是 [TAXONOMY.md](TAXONOMY.md)。不要在此维护一份与真实目录容易漂移的分类全量表。

## 三级目录

~~~text
articles/
├── README.md                  # 读者入口与分类导航
├── CATALOG.md                 # build_catalog.py 自动生成
├── TAXONOMY.md                # 主题归类规范源
├── STRUCTURE.md               # 本文，说明目录结构
├── _templates/
│   └── article/               # 新篇结构模板
├── 01-史论与人物/
│   ├── README.md              # 一级部类导读
│   └── 史事辨/
│       ├── README.md          # 子目定义，空子目亦需真实说明
│       └── 河伯娶妇辨/
│           ├── README.md
│           ├── article.json
│           ├── 河伯娶妇辨.md
│           ├── 河伯娶妇辨.docx
│           └── 河伯娶妇辨.pdf
└── ...（其余编号部类）
~~~

**一篇一档**。一级取核心论题，二级表示问题域，三级是固定篇名目录；不按 `.md/.pdf/.docx` 另造三套目录。同一篇文章只能有一个权威 Markdown，其余导出格式与网站 HTML 从该文件生成。

## 文件与元数据

每篇 article.json 指定 title、manuscript、category、subcategory、date、status、topics。`manuscript` 必须是相同目录中的真实 Markdown basename，首行 H1 与 title 一致。状态支持 draft、review、published、archived；仅 published 进入已刊总目和自动出版。

正规 JSON 结构和示例见 [归档规范](../docs/article-archive-conventions.md)。

## 占位和旧子目

Git 不跟踪空目录，预留子目应用有内容的 README：列收录范围、归类边界、返回上级入口与未刊状态。**不制造虚构文章、空白 `article.json` 或假出版物**。

现存仓库存在“史事辨／史事辨析”“公共治理／公共政策”等近义子目。这是历史上的真实目录，不能直接删除或批量移动：先判断正式文章归属、检查所有内部链接及公开网页路由，再提出合并与迁移方案。可优先在子目 README 交叉指向另一类，以降低分类漂移。

## 生成与发布

~~~bash
python3 scripts/validate_repository.py
python3 scripts/build_catalog.py
python3 scripts/build_catalog.py --check
python3 scripts/build_articles.py
python3 scripts/validate_repository.py --require-exports
~~~

网站由 `scripts/build_site.py` 读取已刊现代作品，另外从 `classics/` 读取**韩愈本人原典**。两种文本既不能合并作者署名，也不能将现代仿作存入原典目录。

完整投稿路径见 [新增文章操作](../docs/adding-an-article.md)，分类位置见 [TAXONOMY](TAXONOMY.md)，技术边界见 [architecture](../docs/architecture.md)。

# 现代韩愈式论辩文章库 · articles/

> 本库收录现代史论、制度、经济、社会等议题的**韩愈式文言创作**，不是韩愈本人原作；原典请至 [classics/](../classics/README.md)。

## 八部专题导航

| 部类 | 入口 | 内容重点 |
| --- | --- | --- |
| 01 史论与人物 | [打开](01-史论与人物/README.md) | 史实、人物、古代制度 |
| 02 制度与治理 | [打开](02-制度与治理/README.md) | 权责、监督、政策、法治与社会保障 |
| 03 经济与产业 | [打开](03-经济与产业/README.md) | 增长、产业、财政、分配 |
| 04 宗教与风俗 | [打开](04-宗教与风俗/README.md) | 宗教管理、信俗、名实之辨 |
| 05 社会与人情 | [打开](05-社会与人情/README.md) | 人情、城乡、教育、家庭 |
| 06 思想与学术 | [打开](06-思想与学术/README.md) | 哲学、知识、教育、方法 |
| 07 文论与写作 | [打开](07-文论与写作/README.md) | 古文论辩、文章章法与评点 |
| 08 杂说与辨析 | [打开](08-杂说与辨析/README.md) | 其他部类无法稳妥收纳的短辨 |

**现有已刊作品以 [CATALOG.md](CATALOG.md) 为准。** 该总目根据真实 `status=published` 的文章元数据自动生成；不在本文手工重复一份可能过时的篇名清单。网站另提供 [完整文章目录](https://1998x-stack.github.io/YuHan-articles/articles/) 与检索筛选。

## 一篇一档

~~~text
articles/<一级主题>/<二级子目>/<篇名>/
├── README.md           # 论旨、事实来源和阅读链接
├── article.json        # 标题、日期、状态、主分类与 topics
├── <稿名>.md            # 唯一权威正文
├── <稿名>.docx          # published 时生成
└── <稿名>.pdf           # published 时生成
~~~

文章头行 `# <篇名>` 必须与 `article.json.title` 对应；`article.json.manuscript` 不得包含跨目录路径、绝对路径和软链接。本文只存一个主分类，其他主题由 topics 标签关联，不复制一篇文章到多个栏目。

状态为 draft（草稿）、review（审校）、published（已发表）、archived（归档）。当前网站、目录与出版器**只选 published**。子目目录可能因未来预留而仅含 README，这不代表已有正式文章。

## 分类与权限边界

- [TAXONOMY.md](TAXONOMY.md)：现行归类原则与部类定义。
- [STRUCTURE.md](STRUCTURE.md)：真实的文件系统与数据契约。
- [新增现代文章](../docs/adding-an-article.md)：从草稿、核证到发布。
- [编辑与史料核查](../docs/editorial-standard.md)：事实、引述、因果与文风。
- [版权与许可边界](../docs/rights-and-licenses.md)：现代材料与公有领域原典的不同权利。

历史创建的近义子目会暂时保留，以维护已公开的文档链接和网站 URL。新稿优先选择现存合适子目；迁移前应检查外链和归类逻辑。

## 本地检查与发布

~~~bash
python3 scripts/validate_repository.py
python3 scripts/build_catalog.py
python3 scripts/build_catalog.py --check
python3 scripts/build_articles.py
python3 scripts/validate_repository.py --require-exports
~~~

从仓库根目录执行。DOCX/PDF 是衍生物，不能在修改二进制后使 Markdown 与之不一致。Word/PDF 的中文排印还需人工打开检查；CI 只负责结构与构建验证。细节见 [出版规范](../docs/article-archive-conventions.md)。

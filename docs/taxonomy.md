# 分类规则（维护入口）

> **唯一规范源：** [articles/TAXONOMY.md](../articles/TAXONOMY.md)。本站与归档脚本以 articles/ 下真实存在的分类目录、子目、单篇元数据为准；不要在本文重复维护另一份分类树。

## 归类原则

1. 一级按**文章实际讨论对象**归入固定八大部类，不按“论、辨、说、原、解”等文体词归类。
2. 二级按专题问题域；单篇文章只存放在一个主分类目录下，跨主题联系由 `article.json.topics` 表达。
3. 预留子目用包含收录说明的 `README.md` 保留，不制作虚假作品。
4. 任何迁移都应先核查外部链接、文章引用、相邻子目及相关目录导航；不要仅因名称近似而批量搬动文章。
5. `articles/CATALOG.md` 已改为脚本自动生成，正式文章以 `status=published`、正文文件存在及元数据一致为前提。

## 操作入口

- [现行八部分类与归类边界](../articles/TAXONOMY.md)
- [文章库档案结构](../articles/STRUCTURE.md)
- [新增文章手册](adding-an-article.md)
- [自动生成的文章总目](../articles/CATALOG.md)
- [阅读网站设计规范](website.md)

若现行两份文档对同一归档位置存在不同说法，以 **articles/TAXONOMY.md 和真实 article.json 路径**为准；对无法自动归并的旧子目，保持现状并进行人工审查。

# 新增作品操作手册

## 路径选定

按 [分类规则](taxonomy.md) 确定唯一的一级目录和二级子目。例如：

```text
articles/03-经济与产业/增长与分配/原富民论/
```

## 单篇归档

1. 复制 `articles/_templates/article/` 下模板到选定的篇名目录。
2. 将唯一正文保存为 `篇名.md`，首行写 `# 篇名`。正文与来源/资料依据均写入同一文件。
3. 在 `article.json` 填写 `title`、`manuscript`、`category`、`subcategory`、`date`、`status`、`topics`；字段值必须与目录路径和实际文件对应。
4. 编辑单篇 `README.md`：给出篇旨、研究或事实边界、三格式链接、返回目录。
5. 修改子目与分类索引及 `articles/CATALOG.md`。仅对正式收录的作品列目录项。
6. 运行 `python3 scripts/build_articles.py` 生成同名 DOCX/PDF；或向默认分支提交 Markdown 后，由 `.github/workflows/publish-articles.yml` 自动发布。
7. 发布后检查 Markdown、DOCX、PDF 三者均存在且内容统一；重要的版面问题应通过调整生成脚本和重建修复。

## 命名与版本

- 一级：`01-史论与人物` 等固定编号目录。
- 二级：简明中文问题域；三级：与篇名一致，勿在标题中拼接日期与版本号。
- 题名中文文件：`篇名.md`、`篇名.docx`、`篇名.pdf`；其他元信息写 `article.json`。
- Markdown 为文字唯一事实来源；衍生格式不分头修改。
- 有争议的材料要在正文中保留出处和适当限定，不因文言化将猜测冒充史实。

## 发布核对

- [ ] 所属子目与正文主题匹配，未重复建稿
- [ ] `article.json` 路径、标题、日期、状态有效
- [ ] 正文无空占位、无虚构史料、资料引用可识别
- [ ] 类别、子目、总目录与篇内导读链接可达
- [ ] DOCX、PDF 已实际生成，而非仅有目录中的预期链接

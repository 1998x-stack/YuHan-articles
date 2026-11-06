# 仓库审查与修复记录

**审查日期：2026-11-06。** 本文是针对当前仓库源码、归档与 GitHub Actions 的维护检查，不代表对全部文章史料或每一种浏览器均已完成事实与视觉核验。

## 发现与处置

| 范围 | 发现的问题或风险 | 已采取的处理 | 验证方式 |
| --- | --- | --- | --- |
| 内容维护 | CATALOG.md 长期手工增补，随着新篇连续发布容易漏收或失去一致性 | 新增 scripts/build_catalog.py，以 published 的 article.json 和实际正文生成目录；出版工作流同步更新 | 自动出版脚本运行成功，CATALOG 显示 10 篇真实稿件 |
| 自动出版 | Word/PDF 是二进制，曾在并发更新后发生 Git rebase 冲突，导致 Actions 失败 | 改为每次取最新 main 后重新生成并提交，失败时再取最新状态重试；不对二进制文件 rebase | 修复后的 Publish article formats 工作流成功 |
| Markdown 脚注 | 文章内联用 〔1〕，末尾定义用 [^1]:，生成 HTML 时部分返回链接找不到目标 | 构建 HTML 时把已有数字角标关联至对应 Markdown 脚注定义，不修改原稿 | 站点的链接校验先定位问题，修正后的完整构建成功 |
| 网页发布 | 旧仓库有 Markdown 和 PDF，却缺乏可供普通读者使用的阅读站 | 新建 site/ 模板、CSS/JS、静态生成器、GitHub Pages 自动部署 | Build and deploy reading site 成功完成 build 与 deploy |
| 内容安全 | Markdown 可能包含未经转义的原生 HTML，直接拼接有脚本执行风险 | Python Markdown 转换、Bleach 白名单、Jinja2 元数据自动转义 | 脚本扫描 HTML 输出及站内链接；新增回归测试 |
| URL 与资源 | 中文路径及 GitHub Pages 项目路径容易产生无效跳转 | 统一逐段百分号编码、项目根路径及文件下载路径；生成 sitemap、canonical | scripts/validate_site.py 在 Actions 检查内部链接和图片资源 |
| 字体依赖 | 固定 Linux 中文字体绝对路径在 Windows/macOS/不同容器内不可用 | 已加入可配置 CJK 字体、自动候选与无字库 CID 回退；站点只用 CSS 系统字体栈 | 字体单元测试及出版构建 |
| 文档分类 | articles/TAXONOMY.md、articles/STRUCTURE.md、docs/taxonomy.md 有部分重叠、历史子目名称不一致 | 指定 articles/TAXONOMY.md 为主分类准则，其余为结构或导航说明；保留旧路径以免破坏现有链接 | 检查主分类和文章元数据、明确迁移原则 |

## 仍需关注的边界

- **史料核查是另一项工作**：HTML 构建验证保证页面结构与链接，不等于替每篇文章完成独立历史、法律或时事事实核验。
- **GitHub 仓库体积**：DOCX/PDF 仍作为版本化的二进制文件存放，历史版本会使仓库逐步增大。未来若文章数量显著增长，可评估将导出稿改由 Pages 或 Release Artifact 分发，同时保留 Markdown。
- **旧子目合并**：早期创建的近义子目为避免破坏公开链接暂不强制移动，未来可先核查引用与所有文章主分类后逐步合并；不凭名称相似自动迁移正文。
- **外部引用有效性**：站内链接自动验证，但外部史料网页可能失效；需编辑者定期检查引用并保留出处。
- **主题可视化**：采用浏览器系统字体，跨操作系统字体细节可有差别；正式 PDF 以嵌入可用中文字体为优先。

## 交付与验收命令

~~~bash
python3 -m pip install -r requirements-site.txt
python3 -m unittest discover -s tests -p 'test_site.py'
python3 scripts/build_site.py
python3 scripts/validate_site.py --base-path /YuHan-articles/ --min-articles 1
python3 scripts/build_catalog.py --check
python3 scripts/validate_skills.py
~~~

**部署验证：** [GitHub Pages 工作流](https://github.com/1998x-stack/YuHan-articles/actions/workflows/pages.yml) 与 [文章出版工作流](https://github.com/1998x-stack/YuHan-articles/actions/workflows/publish-articles.yml)。若未来任一自动化失败，按对应运行日志定位，不把曾经通过等同于永久成功。

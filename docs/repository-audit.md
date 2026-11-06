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

## 2026-11-06 后续系统性复审与结构加固

旧表中“10 篇”是**先前某次检查的快照**，不应当作始终准确的仓库总数。当前真实条目以 [CATALOG](../articles/CATALOG.md) 自动生成的数量为准。

| 审查项 | 具体问题 | 本次修复 | 仍需人工确认 |
| --- | --- | --- | --- |
| 文档治理 | 根 README 的旧目录树遗漏原典与网站；AGENTS 对系统形态描述过时 | 重写根文档，新增架构、运维、贡献、编辑、权利及安全指南 | GitHub 上文档链接和实际工作流 |
| 分类漂移 | 历史近义子目共存，手动作品列表可能与自动总目不一致 | 文章库 README 不再复制文章名单；TAXONOMY、STRUCTURE 和新文章说明重新分工 | 合并旧路径前检查公开 URL |
| 资料状态 | Word/PDF 构建器不区分 draft/review/published | 出版器只处理 published；增加标题和正文名一致性检查 | 既有成品的文学及史料质量 |
| 文件路径 | article.json.manuscript 原来允许未经限制的父路径拼接 | 新增纯文件名和库内路径校验，拒绝符号链接及路径穿越 | 不可信贡献的其他安全边界 |
| 站点安全 | resolve 后判断 symlink 导致原始软链接保护无效 | 在清理前检查原始目标，只允许仓库下的 _site；验证链接不逃出构建目录 | 人工审查权限与外部链接 |
| 元数据与文档 | 缺统一的作者、分类、状态、内部链接检查 | 新增 validate_repository.py、单测，并接入 CI | 内容事实、在线外链仍须人工检查 |
| 原典说明 | 《马说》等存在标题通称与原题差异 | 校验兼容篇名的题式差异；现代文章仍严格匹配 H1 | 逐字异文校勘仍须人工完成 |

### 留存风险与长期计划

1. 自动化不能独立核实所有法律、经济、史料数字与外部引用；建议建立逐篇证据复查记录。
2. DOCX/PDF 的 Git 历史膨胀和二进制重复生成仍会占用仓库空间；未来改为 Release/Pages 附件需先设计 URL 兼容。
3. 近义子目合并应先核查历史外链，不应追求命名整齐而破坏地址。
4. 中文字体在不同系统下外观不完全一致；PDF CID 回退不嵌字，需人工检查排印。
5. 如果仓库没有权利人确认的 LICENSE，不应把现代文章与代码默认认为自由再分发；详见 [版权与许可](rights-and-licenses.md)。

### 建议验收

~~~bash
python3 scripts/validate_repository.py
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests -p 'test_repository.py'
python3 scripts/build_catalog.py --check
python3 scripts/build_site.py
python3 scripts/validate_site.py --base-path /YuHan-articles/ --min-classics 5
~~~

以上“修复”最终以实际 GitHub Actions 检查对应提交为准；未执行的人工事实审查不可宣称完成。

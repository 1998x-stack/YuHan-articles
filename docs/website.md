# GitHub Pages 阅读站 · 架构与设计规范

## 目标与约束

网站地址（Pages 启用后）：**https://1998x-stack.github.io/YuHan-articles/**

网站为完全静态的中文论辩阅读站：无需服务器、数据库、JavaScript 框架、外部字体服务或 CDN。现代文章来自 articles/ 的 article.json 和 Markdown；韩愈原典来自 classics/ 的 meta.json 与原文 Markdown；网页是**构建产物**，不能另外手工维护文章副本。

## 信息架构

| 路由 | 功能 |
| --- | --- |
| /YuHan-articles/ | 书页式首页、最新作品、八部主题导航 |
| /YuHan-articles/articles/ | 全部已发表文章、即时搜索与主题筛选 |
| /YuHan-articles/categories/<分类>/ | 八部独立专题页，含空分类状态 |
| /YuHan-articles/read/<分类>/<子目>/<篇名>/ | 单篇深度阅读、关键词、来源、Word/PDF |
| /YuHan-articles/about/ | 写作规范、文集宗旨、事实与引用边界 |
| /YuHan-articles/feed.xml | RSS 2.0 订阅 |
| /YuHan-articles/sitemap.xml | 搜索引擎可识别的站点地图 |

网页路径以百分号编码处理中文目录名，构建器统一添加 Pages 项目子路径，避免页面在多级目录下出现相对链接错误。只有 article.json 中 status 为 published 且 Markdown 确实存在的现代文章才会发布；韩愈原典则按 classics/meta.json 的 status=published 分库发布。未完成的占位目录不会变成空文章页面。

## CSS 设计系统

CSS 在 site/static/assets/style.css，初始九层外另增原典馆层，共分十层：设计令牌、语义与重置、站点导航、首页、目录与分类、长文阅读、Markdown 排印、专题与错误页、响应式与打印。

### 色彩

视觉源于纸张、墨色和朱砂，而非通用企业仪表盘：

| 变量 | 浅色默认 | 用途 |
| --- | --- | --- |
| --paper | #f8f5ef | 整站米白宣纸背景 |
| --sheet | #fffdf8 | 正文卡片的微暖底色 |
| --ink | #252a25 | 高对比度正文墨色 |
| --muted | #676f68 | 辅助文字 |
| --accent | #9b4c38 | 朱砂点题、交互与关键状态 |
| --olive | #607260 | 标签与静态分类标识 |
| --border | #ddd9ce | 纸页分割线 |

完整令牌还包括字号族、间距、圆角、阴影与过渡。深色模式使用独立的背景与文字变量，遵守系统偏好，并允许用户手动切换。

### 字体和阅读

- 文章正文使用 Source Han Serif / Noto Serif CJK / Songti / SimSun 等**本机衬线字体栈**；不用远程下载字体，也不提交第三方字体文件。
- UI、目录、按钮使用系统无衬线字体；题名与核心引文以宋体氛围呈现。
- 正文桌面约 17–19 px、行高约 2.05，阅读列最大 745 px；分段首行缩进两字，移动端减少缩进强度并调整行高。
- HTML 从 Markdown 生成，保留标题、强调、表格、代码、引文、脚注、链接。配套 CSS 为 footnotes、可滚动表格、打印 A4 提供专用规则。
- 桌面采用“左侧主题索引 — 中间正文 — 右侧目录/进度”三栏；平板取消右侧；窄屏仅保留主阅读列。

### 组件

统一组件包括 Brand 标识、主导航、按钮、专题卡片、文章卡片、搜索及筛选、面包屑、元信息、关键词、Word/PDF 资源链接、章节导航、前后篇导航、页脚。

不采用图库水印、侵权图片或外部字体资源；首页以纯 CSS 的书页构图和字符装饰建立视觉识别。

### 可访问性与隐私

- 主地标、跳到正文链接、键盘可见焦点、ARIA 当前页与搜索状态；
- 语义化标题层级与隐藏/空状态；无 JavaScript 时仍可阅读全文；
- 尊重 prefers-reduced-motion、prefers-color-scheme，提供手动浅色/深色切换与打印版；
- 默认**无追踪、无广告、无第三方脚本**。主题偏好只存储在浏览器本机 localStorage。

## Markdown 与安全

scripts/build_site.py 使用 Python Markdown（extra、toc、footnotes）将正文变为 HTML，再由 Bleach 白名单过滤可执行标签、事件属性及不安全 URL 协议；Jinja2 对元数据默认 HTML 转义。避免从用户可编辑的文章中注入脚本。正文 Markdown 是权威来源，不把 HTML 回写到 articles/。

公开文章下载由当前 Markdown 构建对应 Word/PDF，再随 Pages 产物上传，即使另一条出版工作流尚未提交二进制，也不会生成不真实的下载链接。构建器生成 sitemap.xml、RSS 与阅读页 canonical/OG 元信息。

## 本地预览

在仓库根目录执行：

~~~bash
python3 -m pip install -r requirements-site.txt
python3 -m pip install python-docx reportlab
python3 scripts/build_articles.py            # 可选：重建可下载排印版
python3 scripts/build_site.py
python3 scripts/validate_site.py --min-articles 1 --min-classics 5
python3 -m http.server 8000 --directory _site
~~~

浏览 http://localhost:8000/ 时，默认项目 URL 为 /YuHan-articles/，因此应在构建时改用 --site-url http://localhost:8000/ 或把 _site 挂载在 /YuHan-articles/ 目录。推荐本地命令：

~~~bash
python3 scripts/build_site.py --site-url http://localhost:8000/
python3 scripts/validate_site.py --base-path / --min-articles 1 --min-classics 5
python3 -m http.server 8000 --directory _site
~~~

不要提交 _site/；站点由 GitHub Actions 每次重新生成。

## GitHub Pages 发布

1. 打开仓库 **Settings → Pages → Build and deployment → Source**，选择 **GitHub Actions**。这是仓库首次部署时可能必需的一次性设置；默认 GITHUB_TOKEN **不能保证**自动开通 Pages。
2. 向 main 提交网页文件或文章 Markdown，会触发 .github/workflows/pages.yml；也可在 Actions 手动运行 Build and deploy reading site。
3. 工作流从原始 Markdown 构建 Word/PDF、HTML 页面及站点图，对站内链接进行校验，再通过 actions/upload-pages-artifact 与 actions/deploy-pages 发布。
4. 查看运行记录中的 deploy 结果及 GitHub Pages 的 Visit site。若仅 build 成功而 deploy 失败，先检查 Pages 是否已启用且 Source 为 GitHub Actions。

若未来更换域名，须同步更新 Pages 设置与构建参数 --site-url，使 canonical、资源路径与站点地图一致。

## 故障诊断

- 404：检查 Pages 是否开启、是否完成 deploy，以及链接是否带 /YuHan-articles/ 项目子路径。
- PDF 字体：见 docs/fonts.md；网站 HTML 使用浏览器系统字体。
- 分类未显示文章：检查 article.json 的 status=published、分类路径与 manuscript。
- 字体、分页或脚注：统一修改 CSS 或 Markdown 原稿，而不是手工编辑生成 HTML。
- 构建失败：根据工作流 validate_site 输出定位断开的资源路径或 Markdown 输出中的不安全标签。

## 韩愈原典馆

原典馆新增 `/YuHan-articles/classics/` 与五篇 `/classics/<slug>/` 阅读页；网页从 `classics/` 的 `meta.json` 与完整 Markdown 原文自动生成，不需要复制粘贴到 HTML 模板。原典馆不改变 `articles/` 的现代改写稿数量。主导航、首页选读及网站地图均包括这五篇。编辑规范见 [古文版本校阅](classic-editions.md)。

Pages 发布时要求 `python3 -m unittest discover -s tests -p 'test_classics.py'` 和 `python3 scripts/validate_site.py --min-classics 5` 同时成功。

## 当前架构与维护约定

- **主数据源**：现代作品由 articles/ 生成，韩愈原作由 classics/ 生成，网页不是第三份待人工编辑的正文。
- **生成入口**：执行 `python3 scripts/validate_repository.py` 后再运行 `python3 scripts/build_site.py`，避免在元数据冲突时发表错误作者或路径。
- **构建输出保护**：脚本只允许清理实际仓库根目录下的 `_site/`，禁止用软链接或任意输出目录绕过限制；临时预览请使用标准 _site。
- **测试与文档**：[架构说明](architecture.md) · [运行维护](maintainer-runbook.md) · [编辑规范](editorial-standard.md) · [权利政策](rights-and-licenses.md)。

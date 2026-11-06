# 静态阅读站 · Site

本目录存放展示层模板与静态资源；**不存放文章正文**。页面由 scripts/build_site.py 根据 articles/ 中已发表的 article.json + Markdown，以及 classics/ 中的 meta.json + 原典 Markdown 分库生成。

- templates/base.html：全站语义骨架、主导航、元信息与页脚
- templates/home.html：主页导览与精选作品
- templates/archive.html：文章检索及筛选
- templates/category.html：八部主题专题页
- templates/article.html：正文阅读与下载
- templates/about.html：写作原则与来源声明
- static/assets/style.css：设计变量、组件体系、阅读排版、响应式与打印样式
- static/assets/site.js：主题偏好、站内检索、阅读进度

原则：不引用 CDN、外部字体或追踪脚本；无 JavaScript 仍可浏览文章。构建器会对 Markdown 生成的 HTML 进行白名单清理。详情见 docs/website.md。

## 韩愈原典

`classics/` 与 `articles/` 两种内容独立显示：前者属于韩愈本人公有领域古文，后者属于当代按韩愈文风创作的论说。网页入口 `/classics/`，逐篇路径 `/classics/<slug>/`，五篇源码另有明确的来源和版本记录。详情：[原典编纂说明](../docs/classic-editions.md)。

## 文档与构建

[网站架构](../docs/architecture.md) · [详细 CSS 与排印](../docs/website.md) · [维护运行手册](../docs/maintainer-runbook.md)。修改页面或静态资源时运行 `python3 scripts/validate_repository.py`、网站单元测试、build_site 与 validate_site；不要在模板中直接粘贴文章正文。

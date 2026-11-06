# 仓库架构设计 · Architecture

## 一、边界与系统目标

YuHan Articles 将四个职责分开：**文本权威源、写作方法、静态出版、网站展示**。没有独立 Web 后端、账户数据库或内容管理服务。Python 脚本在本机/CI 运行，GitHub Pages 只托管构建后的静态资产。

根级 [README](../README.md) 面向用户；[AGENTS](../AGENTS.md) 约束自动化；此文说明系统组织，不是另一套分类规则。

## 二、数据流

~~~text
             人工写作 / AI 辅助（事实与审校仍由人负责）
                                │
                ┌───────────────┴─────────────────┐
                │                                 │
       articles/<分类>/<子目>/<篇>/         classics/<slug>/
       article.json + 正文.md               meta.json + 原文.md
                │                                 │
                └──────────┬──────────────────────┘
                           ▼
                 scripts/validate_repository.py
                           │
     ┌─────────────────────┴───────────────────────┐
     │                                             │
现代已刊 Markdown                              现代已刊 + 韩愈原典
     │                                             │
     ├─ build_catalog.py ─── articles/CATALOG.md     │
     ├─ build_articles.py ── DOCX / PDF              │
     │                                             ▼
     └─────────────────────────────── build_site.py
                                              │
                                         HTML / JSON
                                         CSS / JS / SVG
                                         sitemap / RSS
                                              │
                                        validate_site.py
                                              │
                                       GitHub Pages
~~~

**正文只有一个权威版本。** 现代文章以 Markdown 为权威，Word、PDF 和 HTML 是衍生物；原典以 classics 的 Markdown 为权威，版本记录单独保存；搜索与网站目录由元数据自动生成。

## 三、目录与文件契约

### articles/

路径 `articles/<category>/<subcategory>/<work>/article.json`。article.json 至少要求：

~~~json
{
  "title": "篇名",
  "manuscript": "篇名.md",
  "category": "02-制度与治理",
  "subcategory": "公共治理",
  "date": "2026-11-06",
  "status": "published",
  "topics": ["制度", "论辩"]
}
~~~

- `category` 和 `subcategory` 必须与路径对应。
- `manuscript` 必须是本目录存在的安全 Markdown 纯文件名。
- `title` 与第一行 `# 篇名` 一致。
- `date` 为 ISO 日期；`topics` 为字符串数组。
- `status` 可用 draft/review/published/archived，**当前正式出版仅选 published**。
- 只归一个主类；不为标签建立重复正文。真实分类依据 [TAXONOMY](../articles/TAXONOMY.md)。

### classics/

`classics/<slug>/meta.json` 记录 title、slug、author、dynasty、genre、order、status、manuscript、source_url 与 source_label。作者和朝代须为韩愈／唐；Markdown 保留原文，README 保存参校依据及现代编辑记录。参阅 [原典版本](classic-editions.md)。

### prompts/ 与 Skills

`prompts/han-yu-master-prompt.md` 是完整写作规范，quick-prompt 供快速使用；OpenCode 与 Pi 分别位于两个约定的 SKILL.md 路径，要求字节一致。

## 四、构建流程

| 脚本 | 输入 | 输出 | 特别边界 |
| --- | --- | --- | --- |
| `validate_repository.py` | 分类、文章/原典元数据、文档链接 | 错误和统计 | 无第三方依赖、只读 |
| `build_catalog.py` | 已刊 article.json + 实际 Markdown | articles/CATALOG.md | 不包含草稿 |
| `build_articles.py` | 已刊 article.json + Markdown | 同名 DOCX/PDF | 路径限制、字体回退 |
| `build_site.py` | 已刊文章 + 原典 + site 模板 | _site/ 静态文件 | Markdown 清洗、编码 URL |
| `validate_site.py` | _site/ | 站内文件/片段等检查 | GitHub Pages 子路径 |
| `validate_skills.py` | 双端 Skills + Prompt | 结构校验 | 两份 Skill 同步 |

自动化工作流：
- **publish-articles.yml**：在最新 main 基础上重建 DOCX/PDF 和 CATALOG，避免二进制 rebase 冲突；
- **pages.yml**：单元测试、重建可下载格式、静态站生成、链接验收、Pages 部署；
- **validate-skills.yml**：Prompt、Skill 与仓库结构、文档链接检查。

工作流运行结果需对应**具体的 Git SHA**；CI 通过不等于事实和文学审校通过。参考 [运维手册](maintainer-runbook.md)。

## 五、安全与可靠性

**输入边界：** 各种 JSON 与 Markdown 都可能来自贡献者，不能假定可信。article.json 的 `manuscript` 不能有相对穿越或库外软链接；原典 meta.json 同理。网站将 Markdown 转为 HTML 后通过 Bleach 白名单清洗，再通过开启自动转义的 Jinja2 模板渲染。为避免本地误删，站点清理目录限定为仓库根目录下的 `_site/`。

**输出边界：** Word/PDF 文件默认存储在文章目录并随 Git 版本管理。长期会增加仓库体积，未来可改成 Pages/Release 下载但需兼顾链接兼容；此迁移不是本次默认操作。

**字体边界：** 站点使用浏览器本机中文字体；PDF 采用 ReportLab 兼容 TrueType，若无可嵌入字体则尝试 STSong-Light CID（不嵌入），不应直接打包来源不明字体。详见 [字体](fonts.md)。

**权限边界：** 静态网站读取文件，不需要凭据或第三方脚本；GitHub Actions 只在需要推送生成件的出版工作流使用写仓库权限；Pages 部署权限应限制在部署任务的必要范围。安全报告说明见 [SECURITY](../SECURITY.md)。

## 六、设计与可访问性

`site/static/assets/style.css` 为设计令牌与排印层，依次实现纸墨朱砂色彩、正文衬线、段落行距、书页卡片、响应式布局、黑暗主题、键盘焦点和打印。Jinja2 模板保证结构可复用，不在每篇 HTML 复制 CSS 或正文。设计说明参阅 [网站手册](website.md)。

## 七、维护禁止项

不得把 `_site/` 提交为正文、手改 CATALOG 后不回写元数据、将原典署名用于 AI 创作、无依据迁移既有 URL，或在尚未查看 GitHub Actions 实际结果时宣称发布完成。文档协同与故障恢复见 [AGENTS](../AGENTS.md) 和 [运行手册](maintainer-runbook.md)。

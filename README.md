# YuHan Articles · 韩愈式古文论辩与原典阅读

> **以文明理，以论驭辞。** 以韩愈文章之法重构现代议论，同时保存韩愈本人的古文原作供研究与阅读。

[![Pages](https://github.com/1998x-stack/YuHan-articles/actions/workflows/pages.yml/badge.svg)](https://github.com/1998x-stack/YuHan-articles/actions/workflows/pages.yml)
[![Skills](https://github.com/1998x-stack/YuHan-articles/actions/workflows/validate-skills.yml/badge.svg)](https://github.com/1998x-stack/YuHan-articles/actions/workflows/validate-skills.yml)
[![Exports](https://github.com/1998x-stack/YuHan-articles/actions/workflows/publish-articles.yml/badge.svg)](https://github.com/1998x-stack/YuHan-articles/actions/workflows/publish-articles.yml)

**在线阅读**：[网站首页](https://1998x-stack.github.io/YuHan-articles/) · [现代论说](https://1998x-stack.github.io/YuHan-articles/articles/) · [韩愈五篇原典](https://1998x-stack.github.io/YuHan-articles/classics/)

本项目兼具 **韩愈式写作 Prompt、OpenCode/Pi Agent Skills、现代古文文章库、原典校阅库和 GitHub Pages 静态阅读网站**。不是“将白话逐字换成文言”的翻译器；先求论证有据、义理明切，再求语言雄健。

## 按需要选择入口

| 目的 | 入口 |
| --- | --- |
| 阅读已发表文章 | [GitHub Pages](https://1998x-stack.github.io/YuHan-articles/) / [文章总目](articles/CATALOG.md) |
| 学习韩愈五篇真作 | [原典馆](classics/README.md) / [版本原则](docs/classic-editions.md) |
| 直接改写现代文章 | [完整版 Prompt](prompts/han-yu-master-prompt.md) / [快速 Prompt](prompts/han-yu-quick-prompt.md) |
| 在编码助手中调用 | [OpenCode Skill](.opencode/skills/han-yu-argumentation/SKILL.md) / [Pi Skill](.pi/skills/han-yu-argumentation/SKILL.md) |
| 新建和审校文章 | [新增文章指南](docs/adding-an-article.md) / [编辑标准](docs/editorial-standard.md) |
| 开发与维护仓库 | [CONTRIBUTING](CONTRIBUTING.md) / [架构](docs/architecture.md) / [运维手册](docs/maintainer-runbook.md) |
| 了解权限与限制 | [SECURITY](SECURITY.md) / [权利及许可边界](docs/rights-and-licenses.md) |

## 两套作品、两种作者归属

### 现代古文论说：articles/

以**八大主题 → 二级子目 → 单篇目录**编排：史论与人物、制度与治理、经济与产业、宗教与风俗、社会与人情、思想与学术、文论与写作、杂说与辨析。

每篇以 Markdown 作为**唯一正文权威源**，由同目录 `article.json` 管理题名、主分类、日期、状态和 `topics` 标签；DOCX/PDF 和 HTML 都由源稿生成。仅 `published` 进入正式目录，`draft` 与 `review` 不冒充已刊作品。

- [文章总目录](articles/CATALOG.md)：由脚本根据实际的已刊文章生成，**不要手动编辑**。
- [分类与归档准则](articles/TAXONOMY.md)：唯一主分类，交叉主题用标签。
- [文章库入口](articles/README.md) 与 [结构说明](articles/STRUCTURE.md)。

### 唐代韩愈原作：classics/

原典与现代仿韩文**严格分库，且不得混淆署名**。首批《师说》《马说》（《杂说四》）《进学解》《原道》《祭十二郎文》，五篇兼顾知名度与文体代表性，**并非所谓公认“前五排名”**。每篇有 `meta.json`、完整原文 Markdown 和逐篇的参校/异文 README；现代标点整理不等于古籍定本。

## 核心写作方法

| 方法 | 思想作用 |
| --- | --- |
| 推原究本 | 由表象探求人情、利害、制度和因果 |
| 反俗立论 | 提出通说，再检验其前提与矛盾 |
| 设难诘问 | 先公平构建强异议，再逐层检验 |
| 辨名核实 | 分清公开宣称、实际行为、效果和利益 |
| 据事明理 | 保留人物、史事、数字、出处及不确定性 |
| 正反互证 | 以同一标准检验正反两种情况 |
| 蓄势断案 | 由疑入辨，结论必须由事实与推论支持 |

追求**义明、理密、辨深、辞健、法活、气贯、意远**，而非单纯堆砌“夫、盖、然则”。原文无证据者不补造；人物获利不等于动机已获证实；不强行移植古人宗教或政治主张。详见 [方法与证据](docs/method-and-evidence.md) 和 [质量量表](docs/quality-rubric.md)。

## 快速使用 Prompt 与 Skills

直接将自己的文章粘贴到 [完整版写作 Prompt](prompts/han-yu-master-prompt.md) 的【待改写原文】位置。默认只需返回篇名和完整古文正文；如需校勘、评述、事实核查或 PDF/DOCX，请明确提出。

两端 Skill 路径：

~~~text
.opencode/skills/han-yu-argumentation/SKILL.md
.pi/skills/han-yu-argumentation/SKILL.md
~~~

在相应工具的项目会话中请求使用 `han-yu-argumentation`。Pi 的部分版本可使用 `/skill:han-yu-argumentation`，具体以已安装版本的 Skill 命令和目录约定为准。两份 Skill 内容应保持**字节级一致**。

## 目录与系统组成

~~~text
.
├── README.md                       # 面向读者、贡献者的总入口
├── AGENTS.md                       # AI Agent 任务与维护规范
├── CONTRIBUTING.md                 # 贡献与变更指引
├── SECURITY.md                     # 安全报告边界
├── articles/                       # 现代文章，八大部类
│   ├── CATALOG.md                  # 自动生成的总目
│   ├── TAXONOMY.md                 # 归类权威依据
│   └── <分类>/<子目>/<篇名>/
│       ├── article.json
│       ├── README.md
│       └── <篇名>.md / .docx / .pdf
├── classics/                       # 韩愈五篇原典
│   └── <slug>/meta.json + 原典.md + README.md
├── prompts/                        # 完整与精简 Prompt
├── .opencode/skills/               # OpenCode Agent Skill
├── .pi/skills/                     # Pi Agent Skill
├── site/
│   ├── templates/                  # Jinja2 网页模板
│   └── static/assets/              # CSS、JS 与 SVG
├── scripts/
│   ├── validate_repository.py      # 目录、元数据、文档链接校验
│   ├── validate_skills.py          # 两端 Skill 同步校验
│   ├── build_catalog.py            # 文章总目
│   ├── build_articles.py           # Markdown → DOCX / PDF
│   ├── build_site.py               # Markdown → HTML
│   └── validate_site.py            # 网站输出与站内链接校验
├── tests/                          # unittest
└── .github/workflows/             # 自动出版、站点部署、结构校验
~~~

## 本地开发与网站预览

建议 Python **3.12**。在仓库根目录：

~~~bash
python3 -m venv .venv
source .venv/bin/activate           # PowerShell: .venv\Scripts\Activate.ps1
python3 -m pip install -r requirements-site.txt
python3 -m pip install python-docx reportlab

# 检查结构、原典、Prompt 与已刊总目
python3 scripts/validate_repository.py
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests -p 'test_repository.py'
python3 -m unittest discover -s tests -p 'test_classics.py'
python3 -m unittest discover -s tests -p 'test_site.py'
python3 -m unittest discover -s tests -p 'test_fonts.py'
python3 scripts/build_catalog.py --check

# 生成 Word/PDF，验证真实导出
python3 scripts/build_articles.py
python3 scripts/validate_repository.py --require-exports

# 本地 HTTP 预览：覆盖线上 Pages 项目子路径
python3 scripts/build_site.py --site-url http://localhost:8000/
python3 scripts/validate_site.py --base-path / --min-articles 1 --min-classics 5
python3 -m http.server 8000 --directory _site
~~~

打开 http://localhost:8000/ 。`_site/` 属于忽略提交的生成目录，切勿当作正文权威源。PDF 字体不足时可能回退到非嵌入 CID；正式分发见 [字体说明](docs/fonts.md)。

## 发布和 CI

| 工作流 | 目的 |
| --- | --- |
| [Validate Han Yu Agent Skills](https://github.com/1998x-stack/YuHan-articles/actions/workflows/validate-skills.yml) | 校验 Prompt、Skill 一致性、目录和文档链接 |
| [Publish article formats](https://github.com/1998x-stack/YuHan-articles/actions/workflows/publish-articles.yml) | 从最新已刊 Markdown 生成 PDF/DOCX 与文章总目 |
| [Build and deploy reading site](https://github.com/1998x-stack/YuHan-articles/actions/workflows/pages.yml) | 测试、构建静态中文阅读站并部署 Pages |

网页支持文章全文排印、分类筛选、原典馆、脚注、RSS、站点地图、深浅色和手机阅读，使用本机字体，不依赖在线数据库。CSS 设计规范见 [docs/website.md](docs/website.md)。

**CI 通过仅证明自动化检查成功，不等于所有史料、社会数字或外部引用已做独立事实核查。** Pages 上线需以 deploy 成功及真实页面可访问为准；参见 [维护手册](docs/maintainer-runbook.md)。

## 文档体系与权利边界

- [AGENTS.md](AGENTS.md)：AI Agent 工作规约与验证矩阵。
- [CONTRIBUTING.md](CONTRIBUTING.md)：贡献与人工审稿流程。
- [docs/architecture.md](docs/architecture.md)：项目模块、数据流与安全。
- [docs/editorial-standard.md](docs/editorial-standard.md)：史料、因果、文言、版本和质量门槛。
- [docs/maintainer-runbook.md](docs/maintainer-runbook.md)：构建、部署、恢复与排障。
- [docs/repository-audit.md](docs/repository-audit.md)：查出的问题、修复记录和剩余风险。
- [docs/rights-and-licenses.md](docs/rights-and-licenses.md)：公有领域原典、现代稿件、字体和许可证的区别。

公开仓库不当然表示所有文件均可无限制再分发。如果仓库尚无明确的根级 `LICENSE`，不能将其默认视为采用某种开源许可证。史料核查和版权归属须独立进行。

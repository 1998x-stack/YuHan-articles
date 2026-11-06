# AGENTS.md · YuHan Articles Agent 工作规范

> 面向在本仓库执行任务的 AI 编程代理、文章写作代理和自动化工具。此文件是**项目执行规范**：须以实际仓库为准，保持原典与现代改写分离，不伪造原文、来源、核验、测试或部署结果。

## 1. 使命、边界与优先级

YuHan Articles 不只是 Prompt 仓库，现有模块包括：

- 现代文章库 `articles/`：韩愈式论辩改写与现代原创，基于客观来源写作。
- 原典库 `classics/`：韩愈本人公有领域作品的简体标点整理，附版本与参校材料。
- 写作规范 `prompts/`、`.opencode/skills/`、`.pi/skills/`。
- 静态阅读站 `site/` 与 `scripts/build_site.py`，由 GitHub Pages 发布。
- 文档出版器 `scripts/build_articles.py`、文章目录生成器 `scripts/build_catalog.py`、校验器与 CI。

**处理顺序：真实与作者归属 > 原文保真及证据 > 安全和版本兼容 > 论证质量 > 文气修辞 > 装饰形式。**

仓库里的旧命令、日期、目录枚举可能已经过时。每次修改前先看 `git status`（有可用本地仓库时）、最新 `main`、目标文件和 CI，不凭历史对话推定文件内容。

## 2. 任务分流与规范源

| 任务类型 | 主入口 | 必要输出 |
| --- | --- | --- |
| 文言改写 | [master-prompt](prompts/han-yu-master-prompt.md)、[编辑规范](docs/editorial-standard.md) | 篇名与完整古文，事实和论旨不变 |
| Prompt/Skill | `prompts/` 与两个 `SKILL.md` | 双端字节一致，内容自包含 |
| 新文章/分类 | [TAXONOMY](articles/TAXONOMY.md)、[新增文章](docs/adding-an-article.md) | article.json、Markdown、README，必要导出 |
| 韩愈原典 | `classics/`、[版本规范](docs/classic-editions.md) | 真正的古人文字与可追溯参校记录 |
| HTML/设计 | `site/`、[网站规范](docs/website.md) | 响应式可阅读站点、站内链接通过 |
| DOCX/PDF | `scripts/build_articles.py`、[字体规则](docs/fonts.md) | 与 Markdown 对应的排印文件 |
| CI、安全与维护 | `.github/workflows/`、[运行手册](docs/maintainer-runbook.md) | 可重现修复、实际运行记录 |

### 单一权威来源

- **现代文章正文**：`articles/<大类>/<子目>/<篇名>/<稿名>.md`。`.docx/.pdf` 与网页 HTML 只能从这份文本生成。
- **现代文章元数据**：同目录 `article.json`，已发表文章总目 `articles/CATALOG.md` 是**生成件**。
- **原典正文与来源**：`classics/<slug>/<原典名>.md` 和对应 `meta.json`；`README.md` 记录版本、异文及出处。
- **分类规范**：`articles/TAXONOMY.md`；`articles/STRUCTURE.md` 与 `docs/taxonomy.md` 只负责说明、导航和迁移。
- **写作法**：`prompts/han-yu-master-prompt.md` 优先，精简版与两端 Skills 不得与其抵触。
- **网页样式**：`site/static/assets/style.css`；模板是展示层，不能复制存储原文。

不要在多个规范中手工维护另一份固定“正式文章数量”、二级子目总数或历史排名。修改规范源后，检查索引、示例和关联文档有无失效。

## 3. 韩愈式写作约束

### 3.1 完整论辩流程

1. **审题**：用一句话界定核心疑问，不仅复述现象。
2. **据事**：保留原文关键人物、事件、数据、引文、因果与限定条件；区分**史实、转述、推断、假设、评价**。
3. **定论势**：识别主流解释，推原究本，选出反对方最强的理由。
4. **设难破惑**：采用正反互证、条件推演、名实对照，反诘须每句推动结论。
5. **行文**：散体为本，骈偶辅助；句长变化、虚词各有逻辑作用；语言古奥而可通读。
6. **复审**：义明、理密、辨深、辞健、法活、气贯、意远；篇末断案回扣篇首。
7. **交付**：普通改写任务默认只输出简雅篇名与文言正文；用户明确要资料、解释或文件时依请求办理。

### 3.2 事实与伦理硬约束

- 不编造韩愈原话、史书正文、古人对话、统计数字、法条、制度细节及作者动机。
- 不以有人获利推定其必然欺诈，不把一例写成普遍规律，不因文气雄健而扩大结论。
- 史载与作者推断、现代报道与访谈转述、真实对话与拟设问答须有可辨标记。
- 不把一切现代议题强行归于儒家道统，也不必赞同韩愈在《原道》等篇中的时代观点。
- 原文未给足材料而用户明确要求事实核查时，应寻证；核验未完成须保留不确定性，不要虚报“已校证”。
- 他人受版权保护的现代原文不可未经许可全文搬运至仓库；遵守合理引用边界。
- 编辑要求见 [docs/editorial-standard.md](docs/editorial-standard.md) 与 [docs/method-and-evidence.md](docs/method-and-evidence.md)。

## 4. 现代文章目录与状态

标准：

~~~text
articles/<编号-主题>/<子目>/<篇名>/
├── README.md
├── article.json
├── <稿名>.md            # 第一行必须是 '# <title>'
├── <稿名>.docx          # 发表后生成
└── <稿名>.pdf           # 发表后生成
~~~

元数据示例（`category`/`subcategory` 必须与真实目录严格相同）：

~~~json
{
  "title": "示例辨",
  "manuscript": "示例辨.md",
  "category": "02-制度与治理",
  "subcategory": "公共治理",
  "date": "2026-11-06",
  "status": "draft",
  "topics": ["制度", "名实"]
}
~~~

**状态规则**：`draft` 草稿；`review` 审校中；`published` 已正式发布；`archived` 已归档。当前生成器以 `status=published` 为正式出版条件。目录占位和未发表的文章不能被自动加入“已刊”索引或导出。

`manuscript` 必须是当前目录内纯文件名（不得有斜线、反斜线、绝对路径或路径穿越）。题名需与正文首行 Markdown H1 一致；`date` 使用 YYYY-MM-DD，`topics` 为字符串数组。只允许一个主分类，跨主题用 topics，不复制同一篇正文到另一部类。空子目须有说明性 README，不凭空创建假文章。

新篇入库前：

~~~bash
python3 scripts/validate_repository.py
python3 scripts/build_catalog.py
python3 scripts/build_catalog.py --check
# 仅在准备正式发表时生成导出：
python3 scripts/build_articles.py
python3 scripts/validate_repository.py --require-exports
~~~

谨慎迁移旧目录：先检查外部链接、当前 Pages URL 与任何 README 引用，再决定是否需要兼容重定向；不要仅因两个子目名称相似就移动全部历史稿件。

## 5. 韩愈本人原作与校勘

`classics/` 只能存放韩愈真实作品，**不能把现代仿韩文或 AI 补写署名“韩愈”**。原典项目结构：

~~~text
classics/<slug>/
├── meta.json          # 标题、作者、朝代、文体、出处、顺序与正文名
├── <原典名>.md         # 古文原作（简体标点整理）
└── README.md          # 底本、版本说明与异文记录
~~~

`meta.json.author` 固定为“韩愈”，`dynasty` 为“唐”；每篇 `slug` 唯一，`order` 为互不重复的正整数。原题和通称可以不同（如《马说》与《杂说四》），在元数据与版本说明中注明，而非未经查核强行改题。古文内容改动须有可复核的底本与逐条校记。

`classics/` 与 `articles/` 分别显示在网站原典馆和现代文章馆；原典馆选目不代表所谓权威前五排名。自动测试只保证结构存在，**不能替代古籍版本逐字校勘**。

## 6. Prompt 与双端 Agent Skills

两份 Skill：

~~~text
.opencode/skills/han-yu-argumentation/SKILL.md
.pi/skills/han-yu-argumentation/SKILL.md
~~~

须**字节级一致**。frontmatter 包含 `name: han-yu-argumentation` 与 description；Skill 内容应自包含，仓库内相对链接仅用于选读深化。不得将核心事实边界或伦理要求从精简版删掉。

更新 Prompt/Skills 时运行：

~~~bash
python3 scripts/validate_skills.py
~~~

并人工检查说明与示例是否体现“推原究本、据事明理、设难诘问”，而非堆叠文言虚词。

## 7. Python、路径安全与静态网站

### Python / 元数据

- 目标运行时 Python 3.12，`requirements-site.txt` 声明 Jinja2、Markdown、Bleach；排印额外依赖 `python-docx` 与 `reportlab`。
- JSON 元数据视为不受信任输入，先核验类型、状态、相对路径和文件名，**不能跟随 symlink 把库外文件读成文章**。
- 构建输出 `_site/` 必须是本仓库根目录的目标路径，不允许删除任意绝对路径或跟随目录软链接。
- 不提交私密密钥、访问令牌、未授权素材及来源不明的中文字体二进制。
- Word/PDF 从 Markdown 统一重建；PDF 非嵌入 CID 字体回退仅是兼容兜底，不保证所有阅读器显示相同。

### 网页 / CSS

- `site/templates/` 是 Jinja2 语义模板，`site/static/assets/style.css` 是视觉变量、响应式、中文排印与打印体系的唯一位置。
- 页面的文章与原典来自 Markdown，渲染后经 Bleach 许可标签和属性过滤；元数据通过 Jinja2 默认转义。任何 `|safe` 的输入必须有明确的白名单来源。
- GitHub Pages 项目路径包含 `/YuHan-articles/`；中英文混合目录应逐段 URL 编码。更换域名须同步构建参数与站点检查。
- 保持无 JS 时仍可阅读全文、键盘焦点可见、HTML 层级语义正确、手机端可读、支持深浅色及 A4 打印。
- 不添加无必要的外部追踪脚本、第三方字体、侵权图片或高风险动态 HTML。

## 8. 测试矩阵

| 变更范围 | 必做检查 |
| --- | --- |
| 任何元数据/文档 | `python3 scripts/validate_repository.py` |
| Prompt/Skill | `python3 scripts/validate_skills.py` |
| 分类与文章 | `python3 scripts/build_catalog.py --check` |
| 原典 | `python3 -m unittest discover -s tests -p 'test_classics.py'` |
| 仓库路径和安全 | `python3 -m unittest discover -s tests -p 'test_repository.py'` |
| 模板/CSS/构站 | `python3 -m unittest discover -s tests -p 'test_site.py'`，生成后运行 `scripts/validate_site.py` |
| 排印与字体 | `python3 -m unittest discover -s tests -p 'test_fonts.py'`，再运行出版器及 `--require-exports` |
| GitHub Pages | Pages 工作流的 **build 与 deploy 均为 success**；公开网址实际可用 |

完整本地命令：

~~~bash
python3 -m pip install -r requirements-site.txt
python3 -m pip install python-docx reportlab
python3 scripts/validate_repository.py
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests -p 'test_repository.py'
python3 -m unittest discover -s tests -p 'test_classics.py'
python3 -m unittest discover -s tests -p 'test_site.py'
python3 -m unittest discover -s tests -p 'test_fonts.py'
python3 scripts/build_catalog.py --check
python3 scripts/build_articles.py
python3 scripts/validate_repository.py --require-exports
python3 scripts/build_site.py
python3 scripts/validate_site.py --base-path /YuHan-articles/ --min-classics 5
~~~

测试通过≠文学作品已完成事实审校；文件存在≠PDF 的版式和中文字体均正确，正式发布需人工抽查实际产物。

## 9. Git、CI 与并发写入

- 每次写入前重新读取 `main`、受影响文件与 CI；不要以先前对话的仓库树作为当前事实。
- 如分支在操作期间推进，**禁止强制推送覆盖他人更改**。只将本次变更追加到新的树，使用预期 SHA 的安全更新。
- 出版工作流需要在最新 Markdown 上重新生成 DOCX/PDF，不能 Git rebase 二进制文件解决冲突。
- `articles/CATALOG.md` 是生成文件，`_site/` 是忽略文件；不得仅为让 CI 绿色而删除测试、放宽安全检查或隐藏真实失败。
- CI 触发依据路径过滤；更新 docs 不一定部署 Pages，必须检查具体 workflow run 及 commit SHA。
- 产出必须说明修复内容、实际验证结果、未解决风险、GitHub commit/CI 链接；**不得预称尚未完成的工具调用和部署已成功**。

## 10. 文档管理与交付标准

README 面向新读者；本文件约束 AI Agent；`docs/architecture.md` 解释设计；`docs/maintainer-runbook.md` 指导操作；`docs/editorial-standard.md` 指导内容审校；`docs/rights-and-licenses.md` 说明权利边界。分类正文以 `articles/TAXONOMY.md` 为准，其他导航不可暗中另立一份标准。

最终提交前检查：真正改动了哪个权威源？旧 URL 是否仍通？文章与作者归属无误？测试覆盖了新增情况？文档命令可运行？是否有来源不明的权利材料？自动化结果是否对应本次提交？

当任务受限无法完成时，应准确区分**已提交、已构建、已部署、未验证**四类状态，不以“系统性完成”掩盖尚未检查的范围。

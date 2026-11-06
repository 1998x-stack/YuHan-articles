# AGENTS.md — YuHan Articles

> 本文件面向在本仓库工作的 AI 编程与写作 Agent。仓库主要产物是高质量 Prompt、Agent Skills、方法文档与示例，而不是可运行的应用程序。

## 目标与原则

让使用者能够可靠地将现代议论文、史论与评论改写为**韩愈式文言论说文**，在保全论旨、关键史实和逻辑链的前提下，突出推原究本、设难破惑、辨名核实、气盛言宜。

核心优先级：**真实与保真 > 论证质量 > 语言古雅 > 修辞华美**。不要追求“像韩愈说过”而伪造古籍或韩愈原话。

## 项目地图

- **prompts/han-yu-master-prompt.md**：规范性完整版 Prompt；变更行为时首先审视此文件。
- **prompts/han-yu-quick-prompt.md**：面向复制粘贴的精简提示词；不得与完整版原则冲突。
- **.opencode/skills/han-yu-argumentation/SKILL.md**：OpenCode 原生 Skill。
- **.pi/skills/han-yu-argumentation/SKILL.md**：Pi 原生 Skill。
- **docs/method-and-evidence.md**：事实、解释、假设、判断的处理细则。
- **docs/quality-rubric.md**：七维质量量表与硬性退稿条件。
- **examples/short-rewrite.md**：人为创作的短例，不冒充历史记载。
- **scripts/validate_skills.py**：无第三方依赖的本地检查。
- **.github/workflows/validate-skills.yml**：自动化结构验证。

## Agent 执行规则

1. **先判明任务**：用户要改写、原创、审稿、事实核查还是维护仓库？不要把所有请求都当作“全文重写”。
2. **改写时提取论点与证据**：对关键信息进行事实／解释／设论／价值判断分类，原文没有的数据不要补造。
3. **优先论辩结构**：从最值得解释的反常现象起笔，经事实、机制、异议、结论逐层推进；不是把现代词汇批量替成古词。
4. **以强对手检验论点**：公平复述异议，避免稻草人；如果反方部分成立，要限制自己的判断。
5. **尊重原文立场**：不要强行添加儒家道统或改变作者的政治、伦理与社会主张。
6. **表达严谨**：人物行为不等于人物动机，获利不等于欺诈，单一案例不等于普遍规律。
7. **输出按用户要求**：默认改写任务只交付篇名与文言正文；如果用户要求解释、对照或文件，则依明确要求。
8. **无原文不假装有原文**：当任务是“改写”却缺少来源时，请用户提供；若是“原创”，明确遵循已有主题与证据范围。

## 维护契约

- **两个 Skill 必须字节级一致**：同一个 name、description、流程与限制。不得擅自修改其中一个而遗忘另一个。
- frontmatter 必须以 YAML 的 --- 开始，含 name 与 description；目录名与 name 都应是 han-yu-argumentation。
- 为保持可移植，Skill 的关键步骤应自包含；仓库内的相对链接仅作可选深化材料。
- 所有新增事实、历史引文和人物言语在发布前必须核查来源；有争议时标明归属与确定性，不得伪造。
- 修改 Prompt、Skill 或文档时审查 README 的目录、示例命令、交付契约是否需要同步。
- 不引入不必要的应用框架或第三方依赖。新增脚本应简洁，安全，无联网副作用。

## 验证与提交

在仓库根目录执行：

~~~bash
python3 scripts/validate_skills.py
~~~

校验通过后，人工对照 docs/quality-rubric.md 复核：保真、论证、名实、句法与交付格式。请勿把纯结构化 CI 通过等同于文学质量通过。

建议提交信息围绕变更目的，例如 docs: refine Han Yu master prompt 或 skill: update argumentation workflow。

## 不可接受的变化

- 仅增添“夫、盖、然则”等词，却削弱事实和推理；
- 移除事实核对要求，或允许伪造引文、年代和数字；
- 将“名实辨析”退化为无证的动机指控；
- 让 OpenCode 与 Pi Skill 流程出现分歧；
- 在无实际检查的情况下宣称文章经过核实或校验通过。

## 文章归档与出版

- 文章按 `articles/01-...` 至 `articles/08-...` 分类，24 个规划子目见 `articles/TAXONOMY.md`；三级为独立篇名目录，空分类以 README 保留。
- 每篇仅有一个主分类；相关分类在子目 README 设置交叉链接，不得复制同一篇文章。
- 每篇须有 `README.md`、`article.json`、Markdown 正文；DOCX/PDF 按正文通过 `python scripts/build_articles.py` 统一生成。
- 编辑正文或新增文章须运行 `python3 scripts/build_catalog.py` 更新 `articles/CATALOG.md` 及分类导航；保持文件名与 `article.json.manuscript` 一致。
- 不要直接分别修改 Word/PDF 内容，以免三版互不相符。详见 `docs/article-archive-conventions.md`。

## 文章分类维护

- 遵守 [articles/TAXONOMY.md](articles/TAXONOMY.md)：按主要论证对象选择唯一主分类，跨主题仅增加 `article.json.topics` 标签。
- 子目 README 是有效占位与入口，勿创建无内容 `.gitkeep` 或虚构作品。
- 发布新篇须维护子目与部类 README，再运行 `python3 scripts/build_catalog.py` 自动更新 `articles/CATALOG.md`，DOCX/PDF 从 Markdown 生成。

## 网站设计与部署契约

- 网站模板与 CSS/JS 只保存在 site/；所有文章从 articles/ 中 status=published 的 article.json 和 Markdown 单一来源生成，禁止将同一篇正文粘贴到 HTML 模板。
- 构建脚本为 scripts/build_site.py，输出到忽略提交的 _site/；正式站点路径包含 /YuHan-articles/，新增静态链接必须处理该项目子路径与中文 URL 编码。
- Markdown 转 HTML 后必须经安全白名单过滤；元数据由 Jinja2 转义，绝不允许文章输入执行脚本。
- 网页兼顾中文衬线长文排印、移动端、键盘操作、打印、深浅色、无 JS 浏览与无远程追踪脚本；详见 docs/website.md。
- 修改网页后必须通过 scripts/validate_site.py 和 GitHub Actions Pages 构建。网站“部署成功”只有在 deploy job 成功并且公开网址确实可访问时才能宣称。

# YuHan Articles · 韩愈式古文论辩写作

以韩愈古文的**论辩方法**重构现代文章，而非把白话逐字替换为文言词汇。

项目提供可直接复制的写作提示词，以及适用于 **OpenCode** 与 **Pi** 的 Agent Skill。核心要求是：**义明、理密、辨深、辞健、法活、气贯、意远**。

## 核心理念

- **推原究本**：由现象追问原因，辨明人情、利害与制度条件。
- **反俗立论**：准确提出通行解释，再检验其前提与结论。
- **设难破惑**：为异议建立最有力的论据，并在其前提内推演。
- **辨名核实**：区分名义、行为、结果与利益，拒绝未经证明的动机推定。
- **据事明理**：保留关键史实、数字、细节与因果过程。
- **蓄势断案**：以论证累积文势，在篇末形成有根据的判断。

写作不等于移植儒家立场，也不等于把所有句子改成“夫、盖、然则”。**先求道理成立，继求文章有气。**

## 文章库

按八大主题、二级子目长期收录，以“主题／子目／单篇”层级组织，一篇文章同时提供 Markdown、Word 和 PDF：

- [文章分类与导航](articles/README.md)
- [作品总目录](articles/CATALOG.md)
- [主题分类体系（24 子目）](articles/TAXONOMY.md)
- [《河伯娶妇辨》](articles/01-史论与人物/史事辨/河伯娶妇辨/README.md)（史论与人物／史事辨）
- [《论执纪之难》](articles/02-制度与治理/纪检监察/论执纪之难/README.md)（制度与治理／纪检监察）
- [《原寺观财弊论》](articles/04-宗教与风俗/宗教治理/原寺观财弊论/README.md)（宗教与风俗／宗教治理）
- [文章分类设计与收录流程](articles/STRUCTURE.md)
- [归档标准与出版流程](docs/article-archive-conventions.md)

Markdown 是唯一正文源；Word、PDF 由 `scripts/build_articles.py` 自动生成，不应直接分头编辑。

## 快速开始

### 直接使用 Prompt

打开 [完整版写作 Prompt](prompts/han-yu-master-prompt.md)，将末尾的 **【待改写原文】** 换成实际文章，并按需调整文体、论证密度与篇幅。

如需快速调用，可用 [精简版 Prompt](prompts/han-yu-quick-prompt.md)。

### 在 OpenCode 中使用

Skill 位于 **.opencode/skills/han-yu-argumentation/SKILL.md**。在本仓库中启动 OpenCode，输入：

~~~text
请使用 han-yu-argumentation skill，把下面的现代评论重构为韩愈式古文论说文。
保留全部核心证据与立场，不得虚构史实；只输出篇名与正文。

【在此粘贴原文】
~~~

### 在 Pi 中使用

Skill 位于 **.pi/skills/han-yu-argumentation/SKILL.md**。在本仓库启动 Pi，可使用：

~~~text
/skill:han-yu-argumentation 将以下文章改写为韩愈式古文论说文，保持事实与论旨不变：【原文】
~~~

Pi 支持项目中的 .pi/skills/ 目录及显式 Skill 命令。若修改 Skill 后当前会话未更新，可执行 Pi 的 /reload。

## 目录

~~~text
.
├── articles/                               # 八大主题文章库
│   ├── CATALOG.md                          # 作品索引
│   ├── STRUCTURE.md                        # 分类体系、子目占位与收录规范
│   ├── TAXONOMY.md                         # 主题、子目与归档规则
│   ├── 01-史论与人物/ ... 08-杂说与辨析/
│   ├── 02-制度与治理/纪检监察/论执纪之难/  # 三格式作品
│   ├── 04-宗教与风俗/宗教治理/原寺观财弊论/ # 三格式作品
│   └── _templates/                         # 单篇目录模板
├── AGENTS.md
├── README.md
├── prompts/
│   ├── han-yu-master-prompt.md
│   └── han-yu-quick-prompt.md
├── .opencode/skills/han-yu-argumentation/SKILL.md
├── .pi/skills/han-yu-argumentation/SKILL.md
├── docs/
│   ├── method-and-evidence.md
│   └── quality-rubric.md
├── examples/
│   └── short-rewrite.md
├── scripts/
│   └── validate_skills.py
└── .github/workflows/
    └── validate-skills.yml
~~~

## 推荐工作流

1. **审原文**：提取中心论断与可核实事实，区分引述、推测和假设。
2. **定论势**：确定最大的矛盾和反方最强解释，安排由疑到辨、由辨到断的推进次序。
3. **重写**：以唐代散体古文为本，长短错综；通过条件、比较、反诘推动逻辑。
4. **复核**：逐一核对人物、数字、引文和因果陈述，删除空论与不承担论证功能的华辞。
5. **交付**：默认仅输出古雅篇名与完整正文；原文未提供时先索取原文。

更多详见 [方法与证据规范](docs/method-and-evidence.md)、[七维质量评估](docs/quality-rubric.md)及[短例](examples/short-rewrite.md)。

## 使用边界

- **不伪造**韩愈原话、古籍引文、史实、数字或人物心理。
- **不偷换**作者的核心立场；现代科学、制度概念应解释其含义后再文言化。
- **不因获利便断定虚伪**；对意图与因果须有证据。
- 事实存疑时，宜保留来源归属或审慎语气；不能把推测写成“史载”。
- 以韩愈为风格与论证方法的参照，生成的文章**不是韩愈真作**。

## 维护与校验

两端 Skill 应保持一致，避免行为漂移。修改一处 Skill 时同步修改另一处，然后在仓库根目录运行：

~~~bash
python3 scripts/validate_skills.py
~~~

持续集成也会检查 Skill frontmatter、路径、同步状态与 Prompt 文档是否存在。编辑规则见 [AGENTS.md](AGENTS.md)。

## 兼容性参考

- [OpenCode Agent Skills 文档](https://docs.opencode.ai/docs/skills/)
- [Pi Skills 文档](https://pi.dev/docs/latest/skills)
- [Agent Skills 规范](https://agentskills.io/specification)

本仓库内容用于文体学习与文字创作，历史与时事事实仍需独立核验。

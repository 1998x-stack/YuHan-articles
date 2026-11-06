# 仓库运行与维护手册 · Maintainer Runbook

## 1. 系统组成与值班观察点

| 系统 | 主要文件 | 预期结果 |
| --- | --- | --- |
| 写作规范 | `prompts/`、双端 Skill | agent 文风规则一致、文字可复用 |
| 现代作品 | `articles/`、`article.json` | 真实已刊文章与元数据保持一致 |
| 韩愈真作 | `classics/`、`meta.json` | 五篇原典可读、署名与参校可追 |
| 自动目录 | `scripts/build_catalog.py` | CATALOG 自动反映 published 文件 |
| 排印 | `scripts/build_articles.py` | 同名 DOCX/PDF、中文可读 |
| 网站 | `scripts/build_site.py` + `site/` | 静态 HTML、RSS、站点地图、检索与分类 |
| 验收 | `scripts/validate_repository.py` + 单测 + `validate_site.py` | 失败时报明确文件和问题 |
| 部署 | 三个 `.github/workflows/*.yml` | 相应 CI 与 Pages deploy 通过 |

技术总体设计见 [architecture.md](architecture.md)，网站视觉体系见 [website.md](website.md)。

## 2. 环境准备

建议 Python 3.12：

~~~bash
python3 -m venv .venv
source .venv/bin/activate           # Windows: .venv\Scripts\Activate.ps1
python3 -m pip install -r requirements-site.txt
python3 -m pip install python-docx reportlab
~~~

系统字体不是代码依赖的必需文件，但专业排印建议安装有许可证的中文 TrueType 字库并通过 `YUHAN_CJK_FONT` 指定。缺字库时会回退到不嵌入字体的 CID，具体见 [fonts.md](fonts.md)。

## 3. 验收等级

**结构检查（无需联网）**

~~~bash
python3 scripts/validate_repository.py
python3 scripts/validate_skills.py
python3 scripts/build_catalog.py --check
python3 -m unittest discover -s tests -p 'test_repository.py'
~~~

**网站检查（需安装 requirements-site.txt）**

~~~bash
python3 -m unittest discover -s tests -p 'test_classics.py'
python3 -m unittest discover -s tests -p 'test_site.py'
python3 scripts/build_site.py --site-url http://localhost:8000/
python3 scripts/validate_site.py --base-path / --min-articles 1 --min-classics 5
python3 -m http.server 8000 --directory _site
~~~

然后在浏览器打开 http://localhost:8000/ ，抽查首页、`/articles/`、`/classics/`、一个长文、一个脚注、一个 PDF 下载，以及手机宽度下的排印。

**出版检查（需 python-docx/reportlab）**

~~~bash
python3 -m unittest discover -s tests -p 'test_fonts.py'
python3 scripts/build_articles.py
python3 scripts/validate_repository.py --require-exports
~~~

若 DOCX/PDF 实际显示缺字或脚注格式混乱，不能仅凭文件存在断言“出版质量通过”。

## 4. 新作品上线操作

1. 在 [归类规范](../articles/TAXONOMY.md) 中确认唯一主分类，优先选既有子目。
2. 复制 [单篇模板](../articles/_templates/article/README.md)；填写对应的 `article.json` 和 `# 标题`。
3. 使用 `draft` 或 `review` 暂存稿件并审校证据；只有完成审稿才改为 `published`。
4. 运行仓库结构检查和 `python3 scripts/build_catalog.py`，不要手工编辑 CATALOG。
5. 若需本地验证排印则运行 `build_articles.py`；正式提交可能触发出版工作流自动重建。
6. 修改发布状态后核对分类页、篇名、下载链接，检查 Pages 的部署状态。
7. 若发布到旧 URL，防止移动中文目录导致既有外链失效。

不要将原典收进现代论说分类。新增韩愈原典必须经过来源与异文核查，`meta.json` 的作者、文体、卷次、原典参校来源须准确。

## 5. GitHub Actions 故障诊断

### Agent Skills Validation 失败

先读 [validate-skills.yml](../.github/workflows/validate-skills.yml) 中失败的命令。常见问题是双端 SKILL 不一致、frontmatter 格式、README 链接不存在、metadata 不合规。先修正确凿错误再重新运行，禁止关闭相关校验以求绿色。

### PDF/Word Publication 失败

读 [publish-articles.yml](../.github/workflows/publish-articles.yml) 的最新作业日志。确认字体包、Python 依赖、稿件 status、标题和正文名一致。该工作流曾因 PDF/DOCX 二进制 rebase 冲突失败，现需从最新 `origin/main` 重新计算并尝试提交，**不对二进制做 rebase**。

如果连续推送造成多次失败：确认远端分支近期变更是否来自其他成员，再从最新 main 单独复现出版构建；禁止 `git push --force` 覆盖他人的稿件。若文件是生成件而非源码，不要直接在 GitHub 网页上编辑二进制。

### GitHub Pages 构建失败

读 [pages.yml](../.github/workflows/pages.yml)，按先后顺序核查：Python 安装 → repository 结构/单测 → Word/PDF → build_site.py → validate_site.py → artifact 上传 → deploy。若 build 失败，网页尚未更新；若 deploy 失败，应检查 GitHub Pages 的 Source 设置、权限和环境限制。

Pages 网址为 https://1998x-stack.github.io/YuHan-articles/ 。生产链接必须带 `/YuHan-articles/` 子路径；本地预览为根目录时指定 `--site-url http://localhost:8000/` 且检查时使用 `--base-path /`。

### 网站缺文章或下载

检查 `article.json.status` 是否 `published`、`manuscript` 是否为本目录真实 Markdown 文件、`# 标题` 是否一致，以及导出是否确实生成。RSS、站点目录和分类卡片通过元数据生成，**不能通过修改 HTML 模板冒充文章已发布**。

### 字体和排印

参考 [fonts.md](fonts.md)：优先选择可合法嵌入的 TTF，不要把 OTF 改扩展名；Word 字体是阅读器侧名称，不能保证对方已有相同字库。CJK CID 回退只保证构建路径，不保证每个 PDF 阅读器显示一致。

## 6. 发布回滚与应急处置

遇到错误发布，不要直接删除所有生成资源或强制改写历史。先记录错误网页 URL、对应 commit SHA 与 Actions run ID；确认是否涉及事实错误、侵权材料或安全问题。公开内容如有隐私/侵权风险，按 [SECURITY](../SECURITY.md) 处理，优先降低继续传播的风险。

正常工程回滚使用**针对性 revert 或补丁提交**，保留他人的并发改动，并让 Pages 重建。自动生成的 Word/PDF 应由修正后的 Markdown 重建，不以 Git 的二进制冲突解决思路回退文字。

## 7. 定期维护任务

建议按批次审查：公开文档的相对链接、源码依赖版本、GitHub Actions 是否仍有兼容性问题、外部史料链接是否失效、仓库二进制历史是否膨胀、字体许可是否清楚、标注为 published 的文章是否真的完成了人工事实审校。

脚本没有外部连接时只能做本地结构检查；链接可访问性、事实来源与浏览器排版仍需单独验证。不要把自动测试合格混同于文学、学术或法律审查完成。

## 8. 文档、权限和交付

- 项目说明：[README](../README.md)
- Agent 工作契约：[AGENTS](../AGENTS.md)
- 贡献流程：[CONTRIBUTING](../CONTRIBUTING.md)
- 权利边界：[rights-and-licenses.md](rights-and-licenses.md)
- 编辑原则：[editorial-standard.md](editorial-standard.md)
- 审计记录：[repository-audit.md](repository-audit.md)

完工总结须附修改路径、实际测试情况、对应 GitHub commit、Actions / Pages 结果和未完成风险。没有运行工具时不能宣称 CI 通过；没有人工事实核验时不能宣称文章已经全部考证。

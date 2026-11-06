# 贡献指南 · Contributing to YuHan Articles

感谢对古文、史料、论辩方法、排版质量与代码维护的改进建议。本仓库的核心要求：**事实和署名准确，正文只有一个权威版本，自动构建结果可检验**。

## 先选择贡献类型

| 目的 | 修改范围 | 需要特别注意 |
| --- | --- | --- |
| 新增现代论辩文章 | `articles/<分类>/<子目>/<篇名>/` | 主分类唯一、正文证据可核查、metadata 有效 |
| 修订既有文言稿 | 原 Markdown + README / 依据 | 不擅自改变原作者立场或删除不利证据 |
| 校对韩愈原作 | `classics/<slug>/` | 提供底本、记录异文；不把通行说法误当定本 |
| 改进 Prompt/Skill | `prompts/`、`.opencode/`、`.pi/` | 两端 Skill 必须同步 |
| 改进 Pages 网页 | `site/`、`scripts/build_site.py` | 长文、手机、脚注、链接、安全与可访问性 |
| 修复构建和 CI | `scripts/`、`tests/`、`.github/` | 必须有复现、回归测试及实际运行结果 |
| 修订文档 | `README.md`、`AGENTS.md`、`docs/` | 不维护相互矛盾的多个分类和版本清单 |

## 投稿要求

文章使用 UTF-8 Markdown；首行使用 `# 篇名`。将史实、受访者描述、假设与评断明确区分。对于现代经济数字、法规、政府通报、学术断言和经典引文，尽可能在文末列可访问的原始出处；只知道二手出处时须明确来源层级。

对于争议材料，不要把“需要核实”改写成“已有确证”。比较不同群体、组织或利益方时，不能只因某方获利就断定其所有行为与言论虚伪。

**禁止**将他人受保护的整篇文章直接导入公开仓库。公有领域的古人原作和后人编者的标点、注释、翻译需要分开判断权利。

## 从草稿到正式发表

1. 参照 [分类准则](articles/TAXONOMY.md) 选择真实存在的一级目录和二级子目。
2. 复制 [文章模板](articles/_templates/article/README.md)，新建 article.json、正文 Markdown 与 README；不要直接改总目录。
3. 将 status 置为 `draft`，组织证据和论辩，再进入 `review`。
4. 人工复核事实、引用、归属与逻辑；满足发表条件后才切换 `published`。
5. 运行结构测试与总目生成；出版器从同一 Markdown 输出 PDF/Word。
6. 在 Pull Request 中说明证据来源、修改理由、影响路径、运行过的命令与可复现结果。

完整指南见 [新增文章](docs/adding-an-article.md) 与 [编辑与事实标准](docs/editorial-standard.md)。

## 本地检查

建议 Python 3.12：

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
~~~

只修改文章文字可在生成前检查数据和总目；发布前还须运行 `python3 scripts/build_articles.py`、`python3 scripts/validate_repository.py --require-exports`，并抽查实际 PDF/DOCX。修改网站需运行：

~~~bash
python3 scripts/build_site.py --site-url http://localhost:8000/
python3 scripts/validate_site.py --base-path / --min-articles 1 --min-classics 5
python3 -m http.server 8000 --directory _site
~~~

不要提交 `_site/`、虚拟环境、系统字体或任何密钥。Word/PDF 是生成件；改变文本时只编辑 Markdown。为避免并发生成的二进制冲突，请由出版工作流在最新 main 上重新生成。

## Pull Request 内容

建议标题 `type(scope): summary`，例如：

- `docs: unify taxonomy and publishing guidance`
- `fix(pages): validate manuscript relative paths`
- `feat(article): add new classical-style essay`

PR 描述应列明**目的、涉及文件、数据出处、兼容性/URL 风险、测试命令及结果**。对于原典更改，应增加“异文：旧字形/新字形/依据版本”的记录；对于 UI 更改，最好附桌面及手机截图（可使用自己制作的截图，不含私人资料）。

## 评审与合并

自动化通过只是最低标准，不能代替古文审稿、事实核验和浏览器人工验收。已有篇名、公开 URL 或原典内容涉及迁移时优先保持兼容。请勿通过删除测试、放松来源要求或改写历史证据来让 CI 勉强通过。

尚未建立的议题可创建 Issue 讨论，但**不要用空白文章或虚构内容占用“已发表”条目**。有关项目结构与具体排障，参阅 [架构](docs/architecture.md) 与 [维护手册](docs/maintainer-runbook.md)。

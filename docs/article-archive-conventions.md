# 文章库结构与出版规范

## 一、目录分类

一级：固定八大主题 `articles/01-...` 至 `articles/08-...`；二级：具体子目；三级：每一篇文章一个独立目录。不得按 Markdown/Word/PDF 三种格式分别建立散乱的文件夹。

文章一律以中文题名命名，一级分类以两位数字排序。新增题类须在分类 `README.md` 写明收录范围，并更新 `articles/README.md`、`articles/TAXONOMY.md` 与 `articles/CATALOG.md`。一篇仅存一个主分类，其他类用交叉链接；24 个规划子目均以真实 README 文件夹占位。

## 二、单篇构成

```text
articles/02-制度与治理/纪检监察/论执纪之难/
├── README.md         # 摘要、事实边界与阅读链接
├── article.json      # 标题、分类、日期、状态、标签
├── 论执纪之难.md      # 唯一正文来源
├── 论执纪之难.docx    # 自动生成
└── 论执纪之难.pdf     # 自动生成
```

`article.json` 中 `manuscript` 必须指向同目录 Markdown。所有正文更新须改 Markdown，再运行 `python scripts/build_articles.py`，不可直接编辑衍生文档后不回填 Markdown。

## 三、写作与史料边界

保留原文所可证的关键事实与推断边界；人物转述应明示转述属性，不得把推测写成已经证实的史事。古文论说须有明确论旨及其论据，不能只堆叠虚词。引用需核对出处，现代法律与数据应以可查材料为据。

## 四、出版与维护

`pip install python-docx reportlab` 并安装中文 TrueType 字体，例如 Ubuntu 的 `fonts-arphic-gbsn00lp`，然后运行 `python scripts/build_articles.py`。

GitHub Actions 会在正文、生成脚本或工作流变化后生成 DOCX/PDF 并提交。发布后检查 GitHub 的文件列表，确保同名的 `.md/.docx/.pdf` 均存在。二进制文件为自动生成件，排版改动应修改生成脚本。

## 五、预设子目与检索

八大部类下的预留子目须创建有实际用途的 `README.md`：写明收录范围、返回导航与当前状态，不使用空文件或虚构篇名作占位。新增子目须维护该部类的 README、`articles/README.md`、`articles/STRUCTURE.md`。单篇只归档于一个最相关子目；其它目录引用其 canonical 路径即可。

## 六、参考资料与版本

Markdown 正文可采用 `[^1]` 方式标识来源，并在文末以 `[^1]:` 逐条给出可访问链接。出版脚本应将标号转换为易读的脚注标记，并将来源收于末尾；不可把 Markdown 标记本身误排为正文。

原始附件与仓库通过 Markdown 重新生成的 Word/PDF 可能排版不完全一致；正文和参考资料以 Markdown 为准。大型修订可另建版本目录或在 Git 历史中保留，不应误称二进制出版物为原附件的逐字节副本。

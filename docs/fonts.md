# 字体配置与 PDF 发布

**仓库不提交第三方字体二进制文件。** 原先的 `/usr/share/fonts/truetype/...` 是 Ubuntu/Linux 下的可选安装位置，并非所有系统都存在。编辑文章或在 GitHub 上构建 PDF 不应以本机是否有固定绝对路径作为必要条件。

## 默认行为

1. 若设置环境变量 `YUHAN_CJK_FONT`，尝试加载该文件并将兼容的 TrueType 字体嵌入 PDF。路径不存在、字体不兼容时明确报错，避免错误地以为 PDF 已嵌字。
2. 否则依序尝试常见的系统中文 TrueType 字体路径，找到兼容字体即嵌入。
3. 若没有兼容字体，使用 ReportLab 的 **`STSong-Light` Unicode CID** 字体，无需本地字体文件即可生成包含中文的 PDF。

**注意**：内置 CID 字体**不会嵌入 PDF**。不同平台的阅读器可能使用替代字体，存在外观差异甚至缺字风险；长期归档与专业印刷宜选用可嵌入的字体并验收 PDF。

## 安装或指定嵌入字体

Linux / Ubuntu（项目 GitHub Actions 构建用）：

```bash
sudo apt-get update
sudo apt-get install -y fonts-arphic-gbsn00lp
python3 -m pip install python-docx reportlab
python3 scripts/build_articles.py
```

如果发行版路径不同，可显式指定允许嵌入的本地字体：

```bash
export YUHAN_CJK_FONT="/absolute/path/to/your/chinese-font.ttf"
python3 scripts/build_articles.py
```

PowerShell（Windows）：

```powershell
$env:YUHAN_CJK_FONT = "C:\\Windows\\Fonts\\simhei.ttf"
python scripts/build_articles.py
```

以上 Windows 路径仅为一种可能的安装位置；请使用**本机确实存在且许可允许嵌入**的字体文件。未安装指定字体时，移除环境变量以使用自动候选与 CID 回退。

若希望单篇 Word 文档采用另一字体族，可以独立指定 `YUHAN_DOCX_FONT`，如 `SimSun`。Word 字体名称不代表 PDF 嵌入权限，也不保证阅读端安装该字库。

## 字体格式与兼容性

ReportLab 的 `TTFont` 支持兼容的 TrueType-outlines `.ttf` 以及部分 `.ttc` 字体集合；并非所有 OpenType/CFF 字体或 TTC 都能嵌入。若自定义字体不兼容，请换成合法且与 ReportLab 兼容的字体文件，不要把 `.otf` 简单改名为 `.ttf`。

本项目只提交代码与配置，不附带任何字体文件，也不在 GitHub Actions 中绕过字体授权限制。需要分发字体时请先核实字体许可证中的再分发与 PDF 嵌入条款，保留要求的版权和许可证信息；来源不明的字库不得作为仓库资产提交。

## 验证

```bash
python3 -m unittest discover -s tests -p 'test_fonts.py'
python3 scripts/build_articles.py
```

检查生成的 PDF 是否正确显示中文、段落与粗体。若需要确保字体实际嵌入，可用本机的 `pdffonts` 命令检查生成结果的 `emb` 列；CID 回退为未嵌入的方案，应按预期确认而不是视为排版故障。

参考：[ReportLab 官方字体使用指南](https://docs.reportlab.com/reportlab/userguide/ch3_fonts/)。

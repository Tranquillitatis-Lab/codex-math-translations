# 自守形式、表示与 L 函数：中文合订本

两册的38篇主文章及1篇附录已全文翻译并合编，`main.tex` 为统一入口。包含统一目录、连续页码、作者索引与附加术语表；用户补充的原第295页已译入Ihara一文。

交付合订 PDF 共 752 页，已使用 XeLaTeX 生成。各分工记录中的“未编译”指单篇翻译阶段，主工程已统一编译。

## 排版与构建

- 使用本机 TeX Live 2025、XeLaTeX、ctexbook。
- 中文宋体，标题黑体，西文 Times New Roman；数学采用 amsmath / amssymb。
- A4 双面排版，统一目录、连续页码、按作者索引。
- 每篇保留原书内部节号、定理号、公式号；原册号和起始页见篇首。
- 可重绘的交换图、示意图使用 TikZ / TikZ-CD；表格使用 booktabs。
- 原文中若有程序，listings 提供语法高亮。

在工程目录运行 `make`，结果位于 `output/pdf/自守形式、表示与L函数-中文合订本.pdf`；构建结束后自动清理编译中间文件。

## 原文与翻译记录

- `articles.json`：38 篇主文章及 1 篇附录的目录、作者、原书页码与 PDF 页码。
- 原 PDF 文本缓存已清理，需要时运行 `python3 tools/extract_source_text.py` 重建 `source-text/`（需保留原 PDF，并安装 `pdftotext`）；缓存不参与合订本编译。
- `chapters/`：逐篇中文 XeLaTeX 译文。
- `notes/NN-status.md`：各篇覆盖范围、扫描本疑点及处理说明。
- `TRANSLATION.md`：统一术语与翻译规范。

## 第295页补页来源

第二册原PDF从原书第294页跳至第296页。用户随后提供了第295页图像，已保存为 `source-supplements/volume-2-p295.png`。本页完整译文、公式与TikZ树图编入Ihara一文；此前缺页占位撤销。

## 翻译原则

逐段翻译，技术术语首次出现括注英文，参考文献保留检索用原题名。沿用原文的历史语境，疑似排印错误在正文译注中说明，不静默更改作者原式。原文件保持不变。

## 空间清理

已删除逐页渲染缓存、阶段稿、编译日志与中间文件、重复 PDF、源码 ZIP 和未使用的旧图裁切。保留源码、正文所需图表、补页原图、翻译记录及最终 PDF。需要源码压缩包时，运行 `python3 tools/package_sources.py` 重新生成。

合并仓库后，补提取文字层时设置 `AUTOMORPHIC_SOURCE_DIR` 为两册原 PDF 所在目录；编译中文译本不需要原 PDF。

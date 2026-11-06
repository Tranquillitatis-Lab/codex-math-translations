# 函子代数几何导论：第一卷·仿射代数几何

A. Grothendieck 讲授，Federico Gaeta 笔记。

## 阅读

打开 `函子代数几何导论·第一卷·中文译本.pdf`。目录、正文术语与书末中英法对照表均带内部跳转链接。书末列出的页码属于译本；同页出现多次的术语以括号中的序号分别返回各处正文。正文外侧的灰色页码属于原书。

## 重新编译

需要 XeLaTeX（TeX Live 2025 或具有相应宏包的发行版）、Python 3，以及字体 Songti SC、Heiti SC、Kaiti SC、TeX Gyre Pagella、TeX Gyre Heros 和 Latin Modern Mono、Times New Roman。中文字体可在 `main.tex` 中更换为本机安装的思源宋体/黑体等字体。

在工程目录运行：

```sh
python3 build_book.py
```

脚本为正文术语添加链接，运行三遍 XeLaTeX，并依据实际译本页码生成返回各处正文的链接。生成结果同时存放于 `build/main.pdf` 和工程根目录的中文文件名 PDF。

## 文件

- `main.tex`：版式、字体、公共数学命令、目录与术语链接样式。
- `cover.tex`：TikZ 矢量封面。
- `chapters/a.tex` 至 `chapters/g.tex`：完整分段译文。
- `glossary.json`：中英法术语数据与中文别称。
- `glossary-sources.md`：法语术语参照。
- `build_book.py`：生成互链和编译。
- `build/`：自动生成的正文、术语表、编译辅助文件。
- `source-pages/`、`ocr/`：本地翻译工作中的原页图像与轻量 OCR 参考；重新编译不需要这两个目录。

公式和交换图在译文中重排，原书明显排印错误以译注标明。OCR 仅作文字参考，译文以扫描原页为依据。

合并清理后，`source-pages/`、`ocr/`、`build/` 和重复 ZIP 已移除；重新构建会生成 `build/`。正式 PDF 保留在本目录。

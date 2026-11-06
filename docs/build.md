# 编辑与构建

在仓库根目录用 `python3 tools/build.py <项目> [SGA册号]` 调用各书原有构建流程。Python 脚本默认沿用当前 Python 3；普通译本构建主要使用标准库及现有 TeX Live。

| 项目名 | 在对应书目录内使用的原入口 | 编辑对象 |
| --- | --- | --- |
| `sga4-5` | `python3 tools/build.py` | `chapters/`、术语 JSON、`notes/` |
| `fga` | `python3 tools/build.py` | `chapters/`、`notes/` |
| `arithmetic-algebraic-geometry` | `make` | `chapters/`、`translator-notes.tex`、术语数据 |
| `automorphic-forms` | `make` | `chapters/`、`preamble.tex`、`articles.json`、`notes/` |
| `functorial-algebraic-geometry` | `python3 build_book.py` | `chapters/`、`glossary.json`、`main.tex` |
| `faisceaux-pervers` | `zsh build.sh` | `chapters/`、`style/terms-core.tsv`、逐章术语 TSV |
| `sga` | `python3 tools/build.py sga1` 或 `all` | `volumes/*/chunks/`、`glossary/`、`reports/` |

## 环境

各项目沿用原先的 TeX Live / XeLaTeX、latexmk、ctex、TikZ 和 tikz-cd。多数书使用 Fandol 等 TeX Live 字体；函子代数几何导论和自守形式工程还使用 Songti SC、Heiti SC、Kaiti SC 或 Times New Roman 等本机字体，换系统时应在各自主文件或 preamble 中设置替代字体。

部分脚本仍沿用 macOS TeX 的 `/Library/TeX/texbin`，反常层入口使用 zsh。其他系统需相应调整；本次没有替换字体或另建 TeX 环境。

SGA 带原页图的缺失报告需要 PyMuPDF（`fitz`）和原 PDF；文本缓存的重提取还使用 `pdftotext`。沿用已有 Python / Conda 环境即可，不需本地 OCR 模型。

## SGA 后续交付

现有 12 个分册 PDF 已保留。生成总本：

```sh
python3 tools/build.py sga all
```

在 `books/sga/` 中生成带原页图片的缺失报告：

```sh
SGA_SOURCE_DIR=/path/to/original-pdfs python3 tools/build_gap_report.py
```

`reports/missing-content.json` 保留已有原页文字上下文。`collect_gaps.py` 在文字缓存不存在时会沿用这些上下文；需要重新提取时设置 `SGA_SOURCE_DIR` 并运行 `tools/extract_sources.py`，该脚本保留已有进度清单。

SGA 总本有大量术语锚点，原构建入口为该进程单独设置 XeLaTeX 资源参数；继续使用脚本入口。

## 清理约定

`generated/`、`build/`、`work/`、原页渲染、文字缓存、编译中间文件和 ZIP 不进入 Git。正式中文 PDF、正文引用的图表、补页证据、术语源数据及数学疑点记录继续维护。

FGA 原脚本默认生成 `output/pdf/main.pdf`，交付文件另有中文文件名；根目录统一入口会同步这一命名文件；直接调用分书脚本时需自行同步。重复 ZIP 可由 `git archive` 或对应书的打包入口按需生成。

本次归并仅整理源码与已有成品，未运行全书编译。

# FGA 中文译本

Alexander Grothendieck，《代数几何基础》（Fondements de la géométrie algébrique），1962年汇编本；包括八篇1957—1962年Bourbaki报告和作者的评论、勘误。

## 阅读

最终PDF位于 `output/pdf/FGA-代数几何基础-中文译本.pdf`。

- 原书全部内容重新排印，破损后重扫的149-04页使用完整版本，仅收录一次。
- 正文保留法语术语；中文术语链接至书末中英法对照表。
- 对照表中的中文词条返回首次出现处，位置列表逐次返回各个出现处。
- 页边保留报告号和原印页码；目录及PDF书签可跳转。
- 原有公式编号保留，交换图使用TikZ-CD重绘。
- 作者勘误明确标明来源；新增译者注给出条件、反例或补充论证，并另设索引。

## 源码结构

- `main.tex`：XeLaTeX主文件、数学宏与版式。
- `frontmatter.tex`：封面、版权页及译本说明。
- `chapters/00-commentary.tex`：作者评论、勘误。
- `chapters/01-*.tex` 至 `08-*.tex`：八篇报告译文。
- `tools/build.py`：统一术语写法、补全重复出现位置、生成双向链接与索引，然后调用XeLaTeX。
- `generated/`：可直接编译的生成文件，以及术语、译注、原页覆盖清单 `manifest.json`。
- `notes/`：各篇的翻译记录和数学补注依据，供继续编辑时参考。

源码包不包含原书PDF、扫描图、OCR模型、OCR运行程序或临时编译文件。收到用户关于停止本地OCR的要求后，已终止本任务的OCR进程并卸载其GLM-OCR模型；译本构建不调用任何OCR服务或模型。

## 编译

使用已有TeX Live环境，无须下载字体。所用Fandol中文字体、TeX Gyre Pagella、NewPX数学字体以及ctex、TikZ-CD均为TeX Live提供的常见组件。

修改 `chapters/` 后，在本目录运行：

```sh
python3 tools/build.py
```

仅重新生成术语和索引：

```sh
python3 tools/build.py --generate-only
```

若只修改版式，可直接用：

```sh
latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir=output/pdf main.tex
```

`build.py` 只使用Python标准库，编译时调用 `/Library/TeX/texbin/latexmk`；在其他系统可相应修改该可执行文件路径。编译输出名为 `main.pdf`；交付时另存为上述中文文件名。

## 编辑约定

术语写为 `\term{中文}{English}{français}`，由构建脚本分配每次出现的独立锚点。正文优先按最长术语匹配，数学环境、已有术语宏、标题及结构性LaTeX参数保留，不作词语拆分。

原书页标记写为 `\origpage{扫描PDF页号}{报告号-印刷页号}`。

新增译者注写为 `\translatornote{具体说明}`。书前评论保留1962年的历史时态；对“目前尚未解决”等表述，应同时参看作者评论中的后续进展。


清理说明（2026-11-06）
已移除原页图片、提取文字/OCR缓存、排版预览、generated/和LaTeX编译中间文件。原书PDF仍在上一级目录，正文、译注、原始资料及最终交付文件保留。
重新编译请先在本目录运行 python3 tools/build.py；该命令会重建generated/及所需编译文件。

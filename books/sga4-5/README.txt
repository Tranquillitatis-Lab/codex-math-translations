SGA 4½《平展上同调》中文全译本

底本：同目录上级的 SGA4-0.5.pdf（Springer LNM 569，1977）。
法语录入辅助：source/miller，Daniel Miller 的 LaTeX 转写本，来自 NomiL/sga4.5 镜像。
source/pages 保存扫描本文字层，仅作辨认辅助；公式以扫描图像为准。

文件：
  main.tex：XeLaTeX 主文档、版式与数学环境。
  frontmatter.tex：矢量封面、出版信息和使用说明。
  chapters/：可编辑中文正文。
  generated/：由正文生成的双向术语链接、译者注索引；不要直接编辑。
  math-macros.tex：与法语转写源兼容的数学宏。
  references.bib：正文引用总表；各篇原有书目另在篇末保留。
  术语对照表.csv：中、英、法术语与出现次数。
  notes/：翻译过程中记录的转写纠错与数学疑点。
  output/pdf/SGA4.5-平展上同调-中文全译本.pdf：完整中文译本。
  output/pdf/main.pdf：latexmk 默认构建目标，与上述PDF相同。

构建：
  make
或：
  python3 tools/build.py
需要已安装的 TeX Live（含 XeLaTeX、latexmk、ctex、Fandol、xy、TikZ 等）。
默认 Makefile 使用 python3，可通过 make PYTHON=/path/to/python 覆盖。
不需要 OCR、GPU 或本地语言模型。

正文中的 \term{中文}{English}{français} 会生成前往文末术语表的链接；
同一术语的普通中文重复出现也会自动匹配，数学环境和结构性参数受到保护。
术语表中文词头返回首次出现位置，页码列表则逐一返回每次出现位置。
\translatornote{...} 生成有独立索引的译者注；\origpage{PDF物理页}{原书页码} 标记原页。


清理说明（2026-11-06）
已移除原页图片、提取文字/OCR缓存、排版预览、generated/和LaTeX编译中间文件。原书PDF仍在上一级目录，正文、译注、原始资料及最终交付文件保留。
重新编译请先在本目录运行 python3 tools/build.py；该命令会重建generated/及所需编译文件。

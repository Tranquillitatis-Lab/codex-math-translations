《算术代数几何》中文 XeLaTeX 工程

原书：Lecture Notes in Mathematics 1553，Springer-Verlag，1993。
原文件另含2008年第一篇勘误两页，已译于errata.tex。

构建：在本目录执行 make。需完整TeX Live（含XeLaTeX、ctex、newpxmath、TikZ-cd）及Python 3。
使用TeX Live自带Fandol中文字库与TeX Gyre Pagella西文字库，无需安装额外商业字体。

main.tex：排版主文件。
frontmatter.tex：封面、出版信息、译本说明及序言。
chapters/：八个原始翻译分块，合为原书三篇讲义。
errata.tex：后补勘误与评论的完整译文。
reading-notes.tex：第三篇的原书记号及表述附记。
participants.tex：讲习班参加者名单。
figures/：需要另存的重绘或裁切图。许多图已直接以TikZ-cd写入正文。
tools/prepare.py：收集术语，生成正文与术语表双向链接；不会改动原始翻译分块。
generated/：生成的带链接TeX、术语JSON和翻译用词差异记录；重新构建会覆盖。
术语对照表.csv：独立中英法词表。
source/pages/、source/rendered/：辅助文字与原页图片，仅供原文查阅，保留在工作目录中，不纳入源码包，编译不依赖这些数据。
output/pdf/arithmetic-algebraic-geometry-zh-annotated.pdf：编译的中文译本。
notes-*.md：各分块的识别说明及疑难记录。

术语宏：\term{中文}{English}{français}。
第一篇显示中文（法语），后两篇显示中文（英语）；文末统一列三语。
术语表末列保留各处的反向链接，同页不同出现处有独立链接。
原书印刷页码以页边标记保留，所有定理与公式编号沿用原文。

2026-11-05 译者补注版

依据用户提供的29项勘误说明，在原文相应位置加入编号1–29的译者补注，另有若干相关位置的跳转提示。正文原式和原有编号保留，补注给出说明建议的修正式、适用条件与理由。第2项明确列为定理6.4的证明范围缺口。
translator-notes.tex：全部29项补注正文。
translator-notes-index.tex：可往返跳转的补注索引，页码在编译时自动更新。
annotations/received-corrections-2026-11-05.txt：收到的勘误说明原文。
annotations/note-locations.json：补注与章节定位的对应记录。
旧版PDF与旧版源码包保留在原工作目录的output中。


清理说明（2026-11-06）
已移除原页图片、提取文字/OCR缓存、排版预览、generated/和LaTeX编译中间文件。原书PDF仍在上一级目录，正文、译注、原始资料及最终交付文件保留。
重新编译请先在本目录运行 make；该命令会重建generated/及所需编译文件。

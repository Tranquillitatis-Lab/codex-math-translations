# 翻译共同约定

这是用户要求的全书中文翻译工程。用户授权并行子 Agent。不要缩写、概述、遗漏证明、公式、注、参考文献或脚注。语言要自然、准确，不增添原文未有的数学断言。原书扫描文字层错误很多，必须阅读 rendered/page-NNN.png 辨认数学，不得直接信任 TXT。文件边界可能切在证明中间，承接即可，不重复前一文件的内容。原文段落、编号、假设、量词必须保留。复杂公式可用更宽松的分行，不能改变内容。

- 源文件是 ../(Lecture Notes in Mathematics 1553)...pdf，共 217 个物理页。
- source/pages/NNN.txt 是每页文字辅助；source/rendered/page-NNN.png 是原页渲染。渲染正在生成；若分配页尚未出现，可用 pdftoppm -f N -l N -scale-to 1900 -singlefile -png 原PDF 自己的临时输出前缀。不要同时启动全书渲染。
- 每个物理页开始在合适段落边界插入 \origpage{物理页}{原书页码}，物理6=原书1，至物理213=原书208（即物理页减5）。跨页公式允许先排完公式再插页码。
- 使用 XeLaTeX、ctexbook、amsmath、amssymb、mathtools、mathrsfs、tikz-cd、tikz、booktabs、longtable、enumitem、graphicx、hyperref；不要使用 unicode-math。
- 用 \mathbb{Q}, \mathbb{Z}, \mathcal{O}, \operatorname{Pic} 等标准数学 LaTeX。可用 \Spec, \Gal, \Pic, \Br, \CH, \Hom, \Ext, \Tor, \coker, \Ker, \im, \rank, \NS, \Alb, \et, \dR, \cris, \tors, \id, \Tr, \Nm。其他宏在 notes.md 告知，不修改公共文件。
- 每条技术术语使用 \term{中文}{English}{français}。宏在正文显示“中文（原文语言术语）”，并自动注册术语表和所有双向跳转。第一篇主文件设为 fr，后两篇 en。相同词尽量统一三列；不要将每一个普通名词都作为术语。数学环境中不要放 \term；在相邻中文叙述中标注。
- 可用 \section*{§1. 标题} 和 \addcontentsline{toc}{section}{§1. 标题} 保留编号；不要让 LaTeX 自动编号改变原文编号。定理/命题/引理用 \begin{statement}{定理 1.2}...\end{statement}；备注用正常段落加粗开头；证明用 \begin{proof}...\end{proof}。不要把声明中的中文都排成斜体。
- 公式保留原编号，用 equation* 内 \tag{1.1} 等，或 align* 和 \tag。无编号保持无编号。避免重复 label。交叉引用可先保留原文字编号，无需自行给全书编引用标签。
- 简单交换图用 tikzcd 重绘，长箭头上/下标精确；确实难以可靠重绘时裁切原图到 figures/自己的前缀-* 并注明源页，裁图必须来自渲染，不截中文叙述。不得凭印象猜测公式。
- 参考文献完整保留作者、原文题名、出处、年份页码；原文题名后可加中文译名，不强制翻译文献题名。保留原引用键，以普通文字列表或 description 环境排版。
- 只有每篇第一分块有 \chapter{中文标题}、\chapterauthor{作者名}。所有分块为主文档直接 \input 的正文，不写 documentclass/document。章节内原文单独的 Part/Chapter 标题也保留。
- 主文件负责字体、颜色、全书标题、术语宏；各 Agent 只拥有指定的 chapters/*.tex 和自己的 notes-*.md、figures/前缀-*，不能改其他文件。不要撤销别人修改。你不是独自工作。
- 用户要求“未要求时不做验证”：不额外写测试或重复跑验证。主 Agent 会为交付执行必要编译；分工 Agent 不要各自编译。
- 完成后给出完成物理页范围、所有文件路径、疑难处。不要把不完整草稿宣称完成。持续执行到你负责范围完整写入。

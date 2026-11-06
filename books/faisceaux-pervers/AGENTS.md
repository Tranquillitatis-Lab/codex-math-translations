# 《反常层》中文全译工程

仅在用户明确要求时使用子 Agent。保留原文件，不运行本地高占用 OCR 模型。源 PDF 为 2018 再版，共192页；必须包含所有原有材料，正文、证明、注、书目、附录和勘误均不得摘要替代或省略。

## 原页证据
- source/text/pNNN.txt：PDF文字层，仅作辅助，有大量数学OCR误差。
- source/pages/pNNN.png：原页渲染；数学公式与文字层不符时以图像为准。
- PDF页码为物理页序号，原版印刷页码不统一，引用保留原书编号。

## 协作与文件
各 Agent 只修改分配的章节文件和对应术语增补/疑点记录文件，不修改 main.tex/style 或其他 Agent 文件。你不是唯一编辑者，不回退他人改动。
采用 UTF-8 XeLaTeX，正文自然中文，数学语义严格一致，完整保留所有编号、证明、限定条件与参考文献标号。作者英文/法文人名照原文。原图用 tikz-cd 或 TikZ 重绘；不会重绘时可用源页裁切，不能把整页法文截图充当翻译。

## TeX接口
- 文件为可直接 input 的正文片段，不含 documentclass/preamble/document。
- 每个原PDF页开始写 \\SourcePage{N}，保持可追踪。一段跨页不要补造标题。
- 原编号段落：\\par\\medskip\\noindent\\textbf{1.2.3. 定义。} 原文。编号手写，保留格式，不用自动计数定理。
- 章：\\chapter{标题}（主文0章用\\setcounter{chapter}{-1}后 chapter；其余main按需要设counter）。节：\\section{标题}，或者跨文件用\\section*{1.4. 粘合}以免计数错位。每个Agent统一用带完整编号的\\section*{1.4. 粘合}和\\addcontentsline{toc}{section}{1.4. 粘合}，不创建chapter，主文件负责章标题。
- 显示公式用 \\[...\\]，编号用 \\begin{equation*}...\\tag{1.2.3.1}\\end{equation*}；大量简单式可用 align*。
- 可用 amsmath/amssymb/mathrsfs/mathtools/bm/tikz-cd/tikz/enumitem。交换图用 tikzcd 包（ampersand replacement=\\&）。
- 默认数学宏：\\D=\\mathrm D, \\Hom, \\RHom, \\Ext, \\Spec, \\Supp, \\Ker, \\Coker, \\im, \\id, \\gr, \\Gal, \\Tr, \\rank, \\IC, \\Z,\\Q,\\R,\\C,\\F,\\ell。不能假定更多自造宏存在，需要者用标准展开式。
- 核心术语用 \\term{key}{中文词}，如下：perverse-sheaf/反常层; sheaf/层; triangulated-category/三角范畴; derived-category/导出范畴; t-structure/$t$-结构; heart/心; intermediate-extension/中间延拓; intersection-cohomology/交叉上同调; intersection-complex/交叉复形; cohomology/上同调; complex/复形; distinguished-triangle/区别三角; stratification/分层; stratum/层片; constructible/可构造; local-system/局部系统; duality/对偶; weight/权; weight-filtration/权滤过; pure/纯; mixed/混合; decomposition-theorem/分解定理; hard-lefschetz/强Lefschetz定理; nearby-cycles/邻近轮换; vanishing-cycles/消失轮换; recollement/粘合; truncation/截断; perverse-cohomology/反常上同调; perversity/反常度; self-dual/自对偶; etale/平展; l-adic/$\\ell$-进; abelian-category/阿贝尔范畴; exact-functor/正合函子; adjunction/伴随; noetherian/诺特; artinian/阿廷; simple-object/单对象; semisimple/半单; monodromy/单值作用; realization-functor/实现函子; filtered-derived-category/滤过导出范畴; support/支撑; cosupport/余支撑; direct-image/正像; inverse-image/逆像; proper/固有; affine/仿射; smooth/光滑; scheme/概形; torsion/挠; filtration/滤过; spectral-sequence/谱序列; homotopy/同伦; cohomological-functor/上同调函子; localization/局部化; extension/扩张; fully-faithful/全忠实; equivalence/等价; finite-type/有限型; injective/内射; projective/投射; nilpotent/幂零; dualizing-complex/对偶化复形。
- 新术语写入自己的 chapters/terms-NN.tsv（key\t中文\tEnglish\tfrançais），不要重复已有key。
- 参考文献的书名/文章名建议中文译名后保留原名；完整出版信息照录。
- 不擅自把原书勘误改进正文，正文忠实原文，明显排印错误可用\\footnote{译注：...}，勘误单独全译。
- 疑点需回看原图解决，不能把[待核]当成完成。确实模糊者在自己的 chapters/notes-NN.md 记录原PDF页、公式编号和理由。

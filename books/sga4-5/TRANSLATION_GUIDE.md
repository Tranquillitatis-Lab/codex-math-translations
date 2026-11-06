# 全书翻译共同约定
用户要求完整中文翻译 SGA4½，允许并行子 Agent。你不是独自工作，不得撤销或改写其他人的文件，只拥有分配的 chapters/*.tex、notes/自己的.md 和必要 figures/自己的前缀文件。持续完成全部分配，不得以梗概代替全文。

## 原文与证据
- 权威底本 SGA4-0.5.pdf（本地底本），320物理页。物理页7=原书1，因此原书页p通常是物理p+6。物理4-5=引言，6=目录，1为空白，请以每页文字实际内容确认：source/pages/NNN.txt。
- source/miller 是 Daniel Miller 法语 LaTeX 转写本的 NomiL/sga4.5 镜像。它存在漏文、错字和公式误写，不得机械信任！原书优先。其交换图可直接保留 xymatrix（矢量重绘），不必转换成 tikzcd。图和公式结构、标签、引用键均保留，不压缩证明。
- 用扫描本文字层辅助逐段对照有无遗漏。公式疑点要渲染原PDF相应页阅读，禁止运行本地OCR模型。命令 /opt/homebrew/bin/pdftoppm -f N -l N -scale-to 1800 -singlefile -png 原PDF source/rendered/自己前缀-N 。用view_image阅读。别渲染整本或运行高负载模型。
- 作者原书章节及公式编号应保留。转写本section通常用阿拉伯数，对应原书的罗马分部号，由主文件统一设置第一篇为罗马显示；不要擅自大改编号机制，保留 \setcounter。
- 第一篇开头转写本漏了原书p4的作者说明和约定，要由1a负责人补回。其余每篇也要注意遗漏的引言、附录、参考文献等。第一篇原书p74-75参考文献由1b负责人完整恢复。各篇末尾参考文献若转写本合并到bib里，仍保留其文献引用，无须自行复写总表，主 Agent 统一整合书目。

## 中文和术语
自然、严谨的数学中文，可调语序但不改变语义，保留所有量词、假设、证明、脚注、引用、公式。\emph 内法语叙述也翻译，数学内部 \text、\mbox 等说明文字译成中文。人名和参考文献题名保留原文，不必汉化。Technical词在括号保留法语，统一用 \term{中文}{English}{français}，主文件会生成所有正文出现位置与术语表的双向链接。请在首现和定义处显式标记，重复出现可写普通中文，主 Agent 会自动链接全文同词。
优先译名：概形schéma，层faisceau，预层préfaisceau，平展étale，平展上同调cohomologie étale，拟紧quasi-compact，拟分离quasi-séparé，约化réduit，正规normal，正则régulier，下降descente，下降资料donnée de descente，栈champ，挠层faisceau de torsion，可构造层faisceau constructible，有限型de type fini，紧支撑上同调cohomologie à supports compacts，自身态射endomorphisme，自同构automorphisme，忠实平坦fidèlement plat，固有propre，光滑lisse，逆极限limite projective，滤过归纳极限limite inductive filtrante，泛点point générique，几何点point géométrique，茎fibre（上下文分辨fibres纤维），扭子torseur，导出范畴catégorie dérivée，三角范畴catégorie triangulée，同调平移translation，截断troncature，Tate扭曲torsion de Tate，消灭effacement，分解归约dévissage。

## LaTeX
保留原源的宏和数学环境，主文件提供 sga-style 全部数学宏和原环境。\term 仅放叙述段落不放公式；标题中尽量普通中文，法语术语放正文首段。章节文件不写documentclass/document/package，不改公共文件。
可用 \translatornote{...} 添加数学译者注；只在能给出反例、完整修补条件或论证时指出原文数学疏漏。排印误差修复可另在 notes/自己的.md 记，不要把转写本错误说成原著错误。无法确定就记录疑点，不编造错误。
可用 \origpage{PDF物理页}{原书页码} 在每个能可靠定位的节开始标明原页，不必每页都插，不能猜错。
保留原本 amsthm 环境：theorem、lemma、proposition、corollary、definition及带_或*的变体，主文件统一中文名称。证明用proof。
不单独编译、不跑验证脚本。只完成翻译与必要的辨认。完工汇报覆盖范围、文件、疑点或补回内容。

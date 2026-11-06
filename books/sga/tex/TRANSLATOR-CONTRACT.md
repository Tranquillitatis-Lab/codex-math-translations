# 翻译文件接口

只处理父 Agent 指定的一个块。其他 Agent 同时工作，勿还原、覆盖其文件。

## 交付

- `volumes/<volume>/chunks/<chunk>.tex`：完整译文，仅正文。
- `glossary/<volume>-<chunk>.tex`：该块术语声明。
- `reports/<volume>-<chunk>.json`：实际完整翻译的 PDF 页码范围、原页图像核读情况、疑点；用 `complete` / `partial` 明示。
- 工作图像等放 `work/<volume>-<chunk>/`。
- 向父 Agent 的完成交付只在 final 中简报一次，列文件、页段、状态和源缺数；不要先 send_message 重复全文完成消息，再复制一遍 final。

## TeX 接口

```tex
\SGAchapter{I}{平展态射}{Morphismes étales}
\SourcePage{17}
\SGAsection{1}{微分计算的概念}
正文中的\Term{prescheme}{预概形}。
\begin{SGAresult}{命题}{2.1}
内容，保留原编号。证明写在环境之外。
\end{SGAresult}
\begin{proof}证明。\end{proof}
```

- 章节不使用 LaTeX 自动编号；原书编号由上面接口传入。
- `\SourcePage{N}` 标注每一原 PDF 页起点；如果原文跨页断句，不必截断译文段落，在相邻自然位置标注。
- 段内可用 `\textbf{注记。}`、`\textbf{定义 3.2。}`，但命题定义优先用 SGAresult。
- 公式使用 amsmath / amssymb，交换图使用 tikz-cd；不加载个人宏包。不依赖原书的未定义宏。
- TeX 控制词与紧随的中文之间加空格或空组，例如 `\endgroup 中文`；平展上同调的 ét 下标用 `\text{ét}`，避免旧字体重音编码在 XeLaTeX 中丢字。书写体可用 `\mathscr`（共享模板已加载 mathrsfs）。
- 常用算子可用 `\operatorname{Spec}`、`\operatorname{Hom}`、`\operatorname{Ext}` 等。
- 方程编号用 `\tag{4.1}`；非编号公式用 `\[...\]`。
- tikz-cd 节点若以方括号开头，整个节点须包入花括号，例如 `{[X\mid Y]_n}`，避免把节点内容解析为绘图选项。
- tikz-cd 箭头标签含逗号时须整体加花括号，如 `"{f(x,y)}"`。如把 tikz-cd 放进 resizebox 等宏的参数，使用 `ampersand replacement=\&`，并以 `\&` 分列，避免矩阵符号的类别码错误。
- 跨篇引用先完整保留文本编号，如“第 I 讲 5.8”；内部标签用卷号和讲号前缀，不能假造已存在的引用目标。
- 术语声明格式：`\DeclareSGATerm{prescheme}{预概形}{prescheme}{préschéma}`。正文用 `\Term{prescheme}{预概形}`；同一术语不同语法形式可改变第二参数。标记术语每次实际技术用法，不能只标首次；普通语言不标（如“适当的选择”“容易/平凡地验证”不能链接到固有态射或平凡丛）。不要盲目做全局子串替换。
- 不在标题、目录或数学模式中用 Term；可在标题下首次正文标记。
- 原书索引另建独立正文模块，文件名中包含 `index`；索引词头不再使用 Term，以免正文用例回链混入索引自身。原书目录可由中文标题与译本页码重建，并在报告记录原目录页段。
- 保留撇号、下标、上标、箭头方向、全部假设、否定、脚注和编者补充。译文应流畅，但不得修订原著数学结论。
- 不可识别符号先看原页；仍无法辨认时写 `\SGAunclear{说明}` 并在报告登记，不以猜测替代。
- 用户新决定：原书与现有补源均无法补足的缺字、缺句、缺公式或缺引注，写 `\SGAsourcegap{具体说明}`，并登记 `source_gaps`（PDF页码、讲/节、前后文、证据）。不再额外研究重建；可读内容全译且缺失已登记即可 complete。全部译完后由主 Agent 汇总缺失报告交用户找源。
- 术语候选优先：schéma 概形，préschéma 预概形，étale 平展，lisse 光滑，non ramifié 非分歧，faisceau 层，quasi-cohérent 拟凝聚，cohérent 凝聚，fidèlement plat 忠实平坦，descente 下降，revêtement 覆盖，radiciel 根性，net 净（原文旧称，与非分歧并用），topos 拓扑斯。
- 已统一：proper 固有（普通语言 convenable 仍是适当）；champ 叠，gerbe 凝集；trait 离散赋值环谱；parafactoriel 旁析因；cycles évanescents 消失圈，cycles proches 邻近圈，monodromie 单值性，groupe de monodromie 单值群，biextension 双扩张，pinceau de Lefschetz 为 Lefschetz 铅笔。陌生词首次括注原文。
- 作者用语 respé/respée 指由 resp. 引出的相应版本，通常译“括号中的相应情形/形式”；结合上下文处理，不能因不是常用词而直接标作排印错误。
- 拓扑斯术语沿用：site 景，crible 筛，pré-topologie 预拓扑，topos 拓扑斯，catégorie fibrée 纤维范畴，foncteur conservatif 保守函子。
- SGA 6 术语沿用：complexe parfait 完美复形（perfect-complex），strictement parfait 严格完美（strictly-perfect），amplitude parfaite 完美振幅（perfect-amplitude），dimension parfaite 完美维数（perfect-dimension），tor-dimension Tor 维数（tor-dimension）。
- 不做测试或编译；由父 Agent 统一集成编译。

## 来源

原 PDF 在上级 `SGA/`。`sources/<volume>/pages.jsonl` 按一行一页提供 `pdf_page` 和 `text`；也有 `full.txt`。数学排版丢失之处用 `fitz` 把原 PDF 指定页输出 PNG，再 `view_image` 阅读。不要仅据 OCR 重建疑难公式。

# 全书术语一致性建议

仅产出 terminology-canonical.json 和本记录；未改任何正文。读取的是各篇正在写入中的版本，未编译、测试或作数学审计。

## 可采用的统一

JSON 中的 replacements 是在实际叙述中确认同义的译法或排版统一：

- 换基→基变换。第一篇后半多用“换基”，其他篇用“基变换”。二者在所见上下文均指 changement de base。
- 特殊化→特化，余特殊化→余特化。统一第一篇、第六篇与第七篇。
- 笛卡儿图、Cartesian 图→笛卡尔图。英法词头为 Cartesian diagram / diagramme cartésien。
- 正像、直接像→直像；高阶正像→高阶直像。保留“逆像”的原译。
- 整体截面→全局截面；解消→消解；局部双重对偶→局部双对偶。
- 代数循环→代数闭链。只替换完整的“代数循环”，不对“循环”作全局替换。
- 特征线→离散赋值环谱；严格局部特征线→严格局部离散赋值环谱。这里均指 trait，而非微分方程意义的特征线。第一篇的部分标注已在读取过程中改为“离散赋值环谱”，因此采用该译法统一。
- 有限Tor维数、严格Hensel化、Yoneda积补拉丁词与汉字间空格。
- 开嵌入、闭嵌入→开浸入、闭浸入。只替换这两个明确的 immersion 短语，不全局改变“嵌入”。

建议对 replacements 按旧词长度从长到短处理，避免部分匹配。含英文空格的几项是排版统一；不宜令“高阶直像层”等派生词在已有\term内部再产生嵌套标注。

## 必须按标注上下文单独处理

第一篇后半曾有 \term{投射对象}{pro-object}{pro-objet}，建议只把这一条宏的中文改为“pro-对象”，保留法语 pro-objet。JSON 的 terms 中给出其词头，但 replacements 刻意不含“投射对象→pro-对象”。第八篇的“投射对象”指 projective object，必须保留。第二篇也已经用“pro-对象”说明 pro-层。

“特化态射”在第七篇标为 flèche de spécialisation，在其他篇标为 morphisme de spécialisation；两者在这里同义。术语表建议合并到 morphisme de spécialisation，正文括注若希望严格保留具体原用词，可继续显示 flèche。余特化的 flèche / morphisme 同理。

“摩天楼层”的两个法文标注 faisceau gratte-ciel、faisceau en gratte-ciel 在这里指同一层，可统一术语表词头为 faisceau gratte-ciel。

## 不宜强行合并

- “分裂”对应 scinder / scindé，“分解”可能对应 factorisation、décomposition 或 résolution，不能因中文近似统一。
- “无环”与“无上同调”在本书具体语境常对应 acyclique，但对态射使用“局部无环”，对相对于函子的对象使用“无上同调”；不全局互换。
- “单复形”是 complexe simple 的历史译法，第八篇译者注中也用现代名称“总复形”。无需把所有“单”机械改成“总”，更不能与单纯复形混淆。
- “固有支撑上同调”与“紧支撑上同调”在本文的相应结构态射下由同一 f! 形式体系给出，但分别忠实对应 cohomologie à support propre、cohomologie à supports compacts；术语表可互释，不必抹去法文词头差别。
- “局部无环”“强局部无环”“普遍局部无环”各有不同条件，保留。
- “严格局部化”与“严格 Hensel 化”密切相关，但一个强调局部化对象或过程，另一个强调环的 Hensel 化，保留上下文区别。
- 第四篇的 poids 可指赋予闭链的复形或重数资料，第六篇的 poids 指 Weil 权；同一个法语词存在不同语境，术语表不应把释义限死为其中一种。
- 第七篇已通过译者注明确区分附近循环与现代消失循环；不按法语 cycles évanescents 的字面把它们合并。

## 词形

JSON 的英法词头尽量使用常见单数形式。理论本身惯用复数的词（如 coinvariants、cohomology with compact supports）无需机械改为不自然的单数。屈折形和原句语法用法可保留在正文括注，词表条目则可采用词典形式。

# Codex Math Translations

用 Codex 自动化翻译经典法语数学文献的尝试。

从 Grothendieck 的代数几何讨论班，到平展上同调、反常层和自守形式，我们尝试把扫描本或已有转写本整理成可持续编辑的中文 XeLaTeX 工程：保留数学细节，重排公式与交换图，提供适合长时间阅读的版式，并用术语表连接中文、英语与法语。项目也收录相关英文文献及英法混合文集。

这个仓库合并了此前分别维护的七个翻译项目，统一保存译稿、正式 PDF、术语数据、翻译规范和仍有价值的疑点记录。

## 书目与阅读

| 项目 | 中文 PDF | 可编辑工程与记录 |
| --- | --- | --- |
| SGA 1–7 | [12 个分册](books/sga/output/pdf/) | [工程](books/sga/) · [补源清单](books/sga/reports/missing-content.json) |
| SGA 4½《平展上同调》 | [中文译本](books/sga4-5/output/pdf/SGA4.5-平展上同调-中文全译本.pdf) | [工程](books/sga4-5/) · [疑点与补注](books/sga4-5/notes/) |
| FGA《代数几何基础》 | [中文译本](books/fga/output/pdf/FGA-代数几何基础-中文译本.pdf) | [工程](books/fga/) · [疑点与补注](books/fga/notes/) |
| Arithmetic Algebraic Geometry，LNM 1553 | [译者补注版](books/arithmetic-algebraic-geometry/output/pdf/arithmetic-algebraic-geometry-zh-annotated.pdf) | [工程](books/arithmetic-algebraic-geometry/) · [29 项补注](books/arithmetic-algebraic-geometry/translator-notes.tex) |
| 《自守形式、表示与 L 函数》两册合订 | [中文合订本](books/automorphic-forms/output/pdf/自守形式、表示与L函数-中文合订本.pdf) | [工程](books/automorphic-forms/) · [逐篇记录](books/automorphic-forms/notes/) |
| 《函子代数几何导论》第一卷：仿射代数几何 | [中文译本](books/functorial-algebraic-geometry/函子代数几何导论·第一卷·中文译本.pdf) | [工程](books/functorial-algebraic-geometry/) |
| Faisceaux pervers《反常层》 | [中文译本](books/faisceaux-pervers/output/pdf/反常层-中文译本.pdf) | [工程](books/faisceaux-pervers/) · [逐章记录](books/faisceaux-pervers/chapters/) |

截至本次归并，SGA 的十二册译稿与分册 PDF 已有交付；总本的最终交付流程在原会话中中断，当前仓库保留总入口 `main-all.tex`，尚无正式总本 PDF，也尚无排版后的缺失内容报告。机器可读补源清单已有 **75 条记录**，其中包含原书编者明示待补的内容；不能把这些都理解为扫描漏页。

《自守形式、表示与 L 函数》第二册原第 295 页已由用户补图，译文和重绘树图已编入 Ihara 一文，补图一并保留。

## 我们遇到了哪些 Gap

翻译过程暴露的问题不只在语言转换。扫描本、OCR 和法语转写源可能漏掉假设、上下标、引注甚至整段文字；数学原文的陈述、证明范围和旧术语也需要分别辨认。

以下按已有译注记录举例，详细反例、修补条件和原页定位见 [Gap 记录](docs/gaps.md)。

- **证明覆盖范围不足**：LNM 1553 第一篇定理 6.4 的陈述包含正特征，而书中论证对初级挠元及指数有界性的处理未覆盖全部正特征情形。已有补注把这明确列为证明范围缺口。
- **遗漏假设**：FGA 的一个商构造段落从环层正合性直接推出商的性质；译注以 `P¹ → Spec k` 的平凡等价关系说明问题，并提出补充仿射性后的逐片论证。
- **公式不能仅凭 OCR**：SGA 4½ 的迹公式有遗漏紧支撑下标的记录；普通上同调与紧支撑上同调会产生不同的迹，排印上的小差异有数学后果。
- **“修正”也需要证据**：原著勘误、转写错误、新增数学补注和原文缺损分开记录。FGA 的作者评论不被包装成自动翻译的新发现；SGA 无法补足的字词按既定约定保留标记，等待补源。

## 当前使用的提示词与工作方式

[提示词](docs/prompts.md)整理了历次实际请求及后续纠正，包括全文忠实性、自然中文、原页识读、术语互链、XeLaTeX 排版和数学译注。它是当前可复用的整理版，原会话中的关键要求与变化见 [会话沿革](docs/history.md)。

基本流程是：读取底本与目录 → 按连续语义分块 → 逐段译写并保留原页定位 → 汇总术语与疑点 → 生成分册或合订 PDF。获准并行时，由主 Agent 直接收发译稿，每个新会话只负责一个几十页的语义块；不设置协调 Agent，也不让同一会话不断追加分块、反复压缩上下文。

数学图优先用 TikZ / tikz-cd 重绘。正文中每个术语标注位置建立独立锚点，书末词条可分别返回各次出现处；不同书的实现沿用各自已有宏和构建脚本。

## 编辑与构建

仓库使用 Python 3 和现有 TeX Live / XeLaTeX 环境，不另建一套排版依赖。字体及个别可执行文件路径沿用各书原配置，跨系统使用时参看 [构建说明](docs/build.md)。

从仓库根目录选择一本书：

```sh
python3 tools/build.py fga
python3 tools/build.py sga4-5
python3 tools/build.py sga sga3-2
python3 tools/build.py sga all
```

只编辑 `books/<项目>/` 下的正文、样式和术语源数据。`generated/`、`build/` 和 `work/` 是可重建目录，不提交。原 PDF 通常不参与中文译本编译；补取原文或生成带原页图的缺失报告时，再按 [来源说明](docs/sources.md)配置底本。

## 仓库维护

正式 PDF 与必要插图随源码保留，方便直接阅读。重复源码 ZIP、逐页渲染、OCR 缓存、编译日志及中间文件已清理；小体积的数学疑点、译注依据、补页图和覆盖记录继续维护。归并清理记录见 [migration.json](docs/migration.json)。

本次归并没有重新编译或重新审定既有译文。历史版本和未完成交付文件留在本地 `.local/` 归档，该目录不进入 Git。原文和第三方转写材料保留各自作者、出版与来源信息；本仓库未对它们另行授予统一许可。

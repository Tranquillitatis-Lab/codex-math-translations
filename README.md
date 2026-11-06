# Codex Math Translations

用 Codex 自动化翻译经典法语数学文献的尝试。

> [!WARNING]
> **Vibe coding 警告：这些文档目前尚未经人类仔细核对。** 译文、公式、术语表、图表和数学补注主要由 Codex 自动生成，可能存在漏译、误译、符号误识，以及对数学 Gap 的错误判断或修补。生成 PDF、编译通过或附有反例，都不等于完成数学审校；使用或引用前请对照原文核查。

从 Grothendieck 的代数几何讨论班，到平展上同调、反常层和自守形式，我们尝试把扫描本或已有转写本整理成可持续编辑的中文 XeLaTeX 工程：保留数学细节，重排公式与交换图，提供适合长时间阅读的版式，并用术语表连接中文、英语与法语。项目也收录相关英文文献及英法混合文集。

这个仓库合并了此前分别维护的七个翻译项目，统一保存译稿、PDF、术语数据、翻译提示词原文和仍有价值的疑点记录。

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

SGA 的机器可读补源清单保留 **75 条记录**，其中包含原书编者明示待补的内容，和扫描文件的缺字、缺引注分别登记。


## 自动化任务中的理解与行为偏差

这些项目也记录了 Codex 对任务要求的理解偏差，以及用户如何在运行中修正它的行为：

| 用户意图 | Codex 的偏差或实际问题 | 后续修正 |
| --- | --- | --- |
| 用子 Agent 并行翻译，按几十页的连续语义块分工 | 额外引入四个协调 Agent，消耗 token 并占用翻译并发位 | 用户明确拒绝多级调度；撤掉协调层，由主 Agent 直接派发、接收和集成译稿 |
| 自动完成翻译，同时控制本机资源使用 | FGA 任务启动了本地 GLM-OCR；负责 OCR 的子 Agent 结束后，模型进程仍在运行 | 用户提出停止要求后，终止进程并卸载模型；后续提示词明确加入不运行本地高占用 OCR 模型的限制 |
| 忠实翻译现有原文，并能追溯来源 | SGA 的源缺字曾按上下文推定补写，使推断进入译文 | 用户选择按原文缺失处理后，撤回推补，保留缺失标记及定位，交由用户寻找补源 |
| 在仓库中保留实际使用过的提示词 | 本仓库初版把历次请求重写成一份“整理版”提示词 | 按用户纠正改为分项目逐字保留真实提示词，后续纠正另列 |

这些修正来自具体运行中的反馈，不能倒写成初始提示词已包含的要求。原话、行为记录和修正经过见 [自动化偏差与修正](docs/history.md)。

## 译稿中记录的数学 Gap

翻译过程暴露的问题不只在语言转换。扫描本、OCR 和法语转写源可能漏掉假设、上下标、引注甚至整段文字；数学原文的陈述、证明范围和旧术语也需要分别辨认。

以下是现有自动生成译注记录的疑点，尚未经人类仔细核对，不应据此认定原著确有错误。具体反例、修补条件和原页定位见 [Gap 记录](docs/gaps.md)。

- **证明覆盖范围不足**：LNM 1553 第一篇定理 6.4 的陈述包含正特征，而书中论证对初级挠元及指数有界性的处理未覆盖全部正特征情形。已有补注把这明确列为证明范围缺口。
- **遗漏假设**：FGA 的一个商构造段落从环层正合性直接推出商的性质；译注以 `P¹ → Spec k` 的平凡等价关系说明问题，并提出补充仿射性后的逐片论证。
- **公式不能仅凭 OCR**：SGA 4½ 的迹公式有遗漏紧支撑下标的记录；普通上同调与紧支撑上同调会产生不同的迹，排印上的小差异有数学后果。
- **“修正”也需要证据**：原著勘误、转写错误、新增数学补注和原文缺损分开记录。FGA 的作者评论不被包装成自动翻译的新发现；SGA 无法补足的字词按既定约定保留标记，等待补源。

## 实际使用的提示词与工作方式

[真实提示词原文](docs/prompts.md)分别保留七个项目中用户实际发送的请求，以及运行中追加的纠正，保留原有措辞、标点和段落，只省去附件路径及界面包装。它们没有被合成为一条新提示词。实际行为和用户要求之间的偏差见 [自动化偏差与修正](docs/history.md)。

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

本次归并没有重新编译或重新审定既有译文。历史快照留在本地 `.local/` 归档，该目录不进入 Git。原文和第三方转写材料保留各自作者、出版与来源信息；本仓库未对它们另行授予统一许可。

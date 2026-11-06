# 底本与辅助来源

各书卷首、README、原页标记和清单保留底本信息。原 PDF 不随本次合并重复导入；编译现有中文正文通常不需要原 PDF。

- SGA 原书共十二个 PDF，文件名、册号和页数见 [manifest.json](../books/sga/sources/manifest.json)。读取原书时设置 `SGA_SOURCE_DIR`；默认使用本地 `.local/originals/sga`，该路径不提交。
- SGA 4½ 底本为 LNM 569（1977）。保留 Daniel Miller 的法语 LaTeX 辅助转写，来源为 [NomiL/sga4.5](https://github.com/NomiL/sga4.5)，所在目录为 `books/sga4-5/source/miller/`。转写有遗漏，译稿与疑点记录使用扫描本作比较；辅助转写原有的 Git 元数据不作为嵌套仓库提交。
- FGA 为 1962 年汇编，包含八篇 Bourbaki 报告和作者评论、勘误。书前作者更正与新增译者注分别保留。
- Arithmetic Algebraic Geometry 为 LNM 1553（1993），所给底本另有第一篇 2008 年勘误；新增 29 项补注所依据的说明保存在 `annotations/received-corrections-2026-11-05.txt`。
- 自守形式文集为 PSPM 33 两册（1979）；第 295 页的用户补图保存在 `source-supplements/`。重提取原文时设置 `AUTOMORPHIC_SOURCE_DIR` 为两册 PDF 所在目录，文件名见 `volume-1-pages.json`、`volume-2-pages.json`。
- 函子代数几何导论为 Grothendieck 讲授、Federico Gaeta 笔记的第一卷仿射代数几何。
- 反常层底本为 Astérisque 100 的 2018 年再版，含 1982 年正文及再版新增材料，共 192 个 PDF 物理页。`source/pages.json` 保留原页定位。

## 曾用于 SGA 核读的可下载补源

以下是原会话中的下载地址，供需要时恢复补源文件。大体积下载副本已清理，定位记录仍在各块报告中。

| 原缓存文件 | 来源 |
| --- | --- |
| `SLMath-SGA4-1.pdf` | [SLMath SGA 4 第一册](https://library.slmath.org/nonmsri/sga/sga/pdf/sga4-1.pdf) |
| `SLMath-SGA4-2.pdf` | [SLMath SGA 4 第二册](https://library.slmath.org/nonmsri/sga/sga/pdf/sga4-2.pdf) |
| `SLMath-SGA4-3.pdf` | [SLMath SGA 4 第三册](https://library.slmath.org/nonmsri/sga/sga/pdf/sga4-3.pdf) |
| `IAS-Number12.pdf` | [IAS Number 12](https://publications.ias.edu/sites/default/files/Number12.pdf)；[作者页面](https://publications.ias.edu/node/358) |

来源不够明确的旧扫描副本和独有历史快照保存在本地 `.local/archive/`，未当作可再生缓存删除。所有缺失补源的数学位置仍以原书 PDF 页码及报告中的上下文为准。

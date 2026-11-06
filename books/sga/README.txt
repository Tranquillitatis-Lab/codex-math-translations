SGA 中文全译工程

原书共12册、5146个PDF页面。交付目标：12个独立分册PDF、1个正文汇编总PDF、1份缺失内容报告，并附模块化XeLaTeX源文件。

目录：
sources/       逐页文本层和原书清单。原书PDF仍位于本目录的上一级，不修改。
volumes/       每册独立main.tex和分块正文；正文由分册与总本共同引用。
tex/           共享版式、封面、数学环境、术语链接接口。
glossary/      分块术语和整合后的三语术语库。
reports/       每个语义块的实际进度、原页核读记录及疑点。
tools/         提取、编译输入生成与编译工具。
work/          原页图像及其他工作中间件。
output/pdf/    PDF交付目录。未完成的输出文件名必须含“阶段稿”。

当前状态以 sources/manifest.json 和 reports/ 下逐块报告为准。文本层提取完成不代表翻译完成。

版式：190×260毫米，中文宋体，西文Pagella；深蓝、青蓝与暖金配色；封面使用覆盖空间与纤维主题的TikZ图形。正文边注给出原PDF页码。

术语：正文每次使用Term宏都创建唯一位置锚点，并链接至当前册末的词条；词条给出中英法名称和所有出现位置回链。总本为每册使用独立目标前缀，避免不同册的同名术语互相串跳。

翻译：按语义连续的几十页块分配，每个子Agent只翻译一个块，结束后使用新session。保留原著假设、公式、编号、脚注、编者增补和文献，不擅自纠正数学疑点。扫描本OCR仅作阅读辅助，疑难符号以原页图像为准。

原文残缺：依用户决定，现有原书和补源均缺失的文字、条件、公式或引注，在正文用“〔原文缺失〕”标记，不据推断重建。全套翻译结束后，reports/missing-content.json 及 output/pdf/缺失内容报告.pdf 汇集原文件名、PDF页码、讲次、译文位置和原页图像，供用户寻找可补文本。已从现有原扫描明确恢复的内容另记在对应分块报告中。

编译入口：
  /opt/anaconda3/bin/python tools/build.py sga1
  /opt/anaconda3/bin/python tools/build.py sga3-2 --draft
  /opt/anaconda3/bin/python tools/build.py all --draft

以上 --draft 仅用于有明确进度说明的阶段稿。相应册目完整后去掉 --draft。
build.py 从工程根目录调用 latexmk 的 XeLaTeX 模式，自动完成目录和交叉引用所需的多遍编译。
如直接使用分册 main.tex，工作目录也须设为整个“中文译本”工程根目录。
只将 status=complete 的分块收入编译，以免读到译者尚在写入的文件。

全套译稿齐备后的最终交付批次：
  /opt/anaconda3/bin/python tools/deliver.py
此入口依次生成12个分册、总本及缺失内容报告；编译日志位于 work/delivery-logs/，交付文件清单位于 output/deliverables.json。
总本包含大量位置锚点，build.py 会仅在总本编译进程中调高 XeLaTeX 的内存、字符串池和哈希容量。建议使用上述脚本入口编译总本。

2026-11-06 合并状态：十二个分册 PDF 均在 output/pdf；总本最终交付与缺失报告 PDF 尚未生成。中断时生成的总本 PDF 仅留本地归档，不列为正式交付。reports/missing-content.json 保留75条补源记录。
清理后 work、逐页文字缓存和可下载补源扫描本已移除，正文与分块报告仍可直接用于编译。原 PDF 读取由 SGA_SOURCE_DIR 指定；普通中文译本编译不需要原 PDF，带原图的缺失报告和重新提取文本需要原 PDF。

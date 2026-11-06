《反常层》中文全译本

底本
A. A. Beilinson、J. Bernstein、P. Deligne、O. Gabber，Faisceaux pervers，
Astérisque 100，法国数学会2018年再版（1982年正文及再版新增材料）。
所提供底本共192个PDF物理页，含空白页；全书内容均纳入译稿。

交付内容
1. 反常层-中文译本.pdf：192页，含几何主题矢量封面、全部正文和证明、
   原参考文献及索引、2018年附录、100条勘误与增补、新增参考文献。
2. 中—英—法技术名词对照表：135个词条，约3700处正文术语链接。
   点击正文术语可跳到词条；点击词条下任一页码，可返回对应出现位置。
   同页的多次出现分别保留链接。罗马页码对应卷首部分。
3. 全部交换图以TikZ/tikz-cd重绘；封面由TikZ绘制，可无损缩放。
4. XeLaTeX源文件、术语数据和编译脚本。

阅读与编号
正文沿用原书的定义、命题、公式及引用编号，译本重新分页。
两个原版目录的页码照录，供查阅原版；译本目录使用译本页码。
勘误中的页码、正/负行号依原书说明保留。
明确的原版勘误和原文记号问题在相应处加译注；勘误单独完整翻译，
未以无说明的方式改写原文。
每个源页在译稿中用 \SourcePage{N} 标识，N为底本PDF的物理页序号。
源文件随附的 source/pages.json 可用于回查底本位置。

工程结构
main.tex                         全书入口
style/book.sty                   版式、数学宏、术语双向链接
style/cover.tex                  矢量封面
style/terms-core.tsv             核心术语的中英法对照
style/glossary-entries.tex       自动生成的词条
chapters/*.tex                  各部分中文译稿
chapters/terms-*.tsv             各章补充术语
chapters/notes-*.md              原文公式、符号及引用问题的处理记录
tools/prepare.py                术语合并与正文链接生成
tools/layout.py                 交换图标签、公式换行等排版处理
source/translation-manifest.json 源页覆盖和术语数量记录
build.sh                        编译入口

本机编译
在工程目录执行：
    ./build.sh

脚本汇总术语后运行三遍XeLaTeX，使目录、页码及所有返回链接稳定。
输出位于 output/pdf/反常层-中文译本.pdf。
本机使用TeX Live 2025。字体为TeX Live自带的Fandol、TeX Gyre Pagella、
TeX Gyre Heros及newpx数学字体。Python脚本仅用标准库；优先沿用本机
Conda Python，也可使用系统python3。

源文件已包含术语标记及词条，亦可直接运行三遍：
    xelatex main.tex

修改正文后建议通过build.sh重新生成术语链接。新增词条请在对应TSV中
添加key、中文、英文、法文四列，并在正文使用 \term{key}{显示文字}。

制作日期：2026年11月6日。
本次采用PDF既有文字层与逐页原图人工式识读，没有运行本地OCR模型。

2026-11-06 合并清理：已删除 source/pages、source/text 和 output/pdf 中的预览、日志、辅助文件与重复 ZIP；原页清单、译注和正式 PDF 保留。旧的未链接译稿仅在仓库外的本地归档中保留。

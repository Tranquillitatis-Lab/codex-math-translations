from source_paths import SOURCE_DIR
"""Build the final source-gap handoff report with original-page context."""
from pathlib import Path
from collections import defaultdict
import json
import os
import subprocess
import sys
import fitz

ROOT=Path(__file__).resolve().parents[1]
subprocess.run([sys.executable,str(ROOT/'tools/collect_gaps.py')],check=True)
data=json.loads((ROOT/'reports/missing-content.json').read_text())
manifest={v['id']:v for v in json.loads((ROOT/'sources/manifest.json').read_text())}

def tex(value):
    table={'\\':r'\textbackslash{}','{':r'\{','}':r'\}','%':r'\%','&':r'\&',
           '$':r'\$','#':r'\#','_':r'\_','^':r'\textasciicircum{}','~':r'\textasciitilde{}'}
    return ''.join(table.get(c,c) for c in str(value)).replace('\n',' ')

groups=defaultdict(list)
for gap in data['gaps']:groups[(gap['volume'],gap['pdf_page'])].append(gap)
evidence=ROOT/'reports/evidence';evidence.mkdir(exist_ok=True)
body=[r'\input{tex/preamble.tex}',r'\begin{document}',
 r'\SGAcover{SGA 1—7}{缺失内容报告}{Source lacunae and missing references}{原文定位与补源清单}',
 r'\frontmatter',r'\SGAfrontchapter{使用说明}',
 '本报告汇总译文保留的原书缺字、缺句、缺公式和缺引注，供后续寻找可补文本。',
 '“PDF页码”指用户所给原文件的页面序号，从1开始计数。每组列明缺失说明、译文位置，并附原页图像作为上下文。',
 '已从现有扫描恢复的内容记在各翻译块报告中；本清单列出尚待补足的源内容。',
 '“原书编者明示待补”指编者自己指出尚未补全的引注或论证细节，并不表示扫描漏页。其他项目请依各条说明判断所需补源。',
 f'当前清单共 {len(data["gaps"])} 处，分布于 {len(groups)} 个原PDF页面。',
 r'\tableofcontents',r'\mainmatter']
current=None
for (volume,page),gaps in sorted(groups.items()):
    if volume!=current:
        body.append(r'\SGAfrontchapter{'+tex(manifest[volume]['series'])+'}')
        current=volume
    title=tex(manifest[volume]['source'])+'，PDF第'+str(page)+'页'
    body.append(r'\section*{'+title+'}')
    body.append(r'\addcontentsline{toc}{section}{'+title+'}')
    for gap in gaps:
        body.append(r'\noindent\textbf{'+tex(gap['id'])+r'}\par')
        body.append('讲次：'+tex(gap.get('chapter','详原页'))+r'。\par')
        body.append('类型：'+tex(gap.get('kind_zh','原文缺失（详说明）'))+r'。\par')
        body.append(tex(gap['description'])+r'\par')
        body.append(r'{\footnotesize 译文：\texttt{'+tex(gap['translation_file'])+'}，第'+str(gap['translation_line'])+r'行。\par}')
        body.append(r'{\footnotesize 分块报告：\texttt{'+tex(gap['chunk_report'])+r'}。\par}\smallskip')
    if page:
        image_path=evidence/f'{volume}-pdf-{page}.png'
        document=fitz.open(SOURCE_DIR/manifest[volume]['source'])
        document[page-1].get_pixmap(matrix=fitz.Matrix(2,2)).save(image_path)
        document.close()
        body.append(r'\noindent\includegraphics[width=\linewidth,height=.68\textheight,keepaspectratio]{'+str(image_path.relative_to(ROOT))+'}')
    body.append(r'\clearpage')
body.append(r'\end{document}')
(ROOT/'main-missing.tex').write_text('\n'.join(body)+'\n')
out=ROOT/'work/build/missing-report';out.mkdir(parents=True,exist_ok=True)
env=os.environ.copy();env['PATH']='/Library/TeX/texbin:'+env.get('PATH','')
subprocess.run(['/Library/TeX/texbin/latexmk','-xelatex','-interaction=nonstopmode','-halt-on-error',
                '-file-line-error',f'-outdir={out}','-jobname=缺失内容报告','main-missing.tex'],
               cwd=ROOT,env=env,check=True)
dest=ROOT/'output/pdf/缺失内容报告.pdf'
dest.write_bytes((out/'缺失内容报告.pdf').read_bytes())
print(dest)

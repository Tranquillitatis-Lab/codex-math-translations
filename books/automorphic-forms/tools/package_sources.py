"""Package the editable XeLaTeX book, source text, and user-supplied supplement."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
P=Path(__file__).resolve().parents[1]
output=P/'output'/'自守形式、表示与L函数-中文合订本-XeLaTeX源码.zip'
rootfiles=['main.tex','preamble.tex','frontmatter.tex','publication-note.tex',
           'author-index.tex','terminology.tex','Makefile','.latexmkrc','README.md',
           'TRANSLATION.md','articles.json','volume-1-pages.json','volume-2-pages.json']
folders=['chapters','figures','source-supplements','source-text']
output.parent.mkdir(parents=True, exist_ok=True)
with ZipFile(output,'w',ZIP_DEFLATED,compresslevel=7) as z:
 for name in rootfiles:
  f=P/name
  z.write(f,'automorphic-zh/'+name)
 for name in folders:
  for f in sorted((P/name).rglob('*')):
   if f.is_file():z.write(f,'automorphic-zh/'+str(f.relative_to(P)))
 for f in sorted((P/'notes').glob('*-status.md')):
  z.write(f,'automorphic-zh/notes/'+f.name)
# Keep regeneration utilities with the editable project.
with ZipFile(output,'a',ZIP_DEFLATED,compresslevel=7) as z:
 for f in sorted((P/'tools').glob('*.py')):
  z.write(f,'automorphic-zh/tools/'+f.name)
print(output)

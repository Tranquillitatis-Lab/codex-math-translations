from pathlib import Path
import json
P=Path(__file__).resolve().parents[1]
data=json.loads((P/'articles.json').read_text())
parts={1:'约化群与表示',2:'自守形式与自守表示',3:'自守表示与 $L$ 函数',4:'算术代数几何与自守 $L$ 函数'}
lines=[r'\input{preamble.tex}',r'\begin{document}',r'\frontmatter',r'\input{frontmatter.tex}',r'\tableofcontents',r'\mainmatter']
last=None
for e in data:
 if e['part']!=last:
  lines.append(r'\part{'+parts[e['part']]+'}')
  last=e['part']
 lines.extend([r'\def\ArticleKey{article-'+e['id']+'}',r'\input{'+e['file']+'}'])
lines.extend([r'\backmatter',r'\input{author-index.tex}',r'\input{terminology.tex}',r'\end{document}'])
(P/'main.tex').write_text('\n'.join(lines)+'\n')
# The author index lists all contributions directly, including coauthored articles.
authors={
'Arthur, James':['16'],'Borel, A.':['22','12'],'Cartier, P.':['07'],'Casselman, W.':['29'],
'Deligne, Pierre':['34','36'],'Flath, D.':['10'],'Gelbart, Stephen':['18','15'],
'Gérardin, Paul':['08','27'],'Harder, G.':['39'],'Howe, R.':['17','20'],'Ihara, Yasutaka':['35'],
'Jacquet, Hervé':['23','12','15'],'Kazhdan, D. A.':['38','39'],'Knapp, A. W.':['04','05'],
'Koblitz, N.':['37'],'Kottwitz, R.':['26','31'],'Labesse, J.-P.':['27'],
'Langlands, R. P.':['13','33'],'Lusztig, G.':['09'],'Milne, J. S.':['30'],
'Novodvorsky, Mark E.':['24'],'Ogus, A.':['37'],'Piatetski-Shapiro, I.':['11','14','20'],
'Rallis, S.':['19'],'Shelstad, D.':['06','32'],'Shintani, Takuro':['25'],'Springer, T. A.':['01'],
'Tate, J.':['21'],'Tits, J.':['02'],'Tunnell, J.':['28'],'Wallach, Nolan R.':['03'],'Zuckerman, Gregg':['05']}
lookup={e['id']:e for e in data}
def tex(s):
 for a,b in [('₂',r'$_2$'),('₄',r'$_4$')]:s=s.replace(a,b)
 return s.replace('&',r'\&')
index=[r'\chapter*{作者索引（Author Index）}',r'\addcontentsline{toc}{chapter}{作者索引（Author Index）}', '下列页码为本合订译本页码；括号内保留原册号与文章起始页码。合著者均可独立检索。',r'\begin{description}[leftmargin=0pt,labelsep=0pt,style=nextline]']
for name,ids in authors.items():
 index.append(r'\item[\textsf{'+name+'}]')
 for i in ids:
  e=lookup[i]
  index.append(tex(e['title_zh'])+r'\quad\dotfill\quad\pageref{article-'+i+'}'+f'（原第{e["volume"]}册，第{e["printed_start"]}页）'+r'\par')
index.append(r'\end{description}')
(P/'author-index.tex').write_text('\n'.join(index)+'\n')

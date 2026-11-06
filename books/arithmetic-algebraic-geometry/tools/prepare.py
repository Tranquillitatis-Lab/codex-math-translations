#!/usr/bin/env python3
"""从保留原始翻译的 TeX 生成术语链接及中英法对照表。仅使用 Python 标准库。"""
from pathlib import Path
import csv, json, re, unicodedata

ROOT = Path(__file__).resolve().parent.parent
CHUNKS = [
 ('01-colliot-a','fr',6,29), ('02-colliot-b','fr',30,54),
 ('03-kato-a','en',55,82), ('04-kato-b','en',83,110),
 ('05-kato-c','en',111,138), ('06-kato-d','en',139,168),
 ('07-vojta-a','en',169,191), ('08-vojta-b','en',192,213),
]
OUT = ROOT/'generated'
OUT.mkdir(exist_ok=True)

def group(text,pos):
    while pos<len(text) and text[pos].isspace(): pos+=1
    if pos>=len(text) or text[pos]!='{':
        raise ValueError(f'缺少花括号：{text[max(0,pos-30):pos+80]}')
    start=pos+1; depth=1; pos+=1
    while pos<len(text):
        if text[pos]=='\\': pos+=2; continue
        if text[pos]=='{': depth+=1
        elif text[pos]=='}':
            depth-=1
            if depth==0: return text[start:pos],pos+1
        pos+=1
    raise ValueError('未闭合花括号')

def terms(text):
    pos=0
    while (m:=re.search(r'\\term\s*(?=\{)',text[pos:])):
        start=pos+m.start(); cur=pos+m.end(); args=[]
        for _ in range(3):
            arg,cur=group(text,cur); args.append(arg.strip())
        yield start,cur,args
        pos=cur

# 统一分块间同义译名；仅替换明确的中文术语串，不改循环扩张等异义词。
NORMALIZE = {
 'Abel 群':'阿贝尔群', 'Abel 簇':'阿贝尔簇', 'Chern 类':'陈类',
 'Galois 上同调群':'伽罗瓦上同调群', 'Galois 方法':'伽罗瓦方法',
 'Galois 表示':'伽罗瓦表示', 'Tate 扭':'Tate 扭转',
 '分次幂结构':'分幂结构', '调节子映射':'调节映射',
 '代数循环':'代数闭链', '循环类':'闭链类', '循环映射':'闭链映射',
 '零循环':'零闭链', '挠循环':'挠闭链', 'Artin符号':'Artin 符号',
 'Hecke特征':'Hecke 特征', 'PD包络':'PD 包络',
 'zeta 元素':'zeta 元', '泽塔元素':'zeta 元',
}
# Tate 扭转本已规范，故采用最长键、且在目标重复后缀前不再扩展。
normalizer=re.compile('|'.join(map(re.escape,sorted(NORMALIZE,key=len,reverse=True))))
def normalize(text):
    return normalizer.sub(lambda m: m[0] if m[0]=='Tate 扭' and text[m.end():].startswith('转') else NORMALIZE[m[0]],text)
raw={}; entries={}; variants=[]
for name,lang,lo,hi in CHUNKS:
    path=ROOT/'chapters'/f'{name}.tex'
    if not path.exists():
        raise SystemExit(f'缺少译文分块：{path}')
    raw[name]=normalize(path.read_text())
    for start,end,(zh,en,fr) in terms(raw[name]):
        if zh not in entries:
            entries[zh]={'zh':zh,'en':en,'fr':fr,'occurrences':[]}
        elif entries[zh]['en']!=en or entries[zh]['fr']!=fr:
            variants.append({'zh':zh,'first':[entries[zh]['en'],entries[zh]['fr']],'other':[en,fr],'file':name})

# 补充术语译名同样只在正文实际出现的地方布置链接。
for extra_path in sorted(ROOT.glob('terminology-extra*.json')):
    for item in json.loads(extra_path.read_text()):
        zh=normalize(item['zh'])
        if zh not in entries:
            entries[zh]={'zh':zh,'en':item['en'],'fr':item['fr'],'occurrences':[]}

# 中英文排序以检索方便；中文“正文位置”列保留所有出现点。
ordered=sorted(entries.values(),key=lambda t:unicodedata.normalize('NFKD',re.sub(r'\\[A-Za-z]+','',t['en'])).casefold())
for index,item in enumerate(ordered,1): item['id']=f'{index:04d}'

protected_commands={'chapter':1,'section':1,'subsection':1,'subsubsection':1,
 'addcontentsline':3,'label':1,'ref':1,'pageref':1,'hyperref':0,'url':1,'path':1,
 'includegraphics':1,'input':1,'include':1,'hypertarget':2,'hyperlink':2,
 'newcommand':2,'renewcommand':2,'providecommand':2,'chapterauthor':1}
math_envs={'equation','equation*','align','align*','alignat','alignat*','gather','gather*',
 'multline','multline*','displaymath','math','tikzcd','tikzpicture'}
# 单字概念不作字符串扩展，防止误切复合词；显式 \term 仍全部链接。
names=sorted((z for z in entries if len(z)>1 and not any(c in z for c in '{}')),key=len,reverse=True)
match_terms=re.compile('|'.join(map(re.escape,names))) if names else None
counter=0

def linked(zh,lang,original=None):
    global counter
    counter+=1; item=entries[zh]; occ=f'{counter:05d}'
    item['occurrences'].append(occ)
    return f"\\termuse{{{item['id']}}}{{{occ}}}{{{zh}}}{{{original or item[lang]}}}"

def automatic(text,lang,explicit):
    """只在叙述文字中补链；跳过数学、标题、引用目标、图形及注释。"""
    out=[]; i=0; n=len(text)
    while i<n:
        if text[i]=='\x01':
            end=text.index('\x02',i); out.append(linked(explicit[text[i:end+1]][0],lang,explicit[text[i:end+1]][1])); i=end+1; continue
        if text[i]=='%':
            end=text.find('\n',i)
            if end<0: end=n
            out.append(text[i:end]);i=end;continue
        if match_terms and (m:=match_terms.match(text,i)):
            if m.group()=='代数闭' and text[m.end():].startswith('包'):
                out.append(m.group());i=m.end();continue
            out.append(linked(m.group(),lang));i=m.end();continue
        if text[i]=='$' or text.startswith('\\[',i) or text.startswith('\\(',i):
            if text[i]=='$': delim='$$' if text.startswith('$$',i) else '$'; close=delim
            else: delim=text[i:i+2];close='\\]' if delim=='\\[' else '\\)'
            end=text.find(close,i+len(delim))
            end=n if end<0 else end+len(close)
            out.append(text[i:end]);i=end;continue
        if text.startswith('\\begin{',i):
            env,end=group(text,i+6)
            if env in math_envs:
                stop=text.find('\\end{'+env+'}',end)
                end=n if stop<0 else stop+len(env)+6
                out.append(text[i:end]);i=end;continue
        if text[i]=='\\':
            m=re.match(r'\\([A-Za-z]+)\*?',text[i:])
            if m:
                end=i+m.end(); command=m.group(1)
                if command in protected_commands:
                    cur=end
                    while cur<n and text[cur].isspace(): cur+=1
                    if cur<n and text[cur]=='[':
                        stop=text.find(']',cur);cur=(stop+1 if stop>=0 else cur)
                    try:
                        for _ in range(protected_commands[command]): _,cur=group(text,cur)
                        end=cur
                    except ValueError: pass
                out.append(text[i:end]);i=end;continue
            out.append(text[i:i+2]);i+=2;continue
        out.append(text[i]);i+=1
    return ''.join(out)

for name,lang,lo,hi in CHUNKS:
    text=raw[name]; out=[]; last=0; explicit={}
    for index,(start,end,(zh,en,fr)) in enumerate(terms(text)):
        out.append(text[last:start]); key=f'\x01{index}\x02'
        explicit[key]=(zh,fr if lang=='fr' else en); out.append(key);last=end
    out.append(text[last:]); body=automatic(''.join(out),lang,explicit)
    # 标题等受保护命令内的显式术语仍须展开。
    for key,(zh,original) in explicit.items():
        if key in body: body=body.replace(key,linked(zh,lang,original))
    (OUT/f'{name}.tex').write_text(body)

rows=[]
for item in ordered:
    if not item['occurrences']: continue
    links=', '.join(f'\\hyperlink{{termocc-{occ}}}{{\\pageref*{{termocc-{occ}}}}}' for occ in item['occurrences'])
    rows.append(f"\\hypertarget{{term-{item['id']}}}{{{item['zh']}}} & {item['en']} & {item['fr']} & {links} \\\\\n")
header=r'''\chapter*{中英法技术名词对照表}
\addcontentsline{toc}{chapter}{中英法技术名词对照表}
\noindent 按英语词条顺序排列。单击末列页码可返回正文相应位置；同页重复页码分别指向该页不同出现处。词条的中文及括注术语均可点击跳至本表。第三语言译名由译者补充；参考文献题名中的术语不另行标注。
\par\medskip
\begingroup\footnotesize\raggedright
\setlength{\tabcolsep}{4pt}
\renewcommand{\arraystretch}{1.3}
\begin{longtable}{@{}>{\raggedright\arraybackslash}p{.18\linewidth}>{\raggedright\arraybackslash}p{.24\linewidth}>{\raggedright\arraybackslash}p{.25\linewidth}>{\raggedright\arraybackslash}p{.26\linewidth}@{}}
\toprule 中文 & English & Français & 正文位置（译本页码）\\\midrule
\endfirsthead
\multicolumn{4}{l}{\small\color{Muted}中英法技术名词对照表（续）}\\\toprule
中文 & English & Français & 正文位置（译本页码）\\\midrule
\endhead
\midrule\multicolumn{4}{r}{\scriptsize 续下页}\\\endfoot
\bottomrule\endlastfoot
'''
(OUT/'glossary.tex').write_text(header+''.join(rows)+'\\end{longtable}\n\\endgroup\n')
(OUT/'terminology.json').write_text(json.dumps([t for t in ordered if t['occurrences']],ensure_ascii=False,indent=2))
(OUT/'terminology-variants.json').write_text(json.dumps(variants,ensure_ascii=False,indent=2))
with (ROOT/'术语对照表.csv').open('w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f);w.writerow(['中文','English','Français','术语编号','正文出现次数'])
    for item in ordered:
        if not item['occurrences']: continue
        w.writerow([item['zh'],item['en'],item['fr'],item['id'],len(item['occurrences'])])
print(f'已生成 {len(CHUNKS)} 个译文分块，{len(ordered)} 个术语，{counter} 个双向链接位置。')

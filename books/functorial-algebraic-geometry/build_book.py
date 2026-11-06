#!/usr/bin/env python3
"""Assemble the translation, add bidirectional terminology links, and run XeLaTeX."""
from pathlib import Path
import json, re, subprocess, sys
from collections import defaultdict
ROOT=Path(__file__).resolve().parent
BUILD=ROOT/'build'
BUILD.mkdir(exist_ok=True)
BS=chr(92)
SKIP_ENVS={'equation','equation*','align','align*','aligned','gather','gather*','multline','multline*','eqnarray','eqnarray*','displaymath','math','tikzcd','tikzpicture'}
SKIP_COMMANDS={'addcontentsline':3,'sourcepage':2,'BookChapter':2,'Section':2,'PartTitle':2,'label':1,'ref':1,'pageref':1,'eqref':1,'tag':1,'cite':1,'url':1,'hypertarget':2,'hyperlink':2,'includegraphics':1,'input':1,'section':1,'subsection':1,'subsubsection':1,'chapter':1,'setcounter':2,'newcommand':2,'renewcommand':2,'hspace':1,'vspace':1,'rule':2,'cline':1,'cmidrule':1}

def balanced_end(s,i):
    if i>=len(s) or s[i]!='{':return i
    depth=1;j=i+1
    while j<len(s) and depth:
        if s[j]==BS:j+=2;continue
        if s[j]=='{':depth+=1
        elif s[j]=='}':depth-=1
        j+=1
    return j

def make_linked(s,prefix,vocabulary):
    buckets=defaultdict(list)
    for word,key in vocabulary.items():buckets[word[0]].append((word,key))
    for values in buckets.values():values.sort(key=lambda p:len(p[0]),reverse=True)
    out=[];uses=[];i=0;n=0
    while i<len(s):
        if s[i]=='%':
            j=s.find('\n',i);j=len(s) if j<0 else j
            out.append(s[i:j]);i=j;continue
        if s[i]=='$':
            delim='$$' if s.startswith('$$',i) else '$'
            j=i+len(delim)
            while j<len(s):
                if s[j]==BS:j+=2;continue
                if s.startswith(delim,j):j+=len(delim);break
                j+=1
            out.append(s[i:j]);i=j;continue
        if s[i]==BS:
            if s.startswith(BS+'[',i) or s.startswith(BS+'(',i):
                end=BS+(']' if s[i+1]=='[' else ')');j=s.find(end,i+2)
                j=len(s) if j<0 else j+2
                out.append(s[i:j]);i=j;continue
            m=re.match(r'\\begin\{([^}]+)\}',s[i:])
            if m and m[1] in SKIP_ENVS:
                end=BS+'end{'+m[1]+'}';j=s.find(end,i+len(m[0]))
                j=len(s) if j<0 else j+len(end)
                out.append(s[i:j]);i=j;continue
            m=re.match(r'\\([A-Za-z@]+)\*?',s[i:])
            if m:
                j=i+len(m[0]);cmd=m[1]
                if cmd in SKIP_COMMANDS:
                    if j<len(s) and s[j]=='[':
                        k=s.find(']',j);j=k+1 if k>=0 else j
                    for _ in range(SKIP_COMMANDS[cmd]):
                        k=j
                        while k<len(s) and s[k].isspace():k+=1
                        if k<len(s) and s[k]=='{':j=balanced_end(s,k)
                        else:break
                out.append(s[i:j]);i=j;continue
            out.append(s[i:i+2]);i+=2;continue
        found=False
        for word,key in buckets.get(s[i],[]):
            if not s.startswith(word,i):continue
            after=s[i+len(word):i+len(word)+1]
            before=s[i-1:i] if i else ''
            if len(word)==1 and ((word=='层' and after in {'次','面','级','楼'}) or (word=='环' and after in {'境','绕','节','路'}) or (word=='积' and (after in {'分','累'} or before in {'累','聚'})) or (word=='模' and (after in {'式','型','样','仿'} or before=='规')) or (word=='核' and after in {'心','实','查','对'}) or (word=='景' and before in {'背','风','场','情','前'})):continue
            n+=1;uid=f'{prefix}{n:05d}'
            out.append(BS+'TermUse{'+key+'}{'+uid+'}{'+word+'}')
            uses.append({'key':key,'id':uid,'text':word})
            i+=len(word);found=True;break
        if not found:out.append(s[i]);i+=1
    return ''.join(out),uses

def assemble():
    entries=json.loads((ROOT/'glossary.json').read_text())
    vocabulary={}
    for e in entries:
        for w in [e['zh']]+e.get('aliases',[]):
            if w:vocabulary.setdefault(w,e['key'])
    all_uses=[]
    for p in sorted((ROOT/'chapters').glob('[a-g].tex')):
        translated,uses=make_linked(p.read_text().replace('正向极限','归纳极限'),p.stem,vocabulary)
        (BUILD/f'linked-{p.stem}.tex').write_text(translated)
        all_uses.extend(uses)
    (BUILD/'term-uses.json').write_text(json.dumps(all_uses,ensure_ascii=False,indent=2))
    return entries,all_uses

def make_glossary(entries,uses):
    pages={}
    aux=BUILD/'main.aux'
    if aux.exists():
        for m in re.finditer(r'\\newlabel\{use-([^}]+)\}\{\{[^}]*\}\{([^}]+)\}',aux.read_text()):pages[m[1]]=m[2]
    by_key=defaultdict(list)
    for u in uses:by_key[u['key']].append(u)
    out=[]
    for e in entries:
        out.append(BS+'GlossHeading{'+e['key']+'}{'+e['zh']+'}{'+e['en']+'}{'+e['fr']+'}')
        by_page={}
        for u in by_key[e['key']]:
            p=pages.get(u['id'],'?');by_page.setdefault(p,[]).append(u['id'])
        refs=[]
        for p,ids in by_page.items():
            if p=='?':
                refs.extend(BS+'hyperlink{use-'+uid+'}{'+BS+'pageref*{use-'+uid+'}}' for uid in ids)
            elif len(ids)==1:refs.append(BS+'hyperlink{use-'+ids[0]+'}{'+p+'}')
            else:
                indices=[BS+'hyperlink{use-'+uid+'}{'+str(j+1)+'}' for j,uid in enumerate(ids)]
                refs.append(p+'('+', '.join(indices)+')')
        out.append(BS+'GlossRefs{'+((BS+'enspace '+BS+'allowbreak ').join(refs) if refs else '本表所列相关术语。')+'}')
    (BUILD/'glossary.tex').write_text('\n'.join(out)+'\n')

def compile_once():
    cmd=['/Library/TeX/texbin/xelatex','-interaction=nonstopmode','-halt-on-error','-file-line-error','-output-directory=build','main.tex']
    proc=subprocess.run(cmd,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    (BUILD/'compile-output.txt').write_text(proc.stdout)
    if proc.returncode:
        print('\n'.join(proc.stdout.splitlines()[-45:]))
        raise SystemExit(proc.returncode)
    print('\n'.join(proc.stdout.splitlines()[-4:]),flush=True)

if __name__=='__main__':
    entries,uses=assemble()
    if '--assemble-only' in sys.argv:
        make_glossary(entries,uses)
    else:
        for _ in range(3):
            make_glossary(entries,uses)
            compile_once()
        subprocess.run(['/bin/cp',str(BUILD/'main.pdf'),str(ROOT/'函子代数几何导论·第一卷·中文译本.pdf')],check=True)
        print(f'Completed: {len(entries)} glossary entries; {len(uses)} linked occurrences.')

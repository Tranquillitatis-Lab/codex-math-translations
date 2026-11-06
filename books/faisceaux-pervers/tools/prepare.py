#!/usr/bin/env python3
"""Merge terminology and link prose; math and explicit term calls remain intact."""
from pathlib import Path
import re, json
ROOT=Path(__file__).resolve().parents[1]
TERMS={}
ALIASES={'conservative-functor':'conservative'}
for path in [ROOT/'style/terms-core.tsv',*sorted((ROOT/'chapters').glob('terms-*.tsv'))]:
    if not path.exists():continue
    for line in path.read_text().splitlines():
        if not line.strip() or line.startswith('#'):continue
        parts=(line if '\t' in line else line.replace('\\t','\t')).split('\t')
        if len(parts)!=4:raise ValueError(f'{path.name}: Expected four fields: {line}')
        key,zh,en,fr=parts
        key=ALIASES.get(key,key)
        if key not in TERMS:TERMS[key]=(zh,en,fr)
TERMS.update({
 'trait':('特质','trait','trait'),
 'abelian-subcategory':('阿贝尔子范畴','abelian subcategory','sous-catégorie abélienne'),
 'adjoint-functor':('伴随函子','adjoint functor','foncteur adjoint'),
 'intersection-homology':('交叉同调','intersection homology',"homologie d'intersection"),
 'holonomic-module':('完整模','holonomic module','module holonome'),
 'constant-sheaf':('常值层','constant sheaf','faisceau constant'),
 'coherent-sheaf':('凝聚层','coherent sheaf','faisceau cohérent'),
 'quasi-coherent':('拟凝聚','quasi-coherent','quasi-cohérent'),
 'regular-singularity':('正则奇点','regular singularity','singularité régulière'),
 'hypercohomology':('超上同调','hypercohomology','hypercohomologie'),
 'compact-support':('紧支撑','compact support','support compact'),
 'base-change':('基变换','base change','changement de base'),
 't-exact':('$t$-正合','$t$-exact','$t$-exact'),
 'stack':('叠','stack','champ'),
})
# A term's variants retain their displayed wording while sharing one entry.
variants={v[0]:k for k,v in TERMS.items()}
variants.update({'阿贝尔子范畴':'abelian-subcategory','栈':'stack','保守':'conservative','强 Lefschetz 定理':'hard-lefschetz','局部常值层':'local-system','伴随函子':'adjoint-functor'})
TERMS['local-system']=('局部系统（局部常值层）','local system','système local')
ordered=sorted(variants,key=len,reverse=True)
terms_re=re.compile('|'.join(re.escape(x) for x in ordered))
math_envs={'equation','equation*','align','align*','alignat','alignat*','gather','gather*','multline','multline*','displaymath','math','tikzpicture','tikzcd'}

def group_end(s,pos):
    if pos>=len(s) or s[pos]!='{':return pos
    depth=0
    while pos<len(s):
        if s[pos]=='\\':pos+=2;continue
        if s[pos]=='{':depth+=1
        elif s[pos]=='}':
            depth-=1
            if depth==0:return pos+1
        pos+=1
    return pos

def link_math(s):
    # Technical words inside a formula's text boxes remain ordinary prose.
    pat=re.compile(r'\\(?:text|mbox|textnormal|textup|textbf|textrm|textsf)\{')
    out=[];i=0
    while True:
        m=pat.search(s,i)
        if not m:out.append(s[i:]);break
        end=group_end(s,m.end()-1)
        if end<=m.end() or s[end-1]!='}':
            out.append(s[i:]);break
        out.append(s[i:m.end()]+link_plain(s[m.end():end-1])+'}')
        i=end
    return ''.join(out)

def link_plain(s):
    out=[];i=0
    while i<len(s):
        if s[i]=='%':
            j=s.find('\n',i);j=len(s) if j<0 else j
            out.append(s[i:j]);i=j;continue
        if s.startswith('\\term{',i):
            first=group_end(s,i+5);last=group_end(s,first)
            token=s[i:last]
            for old,new in ALIASES.items():token=token.replace('\\term{'+old+'}', '\\term{'+new+'}')
            out.append(token);i=last;continue
        if s.startswith('\\begin{',i):
            b=re.match(r'\\begin\{([^}]+)\}',s[i:])
            if b and b[1] in math_envs:
                end='\\end{'+b[1]+'}';j=s.find(end,i)
                if j>=0:out.append(link_math(s[i:j+len(end)]));i=j+len(end);continue
        # Match terms including an inline mathematical prefix, e.g. $t$-structure.
        matched=False
        for prefix in ('$t$-结构','$t$-正合','$\\ell$-进'):
            if s.startswith(prefix,i):
                out.append('\\term{'+variants[prefix]+'}{'+prefix+'}');i+=len(prefix);matched=True;break
        if matched:continue
        if s.startswith('\\[',i) or s.startswith('\\(',i):
            closing='\\]' if s[i+1]=='[' else '\\)';j=s.find(closing,i+2)
            if j>=0:out.append(link_math(s[i:j+2]));i=j+2;continue
        if s[i]=='$':
            delim='$$' if s.startswith('$$',i) else '$';j=i+len(delim)
            depth=0
            while j<len(s):
                if s[j]=='\\':j+=2;continue
                if s[j]=='{':depth+=1
                elif s[j]=='}':depth-=1
                elif depth==0 and s.startswith(delim,j):break
                j+=1
            end=min(len(s),j+len(delim))
            out.append(link_math(s[i:end]));i=end;continue
        if s[i]=='\\':
            cmd=re.match(r'\\[A-Za-z@]+\*?',s[i:])
            if cmd:
                name=cmd[0];j=i+len(name)
                if name.rstrip('*') in {'\\chapter','\\section','\\subsection','\\subsubsection','\\addcontentsline','\\markboth','\\markright','\\label','\\hypertarget','\\href','\\url','\\SourcePage','\\newcommand','\\renewcommand','\\providecommand','\\DeclareMathOperator'}:
                    # Skip heading/metadata arguments; links in bookmarks must not add occurrences.
                    while j<len(s) and s[j] in ' \t':j+=1
                    if j<len(s) and s[j]=='[':
                        close=s.find(']',j);j=close+1 if close>=0 else j
                    while j<len(s) and s[j]=='{':j=group_end(s,j)
                    out.append(s[i:j]);i=j;continue
                out.append(name);i=j;continue
            out.append(s[i:i+2]);i+=2;continue
        m=terms_re.match(s,i)
        if m:
            word=m[0]
            # These ordinary words do not name the heart/purity/torsion of an object.
            if (word=='心' and i and s[i-1] in '核中细小重担关') or (word=='纯' and s.startswith('纯粹',i)) or (word=='层' and s.startswith('层次',i)) or (word=='权' and (s.startswith('权限',i) or s.startswith('权威',i))) or (word=='挠' and s.startswith('挠曲',i)):
                out.append(word)
            else:out.append('\\term{'+variants[word]+'}{'+word+'}')
            i=m.end();continue
        out.append(s[i]);i+=1
    return ''.join(out)

# Backups are kept once, outside the deliverable source tree.
backup=ROOT/'source/unlinked-translation';backup.mkdir(parents=True, exist_ok=True)
missing=set();used={};pages=set()
for p in sorted((ROOT/'chapters').glob('*.tex')):
    s=p.read_text()
    s=s.replace(r'\term{abelian-category}{阿贝尔子范畴}',r'\term{abelian-subcategory}{阿贝尔子范畴}').replace(r'\term{adjunction}{伴随函子}',r'\term{adjoint-functor}{伴随函子}')
    if not (backup/p.name).exists():(backup/p.name).write_text(s)
    s=link_plain(s)
    p.write_text(s)
    for key,zh in re.findall(r'\\term\{([^}]+)\}\{([^}]*)\}',s):
        if key not in TERMS:missing.add(key)
        used[key]=used.get(key,0)+1
    pages.update(map(int,re.findall(r'\\SourcePage\{(\d+)\}',s)))
if missing:raise ValueError('Undefined terminology: '+', '.join(sorted(missing)))
with (ROOT/'style/glossary-entries.tex').open('w') as f:
    f.write('% Generated by tools/prepare.py; edit the TSV sources.\n')
    for k,(zh,en,fr) in sorted(TERMS.items(),key=lambda kv:kv[1][1].lower()):
        f.write('\\GlossaryEntry{'+k+'}{'+zh+'}{'+en+'}{'+fr+'}\n')
(ROOT/'source/translation-manifest.json').write_text(json.dumps({'source_pdf_pages':192,'translated_source_pages':sorted(pages),'glossary_entries':len(TERMS),'term_occurrences':sum(used.values()),'occurrences_by_key':used},ensure_ascii=False,indent=2))
print(f'Prepared {len(TERMS)} terminology entries, {sum(used.values())} occurrences; {len(pages)}/192 source pages recorded.')

"""Add occurrence links to unmarked, unambiguous multi-character Chinese terms.

Only completed modules are edited. Existing Term commands, headings, verbatim,
formulae and diagram environments are preserved. Single-character terms continue
to be marked by the translator, since substring replacement would be ambiguous.
"""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
target=sys.argv[1] if len(sys.argv)>1 else None
finished={v['id'] for v in json.loads((ROOT/'sources/manifest.json').read_text()) if v['translation_status']=='complete'}
SKIP_ARGS = {'Term':2,'SGAchapter':3,'SGAsection':2,'SGAsubsection':2,
 'SGAfrontchapter':1,'SourcePage':1,'label':1,'ref':1,'pageref':1,
 'url':1,'href':2,'hyperlink':2,'hypertarget':2,'DeclareSGATerm':4,
 'operatorname':1,'SGAsourceRef':1}
MATH_ENVS = {'equation','equation*','align','align*','gather','gather*',
 'multline','multline*','displaymath','math','tikzcd','tikzpicture',
 'verbatim','Verbatim','lstlisting'}

def group_end(s, pos):
    depth=0
    for i in range(pos,len(s)):
        if s[i]=='\\':
            continue
        if i and s[i-1]=='\\':
            continue
        if s[i]=='{': depth+=1
        elif s[i]=='}':
            depth-=1
            if depth==0: return i+1
    return len(s)

ready={}
for report in (ROOT/'reports').glob('*.json'):
    data=json.loads(report.read_text())
    if isinstance(data,dict) and data.get('status')=='complete': ready[report.stem]=data
terms={}
for path in sorted((ROOT/'glossary').glob('*.tex')):
    if path.stem not in ready: continue
    for key,zh in re.findall(r'\\DeclareSGATerm\{([^{}]+)\}\{([^{}]+)\}',path.read_text()):
        if len(re.findall(r'[\u3400-\u9fff]',zh))>=2 and '\\' not in zh and zh not in {'适当','表示','忠实','自由','单纯','简单','平凡','自然','标准','对应','特殊','分解','作用'}:
            terms.setdefault(zh,key)
boundaries={'自态射':r'(?<!来)自态射','同态':r'同态(?!射)','同构':r'同构(?!造)',
 '仿射':r'(?<!模)仿射','单射':r'(?<!简)单射','单态射':r'(?<!简)单态射',
 '满射':r'(?<!充)满射','可表':r'可表(?!达|述)','可分':r'可分(?!离)'}
pattern=re.compile('|'.join(boundaries.get(x,re.escape(x)) for x in sorted(terms,key=len,reverse=True))) if terms else None

def link(s):
    out=[]; i=0
    while i<len(s):
        if s[i]=='%':
            end=s.find('\n',i)
            if end<0: end=len(s)
            out.append(s[i:end]);i=end;continue
        if s[i]=='$' or s.startswith('\\(',i) or s.startswith('\\[',i):
            opener='$$' if s.startswith('$$',i) else s[i:i+2] if s[i]=='\\' else '$'
            closer={'\\(':'\\)','\\[':'\\]'}.get(opener,opener)
            end=s.find(closer,i+len(opener))
            end=len(s) if end<0 else end+len(closer)
            out.append(s[i:end]);i=end;continue
        if s[i]=='\\':
            env=re.match(r'\\begin\{([^}]+)\}',s[i:])
            if env and env[1] in MATH_ENVS:
                end=s.find('\\end{'+env[1]+'}',i+len(env[0]))
                end=len(s) if end<0 else end+len('\\end{'+env[1]+'}')
                out.append(s[i:end]);i=end;continue
            cmd=re.match(r'\\([A-Za-z@]+)\*?',s[i:])
            if cmd:
                end=i+len(cmd[0])
                for _ in range(SKIP_ARGS.get(cmd[1],0)):
                    while end<len(s) and s[end].isspace():end+=1
                    if end<len(s) and s[end]=='{':end=group_end(s,end)
                out.append(s[i:end]);i=end;continue
            out.append(s[i:i+2]);i+=2;continue
        end=i+1
        while end<len(s) and s[end] not in '\\$%':end+=1
        text=s[i:end]
        out.append(pattern.sub(lambda m:'\\Term{'+terms[m[0]]+'}{'+m[0]+'}',text) if pattern else text)
        i=end
    return ''.join(out)

count=0
for path in ROOT.glob('volumes/*/chunks/*.tex'):
    volume=path.parent.parent.name
    if target and volume!=target:continue
    if not target and volume in finished:continue
    if 'index' in path.stem:continue
    if path.parent.parent.name+'-'+path.stem not in ready:continue
    original=path.read_text();updated=link(original)
    if updated!=original:
        path.write_text(updated);count+=1
print(f'已为 {count} 个完整模块补入多字术语位置链接。')

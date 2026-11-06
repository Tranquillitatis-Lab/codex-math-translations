"""Normalize known XeLaTeX input conventions in completed modules."""
from pathlib import Path
import json
import re
import shutil

ROOT=Path(__file__).resolve().parents[1]

def fix_resized_diagram(match):
    block=match[0]
    block=block.replace('{$\\begin{tikzcd}', '{\\begin{tikzcd}')
    block=block.replace('\\end{tikzcd}$}', '\\end{tikzcd}}')
    start=re.search(r'\\begin\{tikzcd\}(\[[^\]]*\])?',block)
    options=start[1] or '[]'
    if 'ampersand replacement' not in options:
        options='[ampersand replacement=\\&'+(','+options[1:-1] if options!='[]' else '')+']'
        block=block[:start.start()]+'\\begin{tikzcd}'+options+block[start.end():]
    return re.sub(r'(?<!\\)&',r'\\&',block)

def fix_aligned_tag(match):
    block=match[0]
    if re.match(r'\\begin\{aligned\}\s*&',block):
        block=re.sub(r'(\\begin\{aligned\}\s*)&',r'\1{}&',block).replace(r'\\&',r'\\{}&')
    tags=re.findall(r'\\tag\*?\{[^{}]*\}',block)
    if len(tags)==1:
        return block.replace(tags[0],'')+tags[0]
    return block

def protect_footnote_diagrams(source):
    spans=[]
    for match in re.finditer(r'\\footnote(?:\[[^\]]*\])?\{',source):
        depth=1;end=match.end()
        while end<len(source) and depth:
            char=source[end]
            if end==0 or source[end-1]!='\\':
                if char=='{':depth+=1
                elif char=='}':depth-=1
            end+=1
        if depth==0:spans.append((match.end(),end-1))
    for start,end in reversed(spans):
        body=source[start:end]
        body=re.sub(r'\\begin\{tikzcd\}[\s\S]*?\\end\{tikzcd\}',fix_resized_diagram,body)
        source=source[:start]+body+source[end:]
    return source

def lift_source_markers(match):
    block=match[0]
    markers=re.findall(r'\\SourcePage\{\d+\}',block)
    if markers:
        block=re.sub(r'\\SourcePage\{\d+\}','',block)
    return ''.join(markers)+re.sub(r'\n[ \t]*\n+', '\n',block)

def fix_diagram_labels(match):
    def protect(label):
        text=label[1]
        if any(c in text for c in ',[]') and not(text.startswith('{') and text.endswith('}')):
            return '"{'+text+'}"'
        return label[0]
    return re.sub(r'"([^"\n]*)"',protect,match[0])

for p in ROOT.glob('volumes/*/chunks/*.tex'):
    report=ROOT/'reports'/f'{p.parent.parent.name}-{p.stem}.json'
    if not report.exists():continue
    data=json.loads(report.read_text())
    if data.get('status')!='complete':continue
    before=p.read_text()
    after=re.sub(r'(\\[A-Za-z@]+)(?=[\u3400-\u9fff])',r'\1 ',before)
    for graphic in re.finditer(r'\\includegraphics(?:\[[^\]]*\])?\{(work/[^{}]+)\}',after):
        original=ROOT/graphic[1]
        if original.is_file():
            destination=ROOT/'figures'/p.parent.parent.name/(p.stem+'-'+original.name)
            destination.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(original,destination)
            after=after.replace(graphic[1],str(destination.relative_to(ROOT)))
    after=re.sub(r'来\\Term\{[^{}]+\}\{自态射\}',r'来自\\Term{morphism}{态射}',after)
    after=re.sub(r'连\\Term\{[^{}]+\}\{同态\}射',r'连同\\Term{morphism}{态射}',after)
    after=re.sub(r'相\\Term\{[^{}]+\}\{同构\}造','相同构造',after)
    after=re.sub(r'模\\Term\{[^{}]+\}\{仿射\}影',r'模仿\\Term{projective}{射影}',after)
    after=re.sub(r'简\\Term\{[^{}]+\}\{单态射\}','简单态射',after)
    after=re.sub(r'简\\Term\{[^{}]+\}\{单射\}影',r'简单\\Term{projective}{射影}',after)
    after=re.sub(r'\\Term\{trivial-bundle\}\{平凡\}地验证','容易验证',after)
    after=after.replace(r'\mathrm{\acute et}',r'\text{ét}')
    after=after.replace(r'\mathrm{\acute{e}t}',r'\text{ét}')
    after=after.replace(r'\operatorname{prof\acute et}',r'\operatorname{prof\text{ét}}')
    after=after.replace(r'\operatorname{Ptg\acute eom}',r'\operatorname{Ptg\text{é}om}')
    after=re.sub(r'\\(mathrm|operatorname)\{([A-Za-z]*)\\acute\s+e([A-Za-z]*)\}',lambda m:'\\'+m[1]+'{'+m[2]+r'\text{é}'+m[3]+'}',after)
    after=re.sub(r'\\(mathrm|operatorname)\{([A-Za-z]*)\\acute(?:\s+([eE])|\{([eE])\})([A-Za-z]*)\}',lambda m:'\\'+m[1]+'{'+m[2]+r'\text{'+('É' if (m[3] or m[4])=='E' else 'é')+'}'+m[5]+'}',after)
    after=re.sub(r'\\mathscr\{([A-Z])([a-z]+)\}',lambda m:r'\mathscr{'+m[1]+r'}\mathrm{'+m[2]+'}',after)
    after=re.sub(r"\\tag\{(\\(?:dagger|ddagger|star|ast)'*)\}",lambda m:r'\tag{$'+m[1]+'$}',after)
    after=after.replace(r'\Term{constructible-set}{可构造集}合层',r'\Term{constructible}{可构造}\Term{set-sheaf}{集合层}')
    after=re.sub(r'\\begin\{tikzcd\}[\s\S]*?\\end\{tikzcd\}',fix_diagram_labels,after)
    after=re.sub(r'\\resizebox\{[^}]+\}\{[^}]+\}\{\$?\\begin\{tikzcd\}[\s\S]*?\\end\{tikzcd\}\$?\}',fix_resized_diagram,after)
    after=protect_footnote_diagrams(after)
    after=re.sub(r'\\begin\{aligned\}[\s\S]*?\\end\{aligned\}',fix_aligned_tag,after)
    after=re.sub(r'(?<!\\)\$(?!\$)[\s\S]*?(?<!\\)\$',lift_source_markers,after)
    after=re.sub(r'(?<!\\)\\\[[\s\S]*?(?<!\\)\\\]',lift_source_markers,after)
    if after!=before:p.write_text(after)

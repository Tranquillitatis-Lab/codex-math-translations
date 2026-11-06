#!/usr/bin/env python3
"""Generate linked terms and note indices, then typeset with XeLaTeX."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
NAMES = ['00-intro','00-guide','01-arcata-a','01-arcata-b','02-rapport','03-functions','04-cycles','05-duality','06-sums-a','06-sums-b','07-finitude','08-derived','09-erratum','10-catalogue']

SPELLINGS = {
    '准射影':'拟射影', '准紧':'拟紧', '准分离':'拟分离',
    '既约':'约化', '投射极限':'逆极限', '下降数据':'下降资料',
    '皮卡':'Picard', '周坐标':'Chow 坐标',
    'Picard预概形':'Picard 预概形', 'Picard概形':'Picard 概形',
    'Hilbert概形':'Hilbert 概形', 'Hilbert多项式':'Hilbert 多项式',
    '广义雅可比簇':'广义 Jacobi 簇', '连通分量':'连通分支',
    '希尔伯特':'Hilbert', '维特':'Witt',
}
CANONICAL = {
    'schéma':('概形','scheme'), 'faisceau':('层','sheaf'),
    'étale':('平展','étale'), 'cohomologie étale':('平展上同调','étale cohomology'),
    'faisceau constructible':('可构造层','constructible sheaf'),
    'quasi-compact':('拟紧','quasi-compact'), 'quasi-séparé':('拟分离','quasi-separated'),
    'limite projective':('逆极限','inverse limit'),
    'catégorie dérivée':('导出范畴','derived category'),
    'catégorie triangulée':('三角范畴','triangulated category'),
    'torseur':('扭子','torsor'), 'réduit':('约化','reduced'),
}

TERM_SETTINGS = json.loads((ROOT/'terminology-canonical.json').read_text(encoding='utf-8'))
SPELLINGS.update(TERM_SETTINGS['replacements'])
SPELLINGS.update({'pro 对象':'pro-对象'})
ZH_CANONICAL=TERM_SETTINGS['terms']

def spellings(s):
    s=re.sub(r'\\term\{投射对象\}\{pro-object\}\{pro-objet\}',lambda m:r'\term{pro-对象}{pro-object}{pro-objet}',s)
    for old, new in sorted(SPELLINGS.items(),key=lambda item:len(item[0]),reverse=True):
        s = s.replace(old, new)
    for name in ['Picard','Hilbert']:
        s=re.sub(name+r'\s*\\term\{概形\}\{scheme\}\{schéma\}',lambda m:r'\term{'+name+' 概形}{'+name+' scheme}{schéma de '+name+'}',s)
    return re.sub(r'(\\[A-Za-z@]+)(?=[\u3400-\u9fff])',r'\1 ',s)

def annotate_plain(text, dictionary):
    """Tag repeated Chinese terms, preserving formulae and structural TeX arguments."""
    if not dictionary:
        return text
    words = re.compile('|'.join(re.escape(w) for w in sorted(dictionary,key=len,reverse=True)))
    parts, plain, i = [], [], 0
    def flush():
        if plain:
            s = ''.join(plain)
            def replacement(m):
                # Do not mistake domain/neighbourhood, loop/environment, or
                # stratification for the single-character algebraic terms.
                excluded = {'域':['定义域','值域','邻域','区域','领域'],
                            '环':['环境','环路','环面','循环','圆环'],
                            '层':['层面','分层','层次','底层'],
                            '茎':[], '栈':[]}
                for phrase in excluded.get(m.group(),[]):
                    start=0
                    while (start:=s.find(phrase,start))>=0:
                        if start <= m.start() < start+len(phrase): return m.group()
                        start+=1
                return '\\term{'+'}{'.join(dictionary[m.group()])+'}'
            parts.append(words.sub(replacement,s))
            plain.clear()
    protected = {'term':3,'origpage':2,'label':1,'ref':1,'pageref':1,
                 'url':1,'href':2,'hyperlink':2,'input':1,'includegraphics':1,
                 'cite':1,'hypertarget':2,'newcommand':2,'providecommand':2,
                 'addcontentsline':3,'addtocontents':2,'markboth':2,'chaptermark':1}
    math_envs = {'equation','equation*','align','align*','gather','gather*',
                 'multline','multline*','tikzcd','tikzpicture','displaymath',
                 'math','eqnarray','eqnarray*'}
    while i < len(text):
        if text[i] == '%':
            flush(); end = text.find('\n',i)
            if end < 0: end=len(text)
            parts.append(text[i:end]); i=end; continue
        if text[i] == '$' or text.startswith(r'\[',i) or text.startswith(r'\(',i):
            flush()
            token = '$$' if text.startswith('$$',i) else text[i:i+2] if text[i]=='\\' else '$'
            closing = {r'\[':r'\]',r'\(':r'\)'}.get(token,token)
            end = text.find(closing,i+len(token))
            if end < 0: end=len(text)-len(closing)
            chunk = text[i:end+len(closing)]
            chunk = re.sub('[，。；：]',lambda m:r'\text{'+m.group()+'}',chunk)
            parts.append(chunk); i=end+len(closing); continue
        if text[i] == '\\':
            flush()
            m = re.match(r'\\([A-Za-z@]+|.)',text[i:],re.S)
            if not m: parts.append(text[i]);i+=1;continue
            command=m.group(1); end=i+len(m.group())
            if command in {'chapter','section','subsection','subsubsection','paragraph','chapterintro'}:
                if end<len(text) and text[end]=='*': end+=1
                optional=re.match(r'\[[^\]]*\]',text[end:])
                if optional: end+=len(optional.group())
                try:
                    _,pos=arguments(text,end,2 if command=='chapterintro' else 1)
                    parts.append(text[i:pos]);i=pos;continue
                except ValueError: pass
            if command in {'begin','end'}:
                try:
                    a,pos=arguments(text,end,1)
                    if command=='begin' and a[0] in math_envs:
                        close=r'\end{'+a[0]+'}'
                        stop=text.find(close,pos)
                        if stop>=0: pos=stop+len(close)
                    parts.append(text[i:pos]);i=pos;continue
                except ValueError: pass
            if command in protected:
                try:
                    _,pos=arguments(text,end,protected[command])
                    parts.append(text[i:pos]);i=pos;continue
                except ValueError: pass
            if command=='hyperref':
                m2=re.match(r'\[[^\]]*\]',text[end:])
                if m2:
                    end+=len(m2.group())
                    try:
                        _,end=arguments(text,end,1)
                    except ValueError: pass
            parts.append(text[i:end]);i=end;continue
        plain.append(text[i]);i+=1
    flush()
    return ''.join(parts)

def arguments(text, pos, count):
    args = []
    for _ in range(count):
        while pos < len(text) and text[pos].isspace():
            pos += 1
        if pos >= len(text) or text[pos] != '{':
            raise ValueError(f'Missing macro argument near {text[max(0,pos-70):pos+70]!r}')
        start = pos + 1
        level = 1
        pos += 1
        while pos < len(text) and level:
            if text[pos] == '\\':
                pos += 2
                continue
            if text[pos] == '{':
                level += 1
            elif text[pos] == '}':
                level -= 1
            pos += 1
        if level:
            raise ValueError('Unclosed macro argument')
        args.append(text[start:pos-1])
    return args, pos

def normalized(s):
    return ' '.join(unicodedata.normalize('NFC', s).strip().split()).casefold()

def sortkey(s):
    return ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c)).casefold()

def generate(allow_partial=False):
    gen = ROOT / 'generated'
    gen.mkdir(exist_ok=True)
    terms, notes, coverage = {}, [], {}
    dictionary = {zh:(zh,item['en'],item['fr']) for zh,item in ZH_CANONICAL.items()}
    for chapter in NAMES:
        src = ROOT/'chapters'/(chapter+'.tex')
        if not src.exists(): continue
        source = spellings(src.read_text(encoding='utf-8'))
        for m in re.finditer(r'\\term\b',source):
            args,_ = arguments(source,m.end(),3)
            zh,en,fr=args
            # Short generic words and formulae do not form safe lexical matches.
            word=zh[:-1] if zh.endswith('的') else zh
            if word not in {'形式','有限','等价','特征'} and (len(word)>=2 or word in {'层','栈','茎','环','域'}) and re.fullmatch(r'[\w\s\u3400-\u9fff-]+',word) and re.search(r'[\u3400-\u9fff]',word):
                dictionary.setdefault(word,(word,en,fr))
    for chapter in NAMES:
        src = ROOT / 'chapters' / (chapter + '.tex')
        if not src.exists():
            if not allow_partial:
                raise FileNotFoundError(src)
            (gen / (chapter + '.tex')).write_text('', encoding='utf-8')
            continue
        text = spellings(src.read_text(encoding='utf-8'))
        if chapter != '10-catalogue':
            text = annotate_plain(text,dictionary)
        result, cursor, original_page = [], 0, ''
        first_page = re.search(r'\\origpage\b',text)
        if first_page:
            first_args,_ = arguments(text,first_page.end(),2)
            original_page = first_args[1]
        page_ids = []
        pattern = re.compile(r'\\(term|translatornote|origpage)\b')
        serial = 0
        def render_term(args):
            nonlocal serial
            zh,en,fr=args
            if '\\term' in ''.join(args):
                raise ValueError(f'Nested term in {src}: {args}')
            key=hashlib.sha1(normalized(zh).encode()).hexdigest()[:12]
            canonical=CANONICAL.get(normalized(fr),(zh,en))
            preferred=ZH_CANONICAL.get(zh,{'en':canonical[1],'fr':fr})
            item=terms.setdefault(key,{'zh':canonical[0],'en':preferred['en'],'fr':preferred['fr'],'occurrences':[],'variants':[]})
            if (zh,en)!=(item['zh'],item['en']):
                variant={'zh':zh,'en':en}
                if variant not in item['variants']:item['variants'].append(variant)
            serial+=1
            occ=f'{chapter}-{serial:04d}'
            item['occurrences'].append({'id':occ,'original_page':original_page,'chapter':chapter})
            return f'\\termuse{{{key}}}{{{occ}}}{{{zh}}}{{{fr}}}'
        def render_note_terms(note):
            result,pos=[],0
            while m:=re.search(r'\\term\b',note[pos:]):
                start=pos+m.start(); stop=pos+m.end()
                result.append(note[pos:start])
                a,pos=arguments(note,stop,3)
                result.append(render_term(a))
            result.append(note[pos:])
            return ''.join(result)
        while match := pattern.search(text, cursor):
            result.append(text[cursor:match.start()])
            name = match.group(1)
            args, end = arguments(text, match.end(), {'term':3,'translatornote':1,'origpage':2}[name])
            if name == 'origpage':
                original_page = args[1]
                page_ids.append(int(args[0]))
                result.append(text[match.start():end])
            elif name == 'term':
                result.append(render_term(args))
            else:
                nid = f'n{len(notes)+1:03d}'
                notes.append({'id':nid,'text':args[0],'original_page':original_page,'chapter':chapter})
                result.append(f'\\translatornoteuse{{{nid}}}{{{render_note_terms(args[0])}}}')
            cursor = end
        result.append(text[cursor:])
        coverage[chapter] = page_ids
        (gen / (chapter + '.tex')).write_text(''.join(result), encoding='utf-8')
    table = [r'\chapter{中、英、法术语对照表}',
             '按法文词头的字母顺序排列。点击中文词条可返回首次出现处，点击任一位置可返回该次出现处；同页的各链接分别定位到对应词。数字为译本页码；同一页码下的各链接分别指向该页的不同出现位置。',
             r'\begingroup\small\setlength{\parindent}{0pt}',
             r'\setlength{\tabcolsep}{4pt}\renewcommand{\arraystretch}{1.18}',
             r'\begin{longtable}{@{}>{\raggedright\arraybackslash}p{.23\linewidth}>{\raggedright\arraybackslash}p{.31\linewidth}>{\raggedright\arraybackslash}p{.39\linewidth}@{}}',
             r'\toprule\textbf{中文} & \textbf{English} & \textbf{Français}\\\midrule\endfirsthead',
             r'\toprule\textbf{中文} & \textbf{English} & \textbf{Français}\\\midrule\endhead',
             r'\bottomrule\endfoot']
    for key, item in sorted(terms.items(), key=lambda pair:sortkey(pair[1]['fr'])):
        first=item['occurrences'][0]['id']
        table += [f'\\hypertarget{{term-{key}}}{{}}\\hyperlink{{termocc-{first}}}{{\\textbf{{\\color{{Ink}}{item["zh"]}}}}} & {item["en"]} & {item["fr"]}\\\\*']
        links = []
        for occ in item['occurrences']:
            label = r'\pageref*{termocc:' + occ['id'] + '}'
            links.append(f'\\hyperlink{{termocc-{occ["id"]}}}{{{label}}}')
        for start in range(0,len(links),32):
            prefix = '正文：' if start==0 else '续：'
            ending = r'}\\[5pt]\midrule' if start+32>=len(links) else r'}\\'
            table.append(r'\multicolumn{3}{@{}p{.975\linewidth}@{}}{\footnotesize\color{Muted}' + prefix + r'，\allowbreak '.join(links[start:start+32]) + ending)
    table += [r'\end{longtable}',r'\endgroup']
    (gen/'glossary.tex').write_text('\n'.join(table)+'\n', encoding='utf-8')
    index = [r'\chapter{译者注索引}',
             '以下链接分别指向正文中的译者注。原著书末对 SGA 4 的勘误另见前篇；此处仅收录翻译时补充的数学说明。',
             r'\begin{description}[style=nextline,leftmargin=1.5em]']
    for n, item in enumerate(notes, 1):
        text = item['text']
        text = re.sub(r'\\(?:hyperref|hyperlink)(?:\[[^\]]*\]|\{[^}]*\})\{([^{}]*)\}', r'\1', text)
        # Show the opening sentence only; the complete note remains in its footnote.
        excerpt = re.split(r'[。；\n]', text, maxsplit=1)[0]
        if len(excerpt) > 150 or '$' in excerpt or '\\[' in excerpt:
            excerpt = '正文中的补充说明与论证'
        index.append(f'\\item[\\hypertarget{{tn-index-{item["id"]}}}{{}}\\hyperlink{{tn-{item["id"]}}}{{译者注 {n}\\quad 译本第\\pageref*{{tn:{item["id"]}}}页}}] {excerpt}。')
    index.append(r'\end{description}')
    (gen/'translator-notes.tex').write_text('\n'.join(index)+'\n',encoding='utf-8')
    manifest = {'terms':terms, 'notes':notes, 'coverage':coverage,
                'term_count':len(terms),'occurrence_count':sum(len(t['occurrences']) for t in terms.values())}
    (gen/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    import csv
    with (ROOT/'术语对照表.csv').open('w',encoding='utf-8-sig',newline='') as fp:
        writer=csv.writer(fp);writer.writerow(['中文','English','Français','正文出现次数'])
        for item in sorted(terms.values(),key=lambda t:sortkey(t['fr'])):
            writer.writerow([item['zh'],item['en'],item['fr'],len(item['occurrences'])])
    print(f'Generated {len(terms)} terms, {manifest["occurrence_count"]} occurrences, {len(notes)} notes.',flush=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--generate-only',action='store_true')
    ap.add_argument('--allow-partial',action='store_true')
    args = ap.parse_args()
    generate(args.allow_partial)
    if not args.generate_only:
        out = ROOT/'output/pdf'
        out.mkdir(parents=True, exist_ok=True)
        subprocess.run(['/Library/TeX/texbin/latexmk','-xelatex','-interaction=nonstopmode','-halt-on-error',
                        '-file-line-error','-outdir='+str(out),'main.tex'],cwd=ROOT,check=True)
        import shutil
        shutil.copy2(out/'main.pdf',out/'SGA4.5-平展上同调-中文全译本.pdf')

if __name__ == '__main__':
    main()

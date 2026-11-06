"""Generate shared build inputs from the actual translated modules.

This is an input-generation utility, not a claim of translation completeness.
"""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'sources' / 'manifest.json'
volumes = json.loads(MANIFEST.read_text())
META = {
 'sga1': ('Revêtements étales et groupe fondamental', 'A. Grothendieck 等'),
 'sga2': ('Cohomologie locale des faisceaux cohérents et théorèmes de Lefschetz locaux et globaux', 'A. Grothendieck 等'),
 'sga3-1': ('Schémas en groupes · I', 'M. Demazure · A. Grothendieck 等'),
 'sga3-2': ('Schémas en groupes · II', 'M. Demazure · A. Grothendieck 等'),
 'sga3-3': ('Schémas en groupes · III', 'M. Demazure · A. Grothendieck 等'),
 'sga4-1': ('Théorie des topos et cohomologie étale des schémas · I', 'M. Artin · A. Grothendieck · J.-L. Verdier 等'),
 'sga4-2': ('Théorie des topos et cohomologie étale des schémas · II', 'M. Artin · A. Grothendieck · J.-L. Verdier 等'),
 'sga4-3': ('Théorie des topos et cohomologie étale des schémas · III', 'M. Artin · A. Grothendieck · J.-L. Verdier 等'),
 'sga5': ('Cohomologie ℓ-adique et fonctions L', 'A. Grothendieck 等'),
 'sga6': ('Théorie des intersections et théorème de Riemann–Roch', 'P. Berthelot · A. Grothendieck · L. Illusie 等'),
 'sga7-1': ('Groupes de monodromie en géométrie algébrique · I', 'A. Grothendieck 等'),
 'sga7-2': ('Groupes de monodromie en géométrie algébrique · II', 'P. Deligne · N. Katz 等'),
}

ready = set()
for report in (ROOT / 'reports').glob('*.json'):
    data = json.loads(report.read_text())
    if isinstance(data, dict) and data.get('status') == 'complete':
        ready.add(report.stem)
for v in volumes:
    for chunk in v.get('chunks', []):
        if v['id']+'-'+chunk['id'] in ready:
            chunk['status'] = 'complete'
MANIFEST.write_text(json.dumps(volumes, ensure_ascii=False, indent=2)+'\n')
registry = ['% Generated from completed per-chunk terminology declarations.\n']
for f in sorted((ROOT / 'glossary').glob('*.tex')):
    if f.stem in ready:
        registry.append(f'\\input{{glossary/{f.name}}}\n')
(ROOT / 'glossary' / 'registry.tex').write_text(''.join(registry))

active = []
for v in volumes:
    key = v['id']
    dest = ROOT / 'volumes' / key
    (dest / 'chunks').mkdir(parents=True, exist_ok=True)
    files = sorted(f for f in (dest / 'chunks').glob('*.tex') if key+'-'+f.stem in ready)
    body = ''.join(f'\\input{{volumes/{key}/chunks/{f.name}}}\n' for f in files)
    (dest / 'content.tex').write_text(body or '% 尚未开始翻译，正文模块为空。\n')
    pages = sorted(set(int(p) for f in files for p in re.findall(r'\\SourcePage\{(\d+)\}',f.read_text())))
    # Page markers indicate provenance, not proof of complete coverage.
    ranges = []
    for p in pages:
        if ranges and p == ranges[-1][-1] + 1: ranges[-1].append(p)
        else: ranges.append([p])
    provenance = '、'.join(str(r[0]) if len(r)==1 else f'{r[0]}—{r[-1]}' for r in ranges)
    note = ('当前收入模块的来源为原 PDF 第 '+provenance+' 页。' if pages else '本册尚无已收入的译文模块。')
    french, authors = META[key]
    cover = f'\\SGAcover{{{v["series"]}}}{{{v["title"]}}}{{{french}}}{{{authors}}}\n'
    source = v['source'].replace('_','\\_')
    start = f'\\BeginSGAVolume{{{key}}}{{{v["series"]}}}{{{source}}}\n'
    draft = v['translation_status'] != 'complete'
    main = '\\input{tex/preamble.tex}\n\\begin{document}\n'
    main += '\\SGADrafttrue\n' if draft else ''
    main += cover + '\\frontmatter\n' + start
    if draft: main += f'\\SGAdraftnotice{{{note}}}\n'
    main += '\\tableofcontents\n\\mainmatter\n'
    main += f'\\input{{volumes/{key}/content.tex}}\n\\PrintSGAGlossary\n\\end{{document}}\n'
    (dest / 'main.tex').write_text(main)
    if files: active.append((v, start, note))

total_complete = all(v['translation_status']=='complete' for v in volumes)
main = '\\input{tex/preamble.tex}\n\\begin{document}\n\\SGATotaltrue\n'
if not total_complete: main += '\\SGADrafttrue\n'
main += '\\SGAcover{SGA 1—7}{代数几何讨论班}{Séminaire de géométrie algébrique du Bois Marie}{A. Grothendieck 及各讲作者}\n\\frontmatter\n'
if not total_complete:
    main += '\\SGAdraftnotice{本阶段总本只汇集已有译文模块。全套来源共 5,146 个 PDF 页面；本文件并非全套完稿。}\n'
main += '\\tableofcontents\n\\mainmatter\n'
for v, start, note in active:
    main += start
    main += f'\\input{{volumes/{v["id"]}/content.tex}}\n\\PrintSGAGlossary\n'
main += '\\end{document}\n'
(ROOT / 'main-all.tex').write_text(main)
print(f'已生成十二个分册 main 和总 main；当前有译文模块的分册数：{len(active)}。')

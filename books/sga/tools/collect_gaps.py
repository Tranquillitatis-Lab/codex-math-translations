"""Collect source lacunae with page-addressable context for the user's report."""
from pathlib import Path
import json
import re

ROOT=Path(__file__).resolve().parents[1]
manifest={v['id']:v for v in json.loads((ROOT/'sources/manifest.json').read_text())}
existing_path = ROOT/'reports/missing-content.json'
existing = json.loads(existing_path.read_text()).get('gaps', []) if existing_path.exists() else []
retained_text = {(g['volume'], g['pdf_page']): g.get('original_page_text', '') for g in existing}
pages={}
gaps=[]
chapter_state={}
for path in sorted(ROOT.glob('volumes/*/chunks/*.tex')):
    volume=path.parent.parent.name
    report_path=ROOT/'reports'/f'{volume}-{path.stem}.json'
    if not report_path.exists():continue
    try:report=json.loads(report_path.read_text())
    except json.JSONDecodeError:continue
    if report.get('status')!='complete':continue
    source=path.read_text()
    markers=list(re.finditer(r'\\SourcePage\{(\d+)\}',source))
    chapters=list(re.finditer(r'\\SGAchapter\{([^{}]+)\}',source))
    ordinal=0
    for match in re.finditer(r'\\(?:SGAsourcegap|SGAunclear)\{',source):
        depth=1;end=match.end()
        while end<len(source) and depth:
            char=source[end]
            escaped=end>0 and source[end-1]=='\\'
            if not escaped and char=='{':depth+=1
            if not escaped and char=='}':depth-=1
            end+=1
        ordinal+=1
        prior=[m for m in markers if m.start()<match.start()]
        page=int(prior[-1][1]) if prior else None
        prior_chapters=[m for m in chapters if m.start()<match.start()]
        chapter=prior_chapters[-1][1] if prior_chapters else chapter_state.get(volume,'书前材料')
        if 'index' in path.stem:chapter='原书索引'
        if volume not in pages:
            file=ROOT/'sources'/volume/'pages.jsonl'
            pages[volume] = ({p['pdf_page']: p['text'] for p in (json.loads(line) for line in file.read_text().splitlines())}
                             if file.exists() else {page: text for (vol, page), text in retained_text.items() if vol == volume})
        description=source[match.end():end-1]
        explicitly_unfinished=('编者' in description and bool(re.search('待补|尚缺|未补|未完成',description)))
        item={'id':f'{volume}-{path.stem}-G{ordinal:02d}',
              'volume':volume,'chapter':chapter,'source_pdf':manifest[volume]['source'],'pdf_page':page,
              'chunk':path.stem,'description':description,
              'kind':'editorial_todo' if explicitly_unfinished else 'source_lacuna',
              'kind_zh':'原书编者明示待补' if explicitly_unfinished else '原文缺失（详说明）',
              'translated_context_tex':source[max(0,match.start()-240):min(len(source),end+240)],
              'original_page_text':pages[volume].get(page,''),
              'translation_file':str(path.relative_to(ROOT)),
              'translation_line':source.count('\n',0,match.start())+1,
              'chunk_report':str(report_path.relative_to(ROOT)),
              'reported_details':report.get('source_gaps',report.get('unresolved_readings',report.get('uncertainties',[])))}
        gaps.append(item)
    if chapters:chapter_state[volume]=chapters[-1][1]
out={'policy':'依用户指示保留原书缺失；不研究重建。完整译出全部现存内容，最终报告供用户寻找可补文本。',
     'page_numbering':'pdf_page为用户所给原文件的1基PDF页面，不是印刷页码。',
     'gaps':gaps}
(ROOT/'reports/missing-content.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(f'已登记 {len(gaps)} 处源缺失，含原文页上下文和译文位置。')

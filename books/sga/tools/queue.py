from source_paths import SOURCE_DIR
"""Small local queue owned and operated directly by the primary agent."""
from pathlib import Path
import collections
import json
import sys

ROOT=Path(__file__).resolve().parents[1]
path=ROOT/'reports/work-queue.json'
data=json.loads(path.read_text())
chunks=data['chunks']
mode=sys.argv[1] if len(sys.argv)>1 else 'status'
if mode=='show':
    volume,key=sys.argv[2:4]
    c=next(c for c in chunks if c['volume']==volume and c['id']==key)
    manifest=json.loads((ROOT/'sources/manifest.json').read_text())
    source=next(v['source'] for v in manifest if v['id']==volume)
    print(json.dumps({**c,'source_pdf':str(SOURCE_DIR/source)},ensure_ascii=False))
    sys.exit(0)
for c in chunks:
    report=ROOT/'reports'/f'{c["volume"]}-{c["id"]}.json'
    if report.exists():
        try:r=json.loads(report.read_text())
        except json.JSONDecodeError:continue
        if r.get('status')=='complete':c['status']='complete'
if mode=='next':
    volume=sys.argv[2] if len(sys.argv)>2 else None
    candidates=[c for c in chunks if c.get('status') in ('planned','pending','not_started') and (volume is None or c['volume']==volume)]
    print(json.dumps(candidates[0] if candidates else None,ensure_ascii=False))
    sys.exit(0)
elif mode=='claim':
    volume,key,agent=sys.argv[2:5]
    c=next(c for c in chunks if c['volume']==volume and c['id']==key)
    c.update(status='in_progress',agent=agent)
elif mode=='status':
    counts=collections.defaultdict(collections.Counter)
    for c in chunks:counts[c['volume']][c['status']]+=1
    print(json.dumps(counts,ensure_ascii=False))
temporary=path.with_suffix('.tmp')
temporary.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
temporary.replace(path)

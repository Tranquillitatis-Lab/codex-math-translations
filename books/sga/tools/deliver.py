"""Generate the twelve finished volumes, collected edition, and gap report."""
from pathlib import Path
import argparse
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--start-at',default=None)
args=parser.parse_args()
volumes=json.loads((ROOT/'sources/manifest.json').read_text())
if any(v['translation_status']!='complete' for v in volumes):
    sys.exit('全套译文尚未齐备，不能生成最终交付批次。')
logs=ROOT/'work/delivery-logs'
logs.mkdir(parents=True, exist_ok=True)
outputs=[]
started=args.start_at is None
for key in [v['id'] for v in volumes]+['all','missing-report']:
    name='缺失内容报告' if key=='missing-report' else ('SGA-1-7-总本' if key=='all' else key.upper())
    output=ROOT/'output/pdf'/(name+'.pdf')
    if key==args.start_at:started=True
    if not started:
        if not output.exists():sys.exit(f'前序交付文件尚未生成：{output}')
        outputs.append(str(output))
        print(f'沿用已生成：{name}.pdf',flush=True)
        continue
    print(f'正在生成：{key}',flush=True)
    command=[sys.executable,str(ROOT/'tools/build_gap_report.py')] if key=='missing-report' else [sys.executable,str(ROOT/'tools/build.py'),key]
    with (logs/(key+'.log')).open('w') as log:
        subprocess.run(command,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT,check=True)
    outputs.append(str(output))
    print(f'已生成：{name}.pdf',flush=True)
(ROOT/'output/deliverables.json').write_text(json.dumps({'pdfs':outputs,'source_project':str(ROOT),'missing_content_data':str(ROOT/'reports/missing-content.json')},ensure_ascii=False,indent=2)+'\n')
print('最终交付批次已生成。',flush=True)

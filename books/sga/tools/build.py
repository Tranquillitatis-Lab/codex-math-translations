"""Compile the requested edition with XeLaTeX through latexmk."""
from pathlib import Path
import argparse
import json
import os
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('volume', nargs='?', default='all')
parser.add_argument('--draft', action='store_true', help='允许编译带明确标注的阶段稿')
parser.add_argument('--prepared', action='store_true', help='使用批次已统一生成的输入文件')
args = parser.parse_args()
volumes = json.loads((ROOT/'sources/manifest.json').read_text())
keys = [v['id'] for v in volumes]
if args.volume != 'all' and args.volume not in keys:
    parser.error('volume 必须为 all 或 '+', '.join(keys))
selected = volumes if args.volume == 'all' else [v for v in volumes if v['id']==args.volume]
incomplete = any(v['translation_status']!='complete' for v in selected)
if incomplete and not args.draft:
    sys.exit('译文尚未完整。完稿构建已停止；如需阶段稿，请显式加 --draft。')
if not args.prepared:
    subprocess.run([sys.executable, str(ROOT/'tools/normalize_tex.py')], check=True)
    subprocess.run([sys.executable, str(ROOT/'tools/prepare_build.py')], check=True)
source = 'main-all.tex' if args.volume=='all' else f'volumes/{args.volume}/main.tex'
job = 'SGA-1-7-总本' if args.volume=='all' else args.volume.upper()
if incomplete: job += '-阶段稿'
build_dir = ROOT/'work'/'build'/args.volume
build_dir.mkdir(parents=True, exist_ok=True)
env = os.environ.copy()
env['PATH'] = '/Library/TeX/texbin:'+env.get('PATH','')
if args.volume=='all':
    # The collected edition keeps hundreds of thousands of occurrence anchors.
    # These Web2C overrides apply only to this compilation process.
    env.update(extra_mem_top='30000000',extra_mem_bot='20000000',
               pool_size='40000000',max_strings='1500000',hash_extra='1500000')
cmd = ['/Library/TeX/texbin/latexmk','-xelatex','-interaction=nonstopmode','-halt-on-error','-file-line-error',
       f'-outdir={build_dir}',f'-jobname={job}',source]
if args.volume=='all':cmd.insert(1,'-g')
subprocess.run(cmd, cwd=ROOT, env=env, check=True)
dest = ROOT/'output'/'pdf'/f'{job}.pdf'
dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_bytes((build_dir/f'{job}.pdf').read_bytes())
if not incomplete and args.volume!='all' and not args.prepared:
    manifest_path=ROOT/'sources/manifest.json'
    current=json.loads(manifest_path.read_text())
    volume=next(v for v in current if v['id']==args.volume)
    volume.update(compilation_status='complete',output_pdf=str(dest.relative_to(ROOT)))
    manifest_path.write_text(json.dumps(current,ensure_ascii=False,indent=2)+'\n')
    stage=dest.with_name(job+'-阶段稿.pdf')
    if stage.exists():
        archive=ROOT/'work/archive-drafts'/stage.name
        archive.parent.mkdir(exist_ok=True)
        suffix=2
        while archive.exists():
            archive=archive.with_name(stage.stem+f'-{suffix}.pdf')
            suffix+=1
        shutil.move(stage,archive)
print(dest)

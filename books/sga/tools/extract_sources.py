from source_paths import SOURCE_DIR
"""Preserve page-addressable source text without modifying source PDFs."""
from pathlib import Path
import json
import subprocess
import unicodedata
import fitz

ROOT = Path(__file__).resolve().parents[1]
VOLUMES = [
    ('sga1', 'SGA1.pdf', 'SGA 1', '平展覆盖与基本群'),
    ('sga2', 'SGA2.pdf', 'SGA 2', '凝聚层的局部上同调与局部及整体 Lefschetz 定理'),
    ('sga3-1', 'SGA3a.pdf', 'SGA 3 · 第一册', '群概形'),
    ('sga3-2', 'SGA3.b.pdf', 'SGA 3 · 第二册', '群概形'),
    ('sga3-3', 'SGA3.c.pdf', 'SGA 3 · 第三册', '群概形'),
    ('sga4-1', 'SGA 4-1.pdf', 'SGA 4 · 第一册', '拓扑斯理论与概形的平展上同调'),
    ('sga4-2', 'SGA 4-2.pdf', 'SGA 4 · 第二册', '拓扑斯理论与概形的平展上同调'),
    ('sga4-3', 'SGA 4-3.pdf', 'SGA 4 · 第三册', '拓扑斯理论与概形的平展上同调'),
    ('sga5', 'SGA 5.pdf', 'SGA 5', 'ℓ 进上同调与 L 函数'),
    ('sga6', 'SGA 6.pdf', 'SGA 6', '相交理论与 Riemann–Roch 定理'),
    ('sga7-1', 'SGA 7-1.pdf', 'SGA 7 · 第一册', '代数几何中的单值化群'),
    ('sga7-2', 'SGA 7-2.pdf', 'SGA 7 · 第二册', '代数几何中的单值化群'),
]

manifest_path = ROOT / 'sources/manifest.json'
previous = {v['id']: v for v in json.loads(manifest_path.read_text())} if manifest_path.exists() else {}
manifest = []
for key, filename, series, title in VOLUMES:
    source = SOURCE_DIR / filename
    dest = ROOT / 'sources' / key
    dest.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(source)
    full = subprocess.check_output(['/opt/homebrew/bin/pdftotext', '-layout', str(source), '-']).decode('utf-8')
    pages = full.split('\f')
    if pages[-1].strip() == '':
        pages.pop()
    with (dest / 'pages.jsonl').open('w') as out:
        for i in range(len(doc)):
            text = unicodedata.normalize('NFC', pages[i] if i < len(pages) else doc[i].get_text())
            item = {'pdf_page': i + 1, 'text': text, 'image_count': len(doc[i].get_images()), 'chars': len(text.strip())}
            out.write(json.dumps(item, ensure_ascii=False) + '\n')
    (dest / 'full.txt').write_text(full)
    (dest / 'outline.json').write_text(json.dumps(doc.get_toc(), ensure_ascii=False, indent=2))
    volume = {'id': key, 'source': filename, 'series': series, 'title': title, 'pdf_pages': len(doc),
              'source_kind': 'scan_with_ocr' if key in ('sga5', 'sga6', 'sga7-1', 'sga7-2') else 'digital_typeset',
              'translation_status': 'not_started', 'chunks': []}
    volume = {**volume, **previous.get(key, {})}
    manifest.append(volume)
    print(f'{key}: {len(doc)} pages; {len(doc.get_toc())} outline entries')
(ROOT / 'sources' / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')

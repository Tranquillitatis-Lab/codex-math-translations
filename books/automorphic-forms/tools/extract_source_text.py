"""Recreate optional text caches from the two original PDFs without changing metadata."""
from pathlib import Path
import json
import os
import subprocess
P = Path(__file__).resolve().parents[1]
default_sources = P.parents[1] / '.local/originals/automorphic-forms'
SOURCE_DIR = Path(os.environ.get('AUTOMORPHIC_SOURCE_DIR', str(default_sources))).expanduser()
volumes = {}
for volume in (1, 2):
    metadata = json.loads((P / f'volume-{volume}-pages.json').read_text())
    pages = subprocess.check_output(['pdftotext', '-layout', str(SOURCE_DIR / metadata['source']), '-']).decode().split('\f')
    for record in metadata['pages']:
        destination = P / record['text_file']
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(pages[record['pdf_page'] - 1])
    volumes[volume] = metadata
for article in json.loads((P / 'articles.json').read_text()):
    records = volumes[article['volume']]['pages'][article['pdf_start'] - 1:article['pdf_end']]
    text = '\n\n'.join(
        f'===== PDF PAGE {r["pdf_page"]} / PRINTED PAGE {r["printed_page"]} =====\n'
        + (P / r['text_file']).read_text() for r in records)
    (P / 'source-text' / f'{article["id"]}-{article["slug"]}.txt').write_text(text)
print(P / 'source-text')

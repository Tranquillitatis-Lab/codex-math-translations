#!/usr/bin/env python3
"""Dispatch existing book build commands without introducing another TeX toolchain."""
from pathlib import Path
import argparse
import subprocess
import shutil
import sys
ROOT = Path(__file__).resolve().parents[1]
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('book', choices=['sga', 'sga4-5', 'fga', 'arithmetic-algebraic-geometry', 'automorphic-forms', 'functorial-algebraic-geometry', 'faisceaux-pervers'])
p.add_argument('volume', nargs='?', default='all', help='SGA volume, e.g. sga1, sga3-2, all')
a = p.parse_args()
commands = {
    'sga': [sys.executable, 'tools/build.py', a.volume],
    'sga4-5': [sys.executable, 'tools/build.py'],
    'fga': [sys.executable, 'tools/build.py'],
    'arithmetic-algebraic-geometry': ['make'],
    'automorphic-forms': ['make'],
    'functorial-algebraic-geometry': [sys.executable, 'build_book.py'],
    'faisceaux-pervers': ['zsh', 'build.sh'],
}
subprocess.run(commands[a.book], cwd=ROOT/'books'/a.book, check=True)

if a.book == 'fga':
    out = ROOT/'books/fga/output/pdf'
    shutil.copyfile(out/'main.pdf', out/'FGA-代数几何基础-中文译本.pdf')

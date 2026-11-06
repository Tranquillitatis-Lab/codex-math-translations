"""Resolve local original PDFs without embedding a contributor's home directory."""
from pathlib import Path
import os
ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = Path(os.environ.get('SGA_SOURCE_DIR', str(ROOT.parents[1] / '.local/originals/sga'))).expanduser()

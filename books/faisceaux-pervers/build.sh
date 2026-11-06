#!/bin/zsh
set -eu
cd "${0:A:h}"
export PATH="/Library/TeX/texbin:/opt/homebrew/bin:$PATH"
if [[ -x /opt/anaconda3/bin/python ]]; then
  /opt/anaconda3/bin/python tools/prepare.py
  /opt/anaconda3/bin/python tools/layout.py
else
  python3 tools/prepare.py
  python3 tools/layout.py
fi
mkdir -p output/pdf
# Three passes resolve contents, source locations, and all glossary return links.
xelatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=output/pdf -jobname=反常层-中文译本 main.tex
xelatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=output/pdf -jobname=反常层-中文译本 main.tex
xelatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=output/pdf -jobname=反常层-中文译本 main.tex

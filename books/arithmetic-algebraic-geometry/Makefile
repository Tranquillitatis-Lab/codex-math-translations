SHELL := /bin/zsh
.PHONY: all prepare clean
all: prepare
	mkdir -p output/pdf
	PATH="/Library/TeX/texbin:$$PATH" latexmk -xelatex -interaction=nonstopmode -halt-on-error -file-line-error -jobname=arithmetic-algebraic-geometry-zh-annotated -outdir=output/pdf main.tex
prepare:
	python3 tools/prepare.py
clean:
	PATH="/Library/TeX/texbin:$$PATH" latexmk -c -jobname=arithmetic-algebraic-geometry-zh-annotated -outdir=output/pdf main.tex

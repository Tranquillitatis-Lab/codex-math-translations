LATEXMK := /Library/TeX/texbin/latexmk
BOOK_PDF := output/pdf/自守形式、表示与L函数-中文合订本.pdf

.PHONY: all clean
all:
	$(LATEXMK) -xelatex -interaction=nonstopmode -halt-on-error -outdir=output/pdf main.tex
	mv -f output/pdf/main.pdf "$(BOOK_PDF)"
	$(MAKE) clean

clean:
	$(LATEXMK) -c -outdir=output/pdf main.tex
	rm -f output/pdf/main.xdv output/pdf/main.synctex.gz

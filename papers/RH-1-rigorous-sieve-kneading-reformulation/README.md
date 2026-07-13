# Rigorous sieve-kneading reformulation

This folder contains the source for the first theory-focused follow-up paper.

- `main.tex`: manuscript source
- `references.bib`: bibliography
- `rigorous-sieve-kneading-reformulation.pdf`: final verified manuscript

Build from this directory with:

```powershell
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

If `latexmk` is unavailable, use:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The manuscript cites Paper 1 as a published article and Papers 2-5 as manuscripts under review.

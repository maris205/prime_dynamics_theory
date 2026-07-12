# Exact prime kneading orbit and spectral stability

This folder contains the source and reproducibility script for the second theory-focused paper.

- `main.tex`: manuscript source
- `references.bib`: bibliography
- `estimate_prime_parameter.py`: standard-library decimal computation of the nested prime-prefix parameter cylinders
- `exact-prime-kneading-spectral-stability.pdf`: final verified manuscript

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

Reproduce the parameter-cylinder table with:

```powershell
python estimate_prime_parameter.py
```

The numerical computation is auxiliary. The existence, uniqueness, repair, statistical-stability, and periodogram-stability results are analytic.

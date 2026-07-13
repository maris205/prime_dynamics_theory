# Parity-resolved band-merging spectrum

This folder contains the source for the third theory-focused paper:

> *Parity-Resolved Dynamics at a Quadratic Band-Merging Parameter: Peripheral Spectrum, Periodograms, and Two-Step Sequential Stability*

- `main.tex`: manuscript source
- `references.bib`: bibliography
- `parity-resolved-band-merging-spectrum.pdf`: final verified manuscript

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

The paper proves the exact period-two geometry and parity eigenmode at the first quadratic band-merging parameter, identifies the resulting spectral atom at frequency `1/2`, and proves almost-sure weak convergence of finite orbit periodograms for bounded real observables. Under an explicit two-step component spectral-gap hypothesis it derives the full parity-resolved Perron--Frobenius decomposition and analytic continuous spectral remainder.

For non-autonomous maps, the paper proves abstract rank-two tracking and paired Birkhoff theorems under stated cocycle and block-memory hypotheses. It does not claim that every prescribed logarithmic quadratic schedule satisfies those hypotheses.

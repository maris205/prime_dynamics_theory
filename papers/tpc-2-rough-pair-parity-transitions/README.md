# Polynomial-Scale Rough Pairs

This directory contains the source, reproducible experiments, figures, and compiled PDF for the next theory paper in the twin-prime branch of the prime-dynamics program.

## Intended scope

The paper studies two quantitative gaps between finite rough-pair counts and genuine prime-pair counts:

- the gap between the range where a baseline dimension-two lower sieve is positive and the range where every rough survivor is exactly a prime or semiprime;
- the additional parity-allocation gap between a positive rough-pair count and a positive prime-prime sector.

The paper does not prove a twin-prime lower bound. Its rigorous results concern beta-sieve envelopes, Buchstab parity bias, slow-cutoff logarithmic parity balance, finite-factor sector inversion, and a complete-period local bilinear spectrum. The experiments are diagnostics, not substitutes for Type-II estimates.

## Files

- `main.tex` - manuscript source
- `references.bib` - bibliography
- `experiments/` - reproducible counting and plotting code
- `experiments/data/` - retained exact counts for `X=10^8` and four even shifts
- `figures/` - generated figures used in the manuscript
- `polynomial-rough-pair-parity-transitions.pdf` - compiled manuscript

## Build

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

The production experiment, compiler information, and SHA-256 hashes are recorded in `experiments/MANIFEST.md`. The count and histogram fields are deterministic; the `elapsed_seconds` column is intentionally machine-dependent.

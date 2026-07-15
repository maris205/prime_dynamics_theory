# TPC-17 — Assembled Prefixes and TT* Dispersion

Paper title:

> *Assembly and Concentration at a Fixed-Shift Type-II Gate: Cumulative
> Divisor Prefixes, Bilinear Distribution Frontiers, and TT* Dispersion*

## Main results

- The TPC-16 dyadic divisor slices are assembled into a direct
  sharp-prefix estimate for the complete coefficient
  `beta_{<=D0}(k) = sum_{d|k, d<=D0} mu(d)`.
- Using Maynard's published 2025 theorem, the complete prefix reaches
  `D0 = X^(1/21-o(1))` near `L = X^(10/21-o(1))`.
- A separately labelled, version-locked extension using Runbo Li's
  unrefereed arXiv v6 removes the third Maynard constraint. Its exponent
  polytope has vertex `(8/17, 1/17)` and total modulus exponent `9/17`.
- The unresolved symmetric packet is reduced exactly to the signed tail
  `D0 < d <= V`; the tail itself is not estimated.
- For the square-root dyadic block, the coefficient energy is bounded by
  `O(X log^3 X)`. Exact Nyquist Parseval, flat-top localization, and a
  TT* expansion show that a failed zero-phase estimate forces a large
  off-diagonal residual two-form correlation.
- A random-mask theorem and an abstract countermodel show why phase
  energy alone cannot eliminate the distinguished deterministic zero
  mode.

The paper does **not** prove a fixed-shift Hardy–Littlewood asymptotic,
infinitely many twin primes, a new distribution theorem, or a breach of
the sieve parity barrier.

## Dependency split

- Published core: James Maynard, *Primes in Arithmetic Progressions to
  Large Moduli I*, Memoirs AMS 306 (2025), no. 1542.
- Version-locked extension: Runbo Li, arXiv:2602.20917v6, revised
  27 May 2026. This extension must be rechecked if the preprint changes.
- Fourier, random-mask, and TT* results: independent of Li v6.

## Files

- `main.tex` and `sections/*.tex`: paper source.
- `references.bib`: bibliography.
- `experiments/tpc17_certificate.py`: exact exponent and finite Fourier
  checks.
- `experiments/tpc17_certificate.json`: generated certificate.
- `assembled-prefixes-ttstar-dispersion.pdf`: compiled paper.

## Reproduce the certificate

```bash
python experiments/tpc17_certificate.py \
  --output experiments/tpc17_certificate.json
```

## Compile

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

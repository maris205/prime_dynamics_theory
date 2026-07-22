# RH-76: single-arc phase-compression barrier

This directory contains the seventy-sixth RH-layer paper:

> *Single-Arc Phase Compression Does Not Explain the Production Horizons*

## Exact theorems

For a unitary operator `U` and source `x` with spectral measure `mu`,

    dist(U^M x, K_d(U,x))^2
      = inf_{deg p < d} integral |z^M-p(z)|^2 dmu(z).

If the support lies in an arc of width `w`, truncating the binomial expansion
around the arc center gives a degree-`d-1` upper with remainder

    sum_{j=d}^M binom(M,j) [2 sin(w/4)]^j.

Conversely, small phase moments give the coherence lower

    residual^2 >= 1 - d mu^2/[1-(d-1)mu].

Thus useful depth reduction needs genuine phase localization or strong moment
structure.

## Production surrogate audit

The source-weighted frozen Schur phases are treated as an exact-dyadic normal
surrogate and audited with 192-bit Arb moment Gramians.

- At `sigma=0.01`, the 99% arcs have widths `5.9034` (left) and `5.8465`
  (right), close to the full circle `2 pi`.
- At depth `M=32`, the certified normal-surrogate residuals are above `0.7709`
  and `0.6114`.
- Both finest channels require depth `M+1=33` even for 10% error.
- Nine of ten channels require full depth for 10%; all ten require full depth
  for 1%, except that “full depth” is counted relative to their own horizon.

## Route consequence

Single-arc phase compression is marked as a failed branch. This does not
invalidate the log-square block law or Stage-A route: broad phase support can
still have low weighted effective rank, multi-arc structure, or rapid radial
decay. RH-77 tests that fallback.

The Schur decomposition itself is a frozen binary64 diagnostic; no continuum
phase-measure theorem is claimed.

## Reproduction

~~~bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_phase_compression_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf single-arc-phase-compression-barrier.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
~~~

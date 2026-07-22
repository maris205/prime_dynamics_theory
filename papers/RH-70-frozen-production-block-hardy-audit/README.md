# RH-70: frozen-production block Hardy audit

This directory contains the seventieth RH-layer paper:

> *Outward-Rounded Block Hardy Certificates for Frozen Production Matrices*

## Main theorem

For finite matrices A, X, and Y, set

    E^2 = sum_{n>=0} ||Y A^n X||_F^2.

If q_M = ||A^M||_F < 1, then

    E^2 <= sum_{r=0}^{M-1} ||Y A^r X||_F^2
           + ||Y||_F^2 q_M^2/(1-q_M^2)
             sum_{r=0}^{M-1} ||A^r X||_F^2.

The bound is exact in the scalar case. Every stable finite matrix admits a
sufficiently large block horizon with q_M < 1.

## Exact-dyadic interval audit

The production pipeline first creates binary64 arrays. Each entry is then
embedded into Arb/Acb as its exact dyadic rational; all subsequent block
powers, Frobenius energies, margins, and divisions are outward rounded at
128-bit precision.

Across sigma = 0.16, 0.08, 0.04, 0.02, 0.01, with horizons
4, 9, 16, 25, 32, all ten left/right frozen-matrix certificates are green:

- every ||A^M||_F < 0.022 is certified;
- every full upper is at most 1.009370 times its certified finite prefix;
- every archived binary64 Stein energy lies inside the corresponding
  certified lower/upper bracket.

## Claim boundary

This is a two-layer result.

- **Frozen green:** the exact dyadic arrays actually passed to Arb/Acb have
  rigorous terminal Hardy certificates.
- **End-to-end amber:** folded-Gaussian assembly, spectral deflation, and
  source/observation transfer are still performed in binary64 before the
  frozen arrays are formed.

Therefore Stage A1 is not closed. The remaining validation gate has moved
upstream; it is no longer the terminal block-tail calculation.

The augmented block-diagonal construction in production_hardy realizes the
transfer-sequence difference between a frozen model and an upstream-enclosed
model. It provides the next interval bridge without changing the certificate
architecture.

## Reproduction

~~~bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=16 OMP_NUM_THREADS=16 \
  /root/math/.venv/bin/python experiments/run_frozen_production_interval_audit.py
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 \
  /root/math/.venv/bin/python experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf frozen-production-block-hardy-audit.pdf
PYTHONDONTWRITEBYTECODE=1 \
  /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 \
  /root/math/.venv/bin/python experiments/verify_archive.py
~~~

# RH-73: validated peripheral rank-two deflation

This directory contains the seventy-third RH-layer paper:

> *Validated Peripheral Rank-Two Deflation for Repaired Folded-Gaussian Matrices*

## Main theorems

For an exact stochastic matrix `A`, the stationary left vector is recovered
from

    L = I - A^T + 11^T/n.

If an outward-rounded approximate inverse `B` satisfies
`||I-BL||_F < 1`, then `L` is invertible, the Perron eigenvalue is simple,
and the stationary-vector error is bounded by the corresponding Neumann
correction.

The negative parity eigenpair is validated with a bordered Newton map.  If

    beta + gamma*rho + M*rho^2 <= rho,
    gamma + M*rho < 1,

then the joint right-eigenpair ball contains a unique zero.  A second bordered
linear solve validates the left parity vector at that eigenvalue.  The two
vector balls give an explicit normalized rank-one projector bound and hence a
complete Perron/parity rank-two deflation bound.

A Euclidean Grushin/Rouche ledger independently proves that the radius `0.01`
circle around every reported parity center contains exactly one eigenvalue.

## Five-scale certificate

At `sigma = 0.16, 0.08, 0.04, 0.02, 0.01`, for both fine and Haar-coarse
exact stochastic repaired matrices:

- every stationary system is invertible and the Perron eigenvalue is simple;
- every negative parity right and left eigenvector is validated;
- every radius `0.01` parity contour has count one;
- the largest rank-two projector error is below `9.20e-14`;
- the largest deflated-bulk error is below `9.41e-14`;
- the largest contour transport product is below `0.241`.

All Gram products, residuals, projector normalizations, and final error bounds
are computed from exact dyadic matrix/vector data in 160-bit Arb arithmetic.

## Route consequence

The repaired finite matrices now possess a validated stationary Perron factor,
a validated negative parity Riesz factor, and a certified rank-two deflation.
The next finite-scale gate is to propagate these balls through the normalized
source/observation construction and compare the resulting upstream triple with
the frozen triple used by RH-70's Hardy audit.  No small-noise uniform theorem
or RH claim is made here.

## Reproduction

~~~bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/run_validated_peripheral_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf validated-peripheral-rank-two-deflation.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/verify_archive.py
~~~

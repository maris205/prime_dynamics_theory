# RH-72: validated folded-Gaussian assembly

This directory contains the seventy-second RH-layer paper:

> *Validated Folded-Gaussian Assembly and Exact Stochastic Repair*

## Main theorems

For positive row weights, let P be the fully normalized row and S the same
row restricted to a support J and renormalized. If Z_out is the omitted mass
and Z is the full mass, then

    ||P - S||_1 = 2 Z_out / Z.

For a nonnegative frozen binary64 row, leave every entry except its largest
unchanged and replace the largest entry by one minus the exact dyadic sum of
the others. This gives an exactly stochastic dyadic row. Its distance from
the frozen row is exactly the original row-sum defect, and the constant
vector is now an exact Perron right vector.

If outward-rounded row and column sums bound the absolute matrix defect by
R and C, then

    ||P - F||_2 <= sqrt(R C).

The same defect propagates through exact/frozen Haar coarse and detail
embeddings with an explicit three-term product bound.

## Five-scale certificate

At sigma = 0.16, 0.08, 0.04, 0.02, 0.01:

- every support-center floor is interval-stable;
- the maximum full-to-8-sigma sparse row L1 defect is below 9.58e-17;
- the finest full-to-repaired matrix 2-norm defect is below 1.50e-14;
- the finest Haar coarse/cross assembly defect is below 1.54e-14;
- the largest exact stochastic correction is below 3.87e-16;
- every repaired pivot remains above 0.0775.

The algebraic parameter is independently enclosed as the unique root of

    u^3 - 2 u^2 + 2 u - 2 = 0

inside the archived interval.

## Route consequence

Kernel evaluation, sparse truncation, row normalization, the Haar constants,
and the Perron right vector are no longer active finite-scale gates. The next
paper should validate the stationary Perron left vector and the parity Riesz
pair, then assemble the complete rank-two deflation.

This paper validates a midpoint matrix family. The continuum/Ulam transfer is
inherited from the earlier strong--weak cutoff theory and is not re-proved
here. Stage A1 remains open.

## Reproduction

~~~bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/run_interval_assembly_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf validated-folded-gaussian-assembly.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python \
  experiments/verify_archive.py
~~~

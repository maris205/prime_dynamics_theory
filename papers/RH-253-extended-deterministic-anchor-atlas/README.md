# RH-253: Extended Deterministic Anchor Atlas

RH-252 supplies the analytic all-order target-tail interface.  This paper
extends the exact deterministic coefficient dictionary of RH-243 from orders
`2--12` to orders `2--28` using the archived Collet--Eckmann periodic-point
formula.  The new block contains 16 orders and, at order 28, 32,767 physical
fixed points.

The order-13--28 unit-disk logarithmic contribution is
`0.0021942543215719553`, while the order-2--28 finite norm is
`0.496699690013014`.  A log-linear fit to the new finite coefficients has root
rate `0.7009986349...`; this is a descriptive finite fit, not an all-order
envelope or a cloud identification.

Gates A--E remain false/open.  No Hilbert--Polya operator, zeta-divisor
equality, Riemann-zero identification, or RH implication is claimed.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_extended_anchor_atlas.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python -m pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf extended-deterministic-anchor-atlas.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```

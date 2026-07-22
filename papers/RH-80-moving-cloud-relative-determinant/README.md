# RH-80: moving-cloud relative determinant

This directory contains the eightieth RH-layer paper:

> *Moving-Cloud Renormalization and the Relative Determinant Gate*

## Main result

The canonical finite cloud resolving the deterministic double pole is

    C_N(w) = Pi_N(w/lambda)^2.

Writing `q=w/lambda` gives the exact identity

    (1-q)^2 C_N(w) = (1-q^(N+1))^2.

Consequently, multiplying by the fixed limiting pole factor works uniformly
on every strict interior disk `|q|<=r<1`, with error at most

    2 r^(N+1) + r^(2N+2),

but it grows exponentially at every fixed point `|q|>1`. Thus fixed scalar
pole cancellation cannot open a disk crossing `|w|=lambda`, even in the
exact canonical model.

The correct sufficient construction is an exact moving spectral factor. If
`P_sigma` is a finite-rank reducing cloud projection for
`T_sigma=B_sigma^2`, then

    det(I-w T_sigma) = C_sigma(w) R_sigma(w),

where `C_sigma` is the finite cloud polynomial and `R_sigma` is the Fredholm
determinant of the complementary block. A uniform trace-norm bound on that
complement makes `{R_sigma}` a normal family on every fixed disk. Trace-norm
convergence gives quantitative locally uniform convergence by the standard
determinant inequality.

This is a sufficient relative-determinant gate, not a construction of the
required cloud projection for the present dynamics.

## Archived cloud audit

A 256-bit Arb replay propagates the archived RH-15 decimal resonance cloud
coordinates through the RH-46 two-step centering calculation. At the finest
level `sigma=1e-4`:

- the selected cloud degree is `N=7`;
- the centered two-step radius is `1.8751435740`, still `11.71%` above the
  deterministic pole `lambda=1.6785735104`;
- the selected zero-radius band is `[1.7449450709, 1.9816784182]`;
- on edge coordinates `s=-1,-1/2,0,1/2,1`, the mean error from the finite
  geometric profile is at most `0.03632944`, and the maximum is at most
  `0.11589965`.

The audit supports a moving-cloud interpretation but does not prove a Riesz
projection or a uniformly trace-class complement. Stage A5 therefore remains
open, now with a precise operator-theoretic target.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_cloud_renormalization_audit.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_cloud_renormalization_audit.py --smoke
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf moving-cloud-relative-determinant.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```


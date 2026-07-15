# Primal--dual directional certificate

This directory contains the twenty-sixth-layer paper in the quadratic
prime-dynamics spectral program:

> *Primal--Dual Residual Squaring for Directional Feshbach Certification at
> a Quadratic Band-Merging Map: Goal-Oriented Error Identities, Enlarged
> Resolvent Budgets, and an Inverse-Information No-Go Theorem*

RH-25 reduced the exact Feshbach error to a low-rank directional solve. RH-26
adds an adjoint solve and proves the exact identity

```text
r = R - A_z Y_hat,
s = E* - A_z* Z_hat,

-E A_z^(-1) R
  = -E Y_hat - Z_hat* r - s* A_z^(-1) r.
```

The first two terms are computable packet matrices. The remaining term
contains both the primal and dual residuals. If `M >= ||A_z^(-1)||_2`, its
preconditioned matrix-Rouché contribution is bounded by

```text
M ||F_J^(-1) s*||_2 ||r||_2.
```

This defines an admissible resolvent budget

```text
M_* = (1 - ||F_J^(-1) Delta_hat||_2)
      / (||F_J^(-1) s*||_2 ||r||_2).
```

The paper also proves a no-free-lunch theorem: unit primal and dual
residuals can produce an arbitrarily large bilinear remainder even when
`||A_z||_2 <= 1`. Primal--dual residual squaring greatly enlarges the
acceptable inverse bound, but cannot remove the need for some inverse
information unless one residual is exactly zero.

## Main finite-matrix results

Across seven scales from `sigma=1e-2` to `1e-4`:

- dimensions range from 2,048 to 204,800 and packet ranks from 4 to 9;
- every deepest-dual corrected 32-node determinant has sampled winding 1;
- the maximum computed primal--dual Rouché ratio is `4.9720e-11`;
- the minimum one-sided resolvent budget is `4.2166e10`;
- the minimum primal--dual resolvent budget is `3.3518e24`;
- the worst pointwise budget gain is `5.4823e13`;
- the minimum budget divided by the RH-23 physical one-vector lower bound is
  `8.9347e22`—a conditioning comparison only, not an upper-bound proof;
- deep primal and dual true residuals are at most `2.91e-13` and
  `2.63e-14`, respectively;
- changing the dual depth from `J` through `J+8` to `J+16` changes the
  minimum budget by at most 2.83%.

At the two informative smallest scales, the maximum primal--dual correction
agrees with the independent RH-25 direct correction to within 0.58% and
0.39%.

The evidence hierarchy remains essential. The primal--dual identity,
conditional Rouché criterion, budget formula, and no-go theorem are exact
finite-dimensional results. The tabulated residuals, budgets, and windings
are floating-point evidence. No interval residual enclosure, rigorous
complement-resolvent upper bound, continuous contour certificate, continuum
theorem, or small-noise theorem is claimed.

## Reproduction

Run the seven unit tests:

```bash
PYTHONPATH=src /root/math/.venv/bin/pytest -q
```

Run the complete seven-scale audit:

```bash
PYTHONPATH=src:experiments OPENBLAS_NUM_THREADS=16 \
  /root/math/.venv/bin/python experiments/run_primal_dual_audit.py
```

Resume an interrupted run while preserving completed scales:

```bash
PYTHONPATH=src:experiments OPENBLAS_NUM_THREADS=16 \
  /root/math/.venv/bin/python experiments/run_primal_dual_audit.py --resume
```

Regenerate figures and metadata from committed tables:

```bash
PYTHONPATH=src:experiments /root/math/.venv/bin/python \
  experiments/run_primal_dual_audit.py --reuse
```

Build the manuscript:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The committed results contain 672 contour/depth rows, seven scale summaries,
source hashes, software versions, timings, and PDF/PNG figures.

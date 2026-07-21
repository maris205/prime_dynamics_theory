# RH-57: mixed Haar-channel Riesz overlap budgets

This directory contains the fifty-seventh RH-layer paper:

> *Mixed Haar-Channel Riesz Overlap Budgets: Cross-Stein Identities and a
> Radial-Block Obstruction*

## Main result

For a stable finite operator `A`, source `X`, observation `Y`, and any Riesz
partition `P_j`, the complete directional Hardy response has a positive
cross-block Gram matrix

```text
K[j,k] = tr(Y P_j G P_k^* Y^*)
G - A G A^* = X X^*
E^2 = sum_{j,k} K[j,k]
```

The normalized block matrix gives the sufficient upper bound

```text
E^2 <= lambda_max(C) * sum_j K[j,j]
```

where `C[j,k] = K[j,k]/sqrt(K[j,j] K[k,k])`. The exact signed aggregate is
measured by

```text
eta = (1^* K 1) / tr(K).
```

The theorem is finite-dimensional and does not require normality,
diagonalizability, or individual eigenvector condition estimates. For simple
modes it reduces to the geometric Hardy Cauchy kernel

```text
tr(Z_j Z_k^*) / (1 - mu_j conjugate(mu_k) / r^2).
```

## What the audit found

The deterministic dense audit uses the RH-51 folded-Gaussian family with
`N*sigma=5.12`, five scales, and fixed physical radial cuts `0.15, 0.35,
0.55`. It includes every source column and solves the full Lyapunov Gramian.

- The exact aggregate energies at `sigma=0.01` are `1.4681` (left) and
  `1.7603` (right), matching the prior all-column audit.
- The corresponding coherence-weighted radial-block uppers are `81.68` and
  `672.41`.
- The largest radial Riesz projector norms are about `2705.75` and `2531.73`.
- The signed fusion ratios at that scale are about `6.48e-4` and `1.38e-5`.
- Reconstruction, partition, and Stein residuals remain at binary64 precision.

The conclusion is a route boundary, not a Hardy-divergence theorem. Fixed
radial Riesz blocks are too oblique for a uniform absolute or worst-direction
coherence budget in this audit. The exact cross-Stein quadratic form remains
the right object for a direct signed estimate, angular cloud construction, or
time-ordered Schur/observability treatment.

## Evidence boundary

Analytic or exact in the stated finite-dimensional scope:

- the cross-Stein Riesz identity;
- the normalized coherence and Gershgorin bounds;
- the simple-mode Cauchy kernel;
- the block prefix-tail implication;
- the scalar two-block Arb formula audit.

Binary64 diagnostic only:

- production eigenspaces and grouped Riesz projectors;
- five-scale Lyapunov energies and fitted slopes;
- projector norms and block coherence values.

Still open:

- a dyadically uniform cross-Stein budget for the physical small-noise family;
- RH-54 Stage A1 and unconditional Stage A4 intrinsic identification;
- an arithmetic prime-power trace formula, zeta-zero identity, self-adjoint
  Hilbert-Polya operator, `T log T` law, or Riemann-hypothesis result.

## Reproduction

From this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_overlap_pilot.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_arb_block_audit.py
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf mixed-haar-channel-overlap-budget.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```

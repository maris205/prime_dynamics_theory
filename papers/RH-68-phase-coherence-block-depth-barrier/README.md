# RH-68: phase-coherence block-depth barrier

This directory contains the sixty-eighth RH-layer paper:

> *Phase-Coherence Barriers to Uniform Block Krylov Depth*

## Exact no-go theorem

Let

```text
A_d = q diag(1, omega, ..., omega^(d-1)),
z_d = d^(-1/2) (1,...,1),
omega = exp(2 pi i / d).
```

The normalized Krylov vectors

```text
v_m = q^(-m) A_d^m z_d
```

are the discrete Fourier basis. Therefore, for `k <= L < d`,

```text
distance(v_L, span(v_0,...,v_(k-1))) = 1.
```

The canonical Lyapunov metric is a scalar multiple of the identity, with
condition number one, and every residual still contracts exactly by `q`.
Thus stability, spectral radius, and perfect metric conditioning cannot imply
a universal fixed block depth.

## Robust theorem

For a basis Gram `G` and target correlations `c`,

```text
distance^2 = 1 - c* G^(-1) c
           >= 1 - ||c||^2 / lambda_min(G).
```

If all mutual coherences are at most `mu`, then for `p` block Krylov vectors

```text
distance^2 >= 1 - p mu^2 / (1-(p-1)mu).
```

This extends directly to block width `r` by taking `p = k r`.

## Audit

- Exact rings with horizons `8,16,32,64` require depths `9,17,33,65` for
  10% projection error.
- A 0.5-cell deterministic phase perturbation still has error `0.9851` at
  depth 32 for horizon 32.
- At horizon 32, compressing the phase support to arcs of widths
  `0, 0.03, 0.1, 0.3, 1, 3, 2pi` changes the required depth to
  `1,2,3,7,16,28,33`.

A 256-bit Arb/Acb audit certifies the displayed eight-point Fourier ring.

## Route consequence

The route remains open only through physical phase compression, weighted
effective-rank decay, or a proved admissible growing-depth budget. RH-69
should combine these alternatives into one adaptive certificate ledger.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_depth_barrier_pilot.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_arb_fourier_ring_audit.py
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf phase-coherence-block-depth-barrier.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```

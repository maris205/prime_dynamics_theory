# Parity-renormalized long-cycle determinants

This directory contains the tenth-layer theory paper in the quadratic
prime-dynamics program:

> *Parity-Renormalized Long-Cycle Determinants at a Quadratic Band-Merging
> Map: Exact Markov Counts, Noncommuting Small-Noise Limits, and a
> Logarithmic Cycle Horizon*

## Main results

- At the algebraic band-merging parameter, the exact number of physical roots
  of `f^m(x)=x` is `1` for odd `m` and `2^(m/2+1)-1` for even `m`.
- An explicit primitive even cycle approaches the noise boundary with
  clearance `Theta(lambda^(-m))`, where
  `lambda=2*u_c*(u_c-1)`. Consequently the fixed-length localization theorem
  can only be used uniformly through a logarithmic cycle horizon.
- For every fixed positive noise, compact strong positivity forces
  `tr(K_sigma^m) -> 1`. Under an explicitly stated deterministic flat-trace
  gap hypothesis, the opposite iterated limit along even lengths is `2`.
  Thus the small-noise and long-cycle limits do not commute.
- Removing the Perron and parity modes gives the correct Hilbert--Schmidt
  regularized bulk determinant. The deterministic parity factor is exactly
  `1-z^2`.
- Numerically, the negative resonance satisfies
  `1+lambda_-(sigma) ~ sigma^(2/3)` over the resolved tail. This exponent is
  reported as evidence, not as a theorem.

## Reproduction

Run the unit tests:

```bash
/root/math/.venv/bin/python -m pytest -q
```

Regenerate all numerical tables and figures:

```bash
PYTHONPATH=src OPENBLAS_NUM_THREADS=8 \
  /root/math/.venv/bin/python experiments/run_long_cycle_audit.py
```

Build the manuscript:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The experiment diagonalizes folded dense matrices through dimension `2560`.
It is intended for a multicore machine, while the tests are lightweight.

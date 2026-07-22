# RH-65: physical-family Lyapunov metric conditioning

This directory contains the sixty-fifth RH-layer paper:

> *Conditioning Thresholds for Lyapunov Metrics on Near-Peripheral
> Jordan Families: Why Global Weighting Must Follow Directional Deflation*

## Main result

For the canonical metric

```text
M - A* M A = I,
q_M = ||M^(1/2) A M^(-1/2)||,
```

the contraction is governed exactly by

```text
q_M^2 = 1 - 1 / lambda_max(M).
```

For the `d`-step family

```text
A_s = sqrt(1-s) I + c_s N_d,
```

there is a sharp coupling/gap threshold.

- If `c_s = O(s)`, then `M_s` is comparable to `s^(-1) I`, its condition
  number stays bounded for fixed `d`, and `1-q_M` is of order `s`.
- If `c_s = kappa s^alpha` with `alpha < 1`, then the full-space metric
  has the lower-cost obstruction

```text
cond(M_s) >= constant * s^(-2(d-1)(1-alpha)),
1-q_M <= constant * s^(1+2(d-1)(1-alpha)).
```

For fixed coupling, the exponents are `2(d-1)` and `2d-1`. If `d` grows
logarithmically, the condition number is already super-polynomial.

## Numerical audit

The 140-decimal-digit pilot recovers the predicted exponents. In dimension
four, fixed coupling gives fitted exponents `6.000004` for conditioning and
`7.000002` for the metric gap. Gap-scale coupling gives `0.0000004` and
`1.0000005`; its endpoint condition number is about `1.947`.

A 256-bit Arb calculation certifies the exact two-step metric at one fixed-
coupling and one matched-coupling point.

## Route consequence

RH-64 remains useful as a terminal mechanism, but a global Lyapunov metric
cannot replace slow-direction removal. The viable order is:

```text
Krylov/block deflation -> localized residual family -> weighted terminal tail.
```

This is a no-go result for unlocalized full-space weighting, not for local,
block, observation-weighted, or residual-subspace metrics.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_family_conditioning_pilot.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_arb_two_step_audit.py
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf physical-family-metric-conditioning.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```

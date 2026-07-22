# RH-69: adaptive upper/lower certificate portfolio

This directory contains the sixty-ninth RH-layer paper:

> *An Adaptive Upper--Lower Certificate Portfolio for Directional Stein
> Tails*

## Main result

Every candidate records a valid upper and a nonnegative cost vector. A
candidate is safely removed only if another candidate weakly improves the
upper and every cost, with at least one strict improvement. The remaining
Pareto frontier preserves every monotone budget decision.

The selector has three statuses:

- `green`: a valid upper meets all displayed budgets;
- `red`: no upper closes and a certified projection lower bound excludes the
  displayed approximation class;
- `amber`: neither conclusion is justified.

Lower bounds are never used to reject a broader class than they prove.

## Composed architecture

```text
finite phase fusion
    -> coherence/depth lower gate
    -> block Krylov + physical covariance upper
    -> weighted terminal residual
    -> Pareto selection under horizon/depth/global-size budgets.
```

For a finite exact prefix `F_L` and any valid tail upper `U_c`,

```text
total energy <= F_L + U_c.
```

Taking the minimum over certified candidates remains valid.

## Archived physical audit

At 1% completion tolerance, the RH-60 five-scale phase selector uses
horizons `4,8,16,32,32` on both sides. At `sigma=0.01`, the RH-61 geometric
horizons are `1111` and `307`, versus selected horizon `32`, savings of
`34.7` and `9.59`.

These remain archived binary64 diagnostics, not production validated uppers.

## Other branches

- Generic nonnormal and complex-phase covariance models pass with isotropic
  covariance (`epsilon=1`).
- Exact cancellation needs `epsilon=1e-24`, physical gain `1.001027`, and
  global gain `489.96` for the selected 1.01 target.
- Exact and jittered Fourier rings are red at the displayed depth budgets.
- Phase arcs of width at most `0.3` are green for depth budget 8; wider arcs
  remain amber because only diagnostics, not analytic lower bounds, were
  archived for them.

A 256-bit Arb audit certifies one exact geometric branch, one focused
covariance branch, and one exact Fourier lower-gate branch.

## Reproduction

```bash
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/pytest -q -p no:cacheprovider
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_certificate_portfolio.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/run_arb_portfolio_audit.py
MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/make_figures.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cp main.pdf adaptive-certificate-portfolio.pdf
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/build_archive.py
PYTHONDONTWRITEBYTECODE=1 /root/math/.venv/bin/python experiments/verify_archive.py
```
